# AI Video Scheme Library

This file classifies repeatable AI-circle video formats. Use it after `video_style_router.md` routes the task to AI/tool/Codex content and before copywriting, storyboard, or rendering.

After a reference-led AI video is produced, update `references/ai_reference_video_outcome_registry.md` so we can count which reference styles have been successfully converted into original videos.

## Mandatory First Question

Do not start by asking "what visual style is attractive?" Start by locking the content job:

- Is the video recommending tools/skills?
- Is it teaching an operation?
- Is it explaining news/source evidence?
- Is it comparing workflows?
- Is it giving a checklist/template?
- Is it showing a production stack?

Only after the content job is locked may the visual style be chosen.

## Scheme 1: Skill Recommendation, No Voice

- Canonical name: `方案1: Skill 推荐无人声`
- Typical reference: vertical Douyin list/poster like `Codex 值得装的 10 个 Skill`
- Format: 9:16, 1080x1920, 7-10 seconds, music-led, no narration
- Content job: recommend a set of Skills/tools/plugins and state what each one does
- Best for: `10 个 Skill`, `8 个插件`, `5 个工具`, `值得先装`, `新手先看`
- Design style: clean lavender/white information poster, large headline, numbered row cards, icon tiles, Skill/tool names, right-column Chinese usage notes
- Motion style: title lift, row-by-row reveal, staggered easing, shimmer sweep, subtle background flow, readable hold
- Text rule: every row must be `name + concrete usage`, not generic action slogans
- Audio: no voice unless the reference or user requires it; use user-provided Douyin reference music for Douyin-to-Douyin publishing when technically possible
- Renderer: HyperFrames if available; otherwise a deterministic local poster renderer is allowed for this narrow family if text manifest, QA, and originality are recorded
- Required manual: `references/ai_video_scheme_1_skill_recommendation_no_voice.md`

## Scheme 2: Source-Led AI Tool Tutorial

- Format: usually 16:9, 1920x1080, 45-75 seconds, voice-led
- Content job: teach how to use one AI tool or Codex workflow with proof
- Best for: tutorial, operation walkthrough, coding agent workflow, browser/GitHub/OpenAI docs explanation
- Design style: real UI/source crop, task brief panel, proof rail, operation tray, result card
- Motion style: source focus reveal, cursor/task packet relay, terminal/browser proof tray, keyword-only caption highlights
- Evidence rule: each important claim needs source/proof or must be written as opinion/advice

## Scheme 3: AI News To Beginner Action

- Format: usually 16:9, 1920x1080, 45-60 seconds, voice-led
- Content job: convert a recent AI update into one beginner action, checklist, or decision rule
- Best for: OpenAI/Anthropic/Google/Meta/xAI/product release/news analysis
- Design style: source wall, date/source label, implication card, beginner action template
- Motion style: citation rail wipe, comparison split, final template settle
- Evidence rule: source date and source type must be visible; do not turn news into hype without action

## Scheme 4: Multi-Skill / Production Stack Explainer

- Format: usually 16:9, 1920x1080, 60-90 seconds, voice-led
- Content job: show how several skills/plugins/tools cooperate
- Best for: `ImageGen + Remotion + HyperFrames`, Codex plugins, production system comparisons
- Design style: tool stack map, chapter cards, real operation proof for each named tool
- Motion style: node relay, chapter handoff, proof tray per tool, final stack summary
- Evidence rule: every named tool needs entry/source proof, operation proof, output proof, and viewer-value proof

## Scheme 5: Checklist / Mistake / Template Poster

- Format: 9:16 or 16:9 depending on proof needs; 8-25 seconds if poster-led, 30-60 seconds if narrated
- Content job: give a saveable checklist, mistakes list, or prompt template
- Best for: `5 个避坑`, `3 步流程`, `小白检查表`, `提示词模板`
- Design style: checklist rows, wrong/right chips, before/after mini cards
- Motion style: row reveal, risk chip lock, template lift settle
- Evidence rule: if it claims results or platform rules, add source or soften as advice

## Scheme 6: Operation Proof / Test Result Short

- Format: usually 16:9, 1920x1080, 20-45 seconds, may be voice-led or caption-led
- Content job: prove an operation actually ran
- Best for: code change, browser test, terminal output, CI/lint/test/build result, before/after UI proof
- Design style: repo/file tree, terminal/test output, browser result, proof badge
- Motion style: cursor trace, proof tray slide, pass/fail chip settle
- Evidence rule: no fake terminal, no tiny unreadable proof panels

## Selection Rule

If a user gives a reference video, classify it into one of these schemes before writing text:

- If the reference is a short vertical list of recommended Skills/tools and has no narration, choose Scheme 1.
- If readable UI/docs/source proof is central, choose Scheme 2 or 6 and keep 16:9.
- If the topic starts from recent industry news, choose Scheme 3.
- If multiple tools/skills are the subject, choose Scheme 4.
- If the deliverable is mostly a saveable list/template, choose Scheme 5.

When uncertain, write the classification and why. Do not proceed to rendering until the content job and scheme are locked.

## Outcome Tracking

Every reference-led AI production must write one registry entry after QA:

- `scheme`
- `reference_source`
- `content_job_lock`
- `output_project`
- `final_or_candidate_video`
- `qa_status`
- `publish_status`
- `lessons`

Use the registry to decide which scheme becomes a main production direction. A scheme should be treated as a primary option only after it has at least one usable output, clear QA evidence, and a repeatable production method.
