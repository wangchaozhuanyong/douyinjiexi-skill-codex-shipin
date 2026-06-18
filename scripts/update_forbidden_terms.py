#!/usr/bin/env python3
"""Append detected Douyin risk terms to the learned forbidden-term bank."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_BANK = Path("references/forbidden_terms_learning_bank.jsonl")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_term(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def stable_id(term: str, category: str, source_platform: str) -> str:
    raw = f"{term}|{category}|{source_platform}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def existing_ids(bank: Path) -> set[str]:
    ids: set[str] = set()
    if not bank.exists() or bank.stat().st_size == 0:
        return ids
    for line in bank.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            record = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        record_id = str(record.get("id") or "").strip()
        if record_id:
            ids.add(record_id)
    return ids


def context_from_item(item: dict[str, Any], report: dict[str, Any]) -> str:
    for key in ["context", "field", "source_field", "checked_field", "where"]:
        value = normalize_term(item.get(key))
        if value:
            return value
    checked_files = report.get("checked_files")
    if isinstance(checked_files, list) and checked_files:
        return ", ".join(str(path) for path in checked_files[:3])
    return ""


def records_from_local_report(report: dict[str, Any], source_report: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for item in report.get("risk_items", []) or []:
        if not isinstance(item, dict):
            continue
        term = normalize_term(item.get("text"))
        if not term:
            continue
        category = normalize_term(item.get("category")) or "local_copy_risk"
        level = normalize_term(item.get("level")) or "warning"
        source_platform = "local_check_public_copy"
        records.append(
            {
                "id": stable_id(term, category, source_platform),
                "term": term,
                "level": level,
                "category": category,
                "source_platform": source_platform,
                "source_report": str(source_report),
                "context": context_from_item(item, report),
                "suggestion": normalize_term(item.get("suggestion")) or "改写为更安全、可证据支持的表达。",
                "first_seen_at": datetime.now(timezone.utc).isoformat(),
                "status": "active",
            }
        )
    return records


def qingdou_items(report: dict[str, Any]) -> list[Any]:
    candidates: list[Any] = []
    final_check = report.get("final_check")
    if isinstance(final_check, dict):
        candidates.extend(final_check.get("items") or [])
        candidates.extend(final_check.get("forbidden_words") or [])
        candidates.extend(final_check.get("sensitive_words") or [])
        candidates.extend(final_check.get("replacement_suggestions") or [])
    for key in ["items", "forbidden_words", "sensitive_words", "risk_items", "suggestions"]:
        candidates.extend(report.get(key) or [])
    return candidates


def records_from_qingdou_report(report: dict[str, Any], source_report: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for raw_item in qingdou_items(report):
        item = raw_item if isinstance(raw_item, dict) else {"term": raw_item}
        term = normalize_term(
            item.get("term")
            or item.get("text")
            or item.get("word")
            or item.get("keyword")
            or item.get("sensitive_word")
            or item.get("forbidden_word")
        )
        if not term:
            continue
        category = normalize_term(item.get("category") or item.get("type")) or "qingdou_sensitive_term"
        level = normalize_term(item.get("level") or item.get("severity")) or "error"
        source_platform = "qingdou"
        records.append(
            {
                "id": stable_id(term, category, source_platform),
                "term": term,
                "level": level,
                "category": category,
                "source_platform": source_platform,
                "source_report": str(source_report),
                "context": context_from_item(item, report),
                "suggestion": normalize_term(item.get("suggestion") or item.get("replacement")) or "按轻抖建议改写后重新检测。",
                "first_seen_at": datetime.now(timezone.utc).isoformat(),
                "status": "active",
            }
        )
    return records


def records_from_report(report_path: Path) -> list[dict[str, Any]]:
    report = load_json(report_path)
    records = records_from_local_report(report, report_path)
    records.extend(records_from_qingdou_report(report, report_path))
    return records


def append_records(bank: Path, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    bank.parent.mkdir(parents=True, exist_ok=True)
    seen = existing_ids(bank)
    appended: list[dict[str, Any]] = []
    with bank.open("a", encoding="utf-8") as handle:
        for record in records:
            record_id = str(record.get("id") or "").strip()
            if not record_id or record_id in seen:
                continue
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            seen.add(record_id)
            appended.append(record)
    return appended


def main() -> int:
    parser = argparse.ArgumentParser(description="Append detected risk terms to forbidden_terms_learning_bank.jsonl.")
    parser.add_argument("--report", action="append", required=True, help="Compliance or Qingdou JSON report. Can be repeated.")
    parser.add_argument("--bank", default=str(DEFAULT_BANK), help="Target JSONL forbidden term bank.")
    parser.add_argument("--out", help="Optional JSON update report path.")
    args = parser.parse_args()

    all_records: list[dict[str, Any]] = []
    for raw_report in args.report:
        all_records.extend(records_from_report(Path(raw_report)))

    appended = append_records(Path(args.bank), all_records)
    result = {
        "status": "updated" if appended else "no_new_terms",
        "bank": args.bank,
        "records_found": len(all_records),
        "records_appended": len(appended),
        "appended_terms": [record["term"] for record in appended],
    }
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
