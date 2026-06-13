#!/usr/bin/env python3
"""Technical QA for rendered draft videos."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} is required but was not found on PATH")
    return path


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def probe(path: Path) -> dict[str, Any]:
    ffprobe = require_tool("ffprobe")
    result = run(
        [
            ffprobe,
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe failed")
    return json.loads(result.stdout)


def frame_rate(value: str) -> float:
    numerator, _, denominator = value.partition("/")
    try:
        return round(float(numerator or 0) / float(denominator or 1), 3)
    except Exception:
        return 0.0


def detect_filter(video: Path, filter_name: str, filter_arg: str) -> list[str]:
    ffmpeg = require_tool("ffmpeg")
    result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-vf",
            f"{filter_name}={filter_arg}",
            "-an",
            "-f",
            "null",
            "-",
        ]
    )
    lines = (result.stderr or "").splitlines()
    return [line for line in lines if filter_name in line]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check draft.mp4 technical quality.")
    parser.add_argument("--video", required=True, help="draft.mp4 path")
    parser.add_argument("--out", required=True, help="video_technical_qa.json path")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--max-duration-gap", type=float, default=0.3)
    parser.add_argument("--min-bitrate", type=int, default=3500000)
    args = parser.parse_args()

    video_path = Path(args.video)
    issues: list[str] = []
    warnings: list[str] = []
    if not video_path.exists() or not video_path.is_file() or video_path.stat().st_size <= 0:
        issues.append("video file is missing or empty")
        data: dict[str, Any] = {}
    else:
        data = probe(video_path)

    streams = data.get("streams", []) if data else []
    video_stream = next((item for item in streams if item.get("codec_type") == "video"), {})
    audio_stream = next((item for item in streams if item.get("codec_type") == "audio"), {})
    fmt = data.get("format", {}) if data else {}

    width = int(video_stream.get("width") or 0)
    height = int(video_stream.get("height") or 0)
    fps = frame_rate(str(video_stream.get("avg_frame_rate") or video_stream.get("r_frame_rate") or "0/1"))
    video_duration = float(video_stream.get("duration") or fmt.get("duration") or 0)
    audio_duration = float(audio_stream.get("duration") or 0)
    bitrate = int(float(fmt.get("bit_rate") or 0))

    if width != args.width or height != args.height:
        issues.append(f"resolution must be {args.width}x{args.height}, got {width}x{height}")
    if fps <= 0:
        issues.append("fps could not be detected")
    if not audio_stream:
        issues.append("audio stream is missing")
    elif abs(video_duration - audio_duration) > args.max_duration_gap:
        issues.append("audio/video duration gap exceeds threshold")
    if bitrate and bitrate < args.min_bitrate:
        warnings.append("average bitrate is below the recommended threshold")
    if video_path.exists() and video_path.stat().st_size < 500_000:
        warnings.append("file size is unusually small for a publish-ready video")

    black_events: list[str] = []
    freeze_events: list[str] = []
    if video_path.exists() and video_path.stat().st_size > 0 and shutil.which("ffmpeg"):
        black_events = detect_filter(video_path, "blackdetect", "d=0.4:pic_th=0.98")
        freeze_events = detect_filter(video_path, "freezedetect", "n=0.003:d=1.5")
        if black_events:
            issues.append("possible long black-screen section detected")
        if freeze_events:
            warnings.append("possible frozen-frame section detected")
    else:
        warnings.append("ffmpeg not found; black/frozen frame checks skipped")

    report = {
        "status": "passed" if not issues else "failed",
        "video": {
            "width": width,
            "height": height,
            "fps": fps,
            "duration": round(video_duration, 3),
            "bitrate": bitrate,
            "file_size_bytes": video_path.stat().st_size if video_path.exists() else 0,
        },
        "audio": {
            "has_audio": bool(audio_stream),
            "duration": round(audio_duration, 3),
            "duration_gap": round(abs(video_duration - audio_duration), 3) if audio_stream else None,
        },
        "detectors": {
            "black_events": black_events,
            "freeze_events": freeze_events,
        },
        "blocking_issues": issues,
        "warnings": warnings,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
