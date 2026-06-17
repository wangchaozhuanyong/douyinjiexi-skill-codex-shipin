#!/usr/bin/env python3
"""Health check for the Douyin AI Video Director skill."""

from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "references",
    "references/workflow_contract.md",
    "references/video_quality_contract.md",
    "references/premium_video_quality_playbook.md",
    "references/free_first_open_source_stack.md",
    "references/runtime_decision_matrix.md",
    "references/codex_plugin_integration.md",
    "references/timeline_contract.md",
    "references/shared_video_quality_core.md",
    "references/video_style_router.md",
    "references/content_formats.md",
    "references/topic_selection_rules.md",
    "references/ai_circle_content_rules.md",
    "references/creative_rubric.md",
    "references/script_quality_rules.md",
    "references/douyin_compliance_rules.md",
    "references/reference_video_rules.md",
    "references/visual_sync_rules.md",
    "references/visual_aesthetic_rules.md",
    "references/hyperframes_delivery.md",
    "references/hyperframes_components.md",
    "references/post_publish_review.md",
    "references/learning_bank.md",
    "references/failed_case_library.md",
    "references/director_decision_patterns.md",
    "assets/hyperframes_components/README.md",
    "schemas",
    "schemas/asset_manifest.schema.json",
    "schemas/topic_candidates.schema.json",
    "schemas/copy_package.schema.json",
    "schemas/semantic_review.schema.json",
    "schemas/reference_analysis.schema.json",
    "schemas/storyboard.schema.json",
    "schemas/storyboard_audio_locked.schema.json",
    "schemas/compliance_report.schema.json",
    "schemas/qa_report.schema.json",
    "schemas/visual_review.schema.json",
    "schemas/metadata.schema.json",
    "schemas/post_publish_review.schema.json",
    "schemas/production_postmortem.schema.json",
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
    "tests/test_v3_gates.py",
    "scripts/score_topic.py",
    "scripts/research_topic.py",
    "scripts/score_script.py",
    "scripts/check_public_copy.py",
    "scripts/evaluate_copy_semantic.py",
    "scripts/analyze_reference.py",
    "scripts/extract_reference_frames.py",
    "scripts/validate_storyboard.py",
    "scripts/build_narration_bed.py",
    "scripts/remux_root_audio.py",
    "scripts/check_audio_continuity.py",
    "scripts/validate_assets.py",
    "scripts/video_technical_qa.py",
    "scripts/frame_review.py",
    "scripts/visual_aesthetic_review.py",
    "scripts/qa_gate.py",
    "scripts/promote_final.py",
    "scripts/update_learning_bank.py",
    "scripts/apply_learning_bank.py",
    "scripts/generate_production_postmortem.py",
    "scripts/check_golden_project.py",
    "scripts/run_pipeline.py",
    "scripts/media_probe.py",
    "examples/golden_ai_prompt_case/expected_qa_report.json",
    "examples/golden_ai_prompt_case/internal/topic_candidates.json",
    "examples/golden_ai_prompt_case/internal/copy_package.md",
    "examples/golden_ai_prompt_case/internal/copy_package.json",
    "examples/golden_ai_prompt_case/internal/storyboard.json",
    "examples/golden_ai_prompt_case/internal/asset_manifest.json",
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


def parse_simple_yaml(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    data: dict[str, object] = {}
    current_section: Optional[dict[str, object]] = None
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if ":" not in raw_line:
            raise ValueError(f"invalid YAML line {lineno}: {raw_line}")
        key, value = raw_line.strip().split(":", 1)
        value = value.strip()
        if indent == 0:
            if value:
                data[key] = parse_scalar(value)
                current_section = None
            else:
                section: dict[str, object] = {}
                data[key] = section
                current_section = section
        elif indent == 2 and current_section is not None:
            current_section[key] = parse_scalar(value)
        else:
            raise ValueError(f"unsupported YAML indentation at line {lineno}: {raw_line}")
    interface = data.get("interface")
    policy = data.get("policy")
    if not isinstance(interface, dict):
        raise ValueError("agents/openai.yaml missing interface section")
    if not isinstance(policy, dict):
        raise ValueError("agents/openai.yaml missing policy section")
    for required in ["display_name", "short_description", "default_prompt"]:
        if not interface.get(required):
            raise ValueError(f"agents/openai.yaml missing {required}")
    if policy.get("allow_implicit_invocation") is not True:
        raise ValueError("agents/openai.yaml must allow implicit invocation")
    return data


def parse_scalar(value: str) -> object:
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


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
            if line_count <= 1 and len(text.strip()) > 120:
                issues.append(f"{path.relative_to(ROOT)} appears flattened into one line")
            if path.suffix == ".py" and text.startswith("#!") and "\n" not in text[:120]:
                issues.append(f"{path.relative_to(ROOT)} has code on the shebang line")
            if path.suffix in {".md", ".json"} and len(text) > 500 and line_count < 3:
                issues.append(f"{path.relative_to(ROOT)} has too few lines for a structured {path.suffix} file")
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


def check_script_help() -> list[str]:
    checked: list[str] = []
    for path in sorted((ROOT / "scripts").glob("*.py")):
        result = subprocess.run(
            [sys.executable, str(path), "--help"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=15,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip().splitlines()
            message = detail[-1] if detail else "no output"
            raise RuntimeError(f"{path.relative_to(ROOT)} --help failed: {message}")
        checked.append(str(path.relative_to(ROOT)))
    return checked


def check_pytest_collect() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q", "tests"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"pytest collect failed: {detail}")


def main() -> int:
    if any(arg in {"-h", "--help"} for arg in sys.argv[1:]):
        print("usage: doctor.py\n\nRun skill health checks, script --help checks, and pytest collection.")
        return 0

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

    try:
        check_script_help()
    except Exception as exc:
        issues.append(str(exc))

    try:
        check_pytest_collect()
    except Exception as exc:
        issues.append(str(exc))

    if issues:
        print("Doctor failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("Doctor passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
