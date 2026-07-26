#!/usr/bin/env python3
"""Validate the small shared artifact contract for a Douyin video project."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FORMAT_TYPES = {"tool_explainer", "news_explainer", "list_video"}
TOPIC_SELECTION_MODES = {"user_fixed", "research_selected"}
INTERACTION_MODES = {"step_by_step", "autonomous"}
TOPIC_CONFIRMATION_STATUSES = {"user_confirmed", "not_requested"}
TAXONOMY_BY_FORMAT = {
    "tool_explainer": {
        "level_1": "AI类视频",
        "level_2": "AI工具实操讲解类",
        "category_code": "ai_tool_explainer",
        "project_name_prefix": "AI工具实操讲解-",
    },
    "news_explainer": {
        "level_1": "AI类视频",
        "level_2": "AI新闻与产品更新解读类",
        "category_code": "ai_news_explainer",
        "project_name_prefix": "AI新闻解读-",
    },
    "list_video": {
        "level_1": "AI类视频",
        "level_2": "AI榜单、推荐与对比类",
        "category_code": "ai_list_video",
        "project_name_prefix": "AI榜单对比-",
    },
}
CORE_ARTIFACTS = (
    "source_brief.json",
    "script.json",
    "storyboard.json",
    "asset_manifest.json",
    "qa_report.json",
    "publish_package.json",
)
TYPE_FIELDS = {
    "tool_explainer": (
        "viewer_task",
        "input_method",
        "execution_process",
        "visible_result",
        "before_after",
        "safety_constraints",
        "privacy_redactions",
        "result_acceptance",
        "risk_review",
    ),
    "news_explainer": (
        "event",
        "event_status",
        "what_changed",
        "affected_audience",
        "next_step",
    ),
    "list_video": (
        "list_type",
        "selection_scope",
        "ranking_basis",
        "comparison_dimensions",
        "items",
    ),
}
NEWS_STATUSES = {"released", "announced", "preview", "rolling_out", "reported"}
NEWS_CLAIM_KINDS = {
    "event",
    "report_existence",
    "reported_fact",
    "absence_check",
    "analysis",
    "advice",
}
LIST_TYPES = {"recommendation_list", "comparison_list", "ranked_list", "hot_rank"}
RISK_LEVELS = {"low", "medium", "high"}
DEMO_ENVIRONMENTS = {
    "sanitized_local",
    "test_sandbox",
    "simulated_data",
    "pre_recorded_redacted",
    "real_environment",
}
REAL_ACTION_POLICIES = {"not_applicable", "read_only", "blocked"}
HIGH_RISK_DOMAINS = {
    "credentials",
    "otp",
    "financial_account",
    "financial_transaction",
    "government_id",
    "medical_private",
    "legal_privileged",
    "api_key",
    "secrets",
}
HIGH_RISK_DEMO_ENVIRONMENTS = {
    "test_sandbox",
    "simulated_data",
    "pre_recorded_redacted",
}
HIGH_RISK_KEYWORDS = {
    "credentials": ("密码", "password", "passcode", "登录凭据"),
    "otp": ("otp", "验证码", "短信码", "一次性密码"),
    "financial_account": ("网银", "银行账户", "银行卡", "bank account", "banking"),
    "financial_transaction": ("转账", "汇款", "真实交易", "wire transfer", "bank transfer"),
    "government_id": ("身份证", "护照", "驾驶证", "government id", "passport"),
    "medical_private": ("病历", "诊断记录", "医疗隐私", "medical record"),
    "legal_privileged": ("律师保密", "法律保密", "privileged legal"),
    "api_key": ("api key", "api_key", "密钥"),
    "secrets": ("助记词", "私钥", "secret token", "private key", "seed phrase"),
}
CREATIVE_DIRECTION_FIELDS = (
    "visual_thesis",
    "reason_for_topic",
    "evidence_strategy",
    "motion_logic",
    "continuity_devices",
    "rejected_defaults",
)
SCENE_DIRECTOR_FIELDS = (
    "visual_mode",
    "evidence_display",
    "motion_intent",
    "change_reason",
)
ALLOWED_SUBRENDERERS = {"hyperframes"}
VAGUE_VISUAL_TERMS = {"高级", "科技", "炫酷", "premium", "futuristic", "cool"}
INTERNAL_PUBLIC_TERMS = {
    "proof_id",
    "claim_id",
    "source_brief",
    "asset_manifest",
    "storyboard",
    "证据链",
    "制作门禁",
}


def artifact_path(project: Path, name: str) -> Path:
    direct = project / name
    internal = project / "internal" / name
    if direct.exists() or not internal.exists():
        return direct
    return internal


def load_json(path: Path, issues: list[str]) -> dict[str, Any]:
    if not path.is_file() or path.stat().st_size == 0:
        issues.append(f"missing artifact: {path}")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issues.append(f"invalid JSON {path}: {exc}")
        return {}
    if not isinstance(data, dict):
        issues.append(f"artifact must contain an object: {path}")
        return {}
    return data


def nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return value is not None


def require_fields(data: dict[str, Any], fields: tuple[str, ...], label: str, issues: list[str]) -> None:
    for field in fields:
        if not nonempty(data.get(field)):
            issues.append(f"{label}.{field} is required")


def infer_high_risk_domains(script: dict[str, Any]) -> set[str]:
    parts = [
        script.get("viewer_task"),
        script.get("input_method"),
        script.get("execution_process"),
        script.get("visible_result"),
        script.get("before_after"),
    ]
    for beat in script.get("beats") or []:
        if isinstance(beat, dict):
            parts.append(beat.get("narration"))
    text = " ".join(str(part or "") for part in parts).lower()
    return {
        domain
        for domain, keywords in HIGH_RISK_KEYWORDS.items()
        if any(keyword.lower() in text for keyword in keywords)
    }


def safe_area_from_storyboard(storyboard: dict[str, Any]) -> dict[str, Any]:
    direct = storyboard.get("safe_area")
    if isinstance(direct, dict):
        return direct
    design_system = storyboard.get("design_system")
    if isinstance(design_system, dict) and isinstance(design_system.get("safe_area"), dict):
        return design_system["safe_area"]
    return {}


def safe_area_number(safe_area: dict[str, Any], name: str) -> float | None:
    value = safe_area.get(name)
    if value is None:
        value = safe_area.get(f"{name}_px")
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def validate_preproduction(project: Path) -> tuple[list[str], list[str], dict[str, Any]]:
    issues: list[str] = []
    warnings: list[str] = []
    source = load_json(artifact_path(project, "source_brief.json"), issues)
    script = load_json(artifact_path(project, "script.json"), issues)
    storyboard = load_json(artifact_path(project, "storyboard.json"), issues)
    assets = load_json(artifact_path(project, "asset_manifest.json"), issues)
    high_risk_boundary_proof_ids: set[str] = set()
    high_risk_disclosure = ""

    format_type = str(source.get("format_type") or script.get("format_type") or "").strip()
    if format_type not in FORMAT_TYPES:
        issues.append(f"format_type must be one of {sorted(FORMAT_TYPES)}")
    for label, data in (("source_brief", source), ("script", script), ("storyboard", storyboard)):
        if data and str(data.get("format_type") or "").strip() != format_type:
            issues.append(f"{label}.format_type must match {format_type}")

    require_fields(
        source,
        ("project_name", "classification", "topic", "captured_at", "sources", "claims"),
        "source_brief",
        issues,
    )
    project_name = str(source.get("project_name") or "").strip()
    classification = source.get("classification")
    if not isinstance(classification, dict):
        issues.append("source_brief.classification must be an object")
        classification = {}
    else:
        require_fields(
            classification,
            ("level_1", "level_2", "level_3", "category_code"),
            "source_brief.classification",
            issues,
        )
    expected_taxonomy = TAXONOMY_BY_FORMAT.get(format_type)
    if expected_taxonomy:
        for field in ("level_1", "level_2", "category_code"):
            expected_value = expected_taxonomy[field]
            if str(classification.get(field) or "") != expected_value:
                issues.append(
                    f"source_brief.classification.{field} must be {expected_value} "
                    f"for format_type {format_type}"
                )
        name_prefix = expected_taxonomy["project_name_prefix"]
        if project_name and not project_name.startswith(name_prefix):
            issues.append(f"source_brief.project_name must start with {name_prefix}")
        if project_name and not re.search(r"\d{2}$", project_name):
            issues.append("source_brief.project_name must end with a two-digit sequence")
    if format_type == "tool_explainer":
        topic_selection = source.get("topic_selection")
        if not isinstance(topic_selection, dict):
            issues.append("source_brief.topic_selection must be an object")
        else:
            require_fields(
                topic_selection,
                (
                    "mode",
                    "interaction_mode",
                    "material_scan_completed",
                    "selection_basis",
                    "proof_readiness",
                    "confirmation_status",
                ),
                "source_brief.topic_selection",
                issues,
            )
            mode = str(topic_selection.get("mode") or "")
            interaction_mode = str(topic_selection.get("interaction_mode") or "")
            confirmation_status = str(topic_selection.get("confirmation_status") or "")
            if mode not in TOPIC_SELECTION_MODES:
                issues.append(
                    "source_brief.topic_selection.mode must be one of "
                    f"{sorted(TOPIC_SELECTION_MODES)}"
                )
            if interaction_mode not in INTERACTION_MODES:
                issues.append(
                    "source_brief.topic_selection.interaction_mode must be one of "
                    f"{sorted(INTERACTION_MODES)}"
                )
            if confirmation_status not in TOPIC_CONFIRMATION_STATUSES:
                issues.append(
                    "source_brief.topic_selection.confirmation_status must be one of "
                    f"{sorted(TOPIC_CONFIRMATION_STATUSES)}"
                )
            if topic_selection.get("material_scan_completed") is not True:
                issues.append("source_brief.topic_selection.material_scan_completed must be true")
            if topic_selection.get("proof_readiness") != "passed":
                issues.append("source_brief.topic_selection.proof_readiness must be passed")
            if mode == "research_selected" and not nonempty(
                topic_selection.get("selected_candidate_id")
            ):
                issues.append(
                    "research_selected topic requires "
                    "source_brief.topic_selection.selected_candidate_id"
                )
            if interaction_mode == "step_by_step" and confirmation_status != "user_confirmed":
                issues.append(
                    "step_by_step topic selection requires "
                    "source_brief.topic_selection.confirmation_status=user_confirmed"
                )
    if format_type == "news_explainer":
        require_fields(
            source,
            ("published_at", "event_date", "verification_cutoff", "official_channels_checked"),
            "source_brief",
            issues,
        )
    source_ids: set[str] = set()
    for index, item in enumerate(source.get("sources") or []):
        if not isinstance(item, dict):
            issues.append(f"source_brief.sources[{index}] must be an object")
            continue
        require_fields(
            item,
            ("id", "title", "source_type", "locator", "captured_at", "supports_claims"),
            f"source_brief.sources[{index}]",
            issues,
        )
        source_ids.add(str(item.get("id") or ""))

    claim_ids: set[str] = set()
    for index, claim in enumerate(source.get("claims") or []):
        if not isinstance(claim, dict):
            issues.append(f"source_brief.claims[{index}] must be an object")
            continue
        require_fields(
            claim,
            ("id", "text", "fact_status", "source_ids"),
            f"source_brief.claims[{index}]",
            issues,
        )
        claim_id = str(claim.get("id") or "")
        claim_ids.add(claim_id)
        if claim.get("fact_status") not in {"confirmed", "inference", "unknown"}:
            issues.append(f"claim {claim_id} has invalid fact_status")
        if format_type == "news_explainer":
            require_fields(claim, ("claim_kind",), f"source_brief.claims[{index}]", issues)
            if claim.get("claim_kind") not in NEWS_CLAIM_KINDS:
                issues.append(f"claim {claim_id} has invalid news claim_kind")
        if claim.get("negative_assertion") is True:
            require_fields(
                claim,
                ("verification_method", "verification_cutoff"),
                f"source_brief.claims[{index}]",
                issues,
            )
        for source_id in claim.get("source_ids") or []:
            if source_id not in source_ids:
                issues.append(f"claim {claim_id} references unknown source {source_id}")

    reference = source.get("reference_video")
    if isinstance(reference, dict):
        require_fields(
            reference,
            ("playable_path", "sha256", "duration", "width", "height", "fps", "has_audio"),
            "source_brief.reference_video",
            issues,
        )
        playable = Path(str(reference.get("playable_path") or ""))
        if not playable.is_file():
            issues.append(f"reference video is not playable locally: {playable}")

    require_fields(script, ("title", "hook", "beats", "closing_takeaway"), "script", issues)
    require_fields(script, TYPE_FIELDS.get(format_type, ()), "script", issues)
    if format_type == "tool_explainer":
        beginner_review = script.get("beginner_review")
        if not isinstance(beginner_review, dict):
            issues.append("script.beginner_review must be an object")
        else:
            require_fields(
                beginner_review,
                (
                    "status",
                    "task",
                    "input",
                    "process",
                    "result",
                    "old_method_difference",
                    "read_aloud_passed",
                ),
                "script.beginner_review",
                issues,
            )
            if beginner_review.get("status") != "passed":
                issues.append("script.beginner_review.status must be passed")
            if beginner_review.get("read_aloud_passed") is not True:
                issues.append("script.beginner_review.read_aloud_passed must be true")

        voice_lock = script.get("voice_lock")
        if not isinstance(voice_lock, dict):
            issues.append("script.voice_lock must be an object")
        else:
            require_fields(
                voice_lock,
                (
                    "status",
                    "provider",
                    "voice_id",
                    "persona",
                    "rate",
                    "pitch",
                    "confirmation_source",
                ),
                "script.voice_lock",
                issues,
            )
            if voice_lock.get("status") != "locked":
                issues.append("script.voice_lock.status must be locked")

        public_script_text = " ".join(
            [
                str(script.get("hook") or ""),
                *[
                    str(beat.get("narration") or "")
                    for beat in script.get("beats") or []
                    if isinstance(beat, dict)
                ],
            ]
        ).lower()
        for term in sorted(INTERNAL_PUBLIC_TERMS):
            if term.lower() in public_script_text:
                issues.append(f"public narration contains internal production term: {term}")

        risk = script.get("risk_review")
        if not isinstance(risk, dict):
            issues.append("script.risk_review must be an object")
        else:
            require_fields(
                risk,
                ("level", "demo_environment", "real_action_policy"),
                "script.risk_review",
                issues,
            )
            for field in ("sensitive_domains", "stop_conditions"):
                if not isinstance(risk.get(field), list):
                    issues.append(f"script.risk_review.{field} must be an array")
            level = str(risk.get("level") or "")
            environment = str(risk.get("demo_environment") or "")
            policy = str(risk.get("real_action_policy") or "")
            domains_value = risk.get("sensitive_domains")
            domains = {str(item) for item in domains_value} if isinstance(domains_value, list) else set()
            inferred_domains = infer_high_risk_domains(script)
            if level not in RISK_LEVELS:
                issues.append(f"script.risk_review.level must be one of {sorted(RISK_LEVELS)}")
            if environment not in DEMO_ENVIRONMENTS:
                issues.append(
                    "script.risk_review.demo_environment must be one of "
                    f"{sorted(DEMO_ENVIRONMENTS)}"
                )
            if policy not in REAL_ACTION_POLICIES:
                issues.append(
                    "script.risk_review.real_action_policy must be one of "
                    f"{sorted(REAL_ACTION_POLICIES)}"
                )
            unknown_domains = sorted(domains - HIGH_RISK_DOMAINS)
            if unknown_domains:
                issues.append(
                    "script.risk_review.sensitive_domains contains unknown values: "
                    + ", ".join(unknown_domains)
                )
            missing_domains = sorted(inferred_domains - domains)
            if missing_domains:
                issues.append(
                    "script.risk_review is missing inferred sensitive domains: "
                    + ", ".join(missing_domains)
                )
            if domains & HIGH_RISK_DOMAINS or inferred_domains:
                if level != "high":
                    issues.append("sensitive tool domains require script.risk_review.level=high")
                if policy != "blocked":
                    issues.append("high-risk real actions must be blocked")
                if environment not in HIGH_RISK_DEMO_ENVIRONMENTS:
                    issues.append(
                        "high-risk tool demos require test_sandbox, simulated_data, "
                        "or pre_recorded_redacted"
                    )
                if not nonempty(risk.get("stop_conditions")):
                    issues.append("high-risk tool demos require stop_conditions")
                require_fields(
                    risk,
                    ("blocked_actions", "visible_disclosure", "boundary_proof_ids"),
                    "script.risk_review",
                    issues,
                )
                if not isinstance(risk.get("blocked_actions"), list):
                    issues.append("script.risk_review.blocked_actions must be an array")
                if not isinstance(risk.get("boundary_proof_ids"), list):
                    issues.append("script.risk_review.boundary_proof_ids must be an array")
                else:
                    high_risk_boundary_proof_ids = {
                        str(item) for item in risk.get("boundary_proof_ids") or []
                    }
                high_risk_disclosure = str(risk.get("visible_disclosure") or "").strip()
    if format_type == "news_explainer":
        if script.get("event_status") not in NEWS_STATUSES:
            issues.append(f"script.event_status must be one of {sorted(NEWS_STATUSES)}")
        if script.get("event_status") == "reported":
            claim_kinds = {
                str(item.get("claim_kind") or "")
                for item in source.get("claims") or []
                if isinstance(item, dict)
            }
            for required_kind in ("report_existence", "reported_fact"):
                if required_kind not in claim_kinds:
                    issues.append(
                        "reported news requires separate "
                        f"{required_kind} claim in source_brief.claims"
                    )
    if format_type == "list_video":
        list_type = str(script.get("list_type") or "")
        if list_type not in LIST_TYPES:
            issues.append(f"script.list_type must be one of {sorted(LIST_TYPES)}")
        require_fields(
            script,
            ("order_is_ranked", "methodology"),
            "script",
            issues,
        )
        if list_type in {"ranked_list", "hot_rank"} and script.get("order_is_ranked") is not True:
            issues.append(f"{list_type} requires script.order_is_ranked=true")
        if list_type in {"recommendation_list", "comparison_list"} and script.get("order_is_ranked") is not False:
            issues.append(f"{list_type} requires script.order_is_ranked=false")
        if list_type == "hot_rank":
            require_fields(
                script,
                ("time_window", "timezone", "tie_breaker"),
                "script",
                issues,
            )
        for index, item in enumerate(script.get("items") or []):
            if not isinstance(item, dict):
                issues.append(f"script.items[{index}] must be an object")
                continue
            require_fields(
                item,
                ("id", "name", "task", "reason", "proof_ids", "source_ids"),
                f"script.items[{index}]",
                issues,
            )
            if list_type in {"ranked_list", "hot_rank"}:
                require_fields(
                    item,
                    ("rank", "score_inputs"),
                    f"script.items[{index}]",
                    issues,
                )
    beat_ids: set[str] = set()
    proof_ids_used: set[str] = set()
    claims_used: set[str] = set()
    for index, beat in enumerate(script.get("beats") or []):
        if not isinstance(beat, dict):
            issues.append(f"script.beats[{index}] must be an object")
            continue
        require_fields(beat, ("id", "narration", "claim_ids", "proof_ids"), f"script.beats[{index}]", issues)
        beat_ids.add(str(beat.get("id") or ""))
        for claim_id in beat.get("claim_ids") or []:
            claims_used.add(str(claim_id))
            if claim_id not in claim_ids:
                issues.append(f"beat {beat.get('id')} references unknown claim {claim_id}")
        proof_ids_used.update(str(item) for item in (beat.get("proof_ids") or []))

    missing_claims = sorted(claim_ids - claims_used)
    if missing_claims:
        warnings.append("claims not used by script: " + ", ".join(missing_claims))

    require_fields(
        storyboard,
        ("width", "height", "fps", "creative_direction", "render_plan", "scenes"),
        "storyboard",
        issues,
    )
    safe_area = safe_area_from_storyboard(storyboard)
    if not safe_area:
        issues.append("storyboard.safe_area must be an object")
    else:
        safe_values: dict[str, float] = {}
        for field in ("top", "left", "right", "bottom", "caption_bottom"):
            value = safe_area_number(safe_area, field)
            if value is None:
                issues.append(f"storyboard.safe_area.{field} is required and must be numeric")
            else:
                safe_values[field] = value
        try:
            width = float(storyboard.get("width") or 0)
            height = float(storyboard.get("height") or 0)
        except (TypeError, ValueError):
            width = 0
            height = 0
        if width > 0 and height > 0 and len(safe_values) == 5:
            minimums = {
                "top": height * 120 / 1920,
                "left": width * 84 / 1080,
                "right": width * 180 / 1080,
                "bottom": height * 360 / 1920,
                "caption_bottom": height * 380 / 1920,
            }
            for field, minimum in minimums.items():
                if safe_values[field] + 0.01 < minimum:
                    issues.append(
                        f"storyboard.safe_area.{field} must be at least "
                        f"{minimum:.1f}px for {int(width)}x{int(height)}"
                    )
            if safe_values["caption_bottom"] < safe_values["bottom"]:
                issues.append(
                    "storyboard.safe_area.caption_bottom must not be smaller than bottom"
                )
    creative_direction = storyboard.get("creative_direction")
    if not isinstance(creative_direction, dict):
        issues.append("storyboard.creative_direction must be an object")
    else:
        require_fields(
            creative_direction,
            CREATIVE_DIRECTION_FIELDS,
            "storyboard.creative_direction",
            issues,
        )
        for field in ("continuity_devices", "rejected_defaults"):
            if not isinstance(creative_direction.get(field), list):
                issues.append(f"storyboard.creative_direction.{field} must be an array")

    render_plan = storyboard.get("render_plan")
    canonical_renderer = ""
    optional_subrenderers: list[str] = []
    if not isinstance(render_plan, dict):
        issues.append("storyboard.render_plan must be an object")
    else:
        require_fields(
            render_plan,
            ("canonical_renderer", "composition_id"),
            "storyboard.render_plan",
            issues,
        )
        canonical_renderer = str(render_plan.get("canonical_renderer") or "")
        if canonical_renderer != "remotion":
            issues.append("storyboard.render_plan.canonical_renderer must be remotion")
        raw_subrenderers = render_plan.get("optional_subrenderers")
        if not isinstance(raw_subrenderers, list):
            issues.append("storyboard.render_plan.optional_subrenderers must be an array")
        else:
            optional_subrenderers = [str(item) for item in raw_subrenderers]
            unknown_subrenderers = sorted(set(optional_subrenderers) - ALLOWED_SUBRENDERERS)
            if unknown_subrenderers:
                issues.append(
                    "storyboard.render_plan.optional_subrenderers contains unsupported values: "
                    + ", ".join(unknown_subrenderers)
                )

    scene_claims: set[str] = set()
    scene_proofs: set[str] = set()
    scene_visual_modes: list[str] = []
    previous_end = 0.0
    for index, scene in enumerate(storyboard.get("scenes") or []):
        if not isinstance(scene, dict):
            issues.append(f"storyboard.scenes[{index}] must be an object")
            continue
        require_fields(
            scene,
            (
                "id",
                "start",
                "end",
                "beat_ids",
                "claim_ids",
                "proof_ids",
                "visual_mode",
                "visual",
                "evidence_display",
                "motion_intent",
                "change_reason",
                "caption",
            ),
            f"storyboard.scenes[{index}]",
            issues,
        )
        scene_visual_modes.append(str(scene.get("visual_mode") or ""))
        visual_text = str(scene.get("visual") or "").strip().lower()
        if visual_text in VAGUE_VISUAL_TERMS:
            issues.append(
                f"scene {scene.get('id')} visual must describe visible evidence, not a vague style word"
            )
        try:
            start = float(scene.get("start"))
            end = float(scene.get("end"))
        except (TypeError, ValueError):
            issues.append(f"scene {scene.get('id')} has invalid timing")
            continue
        if start < previous_end - 0.01 or end <= start:
            issues.append(f"scene {scene.get('id')} timing is not monotonic")
        previous_end = max(previous_end, end)
        for beat_id in scene.get("beat_ids") or []:
            if beat_id not in beat_ids:
                issues.append(f"scene {scene.get('id')} references unknown beat {beat_id}")
        scene_claims.update(str(item) for item in (scene.get("claim_ids") or []))
        scene_proofs.update(str(item) for item in (scene.get("proof_ids") or []))

    missing_scene_claims = sorted(claims_used - scene_claims)
    if missing_scene_claims:
        issues.append("script claims missing from storyboard: " + ", ".join(missing_scene_claims))
    missing_scene_proofs = sorted(proof_ids_used - scene_proofs)
    if missing_scene_proofs:
        issues.append("script proofs missing from storyboard: " + ", ".join(missing_scene_proofs))

    require_fields(assets, ("assets",), "asset_manifest", issues)
    asset_ids: set[str] = set()
    proof_asset_ids: set[str] = set()
    for index, item in enumerate(assets.get("assets") or []):
        if not isinstance(item, dict):
            issues.append(f"asset_manifest.assets[{index}] must be an object")
            continue
        require_fields(
            item,
            ("id", "role", "source_kind", "path", "source_locator"),
            f"asset_manifest.assets[{index}]",
            issues,
        )
        if not isinstance(item.get("supports_claims"), list):
            issues.append(f"asset_manifest.assets[{index}].supports_claims must be an array")
        asset_id = str(item.get("id") or "")
        asset_ids.add(asset_id)
        if item.get("role") == "proof":
            proof_asset_ids.add(asset_id)
            if item.get("source_kind") not in {"real_capture", "official_source", "user_provided"}:
                issues.append(f"proof asset {asset_id} has non-evidence source_kind")
            require_fields(
                item,
                ("captured_at",),
                f"asset_manifest.assets[{index}]",
                issues,
            )
        path = Path(str(item.get("path") or ""))
        if path and not path.is_absolute():
            path = project / path
        if not path.is_file():
            issues.append(f"asset file missing: {path}")

    missing_assets = sorted(scene_proofs - asset_ids)
    if missing_assets:
        issues.append("storyboard proof ids missing from asset manifest: " + ", ".join(missing_assets))
    nonproof = sorted(scene_proofs - proof_asset_ids)
    if nonproof:
        issues.append("storyboard proof ids are not marked as proof assets: " + ", ".join(nonproof))
    if high_risk_boundary_proof_ids:
        missing_boundary_assets = sorted(high_risk_boundary_proof_ids - proof_asset_ids)
        if missing_boundary_assets:
            issues.append(
                "high-risk boundary proof ids are not proof assets: "
                + ", ".join(missing_boundary_assets)
            )
        missing_boundary_scenes = sorted(high_risk_boundary_proof_ids - scene_proofs)
        if missing_boundary_scenes:
            issues.append(
                "high-risk boundary proof ids are not used by storyboard: "
                + ", ".join(missing_boundary_scenes)
            )
    if high_risk_disclosure:
        visible_text = " ".join(
            [
                *[
                    str(beat.get("narration") or "")
                    for beat in script.get("beats") or []
                    if isinstance(beat, dict)
                ],
                *[
                    str(scene.get("caption") or "")
                    for scene in storyboard.get("scenes") or []
                    if isinstance(scene, dict)
                ],
            ]
        )
        if high_risk_disclosure not in visible_text:
            issues.append(
                "script.risk_review.visible_disclosure must appear in narration or a storyboard caption"
            )

    return issues, warnings, {
        "format_type": format_type,
        "project_name": project_name,
        "classification": {
            "level_1": classification.get("level_1"),
            "level_2": classification.get("level_2"),
            "level_3": classification.get("level_3"),
            "category_code": classification.get("category_code"),
        },
        "claims": len(claim_ids),
        "beats": len(beat_ids),
        "scenes": len(storyboard.get("scenes") or []),
        "assets": len(asset_ids),
        "canonical_renderer": canonical_renderer,
        "optional_subrenderers": optional_subrenderers,
        "visual_modes": scene_visual_modes,
        "safe_area": safe_area,
    }


def validate_project(project: Path, phase: str) -> dict[str, Any]:
    issues, warnings, summary = validate_preproduction(project)
    if phase in {"qa", "publish"}:
        qa = load_json(artifact_path(project, "qa_report.json"), issues)
        if qa and qa.get("status") != "passed":
            issues.append("qa_report.status must be passed")
    if phase == "publish":
        package = load_json(artifact_path(project, "publish_package.json"), issues)
        if package and package.get("gate", {}).get("status") != "passed":
            issues.append("publish_package.gate.status must be passed")
    return {
        "status": "passed" if not issues else "blocked",
        "phase": phase,
        "project": str(project),
        "summary": summary,
        "blocking_issues": issues,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--phase", choices=("preproduction", "qa", "publish"), default="preproduction")
    parser.add_argument("--out")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    report = validate_project(project, args.phase)
    out = Path(args.out) if args.out else project / "validation_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
