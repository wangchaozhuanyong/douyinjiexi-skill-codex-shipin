#!/usr/bin/env python3
"""Technical QA for rendered draft videos."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from artifact_fingerprint import write_report_with_fingerprints


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


def detect_white(video: Path) -> list[str]:
    ffmpeg = require_tool("ffmpeg")
    result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-vf",
            "negate,blackdetect=d=0.4:pic_th=0.98",
            "-an",
            "-f",
            "null",
            "-",
        ]
    )
    return [line for line in (result.stderr or "").splitlines() if "blackdetect" in line]


def detect_silence(video: Path, duration: float) -> list[str]:
    ffmpeg = require_tool("ffmpeg")
    result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostats",
            "-i",
            str(video),
            "-af",
            f"silencedetect=n=-45dB:d={duration}",
            "-vn",
            "-f",
            "null",
            "-",
        ]
    )
    return [line for line in (result.stderr or "").splitlines() if "silence_" in line]


def silence_duration_seconds(line: str) -> float | None:
    match = re.search(r"silence_duration:\s*([0-9.]+)", line)
    if not match:
        return None
    try:
        return float(match.group(1))
    except ValueError:
        return None


def check_metadata(metadata_path: Path, width: int, height: int, fps: float, duration: float, bitrate: int) -> list[str]:
    issues: list[str] = []
    if not metadata_path.exists() or not metadata_path.is_file() or metadata_path.stat().st_size <= 0:
        issues.append("metadata file is missing or empty")
        return issues
    data = json.loads(metadata_path.read_text(encoding="utf-8"))
    expected_width = int(data.get("target_width") or 0)
    expected_height = int(data.get("target_height") or 0)
    expected_fps = float(data.get("fps") or 0)
    expected_duration = float(data.get("duration") or 0)
    tts_speed = data.get("tts_speed")
    if expected_width and expected_width != width:
        issues.append(f"metadata target_width mismatch: {expected_width} != {width}")
    if expected_height and expected_height != height:
        issues.append(f"metadata target_height mismatch: {expected_height} != {height}")
    if expected_fps and abs(expected_fps - fps) > 0.1:
        issues.append(f"metadata fps mismatch: {expected_fps} != {fps}")
    if expected_duration and abs(expected_duration - duration) > 0.5:
        issues.append("metadata duration mismatch")
    try:
        speed = float(tts_speed)
    except Exception:
        issues.append("metadata tts_speed is missing")
    else:
        approval_text = " ".join(
            [
                str(data.get("voice_speed_policy", "")),
                str(data.get("voice_speed_approval", "")),
                str(data.get("voice", {}).get("approval_status", "") if isinstance(data.get("voice"), dict) else ""),
                str(data.get("voice", {}).get("notes", "") if isinstance(data.get("voice"), dict) else ""),
            ]
        ).lower()
        has_user_approval = any(
            marker in approval_text
            for marker in ["user requested", "user approved", "explicit user", "用户要求", "用户明确", "用户批准"]
        )
        if not (0.95 <= speed <= 1.03 or (1.03 < speed <= 1.10 and has_user_approval)):
            issues.append("metadata tts_speed must be 0.95-1.03 by default, or <=1.10 only with explicit user approval documented")
    quality_spec = data.get("quality_spec")
    if not isinstance(quality_spec, dict):
        issues.append("metadata quality_spec is missing")
    else:
        if str(quality_spec.get("target_quality_level", "")).strip() not in {"high_quality", "breakout_potential"}:
            issues.append("metadata quality_spec.target_quality_level must be high_quality or breakout_potential")
        if str(quality_spec.get("render_quality", "")).strip() not in {
            "hyperframes_high",
            "high_bitrate_h264",
            "hyperframes_high_plus_remux",
        }:
            issues.append("metadata quality_spec.render_quality must document a high-quality render policy")
        try:
            declared_min_bitrate = int(quality_spec.get("min_bitrate", 0))
        except Exception:
            declared_min_bitrate = 0
        if declared_min_bitrate < 3_500_000:
            issues.append("metadata quality_spec.min_bitrate must be at least 3500000")
        if bitrate and declared_min_bitrate and bitrate < declared_min_bitrate:
            issues.append("video bitrate is below metadata quality_spec.min_bitrate")
        for key in [
            "source_asset_policy",
            "sfx_policy",
            "cover_policy",
            "frame_review_policy",
            "narration_continuity_policy",
        ]:
            if not str(quality_spec.get(key, "")).strip():
                issues.append(f"metadata quality_spec.{key} is required")
        narration_policy = str(quality_spec.get("narration_continuity_policy", "")).strip().lower()
        if narration_policy and not (
            "continuous" in narration_policy and ("transition" in narration_policy or "root narration" in narration_policy)
        ):
            issues.append("metadata quality_spec.narration_continuity_policy must describe continuous narration through transitions")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Check draft.mp4 technical quality.")
    parser.add_argument("--video", required=True, help="draft.mp4 path")
    parser.add_argument("--out", required=True, help="video_technical_qa.json path")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--max-duration-gap", type=float, default=0.3)
    parser.add_argument("--min-bitrate", type=int, default=3500000)
    parser.add_argument("--min-size-bytes", type=int, default=500_000)
    parser.add_argument("--max-silence-gap-ms", type=int, default=120)
    parser.add_argument("--metadata", help="Optional metadata.json path for consistency checks")
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
        issues.append("average bitrate is below the required threshold")
    if video_path.exists() and video_path.stat().st_size < args.min_size_bytes:
        issues.append("file size is unusually small for a publish-ready video")

    black_events: list[str] = []
    white_events: list[str] = []
    freeze_events: list[str] = []
    silence_events: list[str] = []
    if video_path.exists() and video_path.stat().st_size > 0 and shutil.which("ffmpeg"):
        black_events = detect_filter(video_path, "blackdetect", "d=0.4:pic_th=0.98")
        white_events = detect_white(video_path)
        freeze_events = detect_filter(video_path, "freezedetect", "n=0.003:d=1.5")
        silence_threshold = max(0.001, args.max_silence_gap_ms / 1000.0)
        if audio_stream:
            silence_events = detect_silence(video_path, silence_threshold)
        if black_events:
            issues.append("possible long black-screen section detected")
        if white_events:
            issues.append("possible long white-screen section detected")
        if freeze_events:
            issues.append("possible frozen-frame section detected")
        long_silences = [
            line
            for line in silence_events
            if (silence_duration_seconds(line) or 0.0) * 1000 > args.max_silence_gap_ms
        ]
        if long_silences:
            issues.append(f"narration silence gap exceeds {args.max_silence_gap_ms}ms")
    else:
        warnings.append("ffmpeg not found; black/frozen frame checks skipped")

    metadata_issues: list[str] = []
    if args.metadata:
        metadata_issues = check_metadata(Path(args.metadata), width, height, fps, video_duration, bitrate)
        issues.extend(metadata_issues)

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
            "white_events": white_events,
            "freeze_events": freeze_events,
            "silence_events": silence_events,
        },
        "metadata_consistency": {
            "checked": bool(args.metadata),
            "issues": metadata_issues,
        },
        "blocking_issues": issues,
        "warnings": warnings,
    }
    input_paths: list[Path] = [video_path]
    if args.metadata:
        input_paths.append(Path(args.metadata))
    write_report_with_fingerprints(report, input_paths)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
