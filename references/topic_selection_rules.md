# Topic Selection Rules

The first quality gate is topic quality. Do not write copy before topic research.

## Candidate Requirements

Produce at least 3 candidates in `topic_candidates.json`. Each candidate must include:

- `topic_id`
- `title_direction`
- `core_angle`
- `target_viewer`
- `viewer_pain`
- `why_now`
- `curiosity_gap`
- `save_reason`
- `comment_trigger`
- `visual_potential`
- `proof_assets_needed`
- `main_claims`
- `sources`
- `risk_flags`
- `scores`

AI news candidates must include source titles, URLs or local notes, visible dates when available, and which claim each source supports.

AI tool tutorial candidates must name what real UI, real recording, terminal output, product result, or official documentation can appear on screen.

## Scoring

Use `scripts/score_topic.py`.

Weighted score:

```text
total_score =
pain_score * 0.25 +
novelty_score * 0.15 +
save_score * 0.25 +
comment_score * 0.10 +
visual_score * 0.15 +
compliance_safety_score * 0.10
```

## Gates

- Total score must be at least 8.0.
- If no topic scores at least 8.0, research again.
- Do not choose generic topics such as `AI 工具推荐`, `AI 很厉害`, or `这个工具很好用`.
- Choose topics with pain, fresh angle, save value, visual proof, and low compliance risk.
