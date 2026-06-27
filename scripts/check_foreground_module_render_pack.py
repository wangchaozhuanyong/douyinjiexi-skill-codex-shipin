#!/usr/bin/env python3
"""Validate generated foreground module HyperFrames render pack assets."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BANNED_RENDER_TERMS = [
    "ordinary fade",
    "plain fade",
    "simple slide",
    "diagonal line sweep",
    "diagonal sweep",
    "普通淡入淡出",
    "普通左右滑入",
    "斜线扫光",
    "斜线扫描",
]
MAX_BACKGROUND_FILL_ALPHA = 0.34
MAX_GLASS_VAR_ALPHA = {
    "--hf-fg-panel": 0.18,
    "--hf-fg-panel-2": 0.28,
    "--hf-glass-shell": 0.18,
    "--hf-glass-reading": 0.34,
    "--hf-glass-proof": 0.34,
}


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def count_attr(html: str, attr: str) -> int:
    return len(re.findall(rf"\b{re.escape(attr)}=", html))


def rgba_alphas(value: str) -> list[float]:
    alphas: list[float] = []
    for match in re.finditer(r"rgba\([^)]*,\s*([0-9]*\.?[0-9]+)\s*\)", value, flags=re.I):
        try:
            alphas.append(float(match.group(1)))
        except ValueError:
            continue
    return alphas


def css_block(css: str, selector: str) -> str:
    match = re.search(rf"{re.escape(selector)}\s*\{{(?P<body>.*?)\n\}}", css, flags=re.S)
    return match.group("body") if match else ""


def validate_glass_transparency(css: str, contract: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    issues: list[str] = []
    signals: dict[str, Any] = {
        "profile": "",
        "stage_background_transparent": False,
        "backdrop_filter_present": False,
        "max_background_fill_alpha": 0.0,
        "checked_alpha_variable_count": 0,
    }

    glass = contract.get("glass_transparency") if isinstance(contract.get("glass_transparency"), dict) else {}
    signals["profile"] = str(glass.get("profile") or "")
    if glass.get("profile") != "glass_transparency_v2":
        issues.append("foreground render contract glass_transparency.profile must be glass_transparency_v2")
    for key in ("dynamic_background_visible", "solid_panel_forbidden", "backdrop_filter_required"):
        if glass.get(key) is not True:
            issues.append(f"foreground render contract glass_transparency.{key} must be true")

    stage = css_block(css, ".hf-foreground-stage")
    if "background: transparent" in stage:
        signals["stage_background_transparent"] = True
    else:
        issues.append("foreground stage background must be transparent so dynamic MP4 remains visible")
    if "linear-gradient" in stage or "radial-gradient" in stage:
        issues.append("foreground stage must not paint a full-frame gradient over the dynamic background")

    signals["backdrop_filter_present"] = "backdrop-filter" in css or "-webkit-backdrop-filter" in css
    if not signals["backdrop_filter_present"]:
        issues.append("foreground glass runtime must include backdrop-filter for local readability")

    checked_vars = 0
    for name, max_alpha in MAX_GLASS_VAR_ALPHA.items():
        match = re.search(rf"{re.escape(name)}\s*:\s*(rgba\([^;]+\))", css, flags=re.I)
        if not match:
            issues.append(f"foreground glass CSS variable missing: {name}")
            continue
        checked_vars += 1
        values = rgba_alphas(match.group(1))
        if not values:
            issues.append(f"foreground glass CSS variable {name} must use rgba with alpha")
            continue
        alpha = values[-1]
        signals[f"{name}_alpha"] = alpha
        if alpha > max_alpha:
            issues.append(f"foreground glass CSS variable {name} alpha {alpha:.2f} exceeds {max_alpha:.2f}")
    signals["checked_alpha_variable_count"] = checked_vars

    high_fill_lines: list[str] = []
    for raw_line in css.splitlines():
        line = raw_line.strip()
        if not line or "background" not in line or "rgba(" not in line:
            continue
        line_alphas = rgba_alphas(line)
        if not line_alphas:
            continue
        line_max = max(line_alphas)
        signals["max_background_fill_alpha"] = max(float(signals["max_background_fill_alpha"]), line_max)
        if line_max > MAX_BACKGROUND_FILL_ALPHA:
            high_fill_lines.append(line)
    if high_fill_lines:
        preview = "; ".join(high_fill_lines[:4])
        issues.append(f"foreground glass runtime has opaque background fills above {MAX_BACKGROUND_FILL_ALPHA:.2f}: {preview}")

    return issues, signals


def validate(project: Path, manifest_path: Path, plan_path: Path, plan_check_path: Path) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    if not exists(manifest_path):
        issues.append(f"foreground module render manifest missing: {manifest_path}")
        return {"status": "failed", "blocking_issues": issues, "warnings": warnings, "signals": {}}
    if not exists(plan_path):
        issues.append(f"foreground module plan missing: {plan_path}")
        return {"status": "failed", "blocking_issues": issues, "warnings": warnings, "signals": {}}

    manifest = load_json(manifest_path)
    plan = load_json(plan_path)
    plan_check = load_json(plan_check_path) if exists(plan_check_path) else {}
    if plan_check.get("status") != "passed":
        issues.append("foreground_module_plan_check.json must pass before render pack can pass")

    html_path = resolve_path(str(manifest.get("html") or ""))
    css_path = resolve_path(str(manifest.get("runtime_css") or ""))
    js_path = resolve_path(str(manifest.get("runtime_js") or ""))
    for label, path in [("html", html_path), ("runtime_css", css_path), ("runtime_js", js_path)]:
        if not exists(path):
            issues.append(f"foreground render {label} missing or empty: {path}")

    html = html_path.read_text(encoding="utf-8") if exists(html_path) else ""
    css = css_path.read_text(encoding="utf-8") if exists(css_path) else ""
    js = js_path.read_text(encoding="utf-8") if exists(js_path) else ""
    combined = "\n".join([html, css, js])
    for term in BANNED_RENDER_TERMS:
        if term in combined:
            issues.append(f"foreground render pack contains banned low-grade motion term: {term}")

    scenes = plan.get("scenes") if isinstance(plan.get("scenes"), list) else []
    expected_scene_ids = [str(scene.get("scene_id") or "") for scene in scenes if isinstance(scene, dict)]
    expected_micro_count = sum(
        len(scene.get("micro_components") or [])
        for scene in scenes
        if isinstance(scene, dict) and isinstance(scene.get("micro_components"), list)
    )
    module_dom_count = count_attr(html, "data-module-id")
    micro_dom_count = count_attr(html, "data-component-id")
    if module_dom_count != len(expected_scene_ids):
        issues.append(f"module DOM count {module_dom_count} does not match plan scene count {len(expected_scene_ids)}")
    if micro_dom_count != expected_micro_count:
        issues.append(f"micro DOM count {micro_dom_count} does not match plan micro count {expected_micro_count}")
    for scene_id in expected_scene_ids:
        if f'data-scene-id="{scene_id}"' not in html:
            issues.append(f"render pack missing scene DOM for {scene_id}")

    manifest_scenes = manifest.get("scene_reports") if isinstance(manifest.get("scene_reports"), list) else []
    if len(manifest_scenes) != len(expected_scene_ids):
        issues.append("foreground render manifest scene_reports must match plan scenes")
    for scene_report in manifest_scenes:
        if not isinstance(scene_report, dict):
            continue
        if int(scene_report.get("micro_component_count") or 0) < 2:
            issues.append(f"{scene_report.get('scene_id')} must render at least 2 micro-components")
        for anchor in scene_report.get("anchors") or []:
            if isinstance(anchor, dict) and not anchor.get("adapter_selector"):
                warnings.append(f"{scene_report.get('scene_id')} anchor {anchor.get('anchor')} has no adapter selector")

    contract = manifest.get("render_contract") if isinstance(manifest.get("render_contract"), dict) else {}
    required_contract = {
        "html_css_svg_gsap_ready": True,
        "real_3d_dependency": False,
        "standalone_micro_components": False,
        "parent_module_primary": True,
    }
    for key, expected in required_contract.items():
        if contract.get(key) is not expected:
            issues.append(f"foreground render contract {key} must be {expected}")
    glass_issues, glass_signals = validate_glass_transparency(css, contract)
    issues.extend(glass_issues)

    return {
        "status": "passed" if not issues else "failed",
        "project": str(project),
        "manifest": str(manifest_path),
        "blocking_issues": issues,
        "warnings": warnings,
        "signals": {
            "plan_scene_count": len(expected_scene_ids),
            "module_dom_count": module_dom_count,
            "expected_micro_count": expected_micro_count,
            "micro_dom_count": micro_dom_count,
            "html": str(html_path),
            "runtime_css": str(css_path),
            "runtime_js": str(js_path),
            "glass_transparency": glass_signals,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate foreground module render pack.")
    parser.add_argument("--project", required=True, help="Project folder such as outputs/demo")
    parser.add_argument("--manifest", help="Defaults to <project>/internal/foreground_module_render_manifest.json")
    parser.add_argument("--plan", help="Defaults to <project>/internal/foreground_module_plan.json")
    parser.add_argument("--plan-check", help="Defaults to <project>/internal/foreground_module_plan_check.json")
    parser.add_argument("--out", help="Defaults to <project>/internal/foreground_module_render_check.json")
    args = parser.parse_args()

    project = resolve_path(args.project)
    manifest = resolve_path(args.manifest) if args.manifest else project / "internal" / "foreground_module_render_manifest.json"
    plan = resolve_path(args.plan) if args.plan else project / "internal" / "foreground_module_plan.json"
    plan_check = resolve_path(args.plan_check) if args.plan_check else project / "internal" / "foreground_module_plan_check.json"
    out = resolve_path(args.out) if args.out else project / "internal" / "foreground_module_render_check.json"
    report = validate(project, manifest, plan, plan_check)
    write_json(out, report)
    print(json.dumps({"status": report["status"], "issues": report["blocking_issues"], "warnings": report["warnings"]}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
