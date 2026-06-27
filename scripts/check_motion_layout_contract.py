#!/usr/bin/env python3
"""Check premium motion recipes and measured layout safety for AI videos."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_FORBIDDEN_EFFECTS = [
    "diagonal line sweep",
    "diagonal sweep",
    "diagonal scan",
    "斜线扫光",
    "斜线扫描",
    "random horizontal light streak",
    "random light streak",
    "横向小光条乱跑",
    "plain fade",
    "ordinary fade",
    "普通淡入淡出",
    "simple slide",
    "ordinary slide",
    "普通左右滑入",
    "decoration-only connector line",
    "decorative line only",
    "无信息作用线条",
    "empty rail sweep",
    "空导轨扫过",
    "card carousel",
    "旧卡片轮播",
]

ADVANCED_RECIPES = {
    "metal_aperture_handoff",
    "glass_prism_refraction",
    "semantic_node_relay",
    "source_evidence_focus",
    "layered_information_assembly",
    "cursor_path_operation",
    "state_lock_microinteraction",
    "checklist_matrix_assembly",
    "proof_lens_magnification",
    "final_template_convergence",
    "source_focus_lens_reveal",
    "citation_rail_wipe",
    "comparison_split_handoff",
    "operation_node_relay",
    "terminal_scan_proof_tray",
    "template_lift_settle",
    "final_controlled_zoom",
    "lens_aperture_reveal",
    "magnetic_data_rail_wipe",
    "prism_layer_refract",
    "source_scan_lock_wipe",
    "node_graph_converge",
    "depth_parallax_lens_swap",
    "proof_panel_morph",
}

NEGATION_MARKERS = [
    "no ",
    "not ",
    "avoid ",
    "without ",
    "ban ",
    "blocked ",
    "禁止",
    "禁用",
    "不得",
    "不能",
    "不要",
    "避免",
    "不允许",
]


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def load_json(path: Path) -> dict[str, Any]:
    if not exists(path):
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def text_blob(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def is_negated(text: str, start: int) -> bool:
    prefix = text[max(0, start - 28) : start].lower()
    return any(marker in prefix for marker in NEGATION_MARKERS)


def forbidden_hits(text: str, forbidden_effects: list[str]) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    lowered = text.lower()
    for term in forbidden_effects:
        if not term:
            continue
        pattern = re.escape(str(term).lower())
        for match in re.finditer(pattern, lowered):
            if is_negated(lowered, match.start()):
                continue
            hits.append({"term": term, "start": match.start(), "context": text[max(0, match.start() - 40) : match.end() + 40]})
    return hits


def collect_motion_text(storyboard: dict[str, Any], metadata: dict[str, Any]) -> str:
    chunks: list[Any] = []
    for scene in storyboard.get("scenes", []) if isinstance(storyboard.get("scenes"), list) else []:
        if isinstance(scene, dict):
            chunks.append(scene.get("motion", {}))
            chunks.append(scene.get("transition", ""))
            chunks.append(scene.get("sfx_cues", []))
    for shot in storyboard.get("director_shots", []) if isinstance(storyboard.get("director_shots"), list) else []:
        if isinstance(shot, dict):
            chunks.append(shot.get("motion", {}))
            chunks.append(shot.get("primary_action", ""))
            chunks.append(shot.get("visual_subject", ""))
    for key in ("production_stack", "quality_spec", "regression_prevention", "motion_layout_contract"):
        if isinstance(metadata.get(key), dict):
            chunks.append(metadata[key])
    return "\n".join(text_blob(chunk) for chunk in chunks if chunk)


def transition_recipe_count(storyboard: dict[str, Any], metadata: dict[str, Any], selection: dict[str, Any]) -> tuple[int, list[str]]:
    text = "\n".join(
        [
            collect_motion_text(storyboard, metadata),
            text_blob(selection.get("transition_sfx_pack", {})),
            text_blob(selection.get("motion_layout_contract", {})),
        ]
    ).lower()
    recipes = sorted(recipe for recipe in ADVANCED_RECIPES if recipe in text)
    return len(recipes), recipes


def layout_manifest_checks(manifest: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    issues: list[str] = []
    signals: dict[str, Any] = {
        "components_checked": 0,
        "three_column_groups_checked": 0,
        "text_boxes_checked": 0,
        "glass_transparency_checked": False,
    }
    if not manifest:
        issues.append("render_layout_manifest.json is required for measured layout/text QA")
        return issues, signals

    if manifest.get("status") == "failed":
        issues.append("render_layout_manifest.status is failed")

    components = manifest.get("components") if isinstance(manifest.get("components"), list) else []
    signals["components_checked"] = len(components)
    for index, component in enumerate(components):
        if not isinstance(component, dict):
            continue
        component_id = str(component.get("id") or f"component[{index}]")
        if component.get("text_overflow") is True:
            issues.append(f"{component_id} has text_overflow=true")
        if component.get("collision") is True or component.get("text_collision") is True:
            issues.append(f"{component_id} has text collision")
        padding = component.get("min_padding_px")
        if padding is not None:
            try:
                if float(padding) < 24:
                    issues.append(f"{component_id} min_padding_px must be >= 24")
            except Exception:
                issues.append(f"{component_id} min_padding_px must be numeric")
        title_padding = component.get("title_padding_px")
        if title_padding is not None:
            try:
                if float(title_padding) < 36:
                    issues.append(f"{component_id} title_padding_px must be >= 36")
            except Exception:
                issues.append(f"{component_id} title_padding_px must be numeric")
        text_boxes = component.get("text_boxes") if isinstance(component.get("text_boxes"), list) else []
        signals["text_boxes_checked"] += len(text_boxes)
        for box_index, box in enumerate(text_boxes):
            if not isinstance(box, dict):
                continue
            label = str(box.get("id") or f"{component_id}.text[{box_index}]")
            if box.get("overflow") is True:
                issues.append(f"{label} overflows its text box")
            if box.get("collides") is True:
                issues.append(f"{label} collides with another visual element")
            lines = box.get("line_count")
            max_lines = box.get("max_lines")
            if lines is not None and max_lines is not None:
                try:
                    if int(lines) > int(max_lines):
                        issues.append(f"{label} line_count exceeds max_lines")
                except Exception:
                    issues.append(f"{label} line_count/max_lines must be numeric")

    three_column_groups = manifest.get("three_column_groups") if isinstance(manifest.get("three_column_groups"), list) else []
    signals["three_column_groups_checked"] = len(three_column_groups)
    for index, group in enumerate(three_column_groups):
        if not isinstance(group, dict):
            continue
        group_id = str(group.get("id") or f"three_column_group[{index}]")
        if group.get("grid_locked") is not True:
            issues.append(f"{group_id} grid_locked must be true")
        for field in ["equal_column_widths", "icon_center_y_aligned", "title_baseline_y_aligned", "body_box_y_aligned"]:
            if group.get(field) is not True:
                issues.append(f"{group_id}.{field} must be true")
        bottom_gap = group.get("bottom_summary_gap_px")
        if bottom_gap is not None:
            try:
                if float(bottom_gap) < 48:
                    issues.append(f"{group_id}.bottom_summary_gap_px must be >= 48")
            except Exception:
                issues.append(f"{group_id}.bottom_summary_gap_px must be numeric")
        max_baseline_delta = group.get("max_baseline_delta_px")
        if max_baseline_delta is not None:
            try:
                if float(max_baseline_delta) > 4:
                    issues.append(f"{group_id}.max_baseline_delta_px must be <= 4")
            except Exception:
                issues.append(f"{group_id}.max_baseline_delta_px must be numeric")

    decorative_paths = manifest.get("decorative_paths") if isinstance(manifest.get("decorative_paths"), list) else []
    for index, path in enumerate(decorative_paths):
        if isinstance(path, dict) and path.get("crosses_text") is True:
            issues.append(f"decorative_paths[{index}] crosses text")

    glass = manifest.get("glass_transparency") if isinstance(manifest.get("glass_transparency"), dict) else {}
    signals["glass_transparency_checked"] = bool(glass)
    if not glass:
        issues.append("render_layout_manifest.glass_transparency is required")
    else:
        if glass.get("profile") != "glass_transparency_v2":
            issues.append("render_layout_manifest.glass_transparency.profile must be glass_transparency_v2")
        if glass.get("dynamic_background_visible") is not True:
            issues.append("render_layout_manifest.glass_transparency.dynamic_background_visible must be true")
        if glass.get("foreground_stage_transparent") is not True:
            issues.append("render_layout_manifest.glass_transparency.foreground_stage_transparent must be true")
        if glass.get("backdrop_filter_present") is not True:
            issues.append("render_layout_manifest.glass_transparency.backdrop_filter_present must be true")
        max_fill_alpha = glass.get("max_background_fill_alpha")
        try:
            alpha = float(max_fill_alpha)
            signals["glass_max_background_fill_alpha"] = alpha
            if alpha > 0.34:
                issues.append("render_layout_manifest.glass_transparency.max_background_fill_alpha must be <= 0.34")
        except Exception:
            issues.append("render_layout_manifest.glass_transparency.max_background_fill_alpha must be numeric")

    return issues, signals


def validate(project: Path, require_layout_manifest: bool = True) -> dict[str, Any]:
    internal = project / "internal"
    selection = load_json(internal / "fixed_template_selection.json")
    storyboard = load_json(internal / "storyboard.json")
    metadata = load_json(internal / "metadata.json")
    layout_manifest = load_json(internal / "render_layout_manifest.json")

    issues: list[str] = []
    warnings: list[str] = []

    motion_contract = selection.get("motion_layout_contract") if isinstance(selection.get("motion_layout_contract"), dict) else {}
    forbidden_effects = [str(item) for item in motion_contract.get("forbidden_low_grade_effects", []) if str(item).strip()]
    if not forbidden_effects:
        forbidden_effects = DEFAULT_FORBIDDEN_EFFECTS

    motion_text = collect_motion_text(storyboard, metadata)
    hits = forbidden_hits(motion_text, forbidden_effects)
    for hit in hits:
        issues.append(f"forbidden low-grade motion effect used: {hit['term']}")

    recipe_count, recipes = transition_recipe_count(storyboard, metadata, selection)
    scene_count = len(storyboard.get("scenes", [])) if isinstance(storyboard.get("scenes"), list) else 0
    director_count = len(storyboard.get("director_shots", [])) if isinstance(storyboard.get("director_shots"), list) else 0
    expected_min = 3 if max(scene_count, director_count) >= 4 else 1
    if recipe_count < expected_min:
        issues.append(f"at least {expected_min} approved advanced transition recipes are required; found {recipe_count}")

    if require_layout_manifest:
        layout_issues, layout_signals = layout_manifest_checks(layout_manifest)
        issues.extend(layout_issues)
    else:
        layout_issues, layout_signals = [], {}
        if not layout_manifest:
            warnings.append("render_layout_manifest.json missing; layout checks skipped by caller")

    report = {
        "status": "passed" if not issues else "failed",
        "project": str(project),
        "checks": {
            "no_forbidden_low_grade_motion": not hits,
            "advanced_transition_recipe_count_ok": recipe_count >= expected_min,
            "layout_manifest_present": bool(layout_manifest),
            "layout_manifest_checks_ok": not layout_issues,
        },
        "signals": {
            "advanced_transition_recipe_count": recipe_count,
            "advanced_transition_recipes": recipes,
            "scene_count": scene_count,
            "director_shot_count": director_count,
            **layout_signals,
        },
        "forbidden_motion_hits": hits,
        "blocking_issues": issues,
        "warnings": warnings,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Check premium motion and measured layout contract for AI videos.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument("--out", help="Output report path; defaults to <project>/internal/layout_motion_contract_report.json")
    parser.add_argument("--allow-missing-layout-manifest", action="store_true", help="Only for early planning smoke checks.")
    args = parser.parse_args()

    project = Path(args.project)
    out = Path(args.out) if args.out else project / "internal" / "layout_motion_contract_report.json"
    report = validate(project, require_layout_manifest=not args.allow_missing_layout_manifest)
    write_json(out, report)
    print(json.dumps({"status": report["status"], "issues": report["blocking_issues"], "warnings": report["warnings"]}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
