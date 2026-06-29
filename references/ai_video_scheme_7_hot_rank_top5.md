# AI Hot Rank TOP5 Scheme

Canonical label: `方案7: AI 热榜 TOP5 榜单`

Use this when the user asks for `AI 热榜 TOP5`, `AI 热榜`, `TOP5`, `榜单`, `排行`, `排名`, `5 个 AI 更新`, or a reference video whose content job is a ranked current AI news/tool/model list.

If the user asks for a beginner Skill/tool/plugin recommendation list, or says the video should explain what each Skill can achieve, route to `方案1: Skill 推荐无人声` instead. A TOP5 visual surface alone is not enough to choose this Scheme 7 news workflow.

## Content Job Lock

The job is to rank five current AI signals from real sources and make each item useful to a viewer.

Do not drift into:

- one-topic news explainer
- generic AI trend commentary
- unranked checklist
- pure tool recommendation without current-source evidence
- Skill recommendation where the main job is `what this Skill does`
- absolute platform ranking claims

## Required Inputs

Before copywriting or rendering, create:

- `internal/hot_rank_scan_report.md`
- `internal/ai_hot_rank_top5.json`
- `internal/director_selection.json` with `scheme.id="scheme_7_ai_hot_rank_top5"`
- `internal/style_recipe.json`

Each ranked item must include:

- `rank`
- `title`
- `source_title`
- `source_url_or_note`
- `visible_date`
- `why_now`
- `why_it_matters`
- `viewer_action`
- `rank_score`
- `score_breakdown`
- `risk_flags`

## Ranking Formula

Use auditable scoring. A recommended default is:

- freshness: 25
- impact: 20
- practical_value: 20
- source_strength: 15
- visual_clarity: 10
- compliance_safety: 10

Total score must be `0-100`. Sort descending. If two items tie, prefer the one with stronger source strength and clearer viewer action.

## Source Rules

- Start with the task date.
- If fewer than five usable current signals exist, expand to the latest seven calendar days and record this in `hot_rank_scan_report.md`.
- Do not use sources older than seven days as ranked items unless the user explicitly asks for a weekly/monthly recap.
- A source without a visible date can be supporting context, but it cannot satisfy the ranked item evidence requirement.
- Do not say `排名第一`, `全网第一`, `最强`, or `行业第一` unless a real official ranked source proves that exact phrase. Prefer `第 1 条值得关注的是...`.

## Copy Shape

Default 9:16 no-long-explainer structure:

1. Hook: `AI 热榜 TOP5`
2. Rank 5 to Rank 2: each item gets one short row, one source/date pin, one viewer action
3. Rank 1: gets a larger emphasis module and one clear reason
4. Close: one saveable takeaway

When the user asks for a short no-voice version, target 8-12 seconds. Keep each row to a concrete object/event plus one beginner action. If the row needs more explanation than that, this is not a short no-voice TOP5; convert it to a narrated news-to-action explainer or ask for a longer duration.

Every visible row should fit this shape:

```text
No.5 | concrete AI object/event | one-line why it matters | source/date pin
```

## Visual Direction

- Use a selected dynamic MP4 background from `assets/ai_background_templates_dynamic/`.
- Use Balanced Glass foreground modules: background visible, frame visible, text readable.
- The ranking rows are information modules, not opaque cards.
- Use source/date micro-components for every item.
- Use countdown motion from 5 to 1; do not randomize order after scoring.

## Audio Direction

If a reference Douyin video contains background music, preserve the BGM when technically possible for same-platform Douyin publishing. If the exact track cannot be used, choose a similar tempo, mood, and energy bed and document:

- `reference_bgm_detected`
- `bgm_policy`
- `bgm_source`
- `substitution_reason` when applicable

If narration is used, keep BGM below voice and prove the final MP4 has an audio stream.

## QA Gates

The video cannot be final unless:

- all five rank items have source/date evidence
- `rank_score` exists for all five items
- sorting is descending by score
- public text avoids absolute ranking claims
- BGM exists when the reference had BGM
- foreground modules pass Glass Transparency checks
- Qingdou/public text gates pass before promotion or publishing
