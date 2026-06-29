#!/usr/bin/env python3
"""Validate asset_manifest.json before HyperFrames QA."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Optional, Tuple

from asset_prompt_contract import (
    background_semantic_binding_issues as contract_background_semantic_binding_issues,
    visual_director_prompt_issues as contract_visual_director_prompt_issues,
)


EVIDENCE_TYPES = {
    "real_ui_screenshot",
    "real_ui_recording",
    "terminal_output",
    "code_or_file_proof",
    "official_doc_screenshot",
}
ASSET_SOURCE_TYPES = {"proof", "support", "generated", "free_stock", "audio", "subtitle"}
BACKGROUND_PROMPT_PACK_NAMES = ("background_prompt_pack.md", "ai_asset_prompt_pack.md")
GENERATED_IMAGE_PROVIDER_TERMS = {
    "gpt-image-2",
    "gpt_image_2",
    "gpt image 2",
    "codex_builtin_imagegen",
    "codex built-in imagegen",
    "codex built in imagegen",
    "imagegen_builtin",
    "built_in_imagegen",
}
LOCAL_GENERATED_PLACEHOLDER_TERMS = {
    "local_pil_renderer",
    "local_pil_renderer_from_prompt_pack",
    "pillow",
    "pil_renderer",
}
ALLOWED_EVIDENCE_VISUAL_TYPES = {
    "real_source_crop",
    "clean_citation_card",
    "abstract_non_official_diagram",
    "real_ui_capture",
    "terminal_or_file_proof",
    "none",
}
FORBIDDEN_EVIDENCE_VISUAL_TERMS = {
    "fake_official_screenshot",
    "tiny_unreadable_source_panel",
    "pseudo_source_card",
    "假官方截图",
    "不可读小证据",
}
LOCAL_SUMMARY_CARD_TERMS = {
    "official_source_card_local_render",
    "source card",
    "summary card",
    "local original card",
    "local render",
    "本地原创证据卡",
    "原创证据卡",
    "自制摘要卡",
}
FORBIDDEN_PROVIDER_TERMS = {
    "elevenlabs",
    "runway",
    "kling",
    "heygen",
    "ressemble",
    "veo",
    "paid stock",
    "paid design",
    "paid video",
    "subscription asset",
    "pinterest",
    "付费素材",
    "付费设计",
    "付费视频",
    "订阅素材",
}
APPROVAL_TERMS = {"explicit user approval", "approved paid exception", "用户明确批准", "用户批准"}
DEFAULT_AI_BACKGROUND_RESOLUTION = (1920, 1080)
VERTICAL_REFERENCE_RESOLUTION = (1080, 1920)
BACKGROUND_SEMANTIC_REQUIRED_FIELDS = (
    "visual_thesis",
    "topic_binding",
    "information_job",
    "background_role",
)
BACKGROUND_SEMANTIC_MIN_CHARS = {
    "visual_thesis": 24,
    "topic_binding": 24,
    "information_job": 24,
    "background_role": 16,
}
GENERIC_BACKGROUND_BINDING_VALUES = {
    "premium information stage",
    "calm premium information stage",
    "quiet stage",
    "premium tech background",
    "高级科技感背景",
    "高级背景",
    "科技感背景",
}
VISUAL_DIRECTOR_REQUIRED_FIELDS = (
    "scene_id",
    "narration_line_supported",
    "scene_function",
    "visual_archetype",
    "brightness_grade",
    "palette_family",
    "material_family",
    "layout_family",
    "energy_level",
    "visual_thesis",
    "topic_binding",
    "beginner_usefulness",
    "information_job",
    "viewer_takeaway",
    "composition",
    "foreground",
    "midground",
    "background",
    "camera_lens",
    "lighting",
    "material_texture",
    "color_hierarchy",
    "color_system",
    "depth_layering",
    "text_safe_zones",
    "motion_usage",
    "animation_affordance",
    "primary_animated_object",
    "dark_light_motion_rule",
    "negative_prompt",
    "regeneration_criteria",
    "diversity_check",
)
VISUAL_DIRECTOR_MIN_CHARS = {
    "scene_id": 2,
    "narration_line_supported": 16,
    "scene_function": 8,
    "visual_archetype": 10,
    "brightness_grade": 8,
    "palette_family": 10,
    "material_family": 10,
    "layout_family": 10,
    "energy_level": 10,
    "visual_thesis": 24,
    "topic_binding": 24,
    "beginner_usefulness": 20,
    "information_job": 24,
    "viewer_takeaway": 18,
    "composition": 32,
    "foreground": 20,
    "midground": 20,
    "background": 20,
    "camera_lens": 16,
    "lighting": 20,
    "material_texture": 20,
    "color_hierarchy": 20,
    "color_system": 40,
    "depth_layering": 24,
    "text_safe_zones": 20,
    "motion_usage": 24,
    "animation_affordance": 24,
    "primary_animated_object": 12,
    "dark_light_motion_rule": 24,
    "negative_prompt": 28,
    "regeneration_criteria": 28,
    "diversity_check": 24,
}
GENERIC_VISUAL_PROMPT_VALUES = {
    "高级",
    "高级感",
    "高级科技感",
    "高级科技感背景",
    "科技感",
    "科技感背景",
    "未来感",
    "赛博",
    "赛博霓虹",
    "酷炫",
    "炫酷",
    "震撼",
    "真实感",
    "设计感",
    "4k",
    "8k",
    "cinematic",
    "premium",
    "premium tech",
    "premium tech background",
    "futuristic",
    "cyberpunk",
    "high quality",
    "ultra detailed",
    "cool background",
    "awesome background",
}
GENERIC_PROMPT_PHRASES = {
    "高级一点",
    "随便高级",
    "做高级",
    "更炫",
    "更酷",
    "爆款",
    "大片感",
    "high quality",
    "ultra detailed",
    "trending on artstation",
    "cinematic 4k",
    "premium tech background",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def resolve_asset_path(raw_path: str, manifest_path: Path, project: Optional[Path]) -> Path:
    raw_path = raw_path.split("#", 1)[0]
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    if project:
        candidate = project / path
        if candidate.exists():
            return candidate
    return manifest_path.parent / path


def parse_resolution(value: str) -> Optional[Tuple[int, int]]:
    match = re.search(r"(\d{2,5})\s*x\s*(\d{2,5})", value, flags=re.IGNORECASE)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def has_forbidden_provider(text: str) -> bool:
    lowered = text.lower()
    if any(term in lowered for term in APPROVAL_TERMS):
        return False
    return any(term in lowered for term in FORBIDDEN_PROVIDER_TERMS)


def is_local_summary_card(asset: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(asset.get("type", "")),
            str(asset.get("provider", "")),
            str(asset.get("source", "")),
            str(asset.get("source_note", "")),
            str(asset.get("qa_notes", "")),
        ]
    ).lower()
    if any(term in text for term in LOCAL_SUMMARY_CARD_TERMS):
        return True
    return "not an official screenshot" in text or "summarizing official" in text


def is_background_plate(asset: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(asset.get("asset_role", "")),
            str(asset.get("role", "")),
            str(asset.get("type", "")),
            str(asset.get("source", "")),
            str(asset.get("source_note", "")),
            str(asset.get("qa_notes", "")),
        ]
    ).lower()
    return "background_plate" in text or "background plate" in text or "背景" in text


def normalized_text(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", " ").replace("_", " ")


def compact_text(value: Any) -> str:
    return re.sub(r"\s+", " ", normalized_text(value))


def vertical_reference_exception_allowed(manifest: dict[str, Any]) -> bool:
    exception = manifest.get("format_exception")
    if not isinstance(exception, dict):
        return False
    status = normalized_text(exception.get("status"))
    mode = normalized_text(exception.get("mode"))
    basis = normalized_text(json.dumps(exception, ensure_ascii=False))
    return (
        status in {"approved", "locked", "passed"}
        and mode == "reference driven lightweight vertical"
        and "reference" in basis
        and "lightweight" in basis
        and "proof heavy" in basis
    )


def background_resolution_allowed(manifest: dict[str, Any], resolution: Optional[Tuple[int, int]]) -> bool:
    if resolution == DEFAULT_AI_BACKGROUND_RESOLUTION:
        return True
    return resolution == VERTICAL_REFERENCE_RESOLUTION and vertical_reference_exception_allowed(manifest)


NORMALIZED_GENERIC_BACKGROUND_BINDING_VALUES = {compact_text(item) for item in GENERIC_BACKGROUND_BINDING_VALUES}
NORMALIZED_GENERIC_VISUAL_PROMPT_VALUES = {compact_text(item) for item in GENERIC_VISUAL_PROMPT_VALUES}


def is_generic_visual_prompt_value(value: Any) -> bool:
    text = compact_text(value)
    if not text:
        return False
    if text in NORMALIZED_GENERIC_VISUAL_PROMPT_VALUES:
        return True
    if len(text) <= 30 and any(term in text for term in NORMALIZED_GENERIC_VISUAL_PROMPT_VALUES):
        return True
    return False


def prompt_path_text(asset: dict[str, Any], manifest_path: Path, project: Optional[Path]) -> str:
    raw_prompt_path = str(asset.get("prompt_path", "")).strip()
    if not raw_prompt_path:
        return ""
    resolved = resolve_asset_path(raw_prompt_path, manifest_path, project)
    if not exists(resolved):
        return ""
    try:
        return resolved.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def background_semantic_binding_issues(asset: dict[str, Any]) -> list[str]:
    asset_id = str(asset.get("asset_id") or "unknown")
    issues: list[str] = []
    for key in BACKGROUND_SEMANTIC_REQUIRED_FIELDS:
        value = str(asset.get(key, "")).strip()
        if not value:
            issues.append(f"{asset_id}: background_plate must document {key} so the generated background is bound to the selected topic")
            continue
        if len(value) < BACKGROUND_SEMANTIC_MIN_CHARS[key]:
            issues.append(f"{asset_id}: background_plate {key} is too vague; describe the topic-specific information job")
        if compact_text(value) in NORMALIZED_GENERIC_BACKGROUND_BINDING_VALUES:
            issues.append(f"{asset_id}: background_plate {key} is generic; it must describe the actual AI topic, not only a premium stage")
    return issues


def visual_director_prompt_issues(asset: dict[str, Any], manifest_path: Path, project: Optional[Path]) -> list[str]:
    asset_id = str(asset.get("asset_id") or "unknown")
    issues: list[str] = []
    for key in VISUAL_DIRECTOR_REQUIRED_FIELDS:
        value = str(asset.get(key, "")).strip()
        if not value:
            issues.append(f"{asset_id}: generated_visual must document visual director field {key}")
            continue
        if len(value) < VISUAL_DIRECTOR_MIN_CHARS[key]:
            issues.append(f"{asset_id}: visual director field {key} is too short; describe the image's concrete information job and shot design")
        if key != "negative_prompt" and is_generic_visual_prompt_value(value):
            issues.append(f"{asset_id}: visual director field {key} is generic; replace taste words with concrete shot design")

    prompt_text = prompt_path_text(asset, manifest_path, project)
    prompt_surface = "\n".join(
        [prompt_text]
        + [str(asset.get(key, "")) for key in VISUAL_DIRECTOR_REQUIRED_FIELDS]
        + [str(asset.get("source", "")), str(asset.get("source_note", "")), str(asset.get("qa_notes", ""))]
    ).lower()
    compact_surface = compact_text(prompt_surface)
    for phrase in GENERIC_PROMPT_PHRASES:
        normalized_phrase = compact_text(phrase)
        if normalized_phrase and normalized_phrase in compact_surface:
            issues.append(f"{asset_id}: generated_visual prompt uses vague material phrase `{phrase}`; rewrite as a concrete visual director brief")
            break

    if prompt_text:
        prompt_text_lower = prompt_text.lower()
        required_marker_groups = {
            "scene function": ("scene function", "scene_function", "场景功能", "镜头功能"),
            "visual archetype": ("visual archetype", "visual_archetype", "视觉原型", "视觉类型"),
            "brightness grade": ("brightness grade", "brightness_grade", "亮度等级", "明暗等级"),
            "palette family": ("palette family", "palette_family", "色彩方案", "调色家族"),
            "material family": ("material family", "material_family", "材质家族"),
            "layout family": ("layout family", "layout_family", "布局家族"),
            "composition": ("composition", "构图", "画面结构"),
            "foreground": ("foreground", "前景"),
            "midground": ("midground", "中景"),
            "background": ("background", "背景"),
            "lighting": ("lighting", "light", "光线", "灯光"),
            "material": ("material", "texture", "材质", "纹理"),
            "color system": ("color system", "color_system", "色彩系统"),
            "depth layering": ("depth/layering", "depth layering", "depth_layering", "空间层", "层次"),
            "motion": ("motion", "animation", "动效", "运动"),
            "primary animated object": ("primary animated object", "primary_animated_object", "主运动对象"),
            "dark light motion rule": ("dark/light motion rule", "dark_light_motion_rule", "明暗运动规则"),
            "negative": ("negative", "avoid", "no ", "避免", "负面"),
            "regeneration": ("regeneration", "regenerate", "重生成", "返工"),
            "diversity check": ("diversity check", "diversity_check", "多样性检查"),
        }
        missing_markers = [
            marker
            for marker, alternatives in required_marker_groups.items()
            if not any(alternative in prompt_text_lower for alternative in alternatives)
        ]
        if missing_markers:
            issues.append(
                f"{asset_id}: prompt_path brief is missing visual director sections: {', '.join(missing_markers)}"
            )

    if compact_text(asset.get("motion_usage")) == compact_text(asset.get("animation_affordance")):
        issues.append(f"{asset_id}: motion_usage and animation_affordance must not be duplicated; one explains HyperFrames use, the other explains animatable layers/zones")
    return issues


def generated_provider_valid(asset: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(asset.get("provider", "")),
            str(asset.get("model", "")),
            str(asset.get("generation_provider", "")),
            str(asset.get("generation_method", "")),
        ]
    ).lower()
    return any(term in text for term in GENERATED_IMAGE_PROVIDER_TERMS) and not any(
        term in text for term in LOCAL_GENERATED_PLACEHOLDER_TERMS
    )


def generated_prompt_fields_valid(asset: dict[str, Any], manifest_path: Path, project: Optional[Path]) -> list[str]:
    asset_id = str(asset.get("asset_id") or "unknown")
    issues: list[str] = []
    if not generated_provider_valid(asset):
        issues.append(
            f"{asset_id}: generated_visual must document gpt-image-2 or Codex built-in ImageGen as provider/model; local PIL/render placeholders are not valid AI image generation"
        )
    for key in ["model", "prompt_id", "prompt_path", "evidence_boundary"]:
        if not str(asset.get(key, "")).strip():
            issues.append(f"{asset_id}: generated_visual must document {key}")
    if asset.get("unique_prompt") is not True:
        issues.append(f"{asset_id}: generated_visual must set unique_prompt=true; do not reuse one generic prompt for multiple images")
    prompt_path = str(asset.get("prompt_path", "")).strip()
    if prompt_path:
        resolved = resolve_asset_path(prompt_path, manifest_path, project)
        if not exists(resolved):
            issues.append(f"{asset_id}: prompt_path file missing or empty: {prompt_path}")
    boundary_text = str(asset.get("evidence_boundary", "")).lower()
    if not any(term in boundary_text for term in ["not evidence", "support only", "not proof", "非证据", "不作为证据"]):
        issues.append(f"{asset_id}: evidence_boundary must say the generated visual is support only and not evidence")
    return issues


def local_support_background_allowed(manifest: dict[str, Any], asset: dict[str, Any], resolution: Optional[Tuple[int, int]]) -> bool:
    """Allow a truthful local support background only when the manifest opts in.

    This is for Codex app runs where the user authorizes the paid Codex built-in
    route but the in-chat ImageGen result cannot be exported as a project file.
    The asset must stay classified as support, never as generated or proof.
    """
    if manifest.get("allow_local_support_background_plate") is not True:
        return False
    if asset.get("type") not in {"designed_card", "other"}:
        return False
    if asset.get("asset_source_type") != "support":
        return False
    if asset.get("is_evidence") is not False:
        return False
    if not background_resolution_allowed(manifest, resolution):
        return False
    policy_text = " ".join(
        [
            str(manifest.get("local_support_background_policy", "")),
            str(asset.get("generation_method", "")),
            str(asset.get("source_note", "")),
            str(asset.get("qa_notes", "")),
        ]
    ).lower()
    return (
        "user_approved" in policy_text
        and "support" in policy_text
        and any(term in policy_text for term in ["not evidence", "not proof", "non-official", "not official"])
    )


def background_prompt_pack_exists(manifest_path: Path) -> bool:
    internal = manifest_path.parent
    return any((internal / name).exists() and (internal / name).stat().st_size > 0 for name in BACKGROUND_PROMPT_PACK_NAMES)


def validate(manifest: dict[str, Any], manifest_path: Path, project: Optional[Path]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    assets = manifest.get("assets", [])
    scene_usage: dict[str, int] = {}
    evidence_count = 0
    source_class_count = 0
    provider_count = 0
    background_plate_count = 0
    background_plate_valid_count = 0
    background_plate_semantic_count = 0
    generated_visual_prompt_count = 0
    visual_director_prompt_count = 0
    generated_prompt_ids: dict[str, str] = {}
    generated_prompt_paths: dict[str, str] = {}

    if manifest.get("background_plate_required", True) is not False and not background_prompt_pack_exists(manifest_path):
        issues.append("background_prompt_pack.md is required before AI knowledge video asset generation")

    if not isinstance(assets, list):
        issues.append("assets must be an array")
        assets = []

    for index, asset in enumerate(assets, start=1):
        asset_id = str(asset.get("asset_id") or f"asset_{index}")
        asset_type = str(asset.get("type", ""))
        asset_source_type = str(asset.get("asset_source_type", "")).strip()
        provider = str(asset.get("provider", "")).strip()
        raw_path = str(asset.get("path", ""))
        asset_path = resolve_asset_path(raw_path, manifest_path, project) if raw_path else manifest_path

        if asset_source_type in ASSET_SOURCE_TYPES:
            source_class_count += 1
        else:
            issues.append(f"{asset_id}: asset_source_type must be proof/support/generated/free_stock/audio/subtitle")

        background_plate = is_background_plate(asset)
        if background_plate:
            background_plate_count += 1

        if provider:
            provider_count += 1
        else:
            issues.append(f"{asset_id}: provider is required")

        provider_surface = " ".join(
            [
                provider,
                str(asset.get("source", "")),
                str(asset.get("source_note", "")),
                raw_path,
            ]
        )
        if has_forbidden_provider(provider_surface):
            issues.append(f"{asset_id}: disabled paid/scraping provider used without explicit approval")

        if not raw_path:
            issues.append(f"{asset_id}: missing path")
        elif not exists(asset_path):
            issues.append(f"{asset_id}: asset file missing or empty: {raw_path}")

        for scene_id in asset.get("used_in_scenes", []) or []:
            scene_usage[scene_id] = scene_usage.get(scene_id, 0) + 1

        is_evidence = bool(asset.get("is_evidence"))
        if is_evidence:
            evidence_count += 1
            if asset_type not in EVIDENCE_TYPES:
                issues.append(f"{asset_id}: evidence asset must use a real proof type, not {asset_type}")
            if asset_source_type != "proof":
                issues.append(f"{asset_id}: evidence asset must use asset_source_type=proof")
            if is_local_summary_card(asset):
                issues.append(
                    f"{asset_id}: local summary/designed cards cannot be counted as proof; use real UI/doc/terminal proof or classify as support"
                )
            evidence_visual_type = str(asset.get("evidence_visual_type", "")).strip()
            if evidence_visual_type:
                if evidence_visual_type not in ALLOWED_EVIDENCE_VISUAL_TYPES:
                    issues.append(f"{asset_id}: unsupported evidence_visual_type={evidence_visual_type}")
                if evidence_visual_type in {"real_source_crop", "clean_citation_card"}:
                    if not str(asset.get("source_url", "")).strip() and not str(asset.get("source_title", "")).strip():
                        issues.append(f"{asset_id}: source evidence needs source_url or source_title")
                    if asset.get("must_be_readable") is not True:
                        issues.append(f"{asset_id}: source evidence must set must_be_readable=true")
                    try:
                        visible_width = int(asset.get("min_visible_width_px") or 0)
                    except Exception:
                        visible_width = 0
                    if visible_width and visible_width < 900:
                        issues.append(f"{asset_id}: min_visible_width_px must be >= 900 for readable source evidence")
            evidence_surface = " ".join(
                [
                    str(asset.get("evidence_visual_type", "")),
                    str(asset.get("source_note", "")),
                    str(asset.get("qa_notes", "")),
                ]
            ).lower()
            if any(term in evidence_surface for term in FORBIDDEN_EVIDENCE_VISUAL_TERMS):
                issues.append(f"{asset_id}: forbidden or fake/tiny evidence visual is not allowed")
        elif asset_source_type == "proof" and is_local_summary_card(asset):
            issues.append(f"{asset_id}: local summary/designed cards cannot use asset_source_type=proof")
        if asset_type == "generated_visual" and is_evidence:
            issues.append(f"{asset_id}: AI-generated visual cannot be counted as real evidence")
        if asset_type == "generated_visual" and asset_source_type == "proof":
            issues.append(f"{asset_id}: generated visual cannot use asset_source_type=proof")
        if asset_type == "generated_visual":
            generated_issues = generated_prompt_fields_valid(asset, manifest_path, project)
            issues.extend(generated_issues)
            if not generated_issues:
                generated_visual_prompt_count += 1
            director_issues = contract_visual_director_prompt_issues(
                asset,
                prompt_path_text(asset, manifest_path, project),
            )
            issues.extend(director_issues)
            duplicate_issues: list[str] = []
            prompt_id = str(asset.get("prompt_id", "")).strip()
            if prompt_id:
                existing_asset = generated_prompt_ids.get(prompt_id)
                if existing_asset and existing_asset != asset_id:
                    duplicate_issues.append(
                        f"{asset_id}: generated_visual reuses prompt_id={prompt_id} from {existing_asset}; every generated image needs its own prompt card"
                    )
                else:
                    generated_prompt_ids[prompt_id] = asset_id
            prompt_path = str(asset.get("prompt_path", "")).strip()
            if prompt_path:
                existing_asset = generated_prompt_paths.get(prompt_path)
                if existing_asset and existing_asset != asset_id:
                    duplicate_issues.append(
                        f"{asset_id}: generated_visual reuses prompt_path={prompt_path} from {existing_asset}; do not batch multiple images from one generic prompt"
                    )
                else:
                    generated_prompt_paths[prompt_path] = asset_id
            issues.extend(duplicate_issues)
            if not generated_issues and not director_issues and not duplicate_issues:
                visual_director_prompt_count += 1
        if asset_source_type == "free_stock" and is_evidence:
            issues.append(f"{asset_id}: free_stock assets cannot be counted as evidence")

        resolution = parse_resolution(str(asset.get("resolution", "")))
        if not resolution:
            warnings.append(f"{asset_id}: resolution is missing or not formatted as WIDTHxHEIGHT")
        elif resolution[0] < 720 or resolution[1] < 720:
            warnings.append(f"{asset_id}: resolution may be too low for readable mobile video")

        if asset.get("contains_private_info") is True:
            issues.append(f"{asset_id}: contains private information")
        if asset.get("contains_contact_info") is True:
            issues.append(f"{asset_id}: contains contact information")
        if asset.get("contains_qr_code") is True:
            issues.append(f"{asset_id}: contains QR code")
        if asset.get("risk") == "high":
            issues.append(f"{asset_id}: high-risk asset requires replacement or documented approval")

        copyright_status = str(asset.get("copyright_status", ""))
        if copyright_status == "unknown":
            warnings.append(f"{asset_id}: copyright status is unknown")
        source_note = str(asset.get("source_note", ""))
        if asset_type == "generated_visual" and any(term in source_note for term in ["官方", "真实", "截图", "评价", "认证"]):
            issues.append(f"{asset_id}: generated visual appears to claim real or official proof")

        if background_plate:
            semantic_issues = contract_background_semantic_binding_issues(asset)
            issues.extend(semantic_issues)
            if not semantic_issues:
                background_plate_semantic_count += 1
            local_support_ok = local_support_background_allowed(manifest, asset, resolution)
            if asset_type != "generated_visual" and not local_support_ok:
                issues.append(f"{asset_id}: background_plate must use type=generated_visual")
            if asset_source_type != "generated" and not local_support_ok:
                issues.append(f"{asset_id}: background_plate must use asset_source_type=generated")
            if is_evidence:
                issues.append(f"{asset_id}: background_plate must not be counted as evidence")
            if not background_resolution_allowed(manifest, resolution):
                issues.append(f"{asset_id}: background_plate must be 1920x1080 for AI knowledge videos unless an approved vertical reference exception is documented")
            boundary_text = f"{source_note} {asset.get('qa_notes', '')}".lower()
            if not any(term in boundary_text for term in ["not official", "not factual proof", "support background", "support visual", "非证据", "不作为证据"]):
                issues.append(f"{asset_id}: background_plate must document that it is support-only, not evidence")
            if (
                asset_type == "generated_visual"
                and asset_source_type == "generated"
                and not is_evidence
                and background_resolution_allowed(manifest, resolution)
                and not semantic_issues
            ):
                background_plate_valid_count += 1
            if local_support_ok and not semantic_issues:
                background_plate_valid_count += 1

    repeated_scenes = [scene_id for scene_id, count in scene_usage.items() if count > 4]
    for scene_id in repeated_scenes:
        warnings.append(f"{scene_id}: many assets reference the same scene; verify duplicate usage is intentional")

    if assets and evidence_count == 0:
        issues.append("asset manifest has no real evidence assets")
    if manifest.get("background_plate_required", True) is not False and background_plate_valid_count == 0:
        if manifest.get("allow_local_support_background_plate") is True:
            issues.append("AI knowledge asset manifest must include at least one valid generated or explicitly user-approved local support background_plate")
        else:
            issues.append("AI knowledge asset manifest must include at least one valid generated text-free background_plate")

    return {
        "status": "passed" if not issues else "failed",
        "asset_count": len(assets),
        "evidence_asset_count": evidence_count,
        "source_class_count": source_class_count,
        "provider_count": provider_count,
        "background_plate_count": background_plate_count,
        "background_plate_valid_count": background_plate_valid_count,
        "background_plate_semantic_count": background_plate_semantic_count,
        "generated_visual_prompt_count": generated_visual_prompt_count,
        "visual_director_prompt_count": visual_director_prompt_count,
        "blocking_issues": issues,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate asset manifest safety and evidence quality.")
    parser.add_argument("--manifest", required=True, help="asset_manifest.json path")
    parser.add_argument("--project", help="Optional project root for relative asset paths")
    parser.add_argument("--out", help="Output asset_validation.json path")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    project = Path(args.project) if args.project else None
    report = validate(load_json(manifest_path), manifest_path, project)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
