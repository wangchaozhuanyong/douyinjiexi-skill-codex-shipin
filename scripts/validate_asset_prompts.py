#!/usr/bin/env python3
"""Validate generated-asset prompt packs before ImageGen or HyperFrames work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from asset_prompt_contract import validate_prompt_pack_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate AI video visual prompt pack quality.")
    parser.add_argument("--prompt-pack", required=True, help="background_prompt_pack.md or ai_asset_prompt_pack.md")
    parser.add_argument("--out", help="Output asset_prompt_validation.json path")
    parser.add_argument("--min-cards", type=int, default=1, help="Minimum visual prompt cards required")
    args = parser.parse_args()

    path = Path(args.prompt_pack)
    if not path.exists() or not path.is_file() or path.stat().st_size == 0:
        report = {
            "status": "failed",
            "prompt_card_count": 0,
            "validated_fields": [],
            "blocking_issues": [f"missing or empty prompt pack: {args.prompt_pack}"],
            "warnings": [],
        }
    else:
        report = validate_prompt_pack_text(path.read_text(encoding="utf-8"), min_cards=args.min_cards)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
