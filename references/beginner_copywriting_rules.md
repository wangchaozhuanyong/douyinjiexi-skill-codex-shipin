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

## Single Topic Spine Rule

Every short AI explainer must have one clear task spine:

```text
one viewer -> one daily task -> one pain example -> one AI action -> one visible result -> one saveable method
```

Do not put two practical topics into one video. If the first half teaches `把重复流程录成可复用规则`, the ending must not switch to `AI 做到一半断了怎么续做`. If the first half explains a new feature release, the body must still keep one beginner task as the main spine. News/source, tool name, and feature name are only context; they cannot become a second topic.

Hard fail symptoms:

- the title names one task, but the ending gives a different task
- the hook says the viewer will learn a workflow, but the conclusion gives a prompt for another problem
- `Record & Replay`, `Skill`, `Agent`, `工作流`, `断点续做`, `提示词`, or `自动化` appear as separate concepts instead of one simple action
- a viewer cannot answer within 5 seconds: "This video teaches me to do what?"

Fix pattern:

```text
Today I teach: <one practical task>.
Use case: <one concrete daily scene>.
Wrong method: <one recognizable bad example>.
Correct method: <three copyable steps>.
Save line: <one sentence the viewer can reuse tomorrow>.
```

## Topic Rule

Prefer `beginner task -> pain -> AI action -> visible result -> three-step tutorial`.

Do not lead with `AI product -> feature -> trend -> vague value` unless the feature becomes a beginner action within 30 seconds.

For self-researched AI news, the news is only the entry point. The body must become:

```text
one-sentence news -> who it affects -> which step it saves -> live demo -> whether a beginner should try it
```

## Title Rule

For AI news, AI tools, ChatGPT, Codex, Gemini, model, website, plugin, or workflow videos, the title must first name the concrete object/source and hook:

- object/source: software, website, company, model, product feature, release, official doc, or news event
- hook: what changed, what was released, what feature/page is being used, or what source is being explained
- takeaway: what the beginner can do after watching

Do not start from a pure method title. `用 ChatGPT 和 Codex 前先写边界清单` is not clear enough because the viewer does not know which feature/news/source caused the topic. Use `ChatGPT 新增应用调用确认：用 Codex 前先写三层边界清单` or another source-led version.

Each title must also name at least two of these four fields:

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

Mandatory opening shape for practical AI tips:

```text
viewer scene -> wrong method -> bad result -> correct method -> visible result
```

For example:

```text
你做视频流程每天都要重讲吗？
错误做法：只说“照上次做”。
结果是 AI 漏查标题、文案和话题。
正确做法：把一套流程录下来。
下次输出检查结果。
```

The tool or product name may appear after the conflict is clear. Do not make the first line a feature name, release name, or abstract concept. If a viewer cannot explain the video topic after the first 5 seconds, the script is not ready for storyboard, images, TTS, render, or publishing.

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
