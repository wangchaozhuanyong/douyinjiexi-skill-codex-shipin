#!/usr/bin/env python3
"""Validate source-backed Skill list rows before rendering Scheme 1 videos."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def resolve_path(raw: str, base: Path) -> Path:
    path = Path(raw).expanduser()
    if path.is_absolute():
        return path
    candidate = base / path
    if candidate.exists():
        return candidate
    return ROOT / path


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def strip_yaml_value(value: str) -> str:
    value = value.strip()
    if "#" in value and not value.startswith(("'", '"')):
        value = value.split("#", 1)[0].strip()
    return value.strip().strip("\"'")


def read_skill_metadata(path: Path) -> dict[str, str]:
    if not path.exists() or not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.match(r"---\n(.*?)\n---\n", text, flags=re.S)
    if not match:
        return {}
    frontmatter = match.group(1)
    metadata: dict[str, str] = {}
    for key in ("name", "description"):
        field_match = re.search(rf"^{key}:\s*(.+)$", frontmatter, flags=re.M)
        if field_match:
            metadata[key] = strip_yaml_value(field_match.group(1))
    return metadata


def read_openai_yaml_metadata(path: Path) -> dict[str, str]:
    if not path.exists() or not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8", errors="ignore")
    metadata: dict[str, str] = {}
    for key in ("display_name", "short_description", "icon_small", "icon_large"):
        match = re.search(rf"^\s*{key}:\s*(.+)$", text, flags=re.M)
        if match:
            metadata[key] = strip_yaml_value(match.group(1))
    return metadata


def normalize_source_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().rstrip(".。")


def local_text_contains(paths: list[Path], needle: str) -> bool:
    normalized_needle = normalize_source_text(needle)
    if not normalized_needle:
        return False
    for path in paths:
        if not path.exists() or not path.is_file():
            continue
        text = normalize_source_text(path.read_text(encoding="utf-8", errors="ignore"))
        if normalized_needle in text:
            return True
    return False


def validate_claim_evidence(
    item: dict[str, Any],
    manifest_path: Path,
    skill_name: str,
    source_path: Path | None,
) -> list[str]:
    issues: list[str] = []
    public_note = str(item.get("public_note") or "").strip()
    source_description = str(item.get("source_description") or "").strip()
    claim_evidence = item.get("claim_evidence")

    if not source_description:
        issues.append(f"{skill_name or '<unknown>'}: source_description is required")
    if not public_note:
        issues.append(f"{skill_name or '<unknown>'}: public_note is required")
    if not isinstance(claim_evidence, list) or not claim_evidence:
        issues.append(f"{skill_name or '<unknown>'}: claim_evidence must contain evidence for every public copy claim")
        claim_evidence = []

    evidence_fields: set[str] = set()
    evidence_source_paths: list[Path] = []
    openai_yaml = str(item.get("openai_yaml") or "").strip()
    if source_path:
        evidence_source_paths.append(source_path)
    if openai_yaml and not openai_yaml.startswith(("http://", "https://")):
        evidence_source_paths.append(resolve_path(openai_yaml, manifest_path.parent))

    for index, evidence in enumerate(claim_evidence, start=1):
        if not isinstance(evidence, dict):
            issues.append(f"{skill_name or '<unknown>'}: claim_evidence[{index}] must be an object")
            continue
        claim_field = str(evidence.get("claim_field") or "").strip()
        claim_text = str(evidence.get("claim_text") or evidence.get("claim") or "").strip()
        source_field = str(evidence.get("source_field") or "").strip()
        source_text = str(evidence.get("source_text") or "").strip()
        derivation = str(evidence.get("derivation") or "").strip()
        if not claim_field:
            issues.append(f"{skill_name or '<unknown>'}: claim_evidence[{index}].claim_field is required")
        else:
            evidence_fields.add(claim_field)
        if not claim_text:
            issues.append(f"{skill_name or '<unknown>'}: claim_evidence[{index}].claim_text is required")
        if not source_field:
            issues.append(f"{skill_name or '<unknown>'}: claim_evidence[{index}].source_field is required")
        if not source_text:
            issues.append(f"{skill_name or '<unknown>'}: claim_evidence[{index}].source_text is required")
        if derivation not in {"direct_quote", "conservative_paraphrase"}:
            issues.append(
                f"{skill_name or '<unknown>'}: claim_evidence[{index}].derivation must be direct_quote or conservative_paraphrase"
            )
        if source_text and evidence_source_paths and not local_text_contains(evidence_source_paths, source_text):
            issues.append(f"{skill_name or '<unknown>'}: claim_evidence[{index}].source_text is not found in local source files")

    if public_note and "public_note" not in evidence_fields:
        issues.append(f"{skill_name or '<unknown>'}: public_note must have claim_evidence with claim_field=public_note")

    legacy_public_fields = [field for field in ("input", "purpose", "output", "usage_note") if str(item.get(field) or "").strip()]
    missing_legacy_evidence = [field for field in legacy_public_fields if field not in evidence_fields]
    if missing_legacy_evidence:
        joined = ", ".join(missing_legacy_evidence)
        issues.append(
            f"{skill_name or '<unknown>'}: legacy public fields require their own claim_evidence entries: {joined}"
        )

    return issues


def validate_item(item: dict[str, Any], manifest_path: Path) -> list[str]:
    issues: list[str] = []
    skill_name = str(item.get("skill_name") or "").strip()
    display_name = str(item.get("display_name") or "").strip()
    source_type = str(item.get("source_type") or "").strip()
    source_path_or_url = str(item.get("source_path_or_url") or "").strip()
    icon_source = str(item.get("icon_source") or "").strip()
    icon_strategy = str(item.get("icon_strategy") or "").strip()
    openai_yaml = str(item.get("openai_yaml") or "").strip()

    if not skill_name:
        issues.append("item.skill_name is required")
    if not display_name:
        issues.append(f"{skill_name or '<unknown>'}: display_name is required")
    if not source_type:
        issues.append(f"{skill_name or '<unknown>'}: source_type is required")
    if not source_path_or_url:
        issues.append(f"{skill_name or '<unknown>'}: source_path_or_url is required")

    source_path: Path | None = None

    if source_path_or_url and not source_path_or_url.startswith(("http://", "https://")):
        source_path = resolve_path(source_path_or_url, manifest_path.parent)
        if not source_path.exists():
            issues.append(f"{skill_name or '<unknown>'}: source_path_or_url does not exist: {source_path_or_url}")
        elif source_path.name == "SKILL.md":
            skill_metadata = read_skill_metadata(source_path)
            real_name = skill_metadata.get("name", "")
            if real_name and skill_name and real_name != skill_name:
                issues.append(f"{skill_name}: skill_name does not match SKILL.md name {real_name}")
            source_description = str(item.get("source_description") or "").strip()
            allowed_descriptions = {normalize_source_text(skill_metadata.get("description", ""))}
            if openai_yaml and not openai_yaml.startswith(("http://", "https://")):
                yaml_path = resolve_path(openai_yaml, manifest_path.parent)
                yaml_metadata = read_openai_yaml_metadata(yaml_path)
                allowed_descriptions.add(normalize_source_text(yaml_metadata.get("short_description", "")))
                real_display_name = yaml_metadata.get("display_name", "")
                if real_display_name and display_name and real_display_name != display_name:
                    issues.append(f"{skill_name}: display_name does not match agents/openai.yaml display_name {real_display_name}")
            if source_description and normalize_source_text(source_description) not in {value for value in allowed_descriptions if value}:
                issues.append(f"{skill_name}: source_description must match SKILL.md description or agents/openai.yaml short_description")

    if icon_strategy == "generic_symbol":
        if not str(item.get("generic_symbol") or "").strip():
            issues.append(f"{skill_name or '<unknown>'}: generic_symbol is required when icon_strategy=generic_symbol")
    else:
        if not icon_source:
            issues.append(f"{skill_name or '<unknown>'}: icon_source is required when rendering a real left icon")
        elif not icon_source.startswith(("http://", "https://")):
            icon_path = resolve_path(icon_source, manifest_path.parent)
            if not icon_path.exists() or not icon_path.is_file() or icon_path.stat().st_size <= 0:
                issues.append(f"{skill_name or '<unknown>'}: icon_source does not exist or is empty: {icon_source}")

    issues.extend(validate_claim_evidence(item, manifest_path, skill_name, source_path))
    return issues


def build_report(manifest_path: Path, scheme_id: str) -> dict[str, Any]:
    issues: list[str] = []
    manifest = load_json(manifest_path)
    if scheme_id and str(manifest.get("scheme_id") or "") != scheme_id:
        issues.append(f"manifest.scheme_id must be {scheme_id}")
    if not str(manifest.get("source_policy") or "").strip():
        issues.append("manifest.source_policy is required")
    copy_mode = str(manifest.get("copy_mode") or "").strip()
    if copy_mode != "source_quoted_or_source_paraphrase":
        issues.append("manifest.copy_mode must be source_quoted_or_source_paraphrase")
    source_scan = manifest.get("source_scan")
    if not isinstance(source_scan, list) or not source_scan:
        issues.append("manifest.source_scan must contain at least one source")
    items = manifest.get("items")
    if not isinstance(items, list) or not items:
        issues.append("manifest.items must contain at least one Skill row")
        items = []
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            issues.append(f"item {index} must be an object")
            continue
        issues.extend(validate_item(item, manifest_path))

    return {
        "status": "passed" if not issues else "failed",
        "manifest": str(manifest_path),
        "scheme_id": scheme_id,
        "item_count": len(items),
        "blocking_issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate source-backed Skill rows before Scheme 1 rendering.")
    parser.add_argument("--manifest", required=True, help="internal/skill_source_manifest.json")
    parser.add_argument("--scheme-id", default="scheme_1_skill_recommendation_no_voice")
    parser.add_argument("--out", help="Optional report path")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    report = build_report(manifest_path, args.scheme_id)
    out = Path(args.out) if args.out else manifest_path.with_name("skill_source_manifest_check.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
