#!/usr/bin/env python3
"""Analyze a Douyin reference input without copying protected expression."""

from __future__ import annotations

import argparse
import json
import re
import shutil
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


def run_probe(path: Path) -> dict[str, Any]:
    try:
        result = subprocess.run(
            [
                shutil.which("ffprobe") or "ffprobe",
                "-v",
                "error",
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                str(path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
    except Exception:
        return {
            "duration_seconds": 0.0,
            "width": 0,
            "height": 0,
            "fps": 0.0,
            "aspect_ratio": "unknown",
        }
    video_stream = next((item for item in data.get("streams", []) if item.get("codec_type") == "video"), {})
    duration = float(data.get("format", {}).get("duration") or video_stream.get("duration") or 0)
    width = int(video_stream.get("width") or 0)
    height = int(video_stream.get("height") or 0)
    fps_text = str(video_stream.get("avg_frame_rate") or video_stream.get("r_frame_rate") or "0/1")
    numerator, _, denominator = fps_text.partition("/")
    fps = float(numerator or 0) / float(denominator or 1)
    return {
        "duration_seconds": round(duration, 3),
        "width": width,
        "height": height,
        "fps": round(fps, 3),
        "aspect_ratio": f"{width}:{height}" if width and height else "unknown",
    }


def write_shot_table(out_dir: Path, duration: float) -> Path:
    shot_table = out_dir / "reference_shot_table.md"
    end = duration if duration else 45
    rows = [
        "| Time | Shot Type | Visual | Text Density | Motion | Why It Works | Learn | Do Not Copy |",
        "|---|---|---|---|---|---|---|---|",
        "| 0-3s | cold open | 待按抽帧人工确认 | 1 句痛点或结果 | 快速进入主题 | 第一屏给理由 | 学开场强度 | 不复制原句和画面 |",
        f"| 3-{min(8, int(end))}s | proof | 待按 contact sheet 标注 | 短标签 | 卡片或 UI 切换 | 建立可信度 | 学证明顺序 | 不复用原素材 |",
        f"| {min(8, int(end))}-{int(end)}s | teaching | 待按镜头拆解 | 方法说明 | 节奏变化 | 完成信息交付 | 学信息层级 | 不复制完整结构 |",
    ]
    shot_table.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return shot_table


def write_style_profile(out_dir: Path, meta: dict[str, Any], assets: dict[str, str]) -> Path:
    profile = {
        "duration_seconds": meta.get("duration_seconds", 0),
        "resolution": {"width": meta.get("width", 0), "height": meta.get("height", 0)},
        "fps": meta.get("fps", 0),
        "aspect_ratio": meta.get("aspect_ratio", "unknown"),
        "observed_from": {
            "contact_sheet": assets.get("reference_contact_sheet"),
            "frames_dir": assets.get("reference_frames_dir"),
        },
        "style_notes": {
            "pace": "derive from shot table after frame review",
            "text_density": "derive from contact sheet",
            "motion_language": "derive from frame changes",
            "proof_style": "derive from real evidence moments",
        },
        "reuse_policy": "learn rhythm and structure only; do not copy frames, subtitles, voice, music, wording, or full sequence",
    }
    path = out_dir / "reference_style_profile.json"
    path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_pacing_curve(out_dir: Path, duration: float) -> Path:
    total = duration if duration else 45.0
    segments = [
        {
            "start": 0,
            "end": min(3.0, total),
            "expected_function": "cold_open",
            "target_energy": "high",
            "learn": "enter conflict or proof immediately",
        },
        {
            "start": min(3.0, total),
            "end": min(8.0, total),
            "expected_function": "proof_or_setup",
            "target_energy": "high-medium",
            "learn": "show why the viewer should trust the method",
        },
        {
            "start": min(8.0, total),
            "end": total,
            "expected_function": "teaching_body",
            "target_energy": "varied",
            "learn": "alternate explanation, proof, and reusable takeaway",
        },
    ]
    path = out_dir / "reference_pacing_curve.json"
    path.write_text(json.dumps({"duration_seconds": total, "segments": segments}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_visual_patterns(out_dir: Path, assets: dict[str, str]) -> Path:
    patterns = {
        "observed_from": {
            "contact_sheet": assets.get("reference_contact_sheet", ""),
            "shot_table": assets.get("reference_shot_table", ""),
        },
        "patterns_to_learn": [
            "cold open gives the viewer a reason to stop",
            "proof frames appear before abstract explanation",
            "text labels stay short and tied to the voiceover",
            "visual focus changes before the scene becomes static",
        ],
        "patterns_to_avoid": [
            "copying original frames or subtitles",
            "using one static image for a full teaching section",
            "stacking dense text over important UI",
            "matching the reference sequence too closely",
        ],
    }
    path = out_dir / "reference_visual_patterns.json"
    path.write_text(json.dumps(patterns, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_fingerprint(out_dir: Path, meta: dict[str, Any], assets: dict[str, str], risk: str) -> Path:
    fingerprint = {
        "duration_bucket": "short" if meta.get("duration_seconds", 0) <= 30 else "medium",
        "resolution": {"width": meta.get("width", 0), "height": meta.get("height", 0)},
        "fps": meta.get("fps", 0),
        "reference_artifacts": assets,
        "similarity_risk": risk,
        "reuse_boundary": "reuse pacing ideas and information hierarchy only; regenerate topic, visuals, script, audio, and proof assets",
    }
    path = out_dir / "reference_fingerprint.json"
    path.write_text(json.dumps(fingerprint, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def extract_reference_assets(input_path: Path, out_dir: Path) -> dict[str, str]:
    assets: dict[str, str] = {}
    if not shutil.which("ffmpeg"):
        assets["warning"] = "ffmpeg not found; frame extraction skipped"
        return assets
    frames_dir = out_dir / "reference_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            shutil.which("ffmpeg") or "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(input_path),
            "-vf",
            "fps=1,scale=360:-1",
            "-q:v",
            "2",
            str(frames_dir / "frame_%04d.jpg"),
        ],
        check=True,
    )
    if list(frames_dir.glob("frame_*.jpg")):
        contact_sheet = out_dir / "reference_contact_sheet.jpg"
        subprocess.run(
            [
                shutil.which("ffmpeg") or "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-pattern_type",
                "glob",
                "-i",
                str(frames_dir / "frame_*.jpg"),
                "-vf",
                "tile=4x4",
                "-frames:v",
                "1",
                str(contact_sheet),
            ],
            check=True,
        )
        assets["reference_frames_dir"] = str(frames_dir)
        assets["reference_contact_sheet"] = str(contact_sheet)
    return assets


def similarity_risk(text: str) -> str:
    high_patterns = ["一模一样", "照抄", "原字幕", "原文案", "原声音", "不要改"]
    medium_patterns = ["90%", "百分之90", "高度相似", "尽量一样"]
    if any(pattern in text for pattern in high_patterns):
        return "high"
    if any(pattern in text for pattern in medium_patterns):
        return "medium"
    return "low"


def build_analysis(raw_input: str, out_path: Path) -> dict[str, Any]:
    reference_type = classify_reference(raw_input)
    out_dir = out_path.parent
    video_meta = run_probe(Path(raw_input).expanduser()) if reference_type == "local_video" else {
        "duration_seconds": 0.0,
        "width": 0,
        "height": 0,
        "fps": 0.0,
        "aspect_ratio": "unknown",
    }
    duration = float(video_meta["duration_seconds"])
    risk = similarity_risk(raw_input)
    topic = "AI 圈知识短视频参考" if reference_type != "share_text" else raw_input[:80]
    extracted_assets: dict[str, str] = {}
    if reference_type == "local_video":
        extracted_assets = extract_reference_assets(Path(raw_input).expanduser(), out_dir)
        shot_table = write_shot_table(out_dir, duration)
        extracted_assets["reference_shot_table"] = str(shot_table)
        style_profile = write_style_profile(out_dir, video_meta, extracted_assets)
        extracted_assets["reference_style_profile"] = str(style_profile)
        pacing_curve = write_pacing_curve(out_dir, duration)
        extracted_assets["reference_pacing_curve"] = str(pacing_curve)
        visual_patterns = write_visual_patterns(out_dir, extracted_assets)
        extracted_assets["reference_visual_patterns"] = str(visual_patterns)
        fingerprint = write_fingerprint(out_dir, video_meta, extracted_assets, risk)
        extracted_assets["reference_fingerprint"] = str(fingerprint)
    return {
        "reference_type": reference_type,
        "duration_seconds": duration,
        "resolution": {
            "width": video_meta["width"],
            "height": video_meta["height"],
        },
        "fps": video_meta["fps"],
        "aspect_ratio": video_meta["aspect_ratio"],
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
        "extracted_assets": extracted_assets,
        "style_profile_path": extracted_assets.get("reference_style_profile", ""),
        "fingerprint_path": extracted_assets.get("reference_fingerprint", ""),
        "pacing_curve_path": extracted_assets.get("reference_pacing_curve", ""),
        "visual_patterns_path": extracted_assets.get("reference_visual_patterns", ""),
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
    parser = argparse.ArgumentParser(description="Analyze reference video/link/share text for V3 workflow.")
    parser.add_argument("--input", help="Douyin URL, share text, or local video path.")
    parser.add_argument("--text", help="Legacy alias for --input.")
    parser.add_argument("--out", required=True, help="Output reference_analysis.json path.")
    parser.add_argument("--project-dir", help="Accepted for backward compatibility; not required in V3.")
    args = parser.parse_args()

    raw_input = args.input or args.text
    if not raw_input:
        parser.error("--input is required")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    analysis = build_analysis(raw_input, out)
    out.write_text(json.dumps(analysis, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(analysis, ensure_ascii=False, indent=2))
    return 1 if analysis["originality_plan"]["similarity_risk"] == "high" else 0


if __name__ == "__main__":
    raise SystemExit(main())
