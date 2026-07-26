#!/usr/bin/env python3
"""Repair blank leading frames in a HyperFrames PNG sequence.

Run this after the main HyperFrames PNG sequence export and before FFmpeg
encoding. The designed cover is inserted later as frame 0, so this script keeps
frame 0 untouched by default and makes frame 1 return to the first real content
frame when the browser export produced blank or initialization frames.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FRAME_NUMBER = re.compile(r"(\d+)(?=\.[^.]+$)")


@dataclass(frozen=True)
class FrameStat:
    path: Path
    frame_number: int
    mean_luma: float
    stddev: float
    extrema_span: float

    @property
    def content_score(self) -> float:
        return self.stddev + (self.extrema_span * 0.15)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def frame_number(path: Path) -> int | None:
    match = FRAME_NUMBER.search(path.name)
    if not match:
        return None
    return int(match.group(1))


def list_frames(frames_dir: Path) -> list[Path]:
    if not frames_dir.exists():
        return []
    frames: list[tuple[int, Path]] = []
    for path in frames_dir.iterdir():
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg"} or not path.is_file():
            continue
        number = frame_number(path)
        if number is None:
            continue
        frames.append((number, path))
    return [path for _, path in sorted(frames)]


def image_stat(path: Path) -> FrameStat:
    try:
        from PIL import Image, ImageStat
    except ImportError as exc:
        raise RuntimeError("Pillow is required for leading-frame repair") from exc

    number = frame_number(path)
    if number is None:
        raise ValueError(f"cannot parse frame number from {path}")
    with Image.open(path) as image:
        gray = image.convert("L")
        stat = ImageStat.Stat(gray)
        extrema = gray.getextrema()
    return FrameStat(
        path=path,
        frame_number=number,
        mean_luma=float(stat.mean[0]),
        stddev=float(stat.stddev[0]),
        extrema_span=float(extrema[1] - extrema[0]),
    )


def find_first_content_frame(frames: list[Path], start_frame: int, max_scan_frames: int, min_score: float) -> FrameStat | None:
    scanned = 0
    for path in frames:
        number = frame_number(path)
        if number is None or number < start_frame:
            continue
        if scanned >= max_scan_frames:
            break
        scanned += 1
        stat = image_stat(path)
        if stat.content_score >= min_score:
            return stat
    return None


def repair_sequence(
    frames_dir: Path,
    *,
    start_frame: int | None = None,
    preserve_leading_frames: int = 1,
    max_scan_frames: int = 90,
    min_score: float = 8.0,
    out: Path | None = None,
) -> dict[str, Any]:
    frames = list_frames(frames_dir)
    first_number = frame_number(frames[0]) if frames else None
    repair_start_frame = start_frame
    if repair_start_frame is None and first_number is not None:
        repair_start_frame = first_number + max(0, preserve_leading_frames)
    elif repair_start_frame is None:
        repair_start_frame = preserve_leading_frames

    report: dict[str, Any] = {
        "status": "passed",
        "action": "not_needed",
        "checked_at": now_iso(),
        "frames_dir": str(frames_dir),
        "start_frame": repair_start_frame,
        "first_frame_number": first_number,
        "preserve_leading_frames": preserve_leading_frames,
        "preserved_frame_numbers": [
            number
            for path in frames[:max(0, preserve_leading_frames)]
            if (number := frame_number(path)) is not None
        ],
        "contract": {
            "cover_slot_preserved": preserve_leading_frames >= 1,
            "frame_one_returns_to_main_timeline": True,
        },
        "max_scan_frames": max_scan_frames,
        "min_content_score": min_score,
        "frame_count": len(frames),
        "first_content_frame": None,
        "repaired_frames": [],
        "issues": [],
    }

    if not frames:
        report["status"] = "failed"
        report["action"] = "failed"
        report["issues"].append("frame sequence is missing or empty")
        if out:
            write_json(out, report)
        return report

    first_content = find_first_content_frame(frames, int(repair_start_frame), max_scan_frames, min_score)
    if first_content is None:
        report["status"] = "failed"
        report["action"] = "failed"
        report["issues"].append("no content-bearing frame found inside scan window")
        if out:
            write_json(out, report)
        return report

    report["first_content_frame"] = {
        "path": str(first_content.path),
        "frame_number": first_content.frame_number,
        "mean_luma": round(first_content.mean_luma, 3),
        "stddev": round(first_content.stddev, 3),
        "extrema_span": round(first_content.extrema_span, 3),
        "content_score": round(first_content.content_score, 3),
    }

    if first_content.frame_number <= int(repair_start_frame):
        if out:
            write_json(out, report)
        return report

    frame_map = {frame_number(path): path for path in frames}
    repaired: list[str] = []
    for number in range(int(repair_start_frame), first_content.frame_number):
        target = frame_map.get(number)
        if target is None:
            continue
        shutil.copy2(first_content.path, target)
        repaired.append(str(target))

    report["action"] = "repaired" if repaired else "not_needed"
    report["repaired_frames"] = repaired
    report["repaired_frame_count"] = len(repaired)
    if out:
        write_json(out, report)
    return report


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Repair blank leading frames in internal/hf_frames.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument("--frames-dir", help="Defaults to <project>/internal/hf_frames")
    parser.add_argument(
        "--start-frame",
        type=int,
        help="Explicit first filename number eligible for repair. Defaults to preserving the first image file as the cover slot.",
    )
    parser.add_argument(
        "--preserve-leading-frames",
        type=int,
        default=1,
        help="Number of leading sequence files to leave untouched for the later one-frame cover overlay.",
    )
    parser.add_argument("--max-scan-frames", type=int, default=90)
    parser.add_argument("--min-content-score", type=float, default=8.0)
    parser.add_argument("--out", help="Defaults to <project>/internal/leading_frame_repair_report.json")
    args = parser.parse_args()

    project = Path(args.project)
    frames_dir = Path(args.frames_dir) if args.frames_dir else project / "internal" / "hf_frames"
    out = Path(args.out) if args.out else project / "internal" / "leading_frame_repair_report.json"
    report = repair_sequence(
        frames_dir,
        start_frame=args.start_frame,
        preserve_leading_frames=args.preserve_leading_frames,
        max_scan_frames=args.max_scan_frames,
        min_score=args.min_content_score,
        out=out,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
