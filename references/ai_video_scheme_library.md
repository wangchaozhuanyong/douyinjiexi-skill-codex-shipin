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
- Content job: recommend a set of Skills/tools/plugins and state what each one does for a beginner
- Best for: `10 个 Skill`, `8 个插件`, `5 个工具`, `值得先装`, `新手先看`
- Design style: clean lavender/white information poster, large headline, numbered row cards, icon tiles, Skill/tool names, right-column Chinese usage notes
- Motion style: title lift, row-by-row reveal, staggered easing, shimmer sweep, subtle background flow, readable hold
- Text rule: every row must be `name + input/content + purpose + output/result`, compressed into plain Chinese; do not use generic action slogans
- Diversion rule: public text must not ask viewers to use a website, URL, link, QR code, private message, download, or claim path. Keep URLs only in internal evidence/source fields.
- Audio: no voice unless the reference or user requires it; use user-provided Douyin reference music for Douyin-to-Douyin publishing when technically possible, and block instead of generating/substituting BGM when the same reference music cannot be obtained
- Music policy: `required_bgm`; music drives pacing because there is no narration
- Renderer: HyperFrames if available; otherwise a deterministic local poster renderer is allowed for this narrow family if text manifest, QA, and originality are recorded
- Required manual: `references/ai_video_scheme_1_skill_recommendation_no_voice.md`

## Scheme 2: Source-Led AI Tool Tutorial

- Format: usually 16:9, 1920x1080, 45-75 seconds, voice-led
- Content job: teach how to use one AI tool or Codex workflow with proof
- Best for: tutorial, operation walkthrough, coding agent workflow, browser/GitHub/OpenAI docs explanation
- Design style: real UI/source crop, task brief panel, proof rail, operation tray, result card
- Motion style: source focus reveal, cursor/task packet relay, terminal/browser proof tray, keyword-only caption highlights
- Evidence rule: each important claim needs source/proof or must be written as opinion/advice
- Music policy: `no_bgm` by default; use narration plus light SFX so proof screens and steps stay clear

## Scheme 3: AI News To Beginner Action

- Format: usually 16:9, 1920x1080, 45-60 seconds, voice-led
- Content job: convert a recent AI update into one beginner action, checklist, or decision rule
- Best for: OpenAI/Anthropic/Google/Meta/xAI/product release/news analysis
- Design style: source wall, date/source label, implication card, beginner action template
- Motion style: citation rail wipe, comparison split, final template settle
- Evidence rule: source date and source type must be visible; do not turn news into hype without action
- Music policy: `voice_only_clean` by default; use BGM only from approved library/reference music and keep it below narration

## Scheme 4: Multi-Skill / Production Stack Explainer

- Format: usually 16:9, 1920x1080, 60-90 seconds, voice-led
- Content job: show how several skills/plugins/tools cooperate
- Best for: `ImageGen + Remotion + HyperFrames`, Codex plugins, production system comparisons
- Design style: tool stack map, chapter cards, real operation proof for each named tool
- Motion style: node relay, chapter handoff, proof tray per tool, final stack summary
- Evidence rule: every named tool needs entry/source proof, operation proof, output proof, and viewer-value proof
- Music policy: `voice_only_clean` by default; narration and tool proof stay primary

## Scheme 5: Checklist / Mistake / Template Poster

- Format: 9:16 or 16:9 depending on proof needs; 8-25 seconds if poster-led, 30-60 seconds if narrated
- Content job: give a saveable checklist, mistakes list, or prompt template
- Best for: `5 个避坑`, `3 步流程`, `小白检查表`, `提示词模板`
- Design style: checklist rows, wrong/right chips, before/after mini cards
- Motion style: row reveal, risk chip lock, template lift settle
- Evidence rule: if it claims results or platform rules, add source or soften as advice
- Music policy: `voice_only_clean` for narrated mode; short poster mode may use approved library/reference music

## Scheme 6: Operation Proof / Test Result Short

