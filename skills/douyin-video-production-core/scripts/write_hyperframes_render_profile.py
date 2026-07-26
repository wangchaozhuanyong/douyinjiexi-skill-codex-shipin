#!/usr/bin/env python3
"""Write the stable HyperFrames PNG-sequence render profile for a project."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_PROFILE: dict[str, Any] = {
    "render_mode": "png_sequence",
    "render_target": "project_directory",
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "worker_count": 1,
    "max_worker_count": 1,
    "protocol_timeout_ms": 900000,
    "page_ready_timeout_ms": 120000,
    "frame_timeout_ms": 120000,
    "retry_policy": "retry_serial_worker_once_after_timeout",
    "output_frames_dir": "internal/hf_frames",
    "post_render_required": [
        "scripts/repair_hyperframes_leading_frames.py",
        "ffmpeg_h264_aac_encode",
        "frame_zero_cover_overlay",
        "ffprobe",
    ],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_profile(project: Path, composition_entry: str, out_frames: str | None = None) -> dict[str, Any]:
    profile = dict(DEFAULT_PROFILE)
    profile["render_target"] = "project_directory"
    if out_frames:
        profile["output_frames_dir"] = out_frames

    worker_count = int(profile.get("worker_count") or 1)
    max_worker_count = int(profile.get("max_worker_count") or worker_count)
    protocol_timeout = int(profile.get("protocol_timeout_ms") or 0)
    issues: list[str] = []
    if str(profile.get("render_mode")) != "png_sequence":
        issues.append("render_mode must be png_sequence")
    if str(profile.get("render_target")) != "project_directory":
        issues.append("render_target must be project_directory")
    if worker_count > max_worker_count or max_worker_count > 1:
        issues.append("PNG screenshot render profile must use the serial stable worker route by default")
    if protocol_timeout < 900000:
        issues.append("protocol_timeout_ms must be at least 900000 for long 1920x1080 screenshot sequences")

    output_frames_dir = str(profile.get("output_frames_dir") or "internal/hf_frames")
    output_path = Path(output_frames_dir)
    if not output_path.is_absolute():
        output_path = project / output_path

    command_template = [
        "npx",
        "--yes",
        "hyperframes",
        "render",
        "--format",
        "png-sequence",
        "--fps",
        str(int(profile.get("fps") or 30)),
        "--protocol-timeout",
        str(protocol_timeout),
        "--workers",
        str(worker_count),
        "--output",
        str(output_path),
    ]

    return {
        "status": "passed" if not issues else "failed",
        "created_at": now_iso(),
        "project": str(project),
        "render_target": "project_directory",
        "command_cwd": str(project),
        "composition_entry": composition_entry,
        "profile": profile,
        "command_template": command_template,
        "output_frames_dir": str(output_path),
        "blocking_issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create internal/hyperframes_render_profile.json.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument(
        "--entry",
        default="index.html",
        help="Recorded composition source path only. Render runs from the project directory.",
    )
    parser.add_argument("--out-frames", help="Override output frame directory")
    parser.add_argument("--out", help="Defaults to <project>/internal/hyperframes_render_profile.json")
    args = parser.parse_args()

    project = Path(args.project)
    report = build_profile(project, args.entry, args.out_frames)
    out = Path(args.out) if args.out else project / "internal" / "hyperframes_render_profile.json"
    write_json(out, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
