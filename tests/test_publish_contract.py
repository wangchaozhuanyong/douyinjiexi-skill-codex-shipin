from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from artifact_fingerprint import write_report_with_fingerprints
BUILD_CONTRACT = ROOT / "scripts" / "build_publish_contract.py"
PRE_PUBLISH_GATE = ROOT / "scripts" / "pre_publish_gate.py"
PROMOTE = ROOT / "scripts" / "promote_final.py"


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_fingerprinted_json(path: Path, data: dict, inputs: list[Path]) -> None:
    write_report_with_fingerprints(data, [item for item in inputs if item.exists() and item.is_file() and item.stat().st_size > 0])
    write_json(path, data)


def write_test_video(path: Path, duration: int = 4) -> bool:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        path.write_bytes(b"video")
        return False
    subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"testsrc2=size=1920x1080:rate=30:duration={duration}",
            "-f",
            "lavfi",
            "-i",
            f"sine=frequency=880:duration={duration}",
            "-c:v",
            "libx264",
            "-preset",
            "ultrafast",
            "-b:v",
            "4500k",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-shortest",
            str(path),
        ],
        check=True,
    )
    return True


def write_visual_regression_gate(internal: Path, *, passed: bool = True) -> None:
    report = {
        "status": "passed" if passed else "failed",
        "checks": {
            "no_legacy_renderer_source": passed,
            "hyperframes_source_present": True,
            "first_frame_cover_matches": True,
            "frame1_returns_to_main_timeline": True,
            "visual_review_passed": True,
            "frame_review_passed": True,
        },
        "issues": [] if passed else ["legacy renderer/source terms detected"],
        "legacy_source_hits": []
        if passed
        else [{"file": str(internal / "generate_video.py"), "rule": "legacy_pil_imagedraw_runtime"}],
        "first_frame": {
            "actual_frame_000_cover": str(internal / "actual_frame_000_cover.png"),
            "actual_frame_001_after_cover": str(internal / "actual_frame_001_after_cover.png"),
        },
    }
    write_fingerprinted_json(internal / "visual_regression_gate.json", report, [internal / "draft.mp4", internal / "metadata.json"])


FRAME_REVIEW_CHECKLIST = {
    "first_5s_has_visual_change": True,
    "first_frame_is_cover_quality": True,
    "captions_readable_on_phone": True,
    "proof_panel_readable": True,
    "no_text_overlap": True,
    "no_generic_background": True,
    "motion_not_random": True,
    "no_freeze_or_black_frames": True,
    "cover_ok": True,
}


