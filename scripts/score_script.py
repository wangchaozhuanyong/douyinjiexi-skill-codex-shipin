#!/usr/bin/env python3
"""Heuristically score a Chinese Douyin copy package."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


BAD_OPENINGS = ["今天给大家介绍", "AI 时代来了", "你知道吗", "很多人不知道", "这个工具太强"]
FORBIDDEN = ["必火", "保证涨粉", "100%", "用了就能赚钱", "全网最强", "第一", "唯一", "评论区打 1"]


def score(text: str) -> dict[str, float]:
    has_hook = "First 5 Seconds" in text or "前 5" in text or "Hook" in text
    has_claim_ledger = "Claim Ledger" in text or "claim ledger" in text.lower()
    has_save = any(term in text for term in ["收藏", "模板", "清单", "步骤", "判断标准", "直接套"])
    has_proof = any(term in text for term in ["截图", "演示", "证据", "真实", "对比"])
    has_bad_opening = any(term in text for term in BAD_OPENINGS)
    has_forbidden = any(term in text for term in FORBIDDEN)
    short_sentences = len(re.findall(r"[。！？\n]", text)) >= 8

    first_5 = 9.2 if has_hook and not has_bad_opening else 6.5
    clarity = 8.5 if short_sentences else 7.0
    specificity = 8.5 if has_proof else 7.0
    save_value = 8.6 if has_save else 6.8
    proof = 8.5 if has_proof else 6.5
    rhythm = 8.3 if short_sentences else 7.0
    compliance = 9.4 if not has_forbidden else 5.0
    script_score = round((first_5 + clarity + specificity + save_value + proof + rhythm + compliance) / 7, 2)

    return {
        "first_5_seconds_score": round(first_5, 2),
        "clarity_score": round(clarity, 2),
        "specificity_score": round(specificity, 2),
        "save_value_score": round(save_value, 2),
        "proof_score": round(proof, 2),
        "rhythm_score": round(rhythm, 2),
        "compliance_score": round(compliance, 2),
        "script_score": script_score,
        "claim_ledger_present": bool(has_claim_ledger),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a copy package before storyboard.")
    parser.add_argument("--copy", required=True, help="copy_package.md")
    parser.add_argument("--out", help="Output JSON score report.")
    args = parser.parse_args()

    text = Path(args.copy).read_text(encoding="utf-8")
    result = score(text)
    passed = (
        result["script_score"] >= 8
        and result["first_5_seconds_score"] >= 9
        and result["save_value_score"] >= 8
        and result["compliance_score"] >= 9
    )
    result["status"] = "passed" if passed else "failed"
    if args.out:
        Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
