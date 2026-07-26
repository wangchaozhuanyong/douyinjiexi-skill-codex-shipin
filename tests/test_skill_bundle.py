from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "douyin-video-production-core",
    "douyin-ai-tool-explainer",
    "douyin-ai-news-explainer",
    "douyin-ai-list-video",
)
RETIRED = (
    "douyin-hyperframes-remake",
    "douyin-ai-premium-director",
    "scheme_7",
    "scheme_1",
    "ant_ai",
    "fixed_template_selection",
    "director_selection",
    "style_recipe",
    "foreground_module",
    "Editorial Chalkboard Evidence Lab",
    *(f"M{index:02d}" for index in range(1, 21)),
    *(f"C{index:02d}" for index in range(1, 31)),
    *(f"TR{index:02d}" for index in range(1, 9)),
)


def test_skill_manifests_are_small_and_named_correctly() -> None:
    for name in SKILLS:
        path = ROOT / "skills" / name / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        assert len(text.splitlines()) <= 200
        frontmatter = yaml.safe_load(text.split("---", 2)[1])
        assert frontmatter["name"] == name
        assert set(frontmatter) == {"name", "description"}


def test_core_is_not_implicitly_invoked() -> None:
    data = yaml.safe_load(
        (ROOT / "skills" / "douyin-video-production-core" / "agents" / "openai.yaml").read_text(encoding="utf-8")
    )
    assert data["policy"]["allow_implicit_invocation"] is False


def test_three_ai_video_categories_are_explicit() -> None:
    expected = {
        "douyin-ai-tool-explainer": (
            "AI工具实操讲解类",
            "ai_tool_explainer",
            "tool_explainer",
        ),
        "douyin-ai-news-explainer": (
            "AI新闻与产品更新解读类",
            "ai_news_explainer",
            "news_explainer",
        ),
        "douyin-ai-list-video": (
            "AI榜单、推荐与对比类",
            "ai_list_video",
            "list_video",
        ),
    }
    for skill_name, identifiers in expected.items():
        text = (ROOT / "skills" / skill_name / "SKILL.md").read_text(encoding="utf-8")
        assert "AI类视频" in text
        for identifier in identifiers:
            assert identifier in text


def test_active_skills_have_no_retired_identifiers() -> None:
    for path in (ROOT / "skills").rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".json", ".jsonl", ".yaml", ".py"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for identifier in RETIRED:
            assert identifier not in text, f"{identifier} found in {path}"


def test_sync_dry_run_lists_four_new_skills() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "sync_skills.py"), "--dry-run"],
        capture_output=True,
        text=True,
        check=True,
    )
    for name in SKILLS:
        assert name in result.stdout
