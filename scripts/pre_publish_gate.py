#!/usr/bin/env python3
"""Validate the publish contract before upload, publish, or promotion."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from artifact_fingerprint import verify_report_inputs, write_report_with_fingerprints
from ai_video_workflow_guard import build_workflow_guard_report


REQUIRED_QINGDOU_FIELDS = {"title", "caption", "topics"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def load_json(path: Path) -> dict[str, Any]:
    if not exists(path):
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_text(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.strip().splitlines()).strip()


def publish_caption_from_text(value: str) -> str:
    text = normalize_text(value)
    if not text:
        return ""
    labels = "标题|发布文案|话题|封面主标题|封面副标题|封面文字"
    match = re.search(rf"(?m)^发布文案\s*[：:]\s*(.*)$", text)
    if not match:
        return text
    collected = [match.group(1).strip()]
    for line in text[match.end() :].splitlines():
        stripped = line.strip()
        if re.match(rf"^({labels})\s*[：:]", stripped):
            break
        if stripped:
            collected.append(stripped)
    return normalize_text("\n".join(item for item in collected if item))


def checked_fields(report: dict[str, Any]) -> set[str]:
    raw = (
        report.get("checked_fields")
        or report.get("checked_text_fields")
        or report.get("checked", {}).get("fields")
        or []
    )
    if not isinstance(raw, list):
        return set()
    return {str(item).strip().lower() for item in raw if str(item).strip()}


def checked_file_matches(report: dict[str, Any], target: Path) -> bool:
    raw = report.get("checked_files")
    if not isinstance(raw, list):
        return False
    target_text = str(target)
    target_resolved = str(target.resolve()) if target.exists() else target_text
    for item in raw:
        path = Path(str(item))
        item_text = str(path)
        item_resolved = str(path.resolve()) if path.exists() else item_text
        if target_text == item_text or target_resolved == item_resolved:
            return True
    return False


def topic_override_allowed(report: dict[str, Any]) -> bool:
    if report.get("status") != "user_override_accepted":
        return False
    final_check = report.get("final_check") if isinstance(report.get("final_check"), dict) else {}
    override = final_check.get("user_override") if isinstance(final_check.get("user_override"), dict) else {}
    topics_text = " ".join(str(item) for item in (report.get("final_topics") or report.get("topics") or []))
    items = final_check.get("items") if isinstance(final_check.get("items"), list) else []
    terms = [
        str(item.get("term") or "").strip()
        for item in items
        if isinstance(item, dict) and str(item.get("term") or "").strip()
    ]
    return (
        override.get("accepted") is True
        and override.get("allowed_by_skill_rule") is True
        and str(override.get("scope") or "") == "required_official_platform_topic"
        and bool(terms)
        and len(terms) == len(items)
        and all(term in topics_text for term in terms)
    )


def qingdou_passes(report: dict[str, Any], publish_copy: str, issues: list[str]) -> None:
    allow_override = topic_override_allowed(report)
    if report.get("status") != "passed" and not allow_override:
        issues.append("qingdou_keyword_check.status must be passed or a narrow user_override_accepted")

    final_check = report.get("final_check")
    if not isinstance(final_check, dict):
        issues.append("qingdou_keyword_check.final_check is required")
        return

    message = str(final_check.get("message") or "")
    final_status = str(final_check.get("status") or "")
    if not allow_override and final_status != "passed" and "未检查到敏感词" not in message:
        issues.append("qingdou final_check must prove no sensitive keywords")
    if not allow_override and final_check.get("items"):
        issues.append("qingdou final_check.items must be empty unless narrow override is accepted")

    missing_fields = REQUIRED_QINGDOU_FIELDS - checked_fields(report)
    if missing_fields:
        issues.append("qingdou checked_fields missing: " + ", ".join(sorted(missing_fields)))

    title = str(report.get("final_title") or report.get("title") or "").strip()
    caption = str(report.get("final_caption") or report.get("caption") or "").strip()
    topics = report.get("final_topics") or report.get("topics") or []
    if not title:
        issues.append("qingdou final_title is required")
    if not caption:
        issues.append("qingdou final_caption is required")
    if not isinstance(topics, list) or not any(str(item).strip() for item in topics):
        issues.append("qingdou final_topics must list checked topics")
    publish_caption = publish_caption_from_text(publish_copy)
    if publish_caption and normalize_text(caption) != normalize_text(publish_caption):
        issues.append("qingdou final_caption must match publish_copy.txt")


def custom_cover_allowed(report: dict[str, Any], checks: dict[str, Any]) -> bool:
    return (
        report.get("cover_type") == "one_off_custom_reviewed"
        and checks.get("custom_cover_user_approved") is True
        and checks.get("local_and_qingdou_rechecked") is True
        and checks.get("cover_text_written") is True
    )


def fixed_cover_passes(report: dict[str, Any], checks: dict[str, Any], issues: list[str]) -> None:
    if custom_cover_allowed(report, checks):
        return
    required_fields = [
        "template_id",
        "canonical_id",
        "template_path",
        "template_aspect",
        "template_rotation_index",
        "selection_method",
        "template_library_size",
    ]
    for field in required_fields:
        if report.get(field) in (None, ""):
            issues.append(f"publish_cover_report.{field} is required for fixed cover rotation")

    if report.get("cover_type") != "fixed_pure_background_runtime_text_first_frame":
        issues.append("publish_cover_report.cover_type must be fixed_pure_background_runtime_text_first_frame or approved one_off_custom_reviewed")
    if report.get("selection_method") != "sequential_by_size_pool":
        issues.append("publish_cover_report.selection_method must be sequential_by_size_pool")
    if int(report.get("template_library_size") or 0) != 10:
        issues.append("publish_cover_report.template_library_size must be 10")

    template_path = Path(str(report.get("template_path") or ""))
    if str(template_path) and not exists(template_path):
        issues.append(f"publish_cover_report.template_path missing or empty: {template_path}")

    required_true_checks = [
        "template_from_fixed_library",
        "fixed_safe_asset",
        "fixed_pure_background_asset",
        "background_contains_text_false",
        "selected_by_video_size",
        "first_frame_required",
        "dynamic_text_overlay_used",
    ]
    for field in required_true_checks:
        if checks.get(field) is not True:
            issues.append(f"publish_cover_report.checks.{field} must be true")

    if report.get("cover_type") == "fixed_pure_background_runtime_text_first_frame":
        for field in ("fixed_pure_background_asset", "background_contains_text_false", "dynamic_text_overlay_used"):
            if checks.get(field) is not True:
                issues.append(f"publish_cover_report.checks.{field} must be true")
        if checks.get("uses_old_cover_template_asset") is not False:
            issues.append("publish_cover_report.checks.uses_old_cover_template_asset must be false")
        for field in (
            "cover_text_fit_safe_rect",
            "primary_text_inside_douyin_center_crop",
            "douyin_center_crop_preview_generated",
            "compact_cover_text_used",
        ):
            if checks.get(field) is not True:
                issues.append(f"publish_cover_report.checks.{field} must be true")
        layout = report.get("cover_layout") if isinstance(report.get("cover_layout"), dict) else {}
        for field in ("text_bbox_px", "recommended_text_safe_rect_px", "douyin_center_crop_rect_px"):
            value = layout.get(field)
            if not isinstance(value, list) or len(value) != 4:
                issues.append(f"publish_cover_report.cover_layout.{field} must be a 4-number rectangle")
        outputs = report.get("outputs") if isinstance(report.get("outputs"), dict) else {}
        preview = Path(str(outputs.get("douyin_center_crop_preview") or ""))
        if not exists(preview):
            issues.append(f"publish_cover_report.outputs.douyin_center_crop_preview missing or empty: {preview}")


def require_report_passed(name: str, path: Path, issues: list[str], allow_warnings: bool = True) -> dict[str, Any]:
    report = load_json(path)
    if not report:
        issues.append(f"{name} missing or empty: {path}")
        return {}
    if report.get("status") != "passed":
        issues.append(f"{name}.status must be passed")
    if report.get("blocking_issues"):
        issues.append(f"{name}.blocking_issues must be empty")
    if not allow_warnings and report.get("warnings"):
        issues.append(f"{name}.warnings must be empty")
    return report


def require_fresh_report(name: str, report: dict[str, Any], expected_paths: list[Path], issues: list[str]) -> None:
    fresh_issues = verify_report_inputs(report, [path for path in expected_paths if exists(path)])
    if fresh_issues:
        issues.extend(f"{name} stale: {issue}" for issue in fresh_issues)


def existing_sources(paths: list[Path]) -> list[Path]:
    return [path for path in paths if exists(path)]


def visual_regression_passes(report: dict[str, Any], issues: list[str]) -> None:
    checks = report.get("checks") if isinstance(report.get("checks"), dict) else {}
    required_true = {
        "no_legacy_renderer_source": "visual_regression_gate.checks.no_legacy_renderer_source must be true",
        "hyperframes_source_present": "visual_regression_gate.checks.hyperframes_source_present must be true",
        "first_frame_cover_matches": "visual_regression_gate.checks.first_frame_cover_matches must be true",
        "frame1_returns_to_main_timeline": "visual_regression_gate.checks.frame1_returns_to_main_timeline must be true",
        "visual_review_passed": "visual_regression_gate.checks.visual_review_passed must be true",
        "frame_review_passed": "visual_regression_gate.checks.frame_review_passed must be true",
    }
    for field, message in required_true.items():
        if checks.get(field) is not True:
            issues.append(message)
    if report.get("legacy_source_hits"):
        issues.append("visual_regression_gate.legacy_source_hits must be empty")
    first_frame = report.get("first_frame") if isinstance(report.get("first_frame"), dict) else {}
    if not first_frame.get("actual_frame_000_cover") or not first_frame.get("actual_frame_001_after_cover"):
        issues.append("visual_regression_gate.first_frame must record actual frame 0 and frame 1 evidence")


def validate_contract(contract: dict[str, Any]) -> tuple[str, list[str]]:
    issues: list[str] = []
    artifacts = contract.get("artifacts") if isinstance(contract.get("artifacts"), dict) else {}
    publish = contract.get("publish") if isinstance(contract.get("publish"), dict) else {}
    checks = contract.get("checks") if isinstance(contract.get("checks"), dict) else {}

    for key in ("video", "metadata", "publish_copy"):
        source = Path(str((artifacts.get(key) or {}).get("source") or ""))
        if not exists(source):
            issues.append(f"artifact {key} missing or empty: {source}")
    cover = artifacts.get("cover") if isinstance(artifacts.get("cover"), dict) else {}
    cover_source = Path(str(cover.get("source") or ""))
    if not exists(cover_source):
        issues.append(f"artifact cover missing or empty: {cover_source}")
    cover_text_source = Path(str(cover.get("text_source") or ""))
    if not exists(cover_text_source):
        issues.append(f"artifact cover.text_source missing or empty: {cover_text_source}")
    contract_fresh_issues = verify_report_inputs(
        contract,
        existing_sources(
            [Path(str((artifacts.get(key) or {}).get("source") or "")) for key in ("video", "metadata", "publish_copy")]
            + [cover_source, cover_text_source]
        ),
    )
    if contract_fresh_issues:
        issues.extend(f"publish_contract stale: {issue}" for issue in contract_fresh_issues)

    title = str(publish.get("title") or "").strip()
    caption = str(publish.get("caption") or "").strip()
    topics = publish.get("topics") or []
    if not title:
        issues.append("publish.title is required")
    if not caption:
        issues.append("publish.caption is required")
    if not isinstance(topics, list) or not topics:
        issues.append("publish.topics must be non-empty")

    qa = require_report_passed("qa_report", Path(str((checks.get("qa_report") or {}).get("path") or "")), issues)
    video_source = Path(str((artifacts.get("video") or {}).get("source") or ""))
    metadata_source = Path(str((artifacts.get("metadata") or {}).get("source") or ""))
    if qa:
        require_fresh_report("qa_report", qa, [video_source, metadata_source], issues)
    hard_gates = qa.get("hard_gates", {})
    if not hard_gates or not all(bool(value) for value in hard_gates.values()):
        issues.append("qa_report.hard_gates must all be true")
    for gate_key in [
        "foreground_module_plan_exists",
        "foreground_module_plan_check_exists",
        "foreground_module_plan_check_passed",
        "foreground_module_render_manifest_exists",
        "foreground_module_render_check_exists",
        "foreground_module_render_check_passed",
    ]:
        if hard_gates.get(gate_key) is not True:
            issues.append(f"qa_report.hard_gates.{gate_key} must be true")

    foreground_report = require_report_passed(
        "foreground_module_plan_check",
        Path(str((checks.get("foreground_module_plan_check") or {}).get("path") or "")),
        issues,
    )
    if foreground_report.get("blocking_issues"):
        issues.append("foreground_module_plan_check.blocking_issues must be empty")
    render_report = require_report_passed(
        "foreground_module_render_check",
        Path(str((checks.get("foreground_module_render_check") or {}).get("path") or "")),
        issues,
    )
    if render_report.get("blocking_issues"):
        issues.append("foreground_module_render_check.blocking_issues must be empty")

    visual_regression = require_report_passed(
        "visual_regression_gate",
        Path(str((checks.get("visual_regression_gate") or {}).get("path") or "")),
        issues,
        allow_warnings=True,
    )
    if visual_regression:
        require_fresh_report("visual_regression_gate", visual_regression, [video_source, metadata_source], issues)
        visual_regression_passes(visual_regression, issues)

    workflow_guard = require_report_passed(
        "workflow_guard",
        Path(str((checks.get("workflow_guard") or {}).get("path") or "")),
        issues,
    )
    workflow_guard_issues = workflow_guard.get("issues") if isinstance(workflow_guard.get("issues"), list) else []
    for issue in workflow_guard_issues:
        issues.append(f"workflow_guard: {issue}")

    provider = require_report_passed(
        "provider_usage_audit",
        Path(str((checks.get("provider_usage_audit") or {}).get("path") or "")),
        issues,
    )
    if provider.get("issues"):
        issues.append("provider_usage_audit.issues must be empty")
    if provider:
        require_fresh_report("provider_usage_audit", provider, [video_source, metadata_source], issues)

    text_report = require_report_passed(
        "text_compliance",
        Path(str((checks.get("text_compliance") or {}).get("path") or "")),
        issues,
    )
    if exists(cover_text_source) and not checked_file_matches(text_report, cover_text_source):
        issues.append("text_compliance.checked_files must include publish cover text")
    risk_items = text_report.get("risk_items")
    if isinstance(risk_items, list) and any(str(item.get("level") or "") == "error" for item in risk_items if isinstance(item, dict)):
        issues.append("text_compliance contains error-level risk_items")

    cover_report = require_report_passed("publish_cover_report", Path(str((checks.get("cover") or {}).get("path") or "")), issues)
    if cover_report and cover_report.get("frame_grab_used") is True:
        issues.append("publish_cover_report.frame_grab_used must be false")
    cover_checks = cover_report.get("checks") if isinstance(cover_report.get("checks"), dict) else {}
    if cover_report and cover_checks.get("cover_text_written") is not True:
        issues.append("publish_cover_report.checks.cover_text_written must be true")
    if cover_report:
        fixed_cover_passes(cover_report, cover_checks, issues)

    publish_copy_path = Path(str((artifacts.get("publish_copy") or {}).get("source") or ""))
    publish_copy = publish_copy_path.read_text(encoding="utf-8") if exists(publish_copy_path) else ""
    qingdou = load_json(Path(str((checks.get("qingdou_keyword_check") or {}).get("path") or "")))
    if not qingdou:
        issues.append("qingdou_keyword_check missing or empty")
    else:
        qingdou_passes(qingdou, publish_copy, issues)

    return ("passed" if not issues else "failed"), issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate publish_contract.json before promote/upload/publish.")
    parser.add_argument("--contract", required=True, help="Path to internal/publish_contract.json")
    parser.add_argument("--out", help="Defaults to overwrite --contract")
    args = parser.parse_args()

    contract_path = Path(args.contract)
    contract = load_json(contract_path)
    if not contract:
        raise SystemExit(f"publish contract missing or empty: {contract_path}")
    project = Path(str(contract.get("project") or contract_path.parents[1]))
    workflow_report = build_workflow_guard_report(project, phase="publish")
    checks = contract.setdefault("checks", {})
    checks["workflow_guard"] = {
        "path": str(project / "internal" / "workflow_guard.json"),
        "status": workflow_report.get("status"),
    }
    status, issues = validate_contract(contract)
    contract["updated_at"] = now_iso()
    contract["gate"] = {
        "status": status,
        "issues": issues,
        "verified_at": now_iso(),
    }
    artifacts = contract.get("artifacts") if isinstance(contract.get("artifacts"), dict) else {}
    gate_inputs = [
        Path(str((artifacts.get(key) or {}).get("source") or ""))
        for key in ("video", "metadata", "publish_copy")
    ]
    cover = artifacts.get("cover") if isinstance(artifacts.get("cover"), dict) else {}
    gate_inputs.append(Path(str(cover.get("source") or "")))
    gate_inputs.append(Path(str(cover.get("text_source") or "")))
    write_report_with_fingerprints(contract, [path for path in gate_inputs if exists(path)])
    out = Path(args.out) if args.out else contract_path
    out.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(contract["gate"], ensure_ascii=False, indent=2))
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
