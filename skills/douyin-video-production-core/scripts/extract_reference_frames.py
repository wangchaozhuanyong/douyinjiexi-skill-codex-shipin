#!/usr/bin/env python3
"""Extract reference video frames and a contact sheet."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Optional


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} is required but was not found on PATH")
    return path


def run_json(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def probe_video(input_path: Path) -> dict[str, Any]:
    ffprobe = require_tool("ffprobe")
    data = run_json(
        [
            ffprobe,
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(input_path),
        ]
    )
    video_stream = next((item for item in data.get("streams", []) if item.get("codec_type") == "video"), {})
    duration = float(data.get("format", {}).get("duration") or video_stream.get("duration") or 0)
    width = int(video_stream.get("width") or 0)
    height = int(video_stream.get("height") or 0)
    fps_text = str(video_stream.get("avg_frame_rate") or video_stream.get("r_frame_rate") or "0/1")
    numerator, _, denominator = fps_text.partition("/")
    fps = float(numerator or 0) / float(denominator or 1)
    return {
        "duration_seconds": round(duration, 3),
        "width": width,
        "height": height,
        "fps": round(fps, 3),
        "aspect_ratio": f"{width}:{height}" if width and height else "unknown",
    }


def extract_frames(input_path: Path, out_dir: Path, interval: float) -> list[str]:
    ffmpeg = require_tool("ffmpeg")
    out_dir.mkdir(parents=True, exist_ok=True)
    pattern = out_dir / "frame_%04d.jpg"
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(input_path),
            "-vf",
            f"fps=1/{interval}",
            "-q:v",
            "2",
            str(pattern),
        ],
        check=True,
    )
    return [path.name for path in sorted(out_dir.glob("frame_*.jpg"))]


def build_contact_sheet(out_dir: Path) -> Optional[str]:
    ffmpeg = require_tool("ffmpeg")
    frames = sorted(out_dir.glob("frame_*.jpg"))
    if not frames:
        return None
    contact_sheet = out_dir / "contact_sheet.jpg"
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-pattern_type",
            "glob",
            "-i",
            str(out_dir / "frame_*.jpg"),
            "-vf",
            "scale=240:-1,tile=4x4",
            "-frames:v",
            "1",
            str(contact_sheet),
        ],
        check=True,
    )
    return contact_sheet.name


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract frames from a local reference video.")
    parser.add_argument("--input", required=True, help="Local reference video path.")
    parser.add_argument("--out", required=True, help="Output directory for frames and metadata.")
    parser.add_argument("--interval", type=float, default=1.0, help="Seconds between sampled frames.")
    args = parser.parse_args()

    input_path = Path(args.input).expanduser()
    if not input_path.exists() or not input_path.is_file():
        raise SystemExit(f"input video not found: {input_path}")
    if args.interval <= 0:
        raise SystemExit("--interval must be greater than 0")

    out_dir = Path(args.out)
    metadata = probe_video(input_path)
    frames = extract_frames(input_path, out_dir, args.interval)
    contact_sheet = build_contact_sheet(out_dir)
    metadata.update(
        {
            "input": str(input_path),
            "interval_seconds": args.interval,
            "frame_count": len(frames),
            "frames": frames,
            "contact_sheet": contact_sheet,
        }
    )
    (out_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0 if frames and contact_sheet else 1


if __name__ == "__main__":
    raise SystemExit(main())
