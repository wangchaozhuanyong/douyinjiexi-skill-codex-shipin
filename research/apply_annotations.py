#!/usr/bin/env python3
"""Merge human-reviewed annotations into the canonical sample registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default="research/sample_registry.json")
    parser.add_argument("--annotations", default="research/sample_annotations.json")
    args = parser.parse_args()

    registry_path = Path(args.registry)
    annotations_path = Path(args.annotations)
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    annotations = json.loads(annotations_path.read_text(encoding="utf-8"))
    sample_ids = {str(sample.get("id") or "") for sample in registry.get("samples") or []}
    if set(annotations) != sample_ids:
        missing = sorted(sample_ids - set(annotations))
        extra = sorted(set(annotations) - sample_ids)
        raise SystemExit(f"annotation ID mismatch: missing={missing}, extra={extra}")

    for sample in registry.get("samples") or []:
        sample.update(annotations[str(sample["id"])])
        sample["status"] = "analyzed"

    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"status": "passed", "annotated_samples": len(sample_ids)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
