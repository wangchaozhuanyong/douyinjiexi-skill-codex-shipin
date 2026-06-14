#!/usr/bin/env python3
"""Append a post-publish review summary to references/learning_bank.md."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def bullet_list(items: list[Any]) -> str:
    if not items:
        return "  - none"
    return "\n".join(f"  - {item}" for item in items)


def build_entry(review: dict[str, Any]) -> str:
    metrics = review.get("metrics_24h", {})
    metrics_text = ", ".join(f"{key}={value}" for key, value in metrics.items()) or "none"
    video_id = review.get("video_id", "unknown-video")
    return f"""
## {review.get('published_at', 'undated')} {video_id}

- Topic: {review.get('topic', '')}
- Format: {review.get('format', '')}
- Hook type: {review.get('hook_type', '')}
- Duration seconds: {review.get('duration_seconds', 0)}
- 24h metrics: {metrics_text}
- Comment insights:
{bullet_list(review.get('comment_insights', []))}
- What worked:
{bullet_list(review.get('what_worked', []))}
- What to fix:
{bullet_list(review.get('what_to_fix', []))}
- Next video ideas:
{bullet_list(review.get('next_video_ideas', []))}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Append post-publish review to the learning bank.")
    parser.add_argument("--review", required=True, help="post_publish_review.json path")
    parser.add_argument("--bank", default=str(ROOT / "references" / "learning_bank.md"))
    args = parser.parse_args()

    review_path = Path(args.review)
    bank_path = Path(args.bank)
    review = load_json(review_path)
    entry = build_entry(review)
    bank_path.parent.mkdir(parents=True, exist_ok=True)
    existing = bank_path.read_text(encoding="utf-8") if bank_path.exists() else "# Learning Bank\n"
    bank_path.write_text(existing.rstrip() + "\n\n" + entry.strip() + "\n", encoding="utf-8")
    print(json.dumps({"status": "updated", "bank": str(bank_path), "video_id": review.get("video_id")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
