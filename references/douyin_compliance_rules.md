# Douyin Compliance Rules

Compliance is broader than keyword scanning. Use `scripts/check_public_copy.py` to produce `compliance_report.json`.

Global scope: this applies to every video type, including AI/tool, renovation/full-house custom, beauty portrait, and any future Douyin-oriented video. Every designed text surface and every publish-entry field must be checked, not only the final caption.

Before writing public-facing copy, first read `references/forbidden_terms_learning_bank.md` and the active records in `references/forbidden_terms_learning_bank.jsonl`. Do not draft title, caption, topics, cover text, subtitles, or on-screen text with known active risk terms.

For publish-ready Douyin videos, this local report is not enough by itself. The exact title, publish caption, and hashtags/topics must also pass Qingdou (`轻抖`) or the current approved Douyin sensitivity checker before `promote_final.py`, upload, or publishing. Record the result in `internal/qingdou_keyword_check.json`; if the checker reports any forbidden or sensitive term, rewrite naturally and rerun until the final result is `未检查到敏感词`.

Before building `internal/publish_contract.json`, the local text compliance report must also include cover text from `internal/publish_cover_text.txt`. `scripts/pre_publish_gate.py` is the final local hard gate: it validates QA, provider audit, Qingdou, cover QA, and text compliance before `promote_final.py` can copy anything into `final/`.

Narrow exception: if Qingdou only flags a user-required official/platform campaign topic and the user explicitly says to keep that exact topic after seeing the failed result, record `status: "user_override_accepted"`, the failed term, the exact topic, the user approval, and a risk note. This exception may continue upload/publishing for that topic only. Do not use it for title, caption body, cover, subtitles, on-screen text, contact info, guarantees, station-out diversion, or any non-topic sensitive term.

Whenever local checks, Qingdou, Douyin upload, or manual review detects a forbidden/sensitive/risky term, record the exact term before rewriting:

```bash
python3 scripts/update_forbidden_terms.py \
  --report outputs/demo/internal/compliance_report.json \
  --report outputs/demo/internal/qingdou_keyword_check.json \
  --out outputs/demo/internal/forbidden_terms_update_report.json
```

The learned bank is part of the next copywriting preflight. Future scripts must avoid active learned terms before first draft, not only after a failed publish check.

## Check Categories

- Absolute or exaggerated wording.
- Guaranteed result wording.
- False authority.
- Induced engagement.
- Station-out diversion.
- Contact information.
- QR code requests.
- Risky marketing.
- Copying or low-originality risk.
- Low-quality content risk.
- AI-generated content disclosure risk.
- Factual claim without source.

## Gates

- `summary.error_count` must be 0.
- Warnings require an explanation in `compliance_report.json`.
- Any detected forbidden/sensitive/risky term must be appended to `references/forbidden_terms_learning_bank.jsonl` or explained in `forbidden_terms_update_report.json` if already present.
- No compliance report means no image generation, TTS, HyperFrames, video render, final delivery, or publishing.
- A `qingdou_keyword_check.json` manual override is acceptable only for the narrow user-required official/platform topic case above, and must not be represented as `passed`.
- A `publish_contract.json` with `gate.status != "passed"` means no upload, no publish, and no `final/` promotion.

## Safer Phrasing

Prefer practical, non-guaranteed phrases:

- `适合`
- `可以`
- `建议`
- `更容易`
- `更清楚`
- `减少重复步骤`
- `结合实际情况`