def write_workflow_guard_scaffold(project: Path, internal: Path) -> None:
    background = project / "assets" / "backgrounds" / "dynamic-bg.mp4"
    background.parent.mkdir(parents=True, exist_ok=True)
    background.write_bytes(b"dynamic background")
    write_json(internal / "topic_candidates.json", {"status": "passed", "items": [{"topic_id": "T001"}]})
    write_json(internal / "selected_topic.json", {"topic_id": "T001", "title": "测试 AI 工具更新"})
    write_json(
        internal / "director_selection.json",
        {
            "status": "passed",
            "content_job_lock": "teach one AI workflow with source proof",
            "scheme": {"id": "scheme_2_source_led_tool_tutorial", "name": "source-led tutorial", "format": "1920x1080"},
        },
    )
    write_json(
        internal / "style_recipe.json",
        {
            "status": "passed",
            "selected_visual_family": "enterprise_console",
            "background_style_id": "dynamic-bg",
        },
    )
    write_json(internal / "hook_variants.json", {"status": "passed", "variants": [{"hook_id": f"H{i:02d}"} for i in range(1, 11)]})
    write_json(internal / "hook_score_report.json", {"status": "passed", "selected_hook": {"hook_id": "H01", "line": "测试 hook"}})
    write_json(internal / "reference_overfit_audit.json", {"status": "passed", "blocking_issues": []})
    write_json(
        internal / "fixed_template_selection.json",
        {
            "status": "passed",
            "background_template": {
                "id": "BG_TEST",
                "render_asset_path": str(background),
                "dynamic_asset_path": str(background),
                "render_asset_is_dynamic": True,
            },
            "inheritance_contract": {
                "background_drives_foreground": True,
                "dynamic_background_default": True,
                "static_background_fallback_removed": True,
                "transition_pack_drives_sfx": True,
                "component_pack_drives_storyboard_shapes": True,
                "voice_profile_drives_tts_and_mix": True,
            },
        },
    )
    (internal / "copy_package.md").write_text("# Copy Package\n安全文案\n", encoding="utf-8")
    write_json(internal / "copy_package.json", {"title_options": ["测试标题"], "cover_text": ["测试标题", "发布级 AI 知识视频"]})
    write_json(internal / "script_score.json", {"status": "passed", "script_score": 8.8})
    write_json(internal / "semantic_review.json", {"status": "passed", "composite_score": 8.8})
    write_json(internal / "content_alignment_report.json", {"status": "passed", "blocking_issues": []})
    write_json(internal / "beginner_value_review.json", {"status": "passed", "final_decision": "pass"})
    write_json(internal / "compliance_report.json", {"status": "passed", "risk_items": []})
    write_json(
        internal / "visual_style_decision.json",
        {
            "status": "locked",
            "style_intent": "source proof tutorial",
            "selected_brightness_grade": "L2 dark with bright proof surfaces",
            "selected_palette_family": "graphite_teal",
            "selected_material_family": "glass_metal",
            "selected_layout_family": "source_wall_grid",
            "why_this_style": "Source proof needs contrast and a controlled evidence wall.",
            "why_not_other_styles": "Poster and generic bright styles weaken proof density.",
        },
    )
    write_json(
        internal / "visual_style_plan.json",
        {
            "status": "locked",
            "foreground_ui_system": "enterprise console panels",
            "caption_system": "safe lower-third captions",
        },
    )
    (internal / "background_prompt_pack.md").write_text(
        "# Background Prompt Pack\n\nVisual thesis: source proof console.\nTopic binding: AI workflow proof.\nInformation job: hold source and result modules.\nBackground role: atmosphere stage.\n",
        encoding="utf-8",
    )
    write_json(internal / "storyboard_validation.json", {"status": "passed", "issues": []})
    write_json(internal / "asset_validation.json", {"status": "passed", "blocking_issues": []})
    write_json(internal / "storyboard.audio_locked.json", {"scenes": [{"scene_id": "S01", "duration_target": 4, "beat_map": [{"t": 0}]}]})


