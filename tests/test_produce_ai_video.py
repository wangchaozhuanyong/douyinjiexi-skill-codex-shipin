from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_produce_module():
    spec = importlib.util.spec_from_file_location("produce_ai_video", ROOT / "scripts" / "produce_ai_video.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_image(path: Path, color: tuple[int, int, int]) -> None:
    pillow = pytest.importorskip("PIL.Image")
    image = pillow.new("RGB", (64, 36), color)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def write_passed_review_reports(internal: Path) -> None:
    (internal / "visual_review.json").write_text('{"status":"passed","blocking_issues":[]}\n', encoding="utf-8")
    (internal / "frame_review_report.json").write_text('{"status":"passed","blocking_issues":[]}\n', encoding="utf-8")


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
