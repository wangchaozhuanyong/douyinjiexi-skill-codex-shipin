#!/usr/bin/env python3
"""Score AI-circle topic candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


WEIGHTS = {
    "pain_score": 0.25,
    "novelty_score": 0.15,
    "save_score": 0.25,
    "comment_score": 0.10,
    "visual_score": 0.15,
    "compliance_safety_score": 0.10,
}


def clamp_score(value: Any) -> float:
    try:
        return max(0.0, min(10.0, float(value)))
    except Exception:
        return 0.0


def candidates_from(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("candidates"), list):
        return data["candidates"]
    if isinstance(data, list):
        return data
    raise ValueError("Input must be a list or an object with candidates.")


def score_candidate(candidate: dict[str, Any]) -> float:
    scores = candidate.setdefault("scores", {})
    total = 0.0
    for key, weight in WEIGHTS.items():
        total += clamp_score(scores.get(key)) * weight
    scores["total_score"] = round(total, 2)
    return scores["total_score"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Score topic candidates and enforce minimum threshold.")
    parser.add_argument("--input", required=True, help="topic_candidates.json")
    parser.add_argument("--out", help="Output path. Defaults to overwriting --input.")
    parser.add_argument("--min-score", type=float, default=8.0)
    args = parser.parse_args()

    path = Path(args.input)
    data = json.loads(path.read_text(encoding="utf-8"))
    candidates = candidates_from(data)
    for candidate in candidates:
        score_candidate(candidate)
    eligible = [item for item in candidates if item.get("scores", {}).get("total_score", 0) >= args.min_score]
    result = data if isinstance(data, dict) else {"candidates": candidates}
    result["eligible_topic_ids"] = [item.get("topic_id") for item in eligible]
    result["status"] = "passed" if eligible else "failed"

    out = Path(args.out) if args.out else path
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "eligible_topic_ids": result["eligible_topic_ids"]}, ensure_ascii=False))
    return 0 if eligible else 1


if __name__ == "__main__":
    raise SystemExit(main())