def create_publish_ready_project(tmp_path: Path, qingdou: dict | None = None, frame_grab_used: bool = False) -> tuple[Path, Path]:
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    write_test_video(internal / "draft.mp4")
    (internal / "cover.png").write_bytes(b"cover")
    (internal / "first_frame_cover.png").write_bytes(b"first-frame-cover")
    (internal / "actual_frame_000_cover.png").write_bytes(b"actual-frame-0")
    (internal / "actual_frame_001_after_cover.png").write_bytes(b"actual-frame-1")
    fixed_asset = internal / "fixed-cover-template.jpg"
    fixed_asset.write_bytes(b"fixed-cover")
    (internal / "cover_publish_vertical.png").write_bytes(b"vertical")
    (internal / "cover_publish_horizontal.png").write_bytes(b"horizontal")
    (internal / "cover_publish_douyin_center_crop.png").write_bytes(b"douyin-center")
    (internal / "publish_cover_text.txt").write_text("测试标题\n发布级 AI 知识视频\n", encoding="utf-8")
    metadata = {
        "task_id": "demo",
        "title": "测试标题",
        "duration": 4,
        "target_width": 1920,
        "target_height": 1080,
        "fps": 30,
        "quality_spec": {
            "provider_policy": "free_first_local_or_authorized_openai_only",
            "runtime_choice": "HyperFrames final timeline; FFmpeg only for mechanical media",
        },
    }
    write_json(internal / "metadata.json", metadata)
    (internal / "publish_copy.txt").write_text("发布文案\n", encoding="utf-8")
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    write_json(internal / "storyboard.json", storyboard)
    write_workflow_guard_scaffold(project, internal)
    write_json(
        internal / "asset_manifest.json",
        {"assets": [{"asset_id": "HF001", "provider": "hyperframes", "asset_source_type": "local_render"}]},
    )
    write_json(internal / "asset_validation.json", {"status": "passed", "blocking_issues": []})
    write_fingerprinted_json(
        internal / "video_technical_qa.json",
        {"status": "passed", "audio": {"has_audio": True}, "blocking_issues": []},
        [internal / "draft.mp4", internal / "metadata.json"],
    )
    frame_review_dir = internal / "frame_review"
    crowded_dir = frame_review_dir / "crowded_frames"
    crowded_dir.mkdir(parents=True)
    (frame_review_dir / "first_5s_contact_sheet.jpg").write_bytes(b"first-five")
    (frame_review_dir / "full_video_contact_sheet.jpg").write_bytes(b"full-video")
    (crowded_dir / "sample_001.jpg").write_bytes(b"crowded")
    write_fingerprinted_json(
        internal / "frame_review_report.json",
        {
            "status": "passed",
            "audio": {"has_audio": True},
            "blocking_issues": [],
            "artifacts": {
                "first_5s_contact_sheet": str(frame_review_dir / "first_5s_contact_sheet.jpg"),
                "full_video_contact_sheet": str(frame_review_dir / "full_video_contact_sheet.jpg"),
                "crowded_frames_dir": str(crowded_dir),
            },
            "manual_review": {
                "status": "passed",
                "reviewer": "test_reviewer",
                "timestamp": "2026-06-28T00:00:00Z",
                "checklist": FRAME_REVIEW_CHECKLIST,
            },
        },
        [internal / "draft.mp4"],
    )
    write_fingerprinted_json(
        internal / "visual_review.json",
        {
            "status": "passed",
            "overall_visual_score": 8.8,
            "scores": {
                "first_5s_score": 9.0,
                "readability_score": 8.8,
                "composition_score": 8.7,
                "layering_score": 9.0,
                "quality_check_score": 9.0,
                "sound_design_score": 8.8,
                "export_readiness_score": 8.8,
            },
            "blocking_issues": [],
        },
        [internal / "storyboard.json", internal / "frame_review_report.json", internal / "metadata.json", internal / "draft.mp4"],
    )
    (internal / "foreground_module_plan.json").write_text(
        (ROOT / "templates" / "foreground_module_plan.example.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    write_json(
        internal / "foreground_module_plan_check.json",
        {"status": "passed", "blocking_issues": [], "warnings": [], "signals": {"scene_count": 1}},
    )
    (internal / "foreground_module_render_pack.html").write_text(
        '<section class="hf-foreground-stage"><article class="hf-module" data-scene-id="S03" data-module-id="M01"><div class="hf-micro" data-component-id="C01"></div><div class="hf-micro" data-component-id="C03"></div></article></section>\n',
        encoding="utf-8",
    )
    write_json(
        internal / "foreground_module_render_manifest.json",
        {
            "status": "rendered",
            "html": str(internal / "foreground_module_render_pack.html"),
            "module_dom_count": 1,
            "micro_dom_count": 5,
            "render_contract": {
                "html_css_svg_gsap_ready": True,
                "real_3d_dependency": False,
                "standalone_micro_components": False,
                "parent_module_primary": True,
            },
        },
    )
    write_json(
        internal / "foreground_module_render_check.json",
        {"status": "passed", "blocking_issues": [], "warnings": [], "signals": {"module_dom_count": 1, "micro_dom_count": 5}},
    )
    write_fingerprinted_json(
        internal / "qa_report.json",
        {
            "status": "passed",
            "quality_level": "high_quality",
            "blocking_issues": [],
            "hard_gates": {
                "qa": True,
                "foreground_module_plan_exists": True,
                "foreground_module_plan_check_exists": True,
                "foreground_module_plan_check_passed": True,
                "foreground_module_render_manifest_exists": True,
                "foreground_module_render_check_exists": True,
                "foreground_module_render_check_passed": True,
            },
        },
        [internal / "draft.mp4", internal / "metadata.json"],
    )
    write_fingerprinted_json(
        internal / "provider_usage_audit.json",
        {"status": "passed", "issues": []},
        [internal / "draft.mp4", internal / "metadata.json"],
    )
    write_visual_regression_gate(internal)
    write_json(
        internal / "on_screen_and_publish_text_compliance_report.json",
        {
            "status": "passed",
            "checked_files": [str(internal / "publish_cover_text.txt"), str(internal / "publish_copy.txt")],
            "risk_items": [],
            "summary": {"error_count": 0, "warning_count": 0},
        },
    )
    write_json(
        internal / "publish_cover_report.json",
        {
            "status": "passed",
            "cover_type": "fixed_pure_background_runtime_text_first_frame",
            "frame_grab_used": frame_grab_used,
            "template_id": "T01",
            "canonical_id": "T01_16x9",
            "template_path": str(fixed_asset),
            "template_aspect": "16:9",
            "background_contains_text": False,
            "recommended_text_safe_rect_px": [690, 150, 1230, 820],
            "cover_layout": {
                "text_bbox_px": [720, 180, 1110, 360],
                "recommended_text_safe_rect_px": [690, 150, 1230, 820],
                "douyin_center_crop_rect_px": [656, 0, 1264, 1080],
                "text_bbox_inside_safe_rect": True,
                "text_bbox_inside_douyin_center_crop": True,
                "compact_cover_text_used": True,
            },
            "accent_rgb": [66, 211, 255],
            "template_rotation_index": 0,
            "selection_method": "sequential_by_size_pool",
            "template_library_size": 10,
            "outputs": {
                "primary": str(internal / "cover.png"),
                "vertical_3_4": str(internal / "cover_publish_vertical.png"),
                "horizontal_4_3": str(internal / "cover_publish_horizontal.png"),
                "douyin_center_crop_preview": str(internal / "cover_publish_douyin_center_crop.png"),
                "cover_text": str(internal / "publish_cover_text.txt"),
            },
            "checks": {
                "cover_text_written": True,
                "not_video_screenshot": not frame_grab_used,
                "template_from_fixed_library": True,
                "fixed_safe_asset": True,
                "fixed_pure_background_asset": True,
                "background_contains_text_false": True,
                "selected_by_video_size": True,
                "first_frame_required": True,
                "dynamic_text_overlay_used": True,
                "uses_old_cover_template_asset": False,
                "cover_text_fit_safe_rect": True,
                "primary_text_inside_douyin_center_crop": True,
                "douyin_center_crop_preview_generated": True,
                "compact_cover_text_used": True,
            },
        },
    )
    if qingdou is None:
        qingdou = {
            "status": "passed",
            "platform": "轻抖",
            "checked_fields": ["title", "caption", "topics"],
            "final_check": {"status": "passed", "message": "未检查到敏感词", "items": []},
            "final_title": "测试标题",
            "final_caption": "发布文案",
            "final_topics": ["#AI工具"],
        }
    write_json(internal / "qingdou_keyword_check.json", qingdou)
    return project, internal


def build_and_gate(project: Path, internal: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
    contract = internal / "publish_contract.json"
    built = subprocess.run(
        [sys.executable, str(BUILD_CONTRACT), "--project", str(project), "--out", str(contract)],
        text=True,
        capture_output=True,
    )
    assert built.returncode == 0
    result = subprocess.run(
        [sys.executable, str(PRE_PUBLISH_GATE), "--contract", str(contract)],
        text=True,
        capture_output=True,
    )
    return result, json.loads(contract.read_text(encoding="utf-8"))


def test_publish_contract_promotes_only_after_gate_passed(tmp_path):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        pytest.skip("ffmpeg/ffprobe are required for promotion media probe")
    project, internal = create_publish_ready_project(tmp_path)
    (project / "assets" / "frames").mkdir(parents=True)
    (project / "assets" / "frames" / "frame_000001.png").write_bytes(b"frame")
    (internal / "hf_frames").mkdir(parents=True)
    (internal / "hf_frames" / "frame_000001.png").write_bytes(b"frame")
    (internal / "silent_hf.mp4").write_bytes(b"silent")
    (internal / "draft_no_cover.mp4").write_bytes(b"draft2")
    (project / "final").mkdir(parents=True)
    (project / "final" / "old-preview.mp4").write_bytes(b"old")
    gate, contract = build_and_gate(project, internal)

    assert gate.returncode == 0
    assert contract["gate"]["status"] == "passed"
    original_video = (internal / "draft.mp4").read_bytes()

    promoted = subprocess.run(
        [sys.executable, str(PROMOTE), "--project", str(project), "--contract", str(internal / "publish_contract.json")],
        text=True,
        capture_output=True,
    )

    assert promoted.returncode == 0
    assert (project / "final" / "final.mp4").read_bytes() == original_video
    assert sorted(path.name for path in (project / "final").iterdir()) == [
        "artifact_manifest.json",
        "final.mp4",
        "promotion_report.json",
    ]
    assert not (internal / "draft.mp4").exists()
    assert not (internal / "draft_no_cover.mp4").exists()
    assert not (internal / "silent_hf.mp4").exists()
    assert not (internal / "hf_frames").exists()
    assert not (project / "assets" / "frames").exists()
    cleanup = json.loads((internal / "cleanup_report.json").read_text(encoding="utf-8"))
    assert cleanup["cleanup_status"] == "final_folder_mp4_with_manifests"
    assert cleanup["removed_count"] >= 5


def test_pre_publish_gate_accepts_labeled_publish_copy_package(tmp_path):
    project, internal = create_publish_ready_project(tmp_path)
    (internal / "publish_copy.txt").write_text(
        "标题：测试标题\n\n发布文案：发布文案\n\n话题：#AI工具\n",
        encoding="utf-8",
    )
    gate, contract = build_and_gate(project, internal)

    assert gate.returncode == 0
    assert contract["gate"]["status"] == "passed"


def test_pre_publish_gate_rejects_frame_grab_cover(tmp_path):
    project, internal = create_publish_ready_project(tmp_path, frame_grab_used=True)
    gate, contract = build_and_gate(project, internal)

    assert gate.returncode == 1
    assert contract["gate"]["status"] == "failed"
    assert "publish_cover_report.frame_grab_used must be false" in contract["gate"]["issues"]


def test_pre_publish_gate_rejects_cover_text_outside_douyin_center_crop(tmp_path):
    project, internal = create_publish_ready_project(tmp_path)
    report_path = internal / "publish_cover_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["cover_layout"]["text_bbox_inside_douyin_center_crop"] = False
    report["checks"]["primary_text_inside_douyin_center_crop"] = False
    write_json(report_path, report)
    gate, contract = build_and_gate(project, internal)

    assert gate.returncode == 1
    assert contract["gate"]["status"] == "failed"
    assert "publish_cover_report.checks.primary_text_inside_douyin_center_crop must be true" in contract["gate"]["issues"]


def test_pre_publish_gate_rejects_legacy_visual_regression_gate(tmp_path):
    project, internal = create_publish_ready_project(tmp_path)
    write_visual_regression_gate(internal, passed=False)
    gate, contract = build_and_gate(project, internal)

    assert gate.returncode == 1
    assert contract["gate"]["status"] == "failed"
    assert "visual_regression_gate.legacy_source_hits must be empty" in contract["gate"]["issues"]


def test_pre_publish_gate_allows_only_user_required_platform_topic_override(tmp_path):
    qingdou = {
        "status": "user_override_accepted",
        "platform": "轻抖",
        "checked_fields": ["title", "caption", "topics"],
        "final_check": {
            "status": "failed",
            "message": "命中用户要求保留的话题",
            "items": [{"term": "#我在抖音聊科技"}],
            "user_override": {
                "accepted": True,
                "allowed_by_skill_rule": True,
                "scope": "required_official_platform_topic",
                "approved_by_user": True,
            },
        },
        "final_title": "测试标题",
        "final_caption": "发布文案",
        "final_topics": ["#我在抖音聊科技", "#AI工具"],
    }
    project, internal = create_publish_ready_project(tmp_path, qingdou=qingdou)
    gate, contract = build_and_gate(project, internal)

    assert gate.returncode == 0
    assert contract["publish"]["first_topic"] == "#我在抖音聊科技"
    assert contract["gate"]["status"] == "passed"
