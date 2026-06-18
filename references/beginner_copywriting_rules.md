# Beginner Copywriting Rules

This skill must write from the beginner's task, not from the AI industry's excitement.

## Core Position

The viewer does not dislike AI knowledge. The viewer dislikes AI knowledge without a use reason.

Every topic must answer:

- Who is this for?
- What task does the viewer want to finish today?
- What visible result appears in the first 5 seconds?
- What wrong method or pain makes the viewer keep watching?
- What concrete example lets the viewer recognize that pain?
- What exact steps can the viewer copy?
- What proof appears on screen?
- What can the viewer save?
- What jargon must be translated into plain Chinese?
- Why is this useful now?

## Topic Rule

Prefer `beginner task -> pain -> AI action -> visible result -> three-step tutorial`.

Do not lead with `AI product -> feature -> trend -> vague value` unless the feature becomes a beginner action within 30 seconds.

For self-researched AI news, the news is only the entry point. The body must become:

```text
one-sentence news -> who it affects -> which step it saves -> live demo -> whether a beginner should try it
```

## Title Rule

Each title must name at least two of these four fields:

- `target_viewer`: who would click
- `task`: what they want to finish
- `visible_result`: what they get after watching
- `why_watch_now`: why this matters now

Preferred title forms:

- `人群/场景 + 任务 + 结果`
- `痛点 + 方法 + 可见收益`
- `错误做法 + 正确做法 + 结果差异`

Reject titles that only say a tool is strong, explosive, useful, or trend-changing.

## First 5 Seconds Rule

The first 5 seconds must show:

- one concrete pain or wrong method
- one example of that pain, such as an actual bad request, vague output, messy table, or repeated manual step
- one visible result or before/after contrast
- a signal that this is a usable tutorial, checklist, template, or decision rule

Do not open with greetings, vague news, broad AI claims, or feature lists.

## Problem Example Rule

Do not only name a problem. Show a small example the beginner can recognize.

Use this pattern:

```text
problem -> example -> why it fails -> corrected action
```

Examples:

- `你不是不会写文案。比如你只发一句“帮我写产品文案”，它只能给你“品质好、体验好”这种套话。`
- `你不是不会整理资料。比如老板丢给你三段会议记录，你先让 AI 分成问题、结论和待办。`
- `你不是不会写标题。比如同一篇内容，先填人群、痛点和结果，再让 AI 给标题。`

Hard fail: a script says `不会`, `问题`, `错误`, `空话`, `套话`, `乱`, or `反复改`, but gives no concrete example in the same section or the next section.

## Language Rule

Translate ability language into action language:

- `多模态理解` -> `看图列卖点`
- `长上下文` -> `一次读完一大段资料`
- `Agent` -> `你给目标，它自己分步骤做`
- `代码能力` -> `帮你批量处理重复文件`
- `联网搜索` -> `先找资料再总结`

Translate vague value into concrete value:

- `提升效率` -> `少复制 3 次，少改 20 分钟`
- `降低门槛` -> `不会写提示词也能照着填`
- `优化流程` -> `先给结果，再拆步骤`

## Review Gate

Run `scripts/validate_beginner_copy.py` after `score_script.py` and `evaluate_copy_semantic.py`.

Pass requirements:

- `total_score >= 8.8`
- `title_clarity >= 9.0`
- `first_5_seconds_pull >= 9.0`
- `visible_result >= 8.5`
- `step_by_step_value >= 8.5`
- `problem_example_score >= 8.5`

Hard fail:

- title does not name a viewer, task, or result
- first 5 seconds lack pain, result, or contrast
- pain or problem is named without a concrete example
- copy explains AI news without a beginner action
- copy says `提升效率`, `很强`, or `很方便` without proof
- no tutorial, checklist, template, decision rule, or before/after result
