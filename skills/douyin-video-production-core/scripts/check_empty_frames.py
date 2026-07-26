#!/usr/bin/env python3
"""Block accidental empty visual spans after frame review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MAX_EMPTY_VISUAL_DURATION_SEC = 0.5
MIN_PRIMARY_REGION_EDGE_DENSITY = 0.015
MIN_PRIMARY_REGION_BRIGHTNESS_STD = 7.5
PRIMARY_REGIONS = {"left", "center", "middle", "main", "content"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(value: Any) -> str:
    return str(value or "").strip()


def as_float(value: Any) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def region_name(value: Any) -> str:
    return normalize(value).lower().replace("_", "-")


def region_duration(record: dict[str, Any]) -> float:
    duration = as_float(record.get("duration_sec"))
    if duration is not None:
        return duration
    start = as_float(record.get("start_sec"))
    end = as_float(record.get("end_sec"))
    if start is not None and end is not None:
        return max(0.0, end - start)
    return 0.0


def low_information_region(record: dict[str, Any]) -> bool:
    edge_density = as_float(record.get("edge_density"))
    brightness_std = as_float(record.get("brightness_std") or record.get("luma_std"))
    visible_objects = as_float(record.get("visible_object_count") or record.get("foreground_object_count"))
    text_boxes = as_float(record.get("text_box_count") or record.get("foreground_text_box_count"))

    if visible_objects is not None and visible_objects >= 1:
        return False
    if text_boxes is not None and text_boxes >= 1:
        return False
    weak_edges = edge_density is not None and edge_density < MIN_PRIMARY_REGION_EDGE_DENSITY
    flat_luma = brightness_std is not None and brightness_std < MIN_PRIMARY_REGION_BRIGHTNESS_STD
    return weak_edges and flat_luma


def structured_region_records(frame_review: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("frame_region_metrics", "region_density_checks", "visual_density_checks"):
        value = frame_review.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def validate(storyboard: dict[str, Any], frame_review: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    warnings: list[str] = []

    shots = storyboard.get("director_shots", [])
    if not isinstance(shots, list) or not shots:
        issues.append("director_shots are required for empty-frame gate")
        shots = []

    subjectless_shots = []
    for shot in shots:
        if not isinstance(shot, dict):
            continue
        shot_id = normalize(shot.get("shot_id"))
        visual_subject = normalize(shot.get("visual_subject"))
        primary_action = normalize(shot.get("primary_action"))
        if not visual_subject or not primary_action or primary_action.lower() in {"none", "static", "无"}:
            subjectless_shots.append(shot_id or "unknown")
    for shot_id in subjectless_shots:
        issues.append(f"{shot_id} lacks a primary visual subject/action")

    candidates = frame_review.get("empty_frame_candidates", [])
    if candidates is None:
        candidates = []
    if not isinstance(candidates, list):
        issues.append("frame_review.empty_frame_candidates must be an array when present")
        candidates = []
    blocking_candidates = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        try:
            duration = float(candidate.get("duration_sec") or 0)
        except Exception:
            duration = 0.0
        intentional = candidate.get("intentional") is True
        if duration > MAX_EMPTY_VISUAL_DURATION_SEC and not intentional:
            blocking_candidates.append(candidate)
    for candidate in blocking_candidates:
        issues.append(
            f"empty visual span exceeds {MAX_EMPTY_VISUAL_DURATION_SEC}s at {candidate.get('start_sec')}s: {candidate.get('duration_sec')}s"
        )

    low_information_regions: list[dict[str, Any]] = []
    for record in structured_region_records(frame_review):
        name = region_name(record.get("region") or record.get("region_name") or record.get("area"))
        normalized = "center" if name == "middle" else name
        if normalized not in PRIMARY_REGIONS:
            continue
        duration = region_duration(record)
        if duration <= MAX_EMPTY_VISUAL_DURATION_SEC:
            continue
        intentional = record.get("intentional") is True
        if not intentional and low_information_region(record):
            low_information_regions.append(record)
    for record in low_information_regions:
        issues.append(
            "primary visual region has low information density for "
            f"{region_duration(record):.2f}s at {record.get('start_sec')}s: {record.get('region') or record.get('area')}"
        )

    if frame_review.get("status") not in {"passed", "review_required"}:
        issues.append("frame_review status must be passed or review_required before empty-frame gate")
    if frame_review.get("status") == "review_required":
        warnings.append("frame_review is review_required; empty-frame gate only checked structured candidates")

    return {
        "status": "passed" if not issues else "failed",
        "max_empty_visual_duration_sec": MAX_EMPTY_VISUAL_DURATION_SEC,
        "director_shot_count": len(shots),
        "subjectless_shots": subjectless_shots,
        "empty_frame_candidate_count": len(candidates),
        "blocking_empty_frame_candidates": blocking_candidates,
        "low_information_primary_regions": low_information_regions,
        "blocking_issues": issues,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check storyboard/frame review for accidental empty frames.")
    parser.add_argument("--storyboard", required=True)
    parser.add_argument("--frame-review", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    report = validate(load_json(Path(args.storyboard)), load_json(Path(args.frame_review)))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
