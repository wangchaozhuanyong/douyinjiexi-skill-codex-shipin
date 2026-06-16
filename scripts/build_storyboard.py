#!/usr/bin/env python3
"""Create a starter storyboard from copy text for manual refinement."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def split_voice(text: str) -> list[str]:
    lines = [item.strip() for item in re.split(r"[。！？\n]+", text) if item.strip()]
    if len(lines) < 6:
        lines.extend(["补充真实证据画面", "总结可保存方法"][: 6 - len(lines)])
    return lines[:6]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a starter storyboard skeleton.")
    parser.add_argument("--copy", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    text = Path(args.copy).read_text(encoding="utf-8")
    voices = split_voice(text)
    scenes = []
    elapsed = 0.0
    for idx, voice in enumerate(voices, start=1):
        duration = 3.5
        scene_type = "screenshot_proof" if idx in {1, 3, 5} else "text_card"
        scenes.append(
            {
                "scene_id": f"S{idx:02d}",
                "concept": "starter single concept",
                "duration_target": duration,
                "voice": voice,
                "caption": voice[:18],
                "on_screen_text": [voice[:10]],
                "visual": {
                    "scene_type": scene_type,
                    "description": "需要替换为真实证据或设计卡片",
                    "evidence_source": "real_ui_screenshot" if scene_type == "screenshot_proof" else "designed_card",
                    "asset_path": f"assets/screenshots/s{idx:02d}.png",
                },
                "motion": {
                    "background_motion": "subtle drift",
                    "foreground_motion": "panel insert",
                    "callout_motion": "highlight current point",
                    "transition": "cut",
                    "purpose": "reveal",
                    "entrance": "0.6s cinematic fade-up from y=20px opacity 0",
                    "stagger": "0.12s-0.18s between title/cards",
                    "keyword_motion": "subtle scale-pop max 1.08x for 0.25s",
                    "camera_motion": "background push-in 100% to 103%, foreground stable",
                    "layering": "background parallax + foreground stable + callout reveal",
                    "caption_motion": "keyword highlight only, no every-word bouncing",
                    "glow": "ambient glow opacity 8%-18%, no flicker",
                    "audio_reactive": "text 3%-5%, background glow 10%-15%",
                    "negative_motion": "no excessive bounce, no chaotic movement, no glitch spam",
                },
                "sync": {
                    "voice_start": elapsed,
                    "voice_end": elapsed + duration,
                    "caption_start": elapsed,
                    "caption_end": elapsed + duration,
                    "narration_track": "continuous_root_audio",
                    "transition_audio_policy": "visual-only transition; narration continues with no restart or mute",
                    "max_audio_gap_ms": 80,
                    "audio_bridge": "continuous narration bed under visual transition; SFX stays below voice",
                },
                "safe_zone": {
                    "top_reserved": True,
                    "bottom_caption_reserved": True,
                    "right_buttons_reserved": True,
                    "top_margin_px": 240,
                    "bottom_margin_px": 360,
                    "left_margin_px": 72,
                    "right_margin_px": 180,
                    "critical_content_inside_safe_area": True,
                },
                "beat_map": [
                    {
                        "voice_fragment": voice[:18],
                        "visual_action": "展示与当前口播对应的证据画面或结构卡片",
                        "caption": voice[:18],
                        "proof_or_explanation": "starter beat; replace with real proof, contrast, template, result, or save value",
                        "motion_trigger": "panel insert and highlight current point",
                    }
                ],
                "qa_notes": ["starter storyboard; replace placeholder assets before production"],
            }
        )
        elapsed += duration
    result = {
        "title": "starter storyboard",
        "target": {"width": 1920, "height": 1080, "fps": 30, "tts_speed": 1.0, "voice_speed_policy": "normal"},
        "scenes": scenes,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
