#!/usr/bin/env python3
"""Validate the premium foreground parent/micro component libraries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_ART_V1 = ROOT / "references" / "foreground_art_module_library_v1.md"
DEFAULT_ART_V2_MD = ROOT / "references" / "foreground_art_module_library_v2.md"
DEFAULT_ART_V2_JSON = ROOT / "references" / "foreground_art_module_library_v2.json"
DEFAULT_MICRO_MD = ROOT / "references" / "foreground_micro_component_library_v1.md"
DEFAULT_MICRO_JSON = ROOT / "references" / "foreground_micro_component_library_v1.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def expected_ids(prefix: str, count: int) -> list[str]:
    return [f"{prefix}{index:02d}" for index in range(1, count + 1)]


def require_file(path: Path, issues: list[str]) -> bool:
    if not path.exists() or not path.is_file() or path.stat().st_size == 0:
        issues.append(f"missing or empty file: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
        return False
    return True


def validate(args: argparse.Namespace) -> dict[str, Any]:
    art_v1 = Path(args.art_v1)
    art_v2_md = Path(args.art_v2_md)
    art_v2_json = Path(args.art_v2_json)
    micro_md = Path(args.micro_md)
    micro_json = Path(args.micro_json)

    issues: list[str] = []
    warnings: list[str] = []
    signals: dict[str, Any] = {}

    for path in [art_v1, art_v2_md, art_v2_json, micro_md, micro_json]:
        require_file(path, issues)
    if issues:
        return {"status": "failed", "blocking_issues": issues, "warnings": warnings, "signals": signals}

    art_v1_text = art_v1.read_text(encoding="utf-8")
    art_v2_text = art_v2_md.read_text(encoding="utf-8")
    micro_text = micro_md.read_text(encoding="utf-8")
    art_data = load_json(art_v2_json)
    micro_data = load_json(micro_json)

    v1_numbered = [f"{index:02d}." for index in range(1, 21)]
    missing_v1 = [marker for marker in v1_numbered if marker not in art_v1_text]
    if missing_v1:
        issues.append(f"v1 art module descriptions missing markers: {missing_v1}")
    if "增量补充" not in art_v2_text or "module_id" not in art_v2_text:
        issues.append("v2 art markdown must declare additive module_id execution rules")
    if "禁止独立成页" not in micro_text or "C01–C30" not in micro_text:
        issues.append("micro markdown must declare C01-C30 and no standalone-page rule")

    modules = art_data.get("modules") if isinstance(art_data.get("modules"), list) else []
    module_ids = [str(item.get("module_id") or "") for item in modules if isinstance(item, dict)]
    signals["art_module_count"] = len(modules)
    if module_ids != expected_ids("M", 20):
        issues.append(f"art module ids must be M01-M20 in order; got {module_ids}")
    if art_data.get("library", {}).get("real_3d_dependency_allowed") is not False:
        issues.append("art module library must set real_3d_dependency_allowed=false")
    transition_ids = sorted((art_data.get("transitions") or {}).keys())
    signals["transition_ids"] = transition_ids
    if transition_ids != expected_ids("TR", 8):
        issues.append(f"transition ids must be TR01-TR08; got {transition_ids}")
    for module in modules:
        module_id = module.get("module_id")
        for key in ["layout", "selection", "text_limits", "implementation", "qa_hard_fail", "transition_ids"]:
            if not module.get(key):
                issues.append(f"{module_id} missing required art execution field: {key}")

    components = micro_data.get("components") if isinstance(micro_data.get("components"), list) else []
    component_ids = [str(item.get("component_id") or "") for item in components if isinstance(item, dict)]
    signals["micro_component_count"] = len(components)
    if component_ids != expected_ids("C", 30):
        issues.append(f"micro component ids must be C01-C30 in order; got {component_ids}")
    library = micro_data.get("library") if isinstance(micro_data.get("library"), dict) else {}
    if library.get("standalone_page_allowed") is not False:
        issues.append("micro component library must set standalone_page_allowed=false")
    if library.get("real_3d_dependency_allowed") is not False:
        issues.append("micro component library must set real_3d_dependency_allowed=false")
    mapping = library.get("module_id_mapping") if isinstance(library.get("module_id_mapping"), dict) else {}
    expected_mapping = {f"{index:02d}": f"M{index:02d}" for index in range(1, 21)}
    if mapping != expected_mapping:
        issues.append("micro component module_id_mapping must map 01-M01 through 20-M20")
    adapters = micro_data.get("parent_module_adapters") if isinstance(micro_data.get("parent_module_adapters"), list) else []
    adapter_ids = [str(item.get("module_id") or "") for item in adapters if isinstance(item, dict)]
    signals["parent_adapter_count"] = len(adapters)
    if adapter_ids != expected_ids("M", 20):
        issues.append(f"parent module adapters must be M01-M20 in order; got {adapter_ids}")
    ready_gate = micro_data.get("ready_gate") if isinstance(micro_data.get("ready_gate"), dict) else {}
    for gate in [
        "component_count_is_30",
        "component_id_range",
        "parent_mapping_complete",
        "no_standalone_component",
        "no_real_3d_dependency",
        "visual_and_motion_budgets_pass",
    ]:
        if gate not in ready_gate:
            issues.append(f"micro ready_gate missing {gate}")
    for component in components:
        component_id = component.get("component_id")
        for key in ["compatibility", "text_slots", "budget", "motion", "qa_hard_fail"]:
            if not component.get(key):
                issues.append(f"{component_id} missing required micro component field: {key}")
        budget = component.get("budget") if isinstance(component.get("budget"), dict) else {}
        for key in ["visual_weight", "motion_weight", "text_weight", "dominant"]:
            if key not in budget:
                issues.append(f"{component_id}.budget missing {key}")

    return {
        "status": "passed" if not issues else "failed",
        "blocking_issues": issues,
        "warnings": warnings,
        "signals": signals,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate foreground parent/micro module libraries.")
    parser.add_argument("--art-v1", default=str(DEFAULT_ART_V1))
    parser.add_argument("--art-v2-md", default=str(DEFAULT_ART_V2_MD))
    parser.add_argument("--art-v2-json", default=str(DEFAULT_ART_V2_JSON))
    parser.add_argument("--micro-md", default=str(DEFAULT_MICRO_MD))
    parser.add_argument("--micro-json", default=str(DEFAULT_MICRO_JSON))
    parser.add_argument("--out", help="Optional report path.")
    args = parser.parse_args()

    report = validate(args)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
