#!/usr/bin/env python3
"""Build a continuous narration bed from per-scene audio files."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from artifact_fingerprint import write_report_with_fingerprints


AUDIO_EXTENSIONS = [".wav", ".mp3", ".m4a", ".aac", ".flac", ".ogg"]
DEFAULT_MAX_GAP_MS = 80
DIRECTOR_DURATION_TOLERANCE_SEC = 0.3


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} is required but was not found on PATH")
    return path


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def ffprobe_duration(path: Path) -> float:
    ffprobe = require_tool("ffprobe")
    result = run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"ffprobe failed for {path}")
    return float(result.stdout.strip())


def ffmpeg_concat(audio_paths: list[Path], out_audio: Path) -> None:
    ffmpeg = require_tool("ffmpeg")
    out_audio.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
        list_path = Path(handle.name)
        for audio_path in audio_paths:
            escaped = str(audio_path.resolve()).replace("'", "'\\''")
            handle.write(f"file '{escaped}'\n")
    try:
        codec_args = ["-c:a", "aac", "-b:a", "192k"]
        suffix = out_audio.suffix.lower()
        if suffix == ".mp3":
            codec_args = ["-c:a", "libmp3lame", "-q:a", "2"]
        elif suffix == ".wav":
            codec_args = ["-c:a", "pcm_s16le"]
        result = run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(list_path),
                *codec_args,
                str(out_audio),
            ]
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "ffmpeg concat failed")
    finally:
        list_path.unlink(missing_ok=True)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def relative_to_project(path: Path, project: Path) -> str:
    try:
        return str(path.resolve().relative_to(project.resolve()))
    except ValueError:
        return str(path)


def find_scene_audio(scene: dict[str, Any], index: int, audio_dir: Path) -> Path:
    scene_id = str(scene.get("scene_id") or f"S{index:02d}")
    explicit = (
        scene.get("audio_path")
        or scene.get("voice_audio_path")
        or (scene.get("sync") if isinstance(scene.get("sync"), dict) else {}).get("audio_path")
    )
    if explicit:
        path = Path(str(explicit)).expanduser()
        if not path.is_absolute():
            path = audio_dir / path
        if path.exists() and path.stat().st_size > 0:
            return path
        raise FileNotFoundError(f"{scene_id}: explicit audio file missing: {explicit}")

    stems = [
        scene_id,
        scene_id.lower(),
        f"scene-{index:02d}",
        f"scene_{index:02d}",
        f"s{index:02d}",
        f"S{index:02d}",
        f"{index:02d}",
    ]
    for stem in stems:
        for extension in AUDIO_EXTENSIONS:
            candidate = audio_dir / f"{stem}{extension}"
            if candidate.exists() and candidate.stat().st_size > 0:
                return candidate
    raise FileNotFoundError(f"{scene_id}: no audio found in {audio_dir}")


def default_transition_policy(sync: dict[str, Any]) -> dict[str, Any]:
    result = dict(sync)
    result.setdefault("narration_track", "continuous_root_audio")
    result.setdefault("transition_audio_policy", "visual-only transition; narration continues with no restart or mute")
    result.setdefault("max_audio_gap_ms", DEFAULT_MAX_GAP_MS)
    result.setdefault("audio_bridge", "continuous clean narration bed under visual transition; no background audio by default")
    return result


def build_lock(storyboard: dict[str, Any], audio_dir: Path, out_audio: Path, project: Path) -> tuple[dict[str, Any], list[Path]]:
    scenes = storyboard.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("storyboard.scenes must be a non-empty array")

    locked = dict(storyboard)
    locked_scenes: list[dict[str, Any]] = []
    scene_audio: list[dict[str, Any]] = []
    audio_paths: list[Path] = []
    cursor = 0.0

    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            raise ValueError(f"scene {index} must be an object")
        scene_id = str(scene.get("scene_id") or f"S{index:02d}")
        audio_path = find_scene_audio(scene, index, audio_dir)
        duration = ffprobe_duration(audio_path)
        start = cursor
        end = cursor + duration
        cursor = end

        locked_scene = dict(scene)
        locked_scene["duration_target"] = round(duration, 3)
        sync = default_transition_policy(scene.get("sync", {}) if isinstance(scene.get("sync"), dict) else {})
        sync.update(
            {
                "voice_start": round(start, 3),
                "voice_end": round(end, 3),
                "caption_start": round(start, 3),
                "caption_end": round(end, 3),
                "audio_path": relative_to_project(audio_path, project),
            }
        )
        locked_scene["sync"] = sync
        locked_scenes.append(locked_scene)
        audio_paths.append(audio_path)
        scene_audio.append(
            {
                "scene_id": scene_id,
                "audio_path": relative_to_project(audio_path, project),
                "duration": round(duration, 3),
                "start": round(start, 3),
                "end": round(end, 3),
                "max_audio_gap_ms": int(sync.get("max_audio_gap_ms") or DEFAULT_MAX_GAP_MS),
            }
        )

    locked["scenes"] = locked_scenes
    sync_director_shot_durations(locked, scene_audio)
    locked["audio_lock"] = {
        "narration_track": "continuous_root_audio",
        "root_narration_path": relative_to_project(out_audio, project),
        "scene_audio": scene_audio,
        "total_audio_duration": round(cursor, 3),
        "max_audio_gap_ms": min(item["max_audio_gap_ms"] for item in scene_audio),
        "transition_audio_policy": "visual-only transitions; narration is continuous root audio and never restarts, mutes, fades, or gaps",
    }
    return locked, audio_paths


def sync_director_shot_durations(storyboard: dict[str, Any], scene_audio: list[dict[str, Any]]) -> None:
    """Copy real audio durations into matching director shots.

    Director shots are the visual source of truth for text-manifest timing.
    After TTS is locked, stale director timings make proofread/contact-sheet
    gates reason about a different video than the rendered one.
    """
    shots = storyboard.get("director_shots")
    if not isinstance(shots, list) or not shots:
        return

    by_scene_id = {str(item.get("scene_id")): item for item in scene_audio if item.get("scene_id")}
    for index, shot in enumerate(shots):
        if not isinstance(shot, dict):
            continue
        shot_id = str(shot.get("shot_id") or "")
        item = by_scene_id.get(shot_id)
        if item is None and index < len(scene_audio):
            item = scene_audio[index]
        if item is None:
            continue
        shot["duration_sec"] = round(float(item.get("duration") or 0), 3)
        shot["timing_source"] = "tts_audio_lock"


def storyboard_without_audio_lock(locked: dict[str, Any]) -> dict[str, Any]:
    synced = dict(locked)
    synced.pop("audio_lock", None)
    return synced


def main() -> int:
    parser = argparse.ArgumentParser(description="Build continuous root narration audio and storyboard.audio_locked.json.")
    parser.add_argument("--storyboard", required=True, help="storyboard.json path")
    parser.add_argument("--audio-dir", required=True, help="Directory containing per-scene audio files")
    parser.add_argument("--out-audio", required=True, help="Continuous narration output path, e.g. assets/audio/narration-continuous.mp3")
    parser.add_argument("--out-lock", required=True, help="storyboard.audio_locked.json output path")
    parser.add_argument(
        "--no-sync-storyboard",
        action="store_true",
        help="Do not write locked scene/director timings back to the source storyboard.json.",
    )
    args = parser.parse_args()

    storyboard_path = Path(args.storyboard)
    audio_dir = Path(args.audio_dir)
    out_audio = Path(args.out_audio)
    out_lock = Path(args.out_lock)
    project = out_lock.parents[1] if out_lock.parent.name == "internal" else storyboard_path.parent.parent

    storyboard = load_json(storyboard_path)
    locked, audio_paths = build_lock(storyboard, audio_dir, out_audio, project)
    ffmpeg_concat(audio_paths, out_audio)
    final_duration = ffprobe_duration(out_audio)
    locked["audio_lock"]["final_audio_duration"] = round(final_duration, 3)
    locked["audio_lock"]["duration_delta"] = round(abs(final_duration - locked["audio_lock"]["total_audio_duration"]), 3)

    out_lock.parent.mkdir(parents=True, exist_ok=True)
    if not args.no_sync_storyboard:
        storyboard_path.write_text(
            json.dumps(storyboard_without_audio_lock(locked), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    fingerprint_inputs = [storyboard_path, *audio_paths, out_audio]
    write_report_with_fingerprints(locked, [path for path in fingerprint_inputs if path.exists() and path.is_file()])
    out_lock.write_text(json.dumps(locked, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(locked["audio_lock"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
