#!/usr/bin/env python3
"""Check a per-video foreground module construction plan."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ART_LIBRARY = ROOT / "references" / "foreground_art_module_library_v2.json"
DEFAULT_MICRO_LIBRARY = ROOT / "references" / "foreground_micro_component_library_v1.json"


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def text_len(value: Any) -> int:
    return len(str(value or "").strip())


def phase_value(scene: dict[str, Any], key: str, fallback: Any = None) -> Any:
    return scene.get(key) if scene.get(key) not in (None, "") else fallback


def component_cost(component: dict[str, Any], instance_count: int) -> tuple[float, float, int]:
    budget = component.get("budget") if isinstance(component.get("budget"), dict) else {}
    visual = float(budget.get("visual_weight") or 0)
    if instance_count > 1:
        visual += float(budget.get("additional_instance_visual_weight") or 0) * (instance_count - 1)
    motion = float(budget.get("motion_weight") or 0)
    text = int(budget.get("text_weight") or 0)
    return visual, motion, text


def validate_text_slots(
    owner_id: str,
    planned_slots: dict[str, Any],
    limits: dict[str, Any],
    issues: list[str],
) -> None:
    for slot, value in planned_slots.items():
        if slot not in limits:
            issues.append(f"{owner_id} uses unknown text slot {slot}")
            continue
        limit = limits.get(slot) if isinstance(limits.get(slot), dict) else {}
        max_chars = limit.get("max_chars")
        if max_chars is not None and text_len(value) > int(max_chars):
            issues.append(f"{owner_id} text slot {slot} exceeds max_chars={max_chars}: {value}")
        max_lines = int(limit.get("max_lines") or 0)
        if max_lines and "\n" in str(value):
            line_count = len(str(value).splitlines())
            if line_count > max_lines:
                issues.append(f"{owner_id} text slot {slot} exceeds max_lines={max_lines}")
    for slot, limit in limits.items():
        if isinstance(limit, dict) and limit.get("required") is True and slot not in planned_slots:
            issues.append(f"{owner_id} missing required text slot {slot}")


def validate(project: Path, plan_path: Path, art_path: Path, micro_path: Path) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    if not plan_path.exists() or not plan_path.is_file() or plan_path.stat().st_size == 0:
        issues.append(f"foreground module plan missing: {plan_path}")
        return {"status": "failed", "blocking_issues": issues, "warnings": warnings, "signals": {}}

    plan = load_json(plan_path)
    art_library = load_json(art_path)
    micro_library = load_json(micro_path)

    modules = {
        str(item.get("module_id")): item
        for item in art_library.get("modules", [])
        if isinstance(item, dict) and item.get("module_id")
    }
    components = {
        str(item.get("component_id")): item
        for item in micro_library.get("components", [])
        if isinstance(item, dict) and item.get("component_id")
    }
    adapters = {
        str(item.get("module_id")): item
        for item in micro_library.get("parent_module_adapters", [])
        if isinstance(item, dict) and item.get("module_id")
    }
    global_rules = micro_library.get("global_rules") if isinstance(micro_library.get("global_rules"), dict) else {}
    activation = global_rules.get("activation") if isinstance(global_rules.get("activation"), dict) else {}
    budgets = global_rules.get("budgets") if isinstance(global_rules.get("budgets"), dict) else {}
    aspect = str(plan.get("aspect_ratio") or "16:9")
    aspect_key = "portrait" if aspect == "9:16" else "landscape"
    visual_budget_max = float(budgets.get("portrait_visual_weight_max" if aspect_key == "portrait" else "landscape_visual_weight_max") or 0)
    motion_budget_max = float(budgets.get("concurrent_motion_weight_max") or 999)
    max_concurrent_animations = int(budgets.get("max_concurrent_component_animations") or 999)
    max_instances = int(activation.get("hard_max_visible_instances") or 9)
    max_types = int(activation.get("hard_max_component_types") or 5)
    max_text_components = int(activation.get("max_text_bearing_components_visible") or 3)
    max_per_anchor = int(activation.get("max_components_per_anchor_region") or 2)

    scenes = plan.get("scenes") if isinstance(plan.get("scenes"), list) else []
    if not scenes:
        issues.append("foreground_module_plan.scenes must contain at least one scene")
    planned_scene_ids = [
        str(scene.get("scene_id") or "")
        for scene in scenes
        if isinstance(scene, dict) and scene.get("scene_id")
    ]
    if len(set(planned_scene_ids)) != len(planned_scene_ids):
        issues.append("foreground_module_plan.scenes must not repeat scene_id values")

    storyboard_path = project / "internal" / "storyboard.json"
    storyboard_scene_ids: list[str] = []
    if storyboard_path.exists() and storyboard_path.is_file() and storyboard_path.stat().st_size > 0:
        storyboard = load_json(storyboard_path)
        storyboard_scenes = storyboard.get("scenes") if isinstance(storyboard.get("scenes"), list) else []
        for index, scene in enumerate(storyboard_scenes, start=1):
            if not isinstance(scene, dict):
                continue
            scene_id = str(scene.get("id") or scene.get("scene_id") or scene.get("shot_id") or f"S{index:02d}")
            storyboard_scene_ids.append(scene_id)
        missing_scene_ids = [scene_id for scene_id in storyboard_scene_ids if scene_id not in planned_scene_ids]
        extra_scene_ids = [scene_id for scene_id in planned_scene_ids if scene_id not in storyboard_scene_ids]
        if missing_scene_ids:
            issues.append(f"foreground_module_plan missing storyboard scene ids: {missing_scene_ids}")
        if extra_scene_ids:
            issues.append(f"foreground_module_plan has scene ids not found in storyboard.json: {extra_scene_ids}")

    scene_reports: list[dict[str, Any]] = []
    for scene in scenes:
        if not isinstance(scene, dict):
            issues.append("foreground_module_plan.scenes contains a non-object scene")
            continue
        scene_id = str(scene.get("scene_id") or "unknown")
        module_id = str(scene.get("parent_module_id") or "")
        scene_aspect = str(phase_value(scene, "aspect_ratio", aspect))
        scene_aspect_key = "portrait" if scene_aspect == "9:16" else "landscape"
        if module_id not in modules:
            issues.append(f"{scene_id} parent_module_id must be M01-M20; got {module_id}")
            continue
        module = modules[module_id]
        adapter = adapters.get(module_id)
        if not adapter:
            issues.append(f"{scene_id} missing parent adapter for {module_id}")
            continue
        validate_text_slots(f"{scene_id}.{module_id}", scene.get("text_slots") or {}, module.get("text_limits") or {}, issues)
        transition_ids = set(art_library.get("transitions", {}).keys())
        module_transition_ids = set(module.get("transition_ids") or [])
        for key in ["transition_in", "transition_out"]:
            if scene.get(key) not in transition_ids:
                issues.append(f"{scene_id}.{key} must be one of {sorted(transition_ids)}")
            elif module_transition_ids and scene.get(key) not in module_transition_ids:
                issues.append(f"{scene_id}.{key} {scene.get(key)} is not allowed for {module_id}; expected one of {sorted(module_transition_ids)}")

        planned_components = scene.get("micro_components") if isinstance(scene.get("micro_components"), list) else []
        adapter_max = adapter.get("max_active") if isinstance(adapter.get("max_active"), dict) else {}
        scene_max_types = min(max_types, int(adapter_max.get(scene_aspect_key) or max_types))
        if len(planned_components) < 2:
            issues.append(f"{scene_id} must plan at least 2 micro-components for premium foreground detail")
        if len(planned_components) > scene_max_types:
            issues.append(f"{scene_id} uses {len(planned_components)} micro-component types; max is {scene_max_types}")

        anchor_map = adapter.get("anchor_map") if isinstance(adapter.get("anchor_map"), dict) else {}
        phase_visual: dict[str, float] = defaultdict(float)
        phase_motion: dict[str, float] = defaultdict(float)
        phase_text_count: dict[str, int] = defaultdict(int)
        phase_component_count: dict[str, int] = defaultdict(int)
        phase_anchor_count: dict[tuple[str, str], int] = defaultdict(int)
        process_light_motion_count = 0
        total_instances = 0
        seen_component_ids: set[str] = set()

        for planned in planned_components:
            if not isinstance(planned, dict):
                issues.append(f"{scene_id} has non-object micro component entry")
                continue
            component_id = str(planned.get("component_id") or "")
            anchor = str(planned.get("anchor") or "")
            phase = str(planned.get("phase") or "")
            instance_count = int(planned.get("instance_count") or 1)
            total_instances += max(1, instance_count)
            if component_id not in components:
                issues.append(f"{scene_id} unknown component_id {component_id}")
                continue
            component = components[component_id]
            compatibility = component.get("compatibility") if isinstance(component.get("compatibility"), dict) else {}
            allowed = set(compatibility.get("preferred_module_ids") or []) | set(compatibility.get("allowed_module_ids") or [])
            if module_id not in allowed:
                issues.append(f"{scene_id}.{component_id} is not compatible with {module_id}")
            allowed_anchors = set(compatibility.get("anchor_types") or [])
            if anchor not in allowed_anchors:
                issues.append(f"{scene_id}.{component_id} anchor {anchor} not allowed; expected one of {sorted(allowed_anchors)}")
            if anchor not in anchor_map:
                issues.append(f"{scene_id}.{component_id} anchor {anchor} is not provided by {module_id} adapter")
            allowed_phases = set(compatibility.get("preferred_parent_phases") or [])
            if allowed_phases and phase not in allowed_phases:
                issues.append(f"{scene_id}.{component_id} phase {phase} not in preferred phases {sorted(allowed_phases)}")
            validate_text_slots(f"{scene_id}.{component_id}", planned.get("text_slots") or {}, component.get("text_slots") or {}, issues)

            visual_cost, motion_cost, text_cost = component_cost(component, instance_count)
            phase_visual[phase] += visual_cost
            phase_motion[phase] += motion_cost
            phase_component_count[phase] += 1
            component_motion = float((component.get("budget") or {}).get("motion_weight") or 0)
            if phase == "process" and component_motion <= 1:
                process_light_motion_count += 1
            if planned.get("text_slots"):
                phase_text_count[phase] += 1
            phase_anchor_count[(phase, anchor)] += 1
            seen_component_ids.add(component_id)

        if len(seen_component_ids) != len(planned_components):
            warnings.append(f"{scene_id} repeats a micro component type; verify this is intentional and instance-count based")
        if total_instances > max_instances:
            issues.append(f"{scene_id} uses {total_instances} visible micro instances; max is {max_instances}")
        for phase, cost in phase_visual.items():
            if visual_budget_max and cost > visual_budget_max:
                issues.append(f"{scene_id}.{phase} visual budget {cost:.2f} exceeds max {visual_budget_max:.2f}")
        for phase, cost in phase_motion.items():
            if cost > motion_budget_max:
                issues.append(f"{scene_id}.{phase} motion budget {cost:.2f} exceeds max {motion_budget_max:.2f}")
        for phase, count in phase_component_count.items():
            if count > max_concurrent_animations:
                issues.append(f"{scene_id}.{phase} animates {count} micro-components; max concurrent animations is {max_concurrent_animations}")
        for phase, count in phase_text_count.items():
            if count > max_text_components:
                issues.append(f"{scene_id}.{phase} has {count} text-bearing micro-components; max is {max_text_components}")
        if process_light_motion_count > 1:
            issues.append(f"{scene_id}.process has {process_light_motion_count} lightweight component motions; max is 1 during parent process action")
        for (phase, anchor), count in phase_anchor_count.items():
            if count > max_per_anchor:
                issues.append(f"{scene_id}.{phase}.{anchor} has {count} micro-components; max per anchor is {max_per_anchor}")

        scene_reports.append(
            {
                "scene_id": scene_id,
                "parent_module_id": module_id,
                "micro_component_count": len(planned_components),
                "visible_instance_count": total_instances,
                "phase_visual_budget": dict(phase_visual),
                "phase_motion_budget": dict(phase_motion),
                "phase_component_count": dict(phase_component_count),
            }
        )

    return {
        "status": "passed" if not issues else "failed",
        "project": str(project),
        "plan_path": str(plan_path),
        "blocking_issues": issues,
        "warnings": warnings,
        "signals": {
            "scene_count": len(scenes),
            "storyboard_scene_count": len(storyboard_scene_ids),
            "aspect_ratio": aspect,
            "visual_budget_max": visual_budget_max,
            "motion_budget_max": motion_budget_max,
            "max_concurrent_animations": max_concurrent_animations,
            "scene_reports": scene_reports,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate foreground_module_plan.json against M/C module libraries.")
    parser.add_argument("--project", required=True, help="Project folder such as outputs/demo")
    parser.add_argument("--plan", help="Plan path. Defaults to <project>/internal/foreground_module_plan.json")
    parser.add_argument("--art-library", default=str(DEFAULT_ART_LIBRARY))
    parser.add_argument("--micro-library", default=str(DEFAULT_MICRO_LIBRARY))
    parser.add_argument("--out", help="Output report path. Defaults to <project>/internal/foreground_module_plan_check.json")
    args = parser.parse_args()

    project = resolve_path(args.project)
    plan_path = resolve_path(args.plan) if args.plan else project / "internal" / "foreground_module_plan.json"
    out = resolve_path(args.out) if args.out else project / "internal" / "foreground_module_plan_check.json"
    report = validate(project, plan_path, resolve_path(args.art_library), resolve_path(args.micro_library))
    write_json(out, report)
    print(json.dumps({"status": report["status"], "issues": report["blocking_issues"], "warnings": report["warnings"]}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
