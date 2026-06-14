#!/usr/bin/env python3
"""Run the V3 pipeline checks in order."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def exists(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def qa_only(project: Path, promote: bool = False) -> None:
    internal = project / "internal"
    if exists(internal / "topic_candidates.json"):
        run([sys.executable, "scripts/score_topic.py", "--input", str(internal / "topic_candidates.json"), "--out", str(internal / "topic_candidates.scored.json")])
    if exists(internal / "copy_package.md"):
        copy_json = internal / "copy_package.json"
        run([sys.executable, "scripts/score_script.py", "--copy", str(internal / "copy_package.md"), "--out", str(internal / "script_score.json")])
        run([sys.executable, "scripts/check_public_copy.py", "--copy", str(internal / "copy_package.md"), "--out", str(internal / "compliance_report.json")])
        semantic_cmd = [sys.executable, "scripts/evaluate_copy_semantic.py", "--copy", str(internal / "copy_package.md"), "--out", str(internal / "semantic_review.json")]
        if exists(copy_json):
            semantic_cmd.extend(["--copy-json", str(copy_json)])
        run(semantic_cmd)
    if exists(internal / "storyboard.json"):
        run([sys.executable, "scripts/validate_storyboard.py", "--storyboard", str(internal / "storyboard.json"), "--out", str(internal / "storyboard_validation.json")])
    if exists(internal / "asset_manifest.json"):
        run([sys.executable, "scripts/validate_assets.py", "--manifest", str(internal / "asset_manifest.json"), "--project", str(project), "--out", str(internal / "asset_validation.json")])
    if exists(internal / "draft.mp4") and exists(internal / "metadata.json"):
        run([sys.executable, "scripts/video_technical_qa.py", "--video", str(internal / "draft.mp4"), "--metadata", str(internal / "metadata.json"), "--out", str(internal / "video_technical_qa.json")])
        run([sys.executable, "scripts/frame_review.py", "--video", str(internal / "draft.mp4"), "--out-dir", str(internal / "frame_review"), "--report", str(internal / "frame_review_report.json")])
    if exists(internal / "storyboard.json") and exists(internal / "frame_review_report.json") and exists(internal / "metadata.json"):
        run([sys.executable, "scripts/visual_aesthetic_review.py", "--storyboard", str(internal / "storyboard.json"), "--frame-review", str(internal / "frame_review_report.json"), "--metadata", str(internal / "metadata.json"), "--out", str(internal / "visual_review.json")])
    run([sys.executable, "scripts/qa_gate.py", "--project", str(project), "--out", str(internal / "qa_report.json")])
    if promote:
        run([sys.executable, "scripts/promote_final.py", "--project", str(project)])


def main() -> int:
    parser = argparse.ArgumentParser(description="Run V3 pipeline checks.")
    parser.add_argument("--project", help="outputs/<date-topic> project path")
    parser.add_argument("--mode", choices=["qa-only", "golden", "full"], default="qa-only")
    args = parser.parse_args()

    if args.mode == "golden":
        run([sys.executable, "scripts/check_golden_project.py"])
        return 0
    if not args.project:
        parser.error("--project is required for qa-only and full modes")
    qa_only(Path(args.project), promote=args.mode == "full")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
