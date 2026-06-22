#!/usr/bin/env python3
"""Promote a pre-publish-gated draft package into the public final folder."""

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


def required_artifact(contract: dict[str, Any], group: str, key: str = "source") -> Path:
    artifacts = contract.get("artifacts") if isinstance(contract.get("artifacts"), dict) else {}
    record = artifacts.get(group) if isinstance(artifacts.get(group), dict) else {}
    path = Path(str(record.get(key) or ""))
    if not exists(path):
        raise SystemExit(f"publish_contract artifact {group}.{key} missing or empty: {path}")
    return path


def optional_artifact(contract: dict[str, Any], group: str, key: str) -> Path | None:
    artifacts = contract.get("artifacts") if isinstance(contract.get("artifacts"), dict) else {}
    record = artifacts.get(group) if isinstance(artifacts.get(group), dict) else {}
    raw = str(record.get(key) or "").strip()
    if not raw:
        return None
    path = Path(raw)
    return path if exists(path) else None


def require_contract_ready(contract: dict[str, Any]) -> None:
    gate = contract.get("gate") if isinstance(contract.get("gate"), dict) else {}
    if gate.get("status") != "passed":
        issues = gate.get("issues") if isinstance(gate.get("issues"), list) else []
        detail = "\n".join(str(item) for item in issues) if issues else "run scripts/pre_publish_gate.py first"
        raise SystemExit("publish_contract.gate.status must be passed before promotion\n" + detail)


def cleanup_intermediates(project: Path, final_video: Path) -> list[str]:
    removed: list[str] = []
    final = project / "final"
    if final.exists():
        for path in final.iterdir():
            if path != final_video and path.is_file():
                path.unlink()
                removed.append(str(path))

    frames = project / "assets" / "frames"
    if frames.exists() and frames.is_dir():
        shutil.rmtree(frames)
        removed.append(str(frames))

    internal = project / "internal"
    if internal.exists():
        for path in internal.glob("*draft*.mp4"):
            if path.is_file():
                path.unlink()
                removed.append(str(path))
    return removed


def promote(project: Path, contract_path: Path) -> dict[str, Any]:
    final = project / "final"
    if not exists(contract_path):
        raise SystemExit(f"publish contract missing or empty: {contract_path}")
    contract = load_json(contract_path)
    require_contract_ready(contract)
    required_artifact(contract, "metadata")
    required_artifact(contract, "cover")
    required_artifact(contract, "publish_copy")
    video_source = required_artifact(contract, "video")
    optional_artifact(contract, "cover", "vertical")
    optional_artifact(contract, "cover", "horizontal")

    final.mkdir(parents=True, exist_ok=True)
    target = final / "final.mp4"
    shutil.copy2(video_source, target)
    removed = cleanup_intermediates(project, target)
    return {
        "cleanup_status": "final_folder_mp4_only",
        "outputs": {"final.mp4": str(target)},
        "removed": removed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote pre-publish-gated draft artifacts to final/.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic>")
    parser.add_argument("--contract", help="Defaults to <project>/internal/publish_contract.json")
    parser.add_argument("--out", help="Optional promotion_report.json path")
    args = parser.parse_args()

    project = Path(args.project)
    contract = Path(args.contract) if args.contract else project / "internal" / "publish_contract.json"
    outputs = promote(project, contract)
    result = {"status": "promoted", **outputs}
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
