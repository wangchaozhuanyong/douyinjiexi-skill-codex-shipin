#!/usr/bin/env python3
"""Automatic visual review using storyboard, frame review, and metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Union

from artifact_fingerprint import verify_report_inputs, write_report_with_fingerprints
from validate_storyboard import cue_is_voice_safe, scene_has_animated_icon_event, scene_sfx_cues
from voice_quality import voice_provider_passes


WEAK_MOTION_TERMS = ["none", "static", "无", "无动画", "loop pulse", "ken burns"]
PREMIUM_SCENE_TYPES = {
    "screenshot_proof",
    "real_ui_demo",
    "comparison",
    "proof_wall",
    "code_or_file_proof",
    "timeline_process",
    "result_reveal",
}
MIN_SAFE_MARGINS = {
    "top_margin_px": 240,
    "bottom_margin_px": 360,
    "left_margin_px": 72,
    "right_margin_px": 180,
}
STORY_QUALITY_SPEC_REQUIRED = [
    "target_quality_level",
    "visual_system",
    "motion_policy",
    "still_image_policy",
    "evidence_policy",
    "sfx_policy",
    "render_policy",
    "cover_policy",
    "frame_review_policy",
    "provider_policy",
    "runtime_choice",
    "caption_template_plan",
    "timeline_contract_ref",
    "narration_continuity_policy",
]
METADATA_QUALITY_SPEC_REQUIRED = [
    "target_quality_level",
    "render_quality",
    "min_bitrate",
    "source_asset_policy",
    "sfx_policy",
    "cover_policy",
    "frame_review_policy",
    "provider_policy",
    "runtime_choice",
    "caption_template_plan",
    "timeline_contract_ref",
    "narration_continuity_policy",
]
ACCEPTED_QUALITY_LEVELS = {"high_quality", "breakout_potential"}
ACCEPTED_RENDER_QUALITY = {"hyperframes_high", "high_bitrate_h264", "hyperframes_high_plus_remux"}
ACCEPTED_PROVIDER_POLICY = "free_first_local_or_authorized_openai_only"
QUALITY_CHECK_REQUIRED = ["source_resolution_ok", "text_safe", "not_template_like", "not_static_dump"]
MIN_METADATA_BITRATE = 3_500_000
ASSET_SOURCE_TYPES = {"proof", "support", "generated", "free_stock"}
NO_SFX_POLICY_TERMS = [
    "no added sfx",
    "no sfx",
    "without sfx",
    "sfx disabled",
    "none",
]
UNUSED_STRUCTURE_TERMS = [
    "unused frame",
    "unused panel",
    "unused card",
    "unused rail",
    "unused slot",
    "unused framework",
    "placeholder frame",
    "placeholder panel",
    "placeholder card",
    "placeholder rail",
    "placeholder slot",
    "placeholder line",
    "placeholder framework",
    "empty frame",
    "empty panel",
    "empty card",
    "empty rail",
    "empty slot",
    "blank frame",
    "blank panel",
    "blank card",
    "blank rail",
    "blank placeholder",
    "blank source wall",
    "decorative frame",
    "decorative panel",
    "decorative card",
    "decorative rail",
    "fake source wall",
    "fake ui slot",
    "空框",
    "空卡",
    "空卡片",
    "空白框",
    "空白卡",
    "空白卡片",
    "占位框",
    "占位卡",
    "占位卡槽",
    "占位线",
    "未使用框",
    "未使用卡",
    "无用框架",
    "装饰性框架",
]
WEAK_RUNTIME_TERMS = [
    "ffmpeg portrait card pipeline",
    "ffmpeg card pipeline",
    "ffmpeg generated frame timeline",
    "ffmpeg generated",
    "pil ffmpeg",
    "pil",
    "portrait card pipeline",
    "card-only",
    "card only",
    "text-card slideshow",
    "text card slideshow",
    "hyperframes compatible",
    "compatible visual contract",
]
CAPTION_TEMPLATES = {
    "word_highlight",
    "side_label",
    "proof_callout",
    "terminal_code_caption",
    "chapter_card",
    "final_takeaway",
    "bottom_light_caption",
    "comparison_label",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def exists(path: Union[str, Path]) -> bool:
    target = Path(path)
    return target.exists() and target.stat().st_size > 0


def motion_layers(scene: dict[str, Any]) -> int:
    motion = scene.get("motion", {})
    if not isinstance(motion, dict):
        return 0
    count = 0
    for value in motion.values():
        text = str(value).strip().lower()
        if text and not any(term in text for term in WEAK_MOTION_TERMS):
            count += 1
    return count


def scene_duration(scene: dict[str, Any]) -> float:
    try:
        return float(scene.get("duration_target", 0))
    except Exception:
        return 0.0


def safe_zone_passes(safe_zone: dict[str, Any]) -> bool:
    if not all(safe_zone.get(key) is True for key in ["top_reserved", "bottom_caption_reserved", "right_buttons_reserved"]):
        return False
    if safe_zone.get("critical_content_inside_safe_area") is not True:
        return False
    for key, minimum in MIN_SAFE_MARGINS.items():
        try:
            if int(safe_zone.get(key, 0)) < minimum:
                return False
        except Exception:
            return False
    return True


def story_quality_spec_valid(storyboard: dict[str, Any]) -> bool:
    quality_spec = storyboard.get("quality_spec")
    if not isinstance(quality_spec, dict):
        return False
    if str(quality_spec.get("target_quality_level", "")).strip() not in ACCEPTED_QUALITY_LEVELS:
        return False
    if quality_spec.get("provider_policy") != ACCEPTED_PROVIDER_POLICY:
        return False
    return all(str(quality_spec.get(key, "")).strip() for key in STORY_QUALITY_SPEC_REQUIRED)


def metadata_quality_spec_valid(metadata: dict[str, Any]) -> bool:
    quality_spec = metadata.get("quality_spec")
    if not isinstance(quality_spec, dict):
        return False
    if str(quality_spec.get("target_quality_level", "")).strip() not in ACCEPTED_QUALITY_LEVELS:
        return False
    if str(quality_spec.get("render_quality", "")).strip() not in ACCEPTED_RENDER_QUALITY:
        return False
    if quality_spec.get("provider_policy") != ACCEPTED_PROVIDER_POLICY:
        return False
    try:
        if int(quality_spec.get("min_bitrate", 0)) < MIN_METADATA_BITRATE:
            return False
    except Exception:
        return False
    return all(str(quality_spec.get(key, "")).strip() for key in METADATA_QUALITY_SPEC_REQUIRED)


def normalized_text(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", " ")


def contains_term(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def iter_scene_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        values: list[str] = []
        for item in value.values():
            values.extend(iter_scene_strings(item))
        return values
    if isinstance(value, list):
        values = []
        for item in value:
            values.extend(iter_scene_strings(item))
        return values
    return []


def unused_structure_terms(scene: dict[str, Any]) -> list[str]:
    text = normalized_text(" ".join(iter_scene_strings(scene)))
    return sorted({term for term in UNUSED_STRUCTURE_TERMS if term in text})


def sfx_policy_passes(*quality_specs: dict[str, Any]) -> bool:
    policies = [normalized_text(spec.get("sfx_policy")) for spec in quality_specs if isinstance(spec, dict)]
    if not policies or not all(policies):
        return False
    return not any(contains_term(policy, NO_SFX_POLICY_TERMS) for policy in policies)


def runtime_choice_passes(*quality_specs: dict[str, Any]) -> bool:
    choices = [normalized_text(spec.get("runtime_choice")) for spec in quality_specs if isinstance(spec, dict)]
    if not choices or not all(choices):
        return False
    combined = " ".join(choices)
    return (
        "hyperframes" in combined
        and "final timeline" in combined
        and not contains_term(combined, WEAK_RUNTIME_TERMS)
    )


def visual_layers_pass(visual: dict[str, Any]) -> bool:
    layers = visual.get("design_layers")
    return isinstance(layers, list) and len([item for item in layers if str(item).strip()]) >= 3


def visual_quality_checks_pass(visual: dict[str, Any]) -> bool:
    checks = visual.get("quality_checks")
    if not isinstance(checks, dict):
        return False
    return all(checks.get(key) is True for key in QUALITY_CHECK_REQUIRED)


def scene_readability_text(scene: dict[str, Any]) -> list[str]:
    """Return only actively designed text, not embedded proof screenshot text."""
    text_layers = scene.get("text_layers")
    if isinstance(text_layers, dict):
        primary = text_layers.get("primary_read_text") or text_layers.get("primary_read_texts")
        if isinstance(primary, list) and primary:
            return [str(item) for item in primary if str(item).strip()]
        if isinstance(primary, str) and primary.strip():
            return [primary]
    for key in ["primary_read_text", "primary_read_texts"]:
        value = scene.get(key)
        if isinstance(value, list) and value:
            return [str(item) for item in value if str(item).strip()]
        if isinstance(value, str) and value.strip():
            return [value]
    values = scene.get("on_screen_text", [])
    if isinstance(values, list):
        return [str(item) for item in values if str(item).strip()]
    return []


def review(storyboard: dict[str, Any], frame_review: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    scenes = storyboard.get("scenes", []) if isinstance(storyboard.get("scenes"), list) else []
    if not scenes:
        issues.append("storyboard has no scenes")
    if frame_review.get("status") != "passed":
        issues.append("frame_review_report.json must be status=passed before visual_review")
    manual_review = frame_review.get("manual_review") if isinstance(frame_review.get("manual_review"), dict) else {}
    if manual_review.get("status") != "passed" or not str(manual_review.get("reviewer") or "").strip():
        issues.append("frame_review_report.json must include approved manual_review with reviewer")

    first_5_visual_changes = 0
    elapsed = 0.0
    dense_text_scenes = 0
    safe_zone_ok = 0
    unsafe_margin_scenes = 0
    low_motion_scenes = 0
    premium_type_count = 0
    layered_scene_count = 0
    quality_check_scene_count = 0
    source_class_scene_count = 0
    caption_template_scene_count = 0
    unused_structure_scene_count = 0
    animated_icon_scene_count = 0
    icon_sfx_scene_count = 0
    caption_templates_used: set[str] = set()
    scene_type_count: dict[str, int] = {}
    storyboard_quality_valid = story_quality_spec_valid(storyboard)
    metadata_quality_valid = metadata_quality_spec_valid(metadata)
    storyboard_quality_spec = storyboard.get("quality_spec") if isinstance(storyboard.get("quality_spec"), dict) else {}
    metadata_quality_spec = metadata.get("quality_spec") if isinstance(metadata.get("quality_spec"), dict) else {}
    storyboard_runtime_spec = {"runtime_choice": storyboard.get("runtime_choice")}
    voice_quality_valid = voice_provider_passes(metadata)
    sfx_quality_valid = sfx_policy_passes(storyboard_quality_spec, metadata_quality_spec)
    runtime_quality_valid = runtime_choice_passes(storyboard_runtime_spec, storyboard_quality_spec, metadata_quality_spec)

    for scene in scenes:
        duration = scene_duration(scene)
        if elapsed < 5:
            first_5_visual_changes += max(1, min(4, motion_layers(scene)))
        elapsed += duration

        text_items = scene_readability_text(scene)
        if isinstance(text_items, list) and sum(len(str(item)) for item in text_items) > 36:
            dense_text_scenes += 1

        safe_zone = scene.get("safe_zone", {})
        if isinstance(safe_zone, dict) and safe_zone_passes(safe_zone):
            safe_zone_ok += 1
        else:
            unsafe_margin_scenes += 1

        if motion_layers(scene) < 2:
            low_motion_scenes += 1

        visual = scene.get("visual", {})
        if isinstance(visual, dict) and visual_layers_pass(visual):
            layered_scene_count += 1
        if isinstance(visual, dict) and visual_quality_checks_pass(visual):
            quality_check_scene_count += 1
        unused_terms = unused_structure_terms(scene)
        if unused_terms:
            unused_structure_scene_count += 1
            scene_id = str(scene.get("id") or scene.get("scene_id") or f"scene_{len(scene_type_count) + 1}")
            issues.append(
                f"{scene_id} contains unused foreground/background framework terms: "
                + ", ".join(unused_terms[:6])
            )
        if scene_has_animated_icon_event(scene):
            animated_icon_scene_count += 1
            cues = scene_sfx_cues(scene)
            scene_id = str(scene.get("id") or scene.get("scene_id") or f"scene_{len(scene_type_count) + 1}")
            if cues and all(cue_is_voice_safe(cue) for cue in cues):
                icon_sfx_scene_count += 1
            else:
                issues.append(
                    f"{scene_id} has animated/status icon motion without voice-safe synchronized SFX cue"
                )
        scene_type = str(visual.get("scene_type", ""))
        scene_type_count[scene_type] = scene_type_count.get(scene_type, 0) + 1
        if scene_type in PREMIUM_SCENE_TYPES or str(visual.get("evidence_source", "")).startswith("real_"):
            premium_type_count += 1
        source_type = str(visual.get("asset_source_type", "")).strip()
        if source_type in ASSET_SOURCE_TYPES:
            source_class_scene_count += 1
        caption_template = str(visual.get("caption_template", "")).strip()
        if caption_template in CAPTION_TEMPLATES:
            caption_template_scene_count += 1
            caption_templates_used.add(caption_template)

    artifacts = frame_review.get("artifacts", {}) if isinstance(frame_review.get("artifacts"), dict) else {}
    missing_artifacts = [
        name for name in ["first_5s_contact_sheet", "full_video_contact_sheet"]
        if artifacts.get(name) and not exists(artifacts[name])
    ]
    if frame_review.get("status") == "failed":
        issues.append("frame_review_report.json is failed")
    if frame_review.get("status") != "passed":
        issues.append("frame_review_report.json must be status=passed before visual_review can pass")
    if missing_artifacts:
        warnings.append("frame review artifacts are referenced but missing: " + ", ".join(missing_artifacts))

    width = int(metadata.get("target_width") or metadata.get("width") or 0)
    height = int(metadata.get("target_height") or metadata.get("height") or 0)
    if width and height and (width < 1080 or height < 1080):
        warnings.append("metadata resolution is below 1080 on one side; verify mobile readability")

    scene_count = max(1, len(scenes))
    first_5s_score = 9.2 if first_5_visual_changes >= 2 else 6.8
    readability_score = 9.0 - dense_text_scenes * 0.6
    composition_score = 8.8 if safe_zone_ok == len(scenes) else 7.0
    motion_energy_score = 8.8 - low_motion_scenes * 0.7
    premium_feel_score = 8.4 + min(1.0, premium_type_count / scene_count)
    variety_score = 8.6 if len(scene_type_count) >= min(4, scene_count) else 7.4
    layering_score = 9.1 if layered_scene_count == len(scenes) else max(5.8, 8.6 - (len(scenes) - layered_scene_count) * 0.8)
    quality_check_score = 9.0 if quality_check_scene_count == len(scenes) else max(5.8, 8.4 - (len(scenes) - quality_check_scene_count) * 0.9)
    caption_variety_score = 8.9 if len(caption_templates_used) >= 2 and caption_template_scene_count == len(scenes) else 6.9
    source_class_score = 8.9 if source_class_scene_count == len(scenes) else 6.8
    sound_design_score = 8.9 if storyboard_quality_valid and metadata_quality_valid and voice_quality_valid and sfx_quality_valid else 6.4
    if animated_icon_scene_count and icon_sfx_scene_count != animated_icon_scene_count:
        sound_design_score = min(sound_design_score, 6.2)
    export_readiness_score = 9.0 if metadata_quality_valid else 6.8

    scores = {
        "first_5s_score": round(max(0.0, first_5s_score), 2),
        "readability_score": round(max(0.0, readability_score), 2),
        "composition_score": round(max(0.0, composition_score), 2),
        "motion_energy_score": round(max(0.0, motion_energy_score), 2),
        "premium_feel_score": round(max(0.0, premium_feel_score), 2),
        "variety_score": round(max(0.0, variety_score), 2),
        "layering_score": round(max(0.0, layering_score), 2),
        "quality_check_score": round(max(0.0, quality_check_score), 2),
        "caption_variety_score": round(max(0.0, caption_variety_score), 2),
        "source_class_score": round(max(0.0, source_class_score), 2),
        "sound_design_score": round(max(0.0, sound_design_score), 2),
        "export_readiness_score": round(max(0.0, export_readiness_score), 2),
    }
    overall = round(sum(scores.values()) / len(scores), 2)

    if first_5_visual_changes < 2:
        issues.append("first 5 seconds need at least 2 meaningful visual changes")
    if dense_text_scenes:
        warnings.append(f"{dense_text_scenes} scenes may be text-dense")
    if low_motion_scenes:
        issues.append(f"{low_motion_scenes} scenes have fewer than 2 motion layers")
    if unsafe_margin_scenes:
        issues.append(f"{unsafe_margin_scenes} scenes do not reserve enough top/bottom phone-safe margins")
    if not storyboard_quality_valid:
        issues.append("storyboard.quality_spec is missing or incomplete")
    if not metadata_quality_valid:
        issues.append("metadata.quality_spec must document high-quality render, bitrate, source asset, SFX, cover, and frame review policies")
    if not voice_quality_valid:
        issues.append("publish-ready videos need a documented approved natural voice sample; macOS say/scratch preview voices are not allowed")
    if not sfx_quality_valid:
        issues.append("publish-ready videos need subtle SFX; no-added-SFX policies are not allowed")
    if not runtime_quality_valid:
        issues.append("premium videos must use a HyperFrames final timeline; FFmpeg-only portrait card pipelines are not allowed")
    if layered_scene_count != len(scenes):
        issues.append("every scene needs at least 3 visual.design_layers")
    if quality_check_scene_count != len(scenes):
        issues.append("every scene visual.quality_checks must pass source/text/template/static checks")
    if unused_structure_scene_count:
        issues.append(
            f"{unused_structure_scene_count} scenes contain empty/placeholder/unused frames or rails; remove unused frameworks and use atmosphere, material depth, and negative space"
        )
    if icon_sfx_scene_count != animated_icon_scene_count:
        issues.append("animated/status icon scenes must include synchronized SFX cues that stay below narration and do not mask voice")
    if source_class_scene_count != len(scenes):
        issues.append("every scene must declare visual.asset_source_type")
    if caption_template_scene_count != len(scenes):
        issues.append("every scene must declare a supported visual.caption_template")
    if len(caption_templates_used) < 2:
        issues.append("publish-ready videos must use at least 2 caption templates")
    if composition_score < 8:
        issues.append("safe-zone reservation is incomplete")
    if layering_score < 8.5:
        issues.append("visual layering score must be >= 8.5")
    if quality_check_score < 8.5:
        issues.append("visual quality-check score must be >= 8.5")
    if caption_variety_score < 8.5:
        issues.append("caption template diversity score must be >= 8.5")
    if source_class_score < 8.5:
        issues.append("asset source classification score must be >= 8.5")
    if sound_design_score < 8.5:
        issues.append("sound design policy must be documented for premium videos")
    if export_readiness_score < 8.5:
        issues.append("export readiness must document high-quality render policy")
    if variety_score < 8:
        issues.append("scene type variety is weak; avoid a text-card slideshow")
    if overall < 8.2:
        issues.append("overall visual aesthetic score must be >= 8.2")

    return {
        "status": "passed" if not issues else "failed",
        "overall_visual_score": overall,
        "scores": scores,
        "blocking_issues": issues,
        "warnings": warnings,
        "signals": {
            "scene_count": len(scenes),
            "first_5_visual_changes": first_5_visual_changes,
            "dense_text_scenes": dense_text_scenes,
            "low_motion_scenes": low_motion_scenes,
            "safe_zone_scene_count": safe_zone_ok,
            "unsafe_margin_scenes": unsafe_margin_scenes,
            "layered_scene_count": layered_scene_count,
            "quality_check_scene_count": quality_check_scene_count,
            "unused_structure_scene_count": unused_structure_scene_count,
            "animated_icon_scene_count": animated_icon_scene_count,
            "icon_sfx_scene_count": icon_sfx_scene_count,
            "source_class_scene_count": source_class_scene_count,
            "caption_template_scene_count": caption_template_scene_count,
            "caption_template_count": len(caption_templates_used),
            "caption_templates_used": sorted(caption_templates_used),
            "storyboard_quality_spec_valid": storyboard_quality_valid,
            "metadata_quality_spec_valid": metadata_quality_valid,
            "voice_provider_approved": voice_quality_valid,
            "sfx_policy_valid": sfx_quality_valid,
            "runtime_choice_valid": runtime_quality_valid,
            "scene_type_count": scene_type_count,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Review visual aesthetics from storyboard and frame artifacts.")
    parser.add_argument("--storyboard", required=True, help="storyboard.json path")
    parser.add_argument("--frame-review", required=True, help="frame_review_report.json path")
    parser.add_argument("--metadata", required=True, help="metadata.json path")
    parser.add_argument("--out", help="visual_review.json path")
    args = parser.parse_args()

    storyboard_path = Path(args.storyboard)
    frame_review_path = Path(args.frame_review)
    metadata_path = Path(args.metadata)
    frame_report = load_json(frame_review_path)
    result = review(load_json(storyboard_path), frame_report, load_json(metadata_path))
    input_paths: list[Path] = [storyboard_path, frame_review_path, metadata_path]
    draft_path = frame_review_path.parent / "draft.mp4"
    if draft_path.exists():
        input_paths.append(draft_path)
        fresh_issues = verify_report_inputs(frame_report, [draft_path])
        if fresh_issues:
            result.setdefault("blocking_issues", []).extend(
                [f"frame_review_report.json stale for current draft: {issue}" for issue in fresh_issues]
            )
            result["status"] = "failed"
    else:
        result.setdefault("blocking_issues", []).append("internal/draft.mp4 missing; cannot verify frame review freshness")
        result["status"] = "failed"
    if result.get("blocking_issues"):
        result["status"] = "failed"
    write_report_with_fingerprints(result, input_paths)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
