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
    "browser",
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


def has_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


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
    if "scale-pop" not in keyword_motion or "1.08" not in keyword_motion or "0.25" not in keyword_motion:
        issues.append(f"{scene_id} motion.keyword_motion must specify subtle scale-pop max 1.08x for 0.25s")
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
    if not any(term in transition for term in ["blur crossfade", "push slide", "dramatic zoom"]):
        issues.append(f"{scene_id} motion.transition must use blur crossfade, smooth push slide, or final dramatic zoom")
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


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True).lower()


def contains_forbidden_provider(text: str) -> bool:
    lowered = text.lower()
    if any(term in lowered for term in APPROVAL_TERMS):
        return False
    return any(term in lowered for term in FORBIDDEN_PROVIDER_TERMS)


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
            elif visual.get("scene_type") in EVIDENCE_TYPES and "proof_chain" not in visual:
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
    provider_policy_valid = target.get("provider_policy") == ACCEPTED_PROVIDER_POLICY
    if not provider_policy_valid:
        issues.append("target.provider_policy must be free_first_local_or_authorized_openai_only")
    ai_format_required = requires_ai_knowledge_format(data)
    ai_format_valid = True
    if ai_format_required:
        width = int(target.get("width") or 0)
        height = int(target.get("height") or 0)
        ai_format_valid = width == AI_KNOWLEDGE_WIDTH and height == AI_KNOWLEDGE_HEIGHT
        if not ai_format_valid:
            issues.append(
                "AI knowledge videos must use 16:9 horizontal target.width=1920 and target.height=1080; do not use 9:16 for AI/tool/tutorial content"
            )
    quality_signals = validate_quality_spec(data, issues)
    stack_signals = validate_production_stack(data, issues, warnings)
    plugin_signals = validate_codex_plugin_plan(data, issues, warnings)

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
    voice_ranges: list[tuple[str, float, float, int]] = []
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
        motion = scene.get("motion", {})
        if validate_premium_motion(str(scene.get("scene_id", "unknown")), motion, issues):
            premium_motion_scene_count += 1
        if motion_layer_count(motion if isinstance(motion, dict) else {}) < 2:
            issues.append(f"{scene.get('scene_id', 'unknown')} needs at least 2 motion layers")
        sync = scene.get("sync", {})
        if validate_audio_continuity(str(scene.get("scene_id", "unknown")), sync, issues):
            audio_continuity_scene_count += 1
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
            if scene_type in EVIDENCE_TYPES and source_type != "proof":
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
        if duration > 8:
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
    if first_five_changes < 2:
        issues.append("first 5 seconds must contain at least 2 visual changes")
    if len(caption_templates_used) < 2:
        issues.append("publish-ready storyboard must use at least 2 caption templates")
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
            "provider_policy_valid": provider_policy_valid,
            "ai_knowledge_16x9_required": ai_format_required,
            "ai_knowledge_16x9_valid": ai_format_valid,
            "layered_scene_count": layered_scene_count,
            "quality_check_scene_count": quality_check_scene_count,
            "source_class_scene_count": source_class_scene_count,
            "caption_template_scene_count": caption_template_scene_count,
            "caption_template_count": len(caption_templates_used),
            "caption_templates_used": sorted(caption_templates_used),
            "forbidden_provider_scene_count": forbidden_provider_scene_count,
            "premium_motion_scene_count": premium_motion_scene_count,
            "audio_continuity_scene_count": audio_continuity_scene_count,
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
