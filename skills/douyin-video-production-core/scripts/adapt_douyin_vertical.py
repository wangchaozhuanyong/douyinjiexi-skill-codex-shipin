#!/usr/bin/env python3
"""Create an optional 9:16 Douyin adaptation without cropping the 16:9 proof master."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def load_json(path: Path) -> dict[str, Any]:
    if not exists(path):
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def adapt(project: Path, source: Path | None = None) -> dict[str, Any]:
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is required for vertical adaptation")
    final = project / "final"
    internal = project / "internal"
    input_video = source or final / "final.mp4"
    if not exists(input_video):
        input_video = internal / "draft.mp4"
    if not exists(input_video):
        raise SystemExit(f"source video missing or empty: {input_video}")

    out_video = final / "final_douyin_9x16.mp4"
    final.mkdir(parents=True, exist_ok=True)
    filter_graph = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        "boxblur=24:2,eq=brightness=-0.08:saturation=0.75[bg];"
        "[0:v]scale=1080:-2[proof];"
        "[bg][proof]overlay=(W-w)/2:(H-h)/2"
    )
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(input_video),
            "-filter_complex",
            filter_graph,
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "copy",
            str(out_video),
        ]
    )
    source_metadata = load_json(internal / "metadata.json")
    vertical_metadata = {
        **source_metadata,
        "target_width": 1080,
        "target_height": 1920,
        "width": 1080,
        "height": 1920,
        "adaptation": {
            "status": "enabled",
            "created_at": now_iso(),
            "source_video": str(input_video),
            "strategy": "centered_16x9_proof_panel_no_crop",
            "requires_separate_qa": True,
        },
    }
    metadata_path = final / "vertical_metadata.json"
    metadata_path.write_text(json.dumps(vertical_metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    qa_path = final / "vertical_video_technical_qa.json"
    run([
        sys.executable,
        str(Path(__file__).with_name("video_technical_qa.py")),
        "--video",
        str(out_video),
        "--width",
        "1080",
        "--height",
        "1920",
        "--out",
        str(qa_path),
    ])
    frame_dir = final / "vertical_frame_review"
    frame_report = final / "vertical_frame_review_report.json"
    run(
        [
            sys.executable,
            str(Path(__file__).with_name("frame_review.py")),
            "--video",
            str(out_video),
            "--out-dir",
            str(frame_dir),
            "--report",
            str(frame_report),
        ]
    )
    return {
        "status": "passed",
        "video": str(out_video),
        "metadata": str(metadata_path),
        "technical_qa": str(qa_path),
        "frame_review": str(frame_report),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Optionally adapt a proof-master video to Douyin 9:16.")
    parser.add_argument("--project", required=True)
    parser.add_argument("--source")
    parser.add_argument("--enable-vertical-adaptation", action="store_true")
    args = parser.parse_args()
    if not args.enable_vertical_adaptation:
        print(json.dumps({"status": "disabled"}, ensure_ascii=False))
        return 0
    result = adapt(Path(args.project), Path(args.source) if args.source else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
