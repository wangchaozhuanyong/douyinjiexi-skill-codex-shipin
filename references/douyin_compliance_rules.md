# Douyin Compliance Rules

Compliance is broader than keyword scanning. Use `scripts/check_public_copy.py` to produce `compliance_report.json`.

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
- No compliance report means no image generation, TTS, HyperFrames, video render, final delivery, or publishing.

## Safer Phrasing

Prefer practical, non-guaranteed phrases:

- `适合`
- `可以`
- `建议`
- `更容易`
- `更清楚`
- `减少重复步骤`
- `结合实际情况`
