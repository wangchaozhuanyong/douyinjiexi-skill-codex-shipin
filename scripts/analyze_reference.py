#!/usr/bin/env python3
"""Create a Douyin remake analysis JSON from share text or URLs.

This script reuses the local desktop parser project instead of duplicating
Douyin parsing and compliance logic in the skill.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict


DEFAULT_PROJECT_DIR = Path("/Users/wangchao/Desktop/抖音解析")


def load_server_module(project_dir: Path):
    project_dir = project_dir.expanduser().resolve()
    if not (project_dir / "douyin_media_server.py").exists():
        raise FileNotFoundError(f"找不到 douyin_media_server.py: {project_dir}")
    sys.path.insert(0, str(project_dir))
    import douyin_media_server  # type: ignore

    return douyin_media_server


def build_analysis(server: Any, text: str) -> Dict[str, Any]:
    urls = server.extract_urls([text])
    url = urls[0] if urls else ""
    record = server.douyin_share_record(url, text) if url else None
    package = server.make_original_remake_package(url, text, record)
    preview = server.build_reference_previews(text, max_items=1)
    return {
        "ok": True,
        "input_text": text,
        "url": url,
        "preview": preview[0] if preview else {},
        "package": package,
        "reference_analysis": package.get("reference_analysis") or {},
        "shot_list": package.get("shot_list") or [],
        "voiceover": package.get("voiceover") or [],
        "publish_caption": package.get("publish_caption") or "",
        "compliance": package.get("compliance") or {},
        "draft_compliance": package.get("draft_compliance") or {},
        "originality": package.get("originality") or {},
        "compliance_sources": package.get("compliance_sources") or [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Douyin share text for HyperFrames remake workflow.")
    parser.add_argument("--text", required=True, help="Douyin URL or copied share text.")
    parser.add_argument("--out", required=True, help="Output JSON path.")
    parser.add_argument("--project-dir", default=str(DEFAULT_PROJECT_DIR), help="Local Douyin parser project directory.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        server = load_server_module(Path(args.project_dir))
        analysis = build_analysis(server, args.text)
    except Exception as exc:
        analysis = {
            "ok": False,
            "input_text": args.text,
            "error": str(exc),
            "fallback_note": "解析脚本失败；可继续基于用户粘贴的分享文案手动拆解，但需在成片说明中标注解析限制。",
        }
    out_path.write_text(json.dumps(analysis, ensure_ascii=False, indent=2), "utf-8")
    print(out_path)
    return 0 if analysis.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
