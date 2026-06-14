#!/usr/bin/env python3
"""Final QA gate for output projects.

The gate validates the internal draft package and writes ``qa_report.json``.
It does not create ``final/`` artifacts; use ``promote_final.py`` after this
report passes.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


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


def get_score(data: dict[str, Any], *names: str, default: float = 0.0) -> float:
    for name in names:
        if name in data:
            try:
                return float(data[name])
            except Exception:
                return default
    return default


def quality_level(scores: dict[str, float], evidence_ratio: float, gates: dict[str, bool]) -> str:
    if (
        scores["topic_score"] >= 9
        and scores.get("first_3_seconds_score", 0) >= 9.4
        and scores["first_5_seconds_score"] >= 9.3
        and scores["script_score"] >= 9
        and scores.get("semantic_score", 0) >= 9
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

    paths = {
        "topic_candidates": internal / "topic_candidates.json",
        "selected_topic": internal / "selected_topic.json",
        "copy_package": internal / "copy_package.md",
        "copy_package_json": internal / "copy_package.json",
        "semantic_review": internal / "semantic_review.json",
        "compliance": internal / "compliance_report.json",
        "storyboard": internal / "storyboard.json",
        "audio_locked": internal / "storyboard.audio_locked.json",
        "asset_manifest": internal / "asset_manifest.json",
        "asset_validation": internal / "asset_validation.json",
        "metadata": internal / "metadata.json",
        "visual_review": internal / "visual_review.json",
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
    bool_gate(gates, "cover_source_exists", exists(paths["cover"]), issues, "missing cover.png")
    bool_gate(gates, "publish_copy_source_exists", exists(paths["publish_copy"]), issues, "missing publish_copy.txt")

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
    aesthetic_score = 0.0
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

    storyboard_report_path = internal / "storyboard_validation.json"
    if exists(storyboard_report_path):
        bool_gate(gates, "storyboard_validation_exists", True, issues, "missing storyboard_validation.json")
        story_report = load_json(storyboard_report_path)
        evidence_ratio = float(story_report.get("evidence_runtime_ratio", 0))
        visual_score = 8.5 if story_report.get("status") == "passed" else 0.0
        sync_score = 9.0 if story_report.get("status") == "passed" else 0.0
        if story_report.get("status") != "passed":
            issues.extend(story_report.get("issues", []))
    else:
        bool_gate(gates, "storyboard_validation_exists", False, issues, "missing storyboard_validation.json")

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
            frame_report.get("status") in {"passed", "review_required"},
            issues,
            "frame_review_report.json is invalid",
        )
        warnings.extend(frame_report.get("warnings", []))
    else:
        bool_gate(gates, "frame_review_exists", False, issues, "missing frame_review_report.json")

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
        issues.extend(visual_report.get("blocking_issues", []))
        warnings.extend(visual_report.get("warnings", []))
    else:
        bool_gate(gates, "visual_review_exists", False, issues, "missing visual_review.json")

    bool_gate(gates, "not_static_image_only", evidence_ratio >= 0.5, issues, "evidence_runtime_ratio must be >= 0.5")
    bool_gate(gates, "audio_video_synced", exists(paths["audio_locked"]), issues, "audio lock is required for sync")

    status = "passed" if not issues and all(gates.values()) else "failed"
    score_values = {
        "topic_score": round(topic_score, 2),
        "first_3_seconds_score": round(first_3, 2),
        "first_5_seconds_score": round(first_5, 2),
        "script_score": round(script_score, 2),
        "semantic_score": round(semantic_score, 2),
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
