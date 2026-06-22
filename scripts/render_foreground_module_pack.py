#!/usr/bin/env python3
"""Render foreground_module_plan.json into reusable HyperFrames HTML assets."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from html import escape
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ART_LIBRARY = ROOT / "references" / "foreground_art_module_library_v2.json"
DEFAULT_MICRO_LIBRARY = ROOT / "references" / "foreground_micro_component_library_v1.json"
RUNTIME_CSS = ROOT / "assets" / "hyperframes_components" / "foreground_modules.css"
RUNTIME_JS = ROOT / "assets" / "hyperframes_components" / "foreground_modules.js"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def slug_class(selector: str) -> str:
    selector = selector.strip()
    if not selector:
        return ""
    selector = selector.split(",")[0].strip()
    selector = selector[1:] if selector.startswith(".") else selector
    return re.sub(r"[^A-Za-z0-9_-]+", "-", selector).strip("-")


def text_value(slots: dict[str, Any], *keys: str, fallback: str = "") -> str:
    for key in keys:
        if key in slots and str(slots[key]).strip():
            return str(slots[key]).strip()
    for value in slots.values():
        if str(value).strip():
            return str(value).strip()
    return fallback


def slot_html(slots: dict[str, Any]) -> str:
    items: list[str] = []
    for label, value in slots.items():
        clean_label = str(label).replace("【", "").replace("】", "")
        items.append(
            '<div class="hf-slot">'
            f'<span class="hf-slot__label">{escape(clean_label)}</span>'
            f'<span class="hf-slot__value">{escape(str(value))}</span>'
            "</div>"
        )
    return "\n".join(items)


def micro_html(component: dict[str, Any]) -> str:
    slots = component.get("text_slots") if isinstance(component.get("text_slots"), dict) else {}
    values: list[str] = []
    for label, value in slots.items():
        clean_label = str(label).replace("【", "").replace("】", "")
        values.append(
            f'<span class="hf-micro__label">{escape(clean_label)}</span>'
            f'<span class="hf-micro__value">{escape(str(value))}</span>'
        )
    return (
        f'<div class="hf-micro" data-component-id="{escape(str(component.get("component_id")))}" '
        f'data-phase="{escape(str(component.get("phase")))}" '
        f'data-anchor="{escape(str(component.get("anchor")))}">'
        + "\n".join(values)
        + "</div>"
    )


def build_anchor_groups(scene: dict[str, Any], adapter: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    planned = scene.get("micro_components") if isinstance(scene.get("micro_components"), list) else []
    anchor_map = adapter.get("anchor_map") if isinstance(adapter.get("anchor_map"), dict) else {}
    grouped: dict[str, list[dict[str, Any]]] = {}
    for component in planned:
        if not isinstance(component, dict):
            continue
        grouped.setdefault(str(component.get("anchor") or ""), []).append(component)

    anchor_records: list[dict[str, Any]] = []
    html_parts: list[str] = []
    for anchor, components in grouped.items():
        adapter_selector = str(anchor_map.get(anchor) or "")
        class_name = slug_class(adapter_selector)
        extra_class = f" {escape(class_name)}" if class_name else ""
        component_html = "\n".join(micro_html(component) for component in components)
        html_parts.append(
            f'<section class="hf-anchor{extra_class}" data-anchor="{escape(anchor)}" data-adapter-selector="{escape(adapter_selector)}">'
            f"{component_html}</section>"
        )
        anchor_records.append(
            {
                "anchor": anchor,
                "adapter_selector": adapter_selector,
                "component_ids": [str(component.get("component_id")) for component in components],
                "micro_count": len(components),
            }
        )
    return "\n".join(html_parts), anchor_records


def module_html(scene: dict[str, Any], module: dict[str, Any], adapter: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    scene_id = str(scene.get("scene_id") or "")
    module_id = str(scene.get("parent_module_id") or "")
    slots = scene.get("text_slots") if isinstance(scene.get("text_slots"), dict) else {}
    title = text_value(slots, "【主标题】", "【待验证结论】", fallback=f"{module_id} foreground")
    kicker = str(module.get("name") or module_id)
    anchor_markup, anchor_records = build_anchor_groups(scene, adapter)
    footer = (
        '<div class="hf-transition-tags">'
        f'<span>{escape(str(scene.get("transition_in")))}</span>'
        f'<span>{escape(str(scene.get("transition_out")))}</span>'
        "</div>"
    )
    html = f"""
