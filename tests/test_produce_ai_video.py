from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_produce_module():
    spec = importlib.util.spec_from_file_location("produce_ai_video", ROOT / "scripts" / "produce_ai_video.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_repair_module():
    spec = importlib.util.spec_from_file_location(
        "repair_hyperframes_leading_frames",
        ROOT / "scripts" / "repair_hyperframes_leading_frames.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_render_profile_module():
    spec = importlib.util.spec_from_file_location(
        "write_hyperframes_render_profile",
        ROOT / "scripts" / "write_hyperframes_render_profile.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_image(path: Path, color: tuple[int, int, int]) -> None:
    pillow = pytest.importorskip("PIL.Image")
    image = pillow.new("RGB", (64, 36), color)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def write_content_image(path: Path) -> None:
    pillow = pytest.importorskip("PIL.Image")
    draw_mod = pytest.importorskip("PIL.ImageDraw")
    image = pillow.new("RGB", (64, 36), (4, 8, 12))
    draw = draw_mod.Draw(image)
    draw.rectangle((8, 6, 56, 28), fill=(210, 220, 228))
    draw.line((8, 30, 56, 12), fill=(60, 200, 240), width=2)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def write_support_card_with_blank_blocks(path: Path) -> None:
    pillow = pytest.importorskip("PIL.Image")
    draw_mod = pytest.importorskip("PIL.ImageDraw")
    image = pillow.new("RGB", (1280, 720), (6, 15, 18))
    draw = draw_mod.Draw(image)
    draw.rectangle((92, 54, 1188, 194), fill=(238, 231, 205))
    draw.rectangle((150, 462, 1130, 634), fill=(238, 231, 205))
    draw.rectangle((92, 245, 1188, 300), fill=(28, 47, 51))
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def write_textured_support_card(path: Path) -> None:
    pillow = pytest.importorskip("PIL.Image")
    draw_mod = pytest.importorskip("PIL.ImageDraw")
    image = pillow.new("RGB", (1280, 720), (6, 15, 18))
    draw = draw_mod.Draw(image)
    for i in range(18):
        x = 80 + i * 62
        color = (35 + i % 4 * 8, 76 + i % 5 * 6, 82 + i % 3 * 12)
        draw.rectangle((x, 90, x + 42, 570), fill=color)
    for y in range(140, 560, 80):
        draw.line((90, y, 1190, y + 20), fill=(82, 190, 202), width=3)
    draw.rectangle((130, 180, 1120, 260), outline=(230, 204, 130), width=4)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def write_passed_review_reports(internal: Path) -> None:
    (internal / "visual_review.json").write_text('{"status":"passed","blocking_issues":[]}\n', encoding="utf-8")
    (internal / "frame_review_report.json").write_text('{"status":"passed","blocking_issues":[]}\n', encoding="utf-8")


def write_asset_manifest_with_support_card(internal: Path, asset_path: str) -> None:
    (internal / "asset_manifest.json").write_text(
        json.dumps(
            {
                "assets": [
                    {
                        "asset_id": "support_card",
                        "type": "designed_card",
                        "path": asset_path,
                        "asset_source_type": "support",
                        "role": "support_card",
                        "provider": "local_original_renderer",
                        "source_note": "local original source summary card; support visual, not evidence",
                    }
                ]
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def write_visual_gate_ready_artifacts(project: Path, metadata: dict | None = None) -> Path:
    internal = project / "internal"
    hyperframes = project / "assets" / "hyperframes"
    internal.mkdir(parents=True, exist_ok=True)
    hyperframes.mkdir(parents=True, exist_ok=True)
    (hyperframes / "index.html").write_text("<main>HyperFrames timeline</main>\n", encoding="utf-8")
    (internal / "draft.mp4").write_bytes(b"placeholder-video")
    write_image(internal / "first_frame_cover.png", (12, 20, 34))
    write_image(internal / "actual_frame_000_cover.png", (12, 20, 34))
    write_image(internal / "actual_frame_001_after_cover.png", (210, 214, 218))
    write_passed_review_reports(internal)
    data = {
        "regression_prevention": {
            "advanced_transitions_only": True,
            "voice_safe_sfx": True,
            "useful_foreground_modules_only": True,
        }
    }
    if metadata:
        data.update(metadata)
    (internal / "metadata.json").write_text(json.dumps(data, ensure_ascii=False) + "\n", encoding="utf-8")
    return internal


def write_passed_png_route_reports(internal: Path) -> None:
    (internal / "hyperframes_render_profile.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "render_target": "project_directory",
                "command_cwd": str(internal.parent),
                "composition_entry": "index.html",
                "profile": {
                    "render_mode": "png_sequence",
                    "render_target": "project_directory",
                    "worker_count": 1,
                    "max_worker_count": 1,
                    "protocol_timeout_ms": 900000,
                },
                "command_template": [
                    "npx",
                    "--yes",
                    "hyperframes",
                    "render",
                    "--format",
                    "png-sequence",
                    "--fps",
                    "30",
                    "--protocol-timeout",
                    "900000",
                    "--workers",
                    "1",
                    "--output",
                    str(internal / "hf_frames"),
                ],
                "blocking_issues": [],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (internal / "leading_frame_repair_report.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "action": "repaired",
                "issues": [],
                "first_content_frame": {"frame_number": 3, "content_score": 12.0},
                "contract": {
                    "cover_slot_preserved": True,
                    "frame_one_returns_to_main_timeline": True,
                },
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def test_visual_regression_gate_blocks_legacy_pil_rawvideo_renderer(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    (internal / "generate_video.py").write_text(
        "from PIL import ImageDraw\n"
        "def render_video():\n"
        "    command = ['ffmpeg', '-f', 'rawvideo']\n"
        "    return ImageDraw.Draw\n",
        encoding="utf-8",
    )
    write_passed_review_reports(internal)

    report = module.visual_regression_gate(project)

    assert report["status"] == "failed"
    assert report["legacy_source_hits"]
    assert any(hit["rule"] == "legacy_pil_imagedraw_import" for hit in report["legacy_source_hits"])


def test_visual_regression_gate_ignores_temporary_internal_build_project(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    hyperframes = project / "assets" / "hyperframes"
    internal.mkdir(parents=True)
    hyperframes.mkdir(parents=True)
    (hyperframes / "index.html").write_text("<main>HyperFrames timeline</main>\n", encoding="utf-8")
    (internal / "build_project.py").write_text(
        "from PIL import ImageDraw\n"
        "command = ['ffmpeg', '-f', 'rawvideo']\n",
        encoding="utf-8",
    )
    (internal / "draft.mp4").write_bytes(b"placeholder-video")
    write_image(internal / "first_frame_cover.png", (12, 20, 34))
    write_image(internal / "actual_frame_000_cover.png", (12, 20, 34))
    write_image(internal / "actual_frame_001_after_cover.png", (210, 214, 218))
    write_passed_review_reports(internal)
    (internal / "metadata.json").write_text(
        '{"regression_prevention":{"advanced_transitions_only":true,"voice_safe_sfx":true,"useful_foreground_modules_only":true}}\n',
        encoding="utf-8",
    )

    report = module.visual_regression_gate(project)

    assert report["status"] == "passed"
    assert report["legacy_source_hits"] == []


def test_repair_hyperframes_leading_frames_moves_first_content_to_frame_one(tmp_path):
    module = load_repair_module()
    frames = tmp_path / "outputs" / "demo" / "internal" / "hf_frames"
    write_image(frames / "frame_000000.png", (0, 0, 0))
    write_image(frames / "frame_000001.png", (0, 0, 0))
    write_image(frames / "frame_000002.png", (0, 0, 0))
    write_content_image(frames / "frame_000003.png")
    before_frame0 = (frames / "frame_000000.png").read_bytes()
    expected_content = (frames / "frame_000003.png").read_bytes()

    report = module.repair_sequence(frames, out=tmp_path / "report.json")

    assert report["status"] == "passed"
    assert report["action"] == "repaired"
    assert report["repaired_frame_count"] == 2
    assert (frames / "frame_000000.png").read_bytes() == before_frame0
    assert (frames / "frame_000001.png").read_bytes() == expected_content
    assert (frames / "frame_000002.png").read_bytes() == expected_content


def test_repair_hyperframes_leading_frames_preserves_first_file_for_one_based_sequence(tmp_path):
    module = load_repair_module()
    frames = tmp_path / "outputs" / "demo" / "internal" / "hf_frames"
    write_image(frames / "frame_000001.png", (0, 0, 0))
    write_image(frames / "frame_000002.png", (0, 0, 0))
    write_content_image(frames / "frame_000003.png")
    preserved_first = (frames / "frame_000001.png").read_bytes()
    expected_content = (frames / "frame_000003.png").read_bytes()

    report = module.repair_sequence(frames, out=tmp_path / "report.json")

    assert report["status"] == "passed"
    assert report["start_frame"] == 2
    assert report["preserved_frame_numbers"] == [1]
    assert (frames / "frame_000001.png").read_bytes() == preserved_first
    assert (frames / "frame_000002.png").read_bytes() == expected_content


def test_write_hyperframes_render_profile_uses_serial_stable_png_route(tmp_path):
    module = load_render_profile_module()
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    (internal / "fixed_template_selection.json").write_text(
        json.dumps(
            {
                "scene_motion_templates": {
                    "hyperframes_render_profile": {
                        "render_mode": "png_sequence",
                        "worker_count": 1,
                        "max_worker_count": 1,
                        "protocol_timeout_ms": 900000,
                    }
                }
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    report = module.build_profile(project, "assets/hyperframes/index.html")

    assert report["status"] == "passed"
    assert report["render_target"] == "project_directory"
    assert report["command_cwd"] == str(project)
    assert report["composition_entry"] == "assets/hyperframes/index.html"
    assert report["profile"]["worker_count"] == 1
    assert report["profile"]["render_target"] == "project_directory"
    assert "--workers" in report["command_template"]
    assert "900000" in report["command_template"]
    assert "assets/hyperframes/index.html" not in report["command_template"]


def test_visual_regression_gate_rejects_old_html_entry_render_profile(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    internal = write_visual_gate_ready_artifacts(
        project,
        {
            "quality_spec": {
                "render_policy": "HyperFrames PNG sequence to FFmpeg stable MP4",
            }
        },
    )
    write_passed_png_route_reports(internal)
    profile_path = internal / "hyperframes_render_profile.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile["render_target"] = "html_entry_file"
    profile["profile"]["render_target"] = "html_entry_file"
    profile["command_template"] = [
        "npx",
        "--yes",
        "hyperframes",
        "render",
        "index.html",
        "--format",
        "png-sequence",
        "--fps",
        "30",
        "--protocol-timeout",
        "900000",
        "--workers",
        "1",
        "--output",
        str(internal / "hf_frames"),
    ]
    profile_path.write_text(json.dumps(profile, ensure_ascii=False) + "\n", encoding="utf-8")

    report = module.visual_regression_gate(project)

    assert report["status"] == "failed"
    assert "hyperframes_render_profile.render_target must be project_directory" in report["issues"]
    assert any("not an HTML entry file: index.html" in issue for issue in report["issues"])


def test_publish_evidence_preflight_reports_missing_strict_evidence(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    (project / "internal").mkdir(parents=True)

    report = module.publish_evidence_preflight(project)

    assert report["status"] == "failed"
    assert any("provider_usage_audit missing or empty" in issue for issue in report["issues"])
    assert any("qingdou_keyword_check missing or empty" in issue for issue in report["issues"])


def test_publish_evidence_preflight_passes_with_required_reports(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    internal.mkdir(parents=True)
    (internal / "provider_usage_audit.json").write_text(
        json.dumps({"status": "passed", "issues": [], "blocking_issues": []}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (internal / "on_screen_and_publish_text_compliance_report.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "checked_files": [str(internal / "publish_cover_text.txt")],
                "blocking_issues": [],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (internal / "publish_cover_report.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "checks": {"dynamic_text_overlay_used": True},
                "blocking_issues": [],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (internal / "qingdou_keyword_check.json").write_text(
        json.dumps({"status": "user_override_accepted", "blocking_issues": []}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    report = module.publish_evidence_preflight(project)

    assert report["status"] == "passed"
    assert report["issues"] == []


def test_visual_regression_gate_requires_png_render_and_leading_reports_for_png_route(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    write_visual_gate_ready_artifacts(
        project,
        {
            "quality_spec": {
                "render_policy": "HyperFrames PNG sequence to FFmpeg stable MP4",
            }
        },
    )

    report = module.visual_regression_gate(project)

    assert report["status"] == "failed"
    assert "hyperframes_render_profile.json missing or empty for HyperFrames PNG sequence route" in report["issues"]
    assert "leading_frame_repair_report.json missing or empty for HyperFrames PNG sequence route" in report["issues"]


def test_visual_regression_gate_requires_visual_beats_after_audio_lock(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    internal = write_visual_gate_ready_artifacts(
        project,
        {
            "tts_speed": 1.0,
            "voice": {"provider": "edge_tts", "voice_id": "zh-CN-YunyangNeural"},
        },
    )
    (internal / "storyboard.audio_locked.json").write_text(
        json.dumps(
            {
                "audio_lock": {
                    "scene_audio": [
                        {"scene_id": "S01", "start": 0, "end": 11.2, "max_audio_gap_ms": 80},
                    ]
                },
                "scenes": [
                    {"scene_id": "S01", "duration_target": 11.2, "beat_map": [{"time_offset_sec": 0.3}]},
                ],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    report = module.visual_regression_gate(project)

    assert report["status"] == "failed"
    assert any("S01 has 1 visual beats for 11.20s locked audio" in issue for issue in report["issues"])


def test_visual_regression_gate_passes_png_route_with_audio_beats_and_repair_reports(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    internal = write_visual_gate_ready_artifacts(
        project,
        {
            "tts_speed": 1.0,
            "voice": {"provider": "edge_tts", "voice_id": "zh-CN-YunyangNeural"},
            "quality_spec": {
                "render_policy": "HyperFrames PNG sequence to FFmpeg stable MP4",
            },
        },
    )
    write_passed_png_route_reports(internal)
    (internal / "storyboard.audio_locked.json").write_text(
        json.dumps(
            {
                "audio_lock": {
                    "scene_audio": [
                        {"scene_id": "S01", "start": 0, "end": 11.2, "max_audio_gap_ms": 80},
                    ]
                },
                "scenes": [
                    {
                        "scene_id": "S01",
                        "duration_target": 11.2,
                        "beat_map": [
                            {"time_offset_sec": 0.3},
                            {"time_offset_sec": 4.2},
                            {"time_offset_sec": 8.4},
                        ],
                    },
                ],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    report = module.visual_regression_gate(project)

    assert report["status"] == "passed"
    assert report["checks"]["stable_png_render_profile_passed"] is True
    assert report["checks"]["leading_frame_repair_passed"] is True
    assert report["checks"]["audio_locked_visual_beats_passed"] is True


def test_visual_regression_gate_passes_with_real_frame_evidence_and_hyperframes_source(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    hyperframes = project / "assets" / "hyperframes"
    internal.mkdir(parents=True)
    hyperframes.mkdir(parents=True)
    (hyperframes / "index.html").write_text("<main>HyperFrames timeline</main>\n", encoding="utf-8")
    (internal / "draft.mp4").write_bytes(b"placeholder-video")
    write_image(internal / "first_frame_cover.png", (12, 20, 34))
    write_image(internal / "actual_frame_000_cover.png", (12, 20, 34))
    write_image(internal / "actual_frame_001_after_cover.png", (210, 214, 218))
    write_passed_review_reports(internal)
    (internal / "metadata.json").write_text(
        '{"regression_prevention":{"advanced_transitions_only":true,"voice_safe_sfx":true,"useful_foreground_modules_only":true}}\n',
        encoding="utf-8",
    )

    report = module.visual_regression_gate(project)

    assert report["status"] == "passed"
    assert report["checks"]["no_legacy_renderer_source"] is True
    assert report["checks"]["first_frame_cover_matches"] is True
    assert report["checks"]["frame1_returns_to_main_timeline"] is True


def test_visual_regression_gate_accepts_legacy_foreground_flag_alias(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    hyperframes = project / "assets" / "hyperframes"
    internal.mkdir(parents=True)
    hyperframes.mkdir(parents=True)
    (hyperframes / "index.html").write_text("<main>HyperFrames timeline</main>\n", encoding="utf-8")
    (internal / "draft.mp4").write_bytes(b"placeholder-video")
    write_image(internal / "first_frame_cover.png", (12, 20, 34))
    write_image(internal / "actual_frame_000_cover.png", (12, 20, 34))
    write_image(internal / "actual_frame_001_after_cover.png", (210, 214, 218))
    write_passed_review_reports(internal)
    (internal / "metadata.json").write_text(
        '{"regression_prevention":{"advanced_transitions_only":true,"voice_safe_sfx":true,"no_useless_background_modules":true}}\n',
        encoding="utf-8",
    )

    report = module.visual_regression_gate(project)

    assert report["status"] == "passed"


def test_visual_regression_gate_rejects_baked_blank_support_card_blocks(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    internal = write_visual_gate_ready_artifacts(project)
    support = project / "assets" / "support" / "bad_card.png"
    write_support_card_with_blank_blocks(support)
    write_asset_manifest_with_support_card(internal, "assets/support/bad_card.png")

    report = module.visual_regression_gate(project)

    assert report["status"] == "failed"
    assert report["checks"]["support_cards_no_baked_blank_blocks"] is False
    assert any("baked blank highlight" in issue for issue in report["issues"])


def test_visual_regression_gate_allows_textured_support_card_without_blank_blocks(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    internal = write_visual_gate_ready_artifacts(project)
    support = project / "assets" / "support" / "good_card.png"
    write_textured_support_card(support)
    write_asset_manifest_with_support_card(internal, "assets/support/good_card.png")

    report = module.visual_regression_gate(project)

    assert report["status"] == "passed"
    assert report["checks"]["support_cards_no_baked_blank_blocks"] is True


def test_visual_regression_gate_requires_layout_motion_report_for_fixed_templates(tmp_path):
    module = load_produce_module()
    project = tmp_path / "outputs" / "demo"
    internal = project / "internal"
    hyperframes = project / "assets" / "hyperframes"
    internal.mkdir(parents=True)
    hyperframes.mkdir(parents=True)
    (hyperframes / "index.html").write_text("<main>HyperFrames timeline</main>\n", encoding="utf-8")
    (internal / "draft.mp4").write_bytes(b"placeholder-video")
    write_image(internal / "first_frame_cover.png", (12, 20, 34))
    write_image(internal / "actual_frame_000_cover.png", (12, 20, 34))
    write_image(internal / "actual_frame_001_after_cover.png", (210, 214, 218))
    write_passed_review_reports(internal)
    (internal / "metadata.json").write_text(
        '{"regression_prevention":{"advanced_transitions_only":true,"voice_safe_sfx":true,"useful_foreground_modules_only":true}}\n',
        encoding="utf-8",
    )
    (internal / "fixed_template_selection.json").write_text(
        '{"motion_layout_contract":{"required_report":"internal/layout_motion_contract_report.json"}}\n',
        encoding="utf-8",
    )

    report = module.visual_regression_gate(project)

    assert report["status"] == "failed"
    assert "layout_motion_contract_report.json missing or empty" in report["issues"]
