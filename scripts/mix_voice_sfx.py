#!/usr/bin/env python3
"""Build a narration-first voice/SFX mix and optionally remux it into a video."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


PRESETS = {
    "balanced": {
        "voice_gain": 1.25,
        "sfx_gain": 0.42,
        "voice_filter": ",".join(
            [
                "highpass=f=65",
                "acompressor=threshold=-20dB:ratio=2.4:attack=8:release=95:makeup=1.5",
                "alimiter=limit=0.90",
            ]
        ),
    },
    "thick-male": {
        "voice_gain": 1.38,
        "sfx_gain": 0.50,
        "voice_filter": ",".join(
            [
                "highpass=f=65",
                "equalizer=f=120:t=q:w=1.0:g=4.2",
                "equalizer=f=220:t=q:w=1.1:g=2.5",
                "equalizer=f=3200:t=q:w=1.0:g=1.2",
                "acompressor=threshold=-20dB:ratio=2.8:attack=8:release=95:makeup=2.2",
                "alimiter=limit=0.90",
            ]
        ),
    },
}


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} is required but was not found on PATH")
    return path


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def ensure_media(path: Path, label: str) -> None:
    if not path.exists() or not path.is_file() or path.stat().st_size <= 0:
        raise SystemExit(f"{label} missing or empty: {path}")


def probe(path: Path) -> dict[str, Any]:
    ffprobe = require_tool("ffprobe")
    result = run(
        [
            ffprobe,
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"ffprobe failed for {path}")
    return json.loads(result.stdout)


def media_duration(path: Path) -> float:
    data = probe(path)
    fmt = data.get("format", {})
    streams = data.get("streams", [])
    durations = [float(item.get("duration") or 0) for item in streams if item.get("duration")]
    durations.append(float(fmt.get("duration") or 0))
    return max(durations or [0.0])


def audio_levels(path: Path) -> dict[str, Any]:
    ffmpeg = require_tool("ffmpeg")
    result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-af",
            "volumedetect",
            "-f",
            "null",
            "-",
        ]
    )
    text = "\n".join([result.stdout or "", result.stderr or ""])
    levels: dict[str, Any] = {"returncode": result.returncode}
    for key in ["mean_volume", "max_volume"]:
        match = re.search(rf"{key}:\s*(-?\d+(?:\.\d+)?)\s*dB", text)
        levels[key] = float(match.group(1)) if match else None
    if result.returncode != 0:
        levels["error"] = (result.stderr or "").strip()
    return levels


def silence_events(path: Path) -> list[str]:
    ffmpeg = require_tool("ffmpeg")
    result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-af",
            "silencedetect=n=-45dB:d=0.75",
            "-f",
            "null",
            "-",
        ]
    )
    return [line for line in (result.stderr or "").splitlines() if "silence_" in line]


def black_events(path: Path) -> list[str]:
    ffmpeg = require_tool("ffmpeg")
    result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostats",
            "-i",
            str(path),
            "-vf",
            "blackdetect=d=0.4:pic_th=0.98",
            "-an",
            "-f",
            "null",
            "-",
        ]
    )
    return [line for line in (result.stderr or "").splitlines() if "blackdetect" in line]


def process_voice(voice: Path, out: Path, duration: float, preset: str) -> None:
    ffmpeg = require_tool("ffmpeg")
    filters = f"{PRESETS[preset]['voice_filter']},apad,atrim=0:{duration:.3f}"
    result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(voice),
            "-af",
            filters,
            "-ar",
            "48000",
            "-ac",
            "2",
            str(out),
        ]
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "voice processing failed")


def mix_audio(processed_voice: Path, sfx: Path | None, out: Path, duration: float, voice_gain: float, sfx_gain: float) -> None:
    ffmpeg = require_tool("ffmpeg")
    out.parent.mkdir(parents=True, exist_ok=True)
    if sfx:
        command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(processed_voice),
            "-i",
            str(sfx),
            "-filter_complex",
            (
                f"[0:a]volume={voice_gain:.3f}[n];"
                f"[1:a]apad,atrim=0:{duration:.3f},volume={sfx_gain:.3f}[s];"
                "[n][s]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
                "alimiter=limit=0.88[out]"
            ),
            "-map",
            "[out]",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(out),
        ]
    else:
        command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(processed_voice),
            "-af",
            f"volume={voice_gain:.3f},alimiter=limit=0.88,atrim=0:{duration:.3f}",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(out),
        ]
    result = run(command)
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "audio mix failed")


def remux_video(video: Path, audio: Path, out: Path) -> None:
    ffmpeg = require_tool("ffmpeg")
    out.parent.mkdir(parents=True, exist_ok=True)
    result = run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            "-shortest",
            str(out),
        ]
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or "video remux failed")


def choose_duration(video: Path | None, voice: Path, override: float | None) -> float:
    if override and override > 0:
        return override
    if video:
        return media_duration(video)
    return media_duration(voice)


def load_mix_profile(path: Path | None) -> dict[str, Any]:
    if not path:
        return {}
    if not path.exists() or not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(f"voice mix profile missing or empty: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    profile = data.get("voice_mix_profile") if isinstance(data.get("voice_mix_profile"), dict) else data
    return profile if isinstance(profile, dict) else {}


def range_default(profile: dict[str, Any], key: str, fallback: float) -> float:
    value = profile.get(key)
    if isinstance(value, list) and value:
        numbers = [float(item) for item in value if isinstance(item, (int, float))]
        if numbers:
            return round(sum(numbers) / len(numbers), 3)
    return fallback


def main() -> int:
    parser = argparse.ArgumentParser(description="Mix thick narration with subtle SFX and optional video remux.")
    parser.add_argument("--video", help="Optional silent or draft MP4 to receive the mixed audio")
    parser.add_argument("--voice", required=True, help="Continuous narration audio path")
    parser.add_argument("--sfx", help="Optional root-level SFX bed path")
    parser.add_argument("--out", required=True, help="Output MP4 when --video is set; otherwise output WAV")
    parser.add_argument("--report", help="Optional JSON QA report path")
    parser.add_argument("--preset", choices=sorted(PRESETS))
    parser.add_argument("--profile-json", help="Optional fixed_template_selection.json or voice profile JSON")
    parser.add_argument("--voice-gain", type=float)
    parser.add_argument("--sfx-gain", type=float)
    parser.add_argument("--duration", type=float, help="Override mix duration in seconds")
    parser.add_argument("--processed-voice-out", help="Optional path to keep processed voice WAV")
    parser.add_argument("--mixed-audio-out", help="Optional path to keep mixed audio WAV")
    args = parser.parse_args()

    video = Path(args.video).expanduser() if args.video else None
    voice = Path(args.voice).expanduser()
    sfx = Path(args.sfx).expanduser() if args.sfx else None
    out = Path(args.out).expanduser()
    report_path = Path(args.report).expanduser() if args.report else None
    processed_voice_out = Path(args.processed_voice_out).expanduser() if args.processed_voice_out else None
    mixed_audio_out = Path(args.mixed_audio_out).expanduser() if args.mixed_audio_out else None
    mix_profile = load_mix_profile(Path(args.profile_json).expanduser() if args.profile_json else None)

    if video:
        ensure_media(video, "video")
    ensure_media(voice, "voice")
    if sfx:
        ensure_media(sfx, "sfx")

    profile_preset = str(mix_profile.get("mix_preset") or "")
    preset_name = args.preset or (profile_preset if profile_preset in PRESETS else "balanced")
    preset = PRESETS[preset_name]
    voice_gain = float(
        args.voice_gain
        if args.voice_gain is not None
        else range_default(mix_profile, "voice_gain_range", preset["voice_gain"])
    )
    sfx_gain = float(
        args.sfx_gain
        if args.sfx_gain is not None
        else range_default(mix_profile, "sfx_gain_range", preset["sfx_gain"])
    )
    duration = choose_duration(video, voice, args.duration)
    if duration <= 0:
        raise SystemExit("could not determine a positive mix duration")

    with tempfile.TemporaryDirectory(prefix="voice-sfx-mix-") as tmp:
        tmpdir = Path(tmp)
        processed_voice = processed_voice_out or tmpdir / "processed_voice.wav"
        mixed_audio = mixed_audio_out or (out if not video else tmpdir / "mixed_audio.wav")
        processed_voice.parent.mkdir(parents=True, exist_ok=True)
        mixed_audio.parent.mkdir(parents=True, exist_ok=True)

        process_voice(voice, processed_voice, duration, preset_name)
        mix_audio(processed_voice, sfx, mixed_audio, duration, voice_gain, sfx_gain)
        if video:
            remux_video(video, mixed_audio, out)

        output_media = out if video else mixed_audio
        final_levels = audio_levels(mixed_audio if video else output_media)
        issues: list[str] = []
        warnings: list[str] = []
        final_max = final_levels.get("max_volume")
        if final_max is None:
            warnings.append("final max_volume could not be detected")
        elif final_max > 0:
            issues.append("final mix clips above 0dB")
        elif final_max < -6:
            warnings.append("final mix is quieter than expected for voice-led Douyin video")

        output_probe = probe(output_media)
        if video:
            streams = output_probe.get("streams", [])
            fmt = output_probe.get("format", {})
            video_stream = next((item for item in streams if item.get("codec_type") == "video"), {})
            audio_stream = next((item for item in streams if item.get("codec_type") == "audio"), {})
            video_duration = float(video_stream.get("duration") or fmt.get("duration") or 0)
            audio_duration = float(audio_stream.get("duration") or 0)
            if not audio_stream:
                issues.append("output video has no audio stream")
            elif abs(video_duration - audio_duration) > 0.3:
                warnings.append("output audio/video duration gap is above 0.3s")
        else:
            video_duration = None
            audio_duration = media_duration(output_media)

        report = {
            "status": "passed" if not issues else "failed",
            "inputs": {
                "video": str(video) if video else None,
                "voice": str(voice),
                "sfx": str(sfx) if sfx else None,
            },
            "output": {
                "path": str(output_media),
                "video_duration": round(video_duration, 3) if video_duration is not None else None,
                "audio_duration": round(audio_duration, 3),
            },
            "mix": {
                "preset": preset_name,
                "profile_id": mix_profile.get("id"),
                "duration": round(duration, 3),
                "voice_gain": voice_gain,
                "sfx_gain": sfx_gain if sfx else None,
                "amix_normalize": 0 if sfx else None,
                "processed_voice_path": str(processed_voice) if processed_voice_out else None,
                "mixed_audio_path": str(mixed_audio) if mixed_audio_out else None,
            },
            "levels": {
                "source_voice": audio_levels(voice),
                "processed_voice": audio_levels(processed_voice),
                "source_sfx": audio_levels(sfx) if sfx else None,
                "final_mix": final_levels,
            },
            "qa": {
                "silencedetect": silence_events(mixed_audio if video else output_media),
                "blackdetect": black_events(output_media) if video else [],
            },
            "blocking_issues": issues,
            "warnings": warnings,
        }
        if report_path:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
