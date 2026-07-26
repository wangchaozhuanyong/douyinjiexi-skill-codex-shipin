#!/usr/bin/env python3
"""Check renderer, media tools, and voice-provider readiness without exposing secrets."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


REQUIRED_REMOTION_PACKAGES = {"remotion", "@remotion/cli", "@remotion/media"}


def command_version(command: list[str]) -> str | None:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    output = (result.stdout or result.stderr).strip().splitlines()
    return output[0] if output else "available"


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def select_voice_provider(requested: str) -> tuple[str | None, list[str]]:
    issues: list[str] = []
    eleven_ready = bool(
        os.environ.get("ELEVENLABS_API_KEY")
        and (os.environ.get("ELEVENLABS_VOICE_ID") or os.environ.get("ELEVEN_VOICE_ID"))
    )
    edge_ready = importlib.util.find_spec("edge_tts") is not None
    if requested == "auto":
        if eleven_ready:
            return "elevenlabs", issues
        if edge_ready:
            return "edge-tts", issues
        issues.append("no configured voice provider: ElevenLabs credentials and edge_tts are unavailable")
        return None, issues
    if requested == "elevenlabs" and not eleven_ready:
        issues.append(
            "ElevenLabs requires ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID "
            "(or ELEVEN_VOICE_ID)"
        )
    if requested == "edge-tts" and not edge_ready:
        issues.append("edge-tts requires the edge_tts Python package")
    if requested == "existing":
        return "existing", issues
    return requested, issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument(
        "--voice-provider",
        choices=("auto", "elevenlabs", "edge-tts", "existing"),
        default="auto",
    )
    parser.add_argument("--out")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    out = Path(args.out).resolve() if args.out else project / "runtime" / "provider_preflight.json"
    issues: list[str] = []
    warnings: list[str] = []

    package_path = project / "package.json"
    package = load_json(package_path)
    packages = {
        *map(str, (package.get("dependencies") or {}).keys()),
        *map(str, (package.get("devDependencies") or {}).keys()),
    }
    missing_packages = sorted(REQUIRED_REMOTION_PACKAGES - packages)
    if not package:
        issues.append(f"missing or invalid package.json: {package_path}")
    if missing_packages:
        issues.append("package.json missing Remotion packages: " + ", ".join(missing_packages))

    remotion_bin = project / "node_modules" / ".bin" / "remotion"
    if not remotion_bin.is_file():
        issues.append("Remotion is declared but not installed; run npm install in the project")

    storyboard = load_json(project / "storyboard.json")
    render_plan = storyboard.get("render_plan") if isinstance(storyboard.get("render_plan"), dict) else {}
    canonical_renderer = str(render_plan.get("canonical_renderer") or "")
    if canonical_renderer != "remotion":
        issues.append("storyboard.render_plan.canonical_renderer must be remotion")

    optional_subrenderers = render_plan.get("optional_subrenderers")
    if not isinstance(optional_subrenderers, list):
        issues.append("storyboard.render_plan.optional_subrenderers must be an array")
        optional_subrenderers = []
    elif "hyperframes" in optional_subrenderers:
        hyperframes = command_version(["npx", "--yes", "hyperframes", "--version"])
        if not hyperframes:
            issues.append("HyperFrames is requested as a subrenderer but its CLI is unavailable")
    else:
        hyperframes = None

    tools = {
        "node": command_version(["node", "--version"]),
        "npm": command_version(["npm", "--version"]),
        "ffmpeg": command_version(["ffmpeg", "-version"]),
        "ffprobe": command_version(["ffprobe", "-version"]),
        "remotion": command_version([str(remotion_bin), "versions"]) if remotion_bin.is_file() else None,
        "hyperframes_optional": hyperframes,
    }
    for required in ("node", "npm", "ffmpeg", "ffprobe", "remotion"):
        if not tools[required]:
            issues.append(f"required tool unavailable: {required}")

    voice_provider, voice_issues = select_voice_provider(args.voice_provider)
    issues.extend(voice_issues)
    if voice_provider == "edge-tts":
        warnings.append("voice provider fallback is explicit: edge-tts")

    report = {
        "status": "passed" if not issues else "blocked",
        "project": str(project),
        "canonical_renderer": canonical_renderer,
        "optional_subrenderers": optional_subrenderers,
        "voice_provider": voice_provider,
        "voice_provider_requested": args.voice_provider,
        "tools": tools,
        "credentials": {
            "elevenlabs_api_key": "configured" if os.environ.get("ELEVENLABS_API_KEY") else "missing",
            "elevenlabs_voice_id": (
                "configured"
                if (os.environ.get("ELEVENLABS_VOICE_ID") or os.environ.get("ELEVEN_VOICE_ID"))
                else "missing"
            ),
        },
        "blocking_issues": sorted(set(issues)),
        "warnings": warnings,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
