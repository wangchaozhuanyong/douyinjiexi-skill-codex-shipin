#!/usr/bin/env python3
"""Generate one continuous narration track and Remotion Caption JSON."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import uuid
from pathlib import Path
from typing import Any


SRT_BLOCK = re.compile(
    r"(?:\d+\s+)?"
    r"(?P<start>\d{2}:\d{2}:\d{2}[,.]\d{3})\s+-->\s+"
    r"(?P<end>\d{2}:\d{2}:\d{2}[,.]\d{3})\s+"
    r"(?P<text>.*?)(?=\n{2,}|\Z)",
    re.DOTALL,
)


def load_script(path: Path) -> tuple[dict[str, Any], str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("script must contain a JSON object")
    beats = data.get("beats")
    if not isinstance(beats, list) or not beats:
        raise ValueError("script.beats must be a non-empty array")
    parts = [
        str(item.get("narration") or "").strip()
        for item in beats
        if isinstance(item, dict) and str(item.get("narration") or "").strip()
    ]
    if not parts:
        raise ValueError("script.beats contain no narration")
    return data, " ".join(parts)


def milliseconds(value: str) -> int:
    hours, minutes, rest = value.replace(",", ".").split(":")
    seconds, fraction = rest.split(".")
    return (
        int(hours) * 3_600_000
        + int(minutes) * 60_000
        + int(seconds) * 1_000
        + int(fraction.ljust(3, "0")[:3])
    )


def parse_srt(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    captions: list[dict[str, Any]] = []
    for match in SRT_BLOCK.finditer(text):
        value = " ".join(match.group("text").split())
        start = milliseconds(match.group("start"))
        end = milliseconds(match.group("end"))
        if value and end > start:
            captions.append(
                {
                    "text": value,
                    "startMs": start,
                    "endMs": end,
                    "timestampMs": start,
                    "confidence": None,
                }
            )
    if not captions:
        raise ValueError(f"no captions parsed from {path}")
    return captions


def split_long_captions(
    captions: list[dict[str, Any]],
    max_characters: int = 12,
) -> list[dict[str, Any]]:
    segmented: list[dict[str, Any]] = []
    for caption in captions:
        text = str(caption["text"]).strip()
        phrases = [
            value.strip()
            for value in re.findall(r"[^，。！？；：、,.!?;:]+[，。！？；：、,.!?;:]?", text)
            if value.strip()
        ]
        chunks: list[str] = []
        for phrase in phrases or [text]:
            while len(phrase) > max_characters:
                chunks.append(phrase[:max_characters])
                phrase = phrase[max_characters:]
            if phrase:
                chunks.append(phrase)
        total_characters = sum(len(value) for value in chunks) or 1
        start = int(caption["startMs"])
        end = int(caption["endMs"])
        cursor = start
        for index, chunk in enumerate(chunks):
            chunk_end = (
                end
                if index == len(chunks) - 1
                else cursor + round((end - start) * len(chunk) / total_characters)
            )
            chunk_end = max(cursor + 1, min(end, chunk_end))
            segmented.append(
                {
                    "text": chunk,
                    "startMs": cursor,
                    "endMs": chunk_end,
                    "timestampMs": cursor,
                    "confidence": caption.get("confidence"),
                }
            )
            cursor = chunk_end
    return segmented


def generate_edge(
    text: str,
    out_audio: Path,
    voice: str,
    rate: str,
    pitch: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if importlib.util.find_spec("edge_tts") is None:
        raise RuntimeError("edge_tts Python package is unavailable")
    with tempfile.TemporaryDirectory(prefix="douyin-edge-tts-") as temp_dir:
        temp = Path(temp_dir)
        input_text = temp / "narration.txt"
        subtitles = temp / "narration.srt"
        input_text.write_text(text, encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "edge_tts",
                "--file",
                str(input_text),
                "--voice",
                voice,
                f"--rate={rate}",
                f"--pitch={pitch}",
                "--write-media",
                str(out_audio),
                "--write-subtitles",
                str(subtitles),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0 or not out_audio.is_file():
            raise RuntimeError(result.stderr.strip() or "edge-tts generation failed")
        captions = split_long_captions(parse_srt(subtitles))
    return captions, {
        "voice": voice,
        "rate": rate,
        "pitch": pitch,
        "alignment": "edge_boundary_segmented",
        "precision_note": "short phrase timing is apportioned inside Edge boundary events",
    }


def http_json(
    url: str,
    *,
    headers: dict[str, str],
    payload: bytes,
    content_type: str,
) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={**headers, "Content-Type": content_type},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return response.read(), dict(response.headers.items())


def multipart_alignment(audio: Path, text: str, api_key: str) -> dict[str, Any]:
    boundary = f"----douyin-{uuid.uuid4().hex}"
    chunks: list[bytes] = []

    def add(value: str) -> None:
        chunks.append(value.encode("utf-8"))

    add(f"--{boundary}\r\n")
    add('Content-Disposition: form-data; name="text"\r\n\r\n')
    add(text)
    add("\r\n")
    add(f"--{boundary}\r\n")
    add(
        'Content-Disposition: form-data; name="file"; '
        f'filename="{audio.name}"\r\n'
    )
    add("Content-Type: audio/mpeg\r\n\r\n")
    chunks.append(audio.read_bytes())
    add("\r\n")
    add(f"--{boundary}--\r\n")
    body, _ = http_json(
        "https://api.elevenlabs.io/v1/forced-alignment",
        headers={"xi-api-key": api_key},
        payload=b"".join(chunks),
        content_type=f"multipart/form-data; boundary={boundary}",
    )
    result = json.loads(body.decode("utf-8"))
    if not isinstance(result, dict):
        raise RuntimeError("ElevenLabs alignment returned an invalid response")
    return result


def generate_eleven(
    text: str,
    out_audio: Path,
    voice_id: str,
    model_id: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is missing")
    if not voice_id:
        raise RuntimeError("ElevenLabs voice id is missing")
    request_body = json.dumps(
        {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.75,
                "style": 0.25,
                "speed": 1.0,
            },
        }
    ).encode("utf-8")
    audio, _ = http_json(
        (
            "https://api.elevenlabs.io/v1/text-to-speech/"
            f"{voice_id}?output_format=mp3_44100_128"
        ),
        headers={"xi-api-key": api_key, "Accept": "audio/mpeg"},
        payload=request_body,
        content_type="application/json",
    )
    if not audio:
        raise RuntimeError("ElevenLabs returned empty audio")
    out_audio.write_bytes(audio)
    alignment = multipart_alignment(out_audio, text, api_key)
    words = alignment.get("words")
    if not isinstance(words, list) or not words:
        raise RuntimeError("ElevenLabs Forced Alignment returned no words")
    captions = []
    for item in words:
        if not isinstance(item, dict):
            continue
        start = int(float(item.get("start") or 0) * 1000)
        end = int(float(item.get("end") or 0) * 1000)
        word = str(item.get("text") or "")
        if word and end > start:
            loss = item.get("loss")
            captions.append(
                {
                    "text": word,
                    "startMs": start,
                    "endMs": end,
                    "timestampMs": start,
                    "confidence": None if loss is None else max(0.0, 1.0 - float(loss)),
                }
            )
    if not captions:
        raise RuntimeError("ElevenLabs alignment did not produce usable captions")
    return captions, {
        "voice": voice_id,
        "model": model_id,
        "alignment": "elevenlabs_forced_alignment",
        "alignment_loss": alignment.get("loss"),
    }


def copy_existing(
    existing_audio: Path,
    existing_captions: Path,
    out_audio: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not existing_audio.is_file() or not existing_captions.is_file():
        raise RuntimeError("existing provider requires audio and captions files")
    shutil.copy2(existing_audio, out_audio)
    captions = json.loads(existing_captions.read_text(encoding="utf-8"))
    if not isinstance(captions, list) or not captions:
        raise RuntimeError("existing captions must be a non-empty JSON array")
    return captions, {
        "voice": "user_provided",
        "model": "not_applicable",
        "alignment": "user_provided",
    }


def analyze_loudness(ffmpeg: str, audio: Path) -> dict[str, str]:
    result = subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "info",
            "-i",
            str(audio),
            "-af",
            "loudnorm=I=-16:LRA=7:TP=-1.5:print_format=json",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    matches = re.findall(r'\{\s*"input_i".*?\}', result.stderr, re.DOTALL)
    if result.returncode != 0 or not matches:
        raise RuntimeError(result.stderr.strip() or "narration loudness analysis failed")
    return json.loads(matches[-1])


def normalize_audio(audio: Path) -> dict[str, float]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required for narration loudness normalization")
    normalized = audio.with_name(f"{audio.stem}.normalized{audio.suffix}")
    measured = analyze_loudness(ffmpeg, audio)
    loudnorm = (
        "loudnorm=I=-16:LRA=7:TP=-1.5:"
        f"measured_I={measured['input_i']}:"
        f"measured_LRA={measured['input_lra']}:"
        f"measured_TP={measured['input_tp']}:"
        f"measured_thresh={measured['input_thresh']}:"
        f"offset={measured['target_offset']}:"
        "linear=true:print_format=summary"
    )
    with tempfile.TemporaryDirectory(prefix="voice-normalize-", dir=audio.parent) as temp_dir:
        intermediate = Path(temp_dir) / "normalized.wav"
        first = subprocess.run(
            [
                ffmpeg,
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(audio),
                "-af",
                loudnorm,
                "-ar",
                "48000",
                "-ac",
                "2",
                "-c:a",
                "pcm_s24le",
                str(intermediate),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if first.returncode != 0 or not intermediate.is_file():
            raise RuntimeError(first.stderr.strip() or "narration normalization failed")
        interim_metrics = analyze_loudness(ffmpeg, intermediate)
        gain_db = min(
            -16.0 - float(interim_metrics["input_i"]),
            -1.5 - float(interim_metrics["input_tp"]),
        )
        final_args = [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(intermediate),
            "-af",
            f"volume={gain_db:.3f}dB",
            "-ar",
            "48000",
            "-ac",
            "2",
        ]
        if audio.suffix.lower() == ".mp3":
            final_args += ["-b:a", "192k"]
        final_args.append(str(normalized))
        final = subprocess.run(
            final_args,
            capture_output=True,
            text=True,
            check=False,
        )
        if final.returncode != 0 or not normalized.is_file():
            raise RuntimeError(final.stderr.strip() or "narration final gain failed")
    normalized.replace(audio)
    final_metrics = analyze_loudness(ffmpeg, audio)
    return {
        "integrated_lufs": float(final_metrics["input_i"]),
        "loudness_range_lu": float(final_metrics["input_lra"]),
        "true_peak_dbtp": float(final_metrics["input_tp"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", required=True)
    parser.add_argument("--out-audio", required=True)
    parser.add_argument("--out-captions", required=True)
    parser.add_argument("--out-report", required=True)
    parser.add_argument(
        "--provider",
        choices=("auto", "elevenlabs", "edge-tts", "existing"),
        default="auto",
    )
    parser.add_argument("--voice-id")
    parser.add_argument("--model-id", default="eleven_v3")
    parser.add_argument("--edge-voice", default="zh-CN-YunyangNeural")
    parser.add_argument("--edge-rate", default="+6%")
    parser.add_argument("--edge-pitch", default="-2Hz")
    parser.add_argument("--existing-audio")
    parser.add_argument("--existing-captions")
    args = parser.parse_args()

    script_path = Path(args.script).resolve()
    out_audio = Path(args.out_audio).resolve()
    out_captions = Path(args.out_captions).resolve()
    out_report = Path(args.out_report).resolve()
    _, text = load_script(script_path)
    provider = args.provider
    voice_id = (
        args.voice_id
        or os.environ.get("ELEVENLABS_VOICE_ID")
        or os.environ.get("ELEVEN_VOICE_ID")
        or ""
    )
    if provider == "auto":
        provider = (
            "elevenlabs"
            if os.environ.get("ELEVENLABS_API_KEY") and voice_id
            else "edge-tts"
        )

    out_audio.parent.mkdir(parents=True, exist_ok=True)
    out_captions.parent.mkdir(parents=True, exist_ok=True)
    out_report.parent.mkdir(parents=True, exist_ok=True)
    if provider == "elevenlabs":
        captions, details = generate_eleven(text, out_audio, voice_id, args.model_id)
    elif provider == "edge-tts":
        captions, details = generate_edge(
            text,
            out_audio,
            args.edge_voice,
            args.edge_rate,
            args.edge_pitch,
        )
    else:
        if not args.existing_audio or not args.existing_captions:
            raise SystemExit("existing provider requires --existing-audio and --existing-captions")
        captions, details = copy_existing(
            Path(args.existing_audio).resolve(),
            Path(args.existing_captions).resolve(),
            out_audio,
        )

    details["loudness_measured"] = normalize_audio(out_audio)
    details["loudness_target"] = {
        "integrated_lufs": -16,
        "loudness_range_lu": 7,
        "true_peak_dbtp": -1.5,
    }
    out_captions.write_text(
        json.dumps(captions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    report = {
        "status": "passed",
        "provider": provider,
        "script": str(script_path),
        "audio": str(out_audio),
        "captions": str(out_captions),
        "caption_count": len(captions),
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "fallback_used": args.provider == "auto" and provider != "elevenlabs",
        "details": details,
    }
    out_report.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
