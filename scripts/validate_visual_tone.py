#!/usr/bin/env python3
"""Validate generated visual tone against the selected brightness grade."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat


GENERATED_VISUAL_TYPES = {"generated_visual", "designed_card"}
VISUAL_ROLES = {"background_plate", "hero_poster", "metaphor_visual", "transition_plate", "diagram_base", "cover", "support_card"}


def luma(rgb: tuple[int, int, int]) -> float:
    red, green, blue = rgb
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def normalize_grade(value: str) -> str:
    text = str(value or "").strip().upper()
    if not text:
        return ""
    return text[:2] if text[:2] in {"L1", "L2", "L3", "L4", "L5"} else text


def analyze_image(path: Path) -> dict[str, float]:
    img = Image.open(path).convert("RGB").resize((320, 180))
    pixels = list(img.getdata())
    lumas = [luma(pixel) for pixel in pixels]
    stat = ImageStat.Stat(img)
    red, green, blue = stat.mean
    return {
        "avg_luma": round(sum(lumas) / len(lumas), 2),
        "dark_ratio": round(sum(1 for value in lumas if value < 55) / len(lumas), 4),
        "bright_ratio": round(sum(1 for value in lumas if value > 185) / len(lumas), 4),
        "teal_blue_bias": round((blue + green) / max(red, 1), 4),
    }


def validate_metrics(path: Path, brightness_grade: str, metrics: dict[str, float]) -> list[str]:
    grade = normalize_grade(brightness_grade)
    issues: list[str] = []
    if grade in {"L4", "L5"}:
        if metrics["avg_luma"] < 135:
            issues.append(f"{path.name}: too dark for {grade}, avg_luma={metrics['avg_luma']:.1f}")
        if metrics["dark_ratio"] > 0.28:
            issues.append(f"{path.name}: too many dark pixels for {grade}, dark_ratio={metrics['dark_ratio']:.2f}")
        if metrics["bright_ratio"] < 0.25:
            issues.append(f"{path.name}: not enough bright surface for {grade}, bright_ratio={metrics['bright_ratio']:.2f}")
    elif grade in {"L1", "L2"}:
        if metrics["avg_luma"] < 65:
            issues.append(f"{path.name}: dark scene is crushed, avg_luma={metrics['avg_luma']:.1f}")
        if metrics["bright_ratio"] < 0.10:
            issues.append(f"{path.name}: dark scene lacks bright proof surfaces, bright_ratio={metrics['bright_ratio']:.2f}")
    elif grade == "L3":
        if metrics["avg_luma"] < 105:
            issues.append(f"{path.name}: too dark for balanced editorial L3, avg_luma={metrics['avg_luma']:.1f}")
        if metrics["dark_ratio"] > 0.45:
            issues.append(f"{path.name}: too many dark pixels for L3, dark_ratio={metrics['dark_ratio']:.2f}")
    else:
        issues.append(f"{path.name}: missing or unsupported brightness_grade={brightness_grade!r}")

    if metrics["teal_blue_bias"] > 2.2:
        issues.append(f"{path.name}: possible teal/blue-only palette, bias={metrics['teal_blue_bias']:.2f}")
    return issues


def resolve_path(raw_path: str, manifest_path: Path, project: Path | None) -> Path:
    path = Path(str(raw_path).split("#", 1)[0]).expanduser()
    if path.is_absolute():
        return path
    if project:
        candidate = project / path
        if candidate.exists():
            return candidate
    return manifest_path.parent / path


def validate_one(path: Path, brightness_grade: str, asset_id: str | None = None) -> dict[str, Any]:
    try:
        metrics = analyze_image(path)
        issues = validate_metrics(path, brightness_grade, metrics)
    except Exception as exc:
        metrics = {}
        issues = [f"{path.name}: could not analyze image: {exc}"]
    return {
        "asset_id": asset_id or path.stem,
        "path": str(path),
        "brightness_grade": brightness_grade,
        "metrics": metrics,
        "status": "passed" if not issues else "failed",
        "issues": issues,
    }


def should_check_asset(asset: dict[str, Any]) -> bool:
    asset_type = str(asset.get("type", ""))
    role = str(asset.get("asset_role", ""))
    return asset_type in GENERATED_VISUAL_TYPES or role in VISUAL_ROLES


def validate_manifest(manifest_path: Path, project: Path | None) -> list[dict[str, Any]]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    results: list[dict[str, Any]] = []
    for index, asset in enumerate(data.get("assets", []) or [], start=1):
        if not should_check_asset(asset):
            continue
        raw_path = str(asset.get("path", "")).strip()
        grade = str(asset.get("brightness_grade", "")).strip()
        asset_id = str(asset.get("asset_id") or f"asset_{index}")
        if not raw_path:
            results.append(
                {
                    "asset_id": asset_id,
                    "path": "",
                    "brightness_grade": grade,
                    "metrics": {},
                    "status": "failed",
                    "issues": [f"{asset_id}: missing path"],
                }
            )
            continue
        results.append(validate_one(resolve_path(raw_path, manifest_path, project), grade, asset_id))
    return results


def build_report(results: list[dict[str, Any]]) -> dict[str, Any]:
    issues = [issue for result in results for issue in result["issues"]]
    return {
        "status": "passed" if not issues else "failed",
        "image_count": len(results),
        "results": results,
        "blocking_issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate visual image tone against brightness-grade rules.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--image", help="Single image path to validate.")
    source.add_argument("--manifest", help="asset_manifest.json path to validate.")
    parser.add_argument("--brightness-grade", choices=["L1", "L2", "L3", "L4", "L5"], help="Required with --image.")
    parser.add_argument("--project", help="Optional project root for manifest-relative paths.")
    parser.add_argument("--out", help="Output visual_tone_report.json path.")
    args = parser.parse_args()

    if args.image:
        if not args.brightness_grade:
            parser.error("--brightness-grade is required with --image")
        results = [validate_one(Path(args.image), args.brightness_grade)]
    else:
        results = validate_manifest(Path(args.manifest), Path(args.project) if args.project else None)

    report = build_report(results)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
