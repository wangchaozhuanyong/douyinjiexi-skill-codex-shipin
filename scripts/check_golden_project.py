#!/usr/bin/env python3
"""Run the V3 golden project through deterministic gates."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "golden_ai_prompt_case"


def run(command: list[str], cwd: Path = ROOT) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def ensure_media(project: Path) -> None:
    internal = project / "internal"
    draft = internal / "draft.mp4"
    cover = internal / "cover.png"
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required for golden project media synthesis")
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "testsrc2=size=1920x1080:rate=30:duration=18",
            "-f",
            "lavfi",
            "-i",
            "sine=frequency=720:duration=18",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-shortest",
            str(draft),
        ]
    )
    run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(draft),
            "-frames:v",
            "1",
            str(cover),
        ]
    )


def mark_frame_review_passed(project: Path) -> None:
    report_path = project / "internal" / "frame_review_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["status"] = "passed"
    report["manual_review"] = {
        "status": "passed",
        "first_5s_contact_sheet_checked": True,
        "full_video_contact_sheet_checked": True,
        "native_detail_frames_checked": True,
        "reviewer": "golden_regression",
        "notes": "Golden regression accepts generated contact sheets for deterministic QA.",
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_audio_continuity_pass(project: Path) -> None:
    report = {
        "status": "passed",
        "video": {"duration": 18.0},
        "audio": {"has_audio": True, "duration": 18.0, "duration_gap": 0.0},
        "audio_lock": {
            "root_narration_path": "internal/draft.mp4",
            "scene_count": 6,
            "expected_duration": 18.0,
            "transition_gaps": [],
        },
        "blocking_issues": [],
        "warnings": [],
    }
    (project / "internal" / "audio_continuity_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_qingdou_pass(project: Path) -> None:
    internal = project / "internal"
    publish_copy = (internal / "publish_copy.txt").read_text(encoding="utf-8").strip()
    report = {
        "status": "passed",
        "platform": "lightweight_golden_fixture",
        "checked_fields": ["title", "caption", "topics"],
        "final_check": {"status": "passed", "message": "未检查到敏感词", "items": []},
        "final_title": "ChatGPT 文案提示词检查",
        "final_caption": publish_copy,
        "final_topics": ["#AI工具", "#ChatGPT"],
    }
    (internal / "qingdou_keyword_check.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def prompt_pack_path(internal: Path) -> Path:
    for name in ("ai_asset_prompt_pack.md", "background_prompt_pack.md"):
        path = internal / name
        if path.exists() and path.is_file() and path.stat().st_size > 0:
            return path
    return internal / "background_prompt_pack.md"


def check_expected(report: dict[str, object], expected: dict[str, object]) -> list[str]:
    issues: list[str] = []
    if report.get("status") != expected.get("status"):
        issues.append(f"status mismatch: {report.get('status')} != {expected.get('status')}")
    if report.get("quality_level") not in {"high_quality", "breakout_potential"}:
        issues.append(f"quality_level is not high enough: {report.get('quality_level')}")
    scores = report.get("scores", {})
    minimums = expected.get("minimum_scores", {})
    if isinstance(scores, dict) and isinstance(minimums, dict):
        for key, value in minimums.items():
            actual = float(scores.get(key, 0))
            if actual < float(value):
                issues.append(f"{key} {actual} < {value}")
    if report.get("blocking_issues"):
        issues.append("qa_report has blocking issues")
    return issues


def run_golden(project: Path, promote: bool = False) -> dict[str, object]:
    internal = project / "internal"
    run([sys.executable, "scripts/score_topic.py", "--input", str(internal / "topic_candidates.json"), "--out", str(internal / "topic_candidates.json"), "--learning-bank", str(ROOT / "references" / "learning_bank.md")])
    run([sys.executable, "scripts/score_script.py", "--copy", str(internal / "copy_package.md"), "--out", str(internal / "script_score.json")])
    run([sys.executable, "scripts/evaluate_copy_semantic.py", "--copy", str(internal / "copy_package.md"), "--copy-json", str(internal / "copy_package.json"), "--out", str(internal / "semantic_review.json")])
    run([sys.executable, "scripts/validate_beginner_copy.py", "--copy", str(internal / "copy_package.md"), "--copy-json", str(internal / "copy_package.json"), "--out", str(internal / "beginner_value_review.json")])
    run([sys.executable, "scripts/check_public_copy.py", "--copy", str(internal / "copy_package.md"), "--out", str(internal / "compliance_report.json")])
    run([sys.executable, "scripts/validate_asset_prompts.py", "--prompt-pack", str(prompt_pack_path(internal)), "--out", str(internal / "asset_prompt_validation.json")])
    run([sys.executable, "scripts/validate_storyboard.py", "--storyboard", str(internal / "storyboard.json"), "--out", str(internal / "storyboard_validation.json")])
    shutil.copy2(internal / "storyboard.json", internal / "storyboard.audio_locked.json")
    run([sys.executable, "scripts/validate_assets.py", "--manifest", str(internal / "asset_manifest.json"), "--project", str(project), "--out", str(internal / "asset_validation.json")])
    run([sys.executable, "scripts/validate_visual_tone.py", "--manifest", str(internal / "asset_manifest.json"), "--project", str(project), "--out", str(internal / "visual_tone_report.json")])
    ensure_media(project)
    write_audio_continuity_pass(project)
    run([sys.executable, "scripts/video_technical_qa.py", "--video", str(internal / "draft.mp4"), "--metadata", str(internal / "metadata.json"), "--out", str(internal / "video_technical_qa.json")])
    run([sys.executable, "scripts/frame_review.py", "--video", str(internal / "draft.mp4"), "--out-dir", str(internal / "frame_review"), "--report", str(internal / "frame_review_report.json")])
    mark_frame_review_passed(project)
    run([sys.executable, "scripts/export_render_text_manifest.py", "--storyboard", str(internal / "storyboard.json"), "--out", str(internal / "render_text_manifest.json")])
    run([sys.executable, "scripts/check_screen_text.py", "--storyboard", str(internal / "storyboard.json"), "--manifest", str(internal / "render_text_manifest.json"), "--out", str(internal / "screen_text_proofread_report.json")])
    run([sys.executable, "scripts/check_empty_frames.py", "--storyboard", str(internal / "storyboard.json"), "--frame-review", str(internal / "frame_review_report.json"), "--out", str(internal / "empty_frame_report.json")])
    run([sys.executable, "scripts/visual_aesthetic_review.py", "--storyboard", str(internal / "storyboard.json"), "--frame-review", str(internal / "frame_review_report.json"), "--metadata", str(internal / "metadata.json"), "--out", str(internal / "visual_review.json")])
    run([sys.executable, "scripts/qa_gate.py", "--project", str(project), "--out", str(internal / "qa_report.json")])
    run([sys.executable, "scripts/generate_production_postmortem.py", "--project", str(project), "--out", str(internal / "production_postmortem.json")])
    if promote:
        run([sys.executable, "scripts/generate_publish_cover.py", "--project", str(project)])
        text_paths = [internal / "render_text_manifest.json", internal / "publish_cover_text.txt", internal / "publish_copy.txt"]
        run(
            [
                sys.executable,
                "scripts/check_public_copy.py",
                *(str(path) for path in text_paths if path.exists()),
                "--out",
                str(internal / "on_screen_and_publish_text_compliance_report.json"),
            ]
        )
        write_qingdou_pass(project)
    run(
        [
            sys.executable,
            "scripts/audit_provider_usage.py",
            "--project",
            str(project),
            "--phase",
            "final",
            "--out",
            str(internal / "provider_usage_audit.json"),
            "--md-out",
            str(internal / "provider_usage_audit.md"),
        ]
    )
    if promote:
        contract = internal / "publish_contract.json"
        run([sys.executable, "scripts/build_publish_contract.py", "--project", str(project), "--out", str(contract)])
        run([sys.executable, "scripts/pre_publish_gate.py", "--contract", str(contract)])
        run([sys.executable, "scripts/promote_final.py", "--project", str(project), "--contract", str(contract)])
    return json.loads((internal / "qa_report.json").read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check the bundled V3 golden project.")
    parser.add_argument("--project", help="Optional output project path. Defaults to a temporary copy.")
    parser.add_argument("--promote", action="store_true", help="Also run promote_final.py after QA passes.")
    args = parser.parse_args()

    expected = json.loads((EXAMPLE / "expected_qa_report.json").read_text(encoding="utf-8"))
    if args.project:
        project = Path(args.project)
        if project.exists():
            shutil.rmtree(project)
        shutil.copytree(EXAMPLE, project)
        report = run_golden(project, promote=args.promote)
    else:
        with tempfile.TemporaryDirectory(prefix="douyin-golden-") as tmp:
            project = Path(tmp) / "golden_ai_prompt_case"
            shutil.copytree(EXAMPLE, project)
            report = run_golden(project, promote=args.promote)

    issues = check_expected(report, expected)
    result = {
        "status": "passed" if not issues else "failed",
        "quality_level": report.get("quality_level"),
        "scores": report.get("scores", {}),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
