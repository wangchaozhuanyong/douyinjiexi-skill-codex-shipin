#!/usr/bin/env python3
"""Small helpers for binding reports to the artifacts they checked."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


def sha256_file(path: str | Path) -> str:
    target = Path(path)
    digest = hashlib.sha256()
    with target.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_fingerprint(path: str | Path) -> dict[str, Any]:
    target = Path(path)
    if not target.exists() or not target.is_file():
        raise FileNotFoundError(f"fingerprint target missing or not a file: {target}")
    stat = target.stat()
    return {
        "path": str(target),
        "sha256": sha256_file(target),
        "size": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }


def _iter_files(paths: Iterable[str | Path]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            files.extend(sorted(item for item in path.rglob("*") if item.is_file()))
        else:
            files.append(path)
    return files


def collect_fingerprints(paths: Iterable[str | Path]) -> dict[str, dict[str, Any]]:
    fingerprints: dict[str, dict[str, Any]] = {}
    for path in _iter_files(paths):
        fingerprints[str(path)] = file_fingerprint(path)
    return fingerprints


def write_report_with_fingerprints(report: dict[str, Any], input_paths: Iterable[str | Path]) -> dict[str, Any]:
    report["input_fingerprints"] = collect_fingerprints(input_paths)
    return report


def _candidate_keys(path: Path) -> list[str]:
    keys = [str(path)]
    try:
        keys.append(str(path.resolve()))
    except OSError:
        pass
    return list(dict.fromkeys(keys))


def _stored_fingerprint(report: dict[str, Any], path: Path) -> dict[str, Any] | None:
    fingerprints = report.get("input_fingerprints")
    if not isinstance(fingerprints, dict):
        return None
    for key in _candidate_keys(path):
        value = fingerprints.get(key)
        if isinstance(value, dict):
            return value
    # Older reports may store an absolute path while callers pass a relative one.
    wanted = str(path)
    wanted_name = path.name
    matches = [
        value
        for key, value in fingerprints.items()
        if isinstance(value, dict)
        and (str(value.get("path")) == wanted or Path(str(key)).name == wanted_name)
    ]
    return matches[0] if len(matches) == 1 else None


def verify_report_inputs(report: dict[str, Any], expected_paths: Iterable[str | Path]) -> list[str]:
    issues: list[str] = []
    if not isinstance(report.get("input_fingerprints"), dict):
        return ["report missing input_fingerprints"]
    for raw in _iter_files(expected_paths):
        path = Path(raw)
        stored = _stored_fingerprint(report, path)
        if stored is None:
            issues.append(f"missing input fingerprint: {path}")
            continue
        if not path.exists() or not path.is_file():
            issues.append(f"current input missing: {path}")
            continue
        current = file_fingerprint(path)
        if stored.get("sha256") != current["sha256"]:
            issues.append(f"stale input sha256 mismatch: {path}")
        if int(stored.get("size") or -1) != int(current["size"]):
            issues.append(f"stale input size mismatch: {path}")
    return issues


def assert_fresh_report(report_path: str | Path, expected_paths: Iterable[str | Path]) -> dict[str, Any]:
    path = Path(report_path)
    if not path.exists() or not path.is_file() or path.stat().st_size <= 0:
        raise SystemExit(f"report missing or empty: {path}")
    report = json.loads(path.read_text(encoding="utf-8"))
    issues = verify_report_inputs(report, expected_paths)
    if issues:
        raise SystemExit(f"stale report inputs for {path}:\n" + "\n".join(issues))
    return report
