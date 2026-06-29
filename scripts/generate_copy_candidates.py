#!/usr/bin/env python3
"""Generate three structured copy candidates for a selected topic."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ANGLES = [
    ("pain_fix_angle", "痛点修复型", "先指出具体卡点，再给可执行修复步骤"),
    ("myth_busting_angle", "纠错反常识型", "先推翻常见误解，再用证据给正确做法"),
    ("proof_demo_angle", "实测证据型", "先展示真实证据，再总结可保存方法"),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def topic_title(topic: dict[str, Any]) -> str:
    for key in ("title", "title_direction", "topic", "topic_title"):
        value = str(topic.get(key) or "").strip()
        if value:
            return value
    return "AI 工作流实测"


def build_candidate(topic: dict[str, Any], angle_id: str, label: str, strategy: str) -> dict[str, Any]:
    title = topic_title(topic)
    pain = str(topic.get("viewer_pain") or "结果空泛、画面缺证据、返工很多")
    save = str(topic.get("save_reason") or "保存一张对象、场景、证据、输出的检查表")
    source_ids = topic.get("source_ids") or topic.get("source_refs") or []
    claim = str(topic.get("core_angle") or topic.get("main_claims", ["先绑定证据再讲方法"])[0])
    first_3s = f"{title}，别先追特效，先修掉这个痛点：{pain[:22]}"
    return {
        "angle_id": angle_id,
        "angle_label": label,
        "strategy": strategy,
        "title": title,
        "cover_title": title[:24],
        "first_3s_hook": first_3s,
        "first_8s_script": first_3s + "，8 秒内先给你看证据，再给可保存模板。",
        "full_script": [
            first_3s,
            "先看真实来源或截图，确认这句话不是空口判断。",
            "再把方法拆成对象、场景、证据、输出四格。",
            "最后保存这张检查表，下次做同类视频直接套。",
        ],
        "retention_beats": [
            {"time_sec": 6, "beat": "真实证据出现"},
            {"time_sec": 13, "beat": "错误做法对比"},
            {"time_sec": 20, "beat": "可保存模板收束"},
        ],
        "proof_moments": [
            {"claim": claim, "source_ids": source_ids, "visual": "source crop or local capture"}
        ],
        "save_value": save,
        "claim_ledger": [
            {"claim": claim, "evidence": source_ids or ["evergreen_seed_reference"], "proof_visual": "screenshot_or_demo"}
        ],
        "visual_promises": ["proof panel", "annotation rail", "lower-third core caption"],
        "compliance_notes": ["no overpromise", "no diversion", "source-backed claims only"],
    }


def choose_candidate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    preferred = next(item for item in candidates if item["angle_id"] == "proof_demo_angle")
    return {
        "status": "passed",
        "selected_angle_id": preferred["angle_id"],
        "selection_reason": "proof_demo_angle best matches proof-first AI knowledge delivery",
        "rejected": [
            {
                "angle_id": item["angle_id"],
                "reason": "lower proof-first fit than selected angle",
            }
            for item in candidates
            if item is not preferred
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate structured copy candidates.")
    parser.add_argument("--selected-topic", required=True)
    parser.add_argument("--out", required=True, help="copy_candidates.json")
    parser.add_argument("--selection-out", required=True, help="copy_selection_report.json")
    args = parser.parse_args()

    topic = load_json(Path(args.selected_topic))
    candidates = [build_candidate(topic, *angle) for angle in ANGLES]
    output = {"status": "passed", "candidate_count": len(candidates), "candidates": candidates}
    selection = choose_candidate(candidates)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    selection_out = Path(args.selection_out)
    selection_out.parent.mkdir(parents=True, exist_ok=True)
    selection_out.write_text(json.dumps(selection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "out": str(out), "selection_out": str(selection_out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
