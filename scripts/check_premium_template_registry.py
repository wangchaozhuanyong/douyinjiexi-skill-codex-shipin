#!/usr/bin/env python3
"""Validate premium AI video template registries and render-ready assets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from asset_prompt_contract import validate_prompt_pack_text
from check_ant_ai_galaxy_template import validate as validate_ant_ai_galaxy_template


ROOT = Path(__file__).resolve().parents[1]
SCENE_REGISTRY = ROOT / "references" / "fixed_ai_scene_motion_templates.json"
TRANSITION_PACKS = ROOT / "references" / "fixed_ai_transition_sfx_packs.json"
MAIN_TEMPLATE = ROOT / "templates" / "hyperframes" / "ai_premium_main_16x9.html"
MOTION_RUNTIME = ROOT / "assets" / "hyperframes_components" / "advanced_motion_templates.js"
MODULE_RUNTIME = ROOT / "assets" / "hyperframes_components" / "premium_foreground_modules.js"
MODULE_CSS = ROOT / "assets" / "hyperframes_components" / "premium_foreground_modules.css"
TOPIC_TEMPLATE = ROOT / "templates" / "topic_candidates_v3.template.json"
TOP5_TEMPLATE = ROOT / "templates" / "ai_hot_rank_top5.template.json"
ANT_AI_TOP5_EXTENDED_DOC = ROOT / "references" / "ai_video_scheme_7_ant_ai_hotlist_extended.md"
ANT_AI_GALAXY_DESIGN_CONTRACT = ROOT / "references" / "ant_ai_hotlist_galaxy_design_contract.md"
ANT_AI_GALAXY_QUALITY_CHECKLIST = ROOT / "references" / "ant_ai_hotlist_galaxy_quality_checklist.md"
ANT_AI_GALAXY_PREVIEW = ROOT / "templates" / "ant_ai_hotlist_galaxy" / "preview.html"
ANT_AI_GALAXY_RENDERER_CONFIG = ROOT / "templates" / "ant_ai_hotlist_galaxy" / "renderer_config.json"
PROMPT_TEMPLATE = ROOT / "templates" / "prompt_pack" / "fixed_background_visual_contract.md"

REQUIRED_RECIPES = {
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
}

REQUIRED_ENTRANCES = {
    "source_proof_snap_in",
    "result_first_plate_reveal",
    "checklist_step_assembly",
    "two_column_compare_build",
    "terminal_proof_rise",
    "cursor_operation_land",
    "metric_lock_sequence",
    "timeline_node_relay_in",
    "final_template_converge_in",
    "micro_component_layer_settle",
}

REQUIRED_MODULES = {
    "source_evidence_card",
    "three_step_checklist",
    "before_after_compare",
    "test_result_panel",
    "conclusion_stamp",
    "state_lock",
    "node_relay",
    "metric_drum",
}

REQUIRED_TOPIC_FIELDS = {
    "topic_id",
    "title_direction",
    "core_angle",
    "content_format",
    "format_reason",
    "target_viewer",
    "viewer_pain",
    "why_now",
    "curiosity_gap",
    "save_reason",
    "comment_trigger",
    "visual_potential",
    "proof_assets_needed",
    "main_claims",
    "sources",
    "risk_flags",
    "beginner_task",
    "visible_result",
    "first_action",
    "time_saving_claim",
    "scores",
}

REQUIRED_SCORE_FIELDS = {
    "beginner_usefulness_score",
    "visible_result_score",
    "time_saving_score",
    "pain_score",
    "novelty_score",
    "save_score",
    "comment_score",
    "visual_score",
    "compliance_safety_score",
    "total_score",
}

REQUIRED_TOP5_RANK_FIELDS = {
    "rank",
    "title",
    "source_title",
    "source_url_or_note",
    "visible_date",
    "why_now",
    "why_it_matters",
    "viewer_action",
    "visual_line",
    "source_pin_text",
    "risk_flags",
    "score_breakdown",
    "rank_score",
}

REQUIRED_TOP5_SCORE_FIELDS = {
    "freshness",
    "impact",
    "practical_value",
    "source_strength",
    "visual_clarity",
    "compliance_safety",
}

BANNED_TEMPLATE_TERMS = [
    "diagonal line sweep",
    "diagonal sweep",
    "random horizontal light streak",
    "plain fade",
    "ordinary fade",
    "ordinary crossfade",
    "simple slide",
    "ordinary slide",
    "decoration-only connector line",
    "empty rail sweep",
    "card carousel",
    "斜线扫光",
    "斜线扫描",
    "横向小光条乱跑",
    "普通淡入淡出",
    "普通左右滑入",
    "无信息作用线条",
    "空导轨扫过",
    "旧卡片轮播",
]

SCAN_TEMPLATE_PATHS = [
    SCENE_REGISTRY,
    MAIN_TEMPLATE,
    MOTION_RUNTIME,
    MODULE_RUNTIME,
    MODULE_CSS,
    TOPIC_TEMPLATE,
    TOP5_TEMPLATE,
    ANT_AI_TOP5_EXTENDED_DOC,
    PROMPT_TEMPLATE,
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if exists(path) else ""


def validate_scene_registry(registry: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    rules = registry.get("rules") if isinstance(registry.get("rules"), dict) else {}
    canvas = registry.get("canvas") if isinstance(registry.get("canvas"), dict) else {}
    if rules.get("premium_only_default") is not True:
        issues.append("scene registry must set premium_only_default=true")
    if rules.get("no_low_grade_fallback") is not True:
        issues.append("scene registry must set no_low_grade_fallback=true")
    if rules.get("block_when_no_matching_template") is not True:
        issues.append("scene registry must block when no matching premium template exists")
    if float(canvas.get("scene_content_deadline_sec") or 9) > 0.4:
        issues.append("scene content deadline must be <= 0.4s")
    if int(canvas.get("cover_frame_count") or 0) != 1:
        issues.append("cover frame count must be exactly 1")

    transitions = registry.get("transition_templates") if isinstance(registry.get("transition_templates"), list) else []
    entrances = registry.get("entrance_rhythm_templates") if isinstance(registry.get("entrance_rhythm_templates"), list) else []
    recipes = {str(item.get("recipe_id")) for item in transitions if isinstance(item, dict)}
    entrance_ids = {str(item.get("entrance_id")) for item in entrances if isinstance(item, dict)}
    if recipes != REQUIRED_RECIPES:
        issues.append(f"transition recipes must match required 10 premium recipes; got {sorted(recipes)}")
    if entrance_ids != REQUIRED_ENTRANCES:
        issues.append(f"entrance templates must match required 10 premium entrances; got {sorted(entrance_ids)}")
    for item in transitions:
        if not isinstance(item, dict):
            continue
        label = str(item.get("recipe_id") or item.get("transition_id"))
        if item.get("quality_tier") != "premium_only":
            issues.append(f"{label} quality_tier must be premium_only")
        if not item.get("information_job"):
            issues.append(f"{label} must bind an information_job")
        if not item.get("sfx_cues"):
            issues.append(f"{label} must bind sfx_cues")
        if float(item.get("frame_content_deadline_sec") or 9) > 0.4:
            issues.append(f"{label} content deadline must be <= 0.4s")
        if len(item.get("target_roles") or []) < 3:
            issues.append(f"{label} needs at least 3 target roles")
    for item in entrances:
        if not isinstance(item, dict):
            continue
        label = str(item.get("entrance_id"))
        if item.get("quality_tier") != "premium_only":
            issues.append(f"{label} quality_tier must be premium_only")
        if not item.get("information_job"):
            issues.append(f"{label} must bind an information_job")
        if not item.get("sfx_cues"):
            issues.append(f"{label} must bind sfx_cues")
        if float(item.get("frame_content_deadline_sec") or 9) > 0.4:
            issues.append(f"{label} content deadline must be <= 0.4s")
        if len(item.get("required_targets") or []) < 3:
            issues.append(f"{label} needs at least 3 required targets")

    runtime = registry.get("foreground_module_runtime") if isinstance(registry.get("foreground_module_runtime"), dict) else {}
    module_types = set(runtime.get("module_types") or [])
    if module_types != REQUIRED_MODULES:
        issues.append(f"foreground module runtime must register 8 module types; got {sorted(module_types)}")
    top5 = registry.get("ai_hot_rank_top5_template") if isinstance(registry.get("ai_hot_rank_top5_template"), dict) else {}
    if top5.get("path") != "templates/ai_hot_rank_top5.template.json":
        issues.append("scene registry must expose ai_hot_rank_top5_template.path")
    if top5.get("scheme_id") != "scheme_7_ai_hot_rank_top5":
        issues.append("scene registry ai_hot_rank_top5_template must use scheme_7_ai_hot_rank_top5")
    extended = top5.get("extended_profiles") if isinstance(top5.get("extended_profiles"), dict) else {}
    ant_ai = extended.get("ant_ai_hotlist_extended") if isinstance(extended.get("ant_ai_hotlist_extended"), dict) else {}
    if not ant_ai:
        issues.append("scene registry must expose ant_ai_hotlist_extended profile")
    else:
        required_pairs = {
            "reference_doc": "references/ai_video_scheme_7_ant_ai_hotlist_extended.md",
            "brand_name": "蚂蚁AI",
            "fixed_cta": "关注 蚂蚁AI",
            "background_template_id": "BG_FIXED_11_ANT_AI_HOTLIST_NEBULA_9X16",
            "bgm_source_id": "ant_ai_scheme7_top5_reference_bgm_7654135072895400421",
            "voice_profile_id": "VOICE_MALE_THICK_YUNYANG_V1",
        }
        for key, expected in required_pairs.items():
            if ant_ai.get(key) != expected:
                issues.append(f"scene registry ant_ai_hotlist_extended.{key} must be {expected}")
        if ant_ai.get("copywriting_grammar_locked") is not True:
            issues.append("scene registry ant_ai_hotlist_extended must lock copywriting grammar")
        if ant_ai.get("source_backed_current_scan_required") is not True:
            issues.append("scene registry ant_ai_hotlist_extended must require source-backed current scan")
    route = registry.get("ffmpeg_route_template") if isinstance(registry.get("ffmpeg_route_template"), dict) else {}
    if route.get("direct_hyperframes_mp4_is_not_final_source") is not True:
        issues.append("ffmpeg route must reject direct HyperFrames MP4 as final source")
    if route.get("final_folder_single_file") != "final/final.mp4":
        issues.append("final route must keep only final/final.mp4")
    cover = registry.get("cover_text_layout") if isinstance(registry.get("cover_text_layout"), dict) else {}
    if cover.get("frame_zero_only") is not True or cover.get("frame_one_returns_to_main_timeline") is not True:
        issues.append("cover layout must enforce frame 0 cover and frame 1 main timeline")
    return issues


def validate_transition_pack_reference(packs: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    entries = packs.get("packs") if isinstance(packs.get("packs"), list) else []
    recipes = {str(item.get("recipe_id")) for item in entries if isinstance(item, dict)}
    if len(entries) != 10:
        issues.append(f"fixed transition/SFX pack count must be 10, got {len(entries)}")
    if not REQUIRED_RECIPES.issubset(recipes):
        issues.append("fixed transition/SFX packs must cover all required premium recipes")
    rules = packs.get("rules") if isinstance(packs.get("rules"), dict) else {}
    if rules.get("premium_only_default") is not True:
        issues.append("fixed transition/SFX packs must set premium_only_default=true")
    if rules.get("transition_must_move_information_state") is not True:
        issues.append("fixed transition/SFX packs must require information-state handoff")
    return issues


def validate_runtime_assets() -> list[str]:
    issues: list[str] = []
    motion_text = text(MOTION_RUNTIME)
    module_text = text(MODULE_RUNTIME)
    css_text = text(MODULE_CSS)
    main_text = text(MAIN_TEMPLATE)
    for recipe in REQUIRED_RECIPES:
        if recipe not in motion_text:
            issues.append(f"advanced motion runtime missing recipe id: {recipe}")
    for entrance in REQUIRED_ENTRANCES:
        if entrance not in motion_text:
            issues.append(f"advanced motion runtime missing entrance id: {entrance}")
    for module_type in REQUIRED_MODULES:
        if module_type not in module_text:
            issues.append(f"premium foreground runtime missing module type: {module_type}")
        css_marker = ".premium-module--" + module_type.replace("_", "-")
        if css_marker not in css_text and ".premium-module" not in css_text:
            issues.append(f"premium foreground CSS missing module styling for: {module_type}")
    required_tokens = [
        "{{BACKGROUND_IMAGE}}",
        "{{SCENES_HTML}}",
        "{{SCENE_DATA_JSON}}",
        "{{MOTION_PLAN_JSON}}",
        "{{COVER_TITLE}}",
        "{{COVER_SUBTITLE}}",
    ]
    for token in required_tokens:
        if token not in main_text:
            issues.append(f"main HyperFrames template missing token {token}")
    for required in ["AdvancedMotionTemplates", "PremiumForegroundModules", "data-cover-frame-count=\"1\"", "setFrame(0)"]:
        if required not in main_text:
            issues.append(f"main HyperFrames template missing required runtime marker: {required}")
    return issues


def validate_topic_template(data: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    candidate = data.get("candidate_template") if isinstance(data.get("candidate_template"), dict) else {}
    missing = sorted(REQUIRED_TOPIC_FIELDS - set(candidate))
    if missing:
        issues.append("topic candidate V3 template missing fields: " + ", ".join(missing))
    scores = candidate.get("scores") if isinstance(candidate.get("scores"), dict) else {}
    missing_scores = sorted(REQUIRED_SCORE_FIELDS - set(scores))
    if missing_scores:
        issues.append("topic candidate V3 template missing score fields: " + ", ".join(missing_scores))
    if int(data.get("minimum_candidates") or 0) < 3:
        issues.append("topic candidate V3 template must require at least 3 candidates")
    if data.get("selection_gate", {}).get("must_not_invent_hot_signal") is not True:
        issues.append("topic candidate V3 template must forbid invented hot signals")
    return issues


def validate_top5_template(data: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if data.get("scheme_id") != "scheme_7_ai_hot_rank_top5":
        issues.append("AI hot rank TOP5 template must use scheme_7_ai_hot_rank_top5")
    policy = data.get("ranking_policy") if isinstance(data.get("ranking_policy"), dict) else {}
    if int(policy.get("rank_count") or 0) != 5:
        issues.append("AI hot rank TOP5 template must require exactly five rank items")
    if policy.get("must_not_invent_hot_signal") is not True:
        issues.append("AI hot rank TOP5 template must forbid invented hot signals")
    if policy.get("absolute_ranking_claims_forbidden_without_official_ranked_source") is not True:
        issues.append("AI hot rank TOP5 template must forbid absolute ranking claims without official ranked source")
    rank_item = data.get("rank_item_template") if isinstance(data.get("rank_item_template"), dict) else {}
    missing = sorted(REQUIRED_TOP5_RANK_FIELDS - set(rank_item))
    if missing:
        issues.append("AI hot rank TOP5 rank item template missing fields: " + ", ".join(missing))
    scores = rank_item.get("score_breakdown") if isinstance(rank_item.get("score_breakdown"), dict) else {}
    missing_scores = sorted(REQUIRED_TOP5_SCORE_FIELDS - set(scores))
    if missing_scores:
        issues.append("AI hot rank TOP5 score breakdown missing fields: " + ", ".join(missing_scores))
    audio = data.get("audio_policy") if isinstance(data.get("audio_policy"), dict) else {}
    if audio.get("reference_bgm_required_when_reference_has_music") is not True:
        issues.append("AI hot rank TOP5 template must require BGM when the reference has music")
    if audio.get("generated_bgm_allowed") is not False:
        issues.append("AI hot rank TOP5 template must forbid generated replacement BGM")
    if audio.get("replacement_requires_explicit_user_approval") is not True:
        issues.append("AI hot rank TOP5 template must require explicit user approval before replacing unavailable reference BGM")
    gate = data.get("selection_gate") if isinstance(data.get("selection_gate"), dict) else {}
    for key in (
        "requires_exactly_five_ranked_items",
        "requires_descending_rank_score",
        "requires_source_for_every_rank",
        "requires_visible_date_for_every_rank",
        "requires_bgm_plan",
    ):
        if gate.get(key) is not True:
            issues.append(f"AI hot rank TOP5 selection gate must set {key}=true")
    extended = data.get("extended_profiles") if isinstance(data.get("extended_profiles"), dict) else {}
    ant_ai = extended.get("ant_ai_hotlist_extended") if isinstance(extended.get("ant_ai_hotlist_extended"), dict) else {}
    if not ant_ai:
        issues.append("AI hot rank TOP5 template must define ant_ai_hotlist_extended")
    else:
        required_pairs = {
            "brand_name": "蚂蚁AI",
            "fixed_cta": "关注 蚂蚁AI",
            "background_template_id": "BG_FIXED_11_ANT_AI_HOTLIST_NEBULA_9X16",
            "dynamic_background_path": "assets/ai_background_templates_dynamic/BG_DYNAMIC_11_蚂蚁AI热榜星云_9x16.mp4",
            "bgm_source_id": "ant_ai_scheme7_top5_reference_bgm_7654135072895400421",
            "voice_profile_id": "VOICE_MALE_THICK_YUNYANG_V1",
            "voice_policy": "required_narration",
        }
        for key, expected in required_pairs.items():
            if ant_ai.get(key) != expected:
                issues.append(f"AI hot rank TOP5 ant_ai_hotlist_extended.{key} must be {expected}")
        search = ant_ai.get("search_policy") if isinstance(ant_ai.get("search_policy"), dict) else {}
        if search.get("real_sources_only") is not True:
            issues.append("AI hot rank TOP5 ant_ai_hotlist_extended must require real_sources_only")
        if search.get("must_not_invent_hot_signal") is not True:
            issues.append("AI hot rank TOP5 ant_ai_hotlist_extended must forbid invented hot signals")
        copy = ant_ai.get("copywriting_policy") if isinstance(ant_ai.get("copywriting_policy"), dict) else {}
        if copy.get("not_fixed_copy") is not True:
            issues.append("AI hot rank TOP5 ant_ai_hotlist_extended must mark copy as grammar-based, not fixed copy")
    return issues


def validate_banned_template_terms() -> list[str]:
    issues: list[str] = []
    for path in SCAN_TEMPLATE_PATHS:
        surface = text(path).lower()
        for term in BANNED_TEMPLATE_TERMS:
            if term.lower() in surface:
                issues.append(f"{path.relative_to(ROOT)} contains banned low-quality motion term: {term}")
    return issues


def validate() -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []
    required_files = [
        SCENE_REGISTRY,
        TRANSITION_PACKS,
        MAIN_TEMPLATE,
        MOTION_RUNTIME,
        MODULE_RUNTIME,
        MODULE_CSS,
        TOPIC_TEMPLATE,
        TOP5_TEMPLATE,
        ANT_AI_TOP5_EXTENDED_DOC,
        ANT_AI_GALAXY_DESIGN_CONTRACT,
        ANT_AI_GALAXY_QUALITY_CHECKLIST,
        ANT_AI_GALAXY_PREVIEW,
        ANT_AI_GALAXY_RENDERER_CONFIG,
        PROMPT_TEMPLATE,
    ]
    for path in required_files:
        if not exists(path):
            issues.append(f"missing required template file: {path.relative_to(ROOT)}")
    if issues:
        return {"status": "failed", "blocking_issues": issues, "warnings": warnings, "signals": {}}

    scene_registry = load_json(SCENE_REGISTRY)
    transition_packs = load_json(TRANSITION_PACKS)
    topic_template = load_json(TOPIC_TEMPLATE)
    top5_template = load_json(TOP5_TEMPLATE)
    prompt_text = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    prompt_report = validate_prompt_pack_text(prompt_text, min_cards=1)
    ant_ai_galaxy_report = validate_ant_ai_galaxy_template()

    issues.extend(validate_scene_registry(scene_registry))
    issues.extend(validate_transition_pack_reference(transition_packs))
    issues.extend(validate_runtime_assets())
    issues.extend(validate_topic_template(topic_template))
    issues.extend(validate_top5_template(top5_template))
    issues.extend(validate_banned_template_terms())
    if prompt_report["status"] != "passed":
        issues.extend("prompt pack template: " + item for item in prompt_report["blocking_issues"])
    if ant_ai_galaxy_report["status"] != "passed":
        issues.extend("ant ai galaxy template: " + item for item in ant_ai_galaxy_report["blocking_issues"])

    return {
        "status": "passed" if not issues else "failed",
        "blocking_issues": issues,
        "warnings": warnings,
        "signals": {
            "transition_template_count": len(scene_registry.get("transition_templates", [])),
            "entrance_template_count": len(scene_registry.get("entrance_rhythm_templates", [])),
            "foreground_module_count": len(scene_registry.get("foreground_module_runtime", {}).get("module_types", [])),
            "prompt_card_count": prompt_report["prompt_card_count"],
            "top5_template": str(TOP5_TEMPLATE.relative_to(ROOT)),
            "ant_ai_galaxy_template": str(ANT_AI_GALAXY_RENDERER_CONFIG.relative_to(ROOT)),
            "main_template": str(MAIN_TEMPLATE.relative_to(ROOT)),
            "motion_runtime": str(MOTION_RUNTIME.relative_to(ROOT)),
            "module_runtime": str(MODULE_RUNTIME.relative_to(ROOT)),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate premium AI video production templates.")
    parser.add_argument("--out", default=str(ROOT / "outputs" / "premium_template_registry_report.json"))
    args = parser.parse_args()

    report = validate()
    write_json(Path(args.out), report)
    print(json.dumps({"status": report["status"], "issues": report["blocking_issues"], "warnings": report["warnings"]}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
