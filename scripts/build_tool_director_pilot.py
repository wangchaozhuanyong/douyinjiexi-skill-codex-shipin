#!/usr/bin/env python3
"""Build real validation evidence, voice, and timing for the free-director pilot."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "samples" / "free-director-tool"
CORE = ROOT / "skills" / "douyin-video-production-core"
VALIDATOR = CORE / "scripts" / "validate_project.py"
VOICEOVER = CORE / "scripts" / "generate_voiceover.py"
CAPTURED_AT = "2026-07-26T22:30:00-07:00"


def write_json(path: Path, data: dict[str, Any] | list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def base_fixture(project: Path) -> None:
    proof = project / "proof.txt"
    proof.write_text("visible result\n", encoding="utf-8")
    write_json(
        project / "source_brief.json",
        {
            "format_type": "tool_explainer",
            "project_name": "AI工具实操讲解-预检证据演示01",
            "classification": {
                "level_1": "AI类视频",
                "level_2": "AI工具实操讲解类",
                "level_3": "Skill / 预检工具",
                "category_code": "ai_tool_explainer",
            },
            "topic": "claim-proof validator demonstration",
            "captured_at": CAPTURED_AT,
            "sources": [
                {
                    "id": "S1",
                    "title": "real local result",
                    "source_type": "real_execution",
                    "locator": "proof.txt",
                    "captured_at": CAPTURED_AT,
                    "supports_claims": ["C1"],
                }
            ],
            "claims": [
                {
                    "id": "C1",
                    "text": "the result is visible",
                    "fact_status": "confirmed",
                    "source_ids": ["S1"],
                }
            ],
        },
    )
    write_json(
        project / "script.json",
        {
            "format_type": "tool_explainer",
            "title": "validator demo",
            "hook": "show the result",
            "viewer_task": "verify a visible tool result",
            "input_method": "one sanitized local request",
            "execution_process": "bind one claim to one proof",
            "visible_result": "a real proof file",
            "before_after": "missing proof to visible proof",
            "safety_constraints": ["read-only local fixture"],
            "privacy_redactions": ["temporary path hidden"],
            "result_acceptance": ["validator returns passed"],
            "risk_review": {
                "level": "low",
                "sensitive_domains": [],
                "demo_environment": "sanitized_local",
                "real_action_policy": "read_only",
                "stop_conditions": ["stop before external action"],
            },
            "beats": [
                {
                    "id": "B1",
                    "narration": "show the result",
                    "claim_ids": ["C1"],
                    "proof_ids": ["P-MISSING"],
                }
            ],
            "closing_takeaway": "claim and proof must match",
        },
    )
    write_json(
        project / "storyboard.json",
        {
            "format_type": "tool_explainer",
            "width": 1080,
            "height": 1920,
            "fps": 30,
            "creative_direction": {
                "visual_thesis": "show the real result as proof",
                "reason_for_topic": "the validation state is the result",
                "evidence_strategy": "keep the proof filename readable",
                "motion_logic": "change only when validation changes",
                "continuity_devices": ["one proof cursor"],
                "rejected_defaults": ["generic card stack"],
            },
            "render_plan": {
                "canonical_renderer": "remotion",
                "composition_id": "Demo",
                "optional_subrenderers": [],
            },
            "scenes": [
                {
                    "id": "SC1",
                    "start": 0,
                    "end": 3,
                    "beat_ids": ["B1"],
                    "claim_ids": ["C1"],
                    "proof_ids": ["P-MISSING"],
                    "visual_mode": "real_result",
                    "visual": "show the exact proof file",
                    "evidence_display": "the proof filename and contents are readable",
                    "motion_intent": "reveal the result once",
                    "change_reason": "the result claim begins",
                    "caption": "visible result",
                }
            ],
        },
    )
    write_json(
        project / "asset_manifest.json",
        {
            "assets": [
                {
                    "id": "P1",
                    "role": "proof",
                    "source_kind": "real_capture",
                    "path": "proof.txt",
                    "source_locator": "real local fixture",
                    "captured_at": CAPTURED_AT,
                    "supports_claims": ["C1"],
                }
            ]
        },
    )


def sanitize_report(report: dict[str, Any], project: Path) -> dict[str, Any]:
    serialized = json.dumps(report, ensure_ascii=False)
    serialized = serialized.replace(str(project), "[sanitized-demo-project]")
    clean = json.loads(serialized)
    clean["privacy_redaction"] = "temporary absolute path replaced with [sanitized-demo-project]"
    clean["evidence_kind"] = "real validator execution"
    return clean


def run_validator(project: Path, out: Path, expected: int) -> dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--project",
            str(project),
            "--phase",
            "preproduction",
            "--out",
            str(out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != expected:
        raise RuntimeError(
            f"validator returned {result.returncode}, expected {expected}\n"
            f"{result.stdout}\n{result.stderr}"
        )
    return json.loads(out.read_text(encoding="utf-8"))


def build_validation_evidence() -> None:
    proof_dir = SAMPLE / "proof"
    proof_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="free-director-proof-") as temp:
        fixture = Path(temp)
        base_fixture(fixture)
        blocked_path = fixture / "blocked.json"
        blocked = run_validator(fixture, blocked_path, expected=2)
        write_json(
            proof_dir / "blocked-validation.json",
            sanitize_report(blocked, fixture),
        )

        script_path = fixture / "script.json"
        storyboard_path = fixture / "storyboard.json"
        script = json.loads(script_path.read_text(encoding="utf-8"))
        storyboard = json.loads(storyboard_path.read_text(encoding="utf-8"))
        script["beats"][0]["proof_ids"] = ["P1"]
        storyboard["scenes"][0]["proof_ids"] = ["P1"]
        write_json(script_path, script)
        write_json(storyboard_path, storyboard)
        passed_path = fixture / "passed.json"
        passed = run_validator(fixture, passed_path, expected=0)
        write_json(
            proof_dir / "passed-validation.json",
            sanitize_report(passed, fixture),
        )


def probe_duration(audio: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "ffprobe duration failed")
    return float(result.stdout.strip())


def sync_storyboard_timing(audio_duration: float) -> None:
    script = json.loads((SAMPLE / "script.json").read_text(encoding="utf-8"))
    storyboard_path = SAMPLE / "storyboard.json"
    storyboard = json.loads(storyboard_path.read_text(encoding="utf-8"))
    beats = script["beats"]
    scenes = storyboard["scenes"]
    if len(beats) != len(scenes):
        raise RuntimeError("pilot expects one scene per narration beat")
    weights = [max(1, len(str(beat["narration"]))) for beat in beats]
    total_weight = sum(weights)
    total_duration = audio_duration + 0.2
    cursor = 0.0
    for index, (scene, weight) in enumerate(zip(scenes, weights)):
        start = cursor
        cursor = total_duration if index == len(scenes) - 1 else cursor + total_duration * weight / total_weight
        scene["start"] = round(start, 3)
        scene["end"] = round(cursor, 3)
    write_json(storyboard_path, storyboard)


def generate_voice(provider: str) -> None:
    audio = SAMPLE / "public" / "audio" / "narration.mp3"
    captions = SAMPLE / "public" / "data" / "captions.json"
    report = SAMPLE / "voiceover_report.json"
    result = subprocess.run(
        [
            sys.executable,
            str(VOICEOVER),
            "--script",
            str(SAMPLE / "script.json"),
            "--out-audio",
            str(audio),
            "--out-captions",
            str(captions),
            "--out-report",
            str(report),
            "--provider",
            provider,
        ],
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("voiceover generation failed")
    sync_storyboard_timing(probe_duration(audio))


def validate_sample() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--project",
            str(SAMPLE),
            "--phase",
            "preproduction",
            "--out",
            str(SAMPLE / "validation_report.json"),
        ],
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("free-director pilot preproduction validation failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--voice-provider",
        choices=("auto", "elevenlabs", "edge-tts"),
        default="auto",
    )
    args = parser.parse_args()
    build_validation_evidence()
    generate_voice(args.voice_provider)
    validate_sample()
    print(
        json.dumps(
            {
                "status": "passed",
                "sample": str(SAMPLE),
                "proof": [
                    str(SAMPLE / "proof" / "blocked-validation.json"),
                    str(SAMPLE / "proof" / "passed-validation.json"),
                ],
                "voiceover": str(SAMPLE / "voiceover_report.json"),
                "validation": str(SAMPLE / "validation_report.json"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
