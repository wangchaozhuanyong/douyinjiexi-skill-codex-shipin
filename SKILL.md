---
name: douyin-hyperframes-remake
description: Analyze a Douyin/TikTok-style video link, local reference video, or share text and remake it as an original short-video production using the local Douyin parser, gpt-image-2/image generation, real product screenshots/recordings, and the HyperFrames plugin. Also use for the user's daily AI tips publishing workflow and Codex/AI Skill tutorial videos that need reference-film breakdown, evidence-led editing, premium product-demo visuals, copy-lock approval, Qingdou checking, stable storyboard/TTS/template/BGM production discipline, and Douyin publishing. Use when the user sends a Douyin link, local video file, or asks Codex to reference, remake, recreate, closely follow, or produce a new publish-ready Douyin video with assets, captions, cover, compliance checks, and a rendered MP4/ZIP package.
---

# Douyin HyperFrames Remake

## Purpose

Turn a user-provided Douyin link, local reference video, or share text into an original short-video package: reference analysis, storyboard, generated image prompts/assets, real evidence assets when needed, HyperFrames composition, rendered MP4, cover, caption, and publishing notes. Default to 9:16 for feed-native Douyin videos, but match the reference or user-requested aspect ratio when the work is clearly horizontal or format-specific.

Do not create a low-effort copy. If the user asks for very high similarity, treat it as reference structure and pacing only: use new visuals, rewritten copy, new captions, and a distinct creative angle.

## Required Tool Order

1. Use `scripts/analyze_reference.py` to extract the reference theme, tags, title direction, storyboard, caption, compliance sources, and originality threshold from the local Douyin parser when a Douyin link/share text is provided. When a local reference video or Codex/AI tool tutorial reference is provided, first extract metadata and representative keyframes/contact sheet, then document shot structure before writing the new script.
2. When the user asks to closely follow a reference video, preserve wording, or change copy by only a stated percent, run the Copy Lock Gate before any production: extract or request the source transcript, draft the exact public-facing text, document similarity and compliance decisions, and wait for the final text to be accepted or explicitly authorized.
3. Read `references/beginner_visual_sync_rules.md` before topic selection, scripting, image prompting, HyperFrames authoring, rendering, or publishing. Lock one plain-language topic, lock the full public-facing copy package, and create a voice-to-visual beat map before production.
4. After drafting the title, first-5-second hook, voiceover, subtitles, on-screen text, cover text, publish caption, hashtags, and any text requested inside generated images, run `scripts/check_public_copy.py` or an equivalent local compliance check, then check the text with Qingdou sensitivity-word detection at `https://www.qingdou.vip/pctool/sensitivity-word`. Use the user's current authorized session or credentials provided in the current conversation only; never write credentials into files, skills, logs, or GitHub.
5. If Qingdou or local checks report sensitive or risky words, rewrite the text and rerun the check until the script is clean enough to proceed. Do not start image generation, TTS, subtitles, HyperFrames authoring, or rendering before this check passes or before the user explicitly accepts a documented unresolved blocker.
6. Read `references/pixelle_pipeline_lessons.md` before TTS, asset generation, or rendering. Create `storyboard.json` with scene text, template preset, voice, speed, BGM plan, intended media paths, and beginner sync fields; then update it with real audio durations after TTS.
7. Use real screenshots, local proof assets, and free/available design methods first. Use image generation for needed visual assets only when it is available and authorized; prefer `gpt-image-2`/built-in image generation for approved visual assets. Save final assets inside the project output folder.
8. Use the free-first tool stack in `references/beginner_visual_sync_rules.md`, plus the HyperFrames by HeyGen skills:
   - `hyperframes` for composition authoring rules.
   - `hyperframes-cli` for `npx hyperframes init`, `lint`, `inspect`, `preview`, and `render`.
9. Package the final deliverables: MP4, cover JPG/PNG, caption TXT, `storyboard.json`, `metadata.json`, production notes, source HyperFrames project, and ZIP when useful.

## Workflow

### 0. Daily AI Publishing Automation

Use this workflow when the user asks for daily or scheduled Douyin publishing about AI tools and advanced usage.

Schedule default:

- Run every day at Beijing time 19:00 when configured as an automation.

Daily topic selection:

- Treat the same-day hot-topic scan as mandatory. Do not write the script, generate images, create TTS, render video, or upload until this scan is complete.
- Browse/search today's hot topics for all four required areas before choosing a topic: `AI`, `Codex`, `Gemini`, and `ChatGPT`.
- Use date-aware searches for the current day first. If same-day signals are weak, expand to the most recent 7 days and say that clearly in the production notes.
- Check at least four source angles: general AI news, Codex/OpenAI, ChatGPT/OpenAI, Gemini/Google AI, plus AI video or AI coding tools when useful.
- Allowed topic pool: Codex, Gemini, ChatGPT, AI video tools, AI coding tools, AI automation workflows, and advanced productivity techniques.
- Compare at least three candidate topics before choosing exactly one practical, high-value topic per day.
- Before final topic selection, check recent local `daily-ai-*`, `daily-ai-dry-run-*`, and `daily-ai-formal-simulation-*` folders in `/Users/wangchao/Desktop/抖音解析`. Do not reuse or closely repeat yesterday's dry-run, formal-simulation, or test topic for a formal daily publish.
- Record the topic deduplication result in `production-notes.md`, including which recent folders or files were checked and why the final topic is sufficiently different.
- For every candidate, perform a mini viral breakdown: hook angle, likely comment emotion, save/share reason, controversy or debate point if safe, visual potential, and whether it teaches something actionable.
- Prefer fresh, high-interest, tutorial-friendly topics over generic introductions.
- Choose topics like a short-video strategist and psychology-aware editor, not like a generic news summarizer. Score each candidate for viewer pain, curiosity gap, practical payoff, novelty, emotional tension, and ease of visual explanation.
- Reject topics that are only “news happened today” but do not give the viewer a reason to stop, listen, save, or share.
- Do not invent trend claims. The final topic must be based on currently browsed sources, not memory or guesses.
- Record source URLs, publish dates when visible, the candidate list, viral breakdown, psychology reason for the final choice, and why viewers would watch past the first 5 seconds in the production notes.

Daily production rules:

