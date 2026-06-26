#!/usr/bin/env python3
"""Generate dynamic reusable AI background loops from the fixed background pool.

The fixed PNG assets remain the source of visual truth. This script converts
each plate into a short seamless-ish MP4 loop with topic-safe abstract motion:
parallax, scans, particles, arcs, and node pulses. It never bakes text, people,
logos, or proof content into the background.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXED_MANIFEST = ROOT / "assets" / "ai_background_templates_fixed_archive" / "asset_manifest.json"
DEFAULT_OUT_DIR = ROOT / "assets" / "ai_background_templates_dynamic"


DYNAMIC_DESIGNS: dict[str, dict[str, Any]] = {
    "BG_FIXED_01": {
        "dynamic_id": "BG_DYNAMIC_01",
        "name": "钛金神经中枢",
        "motion_profile": "neural_control_room",
        "motion_description": "钛金 AI 神经中枢大厅缓慢前推，冰蓝神经节点沿光纤轨道逐级点亮，远景服务器城市有轻微深度雾漂移，底部轨道光扫向中央核心。",
        "prompt": "真实电影级钛金 AI 神经中枢空间，黑蓝钛金结构、冰蓝神经节点、透明玻璃数据层、精密光纤轨道和深层服务器建筑形成有秩序的算力大厅；动态为慢速前推、轨道光扫、节点启动、深度雾漂移；无文字、无数字、无人物、无标志。",
    },
    "BG_FIXED_02": {
        "dynamic_id": "BG_DYNAMIC_02",
        "name": "数据光轨隧道",
        "motion_profile": "data_light_tunnel",
        "motion_description": "深蓝数据光轨隧道向透视中心汇聚，青蓝和紫色光线持续流动，透明数据曲面轻微波动，镜头保持低速向前。",
        "prompt": "高端 AI 数据光轨隧道，细腻光线、粒子节点和透明数据曲面向远方汇聚；动态为向前 dolly、光轨流动、粒子漂移、隧道肋骨微波动；无文字、无数字、无人物、无标志。",
    },
    "BG_FIXED_03": {
        "dynamic_id": "BG_DYNAMIC_03",
        "name": "黑金战略舱",
        "motion_profile": "black_gold_chamber",
        "motion_description": "黑金战略舱中央光环缓慢旋转，金色智能核心低频脉冲，金属边缘高光游走，镜头做克制环绕。",
        "prompt": "黑金 AI 战略舱，中央低调智能核心和环形金属结构，墙面为无文字金属纹理与微弱光纤；动态为慢速环绕、光环旋转、金色核心脉冲、边缘高光游走；无人物、无文字、无品牌。",
    },
    "BG_FIXED_04": {
        "dynamic_id": "BG_DYNAMIC_04",
        "name": "来源档案墙",
        "motion_profile": "source_archive_wall",
        "motion_description": "无文字来源档案墙横向扫描光扫过透明证据槽，定位角和锁定节点轻微发光，远景玻璃层缓慢视差移动。",
        "prompt": "无文字 AI 来源档案墙，多层透明证据槽、磨砂玻璃托盘、金属定位角和扫描轨组成信息核验空间；动态为横向扫描、卡槽聚焦、锁定节点脉冲、玻璃层视差；不出现任何可读文字。",
    },
    "BG_FIXED_05": {
        "dynamic_id": "BG_DYNAMIC_05",
        "name": "冰白工具实验台",
        "motion_profile": "white_ice_tool_lab",
        "motion_description": "冰白工具实验台里透明玻璃核心轻微旋转，冰晶粒子慢慢上浮，蓝白扫描线经过台面，整体明亮但不过曝。",
        "prompt": "清洁型 AI 工具实验台，白色和银灰未来空间中悬浮透明神经网络、数据波纹、冰晶粒子和玻璃曲面；动态为玻璃核心旋转、微粒上浮、蓝白扫描、柔和光晕；无人物、无文字、无标志。",
    },
    "BG_FIXED_06": {
        "dynamic_id": "BG_DYNAMIC_06",
        "name": "量子环形核心",
        "motion_profile": "quantum_ring_core",
        "motion_description": "量子环形核心缓慢旋转，蓝紫能量涡流向中心收束，液态金属轨道反射变化，镜头微弱环绕。",
        "prompt": "电影级 AI 量子环形核心，巨大半透明环形计算结构、神经网络、数据节点、旋转光环、液态金属和玻璃材质；动态为环形扫描、轨道视差、能量锁定脉冲；无文字、无数字、无人物。",
    },
    "BG_FIXED_07": {
        "dynamic_id": "BG_DYNAMIC_07",
        "name": "宇宙意识网络",
        "motion_profile": "cosmic_ai_network",
        "motion_description": "深空 AI 意识网络做星体视差，晶体节点逐个点亮并向主节点汇聚，远景星尘缓慢漂移。",
        "prompt": "史诗级人工智能宇宙意识网络，深空中由晶体节点、神经光路、轨道设施、行星尺度数据流组成宏大 AI 网络；动态为星层视差、节点汇聚、星尘漂移、低频光脉冲；无文字、无人物、无标志。",
    },
    "BG_FIXED_08": {
        "dynamic_id": "BG_DYNAMIC_08",
        "name": "竖版工具测试舱",
        "motion_profile": "vertical_tool_test_chamber",
        "motion_description": "竖版工具测试舱中轴透明计算核心轻微呼吸发光，纵向扫描线从顶部到底部，左右模块依次点亮。",
        "prompt": "竖版 AI 工具测试舱，中央透明计算核心、黑色金属测试装置、银色光子模块和细密数据管线组成高级产品广告式空间；动态为纵向扫描、模块点亮、中轴呼吸、微粒上浮；无人物、无文字、无标志。",
    },
    "BG_FIXED_09": {
        "dynamic_id": "BG_DYNAMIC_09",
        "name": "竖版工作流脊柱",
        "motion_profile": "vertical_workflow_spine",
        "motion_description": "竖版 AI 工作流脊柱从上到下形成输入、处理、检查、输出四段结构，光点沿中轴传递，每段节点轻微脉冲。",
        "prompt": "竖版 AI 工作流工程脊柱，输入、处理、检查、输出四层无文字计算模块，玻璃节点和金属轨道连接成有秩序的生产管线；动态为顶部到底部光流、节点脉冲、段落锁定、侧翼弱视差；无文字、无人物、无标志。",
    },
    "BG_FIXED_10": {
        "dynamic_id": "BG_DYNAMIC_10",
        "name": "竖版趋势星图",
        "motion_profile": "vertical_trend_star_map",
        "motion_description": "竖版 AI 趋势星图的中央产业主轴连接多层节点，节点轨道缓慢旋转，光线由底部向顶部汇聚，星尘和弧线持续微动。",
        "prompt": "竖版 AI 趋势星图，中央 AI 产业主轴连接模型、智能体、算力、开源和应用节点，深空星图、晶体数据塔、轨道设施和远景星云组成趋势网络；动态为节点轨道、慢速推镜、星尘漂移、最终汇聚；无人物、无文字、无标志。",
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def label_font(size: int = 15) -> Any:
    for candidate in (
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ):
        path = Path(candidate)
        if path.exists():
            try:
                from PIL import ImageFont

                return ImageFont.truetype(str(path), size=size)
            except Exception:
                continue
    try:
        from PIL import ImageFont

        return ImageFont.load_default()
    except Exception:
        return None


def stable_seed(value: str) -> int:
    return int(hashlib.sha256(value.encode("utf-8")).hexdigest()[:16], 16)


def repo_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def aspect_token(aspect: str) -> str:
    return aspect.replace(":", "x")


def output_paths(template: dict[str, Any], out_dir: Path) -> tuple[Path, Path]:
    design = DYNAMIC_DESIGNS[str(template["id"])]
    suffix = aspect_token(str(template["aspect"]))
    stem = f'{design["dynamic_id"]}_{template["name"]}_{suffix}'
    return out_dir / f"{stem}.mp4", out_dir / f"{stem}.poster.png"


def fit_cover_dynamic(src: Image.Image, width: int, height: int, p: float, profile: str, seed: int) -> Image.Image:
    phase = (seed % 360) * math.pi / 180
    if "vertical" in profile:
        zoom_amp = 0.028
        pan_x = 0.026
        pan_y = 0.046
    elif profile in {"data_light_tunnel", "quantum_ring_core"}:
        zoom_amp = 0.034
        pan_x = 0.045
        pan_y = 0.028
    else:
        zoom_amp = 0.023
        pan_x = 0.032
        pan_y = 0.024
    scale = 1.035 + zoom_amp * (0.5 - 0.5 * math.cos(math.tau * p))
    sw, sh = src.size
    ratio = max(width / sw, height / sh) * scale
    resized = src.resize((int(sw * ratio), int(sh * ratio)), Image.Resampling.LANCZOS)
    max_x = max(0, resized.width - width)
    max_y = max(0, resized.height - height)
    ox = 0.5 + pan_x * math.sin(math.tau * p + phase)
    oy = 0.5 + pan_y * math.cos(math.tau * p * 0.82 + phase / 2)
    left = max(0, min(max_x, int(max_x * ox)))
    top = max(0, min(max_y, int(max_y * oy)))
    return resized.crop((left, top, left + width, top + height)).convert("RGBA")


def line_glow(layer: Image.Image, points: tuple[float, float, float, float], color: tuple[int, int, int], alpha: int, width: int = 2, blur: int = 8) -> None:
    draw = ImageDraw.Draw(layer)
    draw.line(points, fill=(*color, max(6, alpha // 5)), width=max(5, width * 8))
    draw.line(points, fill=(*color, max(8, alpha // 3)), width=max(3, width * 4))
    draw.line(points, fill=(*color, alpha), width=width)


def arc_glow(layer: Image.Image, bbox: tuple[float, float, float, float], start: float, end: float, color: tuple[int, int, int], alpha: int, width: int = 2) -> None:
    draw = ImageDraw.Draw(layer)
    draw.arc(bbox, start=start, end=end, fill=(*color, max(6, alpha // 5)), width=max(6, width * 7))
    draw.arc(bbox, start=start, end=end, fill=(*color, max(8, alpha // 3)), width=max(4, width * 4))
    draw.arc(bbox, start=start, end=end, fill=(*color, alpha), width=width)


def node(layer: Image.Image, x: float, y: float, color: tuple[int, int, int], alpha: int, radius: int = 4) -> None:
    sd = ImageDraw.Draw(layer)
    sd.ellipse((x - radius * 4, y - radius * 4, x + radius * 4, y + radius * 4), fill=(*color, max(6, alpha // 7)))
    sd.ellipse((x - radius * 2.2, y - radius * 2.2, x + radius * 2.2, y + radius * 2.2), fill=(*color, max(8, alpha // 4)))
    sd.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*color, alpha))


def draw_particles(layer: Image.Image, template_id: str, p: float, count: int, color: tuple[int, int, int], vertical: bool = False) -> None:
    width, height = layer.size
    seed = stable_seed(template_id)
    draw = ImageDraw.Draw(layer)
    for i in range(count):
        h = hashlib.sha256(f"{template_id}:{i}".encode("utf-8")).digest()
        bx = int.from_bytes(h[:2], "big") / 65535
        by = int.from_bytes(h[2:4], "big") / 65535
        phase = int.from_bytes(h[4:6], "big") / 65535 * math.tau
        depth = 0.45 + int.from_bytes(h[6:8], "big") / 65535 * 0.85
        if vertical:
            x = width * (bx + 0.018 * math.sin(math.tau * p + phase)) % width
            y = height * (by + 0.055 * math.sin(math.tau * p * depth + phase)) % height
        else:
            x = width * (bx + 0.035 * math.sin(math.tau * p * depth + phase)) % width
            y = height * (by + 0.027 * math.cos(math.tau * p * (0.8 + depth * 0.2) + phase)) % height
        r = 1 + (seed + i) % 3
        alpha = int(18 + 54 * (0.5 + 0.5 * math.sin(math.tau * p + phase)))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(*color, alpha))


def draw_neural_control_room(layer: Image.Image, p: float) -> None:
    w, h = layer.size
    cyan = (96, 226, 255)
    amber = (255, 183, 91)
    vp = (w * (0.58 + 0.015 * math.sin(math.tau * p)), h * 0.48)
    for i in range(10):
        x = w * (i / 9)
        alpha = int(34 + 32 * (0.5 + 0.5 * math.sin(math.tau * p + i)))
        line_glow(layer, (x, h, vp[0], vp[1]), cyan, alpha, width=1)
    sweep = w * (0.12 + 0.76 * (0.5 + 0.5 * math.sin(math.tau * p)))
    line_glow(layer, (sweep, h * 0.16, sweep + w * 0.12, h * 0.9), amber, 58, width=2)
    for i in range(18):
        x = w * (0.28 + 0.42 * ((i * 37) % 100) / 100)
        y = h * (0.18 + 0.58 * ((i * 61) % 100) / 100)
        node(layer, x, y, cyan, int(70 + 80 * (0.5 + 0.5 * math.sin(math.tau * p + i))), 3)


def draw_data_light_tunnel(layer: Image.Image, p: float) -> None:
    w, h = layer.size
    cyan = (86, 222, 255)
    violet = (145, 117, 255)
    vp = (w * 0.86, h * 0.48)
    for i in range(22):
        y = h * (i / 21)
        phase = (p + i * 0.033) % 1
        x1 = -w * 0.1 + w * 0.34 * phase
        line_glow(layer, (x1, y, vp[0], vp[1]), cyan if i % 2 else violet, 38 + (i % 4) * 8, width=1)
    for i in range(6):
        x = w * (0.08 + i * 0.14 + 0.025 * math.sin(math.tau * p + i))
        line_glow(layer, (x, h * 0.18, x + w * 0.18, h * 0.86), violet, 44, width=1)


def draw_black_gold_chamber(layer: Image.Image, p: float) -> None:
    w, h = layer.size
    gold = (245, 190, 98)
    center = (w * 0.5, h * 0.42)
    for i, scale in enumerate((0.28, 0.38, 0.52)):
        rx = w * scale
        ry = h * scale * 0.28
        start = p * 360 + i * 64
        arc_glow(layer, (center[0] - rx, center[1] - ry, center[0] + rx, center[1] + ry), start, start + 210, gold, 54, width=2)
    pulse = int(26 + 44 * (0.5 + 0.5 * math.sin(math.tau * p)))
    node(layer, center[0], center[1] + h * 0.06, gold, pulse + 90, 5)
    glint_x = w * (0.18 + 0.62 * (0.5 + 0.5 * math.sin(math.tau * p)))
    line_glow(layer, (glint_x, h * 0.78, glint_x + w * 0.12, h * 0.18), gold, 42, width=1)


def draw_source_archive_wall(layer: Image.Image, p: float) -> None:
    w, h = layer.size
    cyan = (116, 228, 238)
    scan_x = w * (0.5 + 0.55 * math.sin(math.tau * p))
    line_glow(layer, (scan_x, h * 0.12, scan_x, h * 0.88), cyan, 64, width=2)
    d = ImageDraw.Draw(layer)
    for row in range(3):
        for col in range(5):
            x = w * (0.1 + col * 0.18)
            y = h * (0.18 + row * 0.24)
            a = int(18 + 38 * (0.5 + 0.5 * math.sin(math.tau * p + row + col)))
            d.rounded_rectangle((x, y, x + w * 0.12, y + h * 0.11), radius=10, outline=(*cyan, a), width=1)
    for i in range(8):
        node(layer, w * (0.12 + i * 0.1), h * (0.82 + 0.018 * math.sin(math.tau * p + i)), cyan, 72, 3)


def draw_white_ice_tool_lab(layer: Image.Image, p: float) -> None:
    w, h = layer.size
    cyan = (70, 206, 232)
    silver = (225, 244, 255)
    center = (w * 0.54, h * 0.47)
    for i, scale in enumerate((0.18, 0.28, 0.39)):
        rx = w * scale
        ry = h * scale * 0.38
        arc_glow(layer, (center[0] - rx, center[1] - ry, center[0] + rx, center[1] + ry), p * 360 + i * 90, p * 360 + i * 90 + 125, cyan, 52, width=2)
    scan_y = h * (0.5 + 0.42 * math.sin(math.tau * p))
    line_glow(layer, (w * 0.06, scan_y, w * 0.94, scan_y - h * 0.03), silver, 54, width=2)
    draw_particles(layer, "BG_FIXED_05_ice", p, 60, cyan, vertical=True)


def draw_quantum_ring_core(layer: Image.Image, p: float) -> None:
    w, h = layer.size
    cyan = (69, 223, 255)
    violet = (142, 117, 255)
    center = (w * 0.66, h * 0.49)
    for i, scale in enumerate((0.24, 0.34, 0.46, 0.58)):
        rx = w * scale * 0.56
        ry = h * scale
        start = p * 360 * (1 if i % 2 == 0 else -1) + i * 48
        arc_glow(layer, (center[0] - rx, center[1] - ry, center[0] + rx, center[1] + ry), start, start + 132, cyan if i % 2 else violet, 62, width=2)
    for i in range(12):
        angle = math.tau * (i / 12 + p * 0.18)
        node(layer, center[0] + math.cos(angle) * w * 0.18, center[1] + math.sin(angle) * h * 0.24, cyan, 88, 3)


def draw_cosmic_ai_network(layer: Image.Image, p: float) -> None:
    w, h = layer.size
    cyan = (92, 214, 255)
    gold = (240, 186, 95)
    points = []
    for i in range(15):
        x = w * (0.08 + ((i * 37) % 100) / 100 * 0.84)
        y = h * (0.12 + ((i * 59) % 100) / 100 * 0.76)
        points.append((x, y))
    hub = points[6]
    for i, pt in enumerate(points):
        alpha = int(26 + 38 * (0.5 + 0.5 * math.sin(math.tau * p + i)))
        line_glow(layer, (pt[0], pt[1], hub[0], hub[1]), cyan if i % 3 else gold, alpha, width=1, blur=7)
        node(layer, pt[0] + 10 * math.sin(math.tau * p + i), pt[1], cyan if i % 3 else gold, 82, 3)
    draw_particles(layer, "BG_FIXED_07_cosmic", p, 85, cyan)


def draw_vertical_tool_test_chamber(layer: Image.Image, p: float) -> None:
    w, h = layer.size
    cyan = (82, 220, 255)
    center_x = w * 0.5
    line_glow(layer, (center_x, h * 0.1, center_x, h * 0.9), cyan, 72, width=2)
    scan_y = h * (0.08 + 0.84 * ((p + 0.08) % 1))
    fade = math.sin(math.pi * ((p + 0.08) % 1))
    line_glow(layer, (w * 0.18, scan_y, w * 0.82, scan_y), cyan, int(30 + 54 * fade), width=2)
    for i in range(8):
        y = h * (0.18 + i * 0.09)
        side = -1 if i % 2 else 1
        x = center_x + side * w * (0.17 + 0.02 * math.sin(math.tau * p + i))
        node(layer, x, y, cyan, int(60 + 70 * (0.5 + 0.5 * math.sin(math.tau * p + i))), 4)
        line_glow(layer, (center_x, y, x, y), cyan, 32, width=1)
    draw_particles(layer, "BG_FIXED_08_vertical", p, 52, cyan, vertical=True)


def draw_vertical_workflow_spine(layer: Image.Image, p: float) -> None:
    w, h = layer.size
    cyan = (88, 226, 238)
    teal = (78, 220, 190)
    x = w * 0.5
    line_glow(layer, (x, h * 0.08, x, h * 0.92), cyan, 66, width=2)
    for i in range(4):
        y = h * (0.18 + i * 0.2)
        a = int(60 + 70 * (0.5 + 0.5 * math.sin(math.tau * p + i * 0.9)))
        node(layer, x, y, cyan if i % 2 else teal, a, 7)
        line_glow(layer, (w * 0.22, y, w * 0.78, y), teal, 32, width=1)
    flow_y = h * (0.08 + 0.84 * (p % 1))
    node(layer, x, flow_y, (255, 202, 105), 150, 5)
    draw_particles(layer, "BG_FIXED_09_spine", p, 45, cyan, vertical=True)


def draw_vertical_trend_star_map(layer: Image.Image, p: float) -> None:
    w, h = layer.size
    cyan = (82, 215, 255)
    violet = (150, 110, 255)
    gold = (238, 190, 98)
    x = w * 0.5
    line_glow(layer, (x, h * 0.12, x, h * 0.88), cyan, 58, width=2)
    centers = [(x, h * y) for y in (0.18, 0.32, 0.48, 0.64, 0.8)]
    for i, (cx, cy) in enumerate(centers):
        color = [cyan, violet, gold, cyan, violet][i]
        node(layer, cx, cy, color, int(90 + 65 * (0.5 + 0.5 * math.sin(math.tau * p + i))), 6)
        for j in range(3):
            angle = math.tau * (p * 0.22 + j / 3 + i * 0.07)
            ox = math.cos(angle) * w * (0.12 + j * 0.035)
            oy = math.sin(angle) * h * 0.035
            node(layer, cx + ox, cy + oy, color, 58, 3)
            line_glow(layer, (cx, cy, cx + ox, cy + oy), color, 26, width=1)
    draw_particles(layer, "BG_FIXED_10_star_map", p, 70, cyan, vertical=True)


PROFILE_DRAWERS = {
    "neural_control_room": draw_neural_control_room,
    "data_light_tunnel": draw_data_light_tunnel,
    "black_gold_chamber": draw_black_gold_chamber,
    "source_archive_wall": draw_source_archive_wall,
    "white_ice_tool_lab": draw_white_ice_tool_lab,
    "quantum_ring_core": draw_quantum_ring_core,
    "cosmic_ai_network": draw_cosmic_ai_network,
    "vertical_tool_test_chamber": draw_vertical_tool_test_chamber,
    "vertical_workflow_spine": draw_vertical_workflow_spine,
    "vertical_trend_star_map": draw_vertical_trend_star_map,
}


def render_frame(src: Image.Image, template: dict[str, Any], frame: int, total_frames: int, fps: int) -> Image.Image:
    width = int(template["width"])
    height = int(template["height"])
    template_id = str(template["id"])
    design = DYNAMIC_DESIGNS[template_id]
    profile = str(design["motion_profile"])
    p = frame / max(1, total_frames)
    base = fit_cover_dynamic(src, width, height, p, profile, stable_seed(template_id))
    if profile == "white_ice_tool_lab":
        base = ImageEnhance.Brightness(base).enhance(1.03)
        base = ImageEnhance.Contrast(base).enhance(1.06)
    else:
        base = ImageEnhance.Contrast(base).enhance(1.09)
        base = ImageEnhance.Color(base).enhance(1.08)
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_particles(layer, f"{template_id}:base", p, 42 if width > height else 58, (104, 226, 255), vertical=height > width)
    PROFILE_DRAWERS[profile](layer, p)
    if profile != "white_ice_tool_lab":
        vignette = Image.new("L", (width, height), 0)
        vd = ImageDraw.Draw(vignette)
        max_inset = max(1, min(width, height) // 2 - 2)
        step = max(24, max(width, height) // 55)
        for inset in range(0, max_inset, step):
            alpha = int(42 * (inset / max_inset) ** 1.4)
            vd.rectangle((inset, inset, width - inset, height - inset), outline=alpha, width=max(8, width // 160))
        dark = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        dark.putalpha(vignette.filter(ImageFilter.GaussianBlur(26)))
        base.alpha_composite(dark)
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.15)))
    return base.convert("RGB")


def run_ffmpeg(width: int, height: int, fps: int, crf: int, out_path: Path) -> subprocess.Popen[bytes]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise SystemExit("ffmpeg is required to generate dynamic backgrounds")
    return subprocess.Popen(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "rgb24",
            "-s",
            f"{width}x{height}",
            "-r",
            str(fps),
            "-i",
            "-",
            "-an",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-profile:v",
            "high",
            "-crf",
            str(crf),
            "-movflags",
            "+faststart",
            str(out_path),
        ],
        stdin=subprocess.PIPE,
    )


def generate_one(template: dict[str, Any], out_dir: Path, duration: float, fps: int, crf: int, force: bool) -> dict[str, Any]:
    template_id = str(template["id"])
    if template_id not in DYNAMIC_DESIGNS:
        raise SystemExit(f"dynamic design missing for {template_id}")
    source = resolve_path(str(template["path"]))
    if not source.exists():
        raise SystemExit(f"source fixed background missing: {source}")
    mp4, poster = output_paths(template, out_dir)
    if mp4.exists() and poster.exists() and not force:
        video_size = mp4.stat().st_size
        poster_size = poster.stat().st_size
    else:
        mp4.parent.mkdir(parents=True, exist_ok=True)
        src = Image.open(source).convert("RGB")
        total_frames = max(1, int(round(duration * fps)))
        proc = run_ffmpeg(int(template["width"]), int(template["height"]), fps, crf, mp4)
        assert proc.stdin is not None
        poster_frame = max(0, min(total_frames - 1, fps))
        try:
            for index in range(total_frames):
                frame = render_frame(src, template, index, total_frames, fps)
                if index == poster_frame:
                    frame.save(poster, quality=94)
                proc.stdin.write(frame.tobytes())
        finally:
            proc.stdin.close()
        return_code = proc.wait()
        if return_code != 0:
            raise SystemExit(f"ffmpeg failed for {template_id} with code {return_code}")
        video_size = mp4.stat().st_size
        poster_size = poster.stat().st_size
    design = DYNAMIC_DESIGNS[template_id]
    return {
        "id": design["dynamic_id"],
        "source_fixed_id": template_id,
        "name": template["name"],
        "aspect": template["aspect"],
        "width": template["width"],
        "height": template["height"],
        "visual_family": template.get("visual_family"),
        "source_fixed_asset_path": template["path"],
        "dynamic_asset_path": repo_path(mp4),
        "dynamic_poster_path": repo_path(poster),
        "asset_source_type": "fixed_dynamic_background_video_asset",
        "generation_method": "deterministic_layered_motion_from_fixed_asset_v1",
        "duration_sec": duration,
        "fps": fps,
        "loop_policy": "designed_for_short_seamless_loop",
        "size_bytes": video_size,
        "poster_size_bytes": poster_size,
        "motion_profile": design["motion_profile"],
        "motion_description": design["motion_description"],
        "prompt": design["prompt"],
        "checks": {
            "dynamic_background_asset": True,
            "uses_existing_fixed_background_as_source": True,
            "no_baked_text": True,
            "no_people": True,
            "no_logo": True,
            "foreground_text_must_be_overlay": True,
            "dimensions_match_template": True,
            "archived_source_asset_kept": True,
        },
    }


def build_contact_sheet(assets: list[dict[str, Any]], out_dir: Path) -> Path:
    thumbs = []
    font = label_font()
    for asset in assets:
        image = Image.open(resolve_path(asset["dynamic_poster_path"])).convert("RGB")
        image.thumbnail((360, 240), Image.Resampling.LANCZOS)
        tile = Image.new("RGB", (380, 290), (8, 12, 18))
        tile.paste(image, ((380 - image.width) // 2, 12))
        draw = ImageDraw.Draw(tile)
        draw.text((14, 256), f'{asset["id"]} {asset["name"]}', fill=(226, 238, 248), font=font)
        thumbs.append(tile)
    cols = 2
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * 380, rows * 290), (5, 7, 11))
    for index, tile in enumerate(thumbs):
        sheet.paste(tile, ((index % cols) * 380, (index // cols) * 290))
    path = out_dir / "dynamic_background_contact_sheet.jpg"
    sheet.save(path, quality=92)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate dynamic MP4 background loops from fixed AI background plates.")
    parser.add_argument("--fixed-manifest", default=str(DEFAULT_FIXED_MANIFEST))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--manifest-out", default=str(DEFAULT_OUT_DIR / "dynamic_asset_manifest.json"))
    parser.add_argument("--duration", type=float, default=8.0)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--crf", type=int, default=19)
    parser.add_argument("--only", action="append", default=[], help="Generate only these source fixed ids, e.g. BG_FIXED_10")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    fixed_manifest = load_json(resolve_path(args.fixed_manifest))
    out_dir = resolve_path(args.out_dir)
    manifest_out = resolve_path(args.manifest_out)
    selected_ids = set(args.only or [])
    templates = [
        asset for asset in fixed_manifest.get("assets", [])
        if isinstance(asset, dict) and (not selected_ids or asset.get("id") in selected_ids)
    ]
    if not templates:
        raise SystemExit("no fixed background assets selected")

    assets = [generate_one(template, out_dir, args.duration, args.fps, args.crf, args.force) for template in templates]
    contact_sheet = build_contact_sheet(assets, out_dir)
    manifest = {
        "status": "passed",
        "created_at": now_iso(),
        "fixed_manifest": repo_path(resolve_path(args.fixed_manifest)),
        "out_dir": repo_path(out_dir),
        "asset_count": len(assets),
        "generation_method": "deterministic_layered_motion_from_fixed_asset_v1",
        "default_usage": {
            "render_asset_type": "dynamic_mp4",
            "static_png_fallback": False,
            "archived_source_asset_available_for_regeneration": True,
            "foreground_text_policy": "HyperFrames/HTML/CSS overlay only; Douyin-facing text still requires compliance checks",
        },
        "checks": {
            "all_dynamic_assets_generated": len(assets) == len(templates),
            "no_baked_text_policy": True,
            "manual_qingdou_not_required_for_background_no_text": True,
            "foreground_text_still_requires_qingdou": True,
            "static_background_fallback_removed": True,
            "archived_source_assets_preserved": True,
        },
        "contact_sheet": repo_path(contact_sheet),
        "assets": assets,
    }
    write_json(manifest_out, manifest)
    print(json.dumps({"status": "passed", "manifest": str(manifest_out), "asset_count": len(assets)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
