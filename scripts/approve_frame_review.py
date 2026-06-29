#!/usr/bin/env python3
"""Approve generated frame-review contact sheets with a hash-bound checklist."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from artifact_fingerprint import collect_fingerprints, verify_report_inputs, write_report_with_fingerprints


REQUIRED_CHECKLIST_FIELDS = [
    "first_5s_has_visual_change",
    "first_frame_is_cover_quality",
    "captions_readable_on_phone",
    "proof_panel_readable",
    "no_text_overlap",
    "no_generic_background",
    "motion_not_random",
    "no_freeze_or_black_frames",
    "cover_ok",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def artifact_paths(report: dict[str, Any]) -> list[Path]:
    artifacts = report.get("artifacts") if isinstance(report.get("artifacts"), dict) else {}
    paths: list[Path] = []
    for raw in artifacts.values():
        path = Path(str(raw))
        if path.is_dir():
            paths.extend(sorted(item for item in path.rglob("*") if item.is_file()))
        elif exists(path):
            paths.append(path)
    return paths


def validate_checklist(checklist: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    for field in REQUIRED_CHECKLIST_FIELDS:
        if checklist.get(field) is not True:
            issues.append(f"checklist.{field} must be true")
    return issues


def approve(project: Path, reviewer: str, checklist_path: Path) -> dict[str, Any]:
    if not reviewer.strip():
        raise SystemExit("--reviewer is required")
    internal = project / "internal"
    draft = internal / "draft.mp4"
    report_path = internal / "frame_review_report.json"
    if not exists(draft):
        raise SystemExit(f"draft video missing or empty: {draft}")
    if not exists(report_path):
        raise SystemExit(f"frame review report missing or empty: {report_path}")
    checklist = load_json(checklist_path)
    checklist_issues = validate_checklist(checklist)
    if checklist_issues:
        raise SystemExit("frame review checklist failed:\n" + "\n".join(checklist_issues))

    report = load_json(report_path)
    if report.get("status") == "failed" or report.get("blocking_issues"):
        raise SystemExit("frame_review_report.json has blocking issues; regenerate contact sheets first")
    stale_issues = verify_report_inputs(report, [draft])
    if stale_issues:
        raise SystemExit("frame_review_report.json is stale:\n" + "\n".join(stale_issues))

    contacts = artifact_paths(report)
    if not contacts:
        raise SystemExit("frame_review_report.json does not list contact sheet artifacts")

    report["status"] = "passed"
    report["review_state"] = "approved"
    report["warnings"] = []
    report["manual_review"] = {
        "status": "passed",
        "reviewer": reviewer.strip(),
        "reviewed_at": now_iso(),
        "checklist": checklist,
        "required_checklist_fields": REQUIRED_CHECKLIST_FIELDS,
        "draft": str(draft),
        "contact_sheet_count": len(contacts),
    }
    report["approval_fingerprints"] = {
        "draft": collect_fingerprints([draft]),
        "contact_sheets": collect_fingerprints(contacts),
    }
    write_report_with_fingerprints(report, [draft, *contacts])
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"status": "approved", "report": str(report_path), "contact_sheet_count": len(contacts)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Approve frame_review_report.json after visual inspection.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic>")
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--checklist-json", required=True)
    args = parser.parse_args()

    result = approve(Path(args.project), args.reviewer, Path(args.checklist_json))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