- Produce an original short video, not a copied reference.
- Title, voiceover, subtitles, publish caption, and hashtags must be written before generation.
- The title, first-5-second hook, voiceover, subtitles, on-screen text, cover text, publish caption, hashtags, and image-text plan must pass compliance review before TTS, image generation, HyperFrames authoring, rendering, or upload.
- Treat the video as a premium editorial product. The goal is not “make a video”; the goal is a high-retention, high-design, highly listenable short video.
- Lock one beginner-friendly topic before writing. A non-professional viewer must understand what the software does, why it is convenient, and what first action to try.
- Define hook reason, watch reason, save reason, share reason, and trust reason before writing. If the video has no reason to save, share, trust, or keep watching, redesign the topic.
- Hashtags must include `#gtp` and `#codex`, plus exactly three safe AI-related hashtags unless the user changes the rule.
- Keep the public caption short and clean.
- Run local compliance and Qingdou sensitivity-word checks before TTS, rendering, or publishing.
- If Qingdou flags a word, rewrite and recheck until clean or stop for user acceptance.
- Generate final video with natural Chinese voice, preferably Edge TTS `zh-CN-YunyangNeural` at `1.10-1.12x` for Mandarin tutorial/daily videos, synchronized captions, premium varied visuals, and no internal labels such as `remake` or `重创重做版本`.
- Generate an independent poster-style cover for every publish-ready video. Do not rely on a random video frame as the only cover.
- The first 5 seconds must be deliberately designed as a retention hook with motion, contrast, curiosity, and a clear promise. If the opening does not make a viewer want to stay, rewrite and redesign it before rendering.
- The first 5 seconds must show or imply a concrete result, proof, mistake correction, or shortcut. Do not open with slow introductions, greetings, or abstract feature names.
- Every scene must include designed motion or interaction: card reveals, cursor paths, toggles, timelines, scroll simulations, panel transforms, focus highlights, comparison switches, progress states, or diagram builds. Do not deliver static slide narration.
- Every voice beat must match the current visual. If the narration says upload, generate, preview, check, or export, the current scene must show that exact action, result, or a clearly labeled concept substitute.
- Visual language must be Chinese-first. On-screen headlines, image text, labels, callouts, charts, UI annotations, covers, and subtitles should default to Chinese. Keep English only for real product names, command names, model names, or unavoidable UI proof.
- Avoid baking Chinese text into generated images. Add important Chinese titles, captions, labels, and CTA in HyperFrames as editable HTML text. Reject images with pseudo-Chinese, garbled Chinese-like characters, risky claims, QR codes, contact details, fake reviews, or fake official badges.
- Reject cheap image zooms. Do not animate a still image by simply scaling from small to large or large to small, especially when it causes flashing, popping, jitter, or low-quality slideshow feeling.
- Give every image an intentional entrance or transformation: layered fly-in, masked reveal, split-screen insert, card stack, parallax depth, push panel, timeline slide, cursor-led focus, wipe, crop reveal, or 3D tilt. A static image with only narration is not acceptable.
- Treat image-over-text collisions as a hard failure. Before render, reserve separate safe zones for headlines, captions, callouts, and proof media; screenshots, product cards, generated images, and inserted pages must never cover or crowd Chinese titles or subtitles.
- Add restrained transition or insertion sound effects when a page switches, screenshot enters, card stack assembles, or proof panel drops in. Keep SFX below narration; never let effects mask Chinese speech.
- Use HD source assets for HD output. Do not scale 720p screenshots into large 1080p proof frames for final delivery; recapture or regenerate important UI/proof assets at the output resolution or higher.
- If sampled keyframes look flat, generic, or low-texture, redesign before render. The video must feel like a premium Chinese product-demo/editorial short, not a basic template export.
- If the rendered 1080p MP4 looks soft, has obvious compression artifacts, or has a very low video bitrate for screenshot-heavy content, rerender with `--quality high` or remux/transcode from the high-quality render using a higher-quality H.264 pass before delivery.
- Keep the delivery folder clean; user-facing output should contain only the approved final MP4 unless additional assets are requested.

Daily publishing authorization:

- The user authorizes routine steps without asking again: web research, copywriting, Qingdou checking, video generation, file cleanup, Chrome upload, filling title/caption/hashtags, selecting public/immediate publishing defaults, clicking publish, and using non-SMS verification methods that the current safety rules allow.
- The user also authorizes next-day performance review for videos published by this workflow: use the current logged-in Douyin creator session in Chrome to open creator analytics, inspect the previous day's published work, and record performance signals for the next video.
- SMS verification is not authorized and cannot be bypassed. If Douyin or another service requires a phone SMS code, stop and tell the user exactly what is needed.
- Do not guess, store, or reuse SMS codes, passwords, cookies, or account secrets.
- If a page requires a CAPTCHA or slider verification, follow the active browser safety rules; ask for user confirmation when required.
- If login expires or the platform requires a user-only action, stop with a short status and keep the relevant tab open when possible.

Daily publish report:

- Today's hot-topic scan: sources, candidate topics, and final pick.
- Yesterday's performance review when available: previous video, views, retention/watch signals, engagement, comments, lessons, and how those lessons changed today's creative decisions.
- Selected topic and why it was chosen.
- Source/trend summary.
- Script score, visual score, first-5-second score, and simulated viewer-review result.
- Audience value result: hook reason, watch reason, save reason, share reason, and trust reason.
- Final title, caption, and hashtags.
- Qingdou result.
- Final video folder.
- Douyin publish result or the exact blocker.

### 0.5. Codex Skill Tutorial Video Mode

Use this mode when the user references a video about Codex, Skills, Agents, HyperFrames, Imagegen, ChatGPT, Gemini, or similar AI tools and asks for a work with the same level of quality.

Read `references/beginner_visual_sync_rules.md` and `references/codex_skill_tutorial_video.md` before planning, scripting, capturing assets, or rendering.

Hard rules:

