from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_skill_source_manifest.py"


def write_skill(path: Path, name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
name: {name}
description: test skill
---

# Test
""",
        encoding="utf-8",
    )


def run_check(manifest: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--manifest", str(manifest)],
        text=True,
        capture_output=True,
    )


def test_source_manifest_requires_real_skill_and_icon(tmp_path: Path) -> None:
    skill = tmp_path / "skill-creator" / "SKILL.md"
    icon = tmp_path / "skill-creator" / "assets" / "skill.svg"
    write_skill(skill, "skill-creator")
    icon.parent.mkdir(parents=True, exist_ok=True)
    icon.write_text("<svg></svg>\n", encoding="utf-8")
    manifest = tmp_path / "skill_source_manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "scheme_id": "scheme_1_skill_recommendation_no_voice",
                "copy_mode": "source_quoted_or_source_paraphrase",
                "source_policy": "real skill names, icons, and source-backed public copy only",
                "source_scan": [{"type": "local", "path": str(skill)}],
                "items": [
                    {
                        "skill_name": "skill-creator",
                        "display_name": "Skill Creator",
                        "source_type": "local_installed_skill",
                        "source_path_or_url": str(skill),
                        "icon_source": str(icon),
                        "source_description": "test skill",
                        "public_note": "官方描述：test skill。",
                        "claim_evidence": [
                            {
                                "claim_field": "public_note",
                                "claim_text": "官方描述：test skill。",
                                "source_field": "SKILL.md frontmatter description",
                                "source_text": "test skill",
                                "derivation": "direct_quote",
                            }
                        ],
                    }
                ],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    result = run_check(manifest)
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads((tmp_path / "skill_source_manifest_check.json").read_text(encoding="utf-8"))
    assert report["status"] == "passed"


def test_source_manifest_rejects_invented_skill_without_source(tmp_path: Path) -> None:
    manifest = tmp_path / "skill_source_manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "scheme_id": "scheme_1_skill_recommendation_no_voice",
                "copy_mode": "source_quoted_or_source_paraphrase",
                "source_policy": "real skill names and icons only",
                "source_scan": [{"type": "local", "path": "missing"}],
                "items": [
                    {
                        "skill_name": "页面整理 Skill",
                        "display_name": "页面整理 Skill",
                        "source_type": "local_installed_skill",
                        "source_path_or_url": "missing/SKILL.md",
                        "icon_source": "missing/icon.svg",
                        "source_description": "missing source",
                        "public_note": "缺失来源的 Skill 介绍。",
                        "claim_evidence": [
                            {
                                "claim_field": "public_note",
                                "claim_text": "缺失来源的 Skill 介绍。",
                                "source_field": "SKILL.md frontmatter description",
                                "source_text": "missing source",
                                "derivation": "conservative_paraphrase",
                            }
                        ],
                    }
                ],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    result = run_check(manifest)
    assert result.returncode == 1
    report = json.loads((tmp_path / "skill_source_manifest_check.json").read_text(encoding="utf-8"))
    assert report["status"] == "failed"
    assert any("does not exist" in issue for issue in report["blocking_issues"])


def test_source_manifest_rejects_inferred_legacy_skill_copy_without_claim_evidence(tmp_path: Path) -> None:
    skill = tmp_path / "skill-creator" / "SKILL.md"
    icon = tmp_path / "skill-creator" / "assets" / "skill.svg"
    write_skill(skill, "skill-creator")
    icon.parent.mkdir(parents=True, exist_ok=True)
    icon.write_text("<svg></svg>\n", encoding="utf-8")
    manifest = tmp_path / "skill_source_manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "scheme_id": "scheme_1_skill_recommendation_no_voice",
                "copy_mode": "source_quoted_or_source_paraphrase",
                "source_policy": "real skill names, icons, and source-backed public copy only",
                "source_scan": [{"type": "local", "path": str(skill)}],
                "items": [
                    {
                        "skill_name": "skill-creator",
                        "display_name": "Skill Creator",
                        "source_type": "local_installed_skill",
                        "source_path_or_url": str(skill),
                        "icon_source": str(icon),
                        "source_description": "test skill",
                        "public_note": "官方描述：test skill。",
                        "input": "输入重复流程",
                        "purpose": "生成 Skill 规则",
                        "output": "写成 SKILL.md",
                        "usage_note": "输入重复流程，生成 Skill 规则，写成 SKILL.md。",
                        "claim_evidence": [
                            {
                                "claim_field": "public_note",
                                "claim_text": "官方描述：test skill。",
                                "source_field": "SKILL.md frontmatter description",
                                "source_text": "test skill",
                                "derivation": "direct_quote",
                            }
                        ],
                    }
                ],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    result = run_check(manifest)
    assert result.returncode == 1
    report = json.loads((tmp_path / "skill_source_manifest_check.json").read_text(encoding="utf-8"))
    assert report["status"] == "failed"
    assert any("legacy public fields require" in issue for issue in report["blocking_issues"])
