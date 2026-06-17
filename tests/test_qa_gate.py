import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
QA = ROOT / "scripts" / "qa_gate.py"
PROMOTE = ROOT / "scripts" / "promote_final.py"
PROVIDER_AUDIT = ROOT / "scripts" / "audit_provider_usage.py"
from voice_quality import voice_provider_passes
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
    (internal / "compliance_report.json").write_text('{"status":"passed","checked_files":[],"risk_items":[],"claim_items":[],"summary":{"error_count":0,"warning_count":0}}\n', encoding="utf-8")
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
                        "visual_thesis": "Prompt ambiguity becomes a visible proof desk with a verification lane.",
                        "topic_binding": "This background supports a ChatGPT prompt workflow demo with space for before and after proof.",
                        "information_job": "Hold the proof screenshot, checklist, and final template without competing with captions.",
                        "background_role": "Topic-bound support stage for the prompt workflow explanation.",
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
    (internal / "publish_copy.txt").write_text("发布文案\n", encoding="utf-8")

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
    assert report["hard_gates"]["visual_review_passed"] is True
    assert report["hard_gates"]["normal_tts_speed"] is True
    assert report["hard_gates"]["quality_spec_documented"] is True
    assert report["hard_gates"]["approved_natural_voice"] is True
    assert report["hard_gates"]["subtle_sfx_required"] is True
    assert report["hard_gates"]["hyperframes_runtime_required"] is True
    assert report["hard_gates"]["frame_review_passed"] is True
    assert report["hard_gates"]["background_prompt_pack_exists"] is True
    assert report["hard_gates"]["generated_background_plate_registered"] is True
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

    promoted = subprocess.run(
        [sys.executable, str(PROMOTE), "--project", str(project)],
        text=True,
        capture_output=True,
    )
    assert promoted.returncode == 0
    assert (project / "final" / "final.mp4").read_bytes() == b"placeholder"
    assert (project / "final" / "cover.png").exists()
    assert (project / "final" / "publish_copy.txt").exists()


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
