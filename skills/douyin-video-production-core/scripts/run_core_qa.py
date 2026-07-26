#!/usr/bin/env python3
"""Run content mapping and technical checks, then write qa_report.json."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from artifact_fingerprint import write_report_with_fingerprints
from validate_project import artifact_path, load_json, validate_preproduction


REQUIRED_MANUAL_CHECKS = (
    "first_five_seconds",
    "claim_proof_sync",
    "proof_legibility",
    "creative_direction_fit",
    "visual_repetition",
    "narrative_rhythm",
    "caption_readability",
    "subtitle_sync",
    "voice_naturalness",
    "safe_area",
    "safe_area_overlay",
    "cover_text_overlap",
    "black_or_empty_frames",
    "full_contact_sheet",
)


def command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False)


def probe(video: Path) -> dict[str, Any]:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        return {"error": "ffprobe is unavailable"}
    result = command(
        [
            ffprobe,
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-of",
            "json",
            str(video),
        ]
    )
    if result.returncode != 0:
        return {"error": result.stderr.strip() or "ffprobe failed"}
    return json.loads(result.stdout)


def rate(value: str) -> float:
    left, _, right = value.partition("/")
    try:
        return float(left) / float(right or 1)
    except (TypeError, ValueError, ZeroDivisionError):
        return 0.0


def make_contact_sheet(video: Path, out: Path, duration: float) -> str:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return "ffmpeg is unavailable"
    out.parent.mkdir(parents=True, exist_ok=True)
    interval = max(duration / 12.0, 0.5)
    result = command(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(video),
            "-vf",
            f"fps=1/{interval:.3f},scale=480:-2,tile=4x3:padding=8:margin=8",
            "-frames:v",
            "1",
            str(out),
        ]
    )
    return "" if result.returncode == 0 and out.is_file() else (result.stderr.strip() or "contact sheet failed")


def detect(video: Path, video_filter: str | None = None, audio_filter: str | None = None) -> list[str]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        return []
    args = [ffmpeg, "-hide_banner", "-nostats", "-i", str(video)]
    if video_filter:
        args += ["-vf", video_filter, "-an"]
    if audio_filter:
        args += ["-af", audio_filter, "-vn"]
    args += ["-f", "null", "-"]
    result = command(args)
    markers = ("black_start", "black_end", "silence_start", "silence_end", "silence_duration")
    return [line.strip() for line in result.stderr.splitlines() if any(marker in line for marker in markers)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--video", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    video = Path(args.video).resolve()
    out = Path(args.out) if args.out else artifact_path(project, "qa_report.json")
    pre_issues, pre_warnings, mapping = validate_preproduction(project)
    issues = list(pre_issues)
    warnings = list(pre_warnings)
    script_for_risk = load_json(artifact_path(project, "script.json"), issues)
    risk_review = script_for_risk.get("risk_review")
    high_risk = isinstance(risk_review, dict) and risk_review.get("level") == "high"

    technical: dict[str, Any] = {}
    audio_report: dict[str, Any] = {
        "has_audio": False,
        "duration": 0.0,
        "silence_markers": [],
    }
    frames_report: dict[str, Any] = {
        "black_frame_markers": [],
        "contact_sheet": str(project / "review" / "contact_sheet.jpg"),
        "manual_review": str(project / "review" / "manual_review.json"),
        "status": "not_run",
    }
    if not video.is_file() or video.stat().st_size == 0:
        issues.append(f"rendered video missing or empty: {video}")
    else:
        data = probe(video)
        if data.get("error"):
            issues.append(str(data["error"]))
        else:
            streams = data.get("streams") or []
            vstream = next((item for item in streams if item.get("codec_type") == "video"), {})
            astream = next((item for item in streams if item.get("codec_type") == "audio"), {})
            fmt = data.get("format") or {}
            width = int(vstream.get("width") or 0)
            height = int(vstream.get("height") or 0)
            fps = rate(str(vstream.get("avg_frame_rate") or "0/1"))
            duration = float(fmt.get("duration") or vstream.get("duration") or 0)
            audio_duration = float(astream.get("duration") or duration or 0)
            storyboard = load_json(artifact_path(project, "storyboard.json"), issues)
            expected_width = int(storyboard.get("width") or 0)
            expected_height = int(storyboard.get("height") or 0)
            expected_fps = float(storyboard.get("fps") or 0)
            if (width, height) != (expected_width, expected_height):
                issues.append(f"video resolution {width}x{height} does not match storyboard {expected_width}x{expected_height}")
            if expected_fps and abs(fps - expected_fps) > 0.2:
                issues.append(f"video fps {fps:.3f} does not match storyboard {expected_fps:.3f}")
            if not astream:
                issues.append("audio stream is missing")
            if abs(duration - audio_duration) > 0.35:
                issues.append(f"audio/video duration gap is {abs(duration - audio_duration):.3f}s")
            technical = {
                "width": width,
                "height": height,
                "fps": round(fps, 3),
                "duration": round(duration, 3),
                "audio_duration": round(audio_duration, 3),
                "has_audio": bool(astream),
                "size_bytes": video.stat().st_size,
            }
            frame_markers = detect(video, video_filter="blackdetect=d=0.35:pic_th=0.98")
            silence_markers = detect(video, audio_filter="silencedetect=n=-45dB:d=0.5") if astream else []
            if frame_markers:
                issues.append("detected long black frames")
            if any("silence_duration" in line and not line.rstrip().endswith("0") for line in silence_markers):
                warnings.append("detected audio silence; inspect whether it is intentional")
            technical["black_frame_markers"] = frame_markers
            technical["silence_markers"] = silence_markers
            audio_report = {
                "has_audio": bool(astream),
                "duration": round(audio_duration, 3),
                "silence_markers": silence_markers,
            }

            contact_sheet = project / "review" / "contact_sheet.jpg"
            sheet_error = make_contact_sheet(video, contact_sheet, duration)
            if sheet_error:
                issues.append(sheet_error)
            manual_review_path = project / "review" / "manual_review.json"
            manual_review = load_json(manual_review_path, []) if manual_review_path.exists() else {}
            if manual_review.get("status") != "passed":
                issues.append("review/manual_review.json must record a passed human or independent visual review")
            review_checks = manual_review.get("checks") if isinstance(manual_review.get("checks"), dict) else {}
            for check_name in REQUIRED_MANUAL_CHECKS:
                if review_checks.get(check_name) != "passed":
                    issues.append(
                        "review/manual_review.json checks."
                        f"{check_name} must be passed"
                    )
            review_evidence = (
                manual_review.get("evidence")
                if isinstance(manual_review.get("evidence"), dict)
                else {}
            )
            for evidence_name in ("safe_area_overlay", "cover"):
                evidence_value = str(review_evidence.get(evidence_name) or "")
                evidence_path = Path(evidence_value)
                if evidence_value and not evidence_path.is_absolute():
                    evidence_path = project / evidence_path
                if not evidence_value or not evidence_path.is_file():
                    issues.append(
                        "review/manual_review.json evidence."
                        f"{evidence_name} must point to an existing file"
                    )
            if high_risk and review_checks.get("high_risk_boundary") != "passed":
                issues.append(
                    "high-risk tool video requires review/manual_review.json "
                    "checks.high_risk_boundary=passed"
                )
            frames_report = {
                "black_frame_markers": frame_markers,
                "contact_sheet": str(contact_sheet),
                "manual_review": str(manual_review_path),
                "status": "passed"
                if not frame_markers and not sheet_error and manual_review.get("status") == "passed"
                else "blocked",
                "safe_area": review_checks.get("safe_area", "not_reviewed"),
                "safe_area_overlay": review_checks.get(
                    "safe_area_overlay", "not_reviewed"
                ),
                "cover_text_overlap": review_checks.get(
                    "cover_text_overlap", "not_reviewed"
                ),
                "creative_direction_fit": review_checks.get(
                    "creative_direction_fit", "not_reviewed"
                ),
                "visual_repetition": review_checks.get(
                    "visual_repetition", "not_reviewed"
                ),
                "proof_legibility": review_checks.get(
                    "proof_legibility", "not_reviewed"
                ),
                "subtitle_sync": review_checks.get("subtitle_sync", "not_reviewed"),
                "voice_naturalness": review_checks.get(
                    "voice_naturalness", "not_reviewed"
                ),
                "high_risk_boundary": review_checks.get("high_risk_boundary", "not_applicable"),
            }

    text_check_path = project / "public_text_check.json"
    text_check = load_json(text_check_path, []) if text_check_path.exists() else {}
    if text_check and text_check.get("status") != "passed":
        issues.append("public_text_check.status must be passed")

    report = {
        "status": "passed" if not issues else "blocked",
        "project": str(project),
        "video": str(video),
        "content_mapping": mapping,
        "technical": technical,
        "audio": audio_report,
        "frames": frames_report,
        "public_text": {
            "report": str(text_check_path),
            "status": text_check.get("status") or "not_run",
        },
        "blocking_issues": issues,
        "warnings": warnings,
    }
    inputs = [
        video,
        artifact_path(project, "source_brief.json"),
        artifact_path(project, "script.json"),
        artifact_path(project, "storyboard.json"),
        artifact_path(project, "asset_manifest.json"),
    ]
    write_report_with_fingerprints(report, [path for path in inputs if path.is_file()])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
