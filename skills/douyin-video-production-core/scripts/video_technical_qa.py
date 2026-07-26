#!/usr/bin/env python3
"""Standalone ffprobe/ffmpeg technical QA without creative-template rules."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from artifact_fingerprint import write_report_with_fingerprints


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False)


def frame_rate(value: str) -> float:
    left, _, right = value.partition("/")
    try:
        return float(left) / float(right or 1)
    except (ValueError, ZeroDivisionError):
        return 0.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--fps", type=float)
    parser.add_argument("--min-size-bytes", type=int, default=200_000)
    parser.add_argument("--max-duration-gap", type=float, default=0.35)
    args = parser.parse_args()

    video = Path(args.video).resolve()
    issues: list[str] = []
    if not video.is_file() or video.stat().st_size < args.min_size_bytes:
        issues.append(f"video missing or smaller than {args.min_size_bytes} bytes: {video}")
        data = {}
    elif not shutil.which("ffprobe"):
        issues.append("ffprobe is unavailable")
        data = {}
    else:
        result = run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(video)])
        if result.returncode:
            issues.append(result.stderr.strip() or "ffprobe failed")
            data = {}
        else:
            data = json.loads(result.stdout)

    streams = data.get("streams") or []
    vstream = next((item for item in streams if item.get("codec_type") == "video"), {})
    astream = next((item for item in streams if item.get("codec_type") == "audio"), {})
    fmt = data.get("format") or {}
    width = int(vstream.get("width") or 0)
    height = int(vstream.get("height") or 0)
    fps = frame_rate(str(vstream.get("avg_frame_rate") or "0/1"))
    duration = float(fmt.get("duration") or vstream.get("duration") or 0)
    audio_duration = float(astream.get("duration") or duration or 0)
    if args.width and width != args.width:
        issues.append(f"width must be {args.width}, got {width}")
    if args.height and height != args.height:
        issues.append(f"height must be {args.height}, got {height}")
    if args.fps and abs(fps - args.fps) > 0.2:
        issues.append(f"fps must be {args.fps}, got {fps:.3f}")
    if not vstream:
        issues.append("video stream is missing")
    if not astream:
        issues.append("audio stream is missing")
    if abs(duration - audio_duration) > args.max_duration_gap:
        issues.append(f"audio/video duration gap exceeds {args.max_duration_gap}s")

    report = {
        "status": "passed" if not issues else "blocked",
        "video": str(video),
        "video_stream": {
            "width": width,
            "height": height,
            "fps": round(fps, 3),
            "duration": round(duration, 3),
        },
        "audio": {"has_audio": bool(astream), "duration": round(audio_duration, 3)},
        "blocking_issues": issues,
    }
    if video.is_file():
        write_report_with_fingerprints(report, [video])
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
