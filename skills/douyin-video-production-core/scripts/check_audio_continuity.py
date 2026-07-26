#!/usr/bin/env python3
"""Check final video audio duration and locked scene audio continuity."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from artifact_fingerprint import write_report_with_fingerprints


DEFAULT_MAX_DURATION_GAP = 0.3
DEFAULT_MAX_TRANSITION_GAP_MS = 120


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
        raise RuntimeError(result.stderr.strip() or f"ffprobe failed for {path}")
    return json.loads(result.stdout)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_project_path(raw_path: str, lock_path: Path) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    if lock_path.parent.name == "internal":
        return lock_path.parents[1] / path
    return lock_path.parent / path


def check_scene_gaps(scene_audio: list[dict[str, Any]], max_gap_ms: int) -> tuple[list[dict[str, Any]], list[str]]:
    gaps: list[dict[str, Any]] = []
    issues: list[str] = []
    ordered = sorted(scene_audio, key=lambda item: float(item.get("start", 0)))
    for previous, current in zip(ordered, ordered[1:]):
        previous_end = float(previous.get("end") or 0)
        current_start = float(current.get("start") or 0)
        gap_ms = int(round((current_start - previous_end) * 1000))
        allowed = min(int(previous.get("max_audio_gap_ms") or max_gap_ms), int(current.get("max_audio_gap_ms") or max_gap_ms), max_gap_ms)
        gap = {
            "from_scene_id": previous.get("scene_id"),
            "to_scene_id": current.get("scene_id"),
            "gap_ms": gap_ms,
            "allowed_gap_ms": allowed,
        }
        gaps.append(gap)
        if gap_ms > allowed:
            issues.append(
                f"audio gap between {previous.get('scene_id')} and {current.get('scene_id')} is {gap_ms}ms; must be <= {allowed}ms"
            )
    return gaps, issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check continuous narration against storyboard.audio_locked.json.")
    parser.add_argument("--video", required=True, help="Final or draft MP4 path")
    parser.add_argument("--lock", required=True, help="storyboard.audio_locked.json path")
    parser.add_argument("--out", required=True, help="audio_continuity_report.json output path")
    parser.add_argument("--max-duration-gap", type=float, default=DEFAULT_MAX_DURATION_GAP)
    parser.add_argument("--max-transition-gap-ms", type=int, default=DEFAULT_MAX_TRANSITION_GAP_MS)
    args = parser.parse_args()

    video = Path(args.video)
    lock_path = Path(args.lock)
    out = Path(args.out)
    issues: list[str] = []
    warnings: list[str] = []

    if not video.exists() or video.stat().st_size <= 0:
        issues.append("video file is missing or empty")
        probe_data: dict[str, Any] = {}
    else:
        probe_data = probe(video)

    if not lock_path.exists() or lock_path.stat().st_size <= 0:
        issues.append("storyboard audio lock is missing or empty")
        lock: dict[str, Any] = {}
    else:
        lock = load_json(lock_path)

    streams = probe_data.get("streams", []) if probe_data else []
    fmt = probe_data.get("format", {}) if probe_data else {}
    video_stream = next((item for item in streams if item.get("codec_type") == "video"), {})
    audio_stream = next((item for item in streams if item.get("codec_type") == "audio"), {})
    video_duration = float(video_stream.get("duration") or fmt.get("duration") or 0)
    audio_duration = float(audio_stream.get("duration") or 0)

    if probe_data and not audio_stream:
        issues.append("audio stream is missing")
    elif probe_data and abs(video_duration - audio_duration) > args.max_duration_gap:
        issues.append("audio/video duration gap exceeds threshold")

    audio_lock = lock.get("audio_lock", {}) if isinstance(lock.get("audio_lock"), dict) else {}
    scene_audio = audio_lock.get("scene_audio", []) if isinstance(audio_lock.get("scene_audio"), list) else []
    if not scene_audio:
        issues.append("audio_lock.scene_audio is required")
    gaps, gap_issues = check_scene_gaps(scene_audio, args.max_transition_gap_ms)
    issues.extend(gap_issues)

    root_path_raw = str(audio_lock.get("root_narration_path", "")).strip()
    if root_path_raw:
        root_path = resolve_project_path(root_path_raw, lock_path)
        if not root_path.exists() or root_path.stat().st_size <= 0:
            issues.append(f"root narration audio file is missing or empty: {root_path_raw}")
    else:
        issues.append("audio_lock.root_narration_path is required")

    try:
        expected_duration = float(audio_lock.get("final_audio_duration") or audio_lock.get("total_audio_duration") or 0)
    except Exception:
        expected_duration = 0.0
    if expected_duration and audio_duration and abs(expected_duration - audio_duration) > args.max_duration_gap:
        warnings.append("final video audio duration differs from audio_lock expected duration")

    report = {
        "status": "passed" if not issues else "failed",
        "video": {
            "duration": round(video_duration, 3),
        },
        "audio": {
            "has_audio": bool(audio_stream),
            "duration": round(audio_duration, 3),
            "duration_gap": round(abs(video_duration - audio_duration), 3) if audio_stream else None,
        },
        "audio_lock": {
            "root_narration_path": root_path_raw,
            "scene_count": len(scene_audio),
            "expected_duration": round(expected_duration, 3),
            "transition_gaps": gaps,
        },
        "blocking_issues": issues,
        "warnings": warnings,
    }
    input_paths: list[Path] = [video, lock_path]
    if root_path_raw:
        root_path = resolve_project_path(root_path_raw, lock_path)
        if root_path.exists() and root_path.is_file():
            input_paths.append(root_path)
    write_report_with_fingerprints(report, input_paths)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
