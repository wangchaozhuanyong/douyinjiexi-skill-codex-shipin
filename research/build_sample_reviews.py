#!/usr/bin/env python3
"""Build uniform contact sheets and machine-observed pacing notes for samples."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FFMPEG = "/Users/wangchao/.local/bin/ffmpeg"


def run(command: list[str], *, capture: bool = False) -> str:
    result = subprocess.run(
        command,
        check=True,
        capture_output=capture,
        text=True,
    )
    return result.stderr if capture else ""


def extract_uniform(video: Path, output: Path, duration: float) -> list[Path]:
    output.mkdir(parents=True, exist_ok=True)
    for old in output.glob("uniform_*.jpg"):
        old.unlink()
    interval = max(duration / 16.0, 0.25)
    run(
        [
            FFMPEG,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video),
            "-vf",
            f"fps=1/{interval},scale=360:-2",
            "-frames:v",
            "16",
            "-q:v",
            "2",
            str(output / "uniform_%02d.jpg"),
        ]
    )
    return sorted(output.glob("uniform_*.jpg"))


def extract_opening(video: Path, output: Path, duration: float) -> list[Path]:
    for old in output.glob("opening_*.jpg"):
        old.unlink()
    fps = 1.0 if duration >= 5 else max(5.0 / max(duration, 0.1), 1.0)
    run(
        [
            FFMPEG,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-ss",
            "0",
            "-t",
            str(min(5.0, duration)),
            "-i",
            str(video),
            "-vf",
            f"fps={fps},scale=360:-2",
            "-frames:v",
            "5",
            "-q:v",
            "2",
            str(output / "opening_%02d.jpg"),
        ]
    )
    return sorted(output.glob("opening_*.jpg"))


def tile(pattern: str, output: Path, columns: int, rows: int) -> None:
    run(
        [
            FFMPEG,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-pattern_type",
            "glob",
            "-i",
            pattern,
            "-vf",
            f"tile={columns}x{rows}:padding=6:margin=6:color=0x111318",
            "-frames:v",
            "1",
            str(output),
        ]
    )


def scene_changes(video: Path) -> list[float]:
    stderr = run(
        [
            FFMPEG,
            "-hide_banner",
            "-i",
            str(video),
            "-filter:v",
            "select='gt(scene,0.35)',showinfo",
            "-an",
            "-f",
            "null",
            "-",
        ],
        capture=True,
    )
    changes: list[float] = []
    for line in stderr.splitlines():
        if "showinfo" not in line or "pts_time:" not in line:
            continue
        token = line.split("pts_time:", 1)[1].split()[0]
        try:
            changes.append(round(float(token), 3))
        except ValueError:
            continue
    return changes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="research/sample_registry.json")
    parser.add_argument("--sample", action="append")
    args = parser.parse_args()

    registry_path = Path(args.registry).resolve()
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    wanted = set(args.sample or [])
    failures: list[str] = []

    for sample in registry.get("samples") or []:
        sample_id = str(sample.get("id") or "")
        if wanted and sample_id not in wanted:
            continue
        video = Path(str(sample.get("local_path") or ""))
        if not video.is_absolute():
            video = (ROOT / video).resolve()
        if not video.is_file():
            failures.append(f"{sample_id}: video missing")
            continue
        try:
            duration = float(sample.get("duration") or 0)
            review_dir = ROOT / "research" / "reviews" / sample_id
            uniform = extract_uniform(video, review_dir, duration)
            opening = extract_opening(video, review_dir, duration)
            if not uniform or not opening:
                raise RuntimeError("frame extraction produced no review frames")
            tile(str(review_dir / "uniform_*.jpg"), review_dir / "contact_sheet.jpg", 4, 4)
            tile(str(review_dir / "opening_*.jpg"), review_dir / "opening_five_seconds.jpg", 5, 1)
            changes = scene_changes(video)
            review = {
                "sample_id": sample_id,
                "video": str(video),
                "contact_sheet": str(review_dir / "contact_sheet.jpg"),
                "opening_sheet": str(review_dir / "opening_five_seconds.jpg"),
                "uniform_frame_count": len(uniform),
                "scene_change_threshold": 0.35,
                "scene_change_count": len(changes),
                "scene_changes_seconds": changes,
                "scene_changes_per_minute": (
                    round(len(changes) / (duration / 60.0), 2) if duration else 0
                ),
                "human_review_required": True,
            }
            (review_dir / "review.json").write_text(
                json.dumps(review, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            sample.update(
                {
                    "review_artifacts": {
                        "contact_sheet": str(review_dir / "contact_sheet.jpg"),
                        "opening_five_seconds": str(review_dir / "opening_five_seconds.jpg"),
                        "review_json": str(review_dir / "review.json"),
                    },
                    "scene_change_count": len(changes),
                    "scene_changes_per_minute": review["scene_changes_per_minute"],
                }
            )
            print(f"{sample_id}: review artifacts ready")
        except Exception as exc:
            failures.append(f"{sample_id}: {type(exc).__name__}: {exc}")

    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"failures": failures}, ensure_ascii=False, indent=2))
    return 2 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
