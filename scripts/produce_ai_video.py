#!/usr/bin/env python3
"""Canonical AI video production gate and promotion entrypoint.

This script is intentionally stricter than the legacy QA runner. It blocks the
exact regression class where a project reports high-quality HyperFrames work
while the actual draft was rendered by an old local PIL/rawvideo card pipeline.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_SOURCE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("legacy_pil_imagedraw_import", re.compile(r"\bfrom\s+PIL\s+import\s+.*\bImageDraw\b", re.I)),
    ("legacy_pil_imagedraw_runtime", re.compile(r"\bImageDraw\.Draw\b", re.I)),
    ("legacy_rawvideo_ffmpeg_pipe", re.compile(r"\brawvideo\b", re.I)),
    ("legacy_local_renderer_script", re.compile(r"\brender_vertical_skill_guide\.py\b", re.I)),
    ("legacy_pil_ffmpeg_renderer", re.compile(r"\bPIL\s*\+\s*FFmpeg\b", re.I)),
    ("legacy_poster_renderer", re.compile(r"\bPIL vertical poster renderer\b", re.I)),
    ("legacy_ffmpeg_generated_timeline", re.compile(r"\bffmpeg generated frame timeline\b", re.I)),
    ("legacy_card_only_claim", re.compile(r"\bcard-only\b|\btext-card slideshow\b", re.I)),
]

FORBIDDEN_REPORT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("generic_useless_module_terms", re.compile(r"useless background modules|fake framework boxes|ordinary transition", re.I)),
    ("legacy_renderer_terms", re.compile(r"PIL vertical poster renderer|PIL\s*\+\s*FFmpeg|ffmpeg generated frame timeline", re.I)),
]

SOURCE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".mjs", ".cjs"}
REPORT_SUFFIXES = {".json", ".md", ".txt"}
SKIP_DIRS = {"final", "node_modules", "__pycache__", ".git", "frame_review", "renders"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def load_json(path: Path) -> dict[str, Any]:
    if not exists(path):
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def manual_frame_review_note_for(project: Path, explicit_note: str | None) -> str | None:
    if explicit_note and explicit_note.strip():
        return explicit_note.strip()
    note_path = project / "internal" / "manual_frame_review_note.txt"
    if not exists(note_path):
        return None
    note = read_text(note_path).strip()
    return note or None


def iter_candidate_files(project: Path, suffixes: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in sorted(project.rglob("*")):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        rel_parts = path.relative_to(project).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        if path.name == "visual_regression_gate.json":
            continue
        files.append(path)
    return files


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def scan_patterns(project: Path, suffixes: set[str], patterns: list[tuple[str, re.Pattern[str]]]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in iter_candidate_files(project, suffixes):
        text = read_text(path)
        if not text:
            continue
        for label, pattern in patterns:
            match = pattern.search(text)
            if match:
                hits.append(
                    {
                        "file": str(path),
                        "rule": label,
                        "match": match.group(0)[:120],
                    }
                )
    return hits


def hyperframes_sources(project: Path) -> list[str]:
    candidates: list[Path] = []
    for base in (project / "assets" / "hyperframes", project / "hyperframes"):
        if base.exists():
            candidates.extend(
                path
                for path in base.rglob("*")
                if path.is_file() and path.suffix in {".html", ".js", ".jsx", ".ts", ".tsx", ".json"}
            )
    root_candidates = [
        project / "index.html",
        project / "package.json",
        project / "composition.html",
    ]
    candidates.extend(path for path in root_candidates if exists(path))
    return [str(path) for path in sorted(set(candidates))]


def extract_frame(video: Path, frame_number: int, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        "-i",
        str(video),
        "-vf",
        f"select=eq(n\\,{frame_number})",
        "-frames:v",
        "1",
        str(out),
    ]
    subprocess.run(command, check=True)


def image_rms(path_a: Path, path_b: Path) -> float | None:
    try:
        from PIL import Image, ImageChops, ImageStat
    except ImportError:
        return None
    if not exists(path_a) or not exists(path_b):
        return None
    with Image.open(path_a) as image_a, Image.open(path_b) as image_b:
        a = image_a.convert("RGB")
        b = image_b.convert("RGB").resize(a.size)
        diff = ImageChops.difference(a, b)
        stat = ImageStat.Stat(diff)
        return math.sqrt(sum(value * value for value in stat.rms) / len(stat.rms))


def ensure_first_frame_evidence(project: Path, issues: list[str]) -> dict[str, Any]:
    internal = project / "internal"
    video = internal / "draft.mp4"
    cover = internal / "first_frame_cover.png"
    actual0 = internal / "actual_frame_000_cover.png"
    actual1 = internal / "actual_frame_001_after_cover.png"
    metrics: dict[str, Any] = {
        "expected_cover": str(cover),
        "actual_frame_000_cover": str(actual0),
        "actual_frame_001_after_cover": str(actual1),
    }

    if not exists(video):
        issues.append("internal/draft.mp4 missing; cannot verify real first-frame cover")
        return metrics
    if not exists(cover):
        issues.append("internal/first_frame_cover.png missing; cover must be a real designed frame, not a grab")
        return metrics

    for frame_number, out in ((0, actual0), (1, actual1)):
        if exists(out):
            continue
        try:
            extract_frame(video, frame_number, out)
        except (OSError, subprocess.CalledProcessError) as exc:
            issues.append(f"failed to extract actual frame {frame_number}: {exc}")

    cover_diff = image_rms(cover, actual0)
    frame01_diff = image_rms(actual0, actual1)
    metrics["cover_to_frame0_rms"] = cover_diff
    metrics["frame0_to_frame1_rms"] = frame01_diff
    metrics["cover_match_threshold_rms"] = 14.0
    metrics["frame1_return_threshold_rms"] = 4.0

    if cover_diff is None:
        issues.append("Pillow unavailable or cover/frame0 missing; cannot verify first-frame cover pixels")
    elif cover_diff > 14.0:
        issues.append(f"frame 0 does not match first_frame_cover.png (rms={cover_diff:.2f})")

    if frame01_diff is None:
        issues.append("actual frame 1 missing; cannot prove cover lasts exactly one frame")
    elif frame01_diff < 4.0:
        issues.append(f"frame 1 is still too close to cover frame (rms={frame01_diff:.2f}); cover must last one frame only")

    return metrics


def require_report_passed(internal: Path, name: str, issues: list[str]) -> dict[str, Any]:
    path = internal / name
    report = load_json(path)
    if not report:
        issues.append(f"{name} missing or empty")
        return {}
    if report.get("status") != "passed":
        issues.append(f"{name}.status must be passed")
    if report.get("blocking_issues"):
        issues.append(f"{name}.blocking_issues must be empty")
    return report


def visual_regression_gate(project: Path, out: Path | None = None) -> dict[str, Any]:
    internal = project / "internal"
    issues: list[str] = []
    warnings: list[str] = []

    legacy_source_hits = scan_patterns(project, SOURCE_SUFFIXES, FORBIDDEN_SOURCE_PATTERNS)
    legacy_report_hits = scan_patterns(project, REPORT_SUFFIXES, FORBIDDEN_REPORT_PATTERNS)
    if legacy_source_hits:
        issues.append("legacy renderer/source terms detected; remove old PIL/rawvideo/card renderer from this project")
    if legacy_report_hits:
        warnings.append("legacy warning terms detected in reports; confirm they are not describing the active runtime")

    sources = hyperframes_sources(project)
    if not sources:
        issues.append("HyperFrames source is missing; publish-ready AI videos must keep the final timeline source")

    first_frame = ensure_first_frame_evidence(project, issues)
    visual_review = require_report_passed(internal, "visual_review.json", issues)
    frame_review = require_report_passed(internal, "frame_review_report.json", issues)

    metadata = load_json(internal / "metadata.json")
    production_stack = metadata.get("production_stack") if isinstance(metadata.get("production_stack"), dict) else {}
    runtime_text = json.dumps(production_stack, ensure_ascii=False)
    if runtime_text and re.search(r"PIL|rawvideo|ffmpeg generated frame timeline|card-only", runtime_text, re.I):
        issues.append("metadata.production_stack declares a legacy low-grade renderer")

    required_motion_flags = {
        "advanced_transitions_only": "advanced transition policy must be recorded",
        "voice_safe_sfx": "dynamic icon/status SFX must be recorded as voice-safe",
    }
    regression_contract = metadata.get("regression_prevention") if isinstance(metadata.get("regression_prevention"), dict) else {}
    for key, message in required_motion_flags.items():
        if regression_contract.get(key) is not True:
            issues.append(f"metadata.regression_prevention.{key} missing; {message}")
    useful_foreground_recorded = (
        regression_contract.get("useful_foreground_modules_only") is True
        or regression_contract.get("no_useless_background_modules") is True
    )
    if not useful_foreground_recorded:
        issues.append(
            "metadata.regression_prevention.useful_foreground_modules_only missing; "
            "foreground modules must record current-scene information jobs"
        )

    checks = {
        "no_legacy_renderer_source": not legacy_source_hits,
        "hyperframes_source_present": bool(sources),
        "first_frame_cover_matches": first_frame.get("cover_to_frame0_rms") is not None
        and float(first_frame["cover_to_frame0_rms"]) <= 14.0,
        "frame1_returns_to_main_timeline": first_frame.get("frame0_to_frame1_rms") is not None
        and float(first_frame["frame0_to_frame1_rms"]) >= 4.0,
        "visual_review_passed": bool(visual_review) and visual_review.get("status") == "passed",
        "frame_review_passed": bool(frame_review) and frame_review.get("status") == "passed",
    }

    report = {
        "status": "passed" if not issues else "failed",
        "verified_at": now_iso(),
        "project": str(project),
        "checks": checks,
        "issues": issues,
        "warnings": warnings,
        "legacy_source_hits": legacy_source_hits,
        "legacy_report_hits": legacy_report_hits,
        "hyperframes_sources": sources[:80],
        "first_frame": first_frame,
    }
    if out is None:
        out = internal / "visual_regression_gate.json"
    write_json(out, report)
    return report


def promote_after_visual_gate(project: Path) -> None:
    internal = project / "internal"
    cover_report = internal / "publish_cover_report.json"
    if not exists(cover_report):
        raise SystemExit(
            "missing publish_cover_report.json. Run scripts/select_fixed_cover_template.py before render/promote; "
            "do not auto-generate the old programmatic cover preview."
        )

    text_paths: list[str] = []
    for name in ("render_text_manifest.json", "publish_cover_text.txt", "publish_copy.txt"):
        path = internal / name
        if exists(path):
            text_paths.append(str(path))
    if text_paths:
        run(
            [
                sys.executable,
                "scripts/check_public_copy.py",
                *text_paths,
                "--out",
                str(internal / "on_screen_and_publish_text_compliance_report.json"),
            ]
        )

    run(
        [
            sys.executable,
            "scripts/audit_provider_usage.py",
            "--project",
            str(project),
            "--phase",
            "final",
            "--out",
            str(internal / "provider_usage_audit.json"),
            "--md-out",
            str(internal / "provider_usage_audit.md"),
        ]
    )
    contract = internal / "publish_contract.json"
    run([sys.executable, "scripts/build_publish_contract.py", "--project", str(project), "--out", str(contract)])
    run([sys.executable, "scripts/pre_publish_gate.py", "--contract", str(contract)])
    run([sys.executable, "scripts/promote_final.py", "--project", str(project), "--contract", str(contract)])


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Canonical AI video entrypoint: QA, visual regression gate, contract gate, and optional final promotion."
    )
    parser.add_argument("--project", help="outputs/<date-topic> project path")
    parser.add_argument("--mode", choices=["qa-only", "qa-promote", "visual-gate", "golden"], default="qa-only")
    parser.add_argument("--out", help="Output path for visual-gate mode; defaults to <project>/internal/visual_regression_gate.json")
    parser.add_argument(
        "--manual-frame-review-note",
        help="Optional note confirming contact-sheet and native-frame visual review; also read from internal/manual_frame_review_note.txt when omitted.",
    )
    args = parser.parse_args()

    if args.mode == "golden":
        run([sys.executable, "scripts/check_golden_project.py"])
        return 0
    if not args.project:
        parser.error("--project is required unless --mode golden")

    project = Path(args.project)
    if args.mode in {"qa-only", "qa-promote"}:
        qa_cmd = [sys.executable, "scripts/run_pipeline.py", "--project", str(project), "--mode", "qa-only"]
        manual_note = manual_frame_review_note_for(project, args.manual_frame_review_note)
        if manual_note:
            qa_cmd.extend(["--manual-frame-review-note", manual_note])
        run(qa_cmd)

    report = visual_regression_gate(project, Path(args.out) if args.out else None)
    print(json.dumps({"status": report["status"], "issues": report["issues"], "warnings": report["warnings"]}, ensure_ascii=False, indent=2))
    if report["status"] != "passed":
        return 1

    if args.mode == "qa-promote":
        promote_after_visual_gate(project)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
