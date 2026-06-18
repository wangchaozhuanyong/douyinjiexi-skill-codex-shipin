import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
QA = ROOT / "scripts" / "qa_gate.py"
PROMOTE = ROOT / "scripts" / "promote_final.py"
PROVIDER_AUDIT = ROOT / "scripts" / "audit_provider_usage.py"
BUILD_CONTRACT = ROOT / "scripts" / "build_publish_contract.py"
PRE_PUBLISH_GATE = ROOT / "scripts" / "pre_publish_gate.py"
from voice_quality import voice_provider_passes
from audit_provider_usage import imagegen_provider_assets
from qa_gate import visual_style_decision_issues
QUALITY_SPEC = {
    "target_quality_level": "high_quality",
    "render_quality": "hyperframes_high",
    "min_bitrate": 3500000,
    "source_asset_policy": "use 1080p-or-higher proof assets and avoid low-res upscales",
    "sfx_policy": "subtle UI/click/card cues below narration",
    "cover_policy": "standalone poster cover, not a random frame grab",
    "frame_review_policy": "first 5 seconds, full contact sheet, and crowded details reviewed",
    "provider_policy": "free_first_local_or_authorized_openai_only",
    "runtime_choice": "HyperFrames final timeline; Remotion component clips when needed; FFmpeg only for mechanical media",
    "caption_template_plan": "mix proof_callout, comparison_label, word_highlight, chapter_card, terminal_code_caption, and final_takeaway",
    "timeline_contract_ref": "internal/timeline_contract.md",
    "narration_continuity_policy": "single continuous root narration audio; visual transitions never restart, mute, fade, or gap voice; max planned transition audio gap 80ms",
}
VOICE_SPEC = {
    "provider": "edge_tts",
    "voice_id": "zh-CN-XiaoxiaoNeural",
    "sample_approved": True,
}


