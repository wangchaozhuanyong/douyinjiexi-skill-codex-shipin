#!/usr/bin/env python3
"""Create a local compliance report for public-facing Douyin video copy."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_TERM_BANK = Path("references/forbidden_terms_learning_bank.jsonl")

RISK_PATTERNS: list[dict[str, str]] = [
    {"level": "error", "category": "absolute_claim", "pattern": r"最强|排名第一|行业第一|全网第一|唯一方法|全网最强|100%|百分百|永久|必火|必爆"},
    {"level": "error", "category": "guaranteed_result", "pattern": r"保证|包成功|保证涨粉|包过|稳赚|无风险|秒赚|暴富|躺赚|用了就能赚钱"},
    {"level": "error", "category": "false_authority", "pattern": r"官方认证|国家级|央视推荐|权威背书|专家推荐|权威机构认证"},
    {"level": "error", "category": "induced_engagement", "pattern": r"不点赞就亏|必须收藏|评论区打\s*1|点赞过.*继续讲|转发.*领取"},
    {"level": "error", "category": "external_diversion", "pattern": r"微信|VX|vx|QQ|加群|扫码|私信领取|联系方式|电话[:：]?\\d"},
    {"level": "error", "category": "qr_or_contact", "pattern": r"二维码|QR\\s*code|手机号|手机号码|加我"},
    {"level": "warning", "category": "ai_disclosure", "pattern": r"AI生成|AI 生成|虚拟演示|概念图"},
    {"level": "warning", "category": "low_quality_risk", "pattern": r"随便截|搬运|录屏搬|一张图讲完|图片轮播"},
    {"level": "warning", "category": "pseudo_chinese", "pattern": r"[口囗□�]{2,}"},
]

SUGGESTIONS = {
    "absolute_claim": "改为非绝对表述，例如：我常用的一个方法、适合新手参考。",
    "guaranteed_result": "改为不承诺结果的表述，例如：更容易、更清楚、减少重复步骤。",
    "false_authority": "只有真实来源和授权时才使用权威背书，否则删除。",
    "induced_engagement": "改为自然总结或保存理由，不要诱导点赞评论。",
    "external_diversion": "删除站外引流、联系方式和私域导流表达。",
    "qr_or_contact": "删除二维码、电话、微信、QQ 等联系入口。",
    "ai_disclosure": "确认是否需要标注概念图或 AI 生成，避免冒充真实证据。",
    "low_quality_risk": "改为原创结构、真实证据和分镜化表达。",
    "pseudo_chinese": "重新生成或改用 HyperFrames HTML 添加可编辑中文。",
}


def load_term_bank(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists() or path.stat().st_size == 0:
        return []
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            record = json.loads(stripped)
        except json.JSONDecodeError:
            records.append(
                {
                    "term": "",
                    "status": "invalid",
                    "level": "warning",
                    "category": "invalid_term_bank_record",
                    "source_report": str(path),
                    "line_number": line_number,
                }
            )
            continue
        term = str(record.get("term") or "").strip()
        if not term or str(record.get("status", "active")).strip().lower() not in {"active", "watch"}:
            continue
        records.append(record)
    return records


def load_text(paths: list[str], copy_path: str | None) -> tuple[str, list[str]]:
    checked: list[str] = []
    chunks: list[str] = []
    all_paths = list(paths)
    if copy_path:
        all_paths.insert(0, copy_path)
    if not all_paths:
        return sys.stdin.read(), ["stdin"]
    for raw in all_paths:
        path = Path(raw)
        checked.append(str(path))
        chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks), checked


def scan_risks(text: str) -> list[dict[str, Any]]:
    risks: list[dict[str, Any]] = []
    for rule in RISK_PATTERNS:
        for match in re.finditer(rule["pattern"], text, flags=re.IGNORECASE):
            category = rule["category"]
            risks.append(
                {
                    "level": rule["level"],
                    "category": category,
                    "text": match.group(0),
                    "start": match.start(),
                    "end": match.end(),
                    "suggestion": SUGGESTIONS.get(category, "请改为更安全、可证据支持的表达。"),
                }
            )
    return risks


def scan_learned_terms(text: str, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    risks: list[dict[str, Any]] = []
    for record in records:
        term = str(record.get("term") or "").strip()
        if not term:
            continue
        for match in re.finditer(re.escape(term), text, flags=re.IGNORECASE):
            category = str(record.get("category") or "learned_forbidden_term")
            risks.append(
                {
                    "level": str(record.get("level") or "error"),
                    "category": category,
                    "text": match.group(0),
                    "start": match.start(),
                    "end": match.end(),
                    "suggestion": str(record.get("suggestion") or "命中历史违规/风险词台账，请改写后重新检测。"),
                    "source": "forbidden_terms_learning_bank",
                    "first_seen_at": record.get("first_seen_at"),
                }
            )
    return risks


def parse_claim_ledger(text: str) -> list[dict[str, Any]]:
    claims: list[dict[str, Any]] = []
    in_ledger = False
    for line in text.splitlines():
        if "Claim Ledger" in line or "claim ledger" in line.lower():
            in_ledger = True
            continue
        if not in_ledger:
            continue
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("|") or "---" in stripped or "Claim" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 5:
            continue
        claim, claim_type, source, risk, safe_phrase = cells[:5]
        source_provided = bool(source and source not in {"无", "待补充", "none", "N/A"})
        claims.append(
            {
                "claim": claim,
                "type": claim_type,
                "source_required": claim_type not in {"opinion", "经验", "建议"},
                "source_provided": source_provided,
                "risk": risk,
                "safe_phrase": safe_phrase,
            }
        )
    return claims


def detect_unsourced_claims(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    risks: list[dict[str, Any]] = []
    for item in claims:
        if item["source_required"] and not item["source_provided"]:
            risks.append(
                {
                    "level": "error",
                    "category": "unsourced_claim",
                    "text": item["claim"],
                    "suggestion": "补充来源，或改写成经验/建议，不要作为事实断言。",
                }
            )
    return risks


def build_report(text: str, checked_files: list[str], term_bank_path: Path | None = DEFAULT_TERM_BANK) -> dict[str, Any]:
    learned_records = load_term_bank(term_bank_path)
    risk_items = scan_risks(text)
    risk_items.extend(scan_learned_terms(text, learned_records))
    claim_items = parse_claim_ledger(text)
    risk_items.extend(detect_unsourced_claims(claim_items))
    error_count = sum(1 for item in risk_items if item["level"] == "error")
    warning_count = sum(1 for item in risk_items if item["level"] == "warning")
    return {
        "status": "passed" if error_count == 0 else "failed",
        "checked_files": checked_files,
        "risk_items": risk_items,
        "claim_items": claim_items,
        "term_bank": {
            "path": str(term_bank_path) if term_bank_path else "",
            "active_terms_loaded": len(learned_records),
        },
        "summary": {
            "error_count": error_count,
            "warning_count": warning_count,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check public copy and output compliance_report.json.")
    parser.add_argument("paths", nargs="*", help="UTF-8 text files to scan. Reads stdin if omitted.")
    parser.add_argument("--copy", help="Copy package markdown file.")
    parser.add_argument("--out", help="Output compliance report JSON path.")
    parser.add_argument("--json", action="store_true", help="Print JSON report to stdout.")
    parser.add_argument(
        "--term-bank",
        default=str(DEFAULT_TERM_BANK),
        help="JSONL learned forbidden/risk term bank. Defaults to references/forbidden_terms_learning_bank.jsonl.",
    )
    args = parser.parse_args()

    text, checked_files = load_text(args.paths, args.copy)
    term_bank_path = Path(args.term_bank) if args.term_bank else None
    report = build_report(text, checked_files, term_bank_path)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.json or not args.out:
        print(json.dumps(report, ensure_ascii=False, indent=2))

    return 1 if report["summary"]["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
