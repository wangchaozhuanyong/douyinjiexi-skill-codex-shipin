#!/usr/bin/env python3
"""Validate V3 storyboard gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


EVIDENCE_TYPES = {"real_ui_demo", "screenshot_proof", "comparison", "proof_wall", "code_or_file_proof", "result_reveal"}
STATIC_TYPES = {"generated_visual", "text_card", "cover"}
BEAT_REQUIRED = ["voice_fragment", "visual_action", "caption", "proof_or_explanation", "motion_trigger"]
PROOF_CHAIN_REQUIRED = ["entry_or_source", "operation_or_step", "output_or_result", "viewer_value"]
QUALITY_SPEC_REQUIRED = [
    "target_quality_level",
    "visual_system",
    "motion_policy",
    "still_image_policy",
    "evidence_policy",
    "sfx_policy",
    "render_policy",
    "cover_policy",
    "frame_review_policy",
]
QUALITY_CHECK_REQUIRED = ["source_resolution_ok", "text_safe", "not_template_like", "not_static_dump"]
ACCEPTED_QUALITY_LEVELS = {"high_quality", "breakout_potential"}
STACK_TRIGGER_TERMS = ["codex", "skill", "插件", "remotion", "hyperframes", "imagegen", "image gen", "heygen"]
MIN_SAFE_MARGINS = {
    "top_margin_px": 240,
    "bottom_margin_px": 360,
    "left_margin_px": 72,
    "right_margin_px": 180,
}
MIN_NORMAL_TTS_SPEED = 0.95
MAX_NORMAL_TTS_SPEED = 1.03


def motion_layer_count(motion: dict[str, Any]) -> int:
    keys = ["background_motion", "foreground_motion", "callout_motion", "transition"]
    return sum(1 for key in keys if str(motion.get(key, "")).strip() and str(motion.get(key)).lower() != "none")


def normal_tts_speed(value: Any) -> bool:
    try:
        speed = float(value)
    except Exception:
        return False
    return MIN_NORMAL_TTS_SPEED <= speed <= MAX_NORMAL_TTS_SPEED


def collect_text(data: dict[str, Any]) -> str:
    parts: list[str] = [str(data.get("title", ""))]
    for scene in data.get("scenes", []) or []:
        parts.extend(
            [
                str(scene.get("scene_id", "")),
                str(scene.get("concept", "")),
                str(scene.get("voice", "")),
                str(scene.get("caption", "")),
            ]
        )
        parts.extend(str(item) for item in scene.get("on_screen_text", []) or [])
    return " ".join(parts)


def scene_text(scene: dict[str, Any]) -> str:
    parts = [str(scene.get("concept", "")), str(scene.get("voice", "")), str(scene.get("caption", ""))]
    parts.extend(str(item) for item in scene.get("on_screen_text", []) or [])
    return " ".join(parts).lower()


def requires_production_stack(data: dict[str, Any]) -> bool:
    text = collect_text(data).lower()
    return any(term in text for term in STACK_TRIGGER_TERMS)


def validate_evidence_chain(prefix: str, chain: Any, issues: list[str]) -> bool:
    if not isinstance(chain, dict):
        issues.append(f"{prefix} missing evidence_chain/proof_chain")
        return False
    ok = True
    for key in PROOF_CHAIN_REQUIRED:
        if not str(chain.get(key, "")).strip():
            issues.append(f"{prefix} evidence_chain/proof_chain missing {key}")
            ok = False
    return ok


def validate_quality_spec(data: dict[str, Any], issues: list[str]) -> dict[str, Any]:
    quality_spec = data.get("quality_spec")
    valid = True
    if not isinstance(quality_spec, dict):
        issues.append("quality_spec is required for high-quality video output")
        return {
            "quality_spec_required": True,
            "quality_spec_valid": False,
        }

    for key in QUALITY_SPEC_REQUIRED:
        if not str(quality_spec.get(key, "")).strip():
            issues.append(f"quality_spec.{key} is required")
            valid = False

    level = str(quality_spec.get("target_quality_level", "")).strip()
    if level not in ACCEPTED_QUALITY_LEVELS:
        issues.append("quality_spec.target_quality_level must be high_quality or breakout_potential")
        valid = False

    return {
        "quality_spec_required": True,
        "quality_spec_valid": valid,
    }


def scene_quality_checks_pass(quality_checks: Any) -> bool:
    if not isinstance(quality_checks, dict):
        return False
    return all(quality_checks.get(key) is True for key in QUALITY_CHECK_REQUIRED)


def validate_production_stack(data: dict[str, Any], issues: list[str], warnings: list[str]) -> dict[str, Any]:
    stack_required = requires_production_stack(data)
    stack_valid = True
    tool_proof_chain_count = 0
    scene_texts = [scene_text(scene) for scene in data.get("scenes", []) or []]
    joined_scene_text = " ".join(scene_texts)

    if not stack_required:
        return {
            "production_stack_required": False,
            "production_stack_valid": True,
            "tool_proof_chain_count": 0,
        }

    stack = data.get("production_stack")
    if not isinstance(stack, dict):
        issues.append("production_stack is required for Codex/Skill/plugin/Remotion/HyperFrames/ImageGen tutorial videos")
        return {
            "production_stack_required": True,
            "production_stack_valid": False,
            "tool_proof_chain_count": 0,
        }

    if stack.get("reference_learning_applied") is not True:
        issues.append("production_stack.reference_learning_applied must be true for reference-led skill tutorials")
        stack_valid = False
    workflow_order = stack.get("workflow_order", [])
    if not isinstance(workflow_order, list) or len(workflow_order) < 3:
        issues.append("production_stack.workflow_order must document at least 3 production stages")
        stack_valid = False

    tools = stack.get("primary_tools", [])
    if not isinstance(tools, list) or not tools:
        issues.append("production_stack.primary_tools must list the tools/skills used or taught")
        stack_valid = False
        tools = []

    text = collect_text(data).lower()
    if ("三个" in text or "3 个" in text or "three" in text) and ("skill" in text or "插件" in text) and len(tools) < 3:
        issues.append("three-Skill tutorial storyboards must document at least 3 primary tools")
        stack_valid = False

    for index, tool in enumerate(tools, start=1):
        if not isinstance(tool, dict):
            issues.append(f"production_stack.primary_tools[{index}] must be an object")
            stack_valid = False
            continue
        name = str(tool.get("name", "")).strip()
        role = str(tool.get("role", "")).strip()
        if not name:
            issues.append(f"production_stack.primary_tools[{index}] missing name")
            stack_valid = False
        if not role:
            issues.append(f"production_stack.primary_tools[{index}] missing role")
            stack_valid = False
        if validate_evidence_chain(f"production_stack.primary_tools[{index}]", tool.get("evidence_chain"), issues):
            tool_proof_chain_count += 1
        else:
            stack_valid = False
        aliases = [name.lower()]
        aliases.extend(str(item).lower() for item in tool.get("aliases", []) or [])
        if name and not any(alias and alias in joined_scene_text for alias in aliases):
            issues.append(f"production_stack tool {name} must appear in at least one scene voice/caption/on-screen text")
            stack_valid = False

    tool_names = [str(tool.get("name", "")).strip().lower() for tool in tools if isinstance(tool, dict)]
    for scene in data.get("scenes", []) or []:
        current_text = scene_text(scene)
        mentions_tool = any(name and name in current_text for name in tool_names)
        visual = scene.get("visual", {})
        if isinstance(visual, dict):
            if mentions_tool:
                if not validate_evidence_chain(f"{scene.get('scene_id', 'unknown')} visual", visual.get("proof_chain"), issues):
                    stack_valid = False
            elif visual.get("scene_type") in EVIDENCE_TYPES and "proof_chain" not in visual:
                warnings.append(f"{scene.get('scene_id', 'unknown')} evidence scene should include visual.proof_chain")

    return {
        "production_stack_required": True,
        "production_stack_valid": stack_valid,
        "tool_proof_chain_count": tool_proof_chain_count,
    }


def validate(data: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    target = data.get("target", {})
    if not isinstance(target, dict):
        issues.append("target must be an object")
        target = {}
    if not normal_tts_speed(target.get("tts_speed")):
        issues.append("target.tts_speed must be normal speed between 0.95 and 1.03; do not speed up narration")
    if str(target.get("voice_speed_policy", "")).strip().lower() not in {"normal", "normal_speed"}:
        issues.append("target.voice_speed_policy must be normal")
    quality_signals = validate_quality_spec(data, issues)
    stack_signals = validate_production_stack(data, issues, warnings)

    scenes = data.get("scenes", [])
    if len(scenes) < 6:
        issues.append("storyboard must contain at least 6 scenes")
    first_five_changes = 0
    elapsed = 0.0
    evidence_runtime = 0.0
    total_runtime = 0.0
    layered_scene_count = 0
    quality_check_scene_count = 0
    visual_change_times: list[float] = []
    retention_times: list[float] = []
    for scene in scenes:
        duration = float(scene.get("duration_target") or 0)
        total_runtime += duration
        if elapsed < 5:
            first_five_changes += 1
        visual_change_times.append(elapsed)
        elapsed += duration
        for key in ["scene_id", "concept", "voice", "caption", "on_screen_text", "visual", "motion", "sync", "safe_zone", "qa_notes"]:
            if key not in scene:
                issues.append(f"{scene.get('scene_id', 'unknown')} missing {key}")
        beat_map = scene.get("beat_map", [])
        if not beat_map:
            issues.append(f"{scene.get('scene_id', 'unknown')} missing beat_map")
        for index, beat in enumerate(beat_map, start=1):
            retention_times.append(elapsed - duration)
            for key in BEAT_REQUIRED:
                if not str(beat.get(key, "")).strip():
                    issues.append(f"{scene.get('scene_id', 'unknown')} beat {index} missing {key}")
            voice_fragment = str(beat.get("voice_fragment", "")).strip()
            voice = str(scene.get("voice", ""))
            if voice_fragment and voice_fragment not in voice:
                warnings.append(f"{scene.get('scene_id', 'unknown')} beat {index} voice_fragment not found verbatim in voice")
            if not any(term in str(beat.get("proof_or_explanation", "")) for term in ["对比", "证明", "错误", "模板", "结果", "清单", "真实", "保存"]):
                warnings.append(f"{scene.get('scene_id', 'unknown')} beat {index} should name proof, contrast, template, result, or save value")
        if motion_layer_count(scene.get("motion", {})) < 2:
            issues.append(f"{scene.get('scene_id', 'unknown')} needs at least 2 motion layers")
        visual = scene.get("visual", {})
        if visual.get("scene_type") in EVIDENCE_TYPES:
            evidence_runtime += duration
        design_layers = visual.get("design_layers") if isinstance(visual, dict) else None
        if isinstance(design_layers, list) and len([item for item in design_layers if str(item).strip()]) >= 3:
            layered_scene_count += 1
        else:
            issues.append(f"{scene.get('scene_id', 'unknown')} visual.design_layers must contain at least 3 real design layers")
        if scene_quality_checks_pass(visual.get("quality_checks") if isinstance(visual, dict) else None):
            quality_check_scene_count += 1
        else:
            issues.append(f"{scene.get('scene_id', 'unknown')} visual.quality_checks must pass source/text/template/static checks")
        safe_zone = scene.get("safe_zone", {})
        for key in ["top_reserved", "bottom_caption_reserved", "right_buttons_reserved"]:
            if safe_zone.get(key) is not True:
                issues.append(f"{scene.get('scene_id', 'unknown')} safe_zone.{key} must be true")
        for key, minimum in MIN_SAFE_MARGINS.items():
            try:
                value = int(safe_zone.get(key, 0))
            except Exception:
                value = 0
            if value < minimum:
                issues.append(f"{scene.get('scene_id', 'unknown')} safe_zone.{key} must be >= {minimum}")
        if safe_zone.get("critical_content_inside_safe_area") is not True:
            issues.append(f"{scene.get('scene_id', 'unknown')} safe_zone.critical_content_inside_safe_area must be true")
        new_concepts = scene.get("new_concepts")
        if isinstance(new_concepts, list) and len(new_concepts) > 1:
            issues.append(f"{scene.get('scene_id', 'unknown')} must not introduce more than one new concept")
        concept = str(scene.get("concept", "")).strip()
        if not concept:
            issues.append(f"{scene.get('scene_id', 'unknown')} concept is required")
        if any(separator in concept for separator in ["；", ";", " and ", "以及"]):
            issues.append(f"{scene.get('scene_id', 'unknown')} concept must describe one idea, not multiple ideas")
        if len(scene.get("on_screen_text", [])) > 4:
            warnings.append(f"{scene.get('scene_id', 'unknown')} has dense on-screen text; verify it is one concept")
        if visual.get("scene_type") in STATIC_TYPES and duration > 5:
            issues.append(f"{scene.get('scene_id', 'unknown')} has long narration over a static visual type")
        if duration > 8:
            issues.append(f"{scene.get('scene_id', 'unknown')} duration is too long; split or add reveal/build/focus")
        if duration > 5 and len(beat_map) < 2:
            warnings.append(f"{scene.get('scene_id', 'unknown')} is longer than 5s and should include at least 2 beat_map items")
    if first_five_changes < 2:
        issues.append("first 5 seconds must contain at least 2 visual changes")
    for previous, current in zip(visual_change_times, visual_change_times[1:]):
        if current - previous > 5:
            issues.append("visual changes must happen every 3-5 seconds")
            break
    ratio = evidence_runtime / total_runtime if total_runtime else 0
    if ratio < 0.5:
        issues.append("evidence runtime ratio must be at least 0.5")
    if ratio < 0.6:
        warnings.append("evidence runtime ratio is publishable but below the V3 high-quality target of 0.6")
    if total_runtime >= 8:
        retention_times = retention_times or visual_change_times
        retention_times = sorted(set(round(item, 3) for item in retention_times))
        if not retention_times:
            issues.append("retention beats are missing")
        for previous, current in zip(retention_times, retention_times[1:]):
            if current - previous > 8:
                issues.append("retention beats must appear every 6-8 seconds")
                break
    return {
        "status": "passed" if not issues else "failed",
        "issues": issues,
        "warnings": warnings,
        "scene_count": len(scenes),
        "evidence_runtime_ratio": round(ratio, 3),
        "signals": {
            **quality_signals,
            **stack_signals,
            "layered_scene_count": layered_scene_count,
            "quality_check_scene_count": quality_check_scene_count,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate storyboard.json gates.")
    parser.add_argument("--storyboard", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()

    data = json.loads(Path(args.storyboard).read_text(encoding="utf-8"))
    report = validate(data)
    if args.out:
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
