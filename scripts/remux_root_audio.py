#!/usr/bin/env python3
"""Replace a video's audio stream with the continuous root narration track."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} is required but was not found on PATH")
    return path


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Remux a draft video with continuous root narration audio.")
    parser.add_argument("--video", required=True, help="Input video path")
    parser.add_argument("--audio", required=True, help="Continuous narration audio path")
    parser.add_argument("--out", required=True, help="Output video path")
    args = parser.parse_args()

    video = Path(args.video)
    audio = Path(args.audio)
    out = Path(args.out)
    issues: list[str] = []
    if not video.exists() or video.stat().st_size <= 0:
        issues.append(f"input video missing or empty: {video}")
    if not audio.exists() or audio.stat().st_size <= 0:
        issues.append(f"input audio missing or empty: {audio}")
    if issues:
        raise SystemExit("\n".join(issues))

    ffmpeg = require_tool("ffmpeg")
    out.parent.mkdir(parents=True, exist_ok=True)
    result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(out),
        ]
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "ffmpeg remux failed")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
