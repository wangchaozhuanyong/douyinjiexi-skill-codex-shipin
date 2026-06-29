# Script Quality Rules

Write Chinese spoken copy for a smart beginner, not a professional article.

## Preferred Structure

1. Visible result and pain in the first 5 seconds.
2. Wrong common method with a concrete example.
3. Correct method in three copyable actions.
4. Demonstration proof.
5. Reusable template, checklist, or decision rule.
6. Summary reminder.

## Beginner Director Fields

Before writing the full script, lock these fields:

- `target_viewer`: who will click
- `task`: what they want to finish
- `visible_result`: what appears early on screen
- `why_watch_now`: why this matters now
- `first_action`: what they should do first
- `time_saving_claim`: which step, minute, or repeated edit is saved
- `problem_examples`: the exact bad request, vague output, messy material, or repeated manual step that proves the problem

## Required Scores

Use `scripts/score_script.py`.

- `first_3_seconds_score >= 9.2`
- `first_5_seconds_score >= 9.0`
- `script_score >= 8.5`
- `save_value_score >= 8.5`
- `proof_score >= 8.5`
- `compliance_score >= 9.5`
- `empty_talk_ratio <= 0.18`
- The first 3 seconds must show a clear pain point, result, or counterintuitive claim.
- Every 6-8 seconds needs a retention beat, such as a before/after reveal, proof wall, real UI action, mistake correction, or reusable template.
- Empty phrases like `提升效率`, `很方便`, and `很强` need proof on screen.
- After keyword scoring, run `scripts/evaluate_copy_semantic.py`.
- `semantic_review.composite_score >= 8.5` and `hard_fail_reasons` must be empty. The semantic review also checks content alignment: repeated information jobs, unsourced claims, and non-essential English visible text are hard failures.
- Run `scripts/check_content_alignment.py` before storyboard and again with storyboard. `content_alignment_report.status` must be `passed`.
- After semantic review, run `scripts/validate_beginner_copy.py`.
- `beginner_value_review.total_score >= 8.8`, `title_clarity >= 9.0`, `first_5_seconds_pull >= 9.0`, `visible_result >= 8.5`, `step_by_step_value >= 8.5`, and `problem_example_score >= 8.5`.

## Problem Examples

Whenever the script names a problem, add an example before explaining the fix.

Good:

- `比如你只写“帮我写一条产品文案”，输出就会变成“品质好、体验好”这种套话。`
- `比如老板给你三段会议记录，不要一段段复制，先让 AI 分成问题、结论、待办。`

Reject:

- `很多人不会写文案。`
- `新手提示词写得不好。`
- `这个问题会影响效率。`

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

## Required Copy Package Fields

`copy_package.json` must include:

- `beginner_task_card`
- `problem_examples`
- `before_after_plan`
- `empty_talk_risk`
- `terminology_explained`
- `proof_visual_plan`
- `content_alignment_map`: each claim/copy line maps to `source_ids`, `scene_id`, `visual_job`, and allowed Chinese on-screen text
- `copy_progression_plan`: each scene has exactly one `new_information_job`; do not repeat a result explanation from the previous scene unless it is an explicit proof/example with new evidence

## Hard Beginner Fails

- The title does not name a viewer, task, or visible result.
- The first 5 seconds do not show a result, pain, or contrast.
- The script names a problem but gives no concrete example.
- The script explains AI news without saying what a beginner should do next.
- The script says `提升效率`, `很强`, or `很方便` without a visible before/after proof.
- The script has no tutorial, checklist, template, decision rule, or before/after result.
- A scene repeats the previous scene's result/explanation instead of adding new information.
- A visual scene cannot answer which claim or source-backed copy line it supports.
- Visible text is mostly English without an official product/model/API/UI exception.