- Do not make a generic AI-image slideshow. This mode is an evidence-led product tutorial: real UI screenshots, browser recordings, plugin pages, local output folders, generated result examples, and product-demo motion must carry the video.
- The tutorial must be understandable to beginners. Start from the viewer's problem, show the exact software action, and prove convenience through fewer steps, clearer results, or a before/after.
- Before writing the script, break down the reference video into a shot table: timestamp, visual type, caption/voice beat, motion/transition, and why the shot exists.
- Match the reference format intentionally. If the reference is 16:9 horizontal or another non-vertical format, do not force 9:16 unless the user asks for a vertical Douyin cut.
- For each named tool or skill, include at least one real interface proof shot and one result proof shot. If real evidence is unavailable, stop and either capture it, produce a clearly labeled concept substitute, or ask the user for the missing access.
- At least half of the final runtime should be product evidence or output proof, not generated ambience.
- Use generated visuals only to support transitions, covers, abstract explanations, or result mockups that are clearly not fake real evidence.
- The opening must behave like a creator hook: a bold claim, a visual snap-in, and a clear promise in the first 3 seconds.
- Use the stable production layer from `references/pixelle_pipeline_lessons.md`: `storyboard.json`, per-scene audio, real audio durations, template preset, BGM settings, and `metadata.json`.
- Record the reference breakdown, evidence asset list, aspect-ratio decision, and evidence score in `production-notes.md`.

### 1. Analyze The Reference

Run:

```bash
python /Users/wangchao/.codex/skills/douyin-hyperframes-remake/scripts/analyze_reference.py \
  --text "<douyin share text or URL>" \
  --out "<work-dir>/reference-analysis.json"
```

Use `--project-dir /Users/wangchao/Desktop/抖音解析` unless the parser moved.

Read the JSON and identify:

- `theme`, `category`, `hashtags`, `duration`
- `reference_analysis.signals`
- `reference_analysis.copy_boundary`
- `shot_list`
- `voiceover`
- `publish_caption`
- `compliance` and `draft_compliance`
- `originality.minimum_difference_rate`

If parsing fails because Douyin blocks the link, continue from the pasted share text, but state the limitation in the production notes.

Before production, set `target_duration`:

- If `duration` is known, `target_duration` defaults to approximately the reference duration.
- If `duration` is unknown, infer from the user's request or ask one concise question before producing a full video.
- Do not silently choose a shorter duration for convenience.

### 2. Plan A Safe Remake

Use the reference for:

- topic
- hook style
- pacing pattern
- scene count
- information hierarchy
- audience intent
- approximate duration, unless the user explicitly requests a condensed version

For local video references, inspect the actual media before planning. Record the duration, aspect ratio, resolution, rough scene count, subtitle style, visual system, and recurring edit patterns in `production-notes.md`.

Duration rule:

- If the reference video has a known duration, preserve the same approximate length by default. A 4-minute reference should become a roughly 4-minute remake, not a 30-60 second summary.
- Only shorten the video when the user explicitly asks for a short version, compressed version, highlight version, or platform-specific ad cut.
- If the remake would be long and costly to generate, tell the user before production and offer clear options such as full-length remake, 60-second summary, or 15-second hook cut.
- When delivering a shortened version, label it clearly as a condensed version in production notes and final response.
- Never present a condensed version as the full remake.

Do not use:

- original video frames
- original subtitles
- original voice
- original music
- complete original wording
- simple edits such as mirror, crop, BGM swap, or line-order changes

Read `references/douyin_rules.md` when writing publishing copy or explaining risk.

### 2.0. Copy Lock Gate For Close Reference Requests

Use this gate before TTS, screenshots, image generation, HyperFrames authoring, or rendering whenever the user says the wording should stay very close to a reference, such as `文案只能改百分之10`, `照着这个文案`, `按原视频文案`, or similar.

Hard rules:

- First obtain the source wording. Prefer a real transcript from the reference audio/subtitles. If transcription fails or the source video is missing, stop production and request the original video or full subtitle/voiceover text; do not claim a percent-level rewrite is verified from keyframes alone.
- If the user gives a percent-change limit, treat it as a similarity-control request, not permission to copy unsafe text. Preserve topic, structure, beat order, and sentence function where possible, but compliance, originality, and platform safety override the percent target.
- Do not copy original subtitles, complete original wording, voice, music, or frames. If the user asks for wording that would be too close to the source, explain the safe interpretation: same structure and rhythm with original publish-safe wording.
- Create a copy-lock folder or files before production, including `copy-lock.md` for title/voiceover/subtitles/cover/publish caption/hashtags, `compliance-text.txt` for the exact text to paste into Qingdou, and `compliance-report.md` for local and Qingdou results.
- Run a local risk-word scan first. Remove or soften exaggerated, absolute,诱导, private-domain diversion, illegal, adult, gambling, political/military, medical/financial-claim, and low-originality risk words before Qingdou.
- Paste the complete `compliance-text.txt` into Qingdou using the user's authorized logged-in session. If Qingdou requires login, CAPTCHA, SMS, or user-only action, record the blocker and stop before production.
- Start video production only after the final public-facing text is locked and either Qingdou passes or the user explicitly accepts the documented unresolved Qingdou blocker. If the user said `确定好文案才能开始做视频`, wait for explicit approval of the locked copy before producing assets.
- Record in `production-notes.md`: source transcript path or missing-source blocker, requested similarity limit, what changed and why, local compliance result, Qingdou result, and whether the user approved the locked copy.

### 2.1. Psychology-Led Topic And Script Strategy

Before writing the script, define the viewer psychology in `production-notes.md` or the planning file.

Required planning fields:

- Plain-language topic: one sentence a beginner can repeat after watching.
- Target viewer: who this is for and what they are trying to achieve today.
- Core pain: what problem, confusion, anxiety, wasted time, missed opportunity, or status gap the viewer feels.
- Curiosity gap: what the first 5 seconds makes them want to know.
- Emotional promise: what the viewer will feel if they keep watching, such as clarity, control, advantage, relief, surprise, or confidence.
- Practical payoff: what concrete action or mental model the viewer gets by the end.
- Retention path: why the viewer should keep watching from hook to middle to ending.
- Convenience promise: what the software makes easier and how the video will prove it visually.

Script requirements:

- Write like a smart human creator speaking to another busy human, not like a manual, article, or AI-generated explainer.
- Lead with tension, contrast, or an unexpected reframing. Avoid generic openings like `今天给大家分享`, `你知道吗`, or `随着 AI 发展`.
- The first 5 seconds must include one clear hook: surprising claim, sharp contrast, mistake correction, hidden benefit, or practical promise.
- Every 8-12 seconds, add a retention beat: question, reveal, before/after contrast, mini payoff, visual switch, or “next step” cue.
- Use short spoken Chinese sentences. Avoid long abstract paragraphs, stacked buzzwords, and English-heavy phrasing.
- Explain the workflow like a beginner tutorial: one action, one result, one visual proof at a time.
- Make the viewer feel the content was made for them: use concrete work scenarios, decision points, mistakes, and outcomes.
- The ending should create a save/share reason: a checklist, summary line, decision rule, or repeatable method.

