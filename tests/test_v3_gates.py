import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def complete_visual_director_fields(asset_id: str = "BG001") -> dict[str, object]:
    return {
        "scene_id": "S01",
        "narration_line_supported": "Prompt 不是一句空话，而是目标、约束、证据和验收标准。",
        "scene_function": "tutorial_step",
        "visual_archetype": "bright_productivity_desk",
        "brightness_grade": "L4 bright tutorial",
        "palette_family": "daylight_productivity",
        "material_family": "paper_acrylic",
        "layout_family": "three_step_ladder",
        "energy_level": "useful, clear, beginner-friendly",
        "visual_thesis": "Prompt ambiguity becomes a visible verification desk with a before-after proof lane.",
        "topic_binding": "This background is for an AI prompt tutorial and leaves space for before and after prompt proof.",
        "beginner_usefulness": "The viewer should feel this prompt structure can be copied immediately for a real writing task.",
        "information_job": "Support the screenshot, checklist, and final template without becoming fake evidence.",
        "background_role": "Topic-bound support stage, never proof.",
        "viewer_takeaway": "A good prompt workflow looks like a verification desk, not a decorative AI wallpaper.",
        "composition": "Wide 16:9 editorial proof desk with center proof area, right annotation rail, and lower-third caption-safe band.",
        "foreground": "Subtle glass edge anchors and soft shadows frame the proof area without readable fake text.",
        "midground": "Blank before-after prompt lanes and checklist-card silhouettes wait for HyperFrames labels.",
        "background": "Matte graphite studio depth with quiet source-wall shapes and no pseudo interface text.",
        "camera_lens": "35mm straight-on editorial wide shot, stable and readable.",
        "lighting": "Soft upper-left key light, restrained rim light on panel edges, low ambient falloff, realistic contact shadows.",
        "material_texture": "Smoked glass, matte graphite, brushed metal rails, subtle paper grain, crisp non-plastic edges.",
        "color_hierarchy": "Charcoal base, warm ivory text-safe zones, teal focus accent reserved for the verification path.",
        "color_system": "Brightness grade L4 bright tutorial; daylight productivity palette; warm ivory base; clean paper surfaces; cobalt active accent; amber result highlight; high readability.",
        "depth_layering": "Foreground rail, midground proof lanes, and background source-wall depth are separated by contact shadows and overlap.",
        "text_safe_zones": "Center proof area and lower third stay clean for Chinese titles, subtitles, and proof cards.",
        "motion_usage": "HyperFrames will add slow parallax, reveal proof cards with rail wipes, and focus the checklist path.",
        "animation_affordance": f"{asset_id} has separate foreground rail, midground proof lanes, and background source-wall depth for layered motion.",
        "primary_animated_object": "Three prompt step cards and the final template card.",
        "dark_light_motion_rule": "Active objects become brighter and larger; dark areas stay behind bright proof surfaces.",
        "negative_prompt": "No fake UI, pseudo text, random neon grid, tiny labels, QR code, watermark, stock-photo people, or clutter.",
        "regeneration_criteria": "Regenerate if the image looks like generic tech wallpaper, includes fake text, lacks safe zones, or competes with captions.",
        "diversity_check": "Must not reuse the same visual archetype, palette family, and layout family as the previous scene.",
    }


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


def test_asset_prompt_validation_passes_golden_prompt_pack(tmp_path):
    out = tmp_path / "asset_prompt_validation.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_asset_prompts.py"),
            "--prompt-pack",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "background_prompt_pack.md"),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["prompt_card_count"] >= 1


def test_asset_prompt_validation_rejects_generic_background_language(tmp_path):
    prompt_pack = tmp_path / "background_prompt_pack.md"
    prompt_pack.write_text(
        """# Bad Prompt Pack

## BG-01
Asset role: background_plate
Scene ID: S01
Narration line supported: 用 AI 做一个高级视频。
Visual thesis: 高级科技感背景
Topic binding: 科技感背景
Information job: 高级背景
Background role: 高级科技感背景
Viewer takeaway: 看起来高级
Composition: cinematic 4K premium tech background
Foreground: cool background
Midground: abstract digital technology background
Background: futuristic AI dashboard
Camera/lens: cinematic
Lighting: premium
Material/texture: high quality
Color hierarchy: cyberpunk
Text-safe zones: leave some space
Motion usage in HyperFrames: make it cool
Animation affordance: same as motion usage
Evidence boundary: support only, not evidence
Negative prompt: no text
Regeneration criteria: make it better
""",
        encoding="utf-8",
    )
    out = tmp_path / "asset_prompt_validation.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_asset_prompts.py"),
            "--prompt-pack",
            str(prompt_pack),
            "--out",
            str(out),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert data["status"] == "failed"
    assert any("vague material phrase" in issue or "generic" in issue for issue in data["blocking_issues"])


