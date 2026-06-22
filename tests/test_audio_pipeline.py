import json
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def run(command):
    return subprocess.run(command, text=True, capture_output=True, check=False)


def write_silence(path: Path, duration: float, sample_rate: int = 16000) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = int(duration * sample_rate)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(b"\x00\x00" * frames)


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"), reason="ffmpeg/ffprobe required")
def test_continuous_narration_bed_remux_and_continuity_check(tmp_path):
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    audio_dir = project / "assets" / "audio"
    internal.mkdir(parents=True)
    write_silence(audio_dir / "scene-01.wav", 0.5)
    write_silence(audio_dir / "scene-02.wav", 0.5)
    storyboard = {
        "title": "AI test",
        "target": {"format": "1920x1080"},
        "quality_spec": {"target_quality_level": "high_quality"},
        "director_shots": [
            {"shot_id": "S01", "duration_sec": 9.9},
            {"shot_id": "S02", "duration_sec": 9.9},
        ],
        "scenes": [
            {"scene_id": "S01", "sync": {"max_audio_gap_ms": 80}},
            {"scene_id": "S02", "sync": {"max_audio_gap_ms": 80}},
        ],
    }
    storyboard_path = internal / "storyboard.json"
    storyboard_path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")

    narration = audio_dir / "narration-continuous.wav"
    lock = internal / "storyboard.audio_locked.json"
    build = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_narration_bed.py"),
            "--storyboard",
            str(storyboard_path),
            "--audio-dir",
            str(audio_dir),
            "--out-audio",
            str(narration),
            "--out-lock",
            str(lock),
        ]
    )
    assert build.returncode == 0, build.stderr
    locked = json.loads(lock.read_text(encoding="utf-8"))
    assert locked["audio_lock"]["scene_audio"][0]["start"] == 0
    assert locked["audio_lock"]["scene_audio"][1]["start"] == 0.5
    assert locked["scenes"][0]["sync"]["narration_track"] == "continuous_root_audio"
    assert locked["director_shots"][0]["duration_sec"] == 0.5
    assert locked["director_shots"][0]["timing_source"] == "tts_audio_lock"
    synced_storyboard = json.loads(storyboard_path.read_text(encoding="utf-8"))
    assert synced_storyboard["director_shots"][0]["duration_sec"] == 0.5
    assert "audio_lock" not in synced_storyboard
    assert narration.exists()

    silent_video = internal / "draft_silent.mp4"
    make_video = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=size=160x90:rate=30:duration=1",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(silent_video),
        ]
    )
    assert make_video.returncode == 0, make_video.stderr

    final_video = internal / "draft.mp4"
    remux = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "remux_root_audio.py"),
            "--video",
            str(silent_video),
            "--audio",
            str(narration),
            "--out",
            str(final_video),
        ]
    )
    assert remux.returncode == 0, remux.stderr

    report_path = internal / "audio_continuity_report.json"
    check = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "check_audio_continuity.py"),
            "--video",
            str(final_video),
            "--lock",
            str(lock),
            "--out",
            str(report_path),
            "--max-duration-gap",
            "0.6",
        ]
    )
    assert check.returncode == 0, check.stderr
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["status"] == "passed"
    assert report["audio"]["has_audio"] is True
    assert report["audio_lock"]["transition_gaps"][0]["gap_ms"] == 0


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"), reason="ffmpeg/ffprobe required")
def test_mix_voice_sfx_builds_thick_male_video_mix_report(tmp_path):
    voice = tmp_path / "voice.wav"
    sfx = tmp_path / "sfx.wav"
    video = tmp_path / "silent.mp4"
    out = tmp_path / "out.mp4"
    report_path = tmp_path / "voice_mix_report.json"
    profile_path = tmp_path / "fixed_template_selection.json"
    profile_path.write_text(
        json.dumps(
            {
                "voice_mix_profile": {
                    "id": "VOICE_MALE_THICK_YUNYANG_V1",
                    "mix_preset": "thick-male",
                    "voice_gain_range": [1.35, 1.55],
                    "sfx_gain_range": [0.45, 0.6],
                }
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    make_voice = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=180:duration=1",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(voice),
        ]
    )
    assert make_voice.returncode == 0, make_voice.stderr
    make_sfx = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=900:duration=1",
            "-ar",
            "48000",
            "-ac",
            "2",
            str(sfx),
        ]
    )
    assert make_sfx.returncode == 0, make_sfx.stderr
    make_video = run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:size=160x90:rate=30:duration=1",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(video),
        ]
    )
    assert make_video.returncode == 0, make_video.stderr

    mix = run(
        [
            sys.executable,
            str(ROOT / "scripts" / "mix_voice_sfx.py"),
            "--video",
            str(video),
            "--voice",
            str(voice),
            "--sfx",
            str(sfx),
            "--profile-json",
            str(profile_path),
            "--voice-gain",
            "1.10",
            "--sfx-gain",
            "4.00",
            "--out",
            str(out),
            "--report",
            str(report_path),
        ]
    )
    assert mix.returncode == 0, mix.stderr
    assert out.exists()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["status"] == "passed"
    assert report["mix"]["preset"] == "thick-male"
    assert report["mix"]["profile_id"] == "VOICE_MALE_THICK_YUNYANG_V1"
    assert report["mix"]["amix_normalize"] == 0
    assert report["levels"]["final_mix"]["max_volume"] is not None
    assert report["sfx_audibility"]["status"] == "passed"
    assert report["sfx_audibility"]["effective_sfx_peak_after_gain_dbfs"] >= -15.0

    probed = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_streams",
            str(out),
        ]
    )
    assert probed.returncode == 0, probed.stderr
    streams = json.loads(probed.stdout)["streams"]
    assert any(stream["codec_type"] == "audio" for stream in streams)
