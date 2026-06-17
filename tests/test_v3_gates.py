import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_semantic_review_passes_golden_copy(tmp_path):
    out = tmp_path / "semantic_review.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "evaluate_copy_semantic.py"),
            "--copy",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "copy_package.md"),
            "--copy-json",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "copy_package.json"),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["composite_score"] >= 8.5


def test_visual_review_passes_golden_storyboard(tmp_path):
    frame_review = tmp_path / "frame_review_report.json"
    metadata = tmp_path / "metadata.json"
    out = tmp_path / "visual_review.json"
    frame_review.write_text('{"status":"passed","artifacts":{},"blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    metadata.write_text((ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "metadata.json").read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "visual_aesthetic_review.py"),
            "--storyboard",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "storyboard.json"),
            "--frame-review",
            str(frame_review),
            "--metadata",
            str(metadata),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["overall_visual_score"] >= 8.2


def test_visual_review_ignores_evidence_embedded_text_for_readability(tmp_path):
    storyboard = json.loads((ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "storyboard.json").read_text(encoding="utf-8"))
    storyboard["scenes"][0]["on_screen_text"] = [
        "Selected model is at capacity. Please try a different model. June 16th, 2026",
        "别一直点重试",
    ]
    storyboard["scenes"][0]["text_layers"] = {
        "primary_read_text": ["别一直点重试"],
        "evidence_embedded_text": ["Selected model is at capacity. Please try a different model. June 16th, 2026"],
    }
    storyboard_path = tmp_path / "storyboard.json"
    frame_review = tmp_path / "frame_review_report.json"
    metadata = tmp_path / "metadata.json"
    out = tmp_path / "visual_review.json"
    storyboard_path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    frame_review.write_text('{"status":"passed","artifacts":{},"blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    metadata.write_text((ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "metadata.json").read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "visual_aesthetic_review.py"),
            "--storyboard",
            str(storyboard_path),
            "--frame-review",
            str(frame_review),
            "--metadata",
            str(metadata),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["signals"]["dense_text_scenes"] == 0
    assert data["scores"]["readability_score"] == 9.0


def test_visual_review_rejects_preview_voice_no_sfx_and_card_pipeline(tmp_path):
    frame_review = tmp_path / "frame_review_report.json"
    metadata = tmp_path / "metadata.json"
    out = tmp_path / "visual_review.json"
    frame_review.write_text('{"status":"passed","artifacts":{},"blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    metadata_data = json.loads((ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "metadata.json").read_text(encoding="utf-8"))
    metadata_data["voice"] = {"provider": "macOS say", "voice_id": "Tingting", "sample_approved": False}
    metadata_data["quality_spec"]["sfx_policy"] = "no added SFX; voice-first proof tutorial mix"
    metadata_data["quality_spec"]["runtime_choice"] = "ffmpeg portrait card pipeline"
    metadata.write_text(json.dumps(metadata_data, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "visual_aesthetic_review.py"),
            "--storyboard",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "storyboard.json"),
            "--frame-review",
            str(frame_review),
            "--metadata",
            str(metadata),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert data["signals"]["voice_provider_approved"] is False
    assert data["signals"]["sfx_policy_valid"] is False
    assert data["signals"]["runtime_choice_valid"] is False
    assert any("macOS say" in issue for issue in data["blocking_issues"])
    assert any("no-added-SFX" in issue for issue in data["blocking_issues"])
    assert any("FFmpeg-only portrait card" in issue for issue in data["blocking_issues"])


def test_visual_review_rejects_unapproved_frame_review(tmp_path):
    frame_review = tmp_path / "frame_review_report.json"
    metadata = tmp_path / "metadata.json"
    out = tmp_path / "visual_review.json"
    frame_review.write_text(
        '{"status":"review_required","artifacts":{},"manual_review":{"status":"passed"},"blocking_issues":[],"warnings":[]}\n',
        encoding="utf-8",
    )
    metadata.write_text((ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "metadata.json").read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "visual_aesthetic_review.py"),
            "--storyboard",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "storyboard.json"),
            "--frame-review",
            str(frame_review),
            "--metadata",
            str(metadata),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert any("frame_review_report.json must be status=passed" in issue for issue in data["blocking_issues"])


def test_storyboard_validation_rejects_fast_voice_and_unsafe_margins(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard["target"]["tts_speed"] = 1.12
    storyboard["scenes"][0]["safe_zone"]["bottom_margin_px"] = 120
    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert any("tts_speed" in issue for issue in data["issues"])
    assert any("bottom_margin_px" in issue for issue in data["issues"])


def test_storyboard_validation_rejects_missing_quality_design(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard.pop("quality_spec", None)
    storyboard["scenes"][0]["visual"].pop("design_layers", None)
    storyboard["scenes"][0]["visual"]["quality_checks"]["not_template_like"] = False
    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert data["signals"]["quality_spec_valid"] is False
    assert data["signals"]["layered_scene_count"] == 5
    assert data["signals"]["quality_check_scene_count"] == 5
    assert any("quality_spec" in issue for issue in data["issues"])
    assert any("design_layers" in issue for issue in data["issues"])
    assert any("quality_checks" in issue for issue in data["issues"])


def test_storyboard_validation_requires_free_first_source_and_caption_controls(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard["target"].pop("provider_policy", None)
    storyboard["quality_spec"]["runtime_choice"] = "Use Runway for generated video clips"
    storyboard["scenes"][0]["visual"].pop("asset_source_type", None)
    storyboard["scenes"][1]["visual"].pop("caption_template", None)
    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert data["signals"]["provider_policy_valid"] is False
    assert data["signals"]["source_class_scene_count"] == 5
    assert data["signals"]["caption_template_scene_count"] == 5
    assert any("provider_policy" in issue for issue in data["issues"])
    assert any("disabled paid provider" in issue for issue in data["issues"])
    assert any("asset_source_type" in issue for issue in data["issues"])
    assert any("caption_template" in issue for issue in data["issues"])


def test_storyboard_validation_passes_premium_motion_craft(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["signals"]["premium_motion_scene_count"] == len(storyboard["scenes"])
    assert data["signals"]["audio_continuity_scene_count"] == len(storyboard["scenes"])
    assert data["signals"]["director_shots_valid"] is True
    assert data["signals"]["director_shot_type_count"] >= 4
    assert data["signals"]["director_operation_shot_count"] >= 2


def test_storyboard_validation_rejects_repeated_director_layout(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    for shot in storyboard["director_shots"]:
        shot["layout_family"] = "workspace_ui"
    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert data["signals"]["director_shots_valid"] is False
    assert data["signals"]["director_layout_max_consecutive"] > 2
    assert any("repeats layout_family" in issue for issue in data["issues"])


def test_storyboard_validation_rejects_unapproved_director_text(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard["director_shots"][0]["on_screen_text"]["primary"] = "错误：太空"
    storyboard["director_shots"][0]["on_screen_text"]["approved_primary_text"] = ["空话输出"]
    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert data["signals"]["director_shots_valid"] is False
    assert any("primary text not present" in issue for issue in data["issues"])


def test_storyboard_validation_rejects_stale_director_timing_after_tts_lock(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard["director_shots"][0]["duration_sec"] = storyboard["scenes"][0]["duration_target"] + 1.0
    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert data["signals"]["director_timing_aligned"] is False
    assert data["signals"]["duration_mismatch_count"] >= 1
    assert any("duration_sec" in issue and "duration_target" in issue for issue in data["issues"])


def test_screen_text_gate_exports_and_rejects_unapproved_title(tmp_path):
    storyboard_path = ROOT / "templates" / "storyboard.example.json"
    manifest = tmp_path / "render_text_manifest.json"
    report = tmp_path / "screen_text_proofread_report.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "export_render_text_manifest.py"),
            "--storyboard",
            str(storyboard_path),
            "--out",
            str(manifest),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["texts"]

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "check_screen_text.py"),
            "--storyboard",
            str(storyboard_path),
            "--manifest",
            str(manifest),
            "--out",
            str(report),
        ],
        text=True,
        capture_output=True,
    )
    passed = json.loads(report.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert passed["status"] == "passed"

    manifest_data = json.loads(manifest.read_text(encoding="utf-8"))
    manifest_data["texts"][0]["text"] = "错误：太空"
    manifest.write_text(json.dumps(manifest_data, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "check_screen_text.py"),
            "--storyboard",
            str(storyboard_path),
            "--manifest",
            str(manifest),
            "--out",
            str(report),
        ],
        text=True,
        capture_output=True,
    )
    failed = json.loads(report.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert failed["status"] == "failed"
    assert any("错误：太空" in issue for issue in failed["blocking_issues"])


def test_empty_frame_gate_rejects_long_empty_candidate(tmp_path):
    storyboard_path = ROOT / "templates" / "storyboard.example.json"
    frame_review = tmp_path / "frame_review_report.json"
    out = tmp_path / "empty_frame_report.json"
    frame_review.write_text(
        json.dumps(
            {
                "status": "passed",
                "empty_frame_candidates": [
                    {"start_sec": 12.2, "duration_sec": 1.1, "intentional": False}
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "check_empty_frames.py"),
            "--storyboard",
            str(storyboard_path),
            "--frame-review",
            str(frame_review),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert any("empty visual span" in issue for issue in data["blocking_issues"])


def test_production_postmortem_generates_learning_decisions(tmp_path):
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    (internal / "storyboard.json").write_text((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"), encoding="utf-8")
    (internal / "selected_topic.json").write_text('{"title":"Codex 工作流教程"}\n', encoding="utf-8")
    (internal / "qa_report.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "scores": {
                    "first_5_seconds_score": 9.2,
                    "proof_score": 8.6,
                    "visual_score": 8.8,
                },
                "evidence_runtime_ratio": 0.72,
                "blocking_issues": [],
                "warnings": [],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (internal / "visual_review.json").write_text(
        '{"status":"passed","overall_visual_score":8.8,"signals":{"caption_template_count":3},"blocking_issues":[],"warnings":[]}\n',
        encoding="utf-8",
    )
    (internal / "frame_review_report.json").write_text('{"status":"passed","warnings":[]}\n', encoding="utf-8")
    (internal / "storyboard_validation.json").write_text(
        '{"status":"passed","evidence_runtime_ratio":0.72,"signals":{"director_shots_valid":true},"warnings":[]}\n',
        encoding="utf-8",
    )
    (internal / "screen_text_proofread_report.json").write_text('{"status":"passed","blocking_issues":[]}\n', encoding="utf-8")
    (internal / "empty_frame_report.json").write_text('{"status":"passed","blocking_issues":[]}\n', encoding="utf-8")
    out = internal / "production_postmortem.json"

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "generate_production_postmortem.py"),
            "--project",
            str(project),
            "--out",
            str(out),
            "--user-feedback",
            "操作感比上一版更强",
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["qa_status"] == "passed"
    assert data["human_approval_required"] is True
    assert any("Director shots passed" in item for item in data["what_worked"])
    assert any("skill as execution memory" in item for item in data["reusable_lessons"])


def test_learning_bank_accepts_production_postmortem(tmp_path):
    postmortem = tmp_path / "production_postmortem.json"
    bank = tmp_path / "learning_bank.md"
    postmortem.write_text(
        json.dumps(
            {
                "project": "outputs/demo",
                "topic": "Codex 工作流教程",
                "qa_status": "passed",
                "decision_summary": "use as soft learning",
                "observations": ["user_feedback=PPT感下降"],
                "what_worked": ["真实操作镜头有效"],
                "what_to_fix": ["减少同款卡片"],
                "bottlenecks": [],
                "reusable_lessons": ["先做导演脚本"],
                "next_run_decisions": ["增加 source_evidence"],
                "proposed_rule_changes": ["重复出现再升级"],
                "human_approval_required": True,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "update_learning_bank.py"),
            "--review",
            str(postmortem),
            "--bank",
            str(bank),
        ],
        text=True,
        capture_output=True,
    )
    text = bank.read_text(encoding="utf-8")
    assert result.returncode == 0
    assert "production-postmortem" in text
    assert "Next run decisions" in text
    assert "Human approval required: True" in text


def test_storyboard_validation_rejects_transition_audio_gap(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard["scenes"][1]["sync"]["max_audio_gap_ms"] = 350
    storyboard["scenes"][1]["sync"]["transition_audio_policy"] = "scene transition may restart audio"
    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert data["signals"]["audio_continuity_scene_count"] == len(storyboard["scenes"]) - 1
    assert any("max_audio_gap_ms" in issue for issue in data["issues"])
    assert any("visual-only transitions" in issue for issue in data["issues"])


def test_storyboard_validation_rejects_vague_motion_language(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard["scenes"][0]["motion"] = {
        "background_motion": "高级、炫酷、震撼",
        "foreground_motion": "高级、炫酷、震撼",
        "callout_motion": "高级、炫酷、震撼",
        "transition": "高级、炫酷、震撼",
        "purpose": "高级、炫酷、震撼",
        "entrance": "高级、炫酷、震撼",
        "stagger": "高级、炫酷、震撼",
        "keyword_motion": "高级、炫酷、震撼",
        "camera_motion": "高级、炫酷、震撼",
        "layering": "高级、炫酷、震撼",
        "caption_motion": "高级、炫酷、震撼",
        "glow": "高级、炫酷、震撼",
        "audio_reactive": "高级、炫酷、震撼",
        "negative_motion": "高级、炫酷、震撼",
    }
    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert data["signals"]["premium_motion_scene_count"] == len(storyboard["scenes"]) - 1
    assert any("vague/cheap motion language" in issue for issue in data["issues"])


def test_asset_validation_rejects_paid_provider_and_fake_generated_proof(tmp_path):
    asset_file = tmp_path / "generated.png"
    asset_file.write_bytes(b"placeholder")
    manifest = {
        "assets": [
            {
                "asset_id": "A001",
                "type": "generated_visual",
                "path": str(asset_file),
                "source": "Runway generated output",
                "provider": "Runway",
                "asset_source_type": "proof",
                "source_note": "fake official proof",
                "copyright_status": "self_created",
                "resolution": "1920x1080",
                "used_in_scenes": ["S01"],
                "is_evidence": True,
                "risk": "low",
                "contains_private_info": False,
                "contains_contact_info": False,
                "contains_qr_code": False,
                "qa_notes": "",
            }
        ]
    }
    manifest_path = tmp_path / "asset_manifest.json"
    out = tmp_path / "asset_validation.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_assets.py"),
            "--manifest",
            str(manifest_path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert any("disabled paid" in issue for issue in data["blocking_issues"])
    assert any("generated visual" in issue.lower() for issue in data["blocking_issues"])


def test_asset_validation_rejects_local_summary_card_as_proof(tmp_path):
    asset_file = tmp_path / "source-card.png"
    asset_file.write_bytes(b"placeholder")
    manifest = {
        "assets": [
            {
                "asset_id": "A001",
                "type": "code_or_file_proof",
                "path": str(asset_file),
                "source": "TechCrunch source summary",
                "provider": "official_source_card_local_render",
                "asset_source_type": "proof",
                "source_note": "Local original card summarizing official sources; not an official screenshot.",
                "copyright_status": "self_created",
                "resolution": "1920x1080",
                "used_in_scenes": ["S01"],
                "is_evidence": True,
                "risk": "low",
                "contains_private_info": False,
                "contains_contact_info": False,
                "contains_qr_code": False,
                "qa_notes": "",
            }
        ]
    }
    manifest_path = tmp_path / "asset_manifest.json"
    out = tmp_path / "asset_validation.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_assets.py"),
            "--manifest",
            str(manifest_path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert any("local summary/designed cards" in issue for issue in data["blocking_issues"])


def test_asset_validation_requires_background_prompt_pack_and_plate(tmp_path):
    proof_file = tmp_path / "proof.png"
    background_file = tmp_path / "background.png"
    proof_file.write_bytes(b"proof")
    background_file.write_bytes(b"background")
    manifest = {
        "assets": [
            {
                "asset_id": "A001",
                "type": "real_ui_screenshot",
                "path": str(proof_file),
                "source": "self captured proof",
                "provider": "local_screen_capture",
                "asset_source_type": "proof",
                "source_note": "real local UI proof",
                "copyright_status": "self_captured",
                "resolution": "1920x1080",
                "used_in_scenes": ["S01"],
                "is_evidence": True,
                "risk": "low",
                "contains_private_info": False,
                "contains_contact_info": False,
                "contains_qr_code": False,
                "qa_notes": "real proof",
            }
        ]
    }
    manifest_path = tmp_path / "asset_manifest.json"
    out = tmp_path / "asset_validation.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_assets.py"),
            "--manifest",
            str(manifest_path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert any("background_prompt_pack.md" in issue for issue in data["blocking_issues"])
    assert any("background_plate" in issue for issue in data["blocking_issues"])

    (tmp_path / "background_prompt_pack.md").write_text(
        "# Background Prompt Pack\n\nAsset role: background_plate\nFormat: 16:9 1920x1080\nAvoid: text, fake UI, pseudo-code.\n",
        encoding="utf-8",
    )
    manifest["assets"].append(
        {
            "asset_id": "BG001",
            "type": "generated_visual",
            "asset_role": "background_plate",
            "path": str(background_file),
            "source": "ImageGen generated text-free background plate",
            "provider": "codex_builtin_imagegen",
            "model": "gpt-image-2",
            "prompt_id": "BG001",
            "prompt_path": "background_prompt_pack.md#BG001",
            "unique_prompt": True,
            "evidence_boundary": "support only; not evidence and not official UI",
            "asset_source_type": "generated",
            "source_note": "Support background only; not official UI and not factual proof.",
            "copyright_status": "self_created",
            "resolution": "1920x1080",
            "used_in_scenes": ["S01"],
            "is_evidence": False,
            "risk": "low",
            "contains_private_info": False,
            "contains_contact_info": False,
            "contains_qr_code": False,
            "qa_notes": "support visual, not evidence",
        }
    )
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_assets.py"),
            "--manifest",
            str(manifest_path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["background_plate_valid_count"] == 1
    assert data["generated_visual_prompt_count"] == 1


def test_asset_validation_rejects_local_pil_as_generated_image_provider(tmp_path):
    proof_file = tmp_path / "proof.png"
    background_file = tmp_path / "background.png"
    proof_file.write_bytes(b"proof")
    background_file.write_bytes(b"background")
    (tmp_path / "background_prompt_pack.md").write_text(
        "# Background Prompt Pack\n\nAsset role: background_plate\nFormat: 16:9 1920x1080\n",
        encoding="utf-8",
    )
    manifest = {
        "assets": [
            {
                "asset_id": "A001",
                "type": "real_ui_screenshot",
                "path": str(proof_file),
                "source": "self captured proof",
                "provider": "local_screen_capture",
                "asset_source_type": "proof",
                "source_note": "real local UI proof",
                "copyright_status": "self_captured",
                "resolution": "1920x1080",
                "used_in_scenes": ["S01"],
                "is_evidence": True,
                "risk": "low",
                "contains_private_info": False,
                "contains_contact_info": False,
                "contains_qr_code": False,
                "qa_notes": "real proof",
            },
            {
                "asset_id": "BG001",
                "type": "generated_visual",
                "asset_role": "background_plate",
                "path": str(background_file),
                "source": "local generated placeholder",
                "provider": "local_pil_renderer_from_prompt_pack",
                "model": "local_pil_renderer",
                "prompt_id": "BG001",
                "prompt_path": "background_prompt_pack.md#BG001",
                "unique_prompt": True,
                "evidence_boundary": "support only; not evidence",
                "asset_source_type": "generated",
                "source_note": "Support background only; not official UI and not factual proof.",
                "copyright_status": "self_created",
                "resolution": "1920x1080",
                "used_in_scenes": ["S01"],
                "is_evidence": False,
                "risk": "low",
                "contains_private_info": False,
                "contains_contact_info": False,
                "contains_qr_code": False,
                "qa_notes": "support visual, not evidence",
            },
        ]
    }
    manifest_path = tmp_path / "asset_manifest.json"
    out = tmp_path / "asset_validation.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_assets.py"),
            "--manifest",
            str(manifest_path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert any("gpt-image-2" in issue and "local PIL" in issue for issue in data["blocking_issues"])


def test_storyboard_validation_requires_three_skill_production_stack(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard["title"] = "3 个 Codex Skill 怎么配合做视频"
    storyboard["scenes"][0]["concept"] = "Remotion 负责组件化动画"
    storyboard["scenes"][0]["voice"] = "第一个 Remotion，负责把复杂画面做成组件化动画。"
    storyboard["scenes"][0]["caption"] = "Remotion 做组件动画"
    storyboard["scenes"][0]["on_screen_text"] = ["Remotion", "组件化动画"]
    storyboard["scenes"][1]["concept"] = "HyperFrames 负责最终时间线"
    storyboard["scenes"][1]["voice"] = "第二个 HyperFrames，负责字幕、时间线和最终成片。"
    storyboard["scenes"][1]["caption"] = "HyperFrames 做成片"
    storyboard["scenes"][1]["on_screen_text"] = ["HyperFrames", "最终时间线"]
    storyboard["scenes"][2]["concept"] = "ImageGen 负责视觉素材"
    storyboard["scenes"][2]["voice"] = "第三个 ImageGen，先把封面、概念图和案例图做出来。"
    storyboard["scenes"][2]["caption"] = "ImageGen 做素材"
    storyboard["scenes"][2]["on_screen_text"] = ["ImageGen", "视觉素材"]

    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["signals"]["production_stack_required"] is True
    assert any("production_stack" in issue for issue in data["issues"])

    proof_chain = {
        "entry_or_source": "真实入口或官方/本地证据",
        "operation_or_step": "展示一次可复现操作",
        "output_or_result": "展示生成结果或文件",
        "viewer_value": "说明观众为什么要保存",
    }
    storyboard["production_stack"] = {
        "reference_learning_applied": True,
        "reference_pattern": "three_skill_reference",
        "workflow_order": ["ImageGen 先做视觉素材", "Remotion 做组件化动画", "HyperFrames 做最终成片"],
        "primary_tools": [
            {"name": "Remotion", "role": "组件化动画和数据驱动画面", "evidence_chain": proof_chain},
            {"name": "HyperFrames", "role": "最终时间线、字幕、音画同步和渲染", "evidence_chain": proof_chain},
            {"name": "ImageGen", "aliases": ["Image Gen"], "role": "封面、概念图和结果图素材", "evidence_chain": proof_chain},
        ],
    }
    for scene in storyboard["scenes"][:3]:
        scene["visual"]["proof_chain"] = proof_chain

    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["signals"]["production_stack_valid"] is True
    assert data["signals"]["tool_proof_chain_count"] == 3


def test_storyboard_validation_requires_codex_plugin_plan_for_six_plugins(tmp_path):
    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard["title"] = "6 个 Codex 插件怎么配合做 AI 视频"
    plugin_names = ["Browser", "GitHub", "Hugging Face", "HyperFrames", "OpenAI Developers", "HeyGen"]
    proof_chain = {
        "entry_or_source": "当前 Codex 插件入口或官方/本地证据",
        "operation_or_step": "展示一次插件可复现操作",
        "output_or_result": "展示截图、日志、文件或生成结果",
        "viewer_value": "说明这个插件解决哪一步生产问题",
    }
    for index, name in enumerate(plugin_names):
        scene = storyboard["scenes"][index]
        scene["concept"] = f"{name} 插件角色"
        scene["voice"] = f"{name} 负责这一条视频里的一个可验证环节。"
        scene["caption"] = f"{name} 有明确边界"
        scene["on_screen_text"] = [name, "证据", "边界"]
        scene["visual"]["proof_chain"] = proof_chain

    storyboard["production_stack"] = {
        "reference_learning_applied": True,
        "reference_pattern": "six_codex_plugin_reference",
        "workflow_order": ["Browser 抓证据", "GitHub/Hugging Face 补来源", "HyperFrames 终版成片"],
        "primary_tools": [
            {"name": name, "role": f"{name} 插件能力演示", "evidence_chain": proof_chain}
            for name in plugin_names
        ],
    }

    path = tmp_path / "storyboard.json"
    out = tmp_path / "storyboard_validation.json"
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["signals"]["codex_plugin_plan_required"] is True
    assert any("codex_plugin_plan" in issue for issue in data["issues"])

    storyboard["codex_plugin_plan"] = {
        "use_case": "six-plugin AI video workflow",
        "plugins": [
            {
                "name": "Browser",
                "availability": "available_in_session",
                "role": "capture web and local UI proof",
                "allowed_by_default": True,
                "evidence_required": ["URL", "screenshot", "operation note"],
                "cost_or_auth_boundary": "Codex-included unless Chrome login state is required",
                "fallback": "local screenshot or terminal/file proof",
            },
            {
                "name": "GitHub",
                "availability": "available_in_session",
                "role": "inspect repositories, issues, PRs, and source evidence",
                "allowed_by_default": True,
                "evidence_required": ["repo URL", "file or issue reference", "summary"],
                "cost_or_auth_boundary": "read-only by default; no commit, push, or PR without user request",
                "fallback": "local repo files or public web source",
            },
            {
                "name": "Hugging Face",
                "availability": "available_in_session",
                "role": "inspect models, datasets, papers, and Spaces",
                "allowed_by_default": True,
                "evidence_required": ["Hub URL", "license/source note", "artifact reference"],
                "cost_or_auth_boundary": "public inspection only; jobs/training/hardware need approval",
                "fallback": "official docs or local open-source reference",
            },
            {
                "name": "HyperFrames",
                "availability": "available_in_session",
                "role": "assemble timeline, captions, inspect, render, and delivery",
                "allowed_by_default": True,
                "evidence_required": ["composition path", "inspect log", "rendered MP4", "QA report"],
                "cost_or_auth_boundary": "Codex plugin/runtime path; final delivery still needs QA pass",
                "fallback": "labeled draft only, not final",
            },
            {
                "name": "OpenAI Developers",
                "availability": "available_in_session",
                "role": "verify OpenAI docs and API/App/Agents SDK claims",
                "allowed_by_default": True,
                "evidence_required": ["official docs source", "code path", "terminal output when executed"],
                "cost_or_auth_boundary": "docs/read-only by default; new API keys or paid API calls need approval",
                "fallback": "official OpenAI docs citation without execution claim",
            },
            {
                "name": "HeyGen",
                "availability": "needs_user_approval",
                "role": "optional avatar, presenter, or lipsync segment",
                "allowed_by_default": False,
                "evidence_required": ["user approval", "job/session ID", "generated media path"],
                "cost_or_auth_boundary": "credit/account/upload path must be approved for the current task",
                "fallback": "voiceover plus proof-card scene",
            },
        ],
        "blocked_plugins": [],
        "approval_required_for": ["HeyGen credit-consuming avatar generation"],
    }
    path.write_text(json.dumps(storyboard, ensure_ascii=False), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["signals"]["codex_plugin_plan_valid"] is True
    assert data["signals"]["codex_plugin_count"] == 6
    assert data["signals"]["six_codex_plugins_documented"] is True


def test_score_script_rejects_accelerated_voiceover(tmp_path):
    copy_path = tmp_path / "copy.md"
    out = tmp_path / "script_score.json"
    source = (ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "copy_package.md").read_text(encoding="utf-8")
    copy_path.write_text(source + "\n语速：1.12x\n", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "score_script.py"),
            "--copy",
            str(copy_path),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert "voiceover speed must stay normal; do not use accelerated narration" in data["issues"]


def test_score_topic_can_apply_learning_bank(tmp_path):
    bank = tmp_path / "learning_bank.md"
    out = tmp_path / "topics.json"
    bank.write_text("- What worked:\n  - 真实截图\n  - 对比\n- What to fix:\n  - 抽象背景\n", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "score_topic.py"),
            "--input",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "topic_candidates.json"),
            "--out",
            str(out),
            "--learning-bank",
            str(bank),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["learning_bank_applied"]["worked_terms"]
    assert data["candidates"][0]["learning_bank_adjustment"]["score_delta"] > 0