def test_build_storyboard_outputs_v3_valid_storyboard(tmp_path):
    storyboard = tmp_path / "storyboard.json"
    validation = tmp_path / "storyboard_validation.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "build_storyboard.py"),
            "--copy",
            str(ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "copy_package.md"),
            "--out",
            str(storyboard),
        ],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_storyboard.py"),
            "--storyboard",
            str(storyboard),
            "--out",
            str(validation),
        ],
        text=True,
        capture_output=True,
    )
    data = json.loads(validation.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert data["status"] == "passed"
    assert data["signals"]["director_shots_valid"] is True
    assert data["signals"]["director_operation_shot_count"] >= 2
    assert data["signals"]["caption_template_count"] >= 2


def test_hyperframes_component_library_contains_premium_ai_components():
    component_dir = ROOT / "assets" / "hyperframes_components"
    tokens = (component_dir / "tokens.css").read_text(encoding="utf-8")
    css = (component_dir / "components.css").read_text(encoding="utf-8")
    js = (component_dir / "components.js").read_text(encoding="utf-8")
    for token in ["--stage-bg", "--panel-bg", "--caption-band-height", "--proof-width", "--rail-width", "--radius-lg", "--shadow-proof", "--blur-glass"]:
        assert token in tokens
    for selector in [".hf-cold-open-proof", ".hf-source-wall-grid", ".hf-operation-simulation", ".hf-evidence-result-card", ".hf-process-rail", ".hf-final-template"]:
        assert selector in css
    for name in ["ColdOpenProofCard", "SourceWallGrid", "OperationSimulation", "EvidenceResultCard", "ProcessRail", "FinalTemplate"]:
        assert name in js


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


def test_visual_review_rejects_local_apple_tingting_even_with_qa_status(tmp_path):
    frame_review = tmp_path / "frame_review_report.json"
    metadata = tmp_path / "metadata.json"
    out = tmp_path / "visual_review.json"
    frame_review.write_text('{"status":"passed","artifacts":{},"blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    metadata_data = json.loads((ROOT / "examples" / "golden_ai_prompt_case" / "internal" / "metadata.json").read_text(encoding="utf-8"))
    metadata_data["voice"] = {
        "provider": "local_apple_neural_tts",
        "voice_id": "Tingting",
        "qa_status": "passed",
        "notes": "Continuous narration generated with macOS say for timing preview.",
    }
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
    assert data["signals"]["voice_provider_approved"] is False
    assert any("macOS say" in issue for issue in data["blocking_issues"])


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
        "# Background Prompt Pack\n\nAsset role: background_plate\nScene ID: S01\nNarration line supported: Prompt 不是一句空话，而是目标、约束、证据和验收标准。\nScene function: tutorial_step\nVisual archetype: bright_productivity_desk\nBrightness grade: L4 bright tutorial\nPalette family: daylight_productivity\nMaterial family: paper_acrylic\nLayout family: three_step_ladder\nEnergy level: useful, clear, beginner-friendly\nVisual thesis: the prompt workflow becomes a calm proof desk and verification lane.\nTopic binding: this background is for an AI prompt tutorial and leaves space for before/after prompt proof.\nBeginner usefulness: the viewer should feel the prompt structure can be copied immediately for a real writing task.\nInformation job: support the screenshot, checklist, and final template without becoming fake evidence.\nBackground role: topic-bound support stage, never proof.\nViewer takeaway: a good prompt workflow looks like a verification desk, not a decorative AI wallpaper.\nComposition: wide 16:9 proof desk with center proof area, lower-third caption-safe band, and right annotation rail.\nForeground: subtle glass edge anchors and soft shadows frame the proof area.\nMidground: blank before-after prompt lanes and checklist-card silhouettes wait for HyperFrames labels.\nBackground: matte graphite studio depth with quiet source-wall shapes and no pseudo interface text.\nCamera/lens: 35mm straight-on editorial wide shot.\nLighting: soft upper-left key light, restrained rim light, ambient falloff, realistic contact shadows.\nMaterial/texture: smoked glass, matte graphite, brushed metal rails, subtle paper grain.\nColor hierarchy: charcoal base, warm ivory safe zones, teal accent reserved for verification.\nColor system: brightness grade L4 bright tutorial; daylight productivity palette; warm ivory base; clean paper surfaces; cobalt active accent; amber result highlight; high readability.\nDepth/layering: foreground rail, midground proof lanes, and background depth are separated by contact shadows and overlap.\nText-safe zones: center proof area and lower third stay clean for titles, subtitles, and proof cards.\nMotion usage in HyperFrames: slow parallax, proof-card rail wipes, and checklist focus reveal.\nAnimation affordance: foreground rail, midground proof lanes, and background depth move separately.\nPrimary animated object: three prompt step cards and the final template card.\nDark/light motion rule: active objects become brighter and larger; dark areas stay behind bright proof surfaces.\nEvidence boundary: support only; not evidence and not official UI.\nNegative prompt: no text, fake UI, pseudo-code, logos, watermark, neon grid, random particles, QR code, clutter.\nRegeneration criteria: regenerate if it looks like generic tech wallpaper, includes fake text, lacks safe zones, or competes with captions.\nDiversity check: must not reuse the same visual archetype, palette family, and layout family as the previous scene.\n",
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
            **complete_visual_director_fields("BG001"),
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
    assert data["visual_director_prompt_count"] == 1


def test_asset_validation_rejects_generic_visual_prompt_language(tmp_path):
    proof_file = tmp_path / "proof.png"
    background_file = tmp_path / "background.png"
    proof_file.write_bytes(b"proof")
    background_file.write_bytes(b"background")
    (tmp_path / "background_prompt_pack.md").write_text(
        "# Background Prompt Pack\n\nAsset role: background_plate\nVisual thesis: 高级科技感背景\nTopic binding: 高级科技感背景\nInformation job: 高级科技感背景\nBackground role: 高级背景\nComposition: 高级、炫酷、震撼\nAvoid: fake UI.\n",
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
                "source": "ImageGen generated text-free background plate",
                "provider": "codex_builtin_imagegen",
                "model": "gpt-image-2",
                "prompt_id": "BG001",
                "prompt_path": "background_prompt_pack.md#BG001",
                "unique_prompt": True,
                "evidence_boundary": "support only; not evidence and not official UI",
                "scene_id": "S01",
                "narration_line_supported": "高级科技感背景",
                "visual_thesis": "高级科技感背景",
                "topic_binding": "高级科技感背景",
                "information_job": "高级科技感背景",
                "background_role": "高级背景",
                "viewer_takeaway": "高级科技感",
                "composition": "高级、炫酷、震撼",
                "foreground": "高级",
                "midground": "科技感",
                "background": "未来感",
                "camera_lens": "cinematic",
                "lighting": "酷炫",
                "material_texture": "4K",
                "color_hierarchy": "赛博",
                "text_safe_zones": "设计感",
                "motion_usage": "高级一点",
                "animation_affordance": "随便高级一点",
                "negative_prompt": "no fake UI",
                "regeneration_criteria": "make it better",
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
    assert data["visual_director_prompt_count"] == 0
    assert any("generic" in issue or "vague material phrase" in issue for issue in data["blocking_issues"])


def test_asset_validation_rejects_background_without_topic_binding(tmp_path):
    proof_file = tmp_path / "proof.png"
    background_file = tmp_path / "background.png"
    proof_file.write_bytes(b"proof")
    background_file.write_bytes(b"background")
    (tmp_path / "background_prompt_pack.md").write_text(
        "# Background Prompt Pack\n\nAsset role: background_plate\nFormat: 16:9 1920x1080\nAvoid: text, fake UI.\n",
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
    assert data["background_plate_valid_count"] == 0
    assert any("visual_thesis" in issue for issue in data["blocking_issues"])
    assert any("topic_binding" in issue for issue in data["blocking_issues"])


def test_asset_validation_rejects_local_pil_as_generated_image_provider(tmp_path):
    proof_file = tmp_path / "proof.png"
    background_file = tmp_path / "background.png"
    proof_file.write_bytes(b"proof")
    background_file.write_bytes(b"background")
    (tmp_path / "background_prompt_pack.md").write_text(
        "# Background Prompt Pack\n\nAsset role: background_plate\nVisual thesis: prompt ambiguity is shown as a verification desk with a proof lane.\nTopic binding: this background supports an AI prompt tutorial with before/after prompt panels.\nInformation job: reserve clean zones for proof, risk labels, and final prompt template overlays.\nBackground role: topic-bound support stage, never proof.\nFormat: 16:9 1920x1080\n",
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
                "visual_thesis": "Prompt ambiguity is shown as a verification desk with a proof lane.",
                "topic_binding": "This background supports an AI prompt tutorial with before and after prompt panels.",
                "information_job": "Reserve clean zones for proof, risk labels, and final prompt template overlays.",
                "background_role": "Topic-bound support stage, never proof.",
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