- Format: usually 16:9, 1920x1080, 20-45 seconds, may be voice-led or caption-led
- Content job: prove an operation actually ran
- Best for: code change, browser test, terminal output, CI/lint/test/build result, before/after UI proof
- Design style: repo/file tree, terminal/test output, browser result, proof badge
- Motion style: cursor trace, proof tray slide, pass/fail chip settle
- Evidence rule: no fake terminal, no tiny unreadable proof panels
- Music policy: `no_bgm` by default; proof clicks and pass/fail SFX are safer than BGM over terminal/browser evidence

## Scheme 7: AI Hot Rank TOP5

- Canonical name: `方案7: AI 热榜 TOP5 榜单`
- Format: usually 9:16, 1080x1920, 8-12 seconds for no-voice short lists or 18-35 seconds when narration/source explanation is needed
- Content job: rank five current AI signals from real sources and explain why each matters
- Best for: `AI 热榜 TOP5`, `今日 AI 榜单`, `5 个 AI 更新`, `AI 工具/模型排行`, `本周 AI 重点`
- Design style: dynamic AI background, readable rank rows, visible source/date pins, one conclusion lock, Balanced Glass foreground modules
- Motion style: countdown reveal from 5 to 1, rank row lock, source/date tick, final number-one emphasis, BGM-synced row transitions
- Evidence rule: all five entries need source title, source URL or source note, visible date, rank score, and reason. Do not invent "hot" signals.
- Ranking rule: rank by auditable scoring across freshness, impact, practical value, source strength, visual clarity, and compliance safety. Do not call it `排名第一`, `全网第一`, or an absolute platform ranking unless an official ranked source proves that exact claim.
- Audio: if a Douyin reference video is provided and contains BGM, preserve the BGM or same Douyin music-page track when technically possible for same-platform Douyin publishing; otherwise block for the user's music file, platform same-music selection, or explicit no-BGM approval. Do not use generated or similar replacement music silently.
- Music policy: `required_bgm`; countdown/ranking videos need music for rhythm, row locks, and final emphasis
- Required template: `templates/ai_hot_rank_top5.template.json`

## Selection Rule

If a user gives a reference video, classify it into one of these schemes before writing text:

- If the reference is a short vertical list of recommended Skills/tools and has no narration, choose Scheme 1.
- If the content job is Skill/tool/plugin recommendation for beginners, choose Scheme 1 even when the video uses a TOP5/list/countdown surface.
- If the content job is `AI 热榜`, `TOP5`, a five-item ranked AI update list, or a countdown ranking about current AI news/signals, choose Scheme 7.
- If readable UI/docs/source proof is central, choose Scheme 2 or 6 and keep 16:9.
- If the topic starts from recent industry news, choose Scheme 3.
- If multiple tools/skills are the subject, choose Scheme 4.
- If the deliverable is mostly a saveable list/template, choose Scheme 5.

When uncertain, write the classification and why. Do not proceed to rendering until the content job and scheme are locked.

## Music Decision Rule

After locking the scheme, write `audio_music_decision` before storyboard, TTS, HyperFrames, or mix work. The decision must record:

- `music_policy`: `required_bgm`, `library_music_bgm`, `voice_only_clean`, or `no_bgm`
- `bgm_source_priority`: normally `douyin_reference`, `authorized_local_library`, `pixabay`, `mixkit`, or empty when no BGM is allowed. In reference-led Douyin videos with detected BGM, `douyin_reference` is mandatory and replacement requires explicit user approval.
- `voice_policy`: `no_voice`, `required_narration`, `optional_narration`, `optional_short_narration`, or `contextual`
- `voice_priority`
- `sfx_required`
- `mix_note`
- `generated_bgm_allowed`: must be `false`
- `reference_bgm_policy`: use same reference music when detected; block rather than substitute if unavailable

Default matrix:

- Scheme 1 and Scheme 7: `required_bgm`
- Scheme 2 and Scheme 6: `no_bgm`
- Scheme 3, Scheme 4, and Scheme 5 narrated mode: `voice_only_clean`

Reference-led videos may override the default only when the reference audio relationship is documented. Explicit user no-music requests set `music_policy=voice_only_clean` for narrated videos unless the user later approves BGM. Generated/synthesized/self-created BGM, SFX beds, noise beds, ambience, electric buzz, and texture audio are not allowed for this skill; if exact reference music is required but unavailable, stop for user confirmation instead of selecting a substitute.

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