<article class="hf-module module-{escape(module_id.lower())}" data-scene-id="{escape(scene_id)}" data-module-id="{escape(module_id)}" data-layout-mode="{escape(str(scene.get("layout_mode") or ""))}">
  <header class="hf-module__header">
    <div>
      <div class="hf-module__kicker">{escape(kicker)}</div>
      <h2 class="hf-module__title">{escape(title)}</h2>
    </div>
    {footer}
  </header>
  <main class="hf-module__body">
    <section class="hf-slot-group" data-role="parent-text-slots">
      {slot_html(slots)}
    </section>
    {anchor_markup}
  </main>
  <footer class="hf-module__footer">
    <span>{escape(scene_id)}</span>
    <span>foreground module runtime v1</span>
  </footer>
</article>
"""
    report = {
        "scene_id": scene_id,
        "parent_module_id": module_id,
        "micro_component_count": sum(record["micro_count"] for record in anchor_records),
        "anchor_count": len(anchor_records),
        "anchors": anchor_records,
        "transition_in": scene.get("transition_in"),
        "transition_out": scene.get("transition_out"),
    }
    return html, report


def render(project: Path, plan_path: Path, art_path: Path, micro_path: Path) -> dict[str, Any]:
    plan = load_json(plan_path)
    art = load_json(art_path)
    micro = load_json(micro_path)
    modules = {item["module_id"]: item for item in art.get("modules", []) if isinstance(item, dict) and item.get("module_id")}
    adapters = {item["module_id"]: item for item in micro.get("parent_module_adapters", []) if isinstance(item, dict) and item.get("module_id")}

    asset_dir = project / "assets" / "hyperframes" / "foreground_modules"
    asset_dir.mkdir(parents=True, exist_ok=True)
    css_target = asset_dir / "foreground_modules.css"
    js_target = asset_dir / "foreground_modules.js"
    shutil.copy2(RUNTIME_CSS, css_target)
    shutil.copy2(RUNTIME_JS, js_target)

    scene_reports: list[dict[str, Any]] = []
    html_parts: list[str] = []
    for scene in plan.get("scenes", []):
        if not isinstance(scene, dict):
            continue
        module_id = str(scene.get("parent_module_id") or "")
        module = modules.get(module_id, {"module_id": module_id, "name": module_id})
        adapter = adapters.get(module_id, {"module_id": module_id, "anchor_map": {}})
        markup, report = module_html(scene, module, adapter)
        html_parts.append(markup)
        scene_reports.append(report)

    aspect = str(plan.get("aspect_ratio") or "16:9")
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Foreground Module Render Pack</title>
  <link rel="stylesheet" href="../assets/hyperframes/foreground_modules/foreground_modules.css">
</head>
<body>
  <section class="hf-foreground-stage" data-aspect-ratio="{escape(aspect)}">
    {''.join(html_parts)}
  </section>
  <script src="../assets/hyperframes/foreground_modules/foreground_modules.js"></script>
</body>
</html>
"""
    html_path = project / "internal" / "foreground_module_render_pack.html"
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")

    total_micro = sum(scene["micro_component_count"] for scene in scene_reports)
    manifest = {
        "status": "rendered",
        "version": 1,
        "project": str(project),
        "source_plan": str(plan_path),
        "html": str(html_path),
        "runtime_css": str(css_target),
        "runtime_js": str(js_target),
        "aspect_ratio": aspect,
        "module_dom_count": len(scene_reports),
        "micro_dom_count": total_micro,
        "scene_reports": scene_reports,
        "render_contract": {
            "html_css_svg_gsap_ready": True,
            "real_3d_dependency": False,
            "standalone_micro_components": False,
            "parent_module_primary": True,
            "material_depth_system": "titanium_glass_layered_foreground_runtime",
            "motion_runtime": "gsap_optional_css_fallback",
        },
    }
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Render foreground module plan into HyperFrames-ready HTML/CSS/JS assets.")
    parser.add_argument("--project", required=True, help="Project folder such as outputs/demo")
    parser.add_argument("--plan", help="Plan path. Defaults to <project>/internal/foreground_module_plan.json")
    parser.add_argument("--art-library", default=str(DEFAULT_ART_LIBRARY))
    parser.add_argument("--micro-library", default=str(DEFAULT_MICRO_LIBRARY))
    parser.add_argument("--out", help="Manifest path. Defaults to <project>/internal/foreground_module_render_manifest.json")
    args = parser.parse_args()

    project = resolve_path(args.project)
    plan_path = resolve_path(args.plan) if args.plan else project / "internal" / "foreground_module_plan.json"
    out = resolve_path(args.out) if args.out else project / "internal" / "foreground_module_render_manifest.json"
    manifest = render(project, plan_path, resolve_path(args.art_library), resolve_path(args.micro_library))
    write_json(out, manifest)
    print(json.dumps({"status": manifest["status"], "html": manifest["html"], "scene_count": manifest["module_dom_count"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
