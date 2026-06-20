#!/usr/bin/env python3
"""Audit that reference videos are used as candidates, not templates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FORBIDDEN_TERMS = ["frame", "subtitle", "wording", "voice", "sequence"]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit(selection: dict[str, Any], recipe: dict[str, Any] | None = None) -> list[str]:
    issues: list[str] = []
    if selection.get("status") not in {"passed", "locked"}:
        issues.append("director_selection.json status must be passed or locked")
    policy = selection.get("reference_policy") if isinstance(selection.get("reference_policy"), dict) else {}
    cards = policy.get("selected_reference_cards", [])
    if not isinstance(cards, list) or not cards:
        issues.append("reference_policy.selected_reference_cards must contain at least one reference card")
    if len(cards) > 3:
        issues.append("selected reference cards should be limited to at most three per video")
    if policy.get("latest_reference_is_not_default") is not True:
        issues.append("latest_reference_is_not_default must be true")
    forbidden_blob = " ".join(str(item).lower() for item in policy.get("forbidden_copying", []))
    for term in REQUIRED_FORBIDDEN_TERMS:
        if term not in forbidden_blob:
            issues.append(f"reference_policy.forbidden_copying must mention {term}")
    scope = str(policy.get("reference_scope", "")).lower()
    if "learn" not in scope or "copy" in scope.replace("not copy", ""):
        issues.append("reference_scope must say the reference is learned, not copied")

    components = selection.get("component_mix", [])
    component_ids = [item.get("id") for item in components if isinstance(item, dict)]
    if len(set(component_ids)) < 4:
        issues.append("component_mix must contain at least four distinct components")
    if not selection.get("cooldown_policy"):
        issues.append("cooldown_policy must be documented")
    if not str(selection.get("why_selected", "")).strip():
        issues.append("why_selected must explain the current content job")
    if not selection.get("why_not_other_schemes"):
        issues.append("why_not_other_schemes must document rejected alternatives")

    if recipe:
        recipe_components = recipe.get("component_ids", [])
        if len(set(recipe_components)) < 4:
            issues.append("style_recipe.component_ids must contain at least four distinct components")
        if not recipe.get("style_inheritance"):
            issues.append("style_recipe must document style inheritance across the whole video")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit reference overfit risk.")
    parser.add_argument("--director-selection", required=True)
    parser.add_argument("--style-recipe")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    selection = load_json(Path(args.director_selection))
    recipe = load_json(Path(args.style_recipe)) if args.style_recipe and Path(args.style_recipe).exists() else None
    issues = audit(selection, recipe)
    report = {
        "status": "passed" if not issues else "failed",
        "blocking_issues": issues,
        "summary": "Reference cards are treated as selectable style candidates, not copied templates." if not issues else "Reference overfit risk detected.",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "issue_count": len(issues)}, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
