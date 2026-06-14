#!/usr/bin/env python3
"""Apply learning-bank lessons to topic candidates."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


WORKED_TERMS = ["真实", "截图", "对比", "模板", "清单", "错误纠正", "证明", "保存"]
FIX_TERMS = ["空话", "太静", "太暗", "字幕挡", "低清晰度", "抽象背景", "单图"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def candidates_from(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("candidates"), list):
        return data["candidates"]
    if isinstance(data, list):
        return data
    raise ValueError("Input must be a list or an object with candidates.")


def bank_signals(text: str) -> dict[str, list[str]]:
    worked = sorted({term for term in WORKED_TERMS if term in text})
    fixes = sorted({term for term in FIX_TERMS if term in text})
    next_ideas = re.findall(r"- Next video ideas:\n((?:  - .+\n?)*)", text)
    return {"worked_terms": worked, "fix_terms": fixes, "next_idea_blocks": next_ideas[-3:]}


def adjustment(candidate: dict[str, Any], signals: dict[str, list[str]]) -> tuple[float, list[str]]:
    blob = json.dumps(candidate, ensure_ascii=False)
    reasons: list[str] = []
    value = 0.0
    if any(term in blob for term in signals.get("worked_terms", [])):
        value += 0.25
        reasons.append("matches repeated worked terms")
    if "真实" in signals.get("worked_terms", []) and any(term in blob for term in ["截图", "录屏", "输出", "文件", "UI"]):
        value += 0.2
        reasons.append("uses proof assets favored by learning bank")
    if "对比" in signals.get("worked_terms", []) and any(term in blob for term in ["前后", "对比", "错误", "正确"]):
        value += 0.15
        reasons.append("uses comparison structure favored by learning bank")
    if "抽象背景" in signals.get("fix_terms", []) and any(term in blob for term in ["抽象", "科技背景", "粒子"]):
        value -= 0.35
        reasons.append("matches repeated weak visual pattern")
    if "空话" in signals.get("fix_terms", []) and any(term in blob for term in ["提升效率", "很强", "神器"]):
        value -= 0.35
        reasons.append("matches repeated empty-talk failure")
    return round(max(-0.8, min(0.8, value)), 2), reasons


def apply_bank(data: dict[str, Any], bank_text: str) -> dict[str, Any]:
    signals = bank_signals(bank_text)
    candidates = candidates_from(data)
    for candidate in candidates:
        value, reasons = adjustment(candidate, signals)
        candidate["learning_bank_adjustment"] = {
            "score_delta": value,
            "reasons": reasons,
        }
        scores = candidate.setdefault("scores", {})
        if "total_score" in scores:
            try:
                scores["total_score"] = round(max(0.0, min(10.0, float(scores["total_score"]) + value)), 2)
            except Exception:
                scores["total_score"] = value
    data["learning_bank_applied"] = {
        "worked_terms": signals["worked_terms"],
        "fix_terms": signals["fix_terms"],
    }
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply learning-bank lessons to topic candidate scores.")
    parser.add_argument("--input", required=True, help="topic_candidates.json path")
    parser.add_argument("--bank", default=str(Path(__file__).resolve().parents[1] / "references" / "learning_bank.md"))
    parser.add_argument("--out", required=True, help="Adjusted topic_candidates.json path")
    args = parser.parse_args()

    data = load_json(Path(args.input))
    bank_path = Path(args.bank)
    bank_text = bank_path.read_text(encoding="utf-8") if bank_path.exists() else ""
    result = apply_bank(data, bank_text)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "applied", "out": str(out), "learning_bank_applied": result["learning_bank_applied"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