def write_qingdou_keyword_check(internal: Path, caption: str = "发布文案\n") -> None:
    (internal / "qingdou_keyword_check.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "platform": "轻抖",
                "checked_platform": "斗音",
                "checked_fields": ["title", "caption", "topics"],
                "final_check": {"status": "passed", "message": "未检查到敏感词", "items": []},
                "final_title": "测试标题",
                "final_caption": caption.strip(),
                "final_topics": ["#AI工具"],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def test_voice_quality_rejects_apple_system_voice_disguised_as_passed():
    assert (
        voice_provider_passes(
            {
                "voice": {
                    "provider": "local_apple_neural_tts",
                    "voice_id": "Tingting",
                    "qa_status": "passed",
                    "notes": "Generated with macOS say as a timing preview.",
                }
            }
        )
        is False
    )
    assert voice_provider_passes({"voice": VOICE_SPEC}) is True


def test_provider_audit_does_not_count_unavailable_imagegen_note_as_used():
    local_support_assets = [
        {
            "asset_id": "BG001",
            "type": "designed_card",
            "provider": "local_pil_renderer",
            "source": "local support background after Codex in-chat ImageGen export was unavailable",
            "source_note": "not generated; paid Codex ImageGen did not expose a project file path",
        }
    ]
    real_imagegen_assets = [
        {
            "asset_id": "BG002",
            "type": "generated_visual",
            "provider": "codex_builtin_imagegen",
            "model": "gpt-image-2",
        }
    ]

    assert imagegen_provider_assets(local_support_assets) == []
    assert imagegen_provider_assets(real_imagegen_assets) == real_imagegen_assets


def test_visual_style_decision_rejects_missing_required_fields():
    issues = visual_style_decision_issues(
        {
            "style_intent": "tutorial_template",
            "selected_brightness_grade": "L4 bright tutorial",
        }
    )

    assert "visual_style_decision.json missing required field: selected_palette_family" in issues
    assert "visual_style_decision.json missing required field: why_this_style" in issues


def test_visual_style_decision_rejects_mechanical_daylight_default():
    issues = visual_style_decision_issues(
        {
            "status": "locked",
            "style_intent": "default_bright_tutorial",
            "selected_brightness_grade": "L4 bright tutorial",
            "selected_palette_family": "daylight_productivity",
            "selected_material_family": "paper_acrylic",
            "selected_layout_family": "three_step_ladder",
            "why_this_style": "默认沿用最近成功的浅色模板。",
            "why_not_other_styles": "No comparison documented.",
        }
    )

    assert any("must not choose daylight_productivity" in issue for issue in issues)


def test_visual_style_decision_requires_plan_alignment():
    issues = visual_style_decision_issues(
        {
            "status": "locked",
            "style_intent": "source proof terminal tutorial",
            "selected_brightness_grade": "L2 dark with bright proof surfaces",
            "selected_palette_family": "graphite_ivory_teal",
            "selected_material_family": "matte_editorial",
            "selected_layout_family": "source_wall_grid",
            "why_this_style": "The script is a Codex terminal proof workflow, so source and code evidence need controlled dark contrast.",
            "why_not_other_styles": "Bright tutorial and product keynote styles would weaken the terminal proof and serious source analysis.",
        },
        {
            "primary_brightness_grade": "L4 bright tutorial",
            "primary_palette_family": "daylight_productivity",
            "primary_material_family": "paper_acrylic",
            "primary_layout_family": "three_step_ladder",
        },
    )

    assert any("selected_brightness_grade must match" in issue for issue in issues)
    assert any("selected_palette_family must match" in issue for issue in issues)


def test_visual_style_decision_accepts_content_grounded_daylight_choice():
    issues = visual_style_decision_issues(
        {
            "status": "locked",
            "style_intent": "beginner ChatGPT template tutorial",
            "selected_brightness_grade": "L4 bright tutorial",
            "selected_palette_family": "daylight_productivity",
            "selected_material_family": "paper_acrylic",
            "selected_layout_family": "three_step_ladder",
            "why_this_style": "The copy teaches a beginner prompt template with reusable steps, so a bright tutorial canvas keeps cards readable.",
            "why_not_other_styles": "Newsroom, terminal proof, and warning contrast styles are unnecessary because this is not news, code evidence, or risk correction.",
        },
        {
            "primary_brightness_grade": "L4 bright tutorial",
            "primary_palette_family": "daylight_productivity",
            "primary_material_family": "paper_acrylic",
            "primary_layout_family": "three_step_ladder",
        },
    )

    assert issues == []


def test_qa_gate_fails_when_required_files_missing(tmp_path):
    project = tmp_path / "outputs" / "demo"
    out = project / "internal" / "qa_report.json"
    result = subprocess.run(
        [sys.executable, str(QA), "--project", str(project), "--out", str(out)],
        text=True,
        capture_output=True,
    )
    report = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert report["status"] == "failed"
    assert report["blocking_issues"]


def test_qa_gate_passes_complete_project(tmp_path):
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)

    (internal / "topic_candidates.json").write_text((ROOT / "templates" / "topic_candidates.example.json").read_text(encoding="utf-8"), encoding="utf-8")
    (internal / "selected_topic.json").write_text('{"topic_id":"T001","reason":"highest score"}\n', encoding="utf-8")
    (internal / "copy_package.md").write_text("# Copy Package\n安全文案\n", encoding="utf-8")
    (internal / "copy_package.json").write_text('{"title_options":["A","B","C"],"retention_beats":[]}\n', encoding="utf-8")
    (internal / "semantic_review.json").write_text('{"status":"passed","composite_score":8.7,"scores":{},"hard_fail_reasons":[],"revision_suggestions":[],"signals":{}}\n', encoding="utf-8")
    (internal / "beginner_value_review.json").write_text(
        '{"status":"passed","final_decision":"pass","total_score":9.0,"scores":{"title_clarity":9.2,"first_5_seconds_pull":9.2,"beginner_task_fit":9.0,"visible_result":8.8,"step_by_step_value":8.8,"time_saving_claim":8.8,"problem_example_score":8.8,"jargon_translation":9.2,"save_asset":9.0},"rewrite_required":[]}\n',
        encoding="utf-8",
    )
    (internal / "compliance_report.json").write_text('{"status":"passed","checked_files":[],"risk_items":[],"claim_items":[],"summary":{"error_count":0,"warning_count":0}}\n', encoding="utf-8")
    (internal / "visual_style_decision.json").write_text(
        json.dumps(
            {
                "status": "locked",
                "style_intent": "beginner ChatGPT template tutorial",
                "selected_brightness_grade": "L4 bright tutorial",
                "selected_palette_family": "daylight_productivity",
                "selected_material_family": "paper_acrylic",
                "selected_layout_family": "three_step_ladder",
                "why_this_style": "The copy teaches a beginner prompt template with reusable steps, so a bright tutorial canvas keeps cards readable and useful.",
                "why_not_other_styles": "Newsroom, terminal proof, product keynote, and warning contrast styles are rejected because this is not news, code proof, release, or risk correction.",
                "decision_inputs": {
                    "topic_type": "template tutorial",
                    "copy_mood": "beginner useful",
                    "evidence_density": "medium proof card",
                    "reference_video": "none",
                },
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (internal / "visual_style_plan.json").write_text(
        '{"status":"locked","primary_brightness_grade":"L4 bright tutorial","primary_palette_family":"daylight_productivity","primary_material_family":"paper_acrylic","primary_layout_family":"three_step_ladder","dark_light_rhythm_rule":"active tutorial scenes stay bright and readable","diversity_limits":{"max_consecutive_dark_scenes":1}}\n',
        encoding="utf-8",
    )
    storyboard = (ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8")
    (internal / "storyboard.json").write_text(storyboard, encoding="utf-8")
    (internal / "storyboard.audio_locked.json").write_text(storyboard, encoding="utf-8")
    background = project / "assets" / "backgrounds" / "bg-01.png"
    background.parent.mkdir(parents=True)
    background.write_bytes(b"placeholder")
    (internal / "background_prompt_pack.md").write_text(
        "# Background Prompt Pack\n\nAsset role: background_plate\nVisual thesis: prompt ambiguity becomes a visible proof desk with a verification lane.\nTopic binding: the background supports a ChatGPT prompt workflow demo, with room for before/after prompt proof.\nInformation job: hold the proof screenshot, checklist, and final template without competing with captions.\nBackground role: topic-bound support stage, never evidence.\nFormat: 16:9 1920x1080\nAvoid: text, fake UI, pseudo-code, watermark.\n",
        encoding="utf-8",
    )
    (internal / "asset_manifest.json").write_text(
        json.dumps(
            {
                "assets": [
                    {
                        "asset_id": "BG001",
                        "type": "generated_visual",
                        "asset_role": "background_plate",
                        "path": str(background),
                        "source": "ImageGen generated text-free background plate",
                        "provider": "codex_builtin_imagegen",
                        "model": "gpt-image-2",
                        "prompt_id": "BG001",
                        "prompt_path": "background_prompt_pack.md#BG001",
                        "unique_prompt": True,
                        "evidence_boundary": "support only; not evidence and not official UI",
                        "scene_id": "S01",
                        "narration_line_supported": "Prompt 不是一句空话，而是目标、约束、证据和验收标准。",
                        "scene_function": "tutorial_step",
                        "visual_archetype": "bright_productivity_desk",
                        "brightness_grade": "L4 bright tutorial",
                        "palette_family": "daylight_productivity",
                        "material_family": "paper_acrylic",
                        "layout_family": "three_step_ladder",
                        "energy_level": "useful, clear, beginner-friendly",
                        "visual_thesis": "Prompt ambiguity becomes a visible proof desk with a verification lane.",
                        "topic_binding": "This background supports a ChatGPT prompt workflow demo with space for before and after proof.",
                        "beginner_usefulness": "The viewer can copy the prompt structure into a real writing task.",
                        "information_job": "Hold the proof screenshot, checklist, and final template without competing with captions.",
                        "background_role": "Topic-bound support stage for the prompt workflow explanation.",
                        "viewer_takeaway": "A good prompt workflow looks like a verification desk, not a decorative AI wallpaper.",
                        "composition": "Wide 16:9 proof desk with center proof area, right annotation rail, and lower-third caption-safe band.",
                        "foreground": "Subtle glass edge anchors and soft shadows frame the proof area without readable fake text.",
                        "midground": "Blank before-after prompt lanes and checklist-card silhouettes wait for HyperFrames labels.",
                        "background": "Matte graphite studio depth with quiet source-wall shapes and no pseudo interface text.",
                        "camera_lens": "35mm straight-on editorial wide shot, stable and readable.",
                        "lighting": "Soft upper-left key light, restrained rim light on panel edges, low ambient falloff, realistic shadows.",
                        "material_texture": "Smoked glass, matte graphite, brushed metal rails, subtle paper grain, crisp non-plastic edges.",
                        "color_hierarchy": "Charcoal base, warm ivory text-safe zones, teal focus accent reserved for verification.",
                        "color_system": "Brightness grade L4 bright tutorial; daylight productivity palette; warm ivory proof surfaces; cobalt active accent; amber result highlight.",
                        "depth_layering": "Foreground rail, midground proof lanes, and background source-wall depth are separated by contact shadows and overlap.",
                        "text_safe_zones": "Center proof area and lower third stay clean for Chinese titles, subtitles, and proof cards.",
                        "motion_usage": "HyperFrames will add slow parallax, proof-card rail wipes, and checklist focus reveal.",
                        "animation_affordance": "Foreground rail, midground proof lanes, and background source-wall depth can move separately.",
                        "primary_animated_object": "three prompt step cards and the final template card",
                        "dark_light_motion_rule": "active objects become brighter and larger; dark areas stay behind bright proof surfaces",
                        "negative_prompt": "No fake UI, pseudo text, random neon grid, tiny labels, QR code, watermark, people, or clutter.",
                        "regeneration_criteria": "Regenerate if it looks generic, includes fake text, lacks safe zones, or competes with captions.",
                        "diversity_check": "must not repeat the same visual archetype, palette family, and layout family as the previous generated scene",
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
                ]
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (internal / "asset_validation.json").write_text('{"status":"passed","blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    (internal / "asset_prompt_validation.json").write_text(
        '{"status":"passed","prompt_card_count":1,"validated_fields":[],"blocking_issues":[],"warnings":[]}\n',
        encoding="utf-8",
    )
    (internal / "visual_tone_report.json").write_text(
        '{"status":"passed","image_count":1,"results":[{"asset_id":"BG001","status":"passed","issues":[]}],"blocking_issues":[]}\n',
        encoding="utf-8",
    )
    metadata = {
        "task_id": "demo",
        "created_at": "2026-06-13",
        "final_video_path": "final/final.mp4",
        "duration": 20,
        "scene_count": 6,
        "target_width": 1920,
        "target_height": 1080,
        "fps": 30,
        "tts_speed": 1.0,
        "voice": VOICE_SPEC,
        "quality_spec": QUALITY_SPEC,
    }
    (internal / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False) + "\n", encoding="utf-8")
    (internal / "script_score.json").write_text('{"first_3_seconds_score":9.3,"script_score":8.7,"first_5_seconds_score":9.2,"save_value_score":8.8,"proof_score":8.7,"compliance_score":9.6,"empty_talk_ratio":0.05}\n', encoding="utf-8")
    (internal / "storyboard_validation.json").write_text(
        '{"status":"passed","issues":[],"scene_count":6,"evidence_runtime_ratio":0.62,"signals":{"quality_spec_valid":true,"provider_policy_valid":true,"layered_scene_count":6,"quality_check_scene_count":6,"source_class_scene_count":6,"caption_template_scene_count":6,"caption_template_count":4,"premium_motion_scene_count":6,"audio_continuity_scene_count":6,"forbidden_provider_scene_count":0}}\n',
        encoding="utf-8",
    )
    (internal / "video_technical_qa.json").write_text('{"status":"passed","metadata_consistency":{"checked":true,"issues":[]},"blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    (internal / "audio_continuity_report.json").write_text('{"status":"passed","video":{"duration":20},"audio":{"has_audio":true,"duration":20,"duration_gap":0},"audio_lock":{"root_narration_path":"assets/audio/narration-continuous.mp3","scene_count":6,"expected_duration":20,"transition_gaps":[]},"blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    (internal / "render_text_manifest.json").write_text(
        '{"texts":[{"role":"primary_title","shot_id":"D01","text":"问题可能不是工具","start":0,"end":2.4}]}\n',
        encoding="utf-8",
    )
    (internal / "screen_text_proofread_report.json").write_text('{"status":"passed","blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    (internal / "empty_frame_report.json").write_text('{"status":"passed","blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    (internal / "frame_review_report.json").write_text('{"status":"passed","warnings":[]}\n', encoding="utf-8")
    (internal / "visual_review.json").write_text(
        '{"status":"passed","overall_visual_score":8.8,"scores":{"first_5s_score":9.0,"readability_score":8.8,"composition_score":8.7,"layering_score":9.0,"quality_check_score":9.0,"caption_variety_score":8.9,"source_class_score":8.9,"sound_design_score":8.8,"export_readiness_score":8.8},"blocking_issues":[],"warnings":[],"signals":{"scene_count":6,"layered_scene_count":6,"quality_check_scene_count":6,"source_class_scene_count":6,"caption_template_scene_count":6,"caption_template_count":4,"metadata_quality_spec_valid":true,"voice_provider_approved":true,"sfx_policy_valid":true,"runtime_choice_valid":true}}\n',
        encoding="utf-8",
    )
    (internal / "draft.mp4").write_bytes(b"placeholder")
    (internal / "cover.png").write_bytes(b"placeholder")
    (internal / "cover_publish_vertical.png").write_bytes(b"vertical")
    (internal / "cover_publish_horizontal.png").write_bytes(b"horizontal")
    (internal / "publish_cover_text.txt").write_text("测试标题\n发布级 AI 知识视频\n", encoding="utf-8")
    (internal / "publish_cover_report.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "frame_grab_used": False,
                "outputs": {
                    "primary": str(internal / "cover.png"),
                    "vertical_3_4": str(internal / "cover_publish_vertical.png"),
                    "horizontal_4_3": str(internal / "cover_publish_horizontal.png"),
                    "cover_text": str(internal / "publish_cover_text.txt"),
                },
                "checks": {"cover_text_written": True},
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (internal / "on_screen_and_publish_text_compliance_report.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "checked_files": [str(internal / "publish_cover_text.txt"), str(internal / "publish_copy.txt")],
                "risk_items": [],
                "claim_items": [],
                "summary": {"error_count": 0, "warning_count": 0},
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (internal / "publish_copy.txt").write_text("发布文案\n", encoding="utf-8")
    write_qingdou_keyword_check(internal)

    out = internal / "qa_report.json"
    result = subprocess.run(
        [sys.executable, str(QA), "--project", str(project), "--out", str(out)],
        text=True,
        capture_output=True,
    )
    report = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 0
    assert report["status"] == "passed"
    assert report["quality_level"] == "high_quality"
    assert report["hard_gates"]["semantic_review_passed"] is True
    assert report["hard_gates"]["beginner_value_review_passed"] is True
    assert report["hard_gates"]["visual_review_passed"] is True
    assert report["hard_gates"]["normal_tts_speed"] is True
    assert report["hard_gates"]["quality_spec_documented"] is True
    assert report["hard_gates"]["approved_natural_voice"] is True
    assert report["hard_gates"]["subtle_sfx_required"] is True
    assert report["hard_gates"]["hyperframes_runtime_required"] is True
    assert report["hard_gates"]["frame_review_passed"] is True
    assert report["hard_gates"]["background_prompt_pack_exists"] is True
    assert report["hard_gates"]["asset_prompt_validation_exists"] is True
    assert report["hard_gates"]["asset_prompt_validation_passed"] is True
    assert report["hard_gates"]["generated_background_plate_registered"] is True
    assert report["hard_gates"]["visual_style_decision_exists"] is True
    assert report["hard_gates"]["visual_style_decision_passed"] is True
    assert report["hard_gates"]["visual_style_plan_exists"] is True
    assert report["hard_gates"]["visual_tone_report_exists"] is True
    assert report["hard_gates"]["visual_tone_report_passed"] is True
    assert report["hard_gates"]["free_first_provider_policy"] is True
    assert report["hard_gates"]["storyboard_asset_source_classified"] is True
    assert report["hard_gates"]["storyboard_caption_templates_documented"] is True
    assert report["hard_gates"]["storyboard_premium_motion_documented"] is True
    assert report["hard_gates"]["storyboard_audio_continuity_documented"] is True
    assert report["hard_gates"]["audio_continuity_report_exists"] is True
    assert report["hard_gates"]["audio_continuity_passed"] is True
    assert report["hard_gates"]["layered_scene_design"] is True
    assert report["hard_gates"]["scene_quality_checks_passed"] is True
    assert report["hard_gates"]["visual_asset_source_classified"] is True
    assert report["hard_gates"]["visual_caption_template_variety"] is True
    assert report["hard_gates"]["high_quality_render_policy"] is True
    assert report["blocking_issues"] == []
    assert not (project / "final" / "final.mp4").exists()

    provider_audit = subprocess.run(
        [
            sys.executable,
            str(PROVIDER_AUDIT),
            "--project",
            str(project),
            "--phase",
            "final",
            "--out",
            str(internal / "provider_usage_audit.json"),
            "--md-out",
            str(internal / "provider_usage_audit.md"),
        ],
        text=True,
        capture_output=True,
    )
    provider_report = json.loads((internal / "provider_usage_audit.json").read_text(encoding="utf-8"))
    assert provider_audit.returncode == 0
    assert provider_report["status"] == "passed"

    contract = internal / "publish_contract.json"
    built = subprocess.run(
        [sys.executable, str(BUILD_CONTRACT), "--project", str(project), "--out", str(contract)],
        text=True,
        capture_output=True,
    )
    assert built.returncode == 0

    pre_publish = subprocess.run(
        [sys.executable, str(PRE_PUBLISH_GATE), "--contract", str(contract)],
        text=True,
        capture_output=True,
    )
    gated_contract = json.loads(contract.read_text(encoding="utf-8"))
    assert pre_publish.returncode == 0
    assert gated_contract["gate"]["status"] == "passed"

    promoted = subprocess.run(
        [sys.executable, str(PROMOTE), "--project", str(project), "--contract", str(contract)],
        text=True,
        capture_output=True,
    )
    assert promoted.returncode == 0
    assert (project / "final" / "final.mp4").read_bytes() == b"placeholder"
    assert (project / "final" / "cover.png").exists()
    assert (project / "final" / "publish_copy.txt").exists()
    assert (project / "final" / "publish_contract.json").exists()


def test_pre_publish_gate_requires_qingdou_keyword_check_for_publish_copy(tmp_path):
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    (internal / "qa_report.json").write_text(
        '{"status":"passed","blocking_issues":[],"hard_gates":{"qa":true}}\n',
        encoding="utf-8",
    )
    (internal / "provider_usage_audit.json").write_text(
        '{"status":"passed","issues":[]}\n',
        encoding="utf-8",
    )
    (internal / "draft.mp4").write_bytes(b"placeholder")
    (internal / "cover.png").write_bytes(b"placeholder")
    (internal / "publish_cover_text.txt").write_text("测试标题\n发布级 AI 知识视频\n", encoding="utf-8")
    (internal / "publish_cover_report.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "frame_grab_used": False,
                "outputs": {"cover_text": str(internal / "publish_cover_text.txt")},
                "checks": {"cover_text_written": True},
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (internal / "on_screen_and_publish_text_compliance_report.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "checked_files": [str(internal / "publish_cover_text.txt")],
                "risk_items": [],
                "summary": {"error_count": 0, "warning_count": 0},
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (internal / "metadata.json").write_text('{"task_id":"demo"}\n', encoding="utf-8")
    (internal / "publish_copy.txt").write_text("发布文案\n", encoding="utf-8")

    contract = internal / "publish_contract.json"
    build = subprocess.run(
        [sys.executable, str(BUILD_CONTRACT), "--project", str(project), "--out", str(contract)],
        text=True,
        capture_output=True,
    )
    assert build.returncode == 0

    result = subprocess.run(
        [sys.executable, str(PRE_PUBLISH_GATE), "--contract", str(contract)],
        text=True,
        capture_output=True,
    )
    gated_contract = json.loads(contract.read_text(encoding="utf-8"))

    assert result.returncode != 0
    assert gated_contract["gate"]["status"] == "failed"
    assert "qingdou_keyword_check missing or empty" in gated_contract["gate"]["issues"]
    assert not (project / "final" / "final.mp4").exists()


def test_provider_audit_requires_plugin_plan_for_plugin_workflow(tmp_path):
    project = tmp_path / "outputs" / "plugin-demo"
    internal = project / "internal"
    internal.mkdir(parents=True)

    storyboard = json.loads((ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8"))
    storyboard["title"] = "6 个 Codex 插件怎么配合做 AI 视频"
    proof_chain = {
        "entry_or_source": "真实插件入口或官方来源",
        "operation_or_step": "展示一次可复现操作",
        "output_or_result": "展示截图、日志、文件或生成结果",
        "viewer_value": "说明这个插件解决哪一步生产问题",
    }
    plugin_names = ["Browser", "GitHub", "Hugging Face", "HyperFrames", "OpenAI Developers", "HeyGen"]
    storyboard["production_stack"] = {
        "reference_learning_applied": True,
        "reference_pattern": "six_codex_plugin_reference",
        "workflow_order": ["Browser 抓证据", "GitHub/Hugging Face 补来源", "HyperFrames 终版成片"],
        "primary_tools": [
            {"name": name, "role": f"{name} 插件能力演示", "evidence_chain": proof_chain}
            for name in plugin_names
        ],
    }
    for index, name in enumerate(plugin_names):
        scene = storyboard["scenes"][index]
        scene["concept"] = f"{name} 插件角色"
        scene["voice"] = f"{name} 负责这一条视频里的一个可验证环节。"
        scene["caption"] = f"{name} 有明确边界"
        scene["on_screen_text"] = [name, "证据", "边界"]
        scene["visual"]["proof_chain"] = proof_chain

    (internal / "storyboard.json").write_text(json.dumps(storyboard, ensure_ascii=False) + "\n", encoding="utf-8")
    (internal / "metadata.json").write_text(
        json.dumps({"task_id": "plugin-demo", "quality_spec": QUALITY_SPEC}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (internal / "asset_manifest.json").write_text('{"assets":[]}\n', encoding="utf-8")
    (internal / "video_technical_qa.json").write_text('{"status":"passed"}\n', encoding="utf-8")
    (internal / "frame_review_report.json").write_text('{"status":"passed"}\n', encoding="utf-8")
    (internal / "visual_review.json").write_text('{"status":"passed"}\n', encoding="utf-8")
    (internal / "qa_report.json").write_text('{"status":"passed","quality_level":"high_quality"}\n', encoding="utf-8")
    (internal / "draft.mp4").write_bytes(b"placeholder")

    result = subprocess.run(
        [
            sys.executable,
            str(PROVIDER_AUDIT),
            "--project",
            str(project),
            "--phase",
            "final",
            "--out",
            str(internal / "provider_usage_audit.json"),
        ],
        text=True,
        capture_output=True,
    )
    provider_report = json.loads((internal / "provider_usage_audit.json").read_text(encoding="utf-8"))
    assert result.returncode == 2
    assert provider_report["status"] == "failed"
    assert any("codex_plugin_plan" in issue for issue in provider_report["issues"])


def test_qa_gate_rejects_empty_draft_file(tmp_path):
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    (internal / "topic_candidates.json").write_text((ROOT / "templates" / "topic_candidates.example.json").read_text(encoding="utf-8"), encoding="utf-8")
    (internal / "selected_topic.json").write_text('{"topic_id":"T001"}\n', encoding="utf-8")
    (internal / "copy_package.md").write_text("# Copy Package\n", encoding="utf-8")
    (internal / "copy_package.json").write_text('{"title_options":["A","B","C"]}\n', encoding="utf-8")
    (internal / "semantic_review.json").write_text('{"status":"passed","composite_score":8.7,"scores":{},"hard_fail_reasons":[],"revision_suggestions":[],"signals":{}}\n', encoding="utf-8")
    (internal / "compliance_report.json").write_text('{"status":"passed","checked_files":[],"risk_items":[],"claim_items":[],"summary":{"error_count":0,"warning_count":0}}\n', encoding="utf-8")
    storyboard = (ROOT / "templates" / "storyboard.example.json").read_text(encoding="utf-8")
    (internal / "storyboard.json").write_text(storyboard, encoding="utf-8")
    (internal / "storyboard.audio_locked.json").write_text(storyboard, encoding="utf-8")
    (internal / "asset_manifest.json").write_text('{"assets":[]}\n', encoding="utf-8")
    (internal / "asset_validation.json").write_text('{"status":"passed","blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    (internal / "metadata.json").write_text(
        json.dumps({"task_id": "demo", "tts_speed": 1.0, "voice": VOICE_SPEC, "quality_spec": QUALITY_SPEC}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (internal / "script_score.json").write_text('{"first_3_seconds_score":9.3,"script_score":8.7,"first_5_seconds_score":9.2,"save_value_score":8.8,"proof_score":8.7,"compliance_score":9.6,"empty_talk_ratio":0.05}\n', encoding="utf-8")
    (internal / "storyboard_validation.json").write_text(
        '{"status":"passed","issues":[],"scene_count":6,"evidence_runtime_ratio":0.58,"signals":{"quality_spec_valid":true,"provider_policy_valid":true,"layered_scene_count":6,"quality_check_scene_count":6,"source_class_scene_count":6,"caption_template_scene_count":6,"caption_template_count":4,"premium_motion_scene_count":6,"audio_continuity_scene_count":6,"forbidden_provider_scene_count":0}}\n',
        encoding="utf-8",
    )
    (internal / "video_technical_qa.json").write_text('{"status":"passed","metadata_consistency":{"checked":true,"issues":[]},"blocking_issues":[],"warnings":[]}\n', encoding="utf-8")
    (internal / "frame_review_report.json").write_text('{"status":"passed","warnings":[]}\n', encoding="utf-8")
    (internal / "visual_review.json").write_text(
        '{"status":"passed","overall_visual_score":8.8,"scores":{"first_5s_score":9.0,"readability_score":8.8,"composition_score":8.7,"layering_score":9.0,"quality_check_score":9.0,"caption_variety_score":8.9,"source_class_score":8.9,"sound_design_score":8.8,"export_readiness_score":8.8},"blocking_issues":[],"warnings":[],"signals":{"scene_count":6,"layered_scene_count":6,"quality_check_scene_count":6,"source_class_scene_count":6,"caption_template_scene_count":6,"caption_template_count":4,"metadata_quality_spec_valid":true,"voice_provider_approved":true,"sfx_policy_valid":true,"runtime_choice_valid":true}}\n',
        encoding="utf-8",
    )
    (internal / "draft.mp4").write_bytes(b"")
    (internal / "cover.png").write_bytes(b"placeholder")
    (internal / "publish_copy.txt").write_text("发布文案\n", encoding="utf-8")

    out = internal / "qa_report.json"
    result = subprocess.run(
        [sys.executable, str(QA), "--project", str(project), "--out", str(out)],
        text=True,
        capture_output=True,
    )
    report = json.loads(out.read_text(encoding="utf-8"))
    assert result.returncode == 1
    assert report["status"] == "failed"
    assert "missing draft.mp4" in report["blocking_issues"]
    assert not (project / "final" / "final.mp4").exists()
