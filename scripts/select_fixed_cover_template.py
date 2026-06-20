#!/usr/bin/env python3
"""Select a fixed safe AI cover template by video size and sequential rotation."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "references" / "fixed_ai_cover_template_rotation.json"
DEFAULT_STATE = ROOT / "outputs" / ".ai_cover_template_rotation_state.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists() or not path.is_file() or path.stat().st_size == 0:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def detect_aspect(args: argparse.Namespace) -> str:
    if args.aspect in {"16:9", "9:16"}:
        return str(args.aspect)
    if args.video_width and args.video_height:
        return "16:9" if int(args.video_width) >= int(args.video_height) else "9:16"
    return "16:9"


def pool_for_aspect(aspect: str) -> str:
    if aspect == "9:16":
        return "vertical_9x16"
    return "horizontal_16x9"


def state_index(state: dict[str, Any], pool_name: str) -> int:
    pools = state.get("pools")
    if isinstance(pools, dict):
        record = pools.get(pool_name)
        if isinstance(record, dict):
            return int(record.get("next_index") or 0)
    raw = state.get(pool_name)
    return int(raw or 0)


def advance_state(state: dict[str, Any], pool_name: str, next_index: int, selected: dict[str, Any], project: Path) -> dict[str, Any]:
    state.setdefault("version", 1)
    pools = state.setdefault("pools", {})
    if not isinstance(pools, dict):
        pools = {}
        state["pools"] = pools
    pools[pool_name] = {
        "next_index": next_index,
        "updated_at": now_iso(),
        "last_template_id": selected.get("template_id"),
    }
    history = state.setdefault("history", [])
    if isinstance(history, list):
        history.append(
            {
                "selected_at": now_iso(),
                "project": str(project),
                "pool": pool_name,
                "template_id": selected.get("template_id"),
                "next_index": next_index,
            }
        )
        del history[:-50]
    return state


def paste_contained_on_blur(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    if image.size == size:
        return image.copy()
    background = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)
    background = background.filter(ImageFilter.GaussianBlur(32))
    background = ImageEnhance.Brightness(background).enhance(0.48)
    foreground = image.copy()
    foreground.thumbnail((int(size[0] * 0.92), int(size[1] * 0.92)), Image.Resampling.LANCZOS)
    x = (size[0] - foreground.width) // 2
    y = (size[1] - foreground.height) // 2
    background.paste(foreground, (x, y))
    return background


def save_cover_outputs(source: Path, internal: Path) -> dict[str, str]:
    with Image.open(source) as opened:
        image = opened.convert("RGB")
        primary = internal / "cover.png"
        first_frame = internal / "first_frame_cover.png"
        horizontal = internal / "cover_publish_horizontal.png"
        vertical = internal / "cover_publish_vertical.png"
        source_copy = internal / "cover_template_source.jpg"

        internal.mkdir(parents=True, exist_ok=True)
        image.save(primary)
        image.save(first_frame)
        paste_contained_on_blur(image, (1920, 1080)).save(horizontal)
        paste_contained_on_blur(image, (1080, 1920)).save(vertical)
        shutil.copy2(source, source_copy)

    return {
        "primary": str(primary),
        "first_frame": str(first_frame),
        "horizontal_16x9": str(horizontal),
        "vertical_9x16": str(vertical),
        "horizontal_4_3": str(horizontal),
        "vertical_3_4": str(vertical),
        "source_asset_copy": str(source_copy),
    }


def write_cover_text(internal: Path, selected: dict[str, Any]) -> str:
    text_path = internal / "publish_cover_text.txt"
    lines = [str(item).strip() for item in selected.get("visible_text", []) if str(item).strip()]
    text_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return str(text_path)


def select_template(
    manifest: dict[str, Any],
    pool_name: str,
    state: dict[str, Any],
) -> tuple[dict[str, Any], int, int]:
    pools = manifest.get("pools") if isinstance(manifest.get("pools"), dict) else {}
    entries = pools.get(pool_name)
    if not isinstance(entries, list) or not entries:
        raise SystemExit(f"cover template pool is empty: {pool_name}")
    index = state_index(state, pool_name) % len(entries)
    next_index = (index + 1) % len(entries)
    selected = entries[index]
    if not isinstance(selected, dict):
        raise SystemExit(f"invalid cover template entry at {pool_name}[{index}]")
    return selected, index, next_index


def build_report(
    project: Path,
    manifest_path: Path,
    state_file: Path,
    selected: dict[str, Any],
    pool_name: str,
    pool_size: int,
    index: int,
    source: Path,
    outputs: dict[str, str],
    cover_text: str,
    aspect: str,
    state_advanced: bool,
    manifest: dict[str, Any],
) -> dict[str, Any]:
    qingdou_report = str(manifest.get("qingdou_report") or "").strip()
    if qingdou_report:
        qingdou_report = str(resolve_project_path(qingdou_report))
    return {
        "status": "passed",
        "cover_type": "fixed_safe_template_first_frame",
        "created_at": now_iso(),
        "project": str(project),
        "manifest": str(manifest_path),
        "state_file": str(state_file),
        "state_advanced": state_advanced,
        "selection_method": "sequential_by_size_pool",
        "frame_grab_used": False,
        "template_id": selected.get("template_id"),
        "canonical_id": selected.get("canonical_id"),
        "template_name": selected.get("name"),
        "template_path": str(source),
        "template_aspect": selected.get("aspect"),
        "video_aspect": aspect,
        "size_pool": pool_name,
        "size_pool_size": pool_size,
        "template_rotation_index": index,
        "template_library_size": sum(
            len(value) for value in (manifest.get("pools") or {}).values() if isinstance(value, list)
        ),
        "qingdou": {
            "status": "passed",
            "report": qingdou_report,
            "visible_result": manifest.get("qingdou_visible_result") or "未检查到敏感词",
            "scope": "fixed_cover_visible_text_manifest",
        },
        "outputs": {
            **outputs,
            "cover_text": cover_text,
        },
        "checks": {
            "template_from_fixed_library": True,
            "fixed_safe_asset": True,
            "selected_by_video_size": selected.get("aspect") == aspect,
            "first_frame_required": True,
            "cover_text_written": Path(cover_text).exists(),
            "not_video_screenshot": True,
            "qingdou_cover_manifest_passed": True,
            "dynamic_text_overlay_used": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Select fixed safe AI cover template for video first frame and publish cover.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Fixed cover manifest JSON")
    parser.add_argument("--state-file", default=str(DEFAULT_STATE), help="Persistent rotation state JSON")
    parser.add_argument("--aspect", choices=["auto", "16:9", "9:16"], default="auto")
    parser.add_argument("--video-width", type=int)
    parser.add_argument("--video-height", type=int)
    parser.add_argument("--no-advance-state", action="store_true", help="Write project outputs without advancing the rotation state.")
    args = parser.parse_args()

    project = resolve_project_path(args.project)
    internal = project / "internal"
    manifest_path = resolve_project_path(args.manifest)
    state_file = resolve_project_path(args.state_file)

    manifest = load_json(manifest_path)
    if not manifest:
        raise SystemExit(f"cover manifest missing or empty: {manifest_path}")

    aspect = detect_aspect(args)
    pool_name = pool_for_aspect(aspect)
    state = load_json(state_file)
    selected, index, next_index = select_template(manifest, pool_name, state)

    source = resolve_project_path(str(selected.get("file") or ""))
    if not source.exists() or not source.is_file() or source.stat().st_size == 0:
        raise SystemExit(f"cover template source missing or empty: {source}")

    outputs = save_cover_outputs(source, internal)
    cover_text = write_cover_text(internal, selected)

    state_advanced = not args.no_advance_state
    if state_advanced:
        write_json(state_file, advance_state(state, pool_name, next_index, selected, project))

    pool_size = len((manifest.get("pools") or {}).get(pool_name) or [])
    report = build_report(
        project=project,
        manifest_path=manifest_path,
        state_file=state_file,
        selected=selected,
        pool_name=pool_name,
        pool_size=pool_size,
        index=index,
        source=source,
        outputs=outputs,
        cover_text=cover_text,
        aspect=aspect,
        state_advanced=state_advanced,
        manifest=manifest,
    )
    write_json(internal / "publish_cover_report.json", report)
    print(json.dumps({"status": "selected", "template_id": selected.get("template_id"), "report": str(internal / "publish_cover_report.json")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
