#!/usr/bin/env python3
"""Export approved on-screen text timing from a storyboard.

This is a deterministic manifest for the HyperFrames composition layer. It is
not OCR: the rendered HTML should use this same text inventory, then
``check_screen_text.py`` verifies the final render text against approvals.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(value: Any) -> str:
    return str(value or "").strip()


def number(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def append_text(
    texts: list[dict[str, Any]],
    *,
    shot_id: str,
    role: str,
    text: str,
    start_sec: float,
    end_sec: float,
) -> None:
    if not text:
        return
    texts.append(
        {
            "shot_id": shot_id,
            "role": role,
            "text": text,
            "start_sec": round(start_sec, 3),
            "end_sec": round(end_sec, 3),
        }
    )


def export_manifest(storyboard: dict[str, Any]) -> dict[str, Any]:
    texts: list[dict[str, Any]] = []
    cursor = 0.0
    scene_timing = scene_timing_by_id(storyboard)
    shots = storyboard.get("director_shots", [])
    if isinstance(shots, list) and shots:
        for index, shot in enumerate(shots, start=1):
            if not isinstance(shot, dict):
                continue
            shot_id = normalize(shot.get("shot_id")) or f"SHOT{index:02d}"
            duration = number(shot.get("duration_sec"), 0.0)
            if shot_id in scene_timing:
                start_sec, end_sec = scene_timing[shot_id]
            else:
                start_sec = cursor
                end_sec = cursor + max(duration, 0.0)
            text = shot.get("on_screen_text", {})
            if isinstance(text, dict):
                append_text(
                    texts,
                    shot_id=shot_id,
                    role="primary_title",
                    text=normalize(text.get("primary")),
                    start_sec=start_sec,
                    end_sec=end_sec,
                )
                for item in text.get("secondary", []) or []:
                    append_text(
                        texts,
                        shot_id=shot_id,
                        role="secondary",
                        text=normalize(item),
                        start_sec=start_sec,
                        end_sec=end_sec,
                    )
            cursor = end_sec
    else:
        for index, scene in enumerate(storyboard.get("scenes", []) or [], start=1):
            if not isinstance(scene, dict):
                continue
            shot_id = normalize(scene.get("scene_id")) or f"S{index:02d}"
            start_sec = number(scene.get("sync", {}).get("caption_start"), cursor) if isinstance(scene.get("sync"), dict) else cursor
            duration = number(scene.get("duration_target"), 0.0)
            end_sec = number(scene.get("sync", {}).get("caption_end"), start_sec + duration) if isinstance(scene.get("sync"), dict) else start_sec + duration
            append_text(
                texts,
                shot_id=shot_id,
                role="large_caption",
                text=normalize(scene.get("caption")),
                start_sec=start_sec,
                end_sec=end_sec,
            )
            for item in scene.get("on_screen_text", []) or []:
                append_text(
                    texts,
                    shot_id=shot_id,
                    role="secondary",
                    text=normalize(item),
                    start_sec=start_sec,
                    end_sec=end_sec,
                )
            cursor = max(cursor, end_sec)

    return {
        "version": 1,
        "source": "storyboard",
        "title": storyboard.get("title", ""),
        "texts": texts,
    }


def scene_timing_by_id(storyboard: dict[str, Any]) -> dict[str, tuple[float, float]]:
    timing: dict[str, tuple[float, float]] = {}
    cursor = 0.0
    scenes = storyboard.get("scenes", [])
    if not isinstance(scenes, list):
        return timing
    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            continue
        scene_id = normalize(scene.get("scene_id")) or f"S{index:02d}"
        duration = number(scene.get("duration_target"), 0.0)
        sync = scene.get("sync", {}) if isinstance(scene.get("sync"), dict) else {}
        start_sec = number(sync.get("caption_start"), cursor)
        end_sec = number(sync.get("caption_end"), start_sec + duration)
        timing[scene_id] = (start_sec, end_sec)
        cursor = max(cursor, end_sec)
    return timing


def main() -> int:
    parser = argparse.ArgumentParser(description="Export render_text_manifest.json from storyboard text approvals.")
    parser.add_argument("--storyboard", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    report = export_manifest(load_json(Path(args.storyboard)))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
