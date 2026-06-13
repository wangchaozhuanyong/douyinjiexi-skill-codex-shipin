# Script Quality Rules

Write Chinese spoken copy for a smart beginner, not a professional article.

## Preferred Structure

1. Pain point opening.
2. Wrong common method.
3. Correct method.
4. Demonstration proof.
5. Reusable template, checklist, or decision rule.
6. Summary reminder.

## Required Scores

Use `scripts/score_script.py`.

- `first_5_seconds_score >= 9.0`
- `script_score >= 8.0`
- `save_value_score >= 8.0`
- `compliance_score >= 9.0`
- The first 3 seconds must show a clear pain point, result, or counterintuitive claim.
- Every 6-8 seconds needs a retention beat, such as a before/after reveal, proof wall, real UI action, mistake correction, or reusable template.
- Empty phrases like `提升效率`, `很方便`, and `很强` need proof on screen.

## Bad Openings

Reject openings like:

- `今天给大家介绍一个 AI 工具`
- `AI 时代来了`
- `你知道吗`
- `很多人不知道`
- `这个工具太强了`

## Forbidden Copy Patterns

- Guaranteed results: `必火`, `保证涨粉`, `100% 提升播放量`, `用了就能赚钱`
- Absolute claims: `全网最强`, `第一`, `唯一`
- Fake authority: `官方认证`, `专家推荐`, `国家级`, `世界级`, `权威机构认证` without proof
- Induced engagement: `不点赞就亏了`, `必须收藏`, `评论区打 1 我发你`, `点赞过多少我继续讲`

## Save Value

Every publish-ready script must include at least one of:

- A reusable prompt/template.
- A 3-step workflow.
- A checklist.
- A before/after comparison.
- A decision rule.
- A common mistake correction.

## Retention Beats

`copy_package.json` must include `retention_beats`. Each beat must name:

- `time_range`
- `type`
- `line`
- `visual`
