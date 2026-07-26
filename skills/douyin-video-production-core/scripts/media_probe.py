#!/usr/bin/env python3
"""Probe audio/video duration with ffprobe when available."""

from __future__ import annotations

import argparse
import json
import subprocess
import wave
from pathlib import Path
from typing import Any


def ffprobe(path: Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,sample_rate,channels,width,height",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    duration = float(data.get("format", {}).get("duration") or 0)
    streams = data.get("streams", [])
    return {"duration_seconds": round(duration, 3), "streams": streams}


def wave_probe(path: Path) -> dict[str, Any]:
    with wave.open(str(path), "rb") as handle:
        frames = handle.getnframes()
        rate = handle.getframerate()
        return {
            "duration_seconds": round(frames / float(rate), 3),
            "streams": [{"codec_type": "audio", "sample_rate": rate, "channels": handle.getnchannels()}],
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe media duration.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--audio")
    group.add_argument("--video")
    parser.add_argument("--out")
    args = parser.parse_args()

    path = Path(args.audio or args.video)
    if not path.exists():
        raise SystemExit(f"Missing media file: {path}")
    try:
        probed = ffprobe(path)
    except Exception:
        if path.suffix.lower() == ".wav":
            probed = wave_probe(path)
        else:
            raise
    result = {"path": str(path), **probed}
    if args.out:
        Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
