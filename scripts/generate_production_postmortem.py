#!/usr/bin/env python3
"""Generate a production postmortem from local QA artifacts.

The postmortem is the skill's learning interface: it records observations and
candidate lessons, but it never edits hard rules automatically.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists() or path.stat().st_size == 0:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def add_unique(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def score(report: dict[str, Any], key: str) -> float:
    scores = report.get("scores", {})
    if not isinstance(scores, dict):
        return 0.0
    try:
        return float(scores.get(key, 0.0))
    except Exception:
        return 0.0


def as_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0


def first_float(report: dict[str, Any], keys: list[str]) -> float:
    for key in keys:
        value = report.get(key)
        if value is not None:
            parsed = as_float(value)
            if parsed:
                return parsed
    return 0.0


def topic_from(project: Path, storyboard: dict[str, Any]) -> str:
    selected = load_json(project / "internal" / "selected_topic.json")
    for key in ["title", "topic", "topic_title", "selected_topic"]:
        value = selected.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    title = storyboard.get("title")
    return str(title or project.name).strip()


def build_bottleneck_log(project: Path) -> dict[str, Any]:
    internal = project / "internal"
    frame_export = load_json(internal / "frame_sequence_export_report.json")
    technical = load_json(internal / "video_technical_qa.json")
    cleanup = load_json(internal / "cleanup_report.json")
    leading_repair = load_json(internal / "leading_frame_repair_report.json")

    elapsed_sec = first_float(
        frame_export,
        ["elapsed_sec", "render_elapsed_sec", "export_elapsed_sec", "duration_sec"],
    )
    video = technical.get("video") if isinstance(technical.get("video"), dict) else {}
    video_duration = as_float(video.get("duration"))
    frames_value = frame_export.get("frames") if isinstance(frame_export, dict) else None
    if isinstance(frames_value, list):
        frame_count = len(frames_value)
    else:
        frame_count = int(as_float(frame_export.get("frame_count") or frames_value or 0)) if frame_export else 0

    observations: list[str] = []
    bottlenecks: list[str] = []
    next_actions: list[str] = []

    if elapsed_sec:
        add_unique(observations, f"frame_sequence_elapsed_sec={elapsed_sec:.2f}")
    if video_duration:
        add_unique(observations, f"video_duration_sec={video_duration:.2f}")
    if frame_count:
        add_unique(observations, f"frame_count={frame_count}")
    if cleanup:
        add_unique(observations, f"cleanup_removed_count={int(cleanup.get('removed_count') or 0)}")
    if leading_repair:
        add_unique(observations, f"leading_frame_repair_action={leading_repair.get('action')}")

    long_render = elapsed_sec > 600 and (not video_duration or 60 <= video_duration <= 75)
    if long_render:
        add_unique(bottlenecks, "HyperFrames PNG sequence export exceeded 10 minutes for a normal-length AI video.")
        add_unique(next_actions, "Prefer cached background/decor layers and redraw only active foreground modules, captions, and status nodes.")
    if leading_repair.get("status") == "failed":
        add_unique(bottlenecks, "Leading-frame repair failed; frame 1 may not return to active main content.")
        add_unique(next_actions, "Inspect internal/hf_frames and restage initial scene visibility before encoding.")

    return {
        "status": "needs_optimization" if bottlenecks else "passed",
        "project": str(project),
        "observations": observations,
        "bottlenecks": bottlenecks,
        "next_actions": next_actions,
        "source_reports": [
            str(path.relative_to(project))
            for path in [
                internal / "frame_sequence_export_report.json",
                internal / "video_technical_qa.json",
                internal / "leading_frame_repair_report.json",
                internal / "cleanup_report.json",
            ]
            if path.exists()
        ],
    }


def build_postmortem(project: Path, user_feedback: str = "") -> dict[str, Any]:
    internal = project / "internal"
    storyboard = load_json(internal / "storyboard.json")
    qa = load_json(internal / "qa_report.json")
    visual = load_json(internal / "visual_review.json")
    frame = load_json(internal / "frame_review_report.json")
    story = load_json(internal / "storyboard_validation.json")
    semantic = load_json(internal / "semantic_review.json")
    screen_text = load_json(internal / "screen_text_proofread_report.json")
    empty_frame = load_json(internal / "empty_frame_report.json")
    bottleneck_log = build_bottleneck_log(project)

    observations: list[str] = []
    what_worked: list[str] = []
    what_to_fix: list[str] = []
    bottlenecks: list[str] = []
    reusable_lessons: list[str] = []
    next_run_decisions: list[str] = []
    proposed_rule_changes: list[str] = []

    qa_status = str(qa.get("status") or "missing")
    visual_score = score(qa, "visual_score") or float(visual.get("overall_visual_score") or 0.0)
    first_5 = score(qa, "first_5_seconds_score")
    proof_score = score(qa, "proof_score")
    evidence_ratio = float(qa.get("evidence_runtime_ratio") or story.get("evidence_runtime_ratio") or 0.0)

    add_unique(observations, f"qa_status={qa_status}")
    if visual_score:
        add_unique(observations, f"visual_score={visual_score:.2f}")
    if evidence_ratio:
        add_unique(observations, f"evidence_runtime_ratio={evidence_ratio:.3f}")
    if user_feedback:
        add_unique(observations, f"user_feedback={user_feedback}")

    if qa_status == "passed":
        add_unique(what_worked, "QA passed with no blocking issues.")
    else:
        add_unique(what_to_fix, "QA did not pass; fix blocking reports before final delivery.")

    if first_5 >= 9.0:
        add_unique(what_worked, "First five seconds scored strong enough for retention.")
    elif first_5:
        add_unique(what_to_fix, "First five seconds need stronger conflict, proof, or visual action.")

    if proof_score >= 8.5 or evidence_ratio >= 0.6:
        add_unique(what_worked, "Evidence density is strong enough for an AI tutorial.")
    else:
        add_unique(what_to_fix, "Increase real UI/source/test/result proof instead of abstract explanation.")
        add_unique(next_run_decisions, "Use at least one source-evidence shot and two operation-simulation shots before render.")

    visual_signals = visual.get("signals", {}) if isinstance(visual.get("signals"), dict) else {}
    if visual_signals.get("caption_template_count", 0) >= 2:
        add_unique(what_worked, "Caption templates are varied enough to avoid a single-template feel.")
    else:
        add_unique(what_to_fix, "Add caption-template variety; avoid one repeated lower-third style.")

    story_signals = story.get("signals", {}) if isinstance(story.get("signals"), dict) else {}
    if story_signals.get("director_shots_valid") is True:
        add_unique(what_worked, "Director shots passed visual diversity and operation-feel gates.")
    elif "director_shots_valid" in story_signals:
        add_unique(what_to_fix, "Director shots failed; redesign shot types, layout families, operation elements, or approved text.")

    for issue in as_list(qa.get("blocking_issues")):
        add_unique(bottlenecks, str(issue))
    for issue in as_list(visual.get("blocking_issues")):
        add_unique(bottlenecks, str(issue))
    for issue in as_list(screen_text.get("blocking_issues")):
        add_unique(bottlenecks, str(issue))
    for issue in as_list(empty_frame.get("blocking_issues")):
        add_unique(bottlenecks, str(issue))

    if frame.get("status") == "review_required":
        add_unique(bottlenecks, "Manual frame review still required for readability, overlap, and design quality.")
    for issue in as_list(bottleneck_log.get("bottlenecks")):
        add_unique(bottlenecks, str(issue))
    for observation in as_list(bottleneck_log.get("observations")):
        add_unique(observations, str(observation))
    for action in as_list(bottleneck_log.get("next_actions")):
        add_unique(next_run_decisions, str(action))

    for warning in as_list(qa.get("warnings")) + as_list(visual.get("warnings")) + as_list(story.get("warnings")):
        add_unique(observations, str(warning))

    if semantic.get("composite_score"):
        add_unique(observations, f"semantic_score={float(semantic.get('composite_score')):.2f}")

    if visual_score and visual_score < 8.5:
        add_unique(next_run_decisions, "Before HyperFrames, create a stronger visual director script with more shot variety.")
    if any("empty" in item.lower() or "空" in item for item in bottlenecks + what_to_fix):
        add_unique(next_run_decisions, "Run empty-frame and final on-screen text checks before any final promotion.")
    failure_blob = "\n".join(what_to_fix + bottlenecks + [user_feedback])
    if any(term in failure_blob for term in ["same layout", "PPT", "像PPT", "同款卡片", "模板化", "slide-deck"]):
        add_unique(next_run_decisions, "Limit identical layout families to two consecutive shots and add operation/proof closeups.")

    add_unique(reusable_lessons, "Treat the skill as execution memory; the agent must still make shot, proof, and pacing decisions.")
    add_unique(reusable_lessons, "Promote repeated postmortem lessons into hard rules only after human approval.")
    if what_to_fix:
        add_unique(proposed_rule_changes, "Review recurring fixes; convert only repeated failures into validation gates.")

    return {
        "project": str(project),
        "topic": topic_from(project, storyboard),
        "qa_status": qa_status,
        "decision_summary": "Use this postmortem as learning input for the next video; do not auto-edit hard rules.",
        "user_feedback": user_feedback,
        "observations": observations,
        "what_worked": what_worked,
        "what_to_fix": what_to_fix,
        "bottlenecks": bottlenecks,
        "reusable_lessons": reusable_lessons,
        "next_run_decisions": next_run_decisions,
        "proposed_rule_changes": proposed_rule_changes,
        "human_approval_required": True,
        "bottleneck_log": bottleneck_log,
        "source_reports": [
            str(path.relative_to(project))
            for path in [
                internal / "qa_report.json",
                internal / "visual_review.json",
                internal / "frame_review_report.json",
                internal / "storyboard_validation.json",
                internal / "screen_text_proofread_report.json",
                internal / "empty_frame_report.json",
            ]
            if path.exists()
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate production_postmortem.json from QA artifacts.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument("--out", required=True, help="production_postmortem.json path")
    parser.add_argument("--user-feedback", default="", help="Optional user feedback to fold into the postmortem.")
    args = parser.parse_args()

    report = build_postmortem(Path(args.project), args.user_feedback)
    bottleneck_out = Path(args.project) / "internal" / "production_bottleneck_log.json"
    write_json(bottleneck_out, report.get("bottleneck_log", {}))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    write_json(out, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
