#!/usr/bin/env python3
"""Select fixed reusable production templates for AI videos."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BACKGROUND = ROOT / "references" / "fixed_ai_background_template_rotation.json"
DEFAULT_TRANSITIONS = ROOT / "references" / "fixed_ai_transition_sfx_packs.json"
DEFAULT_COMPONENTS = ROOT / "references" / "fixed_ai_component_template_packs.json"
DEFAULT_VOICE = ROOT / "references" / "fixed_ai_voice_mix_profiles.json"
DEFAULT_SCENE_MOTION = ROOT / "references" / "fixed_ai_scene_motion_templates.json"
DEFAULT_STATE = ROOT / "outputs" / ".ai_production_template_rotation_state.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def load_json(path: Path, default: Any) -> Any:
    if not path.exists() or not path.is_file() or path.stat().st_size == 0:
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def compact_json(path: Path | None) -> str:
    if not path or not path.exists():
        return ""
    try:
        return json.dumps(json.loads(path.read_text(encoding="utf-8")), ensure_ascii=False)
    except json.JSONDecodeError:
        return path.read_text(encoding="utf-8")


def detect_aspect(args: argparse.Namespace) -> str:
    if args.aspect in {"16:9", "9:16"}:
        return str(args.aspect)
    if args.video_width and args.video_height:
        return "16:9" if int(args.video_width) >= int(args.video_height) else "9:16"
    return "16:9"


def fallback_scheme(text: str, aspect: str) -> str:
    lowered = text.lower()
    multi_skill_terms = ["三个", "3个", "skill", "插件", "生产栈", "协作"]
    stack_terms = ["协作", "组合", "组成", "生产栈", "工作流", "workflow"]
    if any(term in lowered for term in multi_skill_terms) and any(term in lowered for term in stack_terms):
        return "scheme_4_multi_skill_stack_explainer"
    skill_terms = ["skill", "skills", "插件", "工具"]
    skill_list_terms = ["top5", "top 5", "top five", "五个", "5个", "8个", "10个", "清单", "推荐", "先学", "先装", "必备", "用途", "功能介绍"]
    current_news_terms = ["热榜", "新闻", "热点", "更新", "发布", "新增", "release"]
    if aspect == "9:16" and any(term in lowered for term in skill_terms) and any(term in lowered for term in skill_list_terms) and not any(
        term in lowered for term in current_news_terms
    ):
        return "scheme_1_skill_recommendation_no_voice"
    if any(term in lowered for term in ["top5", "top 5", "top five", "热榜", "榜单", "排行", "排名"]) and any(
        term in lowered for term in ["ai", "人工智能", "openai", "chatgpt", "gemini", "codex", "模型", "工具"]
    ):
        return "scheme_7_ai_hot_rank_top5"
    if aspect == "9:16" and any(term in lowered for term in ["skill", "工具", "推荐", "清单", "无人声"]):
        return "scheme_1_skill_recommendation_no_voice"
    if any(term in lowered for term in ["新闻", "发布", "新增", "更新", "gemini", "openai", "chatgpt"]):
        return "scheme_3_ai_news_to_beginner_action"
    if any(term in lowered for term in ["三个", "3个", "skill", "插件", "生产栈", "协作"]):
        return "scheme_4_multi_skill_stack_explainer"
    if any(term in lowered for term in ["避坑", "错误", "模板", "清单", "对比"]):
        return "scheme_5_checklist_template_poster"
    if any(term in lowered for term in ["终端", "测试", "操作", "proof", "codex"]):
        return "scheme_6_operation_proof_short"
    return "scheme_2_source_led_tool_tutorial"


def read_scheme_and_style(args: argparse.Namespace, aspect: str) -> tuple[str, str, str]:
    director = load_json(resolve_path(args.director_selection), {}) if args.director_selection else {}
    recipe = load_json(resolve_path(args.style_recipe), {}) if args.style_recipe else {}
    selected_topic = compact_json(resolve_path(args.selected_topic)) if args.selected_topic else ""
    text = " ".join([selected_topic, json.dumps(director, ensure_ascii=False), json.dumps(recipe, ensure_ascii=False)])

    scheme = director.get("scheme") if isinstance(director.get("scheme"), dict) else {}
    scheme_id = str(scheme.get("id") or "").strip() or fallback_scheme(text, aspect)
    visual_system = director.get("visual_system") if isinstance(director.get("visual_system"), dict) else {}
    visual_family = str(
        recipe.get("selected_visual_family")
        or visual_system.get("visual_family")
        or ""
    ).strip()
    background_style_id = str(
        recipe.get("background_style_id")
        or visual_system.get("background_style_id")
        or ""
    ).strip()
    return scheme_id, visual_family, background_style_id


def default_audio_music_decision(scheme_id: str) -> dict[str, Any]:
    if scheme_id in {"scheme_1_skill_recommendation_no_voice", "scheme_7_ai_hot_rank_top5"}:
        return {
            "music_policy": "required_bgm",
            "reason": "scheme default requires BGM-driven pacing",
            "bgm_source_priority": ["douyin_reference", "authorized_local_library", "pixabay", "mixkit"],
            "voice_policy": "no_voice" if scheme_id == "scheme_1_skill_recommendation_no_voice" else "optional_short_narration",
            "voice_priority": False,
            "sfx_required": False,
            "generated_bgm_allowed": False,
            "reference_bgm_policy": "when a user-provided Douyin reference has BGM, use the same reference music or block for user approval; do not generate or silently substitute BGM",
            "allowed_background_audio_modes": ["library_music_bgm"],
            "generated_background_audio_allowed": False,
            "mix_note": "BGM carries rhythm and must come from approved library/reference music; do not create SFX/noise beds.",
        }
    if scheme_id in {"scheme_2_source_led_tool_tutorial", "scheme_6_operation_proof_short"}:
        return {
            "music_policy": "voice_only_clean",
            "reason": "scheme default prioritizes clean narration/proof clarity over background audio",
            "bgm_source_priority": [],
            "voice_policy": "required_narration" if scheme_id == "scheme_2_source_led_tool_tutorial" else "optional_narration",
            "voice_priority": True,
            "sfx_required": False,
            "generated_bgm_allowed": False,
            "allowed_background_audio_modes": ["voice_only_clean", "library_music_bgm"],
            "generated_background_audio_allowed": False,
            "reference_bgm_policy": "default no BGM; if an approved Douyin reference requires BGM, use the same reference music or block",
            "mix_note": "Default to clean narration only; if music is needed, use approved library/reference music and never generate ambience/SFX beds.",
        }
    return {
        "music_policy": "voice_only_clean",
        "reason": "scheme default uses clean narration unless approved library/reference music is explicitly selected",
        "bgm_source_priority": ["authorized_local_library", "pixabay", "mixkit"],
        "voice_policy": "required_narration",
        "voice_priority": True,
        "sfx_required": False,
        "generated_bgm_allowed": False,
        "allowed_background_audio_modes": ["voice_only_clean", "library_music_bgm"],
        "generated_background_audio_allowed": False,
        "reference_bgm_policy": "when a user-provided Douyin reference has BGM, use the same reference music or block for user approval; do not generate or silently substitute BGM",
        "mix_note": "No generated/self-created background audio. If approved music is used, keep it roughly 18dB below narration.",
    }


def read_audio_music_decision(args: argparse.Namespace, scheme_id: str) -> dict[str, Any]:
    director = load_json(resolve_path(args.director_selection), {}) if args.director_selection else {}
    recipe = load_json(resolve_path(args.style_recipe), {}) if args.style_recipe else {}
    for source in (director, recipe):
        decision = source.get("audio_music_decision") if isinstance(source.get("audio_music_decision"), dict) else {}
        if decision:
            result = dict(decision)
            result.setdefault("decision_artifact", "audio_music_decision")
            return result
    result = default_audio_music_decision(scheme_id)
    result["decision_artifact"] = "audio_music_decision"
    result["fallback_generated_by"] = "scripts/select_fixed_ai_templates.py"
    return result


def state_index(state: dict[str, Any], key: str) -> int:
    pools = state.get("pools")
    if isinstance(pools, dict) and isinstance(pools.get(key), dict):
        return int(pools[key].get("next_index") or 0)
    return 0


def advance_state(state: dict[str, Any], key: str, next_index: int, selected_id: str, project: Path) -> dict[str, Any]:
    state.setdefault("version", 1)
    pools = state.setdefault("pools", {})
    if not isinstance(pools, dict):
        pools = {}
        state["pools"] = pools
    pools[key] = {
        "next_index": next_index,
        "last_selected_id": selected_id,
        "updated_at": now_iso(),
    }
    history = state.setdefault("history", [])
    if isinstance(history, list):
        history.append({"selected_at": now_iso(), "project": str(project), "pool": key, "selected_id": selected_id})
        del history[:-80]
    return state


def choose_rotating(
    entries: list[dict[str, Any]],
    state: dict[str, Any],
    state_key: str,
    project: Path,
    advance: bool,
) -> tuple[dict[str, Any], int, int]:
    if not entries:
        raise SystemExit(f"no fixed template candidates for {state_key}")
    index = state_index(state, state_key) % len(entries)
    selected = entries[index]
    next_index = (index + 1) % len(entries)
    if advance:
        advance_state(state, state_key, next_index, str(selected.get("id") or ""), project)
    return selected, index, next_index


def filter_by_scheme(entries: list[dict[str, Any]], scheme_id: str) -> list[dict[str, Any]]:
    matched = [item for item in entries if scheme_id in item.get("scheme_ids", [])]
    return matched or entries


def require_background_asset(background: dict[str, Any]) -> Path:
    asset_path = str(background.get("asset_path") or "").strip()
    template_id = str(background.get("id") or "unknown")
    if not asset_path:
        raise SystemExit(f"dynamic background asset_path missing for {template_id}")
    resolved = resolve_path(asset_path)
    if not resolved.exists() or not resolved.is_file() or resolved.stat().st_size == 0:
        raise SystemExit(f"dynamic background asset missing or empty for {template_id}: {resolved}")
    if resolved.suffix.lower() != ".mp4":
        raise SystemExit(f"dynamic background asset_path must point to an mp4 for {template_id}: {resolved}")
    poster_path = str(background.get("poster_path") or "").strip()
    if poster_path:
        poster = resolve_path(poster_path)
        if not poster.exists() or not poster.is_file() or poster.stat().st_size == 0:
            raise SystemExit(f"dynamic background poster missing or empty for {template_id}: {poster}")
    return resolved


def select_background(
    library: dict[str, Any],
    scheme_id: str,
    aspect: str,
    state: dict[str, Any],
    project: Path,
    advance: bool,
) -> tuple[dict[str, Any], str, int]:
    entries = [
        item for item in library.get("templates", [])
        if isinstance(item, dict) and item.get("aspect") == aspect
    ]
    candidates = filter_by_scheme(entries, scheme_id)
    state_key = f"background:{aspect}:{scheme_id}"
    selected, index, _ = choose_rotating(candidates, state, state_key, project, advance)
    return selected, state_key, index


def select_transition_pack(
    library: dict[str, Any],
    scheme_id: str,
    visual_family: str,
    state: dict[str, Any],
    project: Path,
    advance: bool,
) -> tuple[dict[str, Any], str, int]:
    entries = [item for item in library.get("packs", []) if isinstance(item, dict)]
    candidates = filter_by_scheme(entries, scheme_id)
    family_matches = [
        item for item in candidates
        if visual_family and visual_family in item.get("visual_families", [])
    ]
    if family_matches:
        candidates = family_matches
    state_key = f"transition:{scheme_id}:{visual_family or 'generic'}"
    selected, index, _ = choose_rotating(candidates, state, state_key, project, advance)
    return selected, state_key, index


def select_component_pack(
    library: dict[str, Any],
    scheme_id: str,
    state: dict[str, Any],
    project: Path,
    advance: bool,
) -> tuple[dict[str, Any], str, int]:
    entries = [item for item in library.get("packs", []) if isinstance(item, dict)]
    candidates = filter_by_scheme(entries, scheme_id)
    state_key = f"component:{scheme_id}"
    selected, index, _ = choose_rotating(candidates, state, state_key, project, advance)
    return selected, state_key, index


def select_voice_profile(library: dict[str, Any], scheme_id: str, no_voice: bool) -> dict[str, Any]:
    profiles = [item for item in library.get("profiles", []) if isinstance(item, dict)]
    if no_voice or scheme_id == "scheme_1_skill_recommendation_no_voice":
        for profile in profiles:
            if profile.get("id") == "VOICE_NO_VOICE_SFX_ONLY_V1":
                return profile
    default_id = library.get("default_profile_id") or "VOICE_MALE_THICK_YUNYANG_V1"
    for profile in profiles:
        if profile.get("id") == default_id:
            return profile
    if not profiles:
        raise SystemExit("voice profile library is empty")
    return profiles[0]


def compact_selection(item: dict[str, Any], state_key: str | None = None, rotation_index: int | None = None) -> dict[str, Any]:
    result = dict(item)
    if state_key is not None:
        result["state_key"] = state_key
    if rotation_index is not None:
        result["rotation_index"] = rotation_index
    return result


def build_selection(args: argparse.Namespace) -> dict[str, Any]:
    project = resolve_path(args.project)
    internal = project / "internal"
    aspect = detect_aspect(args)
    scheme_id, visual_family, background_style_id = read_scheme_and_style(args, aspect)
    audio_music_decision = read_audio_music_decision(args, scheme_id)
    state_file = resolve_path(args.state_file)
    state = load_json(state_file, {})
    advance = not args.no_advance_state

    background_library = load_json(resolve_path(args.background_library), {})
    transition_library = load_json(resolve_path(args.transition_library), {})
    component_library = load_json(resolve_path(args.component_library), {})
    voice_library = load_json(resolve_path(args.voice_library), {})
    scene_motion_library = load_json(resolve_path(args.scene_motion_library), {})

    background, background_key, background_index = select_background(background_library, scheme_id, aspect, state, project, advance)
    background_asset = require_background_asset(background)
    transition, transition_key, transition_index = select_transition_pack(transition_library, scheme_id, str(background.get("visual_family") or visual_family), state, project, advance)
    component, component_key, component_index = select_component_pack(component_library, scheme_id, state, project, advance)
    voice = select_voice_profile(voice_library, scheme_id, args.no_voice)

    if advance:
        write_json(state_file, state)

    background_selection = compact_selection(background, background_key, background_index)
    background_selection["fixed_asset_path"] = str(background_asset)
    background_selection["fixed_asset_exists"] = True
    background_selection["fixed_asset_path_legacy_alias"] = True
    background_selection["dynamic_asset_path"] = str(background_asset)
    background_selection["dynamic_asset_exists"] = True
    background_selection["dynamic_asset_source_type"] = background.get("asset_source_type")
    background_selection["dynamic_generation_method"] = background.get("asset_generation_method")
    background_selection["dynamic_motion_profile"] = background.get("motion_profile")
    background_selection["dynamic_motion_description"] = background.get("motion_affordance")
    background_selection["render_asset_path"] = str(background_asset)
    background_selection["render_asset_type"] = "fixed_dynamic_background_video_asset"
    background_selection["render_asset_is_dynamic"] = True

    selection = {
        "status": "passed",
        "created_at": now_iso(),
        "project": str(project),
        "selection_method": "semantic_fit_then_sequential_rotation",
        "state_file": str(state_file),
        "state_advanced": advance,
        "video": {
            "aspect": aspect,
            "width": args.video_width,
            "height": args.video_height,
        },
        "content": {
            "scheme_id": scheme_id,
            "visual_family_from_director": visual_family,
            "background_style_id_from_director": background_style_id,
        },
        "background_template": background_selection,
        "transition_sfx_pack": compact_selection(transition, transition_key, transition_index),
        "component_pack": compact_selection(component, component_key, component_index),
        "voice_mix_profile": voice,
        "audio_music_decision": audio_music_decision,
        "scene_motion_templates": {
            "registry": str(resolve_path(args.scene_motion_library)),
            "version": scene_motion_library.get("version"),
            "main_project_template": scene_motion_library.get("main_project_template", {}),
            "transition_recipes": [
                item.get("recipe_id")
                for item in scene_motion_library.get("transition_templates", [])
                if isinstance(item, dict)
            ],
            "entrance_templates": [
                item.get("entrance_id")
                for item in scene_motion_library.get("entrance_rhythm_templates", [])
                if isinstance(item, dict)
            ],
            "foreground_module_runtime": scene_motion_library.get("foreground_module_runtime", {}),
            "topic_candidate_v3_template": scene_motion_library.get("topic_candidate_v3_template", {}),
            "ai_hot_rank_top5_template": scene_motion_library.get("ai_hot_rank_top5_template", {}),
            "prompt_pack_template": scene_motion_library.get("prompt_pack_template", {}),
            "hyperframes_render_profile": scene_motion_library.get("hyperframes_render_profile", {}),
            "ffmpeg_route_template": scene_motion_library.get("ffmpeg_route_template", {}),
            "cover_text_layout": scene_motion_library.get("cover_text_layout", {}),
            "qa_repair_actions": scene_motion_library.get("qa_repair_actions", []),
        },
        "inheritance_contract": {
            "background_drives_foreground": True,
            "transition_pack_drives_sfx": True,
            "component_pack_drives_storyboard_shapes": True,
            "voice_profile_drives_tts_and_mix": True,
            "music_policy_drives_bgm_and_mix": True,
            "scene_motion_templates_drive_hyperframes": bool(scene_motion_library.get("rules", {}).get("premium_only_default")),
            "no_low_quality_motion_fallback": bool(scene_motion_library.get("rules", {}).get("no_low_grade_fallback")),
            "fixed_background_asset_required": True,
            "dynamic_background_asset_required": True,
            "dynamic_background_default": True,
            "static_background_fallback_removed": True,
            "no_per_scene_random_art_direction": True,
            "dynamic_text_still_requires_compliance": True,
            "premium_motion_library_required": bool(transition_library.get("rules", {}).get("premium_only_default")),
            "forbidden_low_grade_effects_blocking": True,
            "layout_manifest_required": bool(component_library.get("rules", {}).get("layout_manifest_required")),
            "text_fit_before_render_required": bool(component_library.get("rules", {}).get("text_must_fit_before_render")),
            "three_column_grid_required": bool(component_library.get("rules", {}).get("three_column_components_must_use_grid"))
        },
        "motion_layout_contract": {
            "forbidden_low_grade_effects": transition_library.get("rules", {}).get("forbidden_low_grade_effects", []),
            "required_transition_handoff": transition_library.get("rules", {}).get("handoff_required") is True,
            "required_transition_state_change": transition_library.get("rules", {}).get("transition_must_move_information_state") is True,
            "component_layout_contract": component.get("layout_contract") or {},
            "global_layout_rules": component_library.get("rules", {}),
            "required_report": "internal/layout_motion_contract_report.json",
            "required_manifest": "internal/render_layout_manifest.json"
        },
        "required_downstream_usage": [
            "visual_style_plan.json must cite background_template.id, background_template.render_asset_path, background_template.fixed_asset_path, and transition_sfx_pack.id",
            "HyperFrames must use background_template.render_asset_path as the base visual layer; render_asset_path is always a dynamic MP4",
            "storyboard.director_shots must use component_pack.components as shape vocabulary",
            "HyperFrames transitions must use transition_sfx_pack.transition_language and sfx_cues",
            "metadata.voice and voice_mix_report must use voice_mix_profile unless user overrides",
            "storyboard, audio mix, and metadata must cite audio_music_decision.music_policy before choosing BGM",
            "HyperFrames index.html must start from scene_motion_templates.main_project_template instead of a per-video handwritten shell",
            "HyperFrames entrances must use scene_motion_templates.entrance_templates and show primary scene content within 0.4s",
            "foreground modules should render from scene_motion_templates.foreground_module_runtime for the common 8 module types",
            "topic_candidates.json should be generated from scene_motion_templates.topic_candidate_v3_template after live scan",
            "background prompt packs should fill scene_motion_templates.prompt_pack_template instead of ad hoc visual director text",
            "HyperFrames must write positive premium recipe ids and information handoff actions from motion_layout_contract",
            "render_layout_manifest.json must record text boxes, measured text bounds, padding, collisions, and three-column baseline checks",
            "layout_motion_contract_report.json must pass before visual_regression_gate or final delivery"
        ]
    }
    write_json(internal / "fixed_template_selection.json", selection)
    return selection


def main() -> int:
    parser = argparse.ArgumentParser(description="Select fixed background, transition/SFX, component, and voice templates.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument("--selected-topic")
    parser.add_argument("--director-selection")
    parser.add_argument("--style-recipe")
    parser.add_argument("--video-width", type=int)
    parser.add_argument("--video-height", type=int)
    parser.add_argument("--aspect", choices=["auto", "16:9", "9:16"], default="auto")
    parser.add_argument("--no-voice", action="store_true")
    parser.add_argument("--no-advance-state", action="store_true")
    parser.add_argument("--state-file", default=str(DEFAULT_STATE))
    parser.add_argument("--background-library", default=str(DEFAULT_BACKGROUND))
    parser.add_argument("--transition-library", default=str(DEFAULT_TRANSITIONS))
    parser.add_argument("--component-library", default=str(DEFAULT_COMPONENTS))
    parser.add_argument("--voice-library", default=str(DEFAULT_VOICE))
    parser.add_argument("--scene-motion-library", default=str(DEFAULT_SCENE_MOTION))
    args = parser.parse_args()

    selection = build_selection(args)
    print(json.dumps({
        "status": selection["status"],
        "out": str(resolve_path(args.project) / "internal" / "fixed_template_selection.json"),
        "background_template": selection["background_template"]["id"],
        "background_fixed_asset": selection["background_template"]["fixed_asset_path"],
        "background_render_asset": selection["background_template"]["render_asset_path"],
        "background_render_asset_type": selection["background_template"]["render_asset_type"],
        "transition_sfx_pack": selection["transition_sfx_pack"]["id"],
        "component_pack": selection["component_pack"]["id"],
        "voice_mix_profile": selection["voice_mix_profile"]["id"],
        "music_policy": selection["audio_music_decision"]["music_policy"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
