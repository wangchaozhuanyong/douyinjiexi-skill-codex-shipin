#!/usr/bin/env python3
"""Validate the 18-sample research gate without inventing performance data."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="research/sample_registry.json")
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()

    path = Path(args.registry)
    data = json.loads(path.read_text(encoding="utf-8"))
    samples = data.get("samples") or []
    issues: list[str] = []
    warnings: list[str] = []
    if len(samples) != 18:
        issues.append(f"registry must contain 18 slots, got {len(samples)}")
    ids = [str(item.get("id") or "") for item in samples]
    if len(set(ids)) != len(ids):
        issues.append("sample ids must be unique")

    analyzed_counts = Counter()
    group_counts: dict[str, Counter[str]] = {}
    for sample in samples:
        category = str(sample.get("category") or "")
        group_counts.setdefault(category, Counter())
        group_counts[category][str(sample.get("performance_group") or "")] += 1
        if sample.get("status") != "analyzed":
            continue
        analyzed_counts[category] += 1
        video = Path(str(sample.get("local_path") or ""))
        if not video.is_file() or video.stat().st_size == 0:
            issues.append(f"{sample.get('id')} playable body missing: {video}")
            continue
        if sample.get("sha256") != sha256(video):
            issues.append(f"{sample.get('id')} sha256 mismatch")
        for field in (
            "duration",
            "width",
            "height",
            "fps",
            "has_audio",
            "first_five_seconds",
            "copy_structure",
            "proof_types",
            "closing",
        ):
            if sample.get(field) in (None, "", []):
                issues.append(f"{sample.get('id')}.{field} is required")

    for category in ("tool_explainer", "news_explainer", "list_video"):
        if analyzed_counts[category] < 6:
            warnings.append(f"{category}: {analyzed_counts[category]}/6 analyzed")
        counts = group_counts.get(category, Counter())
        if counts["high_visible"] < 4:
            warnings.append(f"{category}: {counts['high_visible']}/4 high_visible")
        if counts["control_visible"] < 2:
            warnings.append(f"{category}: {counts['control_visible']}/2 control_visible")

    incomplete = bool(warnings)
    status = "passed" if not issues and (args.allow_incomplete or not incomplete) else "blocked"
    result = {
        "status": status,
        "analyzed_counts": dict(analyzed_counts),
        "blocking_issues": issues,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if status == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
