import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_skill_pr_boundary import PUBLIC_FORBIDDEN_REFERENCES, is_local_only_path


def test_local_desktop_parser_paths_are_blocked():
    assert is_local_only_path("douyin_media_server.py")
    assert is_local_only_path("douyin_to_mp3.py")
    assert is_local_only_path("build_desktop_app.sh")
    assert is_local_only_path("scripts/generate_ai_daily_20260630.py")
    assert is_local_only_path("reference_downloads/demo/reference_source_video.mp4")
    assert is_local_only_path("assets/source_cosmic_backgrounds/source.jpg")
    assert is_local_only_path("zh-Hans.lproj/InfoPlist.strings")


def test_skill_core_paths_remain_visible_for_review():
    assert not is_local_only_path("SKILL.md")
    assert not is_local_only_path("references/ai_video_scheme_7_ant_ai_hotlist_extended.md")
    assert not is_local_only_path("scripts/generate_ant_ai_hotlist_background.py")
    assert not is_local_only_path("assets/ai_background_templates_dynamic/BG_DYNAMIC_11_demo.mp4")


def test_public_forbidden_references_cover_local_reference_dirs():
    assert "reference_downloads/" in PUBLIC_FORBIDDEN_REFERENCES
    assert "assets/source_cosmic_backgrounds/" in PUBLIC_FORBIDDEN_REFERENCES
