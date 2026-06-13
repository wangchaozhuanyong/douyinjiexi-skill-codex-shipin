# Topic Selection Rules

The first quality gate is topic quality. Do not write copy before topic research.

## Mode Requirement

Use the right topic source for the user input:

- If the user provides a reference video/link/share text/local video, topic research starts from that reference. Extract the reference's topic angle, hook, structure, audience pain, visual rhythm, and comment/save trigger before proposing an original version.
- If the user only asks to "use the skill to make a video" and gives no reference, topic research must start from current AI-circle hot topics and high-quality source material. Do not default to a stale evergreen explanation or a Codex-only topic.

For self-researched videos, collect current material before scoring candidates:

- Search across the broad AI industry, not only Codex: OpenAI, ChatGPT, Anthropic, Claude, Google Gemini/Veo, Meta AI, xAI/Grok, AI agents, AI video generation, coding agents, enterprise AI, AI search, AI hardware, AI safety/regulation, and creator tools.
- Prefer sources with visible dates and clear evidence: official posts, docs, release notes, reputable tech/business media, demo pages, real product screens, terminal/code output, or public benchmark pages.
- Every candidate must name why the topic is timely, what source supports each important claim, and what visual evidence can appear on screen.
- If no current topic is strong enough, research again instead of falling back to a generic lesson.

## Candidate Requirements

Produce at least 5 candidates in `topic_candidates.json`. Each candidate must include:

- `topic_id`
- `title_direction`
- `core_angle`
- `content_format`
- `format_reason`
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
- `content_format` must be one of the formats in `references/content_formats.md`.
