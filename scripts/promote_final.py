#!/usr/bin/env python3
"""Promote a QA-passed draft package into the public final folder."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if exists(path):
            return path
    return paths[0]


def require_passed(report: dict[str, Any]) -> None:
    if report.get("status") != "passed":
        raise SystemExit("qa_report.status must be passed before promotion")
    if report.get("blocking_issues"):
        raise SystemExit("qa_report.blocking_issues must be empty before promotion")
    hard_gates = report.get("hard_gates", {})
    if not hard_gates or not all(bool(value) for value in hard_gates.values()):
        raise SystemExit("all qa_report.hard_gates must be true before promotion")


def require_provider_usage_audit(report: dict[str, Any]) -> None:
    if report.get("status") != "passed":
        raise SystemExit("provider_usage_audit.status must be passed before promotion")
    if report.get("issues"):
        raise SystemExit("provider_usage_audit.issues must be empty before promotion")


def promote(project: Path, qa_report: Path, provider_audit: Path) -> dict[str, str]:
    internal = project / "internal"
    final = project / "final"
    report = load_json(qa_report)
    require_passed(report)
    if not exists(provider_audit):
        raise SystemExit(f"provider usage audit missing or empty: {provider_audit}")
    require_provider_usage_audit(load_json(provider_audit))

    sources = {
        "final.mp4": first_existing(internal / "draft.mp4", project / "draft.mp4"),
        "metadata.json": internal / "metadata.json",
        "cover.png": first_existing(internal / "cover.png", project / "cover.png"),
        "publish_copy.txt": first_existing(internal / "publish_copy.txt", project / "publish_copy.txt"),
    }
    missing = [f"{name} source missing or empty: {path}" for name, path in sources.items() if not exists(path)]
    if missing:
        raise SystemExit("\n".join(missing))

    final.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, str] = {}
    for name, source in sources.items():
        target = final / name
        shutil.copy2(source, target)
        outputs[name] = str(target)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote QA-passed draft artifacts to final/.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic>")
    parser.add_argument("--qa-report", help="Defaults to <project>/internal/qa_report.json")
    parser.add_argument("--provider-audit", help="Defaults to <project>/internal/provider_usage_audit.json")
    parser.add_argument("--out", help="Optional promotion_report.json path")
    args = parser.parse_args()

    project = Path(args.project)
    qa_report = Path(args.qa_report) if args.qa_report else project / "internal" / "qa_report.json"
    provider_audit = Path(args.provider_audit) if args.provider_audit else project / "internal" / "provider_usage_audit.json"
    if not exists(qa_report):
        raise SystemExit(f"qa report missing or empty: {qa_report}")
    outputs = promote(project, qa_report, provider_audit)
    result = {"status": "promoted", "outputs": outputs}
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
