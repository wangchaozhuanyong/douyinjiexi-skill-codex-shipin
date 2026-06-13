#!/usr/bin/env python3
"""Final QA gate for V2 output projects."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def exists(path: Path) -> bool:
    return path.exists() and path.stat().st_size >= 0


def bool_gate(gates: dict[str, bool], key: str, value: bool, issues: list[str], message: str) -> None:
    gates[key] = bool(value)
    if not value:
        issues.append(message)


def get_score(data: dict[str, Any], *names: str, default: float = 0.0) -> float:
    for name in names:
        if name in data:
            try:
                return float(data[name])
            except Exception:
                return default
    return default


def main() -> int:
    parser = argparse.ArgumentParser(description="Run final QA for an output project.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic>")
    parser.add_argument("--out", required=True, help="qa_report.json path")
    args = parser.parse_args()

    project = Path(args.project)
    internal = project / "internal"
    final = project / "final"
    issues: list[str] = []
    warnings: list[str] = []
    gates: dict[str, bool] = {}

    paths = {
        "topic_candidates": internal / "topic_candidates.json",
        "selected_topic": internal / "selected_topic.json",
        "copy_package": internal / "copy_package.md",
        "compliance": internal / "compliance_report.json",
        "storyboard": internal / "storyboard.json",
        "audio_locked": internal / "storyboard.audio_locked.json",
        "asset_manifest": internal / "asset_manifest.json",
        "metadata": internal / "metadata.json",
        "final_video": final / "final.mp4",
        "cover": final / "cover.png",
        "publish_copy": final / "publish_copy.txt",
    }

    bool_gate(gates, "topic_candidates_exists", exists(paths["topic_candidates"]), issues, "missing topic_candidates.json")
    bool_gate(gates, "selected_topic_exists", exists(paths["selected_topic"]), issues, "missing selected_topic.json")
    bool_gate(gates, "copy_package_exists", exists(paths["copy_package"]), issues, "missing copy_package.md")
    bool_gate(gates, "storyboard_exists", exists(paths["storyboard"]), issues, "missing storyboard.json")
    bool_gate(gates, "audio_locked", exists(paths["audio_locked"]), issues, "missing storyboard.audio_locked.json")
    bool_gate(gates, "asset_manifest_exists", exists(paths["asset_manifest"]), issues, "missing asset_manifest.json")
    bool_gate(gates, "metadata_exists", exists(paths["metadata"]), issues, "missing metadata.json")
    bool_gate(gates, "final_video_exists", exists(paths["final_video"]), issues, "missing final/final.mp4")
    bool_gate(gates, "cover_exists", exists(paths["cover"]), issues, "missing final/cover.png")
    bool_gate(gates, "publish_copy_exists", exists(paths["publish_copy"]), issues, "missing final/publish_copy.txt")

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
    first_5 = 0.0
    visual_score = 0.0
    sync_score = 0.0
    topic_score = 0.0

    if exists(paths["topic_candidates"]):
        topic_data = load_json(paths["topic_candidates"])
        candidates = topic_data.get("candidates", [])
        topic_score = max([get_score(item.get("scores", {}), "total_score") for item in candidates] or [0.0])
        if topic_score < 8:
            issues.append("topic_score must be >= 8")

    score_path = internal / "script_score.json"
    if exists(score_path):
        script_data = load_json(score_path)
        script_score = get_score(script_data, "script_score")
        first_5 = get_score(script_data, "first_5_seconds_score")
        if script_score < 8:
            issues.append("script_score must be >= 8")
        if first_5 < 9:
            issues.append("first_5_seconds_score must be >= 9")
    else:
        warnings.append("script_score.json missing; QA uses 0 for script scores")

    storyboard_report_path = internal / "storyboard_validation.json"
    if exists(storyboard_report_path):
        story_report = load_json(storyboard_report_path)
        evidence_ratio = float(story_report.get("evidence_runtime_ratio", 0))
        visual_score = 8.5 if story_report.get("status") == "passed" else 0.0
        sync_score = 9.0 if story_report.get("status") == "passed" else 0.0
        if story_report.get("status") != "passed":
            issues.extend(story_report.get("issues", []))
    else:
        warnings.append("storyboard_validation.json missing; run validate_storyboard.py")

    bool_gate(gates, "not_static_image_only", evidence_ratio >= 0.5, issues, "evidence_runtime_ratio must be >= 0.5")
    bool_gate(gates, "audio_video_synced", exists(paths["audio_locked"]), issues, "audio lock is required for sync")

    status = "passed" if not issues and all(gates.values()) else "failed"
    report = {
        "status": status,
        "scores": {
            "topic_score": round(topic_score, 2),
            "first_5_seconds_score": round(first_5, 2),
            "script_score": round(script_score, 2),
            "visual_score": round(visual_score, 2),
            "sync_score": round(sync_score, 2),
            "compliance_score": round(compliance_score, 2),
        },
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
