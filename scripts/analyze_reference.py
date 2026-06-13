#!/usr/bin/env python3
"""Analyze a Douyin reference input without copying protected expression."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any


def classify_reference(value: str) -> str:
    path = Path(value).expanduser()
    if path.exists():
        return "local_video"
    if re.search(r"https?://", value) and "douyin" in value.lower():
        return "douyin_url"
    return "share_text"


def probe_duration(path: Path) -> float:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return round(float(result.stdout.strip()), 3)
    except Exception:
        return 0.0


def similarity_risk(text: str) -> str:
    high_patterns = ["一模一样", "照抄", "原字幕", "原文案", "原声音", "不要改"]
    medium_patterns = ["90%", "百分之90", "高度相似", "尽量一样"]
    if any(pattern in text for pattern in high_patterns):
        return "high"
    if any(pattern in text for pattern in medium_patterns):
        return "medium"
    return "low"


def build_analysis(raw_input: str) -> dict[str, Any]:
    reference_type = classify_reference(raw_input)
    duration = probe_duration(Path(raw_input).expanduser()) if reference_type == "local_video" else 0.0
    risk = similarity_risk(raw_input)
    topic = "AI 圈知识短视频参考" if reference_type != "share_text" else raw_input[:80]
    return {
        "reference_type": reference_type,
        "duration_seconds": duration,
        "aspect_ratio": "unknown",
        "topic": topic,
        "structure": [
            {
                "segment": "hook",
                "start": 0,
                "end": 5,
                "purpose": "制造痛点或好奇",
                "visual_style": "to be derived from inspected frames or share text",
                "copy_role": "stop scrolling and promise a payoff",
            },
            {
                "segment": "body",
                "start": 5,
                "end": duration if duration else 45,
                "purpose": "解释方法并展示证据",
                "visual_style": "real UI, proof, or structured cards",
                "copy_role": "teach one useful method",
            },
        ],
        "what_to_learn": ["节奏", "信息层级", "场景切换方式", "开头钩子结构"],
        "what_not_to_copy": ["原字幕", "原声音", "原素材", "原音乐", "原完整文案", "原博主个人表达"],
        "originality_plan": {
            "new_angle": "围绕当前 AI 圈选题重新定义观点和证据",
            "new_visuals": "使用真实 UI、真实输出、原创信息图和新的 HyperFrames 视觉系统",
            "new_script": "使用原创中文口播，保留结构启发但不复用原句",
            "similarity_risk": risk,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze reference video/link/share text for V2 workflow.")
    parser.add_argument("--input", help="Douyin URL, share text, or local video path.")
    parser.add_argument("--text", help="Legacy alias for --input.")
    parser.add_argument("--out", required=True, help="Output reference_analysis.json path.")
    parser.add_argument("--project-dir", help="Accepted for backward compatibility; not required in V2.")
    args = parser.parse_args()

    raw_input = args.input or args.text
    if not raw_input:
        parser.error("--input is required")
    analysis = build_analysis(raw_input)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(analysis, ensure_ascii=False, indent=2))
    return 1 if analysis["originality_plan"]["similarity_risk"] == "high" else 0


if __name__ == "__main__":
    raise SystemExit(main())