Reject the script and rewrite it if:

- It sounds like generic AI news.
- It explains a topic but does not create curiosity.
- It is correct but boring.
- It has no clear benefit for the viewer.
- A non-professional viewer cannot tell what to do first or why the software is convenient.
- The script can only be understood by people who already know the professional terms.
- It could be read as a blog post without losing anything.

### 2.2. Viral Breakdown And Topic Scoring

Do not pick a topic only because it is popular. Pick it because it can become a useful, watchable, emotionally clear video.

For at least three candidate topics, score each from 1-10:

- Heat: is the topic fresh, searched, or discussed now?
- Pain: does the viewer have a real problem or anxiety around it?
- Curiosity: does the topic create a clear question the viewer wants answered?
- Payoff: will the viewer leave with a useful method, checklist, or decision rule?
- Visuality: can the topic become premium interaction-driven visuals instead of talking-head filler?
- Safety: can it be explained without risky promises, exaggerated claims, or sensitive wording?

Choose the topic with the best balance, not necessarily the highest heat.

Also write a viral breakdown for the chosen topic:

- Hook angle: why someone stops scrolling.
- Comment emotion: what viewers may say or argue about.
- Save reason: why the video is worth saving.
- Share reason: who the viewer would send it to.
- Completion reason: what unresolved promise keeps them watching to the end.
- Brand fit: why this topic fits the user's AI/Codex/Gemini/ChatGPT account direction.

Reject a topic if it cannot produce a strong hook, practical payoff, or premium visual treatment.

### 2.3. Script Scoring Gate

After drafting the script but before compliance checking, score it from 1-10 in these categories:

- First-5-second hook strength.
- Spoken naturalness in Mandarin.
- Viewer pain clarity.
- Curiosity gap.
- Practical usefulness.
- Audience value: does the script give a clear reason to watch, save, share, and trust?
- Beginner clarity: could a non-professional viewer repeat the topic and first action?
- Voice-to-visual readiness: can every spoken beat be matched to an exact image, UI state, proof, or animation?
- Information density without overload.
- Retention beats every 8-12 seconds.
- Ending save/share value.

Passing threshold:

- Overall score must be at least 8/10.
- First-5-second hook must be at least 9/10.
- Spoken naturalness must be at least 8/10.
- Beginner clarity and voice-to-visual readiness must each be at least 8/10.
- Audience value must be at least 8/10.

If the script fails any threshold, rewrite it and score again. Do not proceed to Qingdou, TTS, image generation, or rendering with a weak script.

The final `production-notes.md` must record the script score and a short reason for the score.

### 2.5. Mandatory Sensitivity-Word Check

Before generating images, TTS, subtitles, or final video, prepare the exact text that will be public-facing:

- voiceover script
- on-screen captions/subtitles
- title or cover text
- publish caption
- hashtags
- text requested inside generated images or screenshots

Run the bundled local compliance check first:

```bash
python /Users/wangchao/.codex/skills/douyin-hyperframes-remake/scripts/check_public_copy.py \
  <work-dir>/compliance-text.txt
```

Then use Qingdou:

```text
https://www.qingdou.vip/pctool/sensitivity-word
```

Rules:

- Log in only with the user's authorized session or credentials provided in the current conversation.
- Never store the username, password, cookies, or screenshots containing private account details in the project, skill, notes, GitHub, or generated deliverables.
- Paste the full public-facing text into Qingdou before production.
- If Qingdou reports sensitive words, rewrite those phrases, then check again.
- Do not proceed to TTS, HyperFrames, or rendering until the final text has passed or the remaining risks are explicitly documented and accepted by the user.
- Do not proceed to image generation until the image-text plan is checked. Image prompts must explicitly prohibit sensitive words, exaggerated claims, contact information, QR codes, fake reviews, fake official certification, and pseudo-Chinese or garbled Chinese-like text.
- Record the final check status in `production-notes.md` as `Qingdou sensitivity check: passed` or include a short summary of unresolved items.

### 3. Generate Image Assets

Create 5-8 distinct scene prompts from the storyboard. Follow `references/beginner_visual_sync_rules.md` for every prompt. Do not let the final video feel like one static image with minor variations. Each prompt should specify:

- target composition: 9:16 vertical for feed-native Douyin videos, or the selected reference/user-requested aspect ratio for format-specific tutorial videos
- subject and scene
- beginner takeaway and why this image exists
- visual style derived from the reference category
- premium, information-rich, commercial-grade composition with crisp details, layered depth, and a clear focal point
- clean text-safe space for HyperFrames titles, captions, subtitles, and CTA
- no text baked into the image unless absolutely necessary
- no sensitive words, exaggerated claims, contact information, QR codes, fake reviews, fake official certification, pseudo-Chinese, malformed Chinese-like glyphs, or unreadable text
- no platform logo, watermark, phone UI, celebrity likeness, or copied source-frame composition

Use image generation once per scene. Save assets in:

```text
<work-dir>/assets/scene-01.png
<work-dir>/assets/scene-02.png
...
```

If the subject is high-risk or fact-sensitive, generate abstract/editorial visuals rather than fake real evidence.

For Codex/AI tool tutorial videos, create an evidence plan before generating images. Capture or collect real screenshots/recordings and real output examples first; image generation should not replace product proof.

If one image contains several ideas, either split it into several scenes or animate the ideas one by one. Do not show all points at once while the voice explains them later.

Before rendering, check a contact sheet or several still frames. If the scenes look too similar, generate or design more varied visuals before continuing.

### 3.5. Premium Visual System

Before writing HyperFrames HTML or generating final assets, create a premium visual direction in `DESIGN.md`.

Required visual decisions:

- Define a mature 4-6 color palette with named roles: background, surface, primary accent, secondary accent, text, muted text.
- Define a Chinese-first typography system. Use Chinese headlines, Chinese labels, Chinese proof captions, and Chinese cover copy by default; keep English only when it is a product name, real UI text, command, file path, or brand term that should not be translated.
- Avoid cheap template palettes: pure neon cyan on dark teal, one-note blue-green screens, heavy purple-blue gradients, flat black backgrounds, or random rainbow accents.
- Use restrained contrast. Prefer deep charcoal, ink, graphite, off-white, warm gray, muted cobalt, silver, glass, or subtle amber accents when appropriate for AI topics.
- Use 1-2 accent colors only. Accent colors should guide attention, not flood the whole page.
- Use layered depth: subtle grain/noise, soft shadows, thin keylines, translucent panels, editorial lighting, paper/card texture, clean screenshot frames, or spatial layers. Do not use generic glow blobs, bokeh circles, or decorative orbs.
- Typography must feel editorial or product-grade: clear hierarchy, generous line height, no cramped text, no tiny labels, no negative letter spacing.
- UI diagrams should look like a polished product demo or premium keynote slide, not a rough wireframe.
- Do not let all scenes share the same background color and layout. Vary composition through diagrams, close-up panels, comparison tables, process flows, code/editor-inspired screens, and abstract system maps.
- Captions should sit in a deliberate safe-area container with enough padding and contrast; avoid large low-quality boxes that look pasted on.
- Every visual should feel intentionally art-directed. Treat each image and scene as a designed poster frame with composition, rhythm, negative space, typography, and focal hierarchy.
- Use a design system, but avoid repetitive templates. Each scene should have a new visual idea while still belonging to the same film.
- For AI/tool/tutorial content, prefer premium interaction metaphors: product dashboards, command palettes, timeline editors, automation maps, approval gates, prompt workbenches, split-screen comparisons, and elegant process diagrams.
- Build micro-interactions into the visual language: hover-like highlights, active states, toggles, checkmarks, progress bars, connecting lines, expanding cards, cursor trails, and step-by-step reveals.

Low-quality visual patterns to reject:

- Oversaturated gradients covering the whole frame.
- Excessive glow, blur, bloom, or fake glass effects.
- Random line diagrams without alignment, spacing, or visual hierarchy.
- Repeated dark teal backgrounds with white text on every scene.
- Large empty areas with one small diagram unless the emptiness is intentionally designed.
- Stock-looking AI brain/robot/circuit imagery unless it is transformed into a coherent visual system.
- Plain text over a flat background with no interaction, depth, or editorial composition.
- Reusing one background image with tiny motion and calling it a finished video.
- Screens that look like template slides rather than a premium short-video design.
- Still images that only scale from small to large, large to small, or pulse in place.
- Image entrances that flash, pop, stutter, or expose a blank/white frame between states.
- English-heavy generated images, English charts, English labels, or English cover text when the video is for a Chinese audience.
- Low-texture AI images with no foreground/midground/background depth, no readable focal hierarchy, and no designed Chinese headline.

Validation:

- Extract 5-6 keyframes and judge color quality before final delivery.
- If the frame looks like a generic AI template, redesign the palette and layout before rendering.
- If the user complains that the page color or visual quality is low, treat it as a design failure and rerender with a stronger visual system.
- If the first 5 seconds do not contain a visually strong hook frame and at least one clear motion/interaction event, redesign the opening.
- If any keyframe would not work as a standalone high-quality poster crop, improve the composition before delivery.

### 3.55. Interaction And Motion Direction

Short videos produced by this skill must feel alive. Motion is not decoration; it should help the viewer understand and keep watching.

Required interaction patterns:

- Opening hook: one strong visual action in the first 1-2 seconds, such as a fast comparison reveal, interface snap-in, timeline zoom, or problem-to-solution transformation.
- Scene transitions: every scene change must have a purposeful transition, not only a hard cut unless the hard cut is intentionally rhythmic.
- Information reveal: complex ideas should build step by step through animated layers, highlights, check states, sliders, cursor movement, or diagram growth.
- Focus guidance: when the narration mentions a key idea, the visual must guide the eye with a highlight, scale shift, underline, mask reveal, or active state.
- Beat-by-beat sync: every important spoken phrase should correspond to the visible action, proof, callout, or image region currently being highlighted.
- Rhythm variation: alternate close-up detail scenes, wider system-map scenes, and human-workflow scenes so the viewer does not feel trapped in one layout.
- Image motion: every still or generated image must enter or change through a designed movement such as fly-in from a screen edge, depth push, mask wipe, card stack insertion, split-screen slide, pinned overlay, parallax drift, 3D tilt, or cursor-led reveal.
- Composited image scenes must include at least two moving layers: for example background drift plus foreground card insertion, screenshot push-in plus callout slide, or product frame reveal plus Chinese caption build.
- Static hold time must be intentional. No image may sit unchanged for more than 2.5 seconds unless the voiceover needs a proof-reading pause and there is a visible focus highlight or cursor motion.

Interaction quality bar:

- Motion must be smooth, restrained, and premium. Avoid shaky camera effects, random bouncing, cheap zoom loops, and constant pulsing.
- Interactions should look like a high-end product demo, not a basic slideshow.
- Do not add movement that distracts from the voiceover.
- If a scene has no meaningful visual change for more than 5 seconds, add a useful reveal, split, highlight, or transition.
- If a scene has multiple knowledge points, reveal or focus them one at a time, or split them into separate scenes.
- Ban the default still-image zoom pattern: do not solve motion by applying only `scale(0.9) -> scale(1.05)`, Ken Burns zoom, or a looping pulse. Use layered scene choreography instead.
- When using screenshots, pages, or images beside text, animate them as inserted panels, side fly-ins, mask reveals, split-screen slides, cursor-led focus frames, or 3D cards. Never let the motion path pass through the title/subtitle safe area unless it is fully masked and visually intentional.
- Avoid flashes caused by opacity jumps, missing assets, white backgrounds, or render timing gaps. Use preload-safe assets, opaque scene backgrounds, and overlap transitions.
- Validate the rendered video, not only the source files. If motion feels cheap after rendering, simplify and rerender.

### 3.58. Layout, SFX, And HD Failure Rules

After any user complaint about visual blocking, weak motion, missing audio rhythm, or low texture, convert the complaint into a hard validation gate for the next render.

Hard failures that require redesign and rerender:

