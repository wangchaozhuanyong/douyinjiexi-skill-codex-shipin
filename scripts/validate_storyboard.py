#!/usr/bin/env python3
"""Validate V3 storyboard gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from check_content_alignment import review_storyboard_alignment


EVIDENCE_TYPES = {"real_ui_demo", "screenshot_proof", "comparison", "proof_wall", "code_or_file_proof", "result_reveal"}
REAL_PROOF_SCENE_TYPES = {"real_ui_demo", "screenshot_proof", "proof_wall", "code_or_file_proof"}
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
    "provider_policy",
    "runtime_choice",
    "caption_template_plan",
    "timeline_contract_ref",
    "narration_continuity_policy",
]
QUALITY_CHECK_REQUIRED = ["source_resolution_ok", "text_safe", "not_template_like", "not_static_dump"]
PREMIUM_MOTION_REQUIRED = [
    "purpose",
    "entrance",
    "stagger",
    "keyword_motion",
    "camera_motion",
    "layering",
    "transition",
    "caption_motion",
    "glow",
    "audio_reactive",
    "negative_motion",
]
ADVANCED_TRANSITION_RECIPES = {
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
BASIC_TRANSITION_ONLY_TERMS = [
    "fade",
    "fade-up",
    "fade up",
    "crossfade",
    "blur crossfade",
    "push slide",
    "slide",
    "hard cut",
    "cut",
    "zoom",
    "wipe",
    "diagonal sweep",
    "diagonal line",
    "diagonal scan",
    "random light streak",
    "decoration-only line",
    "empty rail",
    "斜线扫光",
    "斜线扫描",
    "横向小光条",
    "装饰线",
    "空导轨",
    "旧卡片轮播",
]
ANIMATED_ICON_TERMS = [
    "animated icon",
    "dynamic icon",
    "status icon",
    "status node",
    "lock pulse",
    "clean lock",
    "module lock",
    "check mark",
    "checklist node",
    "cursor click",
    "cursor packet",
    "data node",
    "node emits",
    "节点",
    "动态图标",
    "动态 图标",
    "状态图标",
    "状态节点",
    "锁定脉冲",
    "勾选",
    "光标点击",
]
SFX_CUE_FIELDS = ["sfx_cues", "audio_cues", "icon_audio_cues"]
SFX_TIME_FIELDS = ["time_sec", "time_offset_sec", "offset_sec", "start_sec"]
VOICE_SAFE_SFX_TERMS = [
    "below narration",
    "below voice",
    "under narration",
    "under voice",
    "no masking",
    "not mask",
    "does not mask",
    "不影响人声",
    "不压人声",
    "不盖人声",
    "不盖住旁白",
    "低于旁白",
    "低于人声",
    "-12db",
    "-14db",
    "-16db",
    "-18db",
    "12db-18db",
    "12dB-18dB",
]
SFX_MASKING_BAD_TERMS = [
    "over voice",
    "above voice",
    "mask voice",
    "mask narration",
    "loud foreground",
    "foreground sfx",
    "压过人声",
    "盖住人声",
    "盖住旁白",
    "抢人声",
]
SYNC_REQUIRED = [
    "voice_start",
    "voice_end",
    "caption_start",
    "caption_end",
    "narration_track",
    "transition_audio_policy",
    "max_audio_gap_ms",
    "audio_bridge",
]
MOTION_PURPOSE_TERMS = {"reveal", "compare", "verify", "warn", "connect", "summarize", "focus", "guide"}
FORBIDDEN_MOTION_CN = ["炫酷", "震撼", "高级一点", "酷一点", "更炫", "随便高级"]
FORBIDDEN_MOTION_EN = ["crazy", "explosive", "flashy", "excessive", "chaotic"]
NEGATION_PREFIXES = ("no ", "not ", "avoid ", "without ")
MAX_TRANSITION_AUDIO_GAP_MS = 120
CONTINUOUS_NARRATION_TERMS = ["continuous", "root", "single", "bed", "连续", "根音频", "音频床"]
VISUAL_ONLY_AUDIO_TERMS = ["visual-only", "visual only", "no restart", "no mute", "not restart", "not mute", "不停", "不断", "不重启", "不静音"]
FORBIDDEN_AUDIO_BRIDGE_TERMS = ["restart", "mute", "silence gap", "fade out voice", "stop voice", "重启", "静音", "断音", "停顿"]
ACCEPTED_QUALITY_LEVELS = {"high_quality", "breakout_potential"}
ACCEPTED_PROVIDER_POLICY = "free_first_local_or_authorized_openai_only"
ASSET_SOURCE_TYPES = {"proof", "support", "generated", "free_stock"}
DIRECTOR_REQUIRED = [
    "shot_id",
    "duration_sec",
    "shot_type",
    "layout_family",
    "camera_scale",
    "camera_motion",
    "visual_subject",
    "primary_action",
    "viewer_focus",
    "operation_elements",
    "evidence",
    "on_screen_text",
    "forbidden_risks",
]
DIRECTOR_REQUIRED_SHOT_TYPES = {"hook_conflict", "source_evidence", "operation_simulation", "final_template"}
DIRECTOR_OPERATION_ELEMENTS = {
    "task_brief_panel",
    "repo_or_file_tree",
    "risk_list",
    "module_change",
    "test_or_check_output",
    "evidence_result_card",
}
DIRECTOR_ALLOWED_EVIDENCE_TYPES = {
    "none",
    "real_source_crop",
    "clean_citation_card",
    "abstract_non_official_diagram",
    "real_ui_capture",
    "terminal_or_file_proof",
}
DIRECTOR_FORBIDDEN_EVIDENCE_TYPES = {
    "fake_official_screenshot",
    "tiny_unreadable_source_panel",
    "pseudo_source_card",
}
DIRECTOR_TEXT_ROLES = {"primary", "secondary", "approved_primary_text"}
MAX_SAME_LAYOUT_CONSECUTIVE = 2
MIN_DIRECTOR_SHOT_TYPES = 4
MIN_OPERATION_SHOTS = 2
MIN_OPERATION_ELEMENT_COVERAGE = 2
TIMELINE_DURATION_TOLERANCE_SEC = 0.3
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
STACK_TRIGGER_TERMS = ["codex", "skill", "插件", "remotion", "hyperframes", "imagegen", "image gen", "heygen"]
PLUGIN_TRIGGER_TERMS = [
    "插件",
    "plugin",
    "plugins",
    "browser plugin",
    "浏览器插件",
    "github",
    "hugging face",
    "huggingface",
    "openai developers",
    "heygen",
]
SIX_PLUGIN_TERMS = ["6 个", "6个", "六个", "six"]
CORE_CODEX_PLUGINS = {
    "browser": {"browser"},
    "github": {"github"},
    "hugging face": {"hugging face", "huggingface"},
    "hyperframes": {"hyperframes"},
    "openai developers": {"openai developers", "openai developer", "openai"},
    "heygen": {"heygen"},
}
PLUGIN_AVAILABILITY = {
    "available_in_session",
    "available_if_authenticated",
    "local_cli_or_skill",
    "needs_user_approval",
    "optional_blocked",
    "not_available",
}
MIN_SAFE_MARGINS = {
    "top_margin_px": 240,
    "bottom_margin_px": 360,
    "left_margin_px": 72,
    "right_margin_px": 180,
}
MIN_NORMAL_TTS_SPEED = 0.95
MAX_NORMAL_TTS_SPEED = 1.03
MAX_USER_APPROVED_TTS_SPEED = 1.10
NORMAL_VOICE_SPEED_POLICIES = {"normal", "normal_speed"}
USER_APPROVED_VOICE_SPEED_POLICIES = {"user_approved_1_1x", "explicit_user_override", "user_requested"}
USER_APPROVAL_MARKERS = ["user requested", "user approved", "explicit user", "用户要求", "用户明确", "用户批准"]
AI_KNOWLEDGE_TERMS = [
    "ai",
    "chatgpt",
    "gemini",
    "openai",
    "codex",
    "agent",
    "skill",
    "插件",
    "自动化",
    "ai 工具",
    "ai工具",
    "ai 教程",
    "ai教程",
    "ai 视频",
    "ai视频",
]
AI_KNOWLEDGE_WIDTH = 1920
AI_KNOWLEDGE_HEIGHT = 1080
VERTICAL_REFERENCE_WIDTH = 1080
VERTICAL_REFERENCE_HEIGHT = 1920
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


def motion_layer_count(motion: dict[str, Any]) -> int:
    keys = ["background_motion", "foreground_motion", "callout_motion", "transition"]
    return sum(1 for key in keys if str(motion.get(key, "")).strip() and str(motion.get(key)).lower() != "none")


def contains_with_negative_context(text: str, term: str) -> bool:
    start = 0
    while True:
        index = text.find(term, start)
        if index == -1:
            return False
        prefix = text[max(0, index - 12) : index]
        if not any(prefix.endswith(item) for item in NEGATION_PREFIXES):
            return True
        start = index + len(term)


def forbidden_motion_terms(text: str) -> list[str]:
    lowered = text.lower()
    found: list[str] = []
    found.extend(term for term in FORBIDDEN_MOTION_CN if term in text)
    found.extend(term for term in FORBIDDEN_MOTION_EN if contains_with_negative_context(lowered, term))
    return found


def advanced_transition_recipes(text: str) -> set[str]:
    lowered = text.lower().replace("-", "_").replace(" ", "_")
    return {recipe for recipe in ADVANCED_TRANSITION_RECIPES if recipe in lowered}


def basic_transition_only_terms(text: str) -> set[str]:
    lowered = text.lower()
    if advanced_transition_recipes(lowered):
        return set()
    return {term for term in BASIC_TRANSITION_ONLY_TERMS if term in lowered}


def has_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def number(value: Any, default: float | None = None) -> float | None:
    try:
        return float(value)
    except Exception:
        return default


def beat_offset_seconds(beat: dict[str, Any], duration: float, index: int, total: int) -> float:
    explicit = (
        beat.get("time_offset_sec")
        if "time_offset_sec" in beat
        else beat.get("offset_sec") if "offset_sec" in beat else beat.get("start_sec")
    )
    parsed = number(explicit)
    if parsed is not None:
        return max(0.0, min(duration, parsed))
    if total <= 1:
        return 0.0
    return max(0.0, min(duration, duration * (index - 1) / total))


def max_internal_visual_gap(duration: float, offsets: list[float]) -> float:
    points = sorted({0.0, duration, *[max(0.0, min(duration, item)) for item in offsets]})
    if len(points) < 2:
        return duration
    return max(current - previous for previous, current in zip(points, points[1:]))


def validate_premium_motion(scene_id: str, motion: Any, issues: list[str]) -> bool:
    if not isinstance(motion, dict):
        issues.append(f"{scene_id} motion must be an object")
        return False

    valid = True
    for key in PREMIUM_MOTION_REQUIRED:
        if not str(motion.get(key, "")).strip():
            issues.append(f"{scene_id} motion.{key} is required for premium HyperFrames motion craft")
            valid = False

    combined = " ".join(str(value) for value in motion.values())
    forbidden = forbidden_motion_terms(combined)
    if forbidden:
        issues.append(f"{scene_id} motion uses vague/cheap motion language: {', '.join(sorted(set(forbidden)))}")
        valid = False

    purpose = str(motion.get("purpose", "")).lower()
    if not any(term in purpose for term in MOTION_PURPOSE_TERMS):
        issues.append(f"{scene_id} motion.purpose must state an information purpose such as reveal/compare/verify/connect/summarize")
        valid = False

    entrance = str(motion.get("entrance", "")).lower()
    if not (has_any(entrance, ["fade-up", "fade up"]) and "20px" in entrance and "opacity" in entrance and has_any(entrance, ["0.5", "0.6"])):
        issues.append(f"{scene_id} motion.entrance must specify 0.5s-0.6s fade-up from y=20px with opacity 0")
        valid = False

    stagger = str(motion.get("stagger", "")).lower()
    if "0.12" not in stagger or "0.18" not in stagger:
        issues.append(f"{scene_id} motion.stagger must specify 0.12s-0.18s stagger timing")
        valid = False

    keyword_motion = str(motion.get("keyword_motion", "")).lower()
    legacy_keyword_motion = "scale-pop" in keyword_motion and "1.08" in keyword_motion and "0.25" in keyword_motion
    restrained_keyword_motion = (
        "1.03" in keyword_motion
        and ("brightness pulse" in keyword_motion or "keyword" in keyword_motion and "pulse" in keyword_motion)
        and ("0.20" in keyword_motion or "0.2" in keyword_motion)
    )
    if not (legacy_keyword_motion or restrained_keyword_motion):
        issues.append(
            f"{scene_id} motion.keyword_motion must specify a restrained keyword pulse, e.g. scale max 1.03x for 0.20s"
        )
        valid = False

    camera_motion = str(motion.get("camera_motion", "")).lower()
    if "100" not in camera_motion or "103" not in camera_motion or "stable" not in camera_motion:
        issues.append(f"{scene_id} motion.camera_motion must specify background push-in 100% to 103% with stable foreground")
        valid = False

    layering = str(motion.get("layering", "")).lower()
    if not ("parallax" in layering and "foreground" in layering and ("callout" in layering or "reveal" in layering)):
        issues.append(f"{scene_id} motion.layering must describe background parallax, stable foreground, and callout/reveal layer")
        valid = False

    transition = str(motion.get("transition", "")).lower()
    recipes = advanced_transition_recipes(transition)
    if not recipes:
        issues.append(
            f"{scene_id} motion.transition must use a named advanced transition recipe such as source_focus_lens_reveal, citation_rail_wipe, comparison_split_handoff, terminal_scan_proof_tray, or final_controlled_zoom"
        )
        valid = False
    basic_terms = basic_transition_only_terms(transition)
    if basic_terms:
        issues.append(
            f"{scene_id} motion.transition uses ordinary transition terms without an advanced recipe: {', '.join(sorted(basic_terms))}"
        )
        valid = False

    caption_motion = str(motion.get("caption_motion", "")).lower()
    if not ("keyword" in caption_motion and "highlight" in caption_motion and ("no every-word" in caption_motion or "not every word" in caption_motion)):
        issues.append(f"{scene_id} motion.caption_motion must highlight keywords only and prohibit every-word bouncing")
        valid = False

    glow = str(motion.get("glow", "")).lower()
    if "8%" not in glow or "18%" not in glow or not has_any(glow, ["no flicker", "no flashing", "no strobe"]):
        issues.append(f"{scene_id} motion.glow must specify ambient glow opacity 8%-18% and no flicker")
        valid = False

    audio_reactive = str(motion.get("audio_reactive", "")).lower()
    if "3%" not in audio_reactive or "5%" not in audio_reactive or "10%" not in audio_reactive or "15%" not in audio_reactive:
        issues.append(f"{scene_id} motion.audio_reactive must specify text 3%-5% and background glow 10%-15%")
        valid = False

    negative_motion = str(motion.get("negative_motion", "")).lower()
    if not ("no excessive bounce" in negative_motion and "no chaotic movement" in negative_motion and "no glitch spam" in negative_motion):
        issues.append(f"{scene_id} motion.negative_motion must block excessive bounce, chaotic movement, and glitch spam")
        valid = False

    return valid


def has_forbidden_audio_bridge(text: str) -> bool:
    lowered = text.lower()
    for term in FORBIDDEN_AUDIO_BRIDGE_TERMS:
        if term in {"重启", "静音", "断音", "停顿"}:
            index = text.find(term)
            while index != -1:
                prefix = text[max(0, index - 2) : index]
                if prefix not in {"不", "无", "禁"}:
                    return True
                index = text.find(term, index + len(term))
            continue
        if contains_with_negative_context(lowered, term):
            return True
    return False


def validate_audio_continuity(scene_id: str, sync: Any, issues: list[str]) -> bool:
    if not isinstance(sync, dict):
        issues.append(f"{scene_id} sync must be an object")
        return False

    valid = True
    for key in SYNC_REQUIRED:
        value = sync.get(key)
        if value is None or not str(value).strip():
            issues.append(f"{scene_id} sync.{key} is required for continuous narration through transitions")
            valid = False

    try:
        max_gap_ms = int(sync.get("max_audio_gap_ms"))
    except Exception:
        issues.append(f"{scene_id} sync.max_audio_gap_ms must be an integer <= {MAX_TRANSITION_AUDIO_GAP_MS}")
        max_gap_ms = MAX_TRANSITION_AUDIO_GAP_MS + 1
        valid = False
    if max_gap_ms > MAX_TRANSITION_AUDIO_GAP_MS:
        issues.append(f"{scene_id} sync.max_audio_gap_ms must be <= {MAX_TRANSITION_AUDIO_GAP_MS}")
        valid = False

    narration_track = str(sync.get("narration_track", "")).lower()
    if not any(term in narration_track for term in CONTINUOUS_NARRATION_TERMS):
        issues.append(f"{scene_id} sync.narration_track must describe a continuous/root narration track")
        valid = False

    transition_policy = str(sync.get("transition_audio_policy", "")).lower()
    if not any(term in transition_policy for term in VISUAL_ONLY_AUDIO_TERMS):
        issues.append(f"{scene_id} sync.transition_audio_policy must state visual-only transitions with no restart or mute")
        valid = False

    audio_bridge = str(sync.get("audio_bridge", ""))
    bridge_lower = audio_bridge.lower()
    if not any(term in bridge_lower for term in CONTINUOUS_NARRATION_TERMS + VISUAL_ONLY_AUDIO_TERMS):
        issues.append(f"{scene_id} sync.audio_bridge must describe how narration continues under the visual transition")
        valid = False
    if has_forbidden_audio_bridge(audio_bridge):
        issues.append(f"{scene_id} sync.audio_bridge must not restart, mute, stop, or gap narration")
        valid = False

    return valid


def normal_tts_speed(value: Any) -> bool:
    try:
        speed = float(value)
    except Exception:
        return False
    return MIN_NORMAL_TTS_SPEED <= speed <= MAX_NORMAL_TTS_SPEED


def approved_tts_speed(target: dict[str, Any]) -> bool:
    try:
        speed = float(target.get("tts_speed"))
    except Exception:
        return False
    policy = str(target.get("voice_speed_policy", "")).strip().lower()
    if MIN_NORMAL_TTS_SPEED <= speed <= MAX_NORMAL_TTS_SPEED and policy in NORMAL_VOICE_SPEED_POLICIES:
        return True
    approval_text = " ".join(
        str(target.get(key, ""))
        for key in ["voice_speed_approval", "voice_direction", "voice_persona", "voice_notes"]
    ).lower()
    has_approval = policy in USER_APPROVED_VOICE_SPEED_POLICIES or any(marker in approval_text for marker in USER_APPROVAL_MARKERS)
    return MAX_NORMAL_TTS_SPEED < speed <= MAX_USER_APPROVED_TTS_SPEED and has_approval


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True).lower()


def contains_forbidden_provider(text: str) -> bool:
    lowered = text.lower()
    if any(term in lowered for term in APPROVAL_TERMS):
        return False
    return any(term in lowered for term in FORBIDDEN_PROVIDER_TERMS)


def scene_has_animated_icon_event(scene: dict[str, Any]) -> bool:
    surface = {
        "visual": scene.get("visual"),
        "motion": scene.get("motion"),
        "beat_map": scene.get("beat_map"),
        "on_screen_text": scene.get("on_screen_text"),
        "concept": scene.get("concept"),
    }
    text = json_text(surface)
    return any(term.lower() in text for term in ANIMATED_ICON_TERMS)


def scene_sfx_cues(scene: dict[str, Any]) -> list[Any]:
    cues: list[Any] = []
    for field in SFX_CUE_FIELDS:
        value = scene.get(field)
        if isinstance(value, list):
            cues.extend(value)
        elif isinstance(value, dict):
            cues.append(value)
    return cues


def cue_has_timing(cue: Any) -> bool:
    if not isinstance(cue, dict):
        return False
    return any(field in cue and str(cue.get(field, "")).strip() for field in SFX_TIME_FIELDS)


def cue_describes_event(cue: Any) -> bool:
    if not isinstance(cue, dict):
        return False
    return any(str(cue.get(field, "")).strip() for field in ["visual_event", "event", "target", "motion_event"])


def cue_describes_sound(cue: Any) -> bool:
    if not isinstance(cue, dict):
        return False
    return any(str(cue.get(field, "")).strip() for field in ["sound", "sfx", "effect", "sound_character"])


def cue_is_voice_safe(cue: Any) -> bool:
    text = json_text(cue)
    return any(term.lower() in text for term in VOICE_SAFE_SFX_TERMS) and not any(
        term.lower() in text for term in SFX_MASKING_BAD_TERMS
    )


def validate_animated_icon_sfx(scene_id: str, scene: dict[str, Any], issues: list[str]) -> dict[str, bool]:
    has_icon_event = scene_has_animated_icon_event(scene)
    if not has_icon_event:
        return {"animated_icon_event": False, "icon_sfx_valid": True}

    cues = scene_sfx_cues(scene)
    if not cues:
        issues.append(f"{scene_id} has animated/status icon motion but no sfx_cues/audio_cues/icon_audio_cues")
        return {"animated_icon_event": True, "icon_sfx_valid": False}

    valid = True
    for index, cue in enumerate(cues, start=1):
        prefix = f"{scene_id} sfx cue {index}"
        if not isinstance(cue, dict):
            issues.append(f"{prefix} must be an object")
            valid = False
            continue
        if not cue_has_timing(cue):
            issues.append(f"{prefix} needs time_sec/time_offset_sec/offset_sec/start_sec")
            valid = False
        if not cue_describes_event(cue):
            issues.append(f"{prefix} needs visual_event/event/target/motion_event")
            valid = False
        if not cue_describes_sound(cue):
            issues.append(f"{prefix} needs sound/sfx/effect/sound_character")
            valid = False
        if not cue_is_voice_safe(cue):
            issues.append(f"{prefix} must state SFX stays 12dB-18dB below narration and does not mask voice")
            valid = False
    return {"animated_icon_event": True, "icon_sfx_valid": valid}


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


def requires_codex_plugin_plan(data: dict[str, Any]) -> bool:
    text = collect_text(data).lower()
    return any(term in text for term in PLUGIN_TRIGGER_TERMS)


def requires_six_plugin_plan(data: dict[str, Any]) -> bool:
    text = collect_text(data).lower()
    return ("插件" in text or "plugin" in text) and any(term in text for term in SIX_PLUGIN_TERMS)


def requires_ai_knowledge_format(data: dict[str, Any]) -> bool:
    text = collect_text(data).lower()
    if any(term in text for term in AI_KNOWLEDGE_TERMS):
        return True
    stack = data.get("production_stack")
    if isinstance(stack, dict) and json_text(stack).strip() not in {"{}", "null"}:
        return True
    return False


def vertical_reference_exception_allowed(data: dict[str, Any], target: dict[str, Any]) -> bool:
    exception = data.get("format_exception") or target.get("format_exception")
    if not isinstance(exception, dict):
        return False
    try:
        width = int(target.get("width") or 0)
        height = int(target.get("height") or 0)
    except Exception:
        return False
    if width != VERTICAL_REFERENCE_WIDTH or height != VERTICAL_REFERENCE_HEIGHT:
        return False
    status = str(exception.get("status", "")).strip().lower()
    mode = str(exception.get("mode", "")).strip().lower()
    basis = json_text(exception).lower()
    return (
        status in {"approved", "locked", "passed"}
        and mode == "reference_driven_lightweight_vertical"
        and "reference" in basis
        and "lightweight" in basis
        and "proof-heavy" in basis
    )


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
        value = quality_spec.get(key)
        if value is None or not str(value).strip():
            issues.append(f"quality_spec.{key} is required")
            valid = False

    level = str(quality_spec.get("target_quality_level", "")).strip()
    if level not in ACCEPTED_QUALITY_LEVELS:
        issues.append("quality_spec.target_quality_level must be high_quality or breakout_potential")
        valid = False

    if quality_spec.get("provider_policy") != ACCEPTED_PROVIDER_POLICY:
        issues.append("quality_spec.provider_policy must be free_first_local_or_authorized_openai_only")
        valid = False

    runtime_choice = str(quality_spec.get("runtime_choice", "")).lower()
    if not any(term in runtime_choice for term in ["hyperframes", "remotion", "ffmpeg", "moviepy"]):
        issues.append("quality_spec.runtime_choice must document the Remotion/HyperFrames/FFmpeg runtime split")
        valid = False

    if contains_forbidden_provider(json_text(quality_spec)):
        issues.append("quality_spec references a disabled paid provider without explicit user approval")
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
            elif visual.get("scene_type") in REAL_PROOF_SCENE_TYPES and "proof_chain" not in visual:
                warnings.append(f"{scene.get('scene_id', 'unknown')} evidence scene should include visual.proof_chain")

    return {
        "production_stack_required": True,
        "production_stack_valid": stack_valid,
        "tool_proof_chain_count": tool_proof_chain_count,
    }


def normalize_plugin_name(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", " ").replace("_", " ")


def validate_codex_plugin_plan(data: dict[str, Any], issues: list[str], warnings: list[str]) -> dict[str, Any]:
    plan_required = requires_codex_plugin_plan(data)
    six_required = requires_six_plugin_plan(data)
    if not plan_required:
        return {
            "codex_plugin_plan_required": False,
            "codex_plugin_plan_valid": True,
            "codex_plugin_count": 0,
            "six_codex_plugins_documented": not six_required,
            "blocked_plugin_count": 0,
            "approval_required_count": 0,
        }

    plan = data.get("codex_plugin_plan")
    if not isinstance(plan, dict):
        issues.append("codex_plugin_plan is required when a video teaches, compares, or claims Codex plugins")
        return {
            "codex_plugin_plan_required": True,
            "codex_plugin_plan_valid": False,
            "codex_plugin_count": 0,
            "six_codex_plugins_documented": False,
            "blocked_plugin_count": 0,
            "approval_required_count": 0,
        }

    plan_valid = True
    if not str(plan.get("use_case", "")).strip():
        issues.append("codex_plugin_plan.use_case is required")
        plan_valid = False

    plugins = plan.get("plugins", [])
    if not isinstance(plugins, list) or not plugins:
        issues.append("codex_plugin_plan.plugins must list the plugins used, taught, or evaluated")
        plugins = []
        plan_valid = False

    blocked_plugins = plan.get("blocked_plugins", [])
    approval_required_for = plan.get("approval_required_for", [])
    if not isinstance(blocked_plugins, list):
        issues.append("codex_plugin_plan.blocked_plugins must be an array")
        blocked_plugins = []
        plan_valid = False
    if not isinstance(approval_required_for, list):
        issues.append("codex_plugin_plan.approval_required_for must be an array")
        approval_required_for = []
        plan_valid = False

    plugin_names: list[str] = []
    for index, plugin in enumerate(plugins, start=1):
        if not isinstance(plugin, dict):
            issues.append(f"codex_plugin_plan.plugins[{index}] must be an object")
            plan_valid = False
            continue
        name = str(plugin.get("name", "")).strip()
        normalized_name = normalize_plugin_name(name)
        plugin_names.append(normalized_name)
        availability = str(plugin.get("availability", "")).strip()
        allowed_by_default = plugin.get("allowed_by_default")
        evidence_required = plugin.get("evidence_required", [])
        if not name:
            issues.append(f"codex_plugin_plan.plugins[{index}] missing name")
            plan_valid = False
        if availability not in PLUGIN_AVAILABILITY:
            issues.append(f"codex_plugin_plan.plugins[{index}] availability is unsupported")
            plan_valid = False
        if not str(plugin.get("role", "")).strip():
            issues.append(f"codex_plugin_plan.plugins[{index}] missing role")
            plan_valid = False
        if not isinstance(allowed_by_default, bool):
            issues.append(f"codex_plugin_plan.plugins[{index}] allowed_by_default must be boolean")
            plan_valid = False
        if not isinstance(evidence_required, list) or not any(str(item).strip() for item in evidence_required):
            issues.append(f"codex_plugin_plan.plugins[{index}] evidence_required must list proof artifacts")
            plan_valid = False
        if not str(plugin.get("cost_or_auth_boundary", "")).strip():
            issues.append(f"codex_plugin_plan.plugins[{index}] missing cost_or_auth_boundary")
            plan_valid = False
        if not str(plugin.get("fallback", "")).strip():
            issues.append(f"codex_plugin_plan.plugins[{index}] missing fallback")
            plan_valid = False
        if availability in {"needs_user_approval", "optional_blocked", "not_available"} and allowed_by_default is True:
            issues.append(f"codex_plugin_plan plugin {name} cannot be allowed_by_default when it needs approval or is blocked")
            plan_valid = False
        if "heygen" in normalized_name:
            approval_text = " ".join(str(item).lower() for item in approval_required_for)
            if allowed_by_default is True:
                issues.append("HeyGen must not be allowed_by_default; mark approval-required unless the user authorized the exact generation path")
                plan_valid = False
            if availability not in {"needs_user_approval", "available_if_authenticated", "optional_blocked", "not_available"}:
                warnings.append("HeyGen should usually be marked approval/auth-required, not default production runtime")
            if "heygen" not in approval_text and availability != "not_available":
                issues.append("codex_plugin_plan.approval_required_for must mention HeyGen when HeyGen is part of the plan")
                plan_valid = False

    six_documented = True
    if six_required:
        missing = []
        for canonical, aliases in CORE_CODEX_PLUGINS.items():
            if not any(any(alias in name for alias in aliases) for name in plugin_names):
                missing.append(canonical)
        if missing:
            issues.append("six-plugin Codex videos must document these plugins: " + ", ".join(missing))
            plan_valid = False
            six_documented = False

    return {
        "codex_plugin_plan_required": True,
        "codex_plugin_plan_valid": plan_valid,
        "codex_plugin_count": len(plugins),
        "six_codex_plugins_documented": six_documented,
        "blocked_plugin_count": len(blocked_plugins),
        "approval_required_count": len(approval_required_for),
    }


def validate_director_shots(data: dict[str, Any], issues: list[str], warnings: list[str]) -> dict[str, Any]:
    shots = data.get("director_shots")
    if not isinstance(shots, list) or not shots:
        issues.append("director_shots is required before HyperFrames composition")
        return {
            "director_shots_required": True,
            "director_shots_valid": False,
            "director_shot_count": 0,
            "director_shot_type_count": 0,
            "director_layout_max_consecutive": 0,
            "director_operation_shot_count": 0,
            "director_operation_element_coverage": 0,
            "director_camera_variety_count": 0,
            "director_approved_text_count": 0,
            "director_evidence_authenticity_valid": False,
        }

    valid = True
    shot_types: set[str] = set()
    camera_terms: set[str] = set()
    operation_shot_count = 0
    operation_elements_seen: set[str] = set()
    approved_text_count = 0
    evidence_valid = True
    max_layout_consecutive = 0
    current_layout = ""
    current_layout_count = 0

    for index, shot in enumerate(shots, start=1):
        prefix = f"director_shots[{index}]"
        if not isinstance(shot, dict):
            issues.append(f"{prefix} must be an object")
            valid = False
            continue
        for key in DIRECTOR_REQUIRED:
            value = shot.get(key)
            if value is None or (isinstance(value, str) and not value.strip()) or (isinstance(value, list) and not value):
                issues.append(f"{prefix}.{key} is required for visual director gate")
                valid = False

        shot_id = str(shot.get("shot_id") or f"S{index:02d}")
        shot_type = str(shot.get("shot_type", "")).strip()
        if shot_type:
            shot_types.add(shot_type)
        layout_family = str(shot.get("layout_family", "")).strip()
        if layout_family == current_layout:
            current_layout_count += 1
        else:
            current_layout = layout_family
            current_layout_count = 1
        max_layout_consecutive = max(max_layout_consecutive, current_layout_count)
        if current_layout_count > MAX_SAME_LAYOUT_CONSECUTIVE:
            issues.append(
                f"{shot_id} repeats layout_family={layout_family!r} {current_layout_count} times; max allowed is {MAX_SAME_LAYOUT_CONSECUTIVE}"
            )
            valid = False

        camera_scale = str(shot.get("camera_scale", "")).strip()
        camera_motion = str(shot.get("camera_motion", "")).strip()
        if camera_scale:
            camera_terms.add(f"scale:{camera_scale}")
        if camera_motion:
            camera_terms.add(f"motion:{camera_motion}")

        primary_action = str(shot.get("primary_action", "")).strip()
        if not primary_action or primary_action.lower() in {"none", "static", "无"}:
            issues.append(f"{shot_id} primary_action must describe a visible operation, reveal, or proof action")
            valid = False

        operation_elements = shot.get("operation_elements", [])
        if not isinstance(operation_elements, list):
            issues.append(f"{shot_id} operation_elements must be an array")
            operation_elements = []
            valid = False
        real_operation_elements = {str(item) for item in operation_elements if str(item) in DIRECTOR_OPERATION_ELEMENTS}
        if real_operation_elements:
            operation_shot_count += 1
            operation_elements_seen.update(real_operation_elements)

        evidence = shot.get("evidence", {})
        if not isinstance(evidence, dict):
            issues.append(f"{shot_id} evidence must be an object")
            evidence = {}
            evidence_valid = False
            valid = False
        evidence_type = str(evidence.get("type", "")).strip()
        if evidence_type in DIRECTOR_FORBIDDEN_EVIDENCE_TYPES:
            issues.append(f"{shot_id} uses forbidden evidence visual type: {evidence_type}")
            evidence_valid = False
            valid = False
        elif evidence_type and evidence_type not in DIRECTOR_ALLOWED_EVIDENCE_TYPES:
            issues.append(f"{shot_id} evidence.type is unsupported: {evidence_type}")
            evidence_valid = False
            valid = False
        if evidence_type in {"real_source_crop", "clean_citation_card"}:
            if not str(evidence.get("source_url", "")).strip() and not str(evidence.get("asset_id", "")).strip():
                issues.append(f"{shot_id} source evidence needs source_url or asset_id")
                evidence_valid = False
                valid = False
            if evidence.get("must_be_readable") is not True:
                issues.append(f"{shot_id} source evidence must set must_be_readable=true")
                evidence_valid = False
                valid = False
            try:
                min_width = int(evidence.get("min_visible_width_px") or 0)
            except Exception:
                min_width = 0
            if min_width and min_width < 900:
                issues.append(f"{shot_id} source evidence min_visible_width_px must be >= 900")
                evidence_valid = False
                valid = False

        on_screen_text = shot.get("on_screen_text", {})
        if not isinstance(on_screen_text, dict):
            issues.append(f"{shot_id} on_screen_text must be an object")
            on_screen_text = {}
            valid = False
        primary_text = str(on_screen_text.get("primary", "")).strip()
        approved = on_screen_text.get("approved_primary_text", [])
        if not isinstance(approved, list):
            issues.append(f"{shot_id} on_screen_text.approved_primary_text must be an array")
            approved = []
            valid = False
        approved_texts = {str(item).strip() for item in approved if str(item).strip()}
        approved_text_count += len(approved_texts)
        if primary_text and primary_text not in approved_texts:
            issues.append(f"{shot_id} primary on-screen text must be included in approved_primary_text; primary text not present")
            valid = False

        forbidden_risks = " ".join(str(item) for item in shot.get("forbidden_risks", []) or []).lower()
        if "empty" not in forbidden_risks and "空" not in forbidden_risks:
            warnings.append(f"{shot_id} should explicitly guard against empty_frame risk")
        if "tiny" not in forbidden_risks and "unreadable" not in forbidden_risks and "小字" not in forbidden_risks:
            warnings.append(f"{shot_id} should explicitly guard against tiny_unreadable_text risk")

    missing_types = sorted(DIRECTOR_REQUIRED_SHOT_TYPES - shot_types)
    if missing_types:
        issues.append("director_shots missing required shot_type values: " + ", ".join(missing_types))
        valid = False
    if len(shot_types) < MIN_DIRECTOR_SHOT_TYPES:
        issues.append(f"director_shots must use at least {MIN_DIRECTOR_SHOT_TYPES} shot_type values")
        valid = False
    if operation_shot_count < MIN_OPERATION_SHOTS:
        issues.append(f"director_shots must include at least {MIN_OPERATION_SHOTS} real operation shots")
        valid = False
    if len(operation_elements_seen) < MIN_OPERATION_ELEMENT_COVERAGE:
        issues.append(
            f"director_shots must cover at least {MIN_OPERATION_ELEMENT_COVERAGE} operation element types"
        )
        valid = False
    if len(camera_terms) < 3:
        issues.append("director_shots must vary camera_scale/camera_motion; at least 3 camera terms required")
        valid = False

    return {
        "director_shots_required": True,
        "director_shots_valid": valid,
        "director_shot_count": len(shots),
        "director_shot_type_count": len(shot_types),
        "director_layout_max_consecutive": max_layout_consecutive,
        "director_operation_shot_count": operation_shot_count,
        "director_operation_element_coverage": len(operation_elements_seen),
        "director_camera_variety_count": len(camera_terms),
        "director_approved_text_count": approved_text_count,
        "director_evidence_authenticity_valid": evidence_valid,
    }


def validate_director_timing(data: dict[str, Any], issues: list[str], warnings: list[str]) -> dict[str, Any]:
    shots = data.get("director_shots")
    scenes = data.get("scenes")
    if not isinstance(shots, list) or not isinstance(scenes, list) or not shots or not scenes:
        return {
            "director_timing_aligned": False,
            "director_total_duration": 0.0,
            "scene_total_duration": 0.0,
            "duration_mismatch_count": 0,
        }

    def number(value: Any) -> float:
        try:
            return float(value)
        except Exception:
            return 0.0

    shot_durations = [number(shot.get("duration_sec")) for shot in shots if isinstance(shot, dict)]
    scene_durations = [number(scene.get("duration_target")) for scene in scenes if isinstance(scene, dict)]
    shot_total = round(sum(shot_durations), 3)
    scene_total = round(sum(scene_durations), 3)
    mismatch_count = 0

    if len(shot_durations) != len(scene_durations):
        issues.append(
            f"director_shots count ({len(shot_durations)}) must match scenes count ({len(scene_durations)}) after TTS duration lock"
        )
        return {
            "director_timing_aligned": False,
            "director_total_duration": shot_total,
            "scene_total_duration": scene_total,
            "duration_mismatch_count": abs(len(shot_durations) - len(scene_durations)),
        }

    for index, (shot, scene, shot_duration, scene_duration) in enumerate(
        zip(shots, scenes, shot_durations, scene_durations),
        start=1,
    ):
        shot_id = str(shot.get("shot_id") or f"shot_{index}") if isinstance(shot, dict) else f"shot_{index}"
        scene_id = str(scene.get("scene_id") or f"scene_{index}") if isinstance(scene, dict) else f"scene_{index}"
        delta = abs(shot_duration - scene_duration)
        if delta > TIMELINE_DURATION_TOLERANCE_SEC:
            issues.append(
                f"director_shots {shot_id} duration_sec ({shot_duration:.3f}s) must match {scene_id} duration_target ({scene_duration:.3f}s) after TTS lock; delta={delta:.3f}s"
            )
            mismatch_count += 1

    total_delta = abs(shot_total - scene_total)
    if total_delta > TIMELINE_DURATION_TOLERANCE_SEC:
        issues.append(
            f"director_shots total duration ({shot_total:.3f}s) must match scenes total duration ({scene_total:.3f}s); delta={total_delta:.3f}s"
        )
        mismatch_count += 1

    return {
        "director_timing_aligned": mismatch_count == 0,
        "director_total_duration": shot_total,
        "scene_total_duration": scene_total,
        "duration_mismatch_count": mismatch_count,
    }


def validate(data: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    if data.get("status") == "draft_only" or data.get("production_ready") is False:
        issues.append("draft-only storyboard cannot enter render, QA, or promotion; build a production storyboard first")
    target = data.get("target", {})
    if not isinstance(target, dict):
        issues.append("target must be an object")
        target = {}
    if not approved_tts_speed(target):
        issues.append(
            "target.tts_speed must be 0.95-1.03 by default, or <=1.10 only with explicit user-approved voice_speed_policy and approval note"
        )
    speed_policy = str(target.get("voice_speed_policy", "")).strip().lower()
    if speed_policy not in NORMAL_VOICE_SPEED_POLICIES | USER_APPROVED_VOICE_SPEED_POLICIES:
        issues.append("target.voice_speed_policy must be normal or an explicit user-approved override")
    provider_policy_valid = target.get("provider_policy") == ACCEPTED_PROVIDER_POLICY
    if not provider_policy_valid:
        issues.append("target.provider_policy must be free_first_local_or_authorized_openai_only")
    ai_format_required = requires_ai_knowledge_format(data)
    vertical_reference_exception = vertical_reference_exception_allowed(data, target)
    ai_format_valid = True
    if ai_format_required:
        width = int(target.get("width") or 0)
        height = int(target.get("height") or 0)
        ai_format_valid = (
            width == AI_KNOWLEDGE_WIDTH and height == AI_KNOWLEDGE_HEIGHT
        ) or vertical_reference_exception
        if not ai_format_valid:
            issues.append(
                "AI knowledge videos must use 16:9 horizontal target.width=1920 and target.height=1080 unless format_exception=reference_driven_lightweight_vertical is approved"
            )
    quality_signals = validate_quality_spec(data, issues)
    stack_signals = validate_production_stack(data, issues, warnings)
    plugin_signals = validate_codex_plugin_plan(data, issues, warnings)
    director_signals = validate_director_shots(data, issues, warnings)
    director_timing_signals = validate_director_timing(data, issues, warnings)
    storyboard_alignment = review_storyboard_alignment(data)
    issues.extend(storyboard_alignment.get("blocking_issues", []))
    warnings.extend(storyboard_alignment.get("warnings", []))

    scenes = data.get("scenes", [])
    if len(scenes) < 6:
        issues.append("storyboard must contain at least 6 scenes")
    first_five_changes = 0
    elapsed = 0.0
    evidence_runtime = 0.0
    total_runtime = 0.0
    layered_scene_count = 0
    quality_check_scene_count = 0
    source_class_scene_count = 0
    caption_template_scene_count = 0
    caption_templates_used: set[str] = set()
    forbidden_provider_scene_count = 0
    premium_motion_scene_count = 0
    audio_continuity_scene_count = 0
    animated_icon_scene_count = 0
    icon_sfx_scene_count = 0
    transition_recipes_used: set[str] = set()
    voice_ranges: list[tuple[str, float, float, int]] = []
    visual_change_times: list[float] = []
    retention_times: list[float] = []
    for scene in scenes:
        duration = float(scene.get("duration_target") or 0)
        scene_start = elapsed
        total_runtime += duration
        visual_change_times.append(elapsed)
        elapsed += duration
        for key in ["scene_id", "concept", "voice", "caption", "on_screen_text", "visual", "motion", "sync", "safe_zone", "qa_notes"]:
            if key not in scene:
                issues.append(f"{scene.get('scene_id', 'unknown')} missing {key}")
        beat_map = scene.get("beat_map", [])
        if not beat_map:
            issues.append(f"{scene.get('scene_id', 'unknown')} missing beat_map")
        beat_offsets: list[float] = []
        for index, beat in enumerate(beat_map, start=1):
            offset = beat_offset_seconds(beat, duration, index, len(beat_map)) if isinstance(beat, dict) else 0.0
            beat_offsets.append(offset)
            beat_time = scene_start + offset
            retention_times.append(beat_time)
            visual_change_times.append(beat_time)
            for key in BEAT_REQUIRED:
                if not str(beat.get(key, "")).strip():
                    issues.append(f"{scene.get('scene_id', 'unknown')} beat {index} missing {key}")
            voice_fragment = str(beat.get("voice_fragment", "")).strip()
            voice = str(scene.get("voice", ""))
            if voice_fragment and voice_fragment not in voice:
                warnings.append(f"{scene.get('scene_id', 'unknown')} beat {index} voice_fragment not found verbatim in voice")
            if not any(term in str(beat.get("proof_or_explanation", "")) for term in ["对比", "证明", "错误", "模板", "结果", "清单", "真实", "保存"]):
                warnings.append(f"{scene.get('scene_id', 'unknown')} beat {index} should name proof, contrast, template, result, or save value")
        motion = scene.get("motion", {})
        if validate_premium_motion(str(scene.get("scene_id", "unknown")), motion, issues):
            premium_motion_scene_count += 1
        if isinstance(motion, dict):
            transition_recipes_used.update(advanced_transition_recipes(str(motion.get("transition", ""))))
        if motion_layer_count(motion if isinstance(motion, dict) else {}) < 2:
            issues.append(f"{scene.get('scene_id', 'unknown')} needs at least 2 motion layers")
        sync = scene.get("sync", {})
        if validate_audio_continuity(str(scene.get("scene_id", "unknown")), sync, issues):
            audio_continuity_scene_count += 1
        icon_sfx_signals = validate_animated_icon_sfx(str(scene.get("scene_id", "unknown")), scene, issues)
        if icon_sfx_signals["animated_icon_event"]:
            animated_icon_scene_count += 1
        if icon_sfx_signals["animated_icon_event"] and icon_sfx_signals["icon_sfx_valid"]:
            icon_sfx_scene_count += 1
        if isinstance(sync, dict):
            try:
                voice_start = float(sync.get("voice_start"))
                voice_end = float(sync.get("voice_end"))
                max_gap_ms = int(sync.get("max_audio_gap_ms"))
            except Exception:
                pass
            else:
                if voice_end < voice_start:
                    issues.append(f"{scene.get('scene_id', 'unknown')} sync.voice_end must be >= voice_start")
                voice_ranges.append((str(scene.get("scene_id", "unknown")), voice_start, voice_end, max_gap_ms))
        visual = scene.get("visual", {})
        if visual.get("scene_type") in EVIDENCE_TYPES:
            evidence_runtime += duration
        if isinstance(visual, dict):
            source_type = str(visual.get("asset_source_type", "")).strip()
            caption_template = str(visual.get("caption_template", "")).strip()
            scene_type = str(visual.get("scene_type", "")).strip()
            if source_type in ASSET_SOURCE_TYPES:
                source_class_scene_count += 1
            else:
                issues.append(f"{scene.get('scene_id', 'unknown')} visual.asset_source_type must be proof/support/generated/free_stock")
            if caption_template in CAPTION_TEMPLATES:
                caption_template_scene_count += 1
                caption_templates_used.add(caption_template)
            else:
                issues.append(f"{scene.get('scene_id', 'unknown')} visual.caption_template is missing or unsupported")
            if scene_type in REAL_PROOF_SCENE_TYPES and source_type != "proof":
                issues.append(f"{scene.get('scene_id', 'unknown')} evidence scene must use visual.asset_source_type=proof")
            if scene_type == "generated_visual" and source_type != "generated":
                issues.append(f"{scene.get('scene_id', 'unknown')} generated_visual must use visual.asset_source_type=generated")
            if scene_type in STATIC_TYPES and source_type == "proof":
                issues.append(f"{scene.get('scene_id', 'unknown')} static/generated visual types cannot be counted as proof")
            provider_surface = json_text(
                {
                    "evidence_source": visual.get("evidence_source"),
                    "asset_path": visual.get("asset_path"),
                    "description": visual.get("description"),
                    "qa_notes": scene.get("qa_notes"),
                }
            )
            if contains_forbidden_provider(provider_surface):
                forbidden_provider_scene_count += 1
                issues.append(f"{scene.get('scene_id', 'unknown')} references a disabled paid/scraping provider without explicit user approval")
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
        if duration > 8 and (len(beat_map) < 2 or max_internal_visual_gap(duration, beat_offsets) > 5):
            issues.append(f"{scene.get('scene_id', 'unknown')} duration is too long; split or add reveal/build/focus")
        if duration > 5 and len(beat_map) < 2:
            warnings.append(f"{scene.get('scene_id', 'unknown')} is longer than 5s and should include at least 2 beat_map items")
    for previous, current in zip(voice_ranges, voice_ranges[1:]):
        previous_id, _, previous_end, previous_gap_ms = previous
        current_id, current_start, _, current_gap_ms = current
        gap_ms = int(round((current_start - previous_end) * 1000))
        allowed_gap_ms = min(previous_gap_ms, current_gap_ms, MAX_TRANSITION_AUDIO_GAP_MS)
        if gap_ms > allowed_gap_ms:
            issues.append(
                f"audio continuity gap between {previous_id} and {current_id} is {gap_ms}ms; must be <= {allowed_gap_ms}ms"
            )
    first_five_changes = sum(1 for item in sorted(set(round(time, 3) for time in visual_change_times)) if 0 <= item < 5)
    if first_five_changes < 2:
        issues.append("first 5 seconds must contain at least 2 visual changes")
    if len(caption_templates_used) < 2:
        issues.append("publish-ready storyboard must use at least 2 caption templates")
    if len(transition_recipes_used) < min(3, len(scenes)):
        issues.append(
            "publish-ready storyboard must use at least 3 distinct advanced transition recipes; repeated ordinary transitions are not allowed"
        )
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
            **plugin_signals,
            **director_signals,
            **director_timing_signals,
            "content_alignment_status": storyboard_alignment.get("status"),
            **{
                f"content_alignment_{key}": value
                for key, value in storyboard_alignment.get("signals", {}).items()
            },
            "provider_policy_valid": provider_policy_valid,
            "ai_knowledge_16x9_required": ai_format_required,
            "ai_knowledge_16x9_valid": ai_format_valid,
            "ai_knowledge_vertical_reference_exception": vertical_reference_exception,
            "layered_scene_count": layered_scene_count,
            "quality_check_scene_count": quality_check_scene_count,
            "source_class_scene_count": source_class_scene_count,
            "caption_template_scene_count": caption_template_scene_count,
            "caption_template_count": len(caption_templates_used),
            "caption_templates_used": sorted(caption_templates_used),
            "forbidden_provider_scene_count": forbidden_provider_scene_count,
            "premium_motion_scene_count": premium_motion_scene_count,
            "advanced_transition_recipe_count": len(transition_recipes_used),
            "advanced_transition_recipes_used": sorted(transition_recipes_used),
            "audio_continuity_scene_count": audio_continuity_scene_count,
            "animated_icon_scene_count": animated_icon_scene_count,
            "icon_sfx_scene_count": icon_sfx_scene_count,
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
