"""Shared publish-ready narration voice gates."""

from __future__ import annotations

from typing import Any


BLOCKED_SYSTEM_VOICE_TERMS = [
    "macos say",
    "macos_say",
    "mac os say",
    "local apple",
    "local_apple",
    "apple neural",
    "apple_neural",
    "apple system",
    "system voice",
    "system tts",
    "say",
    "scratch",
    "timing preview",
    "preview voice",
    "tingting",
    "婷婷",
]
APPROVAL_TEXTS = {"approved", "accepted", "user approved", "sample approved"}
LOWER_QUALITY_APPROVAL_TEXTS = {
    "explicit user approval",
    "user approved lower quality",
    "user accepted lower quality",
    "用户明确批准",
    "用户明确接受低质量",
}


def normalized_text(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", " ").replace("_", " ")


def contains_term(text: str, terms: list[str] | set[str]) -> bool:
    normalized = normalized_text(text)
    return any(normalized_text(term) in normalized for term in terms)


def voice_surface(voice: dict[str, Any]) -> str:
    keys = [
        "provider",
        "voice_id",
        "voice_name",
        "render_method",
        "generation_method",
        "engine",
        "source",
        "sample_path",
        "source_narration_path",
        "notes",
    ]
    return " ".join(str(voice.get(key, "")) for key in keys)


def is_preview_or_system_voice(voice: dict[str, Any]) -> bool:
    return contains_term(voice_surface(voice), BLOCKED_SYSTEM_VOICE_TERMS)


def has_explicit_lower_quality_approval(voice: dict[str, Any]) -> bool:
    if voice.get("explicit_lower_quality_approval") is True:
        return True
    approval_text = " ".join(
        [
            str(voice.get("approval_status", "")),
            str(voice.get("sample_approval_status", "")),
            str(voice.get("notes", "")),
        ]
    )
    return contains_term(approval_text, LOWER_QUALITY_APPROVAL_TEXTS)


def has_sample_approval(voice: dict[str, Any]) -> bool:
    if voice.get("sample_approved") is True:
        return True
    approval_text = normalized_text(voice.get("approval_status") or voice.get("sample_approval_status"))
    return approval_text in APPROVAL_TEXTS


def voice_provider_passes(metadata: dict[str, Any]) -> bool:
    """Return True only for a documented, approved publish-ready voice.

    ``qa_status=passed`` is intentionally ignored: a technical QA pass does not
    prove that the narration sounds natural or that a sample was approved.
    """
    voice = metadata.get("voice")
    if not isinstance(voice, dict):
        return False
    provider = normalized_text(voice.get("provider"))
    voice_id = str(voice.get("voice_id", "")).strip()
    if not provider or not voice_id:
        return False
    if is_preview_or_system_voice(voice) and not has_explicit_lower_quality_approval(voice):
        return False
    return has_sample_approval(voice)
