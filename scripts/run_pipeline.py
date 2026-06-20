#!/usr/bin/env python3
"""Run the V3 pipeline checks in order."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def exists(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def prompt_pack_path(internal: Path) -> Path | None:
    for name in ("ai_asset_prompt_pack.md", "background_prompt_pack.md"):
        path = internal / name
        if exists(path):
            return path
    return None


def cover_text_path(internal: Path) -> Path | None:
    report_path = internal / "publish_cover_report.json"
    if exists(report_path):
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            report = {}
        outputs = report.get("outputs") if isinstance(report.get("outputs"), dict) else {}
        path = Path(str(outputs.get("cover_text") or internal / "publish_cover_text.txt"))
        if exists(path):
            return path
    fallback = internal / "publish_cover_text.txt"
    return fallback if exists(fallback) else None


def selected_topic_text(internal: Path) -> str:
    path = internal / "selected_topic.json"
    if not exists(path):
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return path.read_text(encoding="utf-8")
    for key in ("title", "topic", "topic_title", "title_direction"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return json.dumps(data, ensure_ascii=False)


def video_dimensions(internal: Path) -> tuple[int, int]:
    metadata_path = internal / "metadata.json"
    if exists(metadata_path):
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            metadata = {}
        width = int(metadata.get("target_width") or metadata.get("width") or 0)
        height = int(metadata.get("target_height") or metadata.get("height") or 0)
        if width > 0 and height > 0:
            return width, height
    storyboard_path = internal / "storyboard.json"
    if exists(storyboard_path):
        try:
            storyboard = json.loads(storyboard_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            storyboard = {}
        target = storyboard.get("target") if isinstance(storyboard.get("target"), dict) else {}
        fmt = str(target.get("format") or "")
        if "1080x1920" in fmt or "9:16" in fmt:
            return 1080, 1920
    return 1920, 1080


def director_orchestrator(project: Path) -> None:
    internal = project / "internal"
    if not exists(internal / "selected_topic.json"):
        return
    topic = selected_topic_text(internal)
    director = internal / "director_selection.json"
    recipe = internal / "style_recipe.json"
    hooks = internal / "hook_variants.json"
    hook_scores = internal / "hook_score_report.json"
    overfit = internal / "reference_overfit_audit.json"
    if not exists(director) or not exists(recipe):
        cmd = [
            sys.executable,
            "scripts/select_video_style.py",
            "--selected-topic",
            str(internal / "selected_topic.json"),
            "--out",
            str(director),
            "--style-out",
            str(recipe),
        ]
        if exists(internal / "copy_package.json"):
            cmd.extend(["--copy-json", str(internal / "copy_package.json")])
        if exists(internal / "reference_analysis.json"):
            cmd.extend(["--reference-analysis", str(internal / "reference_analysis.json")])
        run(cmd)
    if not exists(hooks):
        run(
            [
                sys.executable,
                "scripts/generate_hook_variants.py",
                "--topic",
                topic,
                "--selected-topic",
                str(internal / "selected_topic.json"),
                "--out",
                str(hooks),
            ]
        )
    if exists(hooks) and not exists(hook_scores):
        run([sys.executable, "scripts/score_hook_variants.py", "--hooks", str(hooks), "--out", str(hook_scores)])
    if exists(director) and not exists(overfit):
        cmd = [
            sys.executable,
            "scripts/audit_reference_overfit.py",
            "--director-selection",
            str(director),
            "--out",
            str(overfit),
        ]
        if exists(recipe):
            cmd.extend(["--style-recipe", str(recipe)])
        run(cmd)
    fixed_templates = internal / "fixed_template_selection.json"
    if exists(director) and exists(recipe) and not exists(fixed_templates):
        width, height = video_dimensions(internal)
        cmd = [
            sys.executable,
            "scripts/select_fixed_ai_templates.py",
            "--project",
            str(project),
            "--director-selection",
            str(director),
            "--style-recipe",
            str(recipe),
            "--video-width",
            str(width),
            "--video-height",
            str(height),
        ]
        if exists(internal / "selected_topic.json"):
            cmd.extend(["--selected-topic", str(internal / "selected_topic.json")])
        run(cmd)


def qa_only(project: Path, promote: bool = False, manual_frame_review_note: str | None = None) -> None:
    internal = project / "internal"
    if exists(internal / "topic_candidates.json"):
        run([sys.executable, "scripts/score_topic.py", "--input", str(internal / "topic_candidates.json"), "--out", str(internal / "topic_candidates.scored.json")])
    director_orchestrator(project)
    if exists(internal / "copy_package.md"):
        copy_json = internal / "copy_package.json"
        run([sys.executable, "scripts/score_script.py", "--copy", str(internal / "copy_package.md"), "--out", str(internal / "script_score.json")])
        semantic_cmd = [sys.executable, "scripts/evaluate_copy_semantic.py", "--copy", str(internal / "copy_package.md"), "--out", str(internal / "semantic_review.json")]
        if exists(copy_json):
            semantic_cmd.extend(["--copy-json", str(copy_json)])
        run(semantic_cmd)
        beginner_cmd = [sys.executable, "scripts/validate_beginner_copy.py", "--copy", str(internal / "copy_package.md"), "--out", str(internal / "beginner_value_review.json")]
        if exists(copy_json):
            beginner_cmd.extend(["--copy-json", str(copy_json)])
        run(beginner_cmd)
        run([sys.executable, "scripts/check_public_copy.py", "--copy", str(internal / "copy_package.md"), "--out", str(internal / "compliance_report.json")])
    prompt_pack = prompt_pack_path(internal)
    if prompt_pack:
        run(
            [
                sys.executable,
                "scripts/validate_asset_prompts.py",
                "--prompt-pack",
                str(prompt_pack),
                "--out",
                str(internal / "asset_prompt_validation.json"),
            ]
        )
    if exists(internal / "storyboard.json"):
        run([sys.executable, "scripts/validate_storyboard.py", "--storyboard", str(internal / "storyboard.json"), "--out", str(internal / "storyboard_validation.json")])
    if exists(internal / "asset_manifest.json"):
        run([sys.executable, "scripts/validate_assets.py", "--manifest", str(internal / "asset_manifest.json"), "--project", str(project), "--out", str(internal / "asset_validation.json")])
        run([sys.executable, "scripts/validate_visual_tone.py", "--manifest", str(internal / "asset_manifest.json"), "--project", str(project), "--out", str(internal / "visual_tone_report.json")])
    if exists(internal / "draft.mp4") and exists(internal / "storyboard.audio_locked.json"):
        run(
            [
                sys.executable,
                "scripts/check_audio_continuity.py",
                "--video",
                str(internal / "draft.mp4"),
                "--lock",
                str(internal / "storyboard.audio_locked.json"),
                "--out",
                str(internal / "audio_continuity_report.json"),
            ]
        )
    if exists(internal / "draft.mp4") and exists(internal / "metadata.json"):
        run([sys.executable, "scripts/video_technical_qa.py", "--video", str(internal / "draft.mp4"), "--metadata", str(internal / "metadata.json"), "--out", str(internal / "video_technical_qa.json")])
        frame_review_cmd = [
            sys.executable,
            "scripts/frame_review.py",
            "--video",
            str(internal / "draft.mp4"),
            "--out-dir",
            str(internal / "frame_review"),
            "--report",
            str(internal / "frame_review_report.json"),
        ]
        if manual_frame_review_note:
            frame_review_cmd.extend(["--manual-pass-note", manual_frame_review_note])
        run(frame_review_cmd)
    if exists(internal / "storyboard.json"):
        run([sys.executable, "scripts/export_render_text_manifest.py", "--storyboard", str(internal / "storyboard.json"), "--out", str(internal / "render_text_manifest.json")])
    if exists(internal / "storyboard.json") and exists(internal / "render_text_manifest.json"):
        run([sys.executable, "scripts/check_screen_text.py", "--storyboard", str(internal / "storyboard.json"), "--manifest", str(internal / "render_text_manifest.json"), "--out", str(internal / "screen_text_proofread_report.json")])
    if exists(internal / "storyboard.json") and exists(internal / "frame_review_report.json"):
        run([sys.executable, "scripts/check_empty_frames.py", "--storyboard", str(internal / "storyboard.json"), "--frame-review", str(internal / "frame_review_report.json"), "--out", str(internal / "empty_frame_report.json")])
    if exists(internal / "storyboard.json") and exists(internal / "frame_review_report.json") and exists(internal / "metadata.json"):
        run([sys.executable, "scripts/visual_aesthetic_review.py", "--storyboard", str(internal / "storyboard.json"), "--frame-review", str(internal / "frame_review_report.json"), "--metadata", str(internal / "metadata.json"), "--out", str(internal / "visual_review.json")])
    run([sys.executable, "scripts/qa_gate.py", "--project", str(project), "--out", str(internal / "qa_report.json")])
    run(
        [
            sys.executable,
            "scripts/generate_production_postmortem.py",
            "--project",
            str(project),
            "--out",
            str(internal / "production_postmortem.json"),
        ]
    )
    if promote:
        cover_report = internal / "publish_cover_report.json"
        if not exists(cover_report):
            raise SystemExit(
                "missing publish_cover_report.json. Run scripts/select_fixed_cover_template.py "
                "before render/promote so the fixed safe cover becomes both first_frame_cover.png "
                "and the publish cover; do not auto-generate the old programmatic cover preview."
            )
        text_paths = []
        if exists(internal / "render_text_manifest.json"):
            text_paths.append(str(internal / "render_text_manifest.json"))
        cover_text = cover_text_path(internal)
        if cover_text:
            text_paths.append(str(cover_text))
        if exists(internal / "publish_copy.txt"):
            text_paths.append(str(internal / "publish_copy.txt"))
        if text_paths:
            run(
                [
                    sys.executable,
                    "scripts/check_public_copy.py",
                    *text_paths,
                    "--out",
                    str(internal / "on_screen_and_publish_text_compliance_report.json"),
                ]
            )
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
        contract = internal / "publish_contract.json"
        run([sys.executable, "scripts/build_publish_contract.py", "--project", str(project), "--out", str(contract)])
        run([sys.executable, "scripts/pre_publish_gate.py", "--contract", str(contract)])
        run([sys.executable, "scripts/promote_final.py", "--project", str(project), "--contract", str(contract)])


def main() -> int:
    parser = argparse.ArgumentParser(description="Run V3 pipeline checks.")
    parser.add_argument("--project", help="outputs/<date-topic> project path")
    parser.add_argument("--mode", choices=["qa-only", "qa-promote", "golden", "full"], default="qa-only")
    parser.add_argument(
        "--manual-frame-review-note",
        help="Optional note confirming first-5s/full/contact-sheet/native frame review; sets frame_review_report.status=passed.",
    )
    args = parser.parse_args()

    if args.mode == "golden":
        run([sys.executable, "scripts/check_golden_project.py"])
        return 0
    if not args.project:
        parser.error("--project is required for qa-only and qa-promote modes")
    if args.mode == "full":
        print("WARNING: --mode full is deprecated; use --mode qa-promote. This runner performs QA + provider audit + promote, not full production from scratch.")
    qa_only(Path(args.project), promote=args.mode in {"qa-promote", "full"}, manual_frame_review_note=args.manual_frame_review_note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
