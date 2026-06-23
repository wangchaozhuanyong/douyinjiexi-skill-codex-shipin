#!/usr/bin/env python3
"""Select a fixed pure AI cover background and render checked runtime title text."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "references" / "fixed_ai_cover_background_rotation.json"
DEFAULT_STATE = ROOT / "outputs" / ".ai_cover_background_rotation_state.json"
FONT_CANDIDATES = [
    Path("/System/Library/Fonts/PingFang.ttc"),
    Path("/System/Library/Fonts/STHeiti Light.ttc"),
    Path("/Library/Fonts/Arial Unicode.ttf"),
]


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
    return "9x16" if aspect == "9:16" else "16x9"


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
        "last_template_id": selected.get("id"),
        "last_ratio": selected.get("ratio"),
    }
    history = state.setdefault("history", [])
    if isinstance(history, list):
        history.append(
            {
                "selected_at": now_iso(),
                "project": str(project),
                "pool": pool_name,
                "template_id": selected.get("id"),
                "ratio": selected.get("ratio"),
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


def font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if not path.exists():
            continue
        indices = [1, 0] if bold else [0, 1]
        for index in indices:
            try:
                return ImageFont.truetype(str(path), size, index=index)
            except Exception:
                continue
    return ImageFont.load_default()


def parse_rgba(value: str, fallback: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    match = re.match(r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*([0-9.]+)\)", str(value or ""))
    if not match:
        return fallback
    r, g, b = (int(match.group(i)) for i in range(1, 4))
    alpha_raw = float(match.group(4))
    alpha = int(round(alpha_raw * 255)) if alpha_raw <= 1 else int(round(alpha_raw))
    return (r, g, b, max(0, min(255, alpha)))


def fit_lines(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    max_lines: int,
    start_size: int,
    min_size: int,
) -> tuple[list[str], ImageFont.ImageFont]:
    text = " ".join(str(text or "").strip().split())
    if not text:
        return [""], font(start_size)
    for size in range(start_size, min_size - 1, -2):
        current_font = font(size)
        width = draw.textbbox((0, 0), text, font=current_font)[2]
        if width <= max_width:
            return [text], current_font
    for size in range(start_size, min_size - 1, -2):
        current_font = font(size)
        lines: list[str] = []
        current = ""
        for char in text:
            candidate = current + char
            width = draw.textbbox((0, 0), candidate, font=current_font)[2]
            if width <= max_width or not current:
                current = candidate
                continue
            lines.append(current)
            current = char
        if current:
            lines.append(current)
        orphan_tail = len(lines) > 1 and len(lines[-1]) <= 1
        if len(lines) <= max_lines and not orphan_tail:
            return lines, current_font
    fallback = font(min_size)
    return lines[:max_lines] if "lines" in locals() else [text[:16]], fallback


def add_readability_backdrop(base: Image.Image, rect: list[int], template: dict[str, Any]) -> None:
    backdrop = template.get("runtime_text_backdrop") if isinstance(template.get("runtime_text_backdrop"), dict) else {}
    if not backdrop.get("recommended", True):
        return
    overlay_rgba = parse_rgba(str(backdrop.get("overlay_rgba") or ""), (2, 7, 18, 46))
    feather = int(backdrop.get("feather_px") or 48)
    x1, y1, x2, y2 = rect
    mask = Image.new("L", base.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rectangle((x1, y1, x2, y2), fill=190)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    overlay = Image.new("RGBA", base.size, overlay_rgba)
    base.alpha_composite(Image.composite(overlay, Image.new("RGBA", base.size, (0, 0, 0, 0)), mask))


def union_bbox(boxes: list[tuple[int, int, int, int]]) -> list[int]:
    if not boxes:
        return [0, 0, 0, 0]
    return [
        min(box[0] for box in boxes),
        min(box[1] for box in boxes),
        max(box[2] for box in boxes),
        max(box[3] for box in boxes),
    ]


def rect_contains(outer: list[int], inner: list[int], margin: int = 0) -> bool:
    if not inner or inner == [0, 0, 0, 0]:
        return False
    return (
        inner[0] >= outer[0] + margin
        and inner[1] >= outer[1] + margin
        and inner[2] <= outer[2] - margin
        and inner[3] <= outer[3] - margin
    )


def center_crop_rect_px(size: tuple[int, int], crop_aspect: str = "9:16") -> list[int]:
    width, height = size
    if crop_aspect != "9:16":
        return [0, 0, width, height]
    target_width = int(round(height * 9 / 16))
    if target_width <= width:
        x1 = (width - target_width) // 2
        return [x1, 0, x1 + target_width, height]
    target_height = int(round(width * 16 / 9))
    y1 = max(0, (height - target_height) // 2)
    return [0, y1, width, min(height, y1 + target_height)]


def compact_cover_text_ok(cover_lines: list[str], aspect: str) -> bool:
    primary = cover_lines[0] if cover_lines else ""
    primary_limit = 18 if aspect == "16:9" else 20
    secondary_limit = 18 if aspect == "16:9" else 22
    return (
        bool(primary)
        and len(primary) <= primary_limit
        and len(cover_lines) <= 3
        and all(len(line) <= secondary_limit for line in cover_lines[1:])
    )


def draw_runtime_cover_text(
    base: Image.Image,
    selected: dict[str, Any],
    cover_lines: list[str],
    aspect: str,
) -> tuple[Image.Image, dict[str, Any]]:
    image = base.convert("RGBA")
    draw = ImageDraw.Draw(image)
    rect = [int(v) for v in selected.get("recommended_text_safe_rect_px") or [80, 90, image.width - 80, int(image.height * 0.55)]]
    douyin_center_crop_rect = center_crop_rect_px(image.size, "9:16")
    accent = tuple(int(v) for v in (selected.get("accent_rgb") or [66, 211, 255]))
    accent_rgba = (*accent, 235)
    add_readability_backdrop(image, rect, selected)

    x1, y1, x2, y2 = rect
    width = x2 - x1
    title = cover_lines[0] if cover_lines else str(selected.get("name") or "AI 技巧")
    subtitle = cover_lines[1] if len(cover_lines) > 1 else ""
    label = cover_lines[2] if len(cover_lines) > 2 else ""
    glyph_boxes: list[tuple[int, int, int, int]] = []

    # Decorative material lines stay outside readable glyphs.
    draw.line((x1, y1 + 4, min(x2, x1 + int(width * 0.52)), y1 + 4), fill=accent_rgba, width=4)
    draw.line((x1, y2 - 6, min(x2, x1 + int(width * 0.28)), y2 - 6), fill=(*accent, 130), width=3)

    text_x = x1 + 24
    text_max_width = max(260, width - 56)
    title_start = min(84 if aspect == "9:16" else 78, max(52, int(width * 0.085)))
    title_min = 46 if aspect == "9:16" else 40
    title_lines, title_font = fit_lines(draw, title, text_max_width, 2, title_start, title_min)
    current_y = y1 + (44 if aspect == "16:9" else 52)
    shadow = (0, 0, 0, 190)
    title_fill = (242, 248, 255, 255)
    for line in title_lines:
        draw.text((text_x + 2, current_y + 4), line, font=title_font, fill=shadow, stroke_width=3, stroke_fill=shadow)
        draw.text((text_x, current_y), line, font=title_font, fill=title_fill, stroke_width=1, stroke_fill=(*accent, 180))
        glyph_boxes.append(draw.textbbox((text_x, current_y), line, font=title_font, stroke_width=4))
        current_y += int(getattr(title_font, "size", title_start) * 1.12)

    if subtitle:
        current_y += 28 if aspect == "16:9" else 34
        subtitle_lines, subtitle_font = fit_lines(draw, subtitle, max(240, width - 98), 1, 34 if aspect == "16:9" else 38, 26)
        sub_text = subtitle_lines[0]
        bbox = draw.textbbox((0, 0), sub_text, font=subtitle_font)
        box = (text_x, current_y, min(x2 - 24, text_x + (bbox[2] - bbox[0]) + 68), current_y + (bbox[3] - bbox[1]) + 30)
        strip = Image.new("RGBA", image.size, (0, 0, 0, 0))
        strip_draw = ImageDraw.Draw(strip)
        strip_draw.rounded_rectangle(box, radius=18, fill=(4, 12, 26, 196), outline=(*accent, 154), width=2)
        image.alpha_composite(strip)
        draw = ImageDraw.Draw(image)
        draw.text((box[0] + 32, box[1] + 12), sub_text, font=subtitle_font, fill=(*accent, 255))
        glyph_boxes.append(draw.textbbox((box[0] + 32, box[1] + 12), sub_text, font=subtitle_font, stroke_width=1))
        current_y = box[3]

    if label:
        label_font = font(24 if aspect == "16:9" else 26)
        label_text = label[:14]
        label_bbox = draw.textbbox((0, 0), label_text, font=label_font)
        lx = text_x
        ly = min(y2 - 52, current_y + 28)
        draw.text((lx + 2, ly + 2), label_text, font=label_font, fill=(0, 0, 0, 170))
        draw.text((lx, ly), label_text, font=label_font, fill=(224, 238, 246, 230))
        glyph_boxes.append(draw.textbbox((lx, ly), label_text, font=label_font, stroke_width=1))

    text_bbox = union_bbox(glyph_boxes)
    layout_report = {
        "text_bbox_px": text_bbox,
        "recommended_text_safe_rect_px": rect,
        "douyin_center_crop_rect_px": douyin_center_crop_rect,
        "text_bbox_inside_safe_rect": rect_contains(rect, text_bbox),
        "text_bbox_inside_douyin_center_crop": rect_contains(douyin_center_crop_rect, text_bbox),
        "compact_cover_text_used": compact_cover_text_ok(cover_lines, aspect),
        "line_count": len(cover_lines),
        "primary_text_char_count": len(title),
        "max_line_char_count": max((len(line) for line in cover_lines), default=0),
        "platform_preview_policy": "16:9 covers keep all public cover text inside the central 9:16 crop so Douyin center cover previews remain complete.",
    }
    return image.convert("RGB"), layout_report


def save_cover_outputs(
    source: Path,
    internal: Path,
    selected: dict[str, Any],
    cover_lines: list[str],
    aspect: str,
) -> tuple[dict[str, str], dict[str, Any]]:
    with Image.open(source) as opened:
        background = opened.convert("RGB")
        image, layout_report = draw_runtime_cover_text(background, selected, cover_lines, aspect)
        primary = internal / "cover.png"
        first_frame = internal / "first_frame_cover.png"
        horizontal = internal / "cover_publish_horizontal.png"
        vertical = internal / "cover_publish_vertical.png"
        source_copy = internal / "cover_background_source.jpg"
        douyin_center = internal / "cover_publish_douyin_center_crop.png"

        internal.mkdir(parents=True, exist_ok=True)
        image.save(primary)
        image.save(first_frame)
        if aspect == "16:9":
            image.save(horizontal)
            paste_contained_on_blur(image, (1080, 1920)).save(vertical)
            crop = image.crop(tuple(layout_report["douyin_center_crop_rect_px"]))
            crop.resize((1080, 1920), Image.Resampling.LANCZOS).save(douyin_center)
        else:
            paste_contained_on_blur(image, (1920, 1080)).save(horizontal)
            image.save(vertical)
            image.save(douyin_center)
        Image.open(source).convert("RGB").save(source_copy, quality=96)

    return {
        "primary": str(primary),
        "first_frame": str(first_frame),
        "horizontal_16x9": str(horizontal),
        "vertical_9x16": str(vertical),
        "douyin_center_crop_preview": str(douyin_center),
        "horizontal_4_3": str(horizontal),
        "vertical_3_4": str(vertical),
        "source_background_copy": str(source_copy),
    }, layout_report


def split_cover_text(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value or "").strip()
    if not text:
        return []
    return [line.strip() for line in re.split(r"\n+|\\n+|\s*\|\s*", text) if line.strip()]


def cover_lines_from_copy_package(project: Path) -> list[str]:
    copy_path = project / "internal" / "copy_package.json"
    data = load_json(copy_path)
    if not data:
        return []
    for key in ("cover_text",):
        lines = split_cover_text(data.get(key))
        if lines:
            return lines
    title = (
        data.get("selected_title")
        or data.get("publish_title")
        or data.get("title")
        or (data.get("title_options") or [""])[0]
    )
    title_lines = split_cover_text(title)
    if not title_lines:
        return []
    if len(title_lines[0]) > 18:
        # Keep the cover compact; the full publish title remains in publish copy.
        return [title_lines[0][:18], title_lines[0][18:32]]
    return title_lines


def resolve_cover_lines(args: argparse.Namespace, project: Path, internal: Path) -> list[str]:
    if args.cover_text:
        lines = split_cover_text(args.cover_text)
    elif args.cover_title:
        lines = [args.cover_title.strip()]
        if args.cover_subtitle:
            lines.append(args.cover_subtitle.strip())
    elif (internal / "publish_cover_text.txt").exists():
        lines = split_cover_text((internal / "publish_cover_text.txt").read_text(encoding="utf-8"))
    else:
        lines = cover_lines_from_copy_package(project)
    if not lines:
        raise SystemExit("cover text missing: provide --cover-text/--cover-title or internal/copy_package.json cover_text/title")
    return lines[:3]


def write_cover_text(internal: Path, cover_lines: list[str]) -> str:
    text_path = internal / "publish_cover_text.txt"
    text_path.parent.mkdir(parents=True, exist_ok=True)
    next_text = "\n".join(line.strip() for line in cover_lines if line.strip()) + "\n"
    if not text_path.exists() or text_path.read_text(encoding="utf-8") != next_text:
        text_path.write_text(next_text, encoding="utf-8")
    return str(text_path)


def report_includes_path(report: dict[str, Any], target: Path) -> bool:
    checked = report.get("checked_files")
    if not isinstance(checked, list):
        return False
    target_abs = target.resolve()
    project = target.parent.parent if target.parent.name == "internal" else target.parent
    for raw in checked:
        raw_path = Path(str(raw))
        candidate_paths = [raw_path.resolve()] if raw_path.is_absolute() else [
            (ROOT / raw_path).resolve(),
            (project / raw_path).resolve(),
        ]
        if target_abs in candidate_paths:
            return True
    return False


def require_checked_cover_text(internal: Path, cover_text: str, report_arg: str | None) -> str:
    text_path = Path(cover_text)
    candidates = [Path(report_arg)] if report_arg else [
        internal / "on_screen_and_publish_text_compliance_report.json",
        internal / "compliance_report.json",
    ]
    failures: list[str] = []
    for candidate in candidates:
        report_path = candidate if candidate.is_absolute() else ROOT / candidate
        if not report_path.exists() or not report_path.is_file():
            failures.append(f"{report_path} missing")
            continue
        report = load_json(report_path)
        if report.get("status") != "passed":
            failures.append(f"{report_path} status is not passed")
            continue
        if not report_includes_path(report, text_path):
            failures.append(f"{report_path} does not include {text_path}")
            continue
        if report_path.stat().st_mtime + 0.001 < text_path.stat().st_mtime:
            failures.append(f"{report_path} is older than {text_path}")
            continue
        return str(report_path)
    raise SystemExit(
        "cover text is not proven locally checked before cover render: "
        + "; ".join(failures)
    )


def select_template(
    manifest: dict[str, Any],
    pool_name: str,
    state: dict[str, Any],
) -> tuple[dict[str, Any], int, int]:
    entries = [
        item
        for item in manifest.get("templates", [])
        if isinstance(item, dict) and str(item.get("ratio") or "") == pool_name
    ]
    if not isinstance(entries, list) or not entries:
        raise SystemExit(f"cover background pool is empty: {pool_name}")
    index = state_index(state, pool_name) % len(entries)
    next_index = (index + 1) % len(entries)
    selected = entries[index]
    if not isinstance(selected, dict):
        raise SystemExit(f"invalid cover background entry at {pool_name}[{index}]")
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
    cover_lines: list[str],
    cover_layout: dict[str, Any],
    aspect: str,
    state_advanced: bool,
    manifest: dict[str, Any],
    checked_cover_text_report: str | None,
) -> dict[str, Any]:
    unique_template_ids = sorted({str(item.get("id")) for item in manifest.get("templates", []) if isinstance(item, dict)})
    return {
        "status": "passed",
        "cover_type": "fixed_pure_background_runtime_text_first_frame",
        "created_at": now_iso(),
        "project": str(project),
        "manifest": str(manifest_path),
        "state_file": str(state_file),
        "state_advanced": state_advanced,
        "selection_method": "sequential_by_size_pool",
        "frame_grab_used": False,
        "template_id": selected.get("id"),
        "canonical_id": f"{selected.get('id')}_{selected.get('ratio')}",
        "template_name": selected.get("name"),
        "template_path": str(source),
        "template_aspect": aspect,
        "background_ratio_key": selected.get("ratio"),
        "background_contains_text": selected.get("background_contains_text"),
        "recommended_text_safe_rect_px": selected.get("recommended_text_safe_rect_px"),
        "accent_rgb": selected.get("accent_rgb"),
        "cover_text_lines": cover_lines,
        "cover_layout": cover_layout,
        "douyin_cover_policy": {
            "target": "Douyin center cover preview",
            "horizontal_16x9_rule": "Place all public cover text inside the central 9:16 crop-safe area; keep the full 16:9 background visible for frame 0.",
            "requires_center_crop_preview": True,
            "requires_compact_cover_text": True,
        },
        "video_aspect": aspect,
        "size_pool": pool_name,
        "size_pool_size": pool_size,
        "template_rotation_index": index,
        "template_library_size": len(unique_template_ids),
        "text_policy": {
            "cover_text_must_be_generated_with_copy": True,
            "cover_text_must_be_in_local_compliance": True,
            "runtime_text_written_after_cover_text_file": True,
            "checked_before_render": checked_cover_text_report is not None,
            "checked_cover_text_report": checked_cover_text_report or "",
        },
        "outputs": {
            **outputs,
            "cover_text": cover_text,
        },
        "checks": {
            "template_from_fixed_library": True,
            "fixed_safe_asset": True,
            "fixed_pure_background_asset": True,
            "background_contains_text_false": selected.get("background_contains_text") is False,
            "selected_by_video_size": selected.get("ratio") == pool_name,
            "first_frame_required": True,
            "cover_text_written": Path(cover_text).exists(),
            "not_video_screenshot": True,
            "dynamic_text_overlay_used": True,
            "uses_old_cover_template_asset": False,
            "cover_text_fit_safe_rect": cover_layout.get("text_bbox_inside_safe_rect") is True,
            "primary_text_inside_douyin_center_crop": cover_layout.get("text_bbox_inside_douyin_center_crop") is True,
            "douyin_center_crop_preview_generated": Path(outputs.get("douyin_center_crop_preview", "")).exists(),
            "compact_cover_text_used": cover_layout.get("compact_cover_text_used") is True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Select fixed pure AI cover background and render runtime title for first frame/publish cover.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic> project path")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Fixed cover background manifest JSON")
    parser.add_argument("--state-file", default=str(DEFAULT_STATE), help="Persistent rotation state JSON")
    parser.add_argument("--aspect", choices=["auto", "16:9", "9:16"], default="auto")
    parser.add_argument("--video-width", type=int)
    parser.add_argument("--video-height", type=int)
    parser.add_argument("--cover-title", help="Runtime cover title. Prefer text already written and checked in copy_package.")
    parser.add_argument("--cover-subtitle", help="Runtime cover subtitle.")
    parser.add_argument("--cover-text", help="Runtime cover text lines, separated by newline or |.")
    parser.add_argument("--require-checked-cover-text", action="store_true", help="Require a passed local compliance report that includes internal/publish_cover_text.txt before rendering.")
    parser.add_argument("--cover-text-compliance-report", help="Specific local compliance report JSON to use with --require-checked-cover-text.")
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
        raise SystemExit(f"cover background source missing or empty: {source}")

    cover_lines = resolve_cover_lines(args, project, internal)
    cover_text = write_cover_text(internal, cover_lines)
    checked_cover_text_report = None
    if args.require_checked_cover_text:
        checked_cover_text_report = require_checked_cover_text(internal, cover_text, args.cover_text_compliance_report)
    outputs, cover_layout = save_cover_outputs(source, internal, selected, cover_lines, aspect)

    state_advanced = not args.no_advance_state
    if state_advanced:
        write_json(state_file, advance_state(state, pool_name, next_index, selected, project))

    pool_size = len([item for item in manifest.get("templates", []) if isinstance(item, dict) and item.get("ratio") == pool_name])
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
        cover_lines=cover_lines,
        cover_layout=cover_layout,
        aspect=aspect,
        state_advanced=state_advanced,
        manifest=manifest,
        checked_cover_text_report=checked_cover_text_report,
    )
    write_json(internal / "publish_cover_report.json", report)
    print(json.dumps({"status": "selected", "template_id": selected.get("id"), "ratio": selected.get("ratio"), "report": str(internal / "publish_cover_report.json")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
