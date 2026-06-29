#!/usr/bin/env python3
"""Canonical AI video production gate and promotion entrypoint.

This script is intentionally stricter than the legacy QA runner. It blocks the
exact regression class where a project reports high-quality HyperFrames work
while the actual draft was rendered by an old local PIL/rawvideo card pipeline.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from artifact_fingerprint import verify_report_inputs, write_report_with_fingerprints


ROOT = Path(__file__).resolve().parents[1]
MAX_SECONDS_PER_VISUAL_BEAT = 5.0
STRICT_STAGES = [
    "source_research",
    "topic_candidates",
    "selected_topic",
    "copy",
    "copy_quality",
    "compliance",
    "reference_analysis",
    "style_profile",
    "background_prompt_pack",
    "storyboard_draft",
    "storyboard_production",
    "asset_manifest",
    "asset_validation",
    "audio_lock",
    "render",
    "video_technical_qa",
    "frame_review",
    "visual_approval",
    "visual_review",
    "qa_gate",
    "provider_usage_audit",
    "promote_final",
]
STAGE_OUTPUTS = {
    "copy_quality": ["script_score.json", "semantic_review.json", "content_alignment_report.json", "beginner_value_review.json"],
    "compliance": ["compliance_report.json"],
    "style_profile": ["visual_style_profile_report.json"],
    "asset_validation": ["asset_validation.json", "visual_tone_report.json"],
    "video_technical_qa": ["video_technical_qa.json"],
    "frame_review": ["frame_review_report.json"],
    "visual_review": ["visual_review.json"],
    "qa_gate": ["qa_report.json", "production_postmortem.json"],
    "provider_usage_audit": ["provider_usage_audit.json", "provider_usage_audit.md", "publish_contract.json"],
    "promote_final": ["cleanup_report.json"],
}
DESIGNED_SUPPORT_CARD_TYPES = {"designed_card", "support_card"}
DESIGNED_SUPPORT_CARD_ROLES = {"support_card", "source_card", "summary_card"}
DESIGNED_SUPPORT_CARD_PROVIDERS = {"local_original_renderer", "local_render", "official_source_card_local_render"}

FORBIDDEN_SOURCE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("legacy_pil_imagedraw_import", re.compile(r"\bfrom\s+PIL\s+import\s+.*\bImageDraw\b", re.I)),
    ("legacy_pil_imagedraw_runtime", re.compile(r"\bImageDraw\.Draw\b", re.I)),
    ("legacy_rawvideo_ffmpeg_pipe", re.compile(r"\brawvideo\b", re.I)),
    ("legacy_local_renderer_script", re.compile(r"\brender_vertical_skill_guide\.py\b", re.I)),
    ("legacy_pil_ffmpeg_renderer", re.compile(r"\bPIL\s*\+\s*FFmpeg\b", re.I)),
    ("legacy_poster_renderer", re.compile(r"\bPIL vertical poster renderer\b", re.I)),
    ("legacy_ffmpeg_generated_timeline", re.compile(r"\bffmpeg generated frame timeline\b", re.I)),
    ("legacy_card_only_claim", re.compile(r"\bcard-only\b|\btext-card slideshow\b", re.I)),
]

FORBIDDEN_REPORT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("generic_useless_module_terms", re.compile(r"useless background modules|fake framework boxes|ordinary transition", re.I)),
    ("legacy_renderer_terms", re.compile(r"PIL vertical poster renderer|PIL\s*\+\s*FFmpeg|ffmpeg generated frame timeline", re.I)),
]

SOURCE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".mjs", ".cjs"}
REPORT_SUFFIXES = {".json", ".md", ".txt"}
SKIP_DIRS = {"final", "node_modules", "__pycache__", ".git", "frame_review", "renders"}
SKIP_GENERATED_SOURCE_FILES = {
    "internal/build_project.py",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def load_json(path: Path) -> dict[str, Any]:
    if not exists(path):
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def resolve_project_path(project: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return project / path


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def remove_downstream_reports(project: Path, stage: str) -> None:
    if stage not in STRICT_STAGES:
        raise SystemExit("--rerun-from must be one of: " + ", ".join(STRICT_STAGES))
    internal = project / "internal"
    start = STRICT_STAGES.index(stage)
    for downstream in STRICT_STAGES[start:]:
        for name in STAGE_OUTPUTS.get(downstream, []):
            path = internal / name
            if path.exists() and path.is_file():
                path.unlink()


def require_strict_artifacts(project: Path) -> list[str]:
    internal = project / "internal"
    required = [
        "topic_candidates.json",
        "selected_topic.json",
        "copy_package.md",
        "copy_package.json",
        "script_score.json",
        "semantic_review.json",
        "content_alignment_report.json",
        "beginner_value_review.json",
        "compliance_report.json",
        "visual_style_profile.json",
        "storyboard.json",
        "asset_manifest.json",
        "asset_validation.json",
        "storyboard.audio_locked.json",
        "draft.mp4",
        "metadata.json",
        "frame_review_report.json",
        "visual_review.json",
    ]
    missing = [name for name in required if not exists(internal / name)]
    selected = load_json(internal / "selected_topic.json")
    if selected and any(marker in json.dumps(selected, ensure_ascii=False).lower() for marker in ["current", "hot", "热点", "热榜", "最新"]):
        for name in ["source_research.json", "source_research_validation.json"]:
            if not exists(internal / name):
                missing.append(name)
    return missing


def strict_full(project: Path, rerun_from: str | None = None) -> None:
    if rerun_from:
        remove_downstream_reports(project, rerun_from)
    missing = require_strict_artifacts(project)
    if missing:
        raise SystemExit("strict-full missing required artifacts: " + ", ".join(missing))
    run([sys.executable, "scripts/run_pipeline.py", "--project", str(project), "--mode", "qa-only"])


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def manual_frame_review_note_for(project: Path, explicit_note: str | None) -> str | None:
    if explicit_note and explicit_note.strip():
        return explicit_note.strip()
    note_path = project / "internal" / "manual_frame_review_note.txt"
    if not exists(note_path):
        return None
    note = read_text(note_path).strip()
    return note or None


def iter_candidate_files(project: Path, suffixes: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in sorted(project.rglob("*")):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        rel_parts = path.relative_to(project).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        if path.relative_to(project).as_posix() in SKIP_GENERATED_SOURCE_FILES:
            continue
        if path.name == "visual_regression_gate.json":
            continue
        files.append(path)
    return files


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def scan_patterns(project: Path, suffixes: set[str], patterns: list[tuple[str, re.Pattern[str]]]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in iter_candidate_files(project, suffixes):
        text = read_text(path)
        if not text:
            continue
        for label, pattern in patterns:
            match = pattern.search(text)
            if match:
                hits.append(
                    {
                        "file": str(path),
                        "rule": label,
                        "match": match.group(0)[:120],
                    }
                )
    return hits


def designed_support_assets(project: Path) -> list[dict[str, Any]]:
    manifest = load_json(project / "internal" / "asset_manifest.json")
    assets = manifest.get("assets")
    if not isinstance(assets, list):
        return []
    matched: list[dict[str, Any]] = []
    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            continue
        asset_type = str(asset.get("type") or "").strip()
        role = str(asset.get("role") or "").strip()
        provider = str(asset.get("provider") or "").strip()
        source_type = str(asset.get("asset_source_type") or "").strip()
        source_note = str(asset.get("source_note") or "").lower()
        if source_type != "support":
            continue
        is_designed = (
            asset_type in DESIGNED_SUPPORT_CARD_TYPES
            or role in DESIGNED_SUPPORT_CARD_ROLES
            or provider in DESIGNED_SUPPORT_CARD_PROVIDERS
            or "local original" in source_note
            or "summary card" in source_note
        )
        if not is_designed:
            continue
        raw_path = str(asset.get("path") or "").strip()
        if not raw_path:
            continue
        normalized_path = raw_path.replace("\\", "/")
        if "/support/" not in f"/{normalized_path}":
            continue
        if "background" in normalized_path.lower() or "background" in role.lower():
            continue
        matched.append(
            {
                "asset_id": str(asset.get("asset_id") or asset.get("id") or f"asset_{index}"),
                "path": raw_path,
                "resolved_path": str(resolve_project_path(project, raw_path)),
                "type": asset_type,
                "role": role,
                "provider": provider,
            }
        )
    return matched


def large_low_detail_bright_regions(image_path: Path) -> list[dict[str, Any]]:
    try:
        from PIL import Image
    except Exception:
        return []
    if not exists(image_path):
        return []
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception:
        return []

    sample_w, sample_h = 160, 90
    sample = image.resize((sample_w, sample_h))
    pixels = sample.load()
    visited = [[False for _ in range(sample_w)] for _ in range(sample_h)]
    regions: list[dict[str, Any]] = []

    def is_blank_highlight(x: int, y: int) -> bool:
        r, g, b = pixels[x, y]
        luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
        saturation = max(r, g, b) - min(r, g, b)
        return luma >= 212 and saturation <= 70

    for y in range(sample_h):
        for x in range(sample_w):
            if visited[y][x] or not is_blank_highlight(x, y):
                continue
            stack = [(x, y)]
            visited[y][x] = True
            count = 0
            min_x = max_x = x
            min_y = max_y = y
            while stack:
                cx, cy = stack.pop()
                count += 1
                min_x = min(min_x, cx)
                max_x = max(max_x, cx)
                min_y = min(min_y, cy)
                max_y = max(max_y, cy)
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if nx < 0 or ny < 0 or nx >= sample_w or ny >= sample_h or visited[ny][nx]:
                        continue
                    if is_blank_highlight(nx, ny):
                        visited[ny][nx] = True
                        stack.append((nx, ny))
            area_ratio = count / float(sample_w * sample_h)
            width_ratio = (max_x - min_x + 1) / float(sample_w)
            height_ratio = (max_y - min_y + 1) / float(sample_h)
            if area_ratio >= 0.035 and width_ratio >= 0.28 and height_ratio >= 0.075:
                regions.append(
                    {
                        "area_ratio": round(area_ratio, 4),
                        "bbox_ratio": [
                            round(min_x / sample_w, 4),
                            round(min_y / sample_h, 4),
                            round((max_x + 1) / sample_w, 4),
                            round((max_y + 1) / sample_h, 4),
                        ],
                    }
                )
    return regions


def support_card_baked_blank_report(project: Path) -> dict[str, Any]:
    checked: list[dict[str, Any]] = []
    issues: list[str] = []
    for asset in designed_support_assets(project):
        path = Path(str(asset["resolved_path"]))
        regions = large_low_detail_bright_regions(path)
        record = {
            "asset_id": asset["asset_id"],
            "path": asset["path"],
            "large_low_detail_bright_regions": regions,
        }
        checked.append(record)
        if regions:
            issues.append(
                f"{asset['asset_id']}: designed support card contains baked blank highlight/decorative block; "
                "render information modules in HTML/CSS foreground instead of image decoration"
            )
    return {
        "status": "passed" if not issues else "failed",
        "checked_assets": checked,
        "issues": issues,
    }


def hyperframes_sources(project: Path) -> list[str]:
    candidates: list[Path] = []
    for base in (project / "assets" / "hyperframes", project / "hyperframes"):
        if base.exists():
            candidates.extend(
                path
                for path in base.rglob("*")
                if path.is_file() and path.suffix in {".html", ".js", ".jsx", ".ts", ".tsx", ".json"}
            )
    root_candidates = [
        project / "index.html",
        project / "package.json",
        project / "composition.html",
    ]
    candidates.extend(path for path in root_candidates if exists(path))
    return [str(path) for path in sorted(set(candidates))]


def attr_count(text: str, attr: str) -> int:
    return len(re.findall(rf"\b{re.escape(attr)}=", text))


def plan_scene_count(plan: dict[str, Any]) -> int:
    scenes = plan.get("scenes")
    return len(scenes) if isinstance(scenes, list) else 0


def scene_micro_count(scene: dict[str, Any]) -> int:
    micro_components = scene.get("micro_components")
    if isinstance(micro_components, list):
        return len(micro_components)
    micro_ids = scene.get("micro_component_ids")
    if isinstance(micro_ids, list):
        return len(micro_ids)
    return 0


def expected_plan_micro_count(plan: dict[str, Any]) -> int:
    scenes = plan.get("scenes")
    if not isinstance(scenes, list):
        return 0
    return sum(scene_micro_count(scene) for scene in scenes if isinstance(scene, dict))


def foreground_module_gate_required(internal: Path, metadata: dict[str, Any]) -> bool:
    regression = metadata.get("regression_prevention") if isinstance(metadata.get("regression_prevention"), dict) else {}
    return (
        regression.get("useful_foreground_modules_only") is True
        or exists(internal / "foreground_module_plan.json")
        or exists(internal / "foreground_module_render_manifest.json")
        or exists(internal / "foreground_module_render_check.json")
    )


def foreground_module_visual_integrity(project: Path, sources: list[str]) -> dict[str, Any]:
    internal = project / "internal"
    issues: list[str] = []
    warnings: list[str] = []

    plan = load_json(internal / "foreground_module_plan.json")
    render_manifest = load_json(internal / "foreground_module_render_manifest.json")
    render_check = load_json(internal / "foreground_module_render_check.json")
    plan_check = load_json(internal / "foreground_module_plan_check.json")

    if not plan:
        issues.append("foreground_module_plan.json missing or empty")
    if not render_manifest:
        issues.append("foreground_module_render_manifest.json missing or empty")
    if not render_check:
        issues.append("foreground_module_render_check.json missing or empty")
    if plan_check and plan_check.get("status") != "passed":
        issues.append("foreground_module_plan_check.json.status must be passed")
    if render_check and render_check.get("status") != "passed":
        issues.append("foreground_module_render_check.json.status must be passed")
    if render_check.get("blocking_issues"):
        issues.append("foreground_module_render_check.json.blocking_issues must be empty")

    expected_scenes = plan_scene_count(plan)
    expected_micro = expected_plan_micro_count(plan)
    if expected_scenes <= 0:
        issues.append("foreground_module_plan.json must include at least one planned scene")
    if expected_micro < expected_scenes * 2 and expected_scenes > 0:
        issues.append("foreground_module_plan.json must include at least two micro-components per scene")

    manifest_html = resolve_project_path(project, str(render_manifest.get("html") or "")) if render_manifest else project / "__missing__"
    manifest_css = resolve_project_path(project, str(render_manifest.get("runtime_css") or "")) if render_manifest else project / "__missing__"
    manifest_js = resolve_project_path(project, str(render_manifest.get("runtime_js") or "")) if render_manifest else project / "__missing__"
    for label, path in (("html", manifest_html), ("runtime_css", manifest_css), ("runtime_js", manifest_js)):
        if not exists(path):
            issues.append(f"foreground render manifest {label} missing or empty: {path}")

    render_html = read_text(manifest_html) if exists(manifest_html) else ""
    render_module_count = attr_count(render_html, "data-module-id")
    render_component_count = attr_count(render_html, "data-component-id")
    if expected_scenes > 0 and render_module_count < expected_scenes:
        issues.append(
            f"foreground render pack module DOM count {render_module_count} is below planned scene count {expected_scenes}"
        )
    if expected_micro > 0 and render_component_count < expected_micro:
        issues.append(
            f"foreground render pack component DOM count {render_component_count} is below planned micro count {expected_micro}"
        )
    if "rendered in project index.html" in render_html.lower():
        issues.append("foreground_module_render_pack.html is a placeholder, not a real module render pack")

    scene_reports = render_manifest.get("scene_reports") if isinstance(render_manifest.get("scene_reports"), list) else []
    if expected_scenes > 0 and len(scene_reports) != expected_scenes:
        issues.append("foreground_module_render_manifest.scene_reports must match planned scene count")
    contract = render_manifest.get("render_contract") if isinstance(render_manifest.get("render_contract"), dict) else {}
    if contract.get("parent_module_primary") is not True:
        issues.append("foreground_module_render_manifest.render_contract.parent_module_primary must be true")

    source_text = "\n".join(read_text(Path(path)) for path in sources)
    source_module_count = attr_count(source_text, "data-module-id")
    source_component_count = attr_count(source_text, "data-component-id")
    runtime_references = len(re.findall(r"foreground_modules\.(?:js|css)", source_text))
    stage_markers = source_text.count("hf-foreground-stage")
    if expected_scenes > 0 and source_module_count < expected_scenes:
        issues.append(
            "final HyperFrames source must mount real foreground modules; "
            f"found {source_module_count} data-module-id markers for {expected_scenes} planned scenes"
        )
    if expected_micro > 0 and source_component_count < expected_micro:
        issues.append(
            "final HyperFrames source must mount real foreground micro-components; "
            f"found {source_component_count} data-component-id markers for {expected_micro} planned components"
        )
    if runtime_references == 0 and stage_markers == 0:
        issues.append("final HyperFrames source does not reference the foreground module runtime or stage")

    return {
        "status": "passed" if not issues else "failed",
        "blocking_issues": issues,
        "warnings": warnings,
        "signals": {
            "expected_scene_count": expected_scenes,
            "expected_micro_count": expected_micro,
            "render_pack_module_dom_count": render_module_count,
            "render_pack_component_dom_count": render_component_count,
            "final_source_module_dom_count": source_module_count,
            "final_source_component_dom_count": source_component_count,
            "final_source_runtime_reference_count": runtime_references,
            "final_source_stage_marker_count": stage_markers,
        },
    }


def extract_frame(video: Path, frame_number: int, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        "-i",
        str(video),
        "-vf",
        f"select=eq(n\\,{frame_number})",
        "-frames:v",
        "1",
        str(out),
    ]
    subprocess.run(command, check=True)


def image_rms(path_a: Path, path_b: Path) -> float | None:
    try:
        from PIL import Image, ImageChops, ImageStat
    except ImportError:
        return None
    if not exists(path_a) or not exists(path_b):
        return None
    with Image.open(path_a) as image_a, Image.open(path_b) as image_b:
        a = image_a.convert("RGB")
        b = image_b.convert("RGB").resize(a.size)
        diff = ImageChops.difference(a, b)
        stat = ImageStat.Stat(diff)
        return math.sqrt(sum(value * value for value in stat.rms) / len(stat.rms))


def ensure_first_frame_evidence(project: Path, issues: list[str]) -> dict[str, Any]:
    internal = project / "internal"
    video = internal / "draft.mp4"
    cover = internal / "first_frame_cover.png"
    actual0 = internal / "actual_frame_000_cover.png"
    actual1 = internal / "actual_frame_001_after_cover.png"
    metrics: dict[str, Any] = {
        "expected_cover": str(cover),
        "actual_frame_000_cover": str(actual0),
        "actual_frame_001_after_cover": str(actual1),
    }

    if not exists(video):
        issues.append("internal/draft.mp4 missing; cannot verify real first-frame cover")
        return metrics
    if not exists(cover):
        issues.append("internal/first_frame_cover.png missing; cover must be a real designed frame, not a grab")
        return metrics

    for frame_number, out in ((0, actual0), (1, actual1)):
        if exists(out):
            continue
        try:
            extract_frame(video, frame_number, out)
        except (OSError, subprocess.CalledProcessError) as exc:
            issues.append(f"failed to extract actual frame {frame_number}: {exc}")

    cover_diff = image_rms(cover, actual0)
    frame01_diff = image_rms(actual0, actual1)
    metrics["cover_to_frame0_rms"] = cover_diff
    metrics["frame0_to_frame1_rms"] = frame01_diff
    metrics["cover_match_threshold_rms"] = 14.0
    metrics["frame1_return_threshold_rms"] = 4.0

    if cover_diff is None:
        issues.append("Pillow unavailable or cover/frame0 missing; cannot verify first-frame cover pixels")
    elif cover_diff > 14.0:
        issues.append(f"frame 0 does not match first_frame_cover.png (rms={cover_diff:.2f})")

    if frame01_diff is None:
        issues.append("actual frame 1 missing; cannot prove cover lasts exactly one frame")
    elif frame01_diff < 4.0:
        issues.append(f"frame 1 is still too close to cover frame (rms={frame01_diff:.2f}); cover must last one frame only")

    return metrics


def require_report_passed(internal: Path, name: str, issues: list[str]) -> dict[str, Any]:
    path = internal / name
    report = load_json(path)
    if not report:
        issues.append(f"{name} missing or empty")
        return {}
    if report.get("status") != "passed":
        issues.append(f"{name}.status must be passed")
    if report.get("blocking_issues"):
        issues.append(f"{name}.blocking_issues must be empty")
    return report


def layout_motion_contract_required(internal: Path) -> bool:
    selection = load_json(internal / "fixed_template_selection.json")
    motion_contract = selection.get("motion_layout_contract") if isinstance(selection.get("motion_layout_contract"), dict) else {}
    inheritance = selection.get("inheritance_contract") if isinstance(selection.get("inheritance_contract"), dict) else {}
    return (
        bool(motion_contract)
        or inheritance.get("layout_manifest_required") is True
        or inheritance.get("forbidden_low_grade_effects_blocking") is True
    )


def metadata_text(metadata: dict[str, Any]) -> str:
    return json.dumps(metadata, ensure_ascii=False).lower()


def png_sequence_route_required(internal: Path, metadata: dict[str, Any]) -> bool:
    if (internal / "hf_frames").exists():
        return True
    text = metadata_text(metadata)
    if "png sequence" in text or "png-sequence" in text or "png_sequence" in text:
        return True
    selection = load_json(internal / "fixed_template_selection.json")
    scene_motion = selection.get("scene_motion_templates") if isinstance(selection.get("scene_motion_templates"), dict) else {}
    ffmpeg_route = scene_motion.get("ffmpeg_route_template") if isinstance(scene_motion.get("ffmpeg_route_template"), dict) else {}
    route = ffmpeg_route.get("route") if isinstance(ffmpeg_route.get("route"), list) else []
    return "hyperframes_png_sequence" in route


def stable_render_profile_uses_project_directory(report: dict[str, Any], project: Path, issues: list[str]) -> None:
    if report.get("render_target") != "project_directory":
        issues.append("hyperframes_render_profile.render_target must be project_directory")

    command_cwd = str(report.get("command_cwd") or "").strip()
    if not command_cwd:
        issues.append("hyperframes_render_profile.command_cwd must point to the project directory")
    else:
        try:
            if Path(command_cwd) != project:
                issues.append("hyperframes_render_profile.command_cwd must match the project directory")
        except TypeError:
            issues.append("hyperframes_render_profile.command_cwd must be a valid path")

    command = report.get("command_template")
    if not isinstance(command, list) or not command:
        issues.append("hyperframes_render_profile.command_template is required")
        return

    tokens = [str(item) for item in command]
    try:
        render_index = tokens.index("render")
    except ValueError:
        issues.append("hyperframes_render_profile.command_template must call hyperframes render")
        return

    positional_targets: list[str] = []
    for token in tokens[render_index + 1 :]:
        if token.startswith("-"):
            break
        positional_targets.append(token)
    html_targets = [
        token
        for token in positional_targets
        if token.endswith(".html") or token in {"index.html", "assets/hyperframes/index.html", "composition.html"}
    ]
    if html_targets:
        issues.append(
            "hyperframes_render_profile must render from the project directory, not an HTML entry file: "
            + ", ".join(html_targets)
        )


def ensure_stable_render_profile(internal: Path, metadata: dict[str, Any], issues: list[str]) -> dict[str, Any]:
    if not png_sequence_route_required(internal, metadata):
        return {"status": "not_required", "reason": "project does not declare the HyperFrames PNG sequence route"}

    project = internal.parent
    report = load_json(internal / "hyperframes_render_profile.json")
    if not report:
        issues.append("hyperframes_render_profile.json missing or empty for HyperFrames PNG sequence route")
        return {"status": "missing"}

    if report.get("status") != "passed":
        issues.append("hyperframes_render_profile.json.status must be passed")
    if report.get("blocking_issues"):
        issues.append("hyperframes_render_profile.json.blocking_issues must be empty")
    stable_render_profile_uses_project_directory(report, project, issues)

    profile = report.get("profile") if isinstance(report.get("profile"), dict) else report
    if str(profile.get("render_mode") or "") != "png_sequence":
        issues.append("hyperframes_render_profile.profile.render_mode must be png_sequence")
    if str(profile.get("render_target") or "") != "project_directory":
        issues.append("hyperframes_render_profile.profile.render_target must be project_directory")
    try:
        worker_count = int(profile.get("worker_count") or 0)
        max_worker_count = int(profile.get("max_worker_count") or worker_count)
    except Exception:
        worker_count = 0
        max_worker_count = 0
    if worker_count < 1 or worker_count > 1 or max_worker_count > 1:
        issues.append("hyperframes_render_profile must use the serial stable PNG render worker route")
    try:
        protocol_timeout = int(profile.get("protocol_timeout_ms") or 0)
    except Exception:
        protocol_timeout = 0
    if protocol_timeout < 900000:
        issues.append("hyperframes_render_profile.profile.protocol_timeout_ms must be at least 900000")
    return report


def ensure_leading_frame_repair(internal: Path, metadata: dict[str, Any], issues: list[str]) -> dict[str, Any]:
    if not png_sequence_route_required(internal, metadata):
        return {"status": "not_required", "reason": "project does not declare the HyperFrames PNG sequence route"}

    report = load_json(internal / "leading_frame_repair_report.json")
    if not report:
        issues.append("leading_frame_repair_report.json missing or empty for HyperFrames PNG sequence route")
        return {"status": "missing"}
    if report.get("status") != "passed":
        issues.append("leading_frame_repair_report.json.status must be passed")
    if report.get("issues"):
        issues.append("leading_frame_repair_report.json.issues must be empty")
    contract = report.get("contract") if isinstance(report.get("contract"), dict) else {}
    if contract.get("cover_slot_preserved") is not True:
        issues.append("leading_frame_repair_report.contract.cover_slot_preserved must be true")
    if contract.get("frame_one_returns_to_main_timeline") is not True:
        issues.append("leading_frame_repair_report.contract.frame_one_returns_to_main_timeline must be true")
    if not isinstance(report.get("first_content_frame"), dict):
        issues.append("leading_frame_repair_report.first_content_frame is required")
    return report


def audio_lock_required(metadata: dict[str, Any]) -> bool:
    if not metadata:
        return False
    if "tts_speed" in metadata or isinstance(metadata.get("voice"), dict):
        return True
    quality_spec = metadata.get("quality_spec") if isinstance(metadata.get("quality_spec"), dict) else {}
    production_stack = metadata.get("production_stack") if isinstance(metadata.get("production_stack"), dict) else {}
    return bool(
        str(quality_spec.get("narration_continuity_policy") or "").strip()
        or str(quality_spec.get("timeline_contract_ref") or "").strip()
        or str(production_stack.get("audio") or "").strip()
    )


def scene_audio_durations(lock: dict[str, Any]) -> dict[str, float]:
    audio_lock = lock.get("audio_lock") if isinstance(lock.get("audio_lock"), dict) else {}
    scene_audio = audio_lock.get("scene_audio") if isinstance(audio_lock.get("scene_audio"), list) else []
    durations: dict[str, float] = {}
    for item in scene_audio:
        if not isinstance(item, dict):
            continue
        scene_id = str(item.get("scene_id") or "").strip()
        if not scene_id:
            continue
        try:
            start = float(item.get("start") or 0)
            end = float(item.get("end") or 0)
            duration = float(item.get("duration") or max(0.0, end - start))
        except Exception:
            continue
        if duration > 0:
            durations[scene_id] = duration
    return durations


def count_visual_beats(scene: dict[str, Any]) -> int:
    count = 0
    for key in ("beat_map", "visual_beats", "beat_points", "timeline_beats", "micro_beats"):
        value = scene.get(key)
        if isinstance(value, list):
            count = max(count, len([item for item in value if isinstance(item, dict) or str(item).strip()]))
    return count


def ensure_audio_locked_visual_beats(internal: Path, metadata: dict[str, Any], issues: list[str]) -> dict[str, Any]:
    if not audio_lock_required(metadata):
        return {"status": "not_required", "reason": "metadata does not declare narration/TTS"}

    lock = load_json(internal / "storyboard.audio_locked.json")
    if not lock:
        issues.append("storyboard.audio_locked.json missing or empty for narrated video")
        return {"status": "missing"}

    scenes = lock.get("scenes") if isinstance(lock.get("scenes"), list) else []
    if not scenes:
        issues.append("storyboard.audio_locked.json.scenes must be a non-empty array")
        return {"status": "failed", "scene_reports": []}

    duration_by_scene = scene_audio_durations(lock)
    scene_reports: list[dict[str, Any]] = []
    beat_issues: list[str] = []
    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            continue
        scene_id = str(scene.get("scene_id") or f"S{index:02d}")
        try:
            duration = float(scene.get("duration_target") or duration_by_scene.get(scene_id) or 0)
        except Exception:
            duration = 0.0
        required_beats = max(1, math.ceil(duration / MAX_SECONDS_PER_VISUAL_BEAT)) if duration > 0 else 1
        beat_count = count_visual_beats(scene)
        passed = beat_count >= required_beats
        if not passed:
            beat_issues.append(
                f"{scene_id} has {beat_count} visual beats for {duration:.2f}s locked audio; needs at least {required_beats}"
            )
        scene_reports.append(
            {
                "scene_id": scene_id,
                "duration_sec": round(duration, 3),
                "visual_beat_count": beat_count,
                "required_visual_beats": required_beats,
                "max_seconds_per_visual_beat": MAX_SECONDS_PER_VISUAL_BEAT,
                "passed": passed,
            }
        )

    issues.extend(beat_issues)
    return {
        "status": "passed" if not beat_issues else "failed",
        "max_seconds_per_visual_beat": MAX_SECONDS_PER_VISUAL_BEAT,
        "scene_reports": scene_reports,
        "blocking_issues": beat_issues,
    }


def visual_regression_gate(project: Path, out: Path | None = None) -> dict[str, Any]:
    internal = project / "internal"
    issues: list[str] = []
    warnings: list[str] = []

    legacy_source_hits = scan_patterns(project, SOURCE_SUFFIXES, FORBIDDEN_SOURCE_PATTERNS)
    legacy_report_hits = scan_patterns(project, REPORT_SUFFIXES, FORBIDDEN_REPORT_PATTERNS)
    if legacy_source_hits:
        issues.append("legacy renderer/source terms detected; remove old PIL/rawvideo/card renderer from this project")
    if legacy_report_hits:
        warnings.append("legacy warning terms detected in reports; confirm they are not describing the active runtime")

    sources = hyperframes_sources(project)
    if not sources:
        issues.append("HyperFrames source is missing; publish-ready AI videos must keep the final timeline source")

    metadata = load_json(internal / "metadata.json")
    stable_render_profile = ensure_stable_render_profile(internal, metadata, issues)
    leading_frame_repair = ensure_leading_frame_repair(internal, metadata, issues)
    audio_locked_visual_beats = ensure_audio_locked_visual_beats(internal, metadata, issues)
    support_card_blank_blocks = support_card_baked_blank_report(project)
    issues.extend(support_card_blank_blocks["issues"])
    first_frame = ensure_first_frame_evidence(project, issues)
    visual_review = require_report_passed(internal, "visual_review.json", issues)
    frame_review = require_report_passed(internal, "frame_review_report.json", issues)
    if frame_review:
        issues.extend(
            f"frame_review_report.json stale: {issue}"
            for issue in verify_report_inputs(frame_review, [internal / "draft.mp4"])
        )
    foreground_integrity: dict[str, Any] = {"status": "not_required"}
    if foreground_module_gate_required(internal, metadata):
        foreground_integrity = foreground_module_visual_integrity(project, sources)
        issues.extend(foreground_integrity.get("blocking_issues", []))
        warnings.extend(foreground_integrity.get("warnings", []))
    layout_motion_report: dict[str, Any] = {}
    if layout_motion_contract_required(internal):
        layout_motion_report = require_report_passed(internal, "layout_motion_contract_report.json", issues)

    production_stack = metadata.get("production_stack") if isinstance(metadata.get("production_stack"), dict) else {}
    runtime_text = json.dumps(production_stack, ensure_ascii=False)
    if runtime_text and re.search(r"PIL|rawvideo|ffmpeg generated frame timeline|card-only", runtime_text, re.I):
        issues.append("metadata.production_stack declares a legacy low-grade renderer")

    required_motion_flags = {
        "advanced_transitions_only": "advanced transition policy must be recorded",
        "voice_safe_sfx": "dynamic icon/status SFX must be recorded as voice-safe",
    }
    regression_contract = metadata.get("regression_prevention") if isinstance(metadata.get("regression_prevention"), dict) else {}
    for key, message in required_motion_flags.items():
        if regression_contract.get(key) is not True:
            issues.append(f"metadata.regression_prevention.{key} missing; {message}")
    useful_foreground_recorded = (
        regression_contract.get("useful_foreground_modules_only") is True
        or regression_contract.get("no_useless_background_modules") is True
    )
    if not useful_foreground_recorded:
        issues.append(
            "metadata.regression_prevention.useful_foreground_modules_only missing; "
            "foreground modules must record current-scene information jobs"
        )

    checks = {
        "no_legacy_renderer_source": not legacy_source_hits,
        "hyperframes_source_present": bool(sources),
        "first_frame_cover_matches": first_frame.get("cover_to_frame0_rms") is not None
        and float(first_frame["cover_to_frame0_rms"]) <= 14.0,
        "frame1_returns_to_main_timeline": first_frame.get("frame0_to_frame1_rms") is not None
        and float(first_frame["frame0_to_frame1_rms"]) >= 4.0,
        "visual_review_passed": bool(visual_review) and visual_review.get("status") == "passed",
        "frame_review_passed": bool(frame_review) and frame_review.get("status") == "passed",
        "layout_motion_contract_passed": not layout_motion_contract_required(internal)
        or (bool(layout_motion_report) and layout_motion_report.get("status") == "passed"),
        "stable_png_render_profile_passed": stable_render_profile.get("status") in {"passed", "not_required"},
        "leading_frame_repair_passed": leading_frame_repair.get("status") in {"passed", "not_required"},
        "audio_locked_visual_beats_passed": audio_locked_visual_beats.get("status") in {"passed", "not_required"},
        "support_cards_no_baked_blank_blocks": support_card_blank_blocks.get("status") == "passed",
        "foreground_module_visual_integrity_passed": foreground_integrity.get("status") in {"passed", "not_required"},
    }

    report = {
        "status": "passed" if not issues else "failed",
        "verified_at": now_iso(),
        "project": str(project),
        "checks": checks,
        "issues": issues,
        "warnings": warnings,
        "legacy_source_hits": legacy_source_hits,
        "legacy_report_hits": legacy_report_hits,
        "hyperframes_sources": sources[:80],
        "first_frame": first_frame,
        "stable_render_profile": stable_render_profile,
        "leading_frame_repair": leading_frame_repair,
        "audio_locked_visual_beats": audio_locked_visual_beats,
        "support_card_blank_blocks": support_card_blank_blocks,
        "foreground_module_visual_integrity": foreground_integrity,
    }
    write_report_with_fingerprints(
        report,
        [
            path
            for path in [
                internal / "draft.mp4",
                internal / "metadata.json",
                internal / "visual_review.json",
                internal / "frame_review_report.json",
                internal / "first_frame_cover.png",
                internal / "actual_frame_000_cover.png",
                internal / "actual_frame_001_after_cover.png",
            ]
            if exists(path)
        ],
    )
    if out is None:
        out = internal / "visual_regression_gate.json"
    write_json(out, report)
    return report


def publish_evidence_preflight(project: Path, out: Path | None = None) -> dict[str, Any]:
    internal = project / "internal"
    issues: list[str] = []
    required_reports = {
        "provider_usage_audit": internal / "provider_usage_audit.json",
        "on_screen_and_publish_text_compliance_report": internal / "on_screen_and_publish_text_compliance_report.json",
        "publish_cover_report": internal / "publish_cover_report.json",
        "qingdou_keyword_check": internal / "qingdou_keyword_check.json",
    }
    reports: dict[str, Any] = {}
    for name, path in required_reports.items():
        report = load_json(path)
        reports[name] = {
            "path": str(path),
            "status": str(report.get("status") or "missing") if report else "missing",
        }
        if not report:
            if name == "qingdou_keyword_check":
                issues.append(
                    f"{name} missing or empty: {path}; run scripts/qingdou_browser_check.py --project {project} --mode prepare"
                )
            else:
                issues.append(f"{name} missing or empty: {path}")
            continue
        if name == "qingdou_keyword_check":
            if report.get("status") not in {"passed", "user_override_accepted"}:
                issues.append("qingdou_keyword_check.status must be passed or user_override_accepted")
        elif report.get("status") != "passed":
            issues.append(f"{name}.status must be passed")
        if name == "provider_usage_audit" and report.get("issues"):
            issues.append("provider_usage_audit.issues must be empty")
        if report.get("blocking_issues"):
            issues.append(f"{name}.blocking_issues must be empty")

    cover = load_json(required_reports["publish_cover_report"])
    cover_checks = cover.get("checks") if isinstance(cover.get("checks"), dict) else {}
    if cover and cover_checks.get("dynamic_text_overlay_used") is not True:
        issues.append("publish_cover_report.checks.dynamic_text_overlay_used must be true")

    text_report = load_json(required_reports["on_screen_and_publish_text_compliance_report"])
    if text_report:
        checked_files = text_report.get("checked_files")
        if not isinstance(checked_files, list) or not any("publish_cover_text.txt" in str(item) for item in checked_files):
            issues.append("on_screen_and_publish_text_compliance_report.checked_files must include publish_cover_text.txt")

    report = {
        "status": "passed" if not issues else "failed",
        "verified_at": now_iso(),
        "project": str(project),
        "reports": reports,
        "issues": issues,
    }
    if out is None:
        out = internal / "publish_evidence_preflight.json"
    write_json(out, report)
    return report


def promote_after_visual_gate(project: Path) -> None:
    internal = project / "internal"
    cover_report = internal / "publish_cover_report.json"
    if not exists(cover_report):
        raise SystemExit(
            "missing publish_cover_report.json. Run scripts/select_fixed_cover_template.py before render/promote; "
            "do not auto-generate the old programmatic cover preview."
        )

    text_paths: list[str] = []
    for name in ("render_text_manifest.json", "publish_cover_text.txt", "publish_copy.txt"):
        path = internal / name
        if exists(path):
            text_paths.append(str(path))
    if text_paths:
        run(
            [
                sys.executable,
                "scripts/check_public_copy.py",
                *text_paths,
                "--out",
                str(internal / "on_screen_and_publish_text_compliance_report.json"),
            ]
        )

    run(
        [
            sys.executable,
            "scripts/audit_provider_usage.py",
            "--project",
            str(project),
            "--phase",
            "final",
            "--out",
            str(internal / "provider_usage_audit.json"),
            "--md-out",
            str(internal / "provider_usage_audit.md"),
        ]
    )
    evidence_preflight = publish_evidence_preflight(project)
    if evidence_preflight["status"] != "passed":
        raise SystemExit(
            "publish evidence preflight failed: "
            + "; ".join(str(item) for item in evidence_preflight.get("issues", []))
        )
    contract = internal / "publish_contract.json"
    run([sys.executable, "scripts/build_publish_contract.py", "--project", str(project), "--out", str(contract)])
    run([sys.executable, "scripts/pre_publish_gate.py", "--contract", str(contract)])
    run([sys.executable, "scripts/promote_final.py", "--project", str(project), "--contract", str(contract)])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Canonical AI video entrypoint: QA, visual regression gate, contract gate, and optional final promotion."
    )
    parser.add_argument("--project", help="outputs/<date-topic> project path")
    parser.add_argument(
        "--mode",
        choices=["qa-only", "qa-promote", "promote", "visual-gate", "strict-full", "golden"],
        default="qa-only",
    )
    parser.add_argument("--out", help="Output path for visual-gate mode; defaults to <project>/internal/visual_regression_gate.json")
    parser.add_argument("--rerun-from", choices=STRICT_STAGES)
    parser.add_argument("--enable-vertical-adaptation", action="store_true")
    parser.add_argument(
        "--manual-frame-review-note",
        help="Deprecated. Use scripts/approve_frame_review.py.",
    )
    args = parser.parse_args()

    if args.mode == "golden":
        run([sys.executable, "scripts/check_golden_project.py"])
        return 0
    if not args.project:
        parser.error("--project is required unless --mode golden")

    project = Path(args.project)
    if args.mode == "strict-full":
        strict_full(project, args.rerun_from)
        return 0
    if args.mode in {"qa-only", "qa-promote"}:
        qa_cmd = [sys.executable, "scripts/run_pipeline.py", "--project", str(project), "--mode", "qa-only"]
        run(qa_cmd)

    report = visual_regression_gate(project, Path(args.out) if args.out else None)
    print(json.dumps({"status": report["status"], "issues": report["issues"], "warnings": report["warnings"]}, ensure_ascii=False, indent=2))
    if report["status"] != "passed":
        return 1

    if args.mode in {"qa-promote", "promote"}:
        promote_after_visual_gate(project)
        if args.enable_vertical_adaptation:
            run([sys.executable, "scripts/adapt_douyin_vertical.py", "--project", str(project), "--enable-vertical-adaptation"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
