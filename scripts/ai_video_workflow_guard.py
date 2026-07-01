#!/usr/bin/env python3
"""Hard workflow guard for publish-ready AI video projects.

This guard closes the gap between written skill rules and publish gates. It is
meant to run before building or accepting a publish contract, so a project
cannot be promoted after skipping TOP5 ranking, cover, frame-review, visual
system, or publish-evidence workflow artifacts.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from artifact_fingerprint import write_report_with_fingerprints


TOP5_REQUIRED_FIELDS = (
    "rank",
    "title",
    "source_title",
    "visible_date",
    "why_now",
    "why_it_matters",
    "viewer_action",
    "rank_score",
    "score_breakdown",
    "risk_flags",
)
TOP5_SCORE_FIELDS = (
    "freshness",
    "impact",
    "practical_value",
    "source_strength",
    "visual_clarity",
    "compliance_safety",
)
ANT_AI_BACKGROUND_TEMPLATE_ID = "BG_FIXED_11_ANT_AI_HOTLIST_NEBULA_9X16"
ANT_AI_BGM_SOURCE_ID = "ant_ai_scheme7_top5_reference_bgm_7654135072895400421"
ANT_AI_VOICE_PROFILE_ID = "VOICE_MALE_THICK_YUNYANG_V1"
ANT_AI_FIXED_CTA = "关注 蚂蚁AI"
FRAME_REVIEW_CHECKLIST_FIELDS = (
    "first_5s_has_visual_change",
    "first_frame_is_cover_quality",
    "captions_readable_on_phone",
    "proof_panel_readable",
    "no_text_overlap",
    "no_generic_background",
    "motion_not_random",
    "no_freeze_or_black_frames",
    "cover_ok",
)
COMMON_WORKFLOW_FILES = (
    "topic_candidates.json",
    "selected_topic.json",
    "director_selection.json",
    "style_recipe.json",
    "hook_variants.json",
    "hook_score_report.json",
    "reference_overfit_audit.json",
    "fixed_template_selection.json",
    "copy_package.md",
    "copy_package.json",
    "script_score.json",
    "semantic_review.json",
    "content_alignment_report.json",
    "beginner_value_review.json",
    "compliance_report.json",
    "visual_style_decision.json",
    "visual_style_plan.json",
    "background_prompt_pack.md",
    "storyboard.json",
    "storyboard_validation.json",
    "foreground_module_plan.json",
    "foreground_module_plan_check.json",
    "foreground_module_render_manifest.json",
    "foreground_module_render_check.json",
    "asset_manifest.json",
    "asset_validation.json",
    "storyboard.audio_locked.json",
    "draft.mp4",
    "metadata.json",
    "video_technical_qa.json",
    "frame_review_report.json",
    "visual_review.json",
)
PUBLISH_WORKFLOW_FILES = (
    "provider_usage_audit.json",
    "on_screen_and_publish_text_compliance_report.json",
    "publish_cover_report.json",
    "publish_cover_text.txt",
    "cover.png",
    "first_frame_cover.png",
    "actual_frame_000_cover.png",
    "actual_frame_001_after_cover.png",
    "cover_publish_douyin_center_crop.png",
    "publish_copy.txt",
    "qingdou_keyword_check.json",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def dir_has_files(path: Path) -> bool:
    return path.exists() and path.is_dir() and any(item.is_file() and item.stat().st_size > 0 for item in path.rglob("*"))


def load_json(path: Path) -> Any:
    if not exists(path):
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_path(project: Path, raw: Any) -> Path:
    path = Path(str(raw or ""))
    if path.is_absolute():
        return path
    return project / path


def report_status_ok(report: Any, accepted: set[str] | None = None) -> bool:
    if accepted is None:
        accepted = {"passed"}
    return isinstance(report, dict) and str(report.get("status") or "") in accepted


def require_file(internal: Path, name: str, issues: list[str], evidence: list[Path]) -> None:
    path = internal / name
    if exists(path):
        evidence.append(path)
    else:
        issues.append(f"missing workflow artifact: internal/{name}")


def require_status(
    internal: Path,
    name: str,
    issues: list[str],
    evidence: list[Path],
    accepted: set[str] | None = None,
) -> dict[str, Any]:
    path = internal / name
    report = load_json(path)
    if not isinstance(report, dict) or not report:
        issues.append(f"missing or invalid report: internal/{name}")
        return {}
    evidence.append(path)
    if not report_status_ok(report, accepted):
        issues.append(f"internal/{name}.status must be one of {sorted(accepted or {'passed'})}")
    blocking = report.get("blocking_issues")
    if isinstance(blocking, list) and blocking:
        issues.append(f"internal/{name}.blocking_issues must be empty")
    return report


def extract_scheme_id(selection: dict[str, Any], internal: Path) -> str:
    scheme = selection.get("scheme") if isinstance(selection.get("scheme"), dict) else {}
    raw = str(scheme.get("id") or selection.get("scheme_id") or "").strip()
    if raw:
        return raw
    if exists(internal / "ai_hot_rank_top5.json"):
        return "scheme_7_ai_hot_rank_top5"
    text = (
        read_text(internal / "selected_topic.json")
        + "\n"
        + read_text(internal / "copy_package.json")
        + "\n"
        + read_text(internal / "copy_package.md")
    ).lower()
    if any(marker in text for marker in ("top5", "top 5", "热榜", "榜单", "排行", "排名")):
        return "scheme_7_ai_hot_rank_top5"
    return raw


def top5_items(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if not isinstance(data, dict):
        return []
    for key in ("items", "rank_items", "ranked_items", "top5", "ranks"):
        value = data.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def validate_top5(internal: Path, issues: list[str], evidence: list[Path]) -> dict[str, Any]:
    path = internal / "ai_hot_rank_top5.json"
    data = load_json(path)
    if exists(path):
        evidence.append(path)
    if not data:
        issues.append("scheme_7 requires internal/ai_hot_rank_top5.json before copywriting or rendering")
        return {"item_count": 0}

    items = top5_items(data)
    if len(items) != 5:
        issues.append("scheme_7 ai_hot_rank_top5 must contain exactly five ranked items")

    ranks: list[int] = []
    scores: list[float] = []
    for index, item in enumerate(items, start=1):
        prefix = f"scheme_7 rank item {index}"
        for field in TOP5_REQUIRED_FIELDS:
            if field not in item or item.get(field) in (None, "", []):
                issues.append(f"{prefix} missing {field}")
        if not (item.get("source_url_or_note") or item.get("source_url") or item.get("evidence_note")):
            issues.append(f"{prefix} missing source_url_or_note")
        try:
            ranks.append(int(item.get("rank")))
        except Exception:
            issues.append(f"{prefix}.rank must be an integer")
        try:
            scores.append(float(item.get("rank_score")))
        except Exception:
            issues.append(f"{prefix}.rank_score must be numeric")
        breakdown = item.get("score_breakdown") if isinstance(item.get("score_breakdown"), dict) else {}
        for field in TOP5_SCORE_FIELDS:
            if field not in breakdown:
                issues.append(f"{prefix}.score_breakdown missing {field}")

    if len(ranks) == 5 and ranks != [1, 2, 3, 4, 5]:
        issues.append("scheme_7 ranks must be exactly 1..5 in display order")
    if len(scores) == 5 and scores != sorted(scores, reverse=True):
        issues.append("scheme_7 rank_score values must be sorted descending")

    scan = internal / "hot_rank_scan_report.md"
    if exists(scan):
        evidence.append(scan)
    else:
        issues.append("scheme_7 requires internal/hot_rank_scan_report.md")

    cover_text = read_text(internal / "publish_cover_text.txt").lower()
    if cover_text and not any(marker in cover_text for marker in ("top5", "top 5", "热榜", "榜单", "排行")):
        issues.append("scheme_7 cover text must clearly signal TOP5/hot-rank content")

    return {"item_count": len(items), "ranks": ranks, "rank_scores": scores}


def validate_fixed_visual_system(internal: Path, project: Path, issues: list[str], evidence: list[Path]) -> dict[str, Any]:
    selection = require_status(internal, "fixed_template_selection.json", issues, evidence, {"passed", "locked"})
    background = selection.get("background_template") if isinstance(selection.get("background_template"), dict) else {}
    background_path = resolve_path(project, background.get("render_asset_path") or background.get("dynamic_asset_path"))
    if not exists(background_path):
        issues.append(f"fixed_template_selection background render asset missing or empty: {background_path}")
    elif background_path.suffix.lower() != ".mp4":
        issues.append("fixed_template_selection background render asset must be a dynamic MP4")
    if background.get("render_asset_is_dynamic") is not True:
        issues.append("fixed_template_selection.background_template.render_asset_is_dynamic must be true")

    inheritance = selection.get("inheritance_contract") if isinstance(selection.get("inheritance_contract"), dict) else {}
    for field in (
        "background_drives_foreground",
        "dynamic_background_default",
        "static_background_fallback_removed",
        "transition_pack_drives_sfx",
        "component_pack_drives_storyboard_shapes",
        "voice_profile_drives_tts_and_mix",
    ):
        if inheritance.get(field) is not True:
            issues.append(f"fixed_template_selection.inheritance_contract.{field} must be true")

    plan = require_status(internal, "foreground_module_plan_check.json", issues, evidence)
    render = require_status(internal, "foreground_module_render_check.json", issues, evidence)
    if plan.get("status") == "passed" and render.get("status") == "passed":
        pass
    ant_ai = validate_ant_ai_extended_selection(selection, issues, evidence)
    return {
        "background_render_asset": str(background_path),
        "foreground_plan_check": plan.get("status"),
        "foreground_render_check": render.get("status"),
        "ant_ai_extended": ant_ai,
    }


def validate_ant_ai_extended_selection(selection: dict[str, Any], issues: list[str], evidence: list[Path]) -> dict[str, Any]:
    content = selection.get("content") if isinstance(selection.get("content"), dict) else {}
    background = selection.get("background_template") if isinstance(selection.get("background_template"), dict) else {}
    audio = selection.get("audio_music_decision") if isinstance(selection.get("audio_music_decision"), dict) else {}
    voice = selection.get("voice_mix_profile") if isinstance(selection.get("voice_mix_profile"), dict) else {}
    markers = {
        str(content.get("scheme_variant") or ""),
        str(content.get("extended_profile") or ""),
        str(content.get("background_style_id_from_director") or ""),
        str(background.get("id") or ""),
        str(audio.get("default_bgm_source_id") or ""),
    }
    is_extended = bool(
        {"ant_ai_hotlist_extended", "scheme7_ant_ai_hotlist_extended", ANT_AI_BACKGROUND_TEMPLATE_ID, ANT_AI_BGM_SOURCE_ID} & markers
    )
    if not is_extended:
        return {"status": "not_required"}

    if background.get("id") != ANT_AI_BACKGROUND_TEMPLATE_ID:
        issues.append(f"ant_ai_hotlist_extended background_template.id must be {ANT_AI_BACKGROUND_TEMPLATE_ID}")
    if content.get("brand_name") != "蚂蚁AI":
        issues.append("ant_ai_hotlist_extended content.brand_name must be 蚂蚁AI")
    if content.get("fixed_cta") != ANT_AI_FIXED_CTA:
        issues.append(f"ant_ai_hotlist_extended content.fixed_cta must be {ANT_AI_FIXED_CTA}")
    if audio.get("default_bgm_source_id") != ANT_AI_BGM_SOURCE_ID:
        issues.append(f"ant_ai_hotlist_extended audio_music_decision.default_bgm_source_id must be {ANT_AI_BGM_SOURCE_ID}")
    if audio.get("voice_policy") != "required_narration":
        issues.append("ant_ai_hotlist_extended audio_music_decision.voice_policy must be required_narration")
    if audio.get("voice_priority") is not True:
        issues.append("ant_ai_hotlist_extended audio_music_decision.voice_priority must be true")
    if audio.get("generated_bgm_allowed") is not False:
        issues.append("ant_ai_hotlist_extended audio_music_decision.generated_bgm_allowed must be false")
    if audio.get("generated_background_audio_allowed") is not False:
        issues.append("ant_ai_hotlist_extended audio_music_decision.generated_background_audio_allowed must be false")
    if audio.get("voice_profile_id") != ANT_AI_VOICE_PROFILE_ID:
        issues.append(f"ant_ai_hotlist_extended audio_music_decision.voice_profile_id must be {ANT_AI_VOICE_PROFILE_ID}")
    if voice.get("id") != ANT_AI_VOICE_PROFILE_ID:
        issues.append(f"ant_ai_hotlist_extended voice_mix_profile.id must be {ANT_AI_VOICE_PROFILE_ID}")
    bgm_path = Path(str(audio.get("default_bgm_local_path") or ""))
    if not exists(bgm_path):
        issues.append(f"ant_ai_hotlist_extended default BGM file missing or empty: {bgm_path}")
    else:
        evidence.append(bgm_path)
    return {
        "status": "checked",
        "background_template_id": background.get("id"),
        "bgm_source_id": audio.get("default_bgm_source_id"),
        "fixed_cta": content.get("fixed_cta"),
        "voice_profile_id": voice.get("id"),
    }


def validate_frame_review(internal: Path, issues: list[str], evidence: list[Path]) -> dict[str, Any]:
    frame = require_status(internal, "frame_review_report.json", issues, evidence)
    manual = frame.get("manual_review") if isinstance(frame.get("manual_review"), dict) else {}
    if manual.get("status") != "passed" or not str(manual.get("reviewer") or "").strip():
        issues.append("frame_review_report must include manual_review.status=passed and reviewer")
    checklist = manual.get("checklist") if isinstance(manual.get("checklist"), dict) else {}
    for field in FRAME_REVIEW_CHECKLIST_FIELDS:
        if checklist.get(field) is not True:
            issues.append(f"frame_review_report.manual_review.checklist.{field} must be true")

    artifacts = frame.get("artifacts") if isinstance(frame.get("artifacts"), dict) else {}
    required_artifacts = ("first_5s_contact_sheet", "full_video_contact_sheet", "crowded_frames_dir")
    artifact_status: dict[str, str] = {}
    for key in required_artifacts:
        raw = artifacts.get(key)
        if not raw:
            issues.append(f"frame_review_report.artifacts.{key} is required")
            artifact_status[key] = "missing"
            continue
        path = Path(str(raw))
        if path.is_dir():
            ok = dir_has_files(path)
        else:
            ok = exists(path)
        if not ok:
            issues.append(f"frame_review_report.artifacts.{key} missing or empty: {path}")
            artifact_status[key] = "missing"
        else:
            artifact_status[key] = "present"
            if path.is_file():
                evidence.append(path)

    return {"manual_review": manual.get("status"), "artifacts": artifact_status}


def validate_visual_review(internal: Path, issues: list[str], evidence: list[Path]) -> dict[str, Any]:
    visual = require_status(internal, "visual_review.json", issues, evidence)
    scores = visual.get("scores") if isinstance(visual.get("scores"), dict) else {}
    thresholds = {
        "first_5s_score": 8.5,
        "readability_score": 8.0,
        "composition_score": 8.0,
        "layering_score": 8.5,
        "quality_check_score": 8.5,
        "sound_design_score": 8.5,
        "export_readiness_score": 8.5,
    }
    for field, minimum in thresholds.items():
        try:
            value = float(scores.get(field) or 0)
        except Exception:
            value = 0.0
        if value < minimum:
            issues.append(f"visual_review.scores.{field} must be >= {minimum}")
    return {"status": visual.get("status"), "scores": scores}


def validate_cover(internal: Path, project: Path, issues: list[str], evidence: list[Path]) -> dict[str, Any]:
    cover = require_status(internal, "publish_cover_report.json", issues, evidence)
    checks = cover.get("checks") if isinstance(cover.get("checks"), dict) else {}
    for field in (
        "dynamic_text_overlay_used",
        "cover_text_written",
        "cover_text_fit_safe_rect",
        "primary_text_inside_douyin_center_crop",
        "douyin_center_crop_preview_generated",
        "compact_cover_text_used",
    ):
        if checks.get(field) is not True:
            issues.append(f"publish_cover_report.checks.{field} must be true")
    if cover.get("frame_grab_used") is True:
        issues.append("publish_cover_report.frame_grab_used must be false")

    for name in (
        "cover.png",
        "first_frame_cover.png",
        "actual_frame_000_cover.png",
        "actual_frame_001_after_cover.png",
        "cover_publish_douyin_center_crop.png",
        "publish_cover_text.txt",
    ):
        require_file(internal, name, issues, evidence)

    outputs = cover.get("outputs") if isinstance(cover.get("outputs"), dict) else {}
    center = resolve_path(project, outputs.get("douyin_center_crop_preview") or internal / "cover_publish_douyin_center_crop.png")
    if not exists(center):
        issues.append(f"publish_cover_report.outputs.douyin_center_crop_preview missing or empty: {center}")
    layout = cover.get("cover_layout") if isinstance(cover.get("cover_layout"), dict) else {}
    for field in ("text_bbox_px", "recommended_text_safe_rect_px", "douyin_center_crop_rect_px"):
        value = layout.get(field)
        if not isinstance(value, list) or len(value) != 4:
            issues.append(f"publish_cover_report.cover_layout.{field} must be a 4-number rectangle")

    return {
        "cover_type": cover.get("cover_type"),
        "center_crop_preview": str(center),
        "checks": {key: checks.get(key) for key in sorted(checks)},
    }


def validate_publish_evidence(internal: Path, issues: list[str], evidence: list[Path]) -> dict[str, Any]:
    provider = require_status(internal, "provider_usage_audit.json", issues, evidence)
    if provider.get("issues"):
        issues.append("provider_usage_audit.issues must be empty")

    text_report = require_status(internal, "on_screen_and_publish_text_compliance_report.json", issues, evidence)
    checked_files = text_report.get("checked_files") if isinstance(text_report.get("checked_files"), list) else []
    for required_name in ("publish_cover_text.txt", "publish_copy.txt"):
        if not any(required_name in str(item) for item in checked_files):
            issues.append(f"on_screen_and_publish_text_compliance_report.checked_files must include {required_name}")

    qingdou = require_status(internal, "qingdou_keyword_check.json", issues, evidence, {"passed", "user_override_accepted"})
    fields = qingdou.get("checked_fields") if isinstance(qingdou.get("checked_fields"), list) else []
    for field in ("title", "caption", "topics"):
        if field not in {str(item).strip().lower() for item in fields}:
            issues.append(f"qingdou_keyword_check.checked_fields must include {field}")

    return {
        "provider_status": provider.get("status"),
        "text_status": text_report.get("status"),
        "qingdou_status": qingdou.get("status"),
    }


def build_workflow_guard_report(project: Path, phase: str = "publish", out: Path | None = None) -> dict[str, Any]:
    project = project.resolve()
    internal = project / "internal"
    issues: list[str] = []
    warnings: list[str] = []
    evidence: list[Path] = []

    if not internal.exists():
        issues.append(f"project internal directory missing: {internal}")

    for name in COMMON_WORKFLOW_FILES:
        require_file(internal, name, issues, evidence)
    if phase == "publish":
        for name in PUBLISH_WORKFLOW_FILES:
            require_file(internal, name, issues, evidence)

    director = require_status(internal, "director_selection.json", issues, evidence, {"passed", "locked"})
    require_status(internal, "style_recipe.json", issues, evidence, {"passed", "locked"})
    require_status(internal, "hook_score_report.json", issues, evidence)
    require_status(internal, "reference_overfit_audit.json", issues, evidence)
    fixed_visual = validate_fixed_visual_system(internal, project, issues, evidence)
    frame_review = validate_frame_review(internal, issues, evidence)
    visual_review = validate_visual_review(internal, issues, evidence)

    scheme_id = extract_scheme_id(director, internal)
    top5_report: dict[str, Any] = {"status": "not_required"}
    if scheme_id == "scheme_7_ai_hot_rank_top5":
        top5_report = validate_top5(internal, issues, evidence)

    cover_report: dict[str, Any] = {"status": "not_checked"}
    publish_report: dict[str, Any] = {"status": "not_checked"}
    if phase == "publish":
        cover_report = validate_cover(internal, project, issues, evidence)
        publish_report = validate_publish_evidence(internal, issues, evidence)

    report = {
        "status": "passed" if not issues else "failed",
        "phase": phase,
        "verified_at": now_iso(),
        "project": str(project),
        "scheme_id": scheme_id,
        "checks": {
            "required_workflow_artifacts_present": not any("missing workflow artifact" in issue for issue in issues),
            "fixed_dynamic_background_and_foreground": not any("fixed_template_selection" in issue for issue in issues),
            "manual_visual_review_evidence": not any("frame_review_report" in issue for issue in issues),
            "visual_review_thresholds": not any("visual_review" in issue for issue in issues),
            "publish_cover_center_crop": phase != "publish" or not any("publish_cover_report" in issue or "cover_" in issue for issue in issues),
            "publish_text_and_qingdou": phase != "publish" or not any("qingdou" in issue or "text_compliance" in issue for issue in issues),
            "scheme7_top5_rank_lock": scheme_id != "scheme_7_ai_hot_rank_top5" or not any("scheme_7" in issue for issue in issues),
        },
        "fixed_visual_system": fixed_visual,
        "frame_review": frame_review,
        "visual_review": visual_review,
        "top5": top5_report,
        "cover": cover_report,
        "publish": publish_report,
        "issues": issues,
        "blocking_issues": issues,
        "warnings": warnings,
    }
    write_report_with_fingerprints(report, [path for path in evidence if exists(path)])
    if out is None:
        out = internal / "workflow_guard.json"
    write_json(out, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the AI video workflow before publish contract gates.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument("--phase", choices=["visual", "publish"], default="publish")
    parser.add_argument("--out", help="Defaults to <project>/internal/workflow_guard.json")
    args = parser.parse_args()

    report = build_workflow_guard_report(
        Path(args.project),
        phase=args.phase,
        out=Path(args.out) if args.out else None,
    )
    print(json.dumps({"status": report["status"], "issues": report["issues"]}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
