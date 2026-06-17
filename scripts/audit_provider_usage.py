#!/usr/bin/env python3
"""Audit runtime and provider usage for AI explainer video projects."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROVIDERS = [
    "hyperframes",
    "ffmpeg",
    "remotion",
    "imagegen",
    "browser_visual_review",
    "openmontage",
    "video_use",
    "manim",
    "github",
    "hugging_face",
    "openai_developers",
    "heygen",
]

FINAL_REQUIRED = {"hyperframes", "ffmpeg", "browser_visual_review"}
OPTIONAL_ADAPTERS = {"openmontage", "video_use", "manim"}
OPTIONAL_CODEX_PLUGINS = {"github", "hugging_face", "openai_developers", "heygen"}
PRODUCTION_STACK_TRIGGER_TERMS = ["codex", "skill", "插件", "plugin", "heygen"]
PLUGIN_TRIGGER_TERMS = [
    "插件",
    "plugin",
    "plugins",
    "browser",
    "github",
    "hugging face",
    "huggingface",
    "openai developers",
    "heygen",
]
SIX_PLUGIN_TERMS = ["6 个", "6个", "六个", "six"]
CORE_CODEX_PLUGINS = {
    "browser": {"browser"},
    "github": {"github"},
    "hugging face": {"hugging face", "huggingface"},
    "hyperframes": {"hyperframes"},
    "openai developers": {"openai developers", "openai developer", "openai"},
    "heygen": {"heygen"},
}
PLUGIN_AVAILABILITY = {
    "available_in_session",
    "available_if_authenticated",
    "local_cli_or_skill",
    "needs_user_approval",
    "optional_blocked",
    "not_available",
}
FREE_FIRST_POLICY = "free_first_local_or_authorized_openai_only"


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists() or path.stat().st_size == 0:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def lower_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True).lower()


def exists(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def add_evidence(evidence: list[str], label: str, path: Path) -> None:
    if exists(path):
        evidence.append(f"{label}: {path}")


def provider_record(
    decision: str,
    available: bool,
    can_improve: bool,
    reason: str,
    evidence: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "decision": decision,
        "available": available,
        "can_improve": can_improve,
        "reason": reason,
        "evidence": evidence or [],
    }


def project_paths(project: Path) -> dict[str, Path]:
    internal = project / "internal"
    return {
        "internal": internal,
        "storyboard": internal / "storyboard.json",
        "metadata": internal / "metadata.json",
        "asset_manifest": internal / "asset_manifest.json",
        "asset_validation": internal / "asset_validation.json",
        "video_technical_qa": internal / "video_technical_qa.json",
        "frame_review": internal / "frame_review_report.json",
        "visual_review": internal / "visual_review.json",
        "qa_report": internal / "qa_report.json",
        "draft": internal / "draft.mp4",
        "final": project / "final" / "final.mp4",
    }


def assets_by_provider(assets: list[dict[str, Any]], terms: list[str]) -> list[dict[str, Any]]:
    matched: list[dict[str, Any]] = []
    for asset in assets:
        text = lower_json(
            {
                "provider": asset.get("provider"),
                "source": asset.get("source"),
                "source_note": asset.get("source_note"),
                "type": asset.get("type"),
            }
        )
        if any(term in text for term in terms):
            matched.append(asset)
    return matched


def production_stack_mentions(storyboard: dict[str, Any], terms: list[str]) -> bool:
    stack = storyboard.get("production_stack", {})
    return any(term in lower_json(stack) for term in terms)


def production_stack_has_tool(storyboard: dict[str, Any], terms: list[str]) -> bool:
    stack = storyboard.get("production_stack", {})
    tools = stack.get("primary_tools", []) if isinstance(stack, dict) else []
    if not isinstance(tools, list):
        return False
    for tool in tools:
        if not isinstance(tool, dict):
            continue
        text = lower_json({"name": tool.get("name"), "role": tool.get("role")})
        chain = tool.get("evidence_chain") or tool.get("proof_chain")
        has_chain = isinstance(chain, dict) and all(
            str(chain.get(key, "")).strip()
            for key in ["entry_or_source", "operation_or_step", "output_or_result", "viewer_value"]
        )
        if has_chain and any(term in text for term in terms):
            return True
    return False


def codex_plugin_plan_mentions(storyboard: dict[str, Any], terms: list[str]) -> bool:
    plan = storyboard.get("codex_plugin_plan", {})
    return any(term in lower_json(plan) for term in terms)


def normalize_plugin_name(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", " ").replace("_", " ")


def plugin_plan_required(project_text: str) -> bool:
    return any(term in project_text for term in PLUGIN_TRIGGER_TERMS)


def six_plugin_plan_required(project_text: str) -> bool:
    return ("插件" in project_text or "plugin" in project_text) and any(term in project_text for term in SIX_PLUGIN_TERMS)


def validate_codex_plugin_plan(storyboard: dict[str, Any], project_text: str) -> dict[str, Any]:
    required = plugin_plan_required(project_text)
    six_required = six_plugin_plan_required(project_text)
    plan = storyboard.get("codex_plugin_plan")
    issues: list[str] = []
    plugin_names: list[str] = []
    approval_text = ""

    if not isinstance(plan, dict):
        if required:
            issues.append("storyboard.codex_plugin_plan is required for plugin/tool workflow videos")
        return {
            "required": required,
            "exists": False,
            "six_required": six_required,
            "plugin_names": plugin_names,
            "approval_text": approval_text,
            "issues": issues,
        }

    if not str(plan.get("use_case", "")).strip():
        issues.append("codex_plugin_plan.use_case is required")

    plugins = plan.get("plugins", [])
    if not isinstance(plugins, list) or not plugins:
        issues.append("codex_plugin_plan.plugins must list plugin decisions")
        plugins = []

    blocked_plugins = plan.get("blocked_plugins", [])
    approval_required_for = plan.get("approval_required_for", [])
    if not isinstance(blocked_plugins, list):
        issues.append("codex_plugin_plan.blocked_plugins must be an array")
    if not isinstance(approval_required_for, list):
        issues.append("codex_plugin_plan.approval_required_for must be an array")
        approval_required_for = []
    approval_text = " ".join(str(item).lower() for item in approval_required_for)

    for index, plugin in enumerate(plugins, start=1):
        if not isinstance(plugin, dict):
            issues.append(f"codex_plugin_plan.plugins[{index}] must be an object")
            continue
        name = normalize_plugin_name(plugin.get("name"))
        plugin_names.append(name)
        availability = str(plugin.get("availability", "")).strip()
        allowed_by_default = plugin.get("allowed_by_default")
        evidence_required = plugin.get("evidence_required", [])
        if not name:
            issues.append(f"codex_plugin_plan.plugins[{index}] missing name")
        if availability not in PLUGIN_AVAILABILITY:
            issues.append(f"codex_plugin_plan.plugins[{index}] availability is unsupported")
        if not str(plugin.get("role", "")).strip():
            issues.append(f"codex_plugin_plan.plugins[{index}] missing role")
        if not isinstance(allowed_by_default, bool):
            issues.append(f"codex_plugin_plan.plugins[{index}] allowed_by_default must be boolean")
        if not isinstance(evidence_required, list) or not any(str(item).strip() for item in evidence_required):
            issues.append(f"codex_plugin_plan.plugins[{index}] evidence_required must list proof artifacts")
        if not str(plugin.get("cost_or_auth_boundary", "")).strip():
            issues.append(f"codex_plugin_plan.plugins[{index}] missing cost_or_auth_boundary")
        if not str(plugin.get("fallback", "")).strip():
            issues.append(f"codex_plugin_plan.plugins[{index}] missing fallback")
        if availability in {"needs_user_approval", "optional_blocked", "not_available"} and allowed_by_default is True:
            issues.append(f"codex_plugin_plan plugin {plugin.get('name')} cannot be allowed_by_default when blocked or approval-required")
        if "heygen" in name:
            if allowed_by_default is True:
                issues.append("HeyGen must not be allowed_by_default")
            if availability != "not_available" and "heygen" not in approval_text:
                issues.append("codex_plugin_plan.approval_required_for must mention HeyGen when HeyGen is part of the plan")

    if six_required:
        missing: list[str] = []
        for canonical, aliases in CORE_CODEX_PLUGINS.items():
            if not any(any(alias in plugin_name for alias in aliases) for plugin_name in plugin_names):
                missing.append(canonical)
        if missing:
            issues.append("six-plugin Codex videos must document these plugins: " + ", ".join(missing))

    return {
        "required": required,
        "exists": True,
        "six_required": six_required,
        "plugin_names": plugin_names,
        "approval_text": approval_text,
        "issues": issues,
    }


def audit_project(project: Path, phase: str) -> dict[str, Any]:
    paths = project_paths(project)
    storyboard = load_json(paths["storyboard"])
    metadata = load_json(paths["metadata"])
    manifest = load_json(paths["asset_manifest"])
    qa_report = load_json(paths["qa_report"])
    visual_review = load_json(paths["visual_review"])
    frame_review = load_json(paths["frame_review"])
    video_technical_qa = load_json(paths["video_technical_qa"])

    quality_spec = metadata.get("quality_spec") if isinstance(metadata.get("quality_spec"), dict) else {}
    storyboard_quality_spec = storyboard.get("quality_spec") if isinstance(storyboard.get("quality_spec"), dict) else {}
    runtime_choice = str(quality_spec.get("runtime_choice") or storyboard.get("quality_spec", {}).get("runtime_choice") or "").lower()
    assets = manifest.get("assets", []) if isinstance(manifest.get("assets"), list) else []
    project_text = lower_json(
        {
            "storyboard": storyboard,
            "metadata": metadata,
            "asset_manifest": manifest,
            "qa_report": qa_report,
        }
    )
    storyboard_text = lower_json(storyboard)

    providers: dict[str, dict[str, Any]] = {}
    structural_issues: list[str] = []
    plugin_plan = validate_codex_plugin_plan(storyboard, project_text)
    structural_issues.extend(plugin_plan["issues"])

    metadata_provider_policy = quality_spec.get("provider_policy")
    storyboard_provider_policy = storyboard.get("target", {}).get("provider_policy") or storyboard_quality_spec.get("provider_policy")
    if metadata_provider_policy != FREE_FIRST_POLICY:
        structural_issues.append("metadata.quality_spec.provider_policy must be free_first_local_or_authorized_openai_only")
    if storyboard_provider_policy != FREE_FIRST_POLICY:
        structural_issues.append("storyboard target/quality_spec provider_policy must be free_first_local_or_authorized_openai_only")
    if "hyperframes" not in runtime_choice:
        structural_issues.append("metadata/storyboard runtime_choice must document HyperFrames as final timeline")
    if not isinstance(storyboard.get("quality_spec"), dict):
        structural_issues.append("storyboard.quality_spec is missing")
    if any(term in storyboard_text for term in PRODUCTION_STACK_TRIGGER_TERMS) and not isinstance(storyboard.get("production_stack"), dict):
        structural_issues.append("storyboard.production_stack is required for AI/plugin/tutorial videos")

    if assets:
        missing_provider = [
            str(asset.get("asset_id") or index)
            for index, asset in enumerate(assets, start=1)
            if not str(asset.get("provider") or "").strip()
        ]
        missing_source_type = [
            str(asset.get("asset_id") or index)
            for index, asset in enumerate(assets, start=1)
            if not str(asset.get("asset_source_type") or "").strip()
        ]
        if missing_provider:
            structural_issues.append(f"asset provider missing: {', '.join(missing_provider[:8])}")
        if missing_source_type:
            structural_issues.append(f"asset_source_type missing: {', '.join(missing_source_type[:8])}")

    hyperframes_evidence: list[str] = []
    add_evidence(hyperframes_evidence, "storyboard", paths["storyboard"])
    add_evidence(hyperframes_evidence, "metadata", paths["metadata"])
    add_evidence(hyperframes_evidence, "draft_video", paths["draft"])
    add_evidence(hyperframes_evidence, "final_video", paths["final"])
    hyperframes_used = "hyperframes" in runtime_choice or bool(assets_by_provider(assets, ["hyperframes"]))
    providers["hyperframes"] = provider_record(
        "used" if hyperframes_used else "blocked",
        True,
        True,
        "HyperFrames is the required final timeline for premium AI explainer videos."
        if hyperframes_used
        else "HyperFrames final timeline is not documented.",
        hyperframes_evidence if hyperframes_used else [],
    )

    ffmpeg_evidence: list[str] = []
    add_evidence(ffmpeg_evidence, "video_technical_qa", paths["video_technical_qa"])
    add_evidence(ffmpeg_evidence, "frame_review", paths["frame_review"])
    ffmpeg_used = (
        "ffmpeg" in runtime_choice
        or bool(assets_by_provider(assets, ["ffmpeg", "ffprobe"]))
        or bool(video_technical_qa)
        or bool(frame_review)
    )
    providers["ffmpeg"] = provider_record(
        "used" if ffmpeg_used else "blocked",
        True,
        True,
        "FFmpeg/ffprobe evidence exists for technical QA, frame extraction, remux, or delivery checks."
        if ffmpeg_used
        else "FFmpeg/ffprobe delivery evidence is missing.",
        ffmpeg_evidence if ffmpeg_used else [],
    )

    remotion_used = production_stack_has_tool(storyboard, ["remotion"]) or bool(assets_by_provider(assets, ["remotion"]))
    remotion_needed = any(term in project_text for term in ["data visual", "chart", "react", "component clip", "frame-accurate", "screen-recording", "remotion"])
    providers["remotion"] = provider_record(
        "used" if remotion_used else ("not_applicable" if not remotion_needed else "blocked"),
        True,
        remotion_needed,
        "Remotion is used for component/data/frame-accurate motion."
        if remotion_used
        else (
            "No component/data/frame-accurate clip requirement was detected; HyperFrames can own final motion."
            if not remotion_needed
            else "Remotion appears useful for this project but no Remotion evidence was found."
        ),
        [str(paths["storyboard"]), str(paths["asset_manifest"])] if remotion_used else [],
    )

    imagegen_assets = assets_by_provider(assets, ["imagegen", "image gen", "gpt-image-2", "gpt_image_2", "gpt image 2"])
    generated_visual_count = sum(1 for asset in assets if asset.get("type") == "generated_visual" or asset.get("asset_source_type") == "generated")
    imagegen_needed = generated_visual_count > 0 or any(term in project_text for term in ["imagegen", "image gen", "generated_visual", "support visual", "cover concept"])
    providers["imagegen"] = provider_record(
        "used" if imagegen_assets else ("not_applicable" if generated_visual_count == 0 else "blocked"),
        True,
        imagegen_needed,
        "ImageGen/generated visual evidence exists for support visuals or cover concepts."
        if imagegen_assets
        else (
            "Project relies on proof cards/local design rather than generated support visuals."
            if generated_visual_count == 0
            else "Generated visuals exist but ImageGen/provider evidence is missing."
        ),
        [str(paths["asset_manifest"])] if imagegen_assets else [],
    )

    visual_evidence: list[str] = []
    add_evidence(visual_evidence, "frame_review", paths["frame_review"])
    add_evidence(visual_evidence, "visual_review", paths["visual_review"])
    browser_used = bool(frame_review) or bool(visual_review)
    providers["browser_visual_review"] = provider_record(
        "used" if browser_used else "blocked",
        True,
        True,
        "Visual review/frame review evidence exists."
        if browser_used
        else "No frame review or visual review evidence was found.",
        visual_evidence if browser_used else [],
    )

    optional_specs = {
        "openmontage": ["openmontage", "open montage"],
        "video_use": ["video-use", "video use", "videouse"],
        "manim": ["manim"],
    }
    for name, terms in optional_specs.items():
        used = any(term in project_text for term in terms) and bool(assets_by_provider(assets, terms))
        mentioned = any(term in project_text for term in terms)
        providers[name] = provider_record(
            "used" if used else ("not_applicable" if not mentioned else "blocked"),
            mentioned,
            mentioned,
            f"{name} evidence is present." if used else (
                f"{name} was not needed for this AI explainer."
                if not mentioned
                else f"{name} was mentioned but no local execution/output evidence was found."
            ),
            [str(paths["asset_manifest"])] if used else [],
        )

    codex_specs = {
        "github": ["github"],
        "hugging_face": ["hugging face", "huggingface"],
        "openai_developers": ["openai developers", "openai developer"],
        "heygen": ["heygen"],
    }
    for name, terms in codex_specs.items():
        # A planning note that a plugin is available is not execution evidence.
        used = bool(assets_by_provider(assets, terms)) or production_stack_has_tool(storyboard, terms)
        plan_mentioned = codex_plugin_plan_mentions(storyboard, terms)
        mentioned = used or production_stack_mentions(storyboard, terms) or plan_mentioned
        if name == "heygen" and mentioned and not used:
            decision = "blocked"
            reason = "HeyGen is mentioned but paid/account/upload use requires explicit approval and evidence."
            available = False
            can_improve = True
        else:
            decision = "used" if used else ("not_applicable" if not mentioned else "blocked")
            reason = (
                f"{name} plugin/source evidence is documented."
                if used
                else (
                    f"{name} was not relevant to this video."
                    if not mentioned
                    else f"{name} was mentioned but no plugin/source evidence was found."
                )
            )
            available = mentioned
            can_improve = mentioned
        providers[name] = provider_record(
            decision,
            available,
            can_improve,
            reason,
            [str(paths["storyboard"]), str(paths["asset_manifest"])] if used else [],
        )

    issues: list[str] = list(structural_issues)
    for name, item in providers.items():
        decision = item["decision"]
        evidence = item.get("evidence") or []
        if decision not in {"used", "blocked", "not_applicable"}:
            issues.append(f"{name}: invalid decision {decision!r}")
        if phase == "final" and name in FINAL_REQUIRED and decision != "used":
            issues.append(f"{name}: final delivery requires this provider/runtime to be used")
        if phase == "final" and decision == "used" and not evidence:
            issues.append(f"{name}: used provider/runtime needs evidence")
        if phase == "final" and item["available"] and item["can_improve"] and decision not in {"used", "blocked", "not_applicable"}:
            issues.append(f"{name}: must resolve final provider decision")
        if name in OPTIONAL_ADAPTERS | OPTIONAL_CODEX_PLUGINS and decision == "blocked":
            # Optional adapters/plugins may be blocked without failing unless the storyboard
            # claims they are part of the actual production evidence chain.
            terms = optional_specs.get(name, codex_specs.get(name, []))
            explicitly_needed = production_stack_mentions(storyboard, terms) or bool(assets_by_provider(assets, terms))
            if explicitly_needed:
                issues.append(f"{name}: mentioned but missing required evidence or approval")

    if phase == "final" and qa_report.get("status") != "passed":
        issues.append("qa_report.json is not passed")

    return {
        "project": str(project),
        "phase": phase,
        "status": "failed" if issues else "passed",
        "providers": providers,
        "qa_status": qa_report.get("status"),
        "quality_level": qa_report.get("quality_level"),
        "issues": issues,
    }


def markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Provider Usage Audit",
        "",
        f"- Status: `{report['status']}`",
        f"- Phase: `{report['phase']}`",
        f"- Project: `{report['project']}`",
        f"- QA status: `{report.get('qa_status')}`",
        f"- Quality level: `{report.get('quality_level')}`",
        "",
        "| Provider / Runtime | Decision | Available | Can improve | Evidence |",
        "| --- | --- | --- | --- | --- |",
    ]
    for name in PROVIDERS:
        item = report["providers"][name]
        lines.append(
            f"| {name} | `{item['decision']}` | `{item['available']}` | "
            f"`{item['can_improve']}` | `{len(item.get('evidence') or [])}` |"
        )
    if report["issues"]:
        lines.extend(["", "## Issues", ""])
        lines.extend(f"- {issue}" for issue in report["issues"])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit AI explainer provider/runtime usage evidence.")
    parser.add_argument("--project", required=True, help="outputs/<date-topic>")
    parser.add_argument("--phase", default="final", choices=["plan", "final"])
    parser.add_argument("--out", help="Optional JSON output path")
    parser.add_argument("--md-out", help="Optional Markdown output path")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    report = audit_project(project, args.phase)
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        out = Path(args.out).resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    if args.md_out:
        md_out = Path(args.md_out).resolve()
        md_out.parent.mkdir(parents=True, exist_ok=True)
        md_out.write_text(markdown_report(report), encoding="utf-8")
    print(text, end="")
    return 0 if report["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
