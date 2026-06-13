from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_skill_manifest_has_required_frontmatter():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\n")
    end = text.find("\n---\n", 4)
    assert end > 0
    frontmatter = text[4:end]
    assert "name: douyin-hyperframes-remake" in frontmatter
    assert "description:" in frontmatter
    assert "AI 圈知识类抖音短视频" in frontmatter


def test_skill_body_is_director_contract_not_rule_wall():
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert "Core Workflow" in text
    assert "references/workflow_contract.md" in text
    assert len(text.splitlines()) < 220
