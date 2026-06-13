#!/usr/bin/env python3
"""Health check for the Douyin AI Video Director skill."""

from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "references",
    "references/workflow_contract.md",
    "references/video_quality_contract.md",
    "references/content_formats.md",
    "references/topic_selection_rules.md",
    "references/ai_circle_content_rules.md",
    "references/script_quality_rules.md",
    "references/douyin_compliance_rules.md",
    "references/reference_video_rules.md",
    "references/visual_sync_rules.md",
    "references/hyperframes_delivery.md",
    "references/hyperframes_components.md",
    "references/post_publish_review.md",
    "assets/hyperframes_components/README.md",
    "schemas",
    "schemas/asset_manifest.schema.json",
    "schemas/topic_candidates.schema.json",
    "schemas/copy_package.schema.json",
    "schemas/reference_analysis.schema.json",
    "schemas/storyboard.schema.json",
    "schemas/compliance_report.schema.json",
    "schemas/qa_report.schema.json",
    "schemas/metadata.schema.json",
    "schemas/post_publish_review.schema.json",
    "templates",
    "templates/copy_package.template.md",
    "templates/hook_bank.md",
    "templates/script_patterns.md",
    "templates/post_publish_review.template.md",
    "templates/topic_candidates.example.json",
    "templates/storyboard.example.json",
    "templates/qa_report.example.json",
    "tests",
    "tests/test_skill_manifest.py",
    "tests/test_yaml_valid.py",
    "tests/test_scripts_compile.py",
    "tests/test_schema_examples.py",
    "tests/test_copy_checker.py",
    "tests/test_qa_gate.py",
    "scripts/score_topic.py",
    "scripts/research_topic.py",
    "scripts/score_script.py",
    "scripts/check_public_copy.py",
    "scripts/analyze_reference.py",
    "scripts/extract_reference_frames.py",
    "scripts/validate_storyboard.py",
    "scripts/video_technical_qa.py",
    "scripts/frame_review.py",
    "scripts/qa_gate.py",
    "scripts/media_probe.py",
]


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    frontmatter = text[4:end]
    data: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def parse_simple_yaml(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "interface:" not in text:
        raise ValueError("agents/openai.yaml missing interface section")
    for required in ["display_name", "short_description", "default_prompt"]:
        if not re.search(rf"^\s*{required}:", text, flags=re.MULTILINE):
            raise ValueError(f"agents/openai.yaml missing {required}")
    if not re.search(r"^\s*policy:", text, flags=re.MULTILINE):
        raise ValueError("agents/openai.yaml missing policy section")
    if "allow_implicit_invocation: true" not in text:
        raise ValueError("agents/openai.yaml must allow implicit invocation")


def check_not_flattened() -> list[str]:
    issues: list[str] = []
    patterns = [
        "SKILL.md",
        "README.md",
        "agents/openai.yaml",
        "references/*.md",
        "schemas/*.json",
        "templates/*.md",
        "templates/*.json",
        "scripts/*.py",
        "tests/*.py",
    ]
    for pattern in patterns:
        for path in sorted(ROOT.glob(pattern)):
            if path.is_dir():
                continue
            text = path.read_text(encoding="utf-8")
            line_count = len(text.splitlines())
            if line_count <= 1 and len(text) > 120:
                issues.append(f"{path.relative_to(ROOT)} appears flattened into one line")
            if path.suffix == ".py" and text.startswith("#!") and "\n" not in text[:120]:
                issues.append(f"{path.relative_to(ROOT)} has code on the shebang line")
    return issues


def compile_scripts() -> list[str]:
    compiled: list[str] = []
    for path in sorted((ROOT / "scripts").glob("*.py")):
        py_compile.compile(str(path), doraise=True)
        compiled.append(str(path.relative_to(ROOT)))
    return compiled


def check_json_files() -> list[str]:
    loaded: list[str] = []
    for folder in ["schemas", "templates"]:
        for path in sorted((ROOT / folder).glob("*.json")):
            json.loads(path.read_text(encoding="utf-8"))
            loaded.append(str(path.relative_to(ROOT)))
    return loaded


def main() -> int:
    issues: list[str] = []
    for raw in REQUIRED_PATHS:
        if not (ROOT / raw).exists():
            issues.append(f"missing {raw}")

    try:
        frontmatter = parse_frontmatter(ROOT / "SKILL.md")
        for key in ["name", "description"]:
            if not frontmatter.get(key):
                issues.append(f"frontmatter missing {key}")
    except Exception as exc:
        issues.append(str(exc))

    try:
        parse_simple_yaml(ROOT / "agents/openai.yaml")
    except Exception as exc:
        issues.append(str(exc))

    issues.extend(check_not_flattened())

    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").exists() else ""
    if "~/.agents/skills" not in readme:
        issues.append("README.md must contain ~/.agents/skills install path")
    if ".agents/skills" not in readme:
        issues.append("README.md must contain repo-level .agents/skills install path")

    try:
        compile_scripts()
    except Exception as exc:
        issues.append(f"script compile failed: {exc}")

    try:
        check_json_files()
    except Exception as exc:
        issues.append(f"json schema/example load failed: {exc}")

    if issues:
        print("Doctor failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Doctor passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