- Any key image, screenshot, generated visual, card, callout, or page insert overlaps or visually crowds the title, subtitle, caption, or CTA at its hero frame.
- Still images only grow from small to large, large to small, or pulse without a purposeful insert/reveal/focus action.
- Scene changes, page switches, proof-panel insertions, or major card assemblies have no audible but restrained SFX cue when the visual style calls for a polished product-demo rhythm.
- A 1920x1080 final uses visibly soft 720p source screenshots for large proof frames.
- The final MP4 is technically 1080p but looks compressed, smeared, low-contrast, or low-texture in representative frames.

Required fixes before delivery:

- Separate text and media into explicit safe zones; shrink, move, crop, or restage media instead of letting it sit under text.
- Run `hyperframes inspect` with dense samples and explicit timestamps for every crowded hero frame.
- Extract full-size detail frames for the most crowded scenes, not only a small contact sheet.
- Generate or mix subtle whoosh/pop/click SFX for transitions and insertions, then confirm the mixed audio is present in the final MP4.
- Recapture screenshots at 1920x1080 or higher when they are used as major proof frames.
- For final 1080p delivery, prefer `npx hyperframes render --quality high`; if the output bitrate is too low or frame detail looks soft, produce the stable `delivery/final.mp4` from the high-quality render with a higher-quality H.264 pass and document it in `metadata.json`.

### 3.56. First Five Seconds Retention Test

Before final render, the opening must pass this test:

- Can the viewer understand the topic without reading the description?
- Is there a strong visual reason to stop scrolling?
- Does the first sentence create tension, surprise, or a promise?
- Does the viewer know what they will gain by watching?
- Is there movement or interaction within the first 2 seconds?
- Is the first visual text in Chinese unless it is a real product name?
- Does the opening avoid the cheap still-image zoom or flash pattern?

If any answer is no, rewrite the hook and redesign the first scene before continuing.

### 3.57. Visual Scoring Gate

Before final render, score the storyboard, design frames, or sampled keyframes from 1-10:

- Premium feel: does it look crafted, editorial, and high-end?
- Composition: is there a clear focal point, spacing, and hierarchy?
- Typography: is text readable, elegant, and not cramped?
- Color: is the palette mature and not cheap or template-like?
- Interaction: does motion/reveal help explain the idea?
- Scene variety: do scenes feel meaningfully different while still coherent?
- Retention support: does the visual make the viewer want to continue?
- Douyin readability: is it understandable on a phone at small size?
- Chinese-first readability: are generated image text, headings, proof labels, and cover text primarily Chinese?
- Texture and depth: does the frame have premium material, lighting, shadow, layered composition, or real UI evidence instead of flat stock-like imagery?
- Motion craft: do images fly in, insert, reveal, split, or transform with purpose instead of merely zooming larger?

Passing threshold:

- Overall visual score must be at least 8/10.
- Premium feel, typography, and interaction must each be at least 8/10.
- First-5-second visual score must be at least 9/10.
- Chinese-first readability, texture and depth, and motion craft must each be at least 8/10.

If the visual score fails, redesign the weak scenes and rerender. Do not publish a video that looks like a template slideshow, even if the script is good.

The final `production-notes.md` must record the visual score and which scenes were improved.

### 3.6. Independent Poster Cover

Create a cover that looks like a standalone Douyin poster, not a low-quality frame grab.

Required cover assets:

- Vertical cover: 3:4 for Douyin's vertical cover slot.
- Horizontal cover: 4:3 for Douyin's horizontal cover slot.
- First-frame poster: target-aspect JPG/PNG inserted as the video's opening frame when direct cover upload is unreliable or Douyin still reports cover quality problems. Use 1080x1920 for vertical Douyin videos.

Cover design requirements:

- It must communicate the video's topic within 1 second, with a clear title, one short benefit line, and 2-5 small keyword chips when useful.
- Use the same premium visual system as `DESIGN.md`, but make the cover stronger and simpler than normal scene frames.
- Treat the cover as a mini poster: strong hierarchy, clear contrast, clean margins, no cramped text, no random screenshot look.
- Avoid generic AI template visuals, tiny unreadable labels, stock robot/brain/circuit cliches, heavy glow, messy gradients, and low-resolution frame crops.
- Do not include internal production labels such as `重创重做版本`, `remake`, `reference`, `参考重制`, or anything that reveals the video was copied or remade.
- Keep cover text short enough to be legible in the Douyin creator preview.

Publishing fallback:

- If Douyin's custom cover upload UI is unreliable, prepend a 1-2 second poster intro to the MP4 and reupload that optimized video.
- After upload, choose the AI recommended cover or the poster frame that matches the designed cover.
- If Douyin reports `封面质量一般`, `封面优化建议`, `横/竖双封面缺失`, or a similar cover warning, do not treat it as final. Redesign the cover or use the poster-first-frame fallback until the page shows cover detection passed, unless the user explicitly accepts the warning.
- Record the final cover status in `production-notes.md`, including whether the page shows `封面效果检测通过` or `暂未发现封面低质问题`.

### 4. Build HyperFrames Project

Read `references/hyperframes_delivery.md` before authoring. Use the HyperFrames CLI:

```bash
npx hyperframes init <project-name> --non-interactive
```

Requirements:

- 1080x1920 root composition for vertical Douyin videos. For a local reference or user request that is clearly 16:9, use 1920x1080 or the reference aspect ratio, then keep subtitles and focal UI inside a mobile-friendly safe area.
- Use `DESIGN.md` before writing HTML. If no explicit style is supplied, derive a minimal style from the reference analysis.
- `DESIGN.md` must include the premium visual system: palette roles, typography, materials, layout rules, motion/interaction language, first-5-second hook design, and explicit anti-patterns.
- Create `storyboard.json` before authoring the final composition. It must include scene voice text, captions, media paths, `template_id`, `voice_id`, `tts_speed`, BGM plan, and real scene durations after TTS.
- Choose one production template preset such as `proof-tutorial-horizontal`, `daily-ai-vertical`, `premium-ai-card`, `blackboard-grid`, or `product-demo-proof-wall`; record it in `storyboard.json` and `DESIGN.md`.
- For repeated/daily work, inspect the latest relevant `metadata.json`, `storyboard.json`, and `production-notes.md` before choosing voice, speed, template, BGM, or render settings.
- Use generated images as scene backgrounds or framed media.
- Add animated captions/subtitles from the rewritten voiceover.
- Use transitions between every scene.
- Keep video and audio tracks compliant with HyperFrames rules.
- Include a final publishing card or end beat only if it fits the content.
- Do not display internal production labels in the final video such as `重创重做版本`, `重做版本`, `参考重制`, `remake`, `recreated`, `reference remake`, or similar wording.
- Do not add visible labels that imply copied or remade content. If attribution, risk notes, or remake explanations are needed, keep them in `production-notes.md`, not inside the final video frame.

