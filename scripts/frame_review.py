#!/usr/bin/env python3
"""Generate contact sheets for manual frame review."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} is required but was not found on PATH")
    return path


def run_ffmpeg(video: Path, vf: str, out: Path) -> None:
    ffmpeg = require_tool("ffmpeg")
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video),
            "-vf",
            vf,
            "-frames:v",
            "1",
            str(out),
        ],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Create contact sheets for visual review.")
    parser.add_argument("--video", required=True, help="draft.mp4 path")
    parser.add_argument("--out-dir", required=True, help="Directory for review images and report")
    parser.add_argument("--report", help="Optional frame_review_report.json path")
    args = parser.parse_args()

    video = Path(args.video)
    out_dir = Path(args.out_dir)
    issues: list[str] = []
    warnings: list[str] = ["manual visual review is still required for readability, overlap, and design quality"]
    artifacts: dict[str, str] = {}

    if not video.exists() or not video.is_file() or video.stat().st_size <= 0:
        issues.append("video file is missing or empty")
    else:
        first_5s = out_dir / "contact_sheet_first_5s.jpg"
        full_video = out_dir / "contact_sheet_full_video.jpg"
        crowded_dir = out_dir / "crowded_frames"
        crowded_sample = crowded_dir / "sample_%03d.jpg"
        run_ffmpeg(video, "trim=end=5,fps=2,scale=240:-1,tile=5x2", first_5s)
        run_ffmpeg(video, "fps=1/4,scale=180:-1,tile=4x4", full_video)
        crowded_dir.mkdir(parents=True, exist_ok=True)
        ffmpeg = require_tool("ffmpeg")
        subprocess.run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(video),
                "-vf",
                "fps=1/6,scale=1080:-1",
                "-frames:v",
                "8",
                str(crowded_sample),
            ],
            check=True,
        )
        artifacts = {
            "contact_sheet_first_5s": str(first_5s),
            "contact_sheet_full_video": str(full_video),
            "crowded_frames_dir": str(crowded_dir),
        }

    report = {
        "status": "failed" if issues else "review_required",
        "artifacts": artifacts,
        "blocking_issues": issues,
        "warnings": warnings,
    }
    report_path = Path(args.report) if args.report else out_dir / "frame_review_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
