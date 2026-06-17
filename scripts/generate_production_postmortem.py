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


def topic_from(project: Path, storyboard: dict[str, Any]) -> str:
    selected = load_json(project / "internal" / "selected_topic.json")
    for key in ["title", "topic", "topic_title", "selected_topic"]:
        value = selected.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    title = storyboard.get("title")
    return str(title or project.name).strip()


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
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