Voiceover and timing requirements:

- Write narration in natural spoken Chinese, not article-style prose. Prefer short sentences with conversational transitions.
- Avoid asking macOS/system TTS to pronounce raw English-heavy strings. Replace difficult terms in the voice text with Chinese equivalents or phonetic wording while keeping display captions clean. Example: voice can say `扣代克斯`, while the on-screen title can still show `Codex`.
- Default Mandarin tutorial/daily voice is Edge TTS `zh-CN-YunyangNeural`; default speed is `1.12`, with `1.10-1.15` allowed after listening. Use `zh-CN-YunjianNeural` for a more energetic male fallback, and `zh-CN-XiaoxiaoNeural` or `zh-CN-XiaoyiNeural` for female narration.
- Use macOS `say` only as an offline fallback. Prefer `Tingting` if it is the only available local Chinese voice, record the fallback reason, and inspect pronunciation before delivery.
- Generate one audio file per scene under `audio/scene-XX.mp3` or `audio/scene-XX.m4a`.
- Keep one source of truth for timing: split narration by scene, read the real audio duration, write it into `storyboard.json`, and use those durations to drive scene cuts, captions, and segment length.
- Do not use one full narration track with hand-guessed subtitle timings unless you verify the sync by inspection and document why per-scene audio was not possible.
- Keep BGM under the voice. Default BGM volume is `0.10-0.15`; reduce or remove BGM when it hurts clarity.

Caption and motion requirements:

- Captions must match the current scene's spoken idea. They can be concise summaries, but they must not drift away from the voiceover.
- Keep subtitle lines inside the selected target safe area. If a line is long, rewrite it or split it before rendering.
- Avoid jittery Ken Burns effects on still images. Do not use continuous frame-by-frame zoom/position changes unless tested and visually smooth. For static AI images, prefer cuts, short fades, and subtle overlay changes.
- If the user complains about shaking, disable background pulse effects, moving crop windows, and animated equalizer bars, then rerender.

### 5. Validate And Render

Run:

```bash
npx hyperframes lint
npx hyperframes inspect --samples 15
npx hyperframes render --quality standard --output <work-dir>/final.mp4
```

Fix lint and inspect errors before final render. If rendering fails, run `npx hyperframes doctor` and address the reported issue.

Quality verification after render:

- Decode-check the MP4.
- Confirm the final output matches the selected target resolution/aspect ratio and has audio when narration is required.
- Confirm transition/page-insert SFX are present when the composition uses page switches, proof-panel insertions, or card assemblies; keep them below the voice.
- Confirm important screenshots or generated proof frames were captured or generated at a resolution appropriate for the final canvas.
- Confirm `storyboard.json` exists, every scene has real duration fields, and the final MP4 duration is within 0.5 seconds of the storyboard total unless an intro/outro or transition tail is documented.
- Confirm `metadata.json` records final video path, duration, file size, scene count, voice, speed, template preset, BGM setting, target resolution, and FPS.
- Extract at least 5-6 keyframes across the full video. Verify that visuals change by scene, captions are not clipped, and the frame does not appear to shake.
- For every dense scene, inspect at least one full-size frame to verify images/cards/pages do not cover or crowd Chinese headlines, subtitles, captions, or CTAs.
- Inspect generated images for pseudo-Chinese, unreadable text, risky words, fake claims, contact details, QR codes, or fake badges. Regenerate or cover with clean HyperFrames text if any appear.
- Check that voice, caption, and scene topic are aligned at those keyframes.
- Run the beginner clarity and voice-to-visual sync review from `references/beginner_visual_sync_rules.md`. Reject the render if a beginner cannot understand the topic, first action, convenience promise, or why the current image matches the current narration.
- Listen to a representative opening, middle, and ending voice segment. If pronunciation sounds robotic, unstable, or misreads tool names, regenerate the affected scene audio before delivery.
- Check that BGM, if used, stays below the narration and does not mask Chinese consonants or key tool names.
- Watch or inspect the first 5 seconds as a separate retention test. If it lacks hook power, interaction, or visual premium quality, revise and rerender.
- Verify that every scene has a meaningful interaction, reveal, transition, or visual change that supports the narration.
- Reject the render if the only visible motion on a still image is scale-up/scale-down/pulse. Replace it with a fly-in, insertion, mask reveal, split-screen slide, parallax layer, cursor-led focus, or proof-wall assembly.
- Reject the render if 1080p screenshot-heavy scenes look soft or low-texture. Recapture assets or rerender/re-encode at higher quality before delivery.
- Run the script scoring gate, visual scoring gate, and simulated viewer review before upload. If any fail, revise and rerender.
- Confirm the audience value gate from `references/beginner_visual_sync_rules.md` still passes after editing and rendering.
- Check at least one early keyframe and one late keyframe for unwanted bottom/footer labels, watermarks, draft notes, or internal production text. Remove them before delivery.
- Verify the cover assets before upload: vertical cover, horizontal cover, and first-frame poster must be readable, poster-like, and free of internal production labels.
- During Douyin upload, check the cover status in the creator page. If the page still shows cover quality suggestions, fix the cover before publishing unless the user explicitly says to ignore it.
- If multiple output filenames exist, copy the approved final render over the commonly opened path so the user does not accidentally review an old render.

### 5.5. Simulated Viewer Review

Before delivery or publishing, simulate a real Douyin viewer seeing the video in-feed.

Review from three perspectives:

- Busy viewer: would they stop in the first 2 seconds?
- Practical learner: do they understand the value and want to save it?
- Aesthetic viewer: does the design feel premium enough to trust?

Answer these questions:

- Where would the viewer want to swipe away?
- Which sentence sounds unnatural or boring?
- Which visual feels cheap, static, unclear, or too template-like?
- Is there a clear reason to watch until the ending?
- Is there a clear reason to save, comment, or share?

If the simulated review finds a serious weakness, fix it before publishing. Do not merely document the weakness unless the user explicitly asks to proceed anyway.

