#!/usr/bin/env python3
"""Scan public-facing Chinese video copy for common short-video risk terms."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


RISK_TERMS: dict[str, list[str]] = {
    "absolute_or_exaggerated": [
        "最强",
        "第一",
        "唯一",
        "保证",
        "100%",
        "百分百",
        "永久",
        "必火",
        "必爆",
        "包成功",
    ],
    "false_authority": [
        "官方认证",
        "国家级",
        "央视推荐",
        "权威背书",
        "专家推荐",
    ],
    "money_or_result_promise": [
        "秒赚",
        "暴富",
        "无风险",
        "稳赚",
        "包过",
        "躺赚",
    ],
    "external_diversion": [
        "微信",
        "VX",
        "vx",
        "QQ",
        "加群",
        "扫码",
        "电话",
        "私信领取",
        "联系方式",
    ],
    "fake_proof": [
        "真实客户评价",
        "客户好评截图",
        "官方通知",
        "认证证书",
        "平台背书",
    ],
}


PSEUDO_CHINESE_PATTERNS = [
    re.compile(r"[口囗□�]{2,}"),
]


def scan_text(text: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for category, terms in RISK_TERMS.items():
        for term in terms:
            for match in re.finditer(re.escape(term), text):
                findings.append(
                    {
                        "category": category,
                        "term": term,
                        "start": match.start(),
                        "end": match.end(),
                    }
                )

    for pattern in PSEUDO_CHINESE_PATTERNS:
        for match in pattern.finditer(text):
            token = match.group(0)
            findings.append(
                {
                    "category": "possible_unreadable_or_pseudo_chinese",
                    "term": token[:20],
                    "start": match.start(),
                    "end": match.end(),
                }
            )
    return findings


def read_input(paths: list[str]) -> str:
    if not paths:
        return sys.stdin.read()

    chunks = []
    for raw_path in paths:
        path = Path(raw_path)
        chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan title, hook, voiceover, subtitles, cover copy, captions, hashtags, and image-text plans."
    )
    parser.add_argument("paths", nargs="*", help="UTF-8 text files to scan. Reads stdin when omitted.")
    parser.add_argument("--json", action="store_true", help="Print JSON findings.")
    args = parser.parse_args()

    text = read_input(args.paths)
    findings = scan_text(text)

    if args.json:
        print(json.dumps({"ok": not findings, "findings": findings}, ensure_ascii=False, indent=2))
    elif findings:
        print("Risk terms found:")
        for finding in findings:
            print(f"- {finding['category']}: {finding['term']}")
    else:
        print("No local risk terms found.")

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
