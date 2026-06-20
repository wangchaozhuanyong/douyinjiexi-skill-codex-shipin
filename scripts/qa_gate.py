#!/usr/bin/env python3
"""Final QA gate for output projects.

The gate validates the internal draft package and writes ``qa_report.json``.
It does not create ``final/`` artifacts. Build ``publish_contract.json`` and run
``pre_publish_gate.py`` before ``promote_final.py``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from voice_quality import voice_provider_passes

NO_SFX_POLICY_TERMS = [
    "no added sfx",
    "no sfx",
    "without sfx",
    "sfx disabled",
    "none",
]
WEAK_RUNTIME_TERMS = [
    "ffmpeg portrait card pipeline",
    "ffmpeg card pipeline",
    "portrait card pipeline",
    "card-only",
    "text-card slideshow",
]
LOCAL_SUMMARY_CARD_TERMS = [
    "official_source_card_local_render",
    "source card",
    "summary card",
    "local original card",
    "local render",
    "本地原创证据卡",
    "原创证据卡",
    "自制摘要卡",
]
BACKGROUND_PROMPT_PACK_NAMES = ("background_prompt_pack.md", "ai_asset_prompt_pack.md")
BACKGROUND_SEMANTIC_REQUIRED_FIELDS = (
    "visual_thesis",
    "topic_binding",
    "information_job",
    "background_role",
)
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
TONE_CHECK_VISUAL_TYPES = {"generated_visual", "designed_card"}
TONE_CHECK_VISUAL_ROLES = {
    "background_plate",
    "hero_poster",
    "metaphor_visual",
    "transition_plate",
    "diagram_base",
    "cover",
    "support_card",
}
VISUAL_STYLE_DECISION_REQUIRED_FIELDS = (
    "style_intent",
    "selected_brightness_grade",
    "selected_palette_family",
    "selected_material_family",
    "selected_layout_family",
    "why_this_style",
    "why_not_other_styles",
)
VISUAL_STYLE_DECISION_PLAN_KEYS = {
    "selected_brightness_grade": ("selected_brightness_grade", "primary_brightness_grade", "brightness_grade"),
    "selected_palette_family": ("selected_palette_family", "primary_palette_family", "palette_family"),
    "selected_material_family": ("selected_material_family", "primary_material_family", "material_family"),
    "selected_layout_family": ("selected_layout_family", "primary_layout_family", "layout_family"),
}
DIRECTOR_SELECTION_REQUIRED_FIELDS = (
    "status",
    "content_job_lock",
    "scheme",
    "reference_policy",
    "visual_system",
    "component_mix",
    "motion_palette",
    "why_selected",
    "why_not_other_schemes",
)
STYLE_RECIPE_REQUIRED_FIELDS = (
    "status",
    "selected_visual_family",
    "background_style_id",
    "component_ids",
    "motion_primitives",
    "caption_template_family",
    "transition_language",
    "sfx_character",
    "cooldown",
)
FIXED_TEMPLATE_REQUIRED_FIELDS = (
    "background_template",
    "transition_sfx_pack",
    "component_pack",
    "voice_mix_profile",
    "inheritance_contract",
)
FIXED_TEMPLATE_REQUIRED_CONTRACT_FLAGS = (
    "background_drives_foreground",
    "fixed_background_asset_required",
    "transition_pack_drives_sfx",
    "component_pack_drives_storyboard_shapes",
    "voice_profile_drives_tts_and_mix",
    "no_per_scene_random_art_direction",
)
REFERENCE_FORBIDDEN_TERMS = ("frame", "subtitle", "wording", "voice", "sequence")
BRIGHT_DEFAULT_STYLE_TERMS = (
    "daylight productivity",
    "daylight_productivity",
    "l4 bright tutorial",
    "l5 cover/result bright",
    "bright productivity",
    "bright_productivity",
    "clean tutorial canvas",
    "浅色",
    "明亮",
)
MECHANICAL_STYLE_REASON_TERMS = (
    "default",
    "same as last",
    "recent success",
    "fixed style",
    "reuse",
    "mechanical",
    "默认",
    "沿用",
    "最近成功",
    "固定",
    "偷懒",
)
CONTENT_STYLE_SIGNAL_TERMS = (
    "tutorial",
    "template",
    "news",
    "source",
    "proof",
    "terminal",
    "code",
    "warning",
    "risk",
    "product",
    "release",
    "reference",
    "list",
    "skill",
    "tool",
    "workflow",
    "evidence",
    "copy",
    "audience",
    "beginner",
    "教程",
    "模板",
    "新闻",
    "证据",
    "终端",
    "源码",
    "避坑",
    "风险",
    "发布",
    "产品",
    "参考",
    "清单",
    "工具",
    "生产栈",
    "工作流",
    "文案",
    "小白",
    "观众",
    "效率",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def dir_exists(path: Path) -> bool:
    return path.exists() and path.is_dir()


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if exists(path):
            return path
    return paths[0]


def bool_gate(gates: dict[str, bool], key: str, value: bool, issues: list[str], message: str) -> None:
    gates[key] = bool(value)
    if not value:
        issues.append(message)


def unique_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        unique.append(item)
    return unique


def get_score(data: dict[str, Any], *names: str, default: float = 0.0) -> float:
    for name in names:
        if name in data:
            try:
                return float(data[name])
            except Exception:
                return default
    return default


def normal_tts_speed(metadata: dict[str, Any]) -> bool:
    try:
        speed = float(metadata.get("tts_speed"))
    except Exception:
        return False
    if 0.95 <= speed <= 1.03:
        return True
    approval_text = " ".join(
        [
            str(metadata.get("voice_speed_policy", "")),
            str(metadata.get("voice_speed_approval", "")),
            str(metadata.get("voice", {}).get("approval_status", "") if isinstance(metadata.get("voice"), dict) else ""),
            str(metadata.get("voice", {}).get("notes", "") if isinstance(metadata.get("voice"), dict) else ""),
        ]
    ).lower()
    has_user_approval = any(
        marker in approval_text
        for marker in ["user requested", "user approved", "explicit user", "用户要求", "用户明确", "用户批准"]
    )
    return 1.03 < speed <= 1.10 and has_user_approval


def normalized_text(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", " ")


def contains_term(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def normalized_style_text(*values: Any) -> str:
    parts: list[str] = []
    for value in values:
        if isinstance(value, (dict, list)):
            parts.append(json.dumps(value, ensure_ascii=False))
        else:
            parts.append(str(value or ""))
    return " ".join(parts).strip().lower().replace("-", " ").replace("_", " ")


def contains_style_term(text: str, terms: tuple[str, ...]) -> bool:
    return any(normalized_style_text(term) in text for term in terms)


def first_nonempty(data: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value
        if value not in (None, "") and not isinstance(value, str):
            return value
    return ""


def visual_style_decision_issues(
    decision: dict[str, Any],
    visual_style_plan: dict[str, Any] | None = None,
) -> list[str]:
    if not isinstance(decision, dict):
        return ["visual_style_decision.json must be a JSON object"]

    issues: list[str] = []
    for field in VISUAL_STYLE_DECISION_REQUIRED_FIELDS:
        if not str(decision.get(field, "")).strip():
            issues.append(f"visual_style_decision.json missing required field: {field}")

    status = normalized_style_text(decision.get("status"))
    if status in {"failed", "draft", "unchecked"}:
        issues.append("visual_style_decision.json status must be locked/passed/selected, not draft or failed")

    plan = visual_style_plan if isinstance(visual_style_plan, dict) else {}
    for selected_key, plan_keys in VISUAL_STYLE_DECISION_PLAN_KEYS.items():
        selected = first_nonempty(decision, (selected_key,))
        planned = first_nonempty(plan, plan_keys)
        if selected and planned and normalized_style_text(selected) != normalized_style_text(planned):
            issues.append(f"visual_style_decision.json {selected_key} must match visual_style_plan.json {plan_keys[0]}")

    why_this_style = normalized_style_text(decision.get("why_this_style"))
    reason_blob = normalized_style_text(
        decision.get("style_intent"),
        decision.get("why_this_style"),
        decision.get("why_not_other_styles"),
        decision.get("decision_inputs"),
        decision.get("content_type"),
        decision.get("copy_mood"),
        decision.get("evidence_density"),
        decision.get("reference_video"),
    )
    selected_blob = normalized_style_text(
        decision.get("selected_brightness_grade"),
        decision.get("selected_palette_family"),
        decision.get("selected_material_family"),
        decision.get("selected_layout_family"),
        decision.get("style_intent"),
    )
    chose_bright_default = contains_style_term(selected_blob, BRIGHT_DEFAULT_STYLE_TERMS)
    content_grounded = contains_style_term(reason_blob, CONTENT_STYLE_SIGNAL_TERMS)
    mechanical_reason = contains_style_term(why_this_style, MECHANICAL_STYLE_REASON_TERMS)

    if chose_bright_default and not content_grounded:
        issues.append(
            "visual_style_decision.json chooses a bright/daylight style but why_this_style does not cite content, copy, evidence, reference, or audience reasons"
        )
    if chose_bright_default and mechanical_reason:
        issues.append(
            "visual_style_decision.json must not choose daylight_productivity/L4-L5 because it is the default, reused, or recently successful"
        )

    recent_same_style_count = decision.get("recent_same_style_count")
    try:
        repeated_style = int(recent_same_style_count) >= 2
    except Exception:
        repeated_style = False
    if repeated_style and not content_grounded:
        issues.append(
            "visual_style_decision.json repeats a recent visual style without a content-specific reason"
        )

    return issues


ENTERPRISE_CONSOLE_REQUIRED_PLAN_FIELDS = (
    "foreground_ui_system",
    "caption_system",
    "local_readability_treatment",
    "component_families",
    "motion_vocabulary",
    "transition_language",
    "sfx_character",
    "technology_restraint_policy",
)


def visual_style_plan_console_issues(plan: dict[str, Any]) -> list[str]:
    if not isinstance(plan, dict) or not plan:
        return []
    missing = [field for field in ENTERPRISE_CONSOLE_REQUIRED_PLAN_FIELDS if not plan.get(field)]
    if not missing:
        return []
    return [
        "visual_style_plan.json missing enterprise AI console fields: "
        + ", ".join(missing)
        + " (see references/enterprise_ai_control_console_visual_system.md)"
    ]


def is_local_summary_card(asset: dict[str, Any]) -> bool:
    text = normalized_text(
        " ".join(
            [
                str(asset.get("type", "")),
                str(asset.get("provider", "")),
                str(asset.get("source", "")),
                str(asset.get("source_note", "")),
                str(asset.get("qa_notes", "")),
            ]
        )
    )
    return contains_term(text, LOCAL_SUMMARY_CARD_TERMS) or "not an official screenshot" in text


def asset_manifest_real_evidence_issues(manifest: dict[str, Any]) -> list[str]:
    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        return ["asset_manifest.assets must be an array"]
    issues: list[str] = []
    for index, asset in enumerate(assets, start=1):
        if not isinstance(asset, dict):
            continue
        asset_id = str(asset.get("asset_id") or index)
        if (asset.get("is_evidence") is True or asset.get("asset_source_type") == "proof") and is_local_summary_card(asset):
            issues.append(
                f"{asset_id}: local summary/designed cards cannot be counted as proof; use real UI/doc/terminal proof or classify as support"
            )
    return issues


def is_background_plate(asset: dict[str, Any]) -> bool:
    text = normalized_text(
        " ".join(
            [
                str(asset.get("asset_role", "")),
                str(asset.get("role", "")),
                str(asset.get("type", "")),
                str(asset.get("source", "")),
                str(asset.get("source_note", "")),
                str(asset.get("qa_notes", "")),
            ]
        )
    )
    return "background_plate" in text or "background plate" in text or "背景" in text


def valid_background_plate_exists(manifest: dict[str, Any]) -> bool:
    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        return False
    for asset in assets:
        if not isinstance(asset, dict) or not is_background_plate(asset):
            continue
        local_support_allowed = (
            manifest.get("allow_local_support_background_plate") is True
            and asset.get("type") in {"designed_card", "other"}
            and asset.get("asset_source_type") == "support"
            and asset.get("is_evidence") is False
            and str(asset.get("resolution", "")).lower().replace(" ", "") == "1920x1080"
            and all(str(asset.get(key, "")).strip() for key in BACKGROUND_SEMANTIC_REQUIRED_FIELDS)
            and all(str(asset.get(key, "")).strip() for key in VISUAL_DIRECTOR_REQUIRED_FIELDS)
            and "user_approved" in normalized_text(
                " ".join(
                    [
                        str(manifest.get("local_support_background_policy", "")),
                        str(asset.get("generation_method", "")),
                        str(asset.get("source_note", "")),
                        str(asset.get("qa_notes", "")),
                    ]
                )
            )
        )
        if local_support_allowed:
            return True
        if (
            asset.get("type") == "generated_visual"
            and asset.get("asset_source_type") == "generated"
            and asset.get("is_evidence") is False
            and str(asset.get("resolution", "")).lower().replace(" ", "") == "1920x1080"
            and all(str(asset.get(key, "")).strip() for key in BACKGROUND_SEMANTIC_REQUIRED_FIELDS)
            and all(str(asset.get(key, "")).strip() for key in VISUAL_DIRECTOR_REQUIRED_FIELDS)
        ):
            return True
    return False


def manifest_requires_visual_tone_report(manifest: dict[str, Any]) -> bool:
    assets = manifest.get("assets", [])
    if not isinstance(assets, list):
        return False
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        asset_type = str(asset.get("type", ""))
        role = str(asset.get("asset_role", ""))
        if asset_type in TONE_CHECK_VISUAL_TYPES or role in TONE_CHECK_VISUAL_ROLES:
            return True
    return False


def background_prompt_pack_exists(internal: Path) -> bool:
    return any(exists(internal / name) for name in BACKGROUND_PROMPT_PACK_NAMES)


def sfx_policy_passes(quality_spec: dict[str, Any]) -> bool:
    policy = normalized_text(quality_spec.get("sfx_policy"))
    return bool(policy) and not contains_term(policy, NO_SFX_POLICY_TERMS)


def runtime_choice_passes(quality_spec: dict[str, Any]) -> bool:
    runtime = normalized_text(quality_spec.get("runtime_choice"))
    return bool(runtime) and "hyperframes" in runtime and not contains_term(runtime, WEAK_RUNTIME_TERMS)


def narration_continuity_passes(quality_spec: dict[str, Any]) -> bool:
    policy = normalized_text(quality_spec.get("narration_continuity_policy"))
    return bool(policy) and "continuous" in policy and ("transition" in policy or "root narration" in policy)


def quality_spec_passes(metadata: dict[str, Any]) -> bool:
    quality_spec = metadata.get("quality_spec")
    if not isinstance(quality_spec, dict):
        return False
    if str(quality_spec.get("target_quality_level", "")).strip() not in {"high_quality", "breakout_potential"}:
        return False
    if str(quality_spec.get("render_quality", "")).strip() not in {
        "hyperframes_high",
        "high_bitrate_h264",
        "hyperframes_high_plus_remux",
    }:
        return False
    if quality_spec.get("provider_policy") != "free_first_local_or_authorized_openai_only":
        return False
    try:
        if int(quality_spec.get("min_bitrate", 0)) < 3_500_000:
            return False
    except Exception:
        return False
    required = [
        "source_asset_policy",
        "sfx_policy",
        "cover_policy",
        "frame_review_policy",
        "runtime_choice",
        "caption_template_plan",
        "timeline_contract_ref",
        "narration_continuity_policy",
    ]
    return (
        all(str(quality_spec.get(key, "")).strip() for key in required)
        and sfx_policy_passes(quality_spec)
        and runtime_choice_passes(quality_spec)
        and narration_continuity_passes(quality_spec)
    )


def director_orchestrator_required(metadata: dict[str, Any]) -> bool:
    quality_spec = metadata.get("quality_spec") if isinstance(metadata.get("quality_spec"), dict) else {}
    if quality_spec.get("director_orchestrator_required") is False:
        return False
    return str(quality_spec.get("target_quality_level", "")).strip() in {"high_quality", "breakout_potential"}


def director_selection_issues(selection: dict[str, Any]) -> list[str]:
    if not isinstance(selection, dict):
        return ["director_selection.json must be a JSON object"]
    issues: list[str] = []
    for field in DIRECTOR_SELECTION_REQUIRED_FIELDS:
        if not selection.get(field):
            issues.append(f"director_selection.json missing required field: {field}")
    if selection.get("status") not in {"passed", "locked"}:
        issues.append("director_selection.json status must be passed or locked")

    scheme = selection.get("scheme") if isinstance(selection.get("scheme"), dict) else {}
    if not all(str(scheme.get(field, "")).strip() for field in ("id", "name", "format")):
        issues.append("director_selection.json scheme must include id, name, and format")

    policy = selection.get("reference_policy") if isinstance(selection.get("reference_policy"), dict) else {}
    cards = policy.get("selected_reference_cards", [])
    if not isinstance(cards, list) or not cards:
        issues.append("director_selection.json reference_policy.selected_reference_cards must not be empty")
    if policy.get("latest_reference_is_not_default") is not True:
        issues.append("director_selection.json must mark latest_reference_is_not_default=true")
    scope = normalized_style_text(policy.get("reference_scope"))
    if "learn" not in scope:
        issues.append("director_selection.json reference_scope must describe learning from references")
    forbidden_blob = normalized_style_text(policy.get("forbidden_copying"))
    for term in REFERENCE_FORBIDDEN_TERMS:
        if term not in forbidden_blob:
            issues.append(f"director_selection.json forbidden_copying must mention {term}")

    components = selection.get("component_mix", [])
    component_ids = [
        str(item.get("id", "")).strip()
        for item in components
        if isinstance(item, dict) and str(item.get("id", "")).strip()
    ]
    if len(set(component_ids)) < 4:
        issues.append("director_selection.json component_mix must contain at least four distinct components")
    if not selection.get("cooldown_policy"):
        issues.append("director_selection.json cooldown_policy must be documented")
    rejected = selection.get("why_not_other_schemes", [])
    if not isinstance(rejected, list) or len(rejected) < 2:
        issues.append("director_selection.json why_not_other_schemes must include at least two rejected alternatives")
    return issues


def style_recipe_issues(recipe: dict[str, Any]) -> list[str]:
    if not isinstance(recipe, dict):
        return ["style_recipe.json must be a JSON object"]
    issues: list[str] = []
    for field in STYLE_RECIPE_REQUIRED_FIELDS:
        if not recipe.get(field):
            issues.append(f"style_recipe.json missing required field: {field}")
    if recipe.get("status") not in {"passed", "locked"}:
        issues.append("style_recipe.json status must be passed or locked")
    component_ids = recipe.get("component_ids", [])
    if not isinstance(component_ids, list) or len(set(component_ids)) < 4:
        issues.append("style_recipe.json component_ids must include at least four distinct components")
    motion = recipe.get("motion_primitives", [])
    if not isinstance(motion, list) or len(set(motion)) < 3:
        issues.append("style_recipe.json motion_primitives must include at least three motion primitives")
    if not recipe.get("style_inheritance"):
        issues.append("style_recipe.json must document whole-video style inheritance")
    return issues


def fixed_template_selection_issues(selection: dict[str, Any]) -> list[str]:
    if not isinstance(selection, dict):
        return ["fixed_template_selection.json must be a JSON object"]
    issues: list[str] = []
    if selection.get("status") not in {"passed", "locked"}:
        issues.append("fixed_template_selection.json status must be passed or locked")
    for field in FIXED_TEMPLATE_REQUIRED_FIELDS:
        if not selection.get(field):
            issues.append(f"fixed_template_selection.json missing required field: {field}")

    for field in ("background_template", "transition_sfx_pack", "component_pack", "voice_mix_profile"):
        record = selection.get(field) if isinstance(selection.get(field), dict) else {}
        if not str(record.get("id") or "").strip():
            issues.append(f"fixed_template_selection.json {field}.id is required")
        if field == "background_template":
            asset_path = str(record.get("fixed_asset_path") or "").strip()
            if not asset_path:
                issues.append("fixed_template_selection.json background_template.fixed_asset_path is required")
            elif not Path(asset_path).exists():
                issues.append("fixed_template_selection.json background_template.fixed_asset_path must exist")
            if record.get("fixed_asset_exists") is not True:
                issues.append("fixed_template_selection.json background_template.fixed_asset_exists must be true")

    contract = selection.get("inheritance_contract") if isinstance(selection.get("inheritance_contract"), dict) else {}
    for flag in FIXED_TEMPLATE_REQUIRED_CONTRACT_FLAGS:
        if contract.get(flag) is not True:
            issues.append(f"fixed_template_selection.json inheritance_contract.{flag} must be true")
    return issues


def hook_score_report_issues(report: dict[str, Any]) -> list[str]:
    if not isinstance(report, dict):
        return ["hook_score_report.json must be a JSON object"]
    issues: list[str] = []
    if report.get("status") != "passed":
        issues.append("hook_score_report.json status must be passed")
    try:
        if int(report.get("variant_count", 0)) < 10:
            issues.append("hook_score_report.json variant_count must be >= 10")
    except Exception:
        issues.append("hook_score_report.json variant_count must be numeric")
    try:
        if float(report.get("top_score", 0)) < 8.5:
            issues.append("hook_score_report.json top_score must be >= 8.5")
    except Exception:
        issues.append("hook_score_report.json top_score must be numeric")
    selected = report.get("selected_hook") if isinstance(report.get("selected_hook"), dict) else {}
    if not str(selected.get("line", "") or selected.get("first_3_seconds_line", "")).strip():
        issues.append("hook_score_report.json selected_hook must include a line")
    issues.extend(report.get("blocking_issues", []))
    return issues


def reference_overfit_audit_issues(report: dict[str, Any]) -> list[str]:
    if not isinstance(report, dict):
        return ["reference_overfit_audit.json must be a JSON object"]
    issues: list[str] = []
    if report.get("status") != "passed":
        issues.append("reference_overfit_audit.json status must be passed")
    issues.extend(report.get("blocking_issues", []))
    return issues


def frame_review_passed(frame_report: dict[str, Any]) -> bool:
    return frame_report.get("status") == "passed"


def quality_level(scores: dict[str, float], evidence_ratio: float, gates: dict[str, bool]) -> str:
    if (
        scores["topic_score"] >= 9
        and scores.get("first_3_seconds_score", 0) >= 9.4
        and scores["first_5_seconds_score"] >= 9.3
        and scores["script_score"] >= 9
        and scores.get("semantic_score", 0) >= 9
        and scores.get("beginner_value_score", 0) >= 9
        and scores.get("save_value_score", 0) >= 9
        and scores.get("proof_score", 0) >= 9
        and scores.get("visual_score", 0) >= 9
        and scores.get("aesthetic_score", 0) >= 9
        and scores.get("sync_score", 0) >= 9.3
        and scores["compliance_score"] >= 9.7
        and evidence_ratio >= 0.7
        and all(gates.values())
    ):
        return "breakout_potential"
    if (
        scores["topic_score"] >= 8.5
        and scores.get("first_3_seconds_score", 0) >= 9.2
        and scores["first_5_seconds_score"] >= 9
        and scores["script_score"] >= 8.5
        and scores.get("semantic_score", 0) >= 8.5
        and scores.get("beginner_value_score", 0) >= 8.8
        and scores.get("save_value_score", 0) >= 8.5
        and scores.get("proof_score", 0) >= 8.5
        and scores.get("visual_score", 0) >= 8
        and scores.get("aesthetic_score", 0) >= 8.2
        and scores.get("sync_score", 0) >= 9
        and scores["compliance_score"] >= 9.5
        and evidence_ratio >= 0.6
        and all(gates.values())
    ):
        return "high_quality"
    return "publishable"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run final QA for an output project.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic>")
    parser.add_argument("--out", required=True, help="qa_report.json path")
    args = parser.parse_args()

    project = Path(args.project)
    internal = project / "internal"
    issues: list[str] = []
    warnings: list[str] = []
    gates: dict[str, bool] = {}
    metadata: dict[str, Any] = {}

    paths = {
        "topic_candidates": internal / "topic_candidates.json",
        "topic_candidates_scored": internal / "topic_candidates.scored.json",
        "selected_topic": internal / "selected_topic.json",
        "director_selection": internal / "director_selection.json",
        "style_recipe": internal / "style_recipe.json",
        "fixed_template_selection": internal / "fixed_template_selection.json",
        "hook_variants": internal / "hook_variants.json",
        "hook_score_report": internal / "hook_score_report.json",
        "reference_overfit_audit": internal / "reference_overfit_audit.json",
        "copy_package": internal / "copy_package.md",
        "copy_package_json": internal / "copy_package.json",
        "semantic_review": internal / "semantic_review.json",
        "beginner_value_review": internal / "beginner_value_review.json",
        "compliance": internal / "compliance_report.json",
        "visual_style_decision": internal / "visual_style_decision.json",
        "visual_style_plan": internal / "visual_style_plan.json",
        "storyboard": internal / "storyboard.json",
        "audio_locked": internal / "storyboard.audio_locked.json",
        "asset_manifest": internal / "asset_manifest.json",
        "asset_validation": internal / "asset_validation.json",
        "asset_prompt_validation": internal / "asset_prompt_validation.json",
        "visual_tone": internal / "visual_tone_report.json",
        "metadata": internal / "metadata.json",
        "audio_continuity": internal / "audio_continuity_report.json",
        "visual_review": internal / "visual_review.json",
        "render_text_manifest": internal / "render_text_manifest.json",
        "screen_text_proofread": internal / "screen_text_proofread_report.json",
        "empty_frame": internal / "empty_frame_report.json",
        "draft_video": first_existing(internal / "draft.mp4", project / "draft.mp4"),
        "cover": first_existing(internal / "cover.png", project / "cover.png"),
        "publish_copy": first_existing(internal / "publish_copy.txt", project / "publish_copy.txt"),
    }

    bool_gate(gates, "internal_dir_exists", dir_exists(internal), issues, "missing internal directory")
    bool_gate(gates, "topic_candidates_exists", exists(paths["topic_candidates"]), issues, "missing topic_candidates.json")
    bool_gate(gates, "selected_topic_exists", exists(paths["selected_topic"]), issues, "missing selected_topic.json")
    bool_gate(gates, "copy_package_exists", exists(paths["copy_package"]), issues, "missing copy_package.md")
    bool_gate(gates, "copy_package_json_exists", exists(paths["copy_package_json"]), issues, "missing copy_package.json")
    bool_gate(gates, "storyboard_exists", exists(paths["storyboard"]), issues, "missing storyboard.json")
    bool_gate(gates, "audio_locked", exists(paths["audio_locked"]), issues, "missing storyboard.audio_locked.json")
    bool_gate(gates, "asset_manifest_exists", exists(paths["asset_manifest"]), issues, "missing asset_manifest.json")
    bool_gate(gates, "metadata_exists", exists(paths["metadata"]), issues, "missing metadata.json")
    bool_gate(gates, "draft_video_exists", exists(paths["draft_video"]), issues, "missing draft.mp4")
    bool_gate(gates, "audio_continuity_report_exists", exists(paths["audio_continuity"]), issues, "missing audio_continuity_report.json")
    bool_gate(gates, "render_text_manifest_exists", exists(paths["render_text_manifest"]), issues, "missing render_text_manifest.json")
    bool_gate(gates, "cover_source_exists", exists(paths["cover"]), issues, "missing cover.png")
    bool_gate(gates, "publish_copy_source_exists", exists(paths["publish_copy"]), issues, "missing publish_copy.txt")

    if exists(paths["metadata"]):
        metadata = load_json(paths["metadata"])
        quality_spec = metadata.get("quality_spec") if isinstance(metadata.get("quality_spec"), dict) else {}
        bool_gate(
            gates,
            "normal_tts_speed",
            normal_tts_speed(metadata),
            issues,
            "metadata.tts_speed must be 0.95-1.03 by default, or <=1.10 only with explicit user approval documented",
        )
        bool_gate(
            gates,
            "quality_spec_documented",
            quality_spec_passes(metadata),
            issues,
            "metadata.quality_spec must document high-quality render, bitrate, provider, runtime, source asset, caption template, SFX, cover, and frame review policies",
        )
        bool_gate(
            gates,
            "approved_natural_voice",
            voice_provider_passes(metadata),
            issues,
            "publish-ready videos need a documented approved natural voice sample; macOS say/scratch preview voices are not allowed",
        )
        bool_gate(
            gates,
            "subtle_sfx_required",
            sfx_policy_passes(quality_spec),
            issues,
            "publish-ready videos need subtle SFX; no-added-SFX policies are not allowed",
        )
        bool_gate(
            gates,
            "hyperframes_runtime_required",
            runtime_choice_passes(quality_spec),
            issues,
            "premium videos must use a HyperFrames final timeline; FFmpeg-only portrait card pipelines are not allowed",
        )
    else:
        bool_gate(gates, "normal_tts_speed", False, issues, "missing metadata.json for tts speed check")
        bool_gate(gates, "quality_spec_documented", False, issues, "missing metadata.json for quality_spec check")
        bool_gate(gates, "approved_natural_voice", False, issues, "missing metadata.json for voice provider check")
        bool_gate(gates, "subtle_sfx_required", False, issues, "missing metadata.json for SFX policy check")
        bool_gate(gates, "hyperframes_runtime_required", False, issues, "missing metadata.json for runtime check")

    if director_orchestrator_required(metadata):
        bool_gate(
            gates,
            "director_selection_exists",
            exists(paths["director_selection"]),
            issues,
            "missing director_selection.json before copy/storyboard/render",
        )
        bool_gate(
            gates,
            "style_recipe_exists",
            exists(paths["style_recipe"]),
            issues,
            "missing style_recipe.json before visual production",
        )
        bool_gate(
            gates,
            "hook_variants_exists",
            exists(paths["hook_variants"]),
            issues,
            "missing hook_variants.json before full copywriting",
        )
        bool_gate(
            gates,
            "hook_score_report_exists",
            exists(paths["hook_score_report"]),
            issues,
            "missing hook_score_report.json before full copywriting",
        )
        bool_gate(
            gates,
            "reference_overfit_audit_exists",
            exists(paths["reference_overfit_audit"]),
            issues,
            "missing reference_overfit_audit.json before storyboard/render",
        )
        bool_gate(
            gates,
            "fixed_template_selection_exists",
            exists(paths["fixed_template_selection"]),
            issues,
            "missing fixed_template_selection.json before visual production",
        )

        if exists(paths["director_selection"]):
            selection_issues = director_selection_issues(load_json(paths["director_selection"]))
            bool_gate(
                gates,
                "director_selection_passed",
                not selection_issues,
                issues,
                "director_selection.json did not pass",
            )
            issues.extend(selection_issues)
        else:
            bool_gate(gates, "director_selection_passed", False, issues, "missing director_selection.json")

        if exists(paths["style_recipe"]):
            recipe_issues = style_recipe_issues(load_json(paths["style_recipe"]))
            bool_gate(
                gates,
                "style_recipe_passed",
                not recipe_issues,
                issues,
                "style_recipe.json did not pass",
            )
            issues.extend(recipe_issues)
        else:
            bool_gate(gates, "style_recipe_passed", False, issues, "missing style_recipe.json")

        if exists(paths["fixed_template_selection"]):
            fixed_issues = fixed_template_selection_issues(load_json(paths["fixed_template_selection"]))
            bool_gate(
                gates,
                "fixed_template_selection_passed",
                not fixed_issues,
                issues,
                "fixed_template_selection.json did not pass",
            )
            issues.extend(fixed_issues)
        else:
            bool_gate(gates, "fixed_template_selection_passed", False, issues, "missing fixed_template_selection.json")

        if exists(paths["hook_score_report"]):
            hook_issues = hook_score_report_issues(load_json(paths["hook_score_report"]))
            bool_gate(
                gates,
                "hook_score_report_passed",
                not hook_issues,
                issues,
                "hook_score_report.json did not pass",
            )
            issues.extend(hook_issues)
        else:
            bool_gate(gates, "hook_score_report_passed", False, issues, "missing hook_score_report.json")

        if exists(paths["reference_overfit_audit"]):
            overfit_issues = reference_overfit_audit_issues(load_json(paths["reference_overfit_audit"]))
            bool_gate(
                gates,
                "reference_overfit_audit_passed",
                not overfit_issues,
                issues,
                "reference_overfit_audit.json did not pass",
            )
            issues.extend(overfit_issues)
        else:
            bool_gate(gates, "reference_overfit_audit_passed", False, issues, "missing reference_overfit_audit.json")

    compliance_score = 0.0
    if exists(paths["compliance"]):
        compliance = load_json(paths["compliance"])
        compliance_passed = compliance.get("status") == "passed" and compliance.get("summary", {}).get("error_count", 1) == 0
        compliance_score = 9.5 if compliance_passed else 0.0
        bool_gate(gates, "compliance_passed", compliance_passed, issues, "compliance_report.json is not passed")
        if compliance.get("summary", {}).get("warning_count", 0):
            warnings.append("compliance report has warnings; verify documented acceptance")
    else:
        bool_gate(gates, "compliance_passed", False, issues, "missing compliance_report.json")

    evidence_ratio = 0.0
    script_score = 0.0
    first_3 = 0.0
    first_5 = 0.0
    save_value_score = 0.0
    proof_score = 0.0
    visual_score = 0.0
    semantic_score = 0.0
    beginner_value_score = 0.0
    aesthetic_score = 0.0
    sync_score = 0.0
    topic_score = 0.0

    topic_source = paths["topic_candidates_scored"] if exists(paths["topic_candidates_scored"]) else paths["topic_candidates"]
    if exists(topic_source):
        topic_data = load_json(topic_source)
        candidates = topic_data.get("candidates", [])
        topic_score = max([get_score(item.get("scores", {}), "total_score") for item in candidates] or [0.0])
        if topic_score < 8:
            issues.append("topic_score must be >= 8")

    score_path = internal / "script_score.json"
    if exists(score_path):
        bool_gate(gates, "script_score_exists", True, issues, "missing script_score.json")
        script_data = load_json(score_path)
        script_score = get_score(script_data, "script_score")
        first_3 = get_score(script_data, "first_3_seconds_score")
        first_5 = get_score(script_data, "first_5_seconds_score")
        save_value_score = get_score(script_data, "save_value_score")
        proof_score = get_score(script_data, "proof_score")
        compliance_score = max(compliance_score, get_score(script_data, "compliance_score"))
        empty_talk_ratio = get_score(script_data, "empty_talk_ratio", "empty_phrase_density")
        if first_3 < 9.2:
            issues.append("first_3_seconds_score must be >= 9.2")
        if first_5 < 9:
            issues.append("first_5_seconds_score must be >= 9")
        if script_score < 8.5:
            issues.append("script_score must be >= 8.5")
        if save_value_score < 8.5:
            issues.append("save_value_score must be >= 8.5")
        if proof_score < 8.5:
            issues.append("proof_score must be >= 8.5")
        if compliance_score < 9.5:
            issues.append("compliance_score must be >= 9.5")
        if empty_talk_ratio > 0.18:
            issues.append("empty_talk_ratio must be <= 0.18")
    else:
        bool_gate(gates, "script_score_exists", False, issues, "missing script_score.json")

    if exists(paths["semantic_review"]):
        semantic = load_json(paths["semantic_review"])
        semantic_score = get_score(semantic, "composite_score")
        bool_gate(
            gates,
            "semantic_review_passed",
            semantic.get("status") == "passed",
            issues,
            "semantic_review.json is not passed",
        )
        if semantic_score < 8.5:
            issues.append("semantic_review.composite_score must be >= 8.5")
        issues.extend(semantic.get("hard_fail_reasons", []))
        warnings.extend(semantic.get("revision_suggestions", []))
    else:
        bool_gate(gates, "semantic_review_exists", False, issues, "missing semantic_review.json")

    if exists(paths["beginner_value_review"]):
        beginner_review = load_json(paths["beginner_value_review"])
        beginner_value_score = get_score(beginner_review, "total_score")
        bool_gate(
            gates,
            "beginner_value_review_passed",
            beginner_review.get("status") == "passed",
            issues,
            "beginner_value_review.json is not passed",
        )
        if beginner_value_score < 8.8:
            issues.append("beginner_value_review.total_score must be >= 8.8")
        beginner_scores = beginner_review.get("scores", {}) if isinstance(beginner_review.get("scores"), dict) else {}
        if get_score(beginner_scores, "title_clarity") < 9.0:
            issues.append("beginner title_clarity must be >= 9.0")
        if get_score(beginner_scores, "first_5_seconds_pull") < 9.0:
            issues.append("beginner first_5_seconds_pull must be >= 9.0")
        if get_score(beginner_scores, "visible_result") < 8.5:
            issues.append("beginner visible_result must be >= 8.5")
        if get_score(beginner_scores, "step_by_step_value") < 8.5:
            issues.append("beginner step_by_step_value must be >= 8.5")
        if get_score(beginner_scores, "problem_example_score") < 8.5:
            issues.append("beginner problem_example_score must be >= 8.5")
        issues.extend(beginner_review.get("rewrite_required", []))
    else:
        bool_gate(gates, "beginner_value_review_exists", False, issues, "missing beginner_value_review.json")

    if exists(paths["asset_validation"]):
        asset_report = load_json(paths["asset_validation"])
        bool_gate(
            gates,
            "asset_validation_passed",
            asset_report.get("status") == "passed",
            issues,
            "asset_validation.json is not passed",
        )
        issues.extend(asset_report.get("blocking_issues", []))
        warnings.extend(asset_report.get("warnings", []))
    else:
        bool_gate(gates, "asset_validation_exists", False, issues, "missing asset_validation.json")

    if background_prompt_pack_exists(internal):
        bool_gate(
            gates,
            "asset_prompt_validation_exists",
            exists(paths["asset_prompt_validation"]),
            issues,
            "missing asset_prompt_validation.json after visual prompt pack",
        )
        if exists(paths["asset_prompt_validation"]):
            prompt_report = load_json(paths["asset_prompt_validation"])
            bool_gate(
                gates,
                "asset_prompt_validation_passed",
                prompt_report.get("status") == "passed",
                issues,
                "asset_prompt_validation.json is not passed",
            )
            issues.extend(prompt_report.get("blocking_issues", []))
            warnings.extend(prompt_report.get("warnings", []))
        else:
            bool_gate(
                gates,
                "asset_prompt_validation_passed",
                False,
                issues,
                "missing asset_prompt_validation.json after visual prompt pack",
            )
    else:
        bool_gate(
            gates,
            "asset_prompt_validation_exists",
            False,
            issues,
            "missing visual prompt pack before asset prompt validation",
        )
        bool_gate(
            gates,
            "asset_prompt_validation_passed",
            False,
            issues,
            "missing visual prompt pack before asset prompt validation",
        )

    if exists(paths["asset_manifest"]):
        asset_manifest = load_json(paths["asset_manifest"])
        visual_tone_required = manifest_requires_visual_tone_report(asset_manifest)
        manifest_evidence_issues = asset_manifest_real_evidence_issues(asset_manifest)
        bool_gate(
            gates,
            "asset_manifest_real_evidence",
            not manifest_evidence_issues,
            issues,
            "asset_manifest contains local summary/designed cards counted as proof",
        )
        issues.extend(manifest_evidence_issues)
        bool_gate(
            gates,
            "background_prompt_pack_exists",
            background_prompt_pack_exists(internal),
            issues,
            "missing background_prompt_pack.md before AI video production",
        )
        bool_gate(
            gates,
            "generated_background_plate_registered",
            valid_background_plate_exists(asset_manifest),
            issues,
            "asset_manifest must register at least one generated 1920x1080 background_plate as support, not proof",
        )
        bool_gate(
            gates,
            "visual_style_decision_exists",
            not visual_tone_required or exists(paths["visual_style_decision"]),
            issues,
            "missing visual_style_decision.json before visual_style_plan.json",
        )
        bool_gate(
            gates,
            "visual_style_plan_exists",
            not visual_tone_required or exists(paths["visual_style_plan"]),
            issues,
            "missing visual_style_plan.json before generated/support visual production",
        )
        if visual_tone_required and exists(paths["visual_style_decision"]):
            visual_style_decision = load_json(paths["visual_style_decision"])
            visual_style_plan = load_json(paths["visual_style_plan"]) if exists(paths["visual_style_plan"]) else {}
            style_decision_issues = visual_style_decision_issues(visual_style_decision, visual_style_plan)
            style_plan_console_issues = visual_style_plan_console_issues(visual_style_plan)
            bool_gate(
                gates,
                "enterprise_console_visual_system_documented",
                not style_plan_console_issues,
                issues,
                "visual_style_plan.json missing enterprise AI console visual system documentation",
            )
            bool_gate(
                gates,
                "visual_style_decision_passed",
                not style_decision_issues,
                issues,
                "visual_style_decision.json is not passed",
            )
            issues.extend(style_plan_console_issues)
            issues.extend(style_decision_issues)
        else:
            bool_gate(
                gates,
                "visual_style_decision_passed",
                not visual_tone_required,
                issues,
                "missing visual_style_decision.json before visual_style_plan.json",
            )
        bool_gate(
            gates,
            "visual_tone_report_exists",
            not visual_tone_required or exists(paths["visual_tone"]),
            issues,
            "missing visual_tone_report.json after generated/support visuals",
        )
        if visual_tone_required and exists(paths["visual_tone"]):
            visual_tone_report = load_json(paths["visual_tone"])
            bool_gate(
                gates,
                "visual_tone_report_passed",
                visual_tone_report.get("status") == "passed",
                issues,
                "visual_tone_report.json is not passed",
            )
            issues.extend(visual_tone_report.get("blocking_issues", []))
        else:
            bool_gate(
                gates,
                "visual_tone_report_passed",
                not visual_tone_required,
                issues,
                "missing visual_tone_report.json after generated/support visuals",
            )
    else:
        bool_gate(gates, "asset_manifest_real_evidence", False, issues, "missing asset_manifest.json")
        bool_gate(gates, "background_prompt_pack_exists", False, issues, "missing background_prompt_pack.md before AI video production")
        bool_gate(gates, "generated_background_plate_registered", False, issues, "missing asset_manifest.json")
        bool_gate(gates, "visual_style_decision_exists", False, issues, "missing asset_manifest.json")
        bool_gate(gates, "visual_style_decision_passed", False, issues, "missing asset_manifest.json")
        bool_gate(gates, "visual_style_plan_exists", False, issues, "missing asset_manifest.json")
        bool_gate(gates, "visual_tone_report_exists", False, issues, "missing asset_manifest.json")
        bool_gate(gates, "visual_tone_report_passed", False, issues, "missing asset_manifest.json")

    storyboard_report_path = internal / "storyboard_validation.json"
    if exists(storyboard_report_path):
        bool_gate(gates, "storyboard_validation_exists", True, issues, "missing storyboard_validation.json")
        story_report = load_json(storyboard_report_path)
        bool_gate(
            gates,
            "storyboard_validation_passed",
            story_report.get("status") == "passed",
            issues,
            "storyboard_validation.json is not passed",
        )
        evidence_ratio = float(story_report.get("evidence_runtime_ratio", 0))
        visual_score = 8.5 if story_report.get("status") == "passed" else 0.0
        sync_score = 9.0 if story_report.get("status") == "passed" else 0.0
        story_signals = story_report.get("signals", {}) if isinstance(story_report.get("signals"), dict) else {}
        bool_gate(
            gates,
            "storyboard_quality_spec_valid",
            story_signals.get("quality_spec_valid") is True,
            issues,
            "storyboard quality_spec must be complete and high_quality/breakout_potential",
        )
        bool_gate(
            gates,
            "free_first_provider_policy",
            story_signals.get("provider_policy_valid") is True,
            issues,
            "storyboard target.provider_policy must use free_first_local_or_authorized_openai_only",
        )
        scene_count = int(story_report.get("scene_count") or story_signals.get("scene_count") or 0)
        bool_gate(
            gates,
            "storyboard_layered_scene_design",
            scene_count > 0 and story_signals.get("layered_scene_count") == scene_count,
            issues,
            "every storyboard scene must include at least 3 visual.design_layers",
        )
        bool_gate(
            gates,
            "storyboard_scene_quality_checks_passed",
            scene_count > 0 and story_signals.get("quality_check_scene_count") == scene_count,
            issues,
            "every storyboard scene visual.quality_checks must pass source/text/template/static checks",
        )
        bool_gate(
            gates,
            "storyboard_asset_source_classified",
            scene_count > 0 and story_signals.get("source_class_scene_count") == scene_count,
            issues,
            "every storyboard scene must classify visual.asset_source_type",
        )
        bool_gate(
            gates,
            "storyboard_caption_templates_documented",
            scene_count > 0 and story_signals.get("caption_template_scene_count") == scene_count and story_signals.get("caption_template_count", 0) >= 2,
            issues,
            "storyboard must document at least 2 caption templates across scenes",
        )
        bool_gate(
            gates,
            "storyboard_premium_motion_documented",
            scene_count > 0 and story_signals.get("premium_motion_scene_count") == scene_count,
            issues,
            "every storyboard scene must document premium HyperFrames motion craft",
        )
        bool_gate(
            gates,
            "storyboard_audio_continuity_documented",
            scene_count > 0 and story_signals.get("audio_continuity_scene_count") == scene_count,
            issues,
            "every storyboard scene must document continuous narration through visual transitions",
        )
        bool_gate(
            gates,
            "storyboard_forbidden_providers_absent",
            story_signals.get("forbidden_provider_scene_count", 0) == 0,
            issues,
            "storyboard references a disabled paid/scraping provider",
        )
        if story_signals.get("production_stack_required"):
            bool_gate(
                gates,
                "production_stack_documented",
                story_signals.get("production_stack_valid") is True,
                issues,
                "production_stack must document the tool roles and proof chains for this tutorial",
            )
        if story_signals.get("codex_plugin_plan_required"):
            bool_gate(
                gates,
                "codex_plugin_plan_documented",
                story_signals.get("codex_plugin_plan_valid") is True,
                issues,
                "codex_plugin_plan must document plugin availability, boundaries, fallbacks, and evidence requirements",
            )
        if story_report.get("status") != "passed":
            issues.extend(story_report.get("issues", []))
    else:
        bool_gate(gates, "storyboard_validation_exists", False, issues, "missing storyboard_validation.json")

    technical_qa_path = internal / "video_technical_qa.json"
    if exists(paths["audio_continuity"]):
        audio_report = load_json(paths["audio_continuity"])
        bool_gate(
            gates,
            "audio_continuity_passed",
            audio_report.get("status") == "passed",
            issues,
            "audio_continuity_report.json is not passed",
        )
        issues.extend(audio_report.get("blocking_issues", []))
        warnings.extend(audio_report.get("warnings", []))
    else:
        bool_gate(gates, "audio_continuity_passed", False, issues, "missing audio_continuity_report.json")

    technical_qa_path = internal / "video_technical_qa.json"
    if exists(technical_qa_path):
        technical_report = load_json(technical_qa_path)
        bool_gate(
            gates,
            "video_technical_qa_passed",
            technical_report.get("status") == "passed",
            issues,
            "video_technical_qa.json is not passed",
        )
        bool_gate(
            gates,
            "metadata_consistency_checked",
            technical_report.get("metadata_consistency", {}).get("checked") is True,
            issues,
            "video_technical_qa.json must include metadata consistency check",
        )
        issues.extend(technical_report.get("blocking_issues", []))
        warnings.extend(technical_report.get("warnings", []))
    else:
        bool_gate(gates, "video_technical_qa_exists", False, issues, "missing video_technical_qa.json")

    frame_review_path = internal / "frame_review_report.json"
    if exists(frame_review_path):
        frame_report = load_json(frame_review_path)
        bool_gate(
            gates,
            "frame_review_exists",
            frame_report.get("status") in {"passed", "review_required", "failed"},
            issues,
            "frame_review_report.json is invalid",
        )
        bool_gate(
            gates,
            "frame_review_passed",
            frame_review_passed(frame_report),
            issues,
            "frame_review_report.json must be status=passed; review_required cannot be promoted by manual notes alone",
        )
        warnings.extend(frame_report.get("warnings", []))
    else:
        bool_gate(gates, "frame_review_exists", False, issues, "missing frame_review_report.json")
        bool_gate(gates, "frame_review_passed", False, issues, "missing frame_review_report.json")

    if exists(paths["screen_text_proofread"]):
        screen_text_report = load_json(paths["screen_text_proofread"])
        bool_gate(
            gates,
            "screen_text_proofread_passed",
            screen_text_report.get("status") == "passed",
            issues,
            "screen_text_proofread_report.json is not passed",
        )
        issues.extend(screen_text_report.get("blocking_issues", []))
        warnings.extend(screen_text_report.get("warnings", []))
    else:
        bool_gate(gates, "screen_text_proofread_exists", False, issues, "missing screen_text_proofread_report.json")

    if exists(paths["empty_frame"]):
        empty_frame_report = load_json(paths["empty_frame"])
        bool_gate(
            gates,
            "empty_frame_check_passed",
            empty_frame_report.get("status") == "passed",
            issues,
            "empty_frame_report.json is not passed",
        )
        issues.extend(empty_frame_report.get("blocking_issues", []))
        warnings.extend(empty_frame_report.get("warnings", []))
    else:
        bool_gate(gates, "empty_frame_check_exists", False, issues, "missing empty_frame_report.json")

    if exists(paths["visual_review"]):
        visual_report = load_json(paths["visual_review"])
        aesthetic_score = get_score(visual_report, "overall_visual_score")
        visual_score = max(visual_score, aesthetic_score)
        bool_gate(
            gates,
            "visual_review_passed",
            visual_report.get("status") == "passed",
            issues,
            "visual_review.json is not passed",
        )
        if aesthetic_score < 8.2:
            issues.append("visual_review.overall_visual_score must be >= 8.2")
        visual_scores = visual_report.get("scores", {})
        if get_score(visual_scores, "first_5s_score") < 8.5:
            issues.append("visual first_5s_score must be >= 8.5")
        if get_score(visual_scores, "readability_score") < 8:
            issues.append("visual readability_score must be >= 8")
        if get_score(visual_scores, "composition_score") < 8:
            issues.append("visual composition_score must be >= 8")
        if get_score(visual_scores, "layering_score") < 8.5:
            issues.append("visual layering_score must be >= 8.5")
        if get_score(visual_scores, "quality_check_score") < 8.5:
            issues.append("visual quality_check_score must be >= 8.5")
        if get_score(visual_scores, "caption_variety_score") < 8.5:
            issues.append("visual caption_variety_score must be >= 8.5")
        if get_score(visual_scores, "source_class_score") < 8.5:
            issues.append("visual source_class_score must be >= 8.5")
        if get_score(visual_scores, "sound_design_score") < 8.5:
            issues.append("visual sound_design_score must be >= 8.5")
        if get_score(visual_scores, "export_readiness_score") < 8.5:
            issues.append("visual export_readiness_score must be >= 8.5")
        visual_signals = visual_report.get("signals", {}) if isinstance(visual_report.get("signals"), dict) else {}
        visual_scene_count = int(visual_signals.get("scene_count") or 0)
        bool_gate(
            gates,
            "layered_scene_design",
            visual_scene_count > 0 and visual_signals.get("layered_scene_count") == visual_scene_count,
            issues,
            "visual_review must confirm every scene has layered design",
        )
        bool_gate(
            gates,
            "scene_quality_checks_passed",
            visual_scene_count > 0 and visual_signals.get("quality_check_scene_count") == visual_scene_count,
            issues,
            "visual_review must confirm every scene quality check passed",
        )
        bool_gate(
            gates,
            "visual_asset_source_classified",
            visual_scene_count > 0 and visual_signals.get("source_class_scene_count") == visual_scene_count,
            issues,
            "visual_review must confirm every scene source class is documented",
        )
        bool_gate(
            gates,
            "visual_caption_template_variety",
            visual_scene_count > 0
            and visual_signals.get("caption_template_scene_count") == visual_scene_count
            and visual_signals.get("caption_template_count", 0) >= 2,
            issues,
            "visual_review must confirm caption template diversity",
        )
        bool_gate(
            gates,
            "high_quality_render_policy",
            visual_signals.get("metadata_quality_spec_valid") is True,
            issues,
            "visual_review must confirm metadata high-quality render policy",
        )
        bool_gate(
            gates,
            "visual_voice_provider_approved",
            visual_signals.get("voice_provider_approved") is True or voice_provider_passes(metadata),
            issues,
            "visual_review must confirm approved natural voice provider",
        )
        bool_gate(
            gates,
            "visual_sfx_policy_valid",
            visual_signals.get("sfx_policy_valid") is True,
            issues,
            "visual_review must confirm subtle SFX policy",
        )
        bool_gate(
            gates,
            "visual_runtime_choice_valid",
            visual_signals.get("runtime_choice_valid") is True,
            issues,
            "visual_review must confirm HyperFrames final timeline runtime",
        )
        issues.extend(visual_report.get("blocking_issues", []))
        warnings.extend(visual_report.get("warnings", []))
    else:
        bool_gate(gates, "visual_review_exists", False, issues, "missing visual_review.json")

    bool_gate(gates, "not_static_image_only", evidence_ratio >= 0.5, issues, "evidence_runtime_ratio must be >= 0.5")
    bool_gate(gates, "audio_video_synced", exists(paths["audio_locked"]), issues, "audio lock is required for sync")

    status = "passed" if not issues and all(gates.values()) else "failed"
    issues = unique_preserve_order(issues)
    warnings = unique_preserve_order(warnings)
    score_values = {
        "topic_score": round(topic_score, 2),
        "first_3_seconds_score": round(first_3, 2),
        "first_5_seconds_score": round(first_5, 2),
        "script_score": round(script_score, 2),
        "semantic_score": round(semantic_score, 2),
        "beginner_value_score": round(beginner_value_score, 2),
        "save_value_score": round(save_value_score, 2),
        "proof_score": round(proof_score, 2),
        "visual_score": round(visual_score, 2),
        "aesthetic_score": round(aesthetic_score, 2),
        "sync_score": round(sync_score, 2),
        "compliance_score": round(compliance_score, 2),
    }

    report = {
        "status": status,
        "quality_level": quality_level(score_values, evidence_ratio, gates),
        "scores": score_values,
        "hard_gates": gates,
        "evidence_runtime_ratio": round(evidence_ratio, 3),
        "blocking_issues": issues,
        "warnings": warnings,
        "revision_required": status != "passed",
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