Record the simulated viewer-review result in `production-notes.md`.

### 5.6. Post-Publish Learning Loop

For this user's daily workflow, do not wait passively for performance data when a previous video was published by this skill. On the next production day, before choosing the new topic, open Douyin creator analytics with the currently logged-in Chrome session and review the previous day's published work when accessible.

Useful data:

- Views.
- 2-second hold rate if available.
- 5-second hold rate if available.
- Average watch duration.
- Completion rate.
- Likes, comments, saves, shares.
- Negative comments or user confusion.
- Cover click or cover-quality signals if visible.

Analyze:

- Did the first 5 seconds work?
- Did viewers stay through the middle?
- Did the ending create saves or comments?
- Which topic, hook, visual style, or caption format performed best?
- What should be repeated, changed, or banned next time?

Required next-day review behavior:

- Check yesterday's video before researching today's topic whenever a previous published video exists and analytics are accessible.
- Check the latest relevant production folder for `metadata.json`, `storyboard.json`, and `production-notes.md` so successful voice, speed, template, BGM, and render settings can be reused when appropriate.
- Record the checked date, video title, publish time when visible, and available metrics in the new `production-notes.md`.
- If exact retention metrics are not available, use visible proxy signals such as views, likes, comments, saves, shares, audience comments, and platform suggestions.
- Convert the result into creative decisions for today's video: hook style, topic type, script pacing, visual density, cover direction, caption length, or hashtag choices.
- If login expires, analytics are delayed, the page requires SMS, or data is unavailable, record the blocker and continue with today's production using the latest available lesson.
- Do not store cookies, passwords, SMS codes, or private account secrets while reviewing analytics.
- When the user explicitly asks to update long-term rules from performance results, update this skill with the new account-specific lesson.

### 6. Publish Package

Production archive can include:

- `final.mp4`
- `cover.jpg` or `cover.png`
- `caption.txt`
- `storyboard.json`
- `metadata.json`
- `production-notes.md`
- `reference-analysis.json`
- HyperFrames project source

Rule publishing:

- When publishing the skill or its rules online, read `references/pixelle_pipeline_lessons.md` and follow the `Online Rule Publishing` section.
- Publish only skill source files and required references/scripts. Do not publish generated videos, temporary frames, account screenshots, cookies, credentials, or private production outputs.
- If the target repository or publishing channel is not known, stop after preparing the local skill and report the missing target instead of guessing.

User-facing delivery defaults:

- The final clickable output folder should contain only the approved finished MP4 unless the user explicitly asks for source files, images, ZIP, cover, or notes.
- After the user confirms the final version, remove temporary render files, sampled reference frames, generated working images, old video versions, ZIPs, and draft media from the delivery folder.
- Keep the final filename stable so the user can reopen the same path without wondering which render is current.
- In the final response, the first deliverable link must be the absolute clickable `delivery/` folder path, not only `delivery/final.mp4`. The user wants to click the folder directly and view the finished video there.
- A direct `delivery/final.mp4` file link may be included after the folder link, but it must not replace the folder link.
- Label the folder link clearly, such as `成片文件夹`, and avoid burying it under notes, metadata, or source-code paths.

The production notes must include:

- what was referenced
- what was changed
- reference duration and final duration
- reference aspect ratio, resolution, and shot-structure breakdown when a local video was provided
- next-day or previous-video performance review when available, including metrics, interpretation, and how it changed the current creative plan
- candidate topic scores and viral breakdown
- topic deduplication check against recent local daily/test folders
- viewer psychology plan: target viewer, core pain, curiosity gap, emotional promise, practical payoff, and retention path
- audience value plan: hook reason, watch reason, save reason, share reason, and trust reason
- script score and rewrite notes if any
- visual score and redesign notes if any
- simulated viewer-review result
- first-5-second hook strategy and whether it passed inspection
- visual system and interaction strategy
- plain-language topic, beginner repeat test, voice-to-visual sync result, image prompt quality result, and whether the video proves the software is convenient for a beginner
- storyboard path, template preset, voice ID, TTS speed, per-scene audio paths, and whether real audio durations were used
- BGM path, BGM volume, and whether BGM was reduced or omitted for clarity
- previous production metadata/storyboard reused, or a note that no suitable prior task was found
- evidence asset list, evidence score, and any missing-proof decisions for Codex/AI tool tutorial videos
- generated asset list
- Douyin risk checks
- public copy compliance result and generated-image text safety result
- free-first tool choices and any paid/cost-uncertain tool that was avoided or explicitly approved
- Douyin cover status and whether cover quality detection passed
- Qingdou sensitivity-word check result
- whether any parsing limitation occurred
- a clear note that platform review is not guaranteed

## Quality Bar

The final video should feel like the same content genre and pacing logic, but not a copy. Aim for a high-quality original remake: new visuals, rewritten narration, distinct layout, and safe publish copy.

If the user asks for “90% similar,” respond with a safer interpretation: same category, beat structure, rhythm, and information hierarchy; original assets and copy.

Never deliver a remake that is only one image with narration, has obvious TTS pronunciation issues, has mismatched voice/subtitles, or uses shaky image movement. Fix these before final delivery.

Never skip the stable production contract for publish-ready work: `storyboard.json`, per-scene audio durations, and `metadata.json` are part of the deliverable unless the user explicitly asks for a quick draft.

Never silently compress a long reference into a short video. Match the source duration by default, or explicitly confirm and label the output as a condensed cut.

Never publish a video while Douyin still reports avoidable cover quality problems unless the user explicitly accepts that risk. A cover warning is not necessarily a violation, but it is a production-quality failure for this workflow.

Never treat topic selection, copywriting, or visual design as filler. This skill must behave like a premium short-video creative director: choose a topic with audience psychology, write copy people want to hear, design frames that feel crafted, and animate interactions that help the viewer stay until the end.

Never publish without passing the intelligent quality gates: viral breakdown, script score, visual score, first-5-second retention test, simulated viewer review, Qingdou compliance, and Douyin cover check.

Never deliver a tutorial where the topic is vague, the copy is professional-only, the image does not match the narration, or the software does not feel easier to use by the end.

Never rely on paid or cost-uncertain services when a free/local/currently available tool can produce the required quality. Ask before using cost-incurring image/video/avatar/voice services at scale.
