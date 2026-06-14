#!/usr/bin/env python3
"""Run the V3 golden project through deterministic gates."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "golden_ai_prompt_case"


def run(command: list[str], cwd: Path = ROOT) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def ensure_media(project: Path) -> None:
    internal = project / "internal"
    draft = internal / "draft.mp4"
    cover = internal / "cover.png"
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required for golden project media synthesis")
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "testsrc2=size=1080x1920:rate=30:duration=18",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=720:duration=18",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-shortest",
            str(draft),
        ]
    )
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(draft),
            "-frames:v",
            "1",
            str(cover),
        ]
    )


def check_expected(report: dict[str, object], expected: dict[str, object]) -> list[str]:
    issues: list[str] = []
    if report.get("status") != expected.get("status"):
        issues.append(f"status mismatch: {report.get('status')} != {expected.get('status')}")
    if report.get("quality_level") not in {"high_quality", "breakout_potential"}:
        issues.append(f"quality_level is not high enough: {report.get('quality_level')}")
    scores = report.get("scores", {})
    minimums = expected.get("minimum_scores", {})
    if isinstance(scores, dict) and isinstance(minimums, dict):
        for key, value in minimums.items():
            actual = float(scores.get(key, 0))
            if actual < float(value):
                issues.append(f"{key} {actual} < {value}")
    if report.get("blocking_issues"):
        issues.append("qa_report has blocking issues")
    return issues


def run_golden(project: Path, promote: bool = False) -> dict[str, object]:
    internal = project / "internal"
    run([sys.executable, "scripts/score_topic.py", "--input", str(internal / "topic_candidates.json"), "--out", str(internal / "topic_candidates.json"), "--learning-bank", str(ROOT / "references" / "learning_bank.md")])
    run([sys.executable, "scripts/score_script.py", "--copy", str(internal / "copy_package.md"), "--out", str(internal / "script_score.json")])
    run([sys.executable, "scripts/evaluate_copy_semantic.py", "--copy", str(internal / "copy_package.md"), "--copy-json", str(internal / "copy_package.json"), "--out", str(internal / "semantic_review.json")])
    run([sys.executable, "scripts/check_public_copy.py", "--copy", str(internal / "copy_package.md"), "--out", str(internal / "compliance_report.json")])
    run([sys.executable, "scripts/validate_storyboard.py", "--storyboard", str(internal / "storyboard.json"), "--out", str(internal / "storyboard_validation.json")])
    shutil.copy2(internal / "storyboard.json", internal / "storyboard.audio_locked.json")
    run([sys.executable, "scripts/validate_assets.py", "--manifest", str(internal / "asset_manifest.json"), "--project", str(project), "--out", str(internal / "asset_validation.json")])
    ensure_media(project)
    run([sys.executable, "scripts/video_technical_qa.py", "--video", str(internal / "draft.mp4"), "--metadata", str(internal / "metadata.json"), "--out", str(internal / "video_technical_qa.json")])
    run([sys.executable, "scripts/frame_review.py", "--video", str(internal / "draft.mp4"), "--out-dir", str(internal / "frame_review"), "--report", str(internal / "frame_review_report.json")])
    run([sys.executable, "scripts/visual_aesthetic_review.py", "--storyboard", str(internal / "storyboard.json"), "--frame-review", str(internal / "frame_review_report.json"), "--metadata", str(internal / "metadata.json"), "--out", str(internal / "visual_review.json")])
    run([sys.executable, "scripts/qa_gate.py", "--project", str(project), "--out", str(internal / "qa_report.json")])
    if promote:
        run([sys.executable, "scripts/promote_final.py", "--project", str(project)])
    return json.loads((internal / "qa_report.json").read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the bundled V3 golden project.")
    parser.add_argument("--project", help="Optional output project path. Defaults to a temporary copy.")
    parser.add_argument("--promote", action="store_true", help="Also run promote_final.py after QA passes.")
    args = parser.parse_args()

    expected = json.loads((EXAMPLE / "expected_qa_report.json").read_text(encoding="utf-8"))
    if args.project:
        project = Path(args.project)
        if project.exists():
            shutil.rmtree(project)
        shutil.copytree(EXAMPLE, project)
        report = run_golden(project, promote=args.promote)
    else:
        with tempfile.TemporaryDirectory(prefix="douyin-golden-") as tmp:
            project = Path(tmp) / "golden_ai_prompt_case"
            shutil.copytree(EXAMPLE, project)
            report = run_golden(project, promote=args.promote)

    issues = check_expected(report, expected)
    result = {
        "status": "passed" if not issues else "failed",
        "quality_level": report.get("quality_level"),
        "scores": report.get("scores", {}),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
