---
name: douyin-hyperframes-remake
description: Analyze a Douyin/TikTok-style video link or share text and remake it as an original short-video production using the local Douyin parser, gpt-image-2/image generation, and the HyperFrames plugin. Also use for the user's daily AI tips publishing workflow that researches hot Codex/Gemini/ChatGPT/AI-video/AI-coding topics, creates an original video, checks copy with Qingdou, and publishes to Douyin. Use when the user sends a Douyin link and asks Codex to reference, remake, recreate, or produce a new publish-ready Douyin video with AI-generated images, captions, cover, compliance checks, and a rendered MP4/ZIP package.
---

# Douyin HyperFrames Remake

## Purpose

Turn a user-provided Douyin link or share text into an original 9:16 short-video package: reference analysis, storyboard, generated image prompts/assets, HyperFrames composition, rendered MP4, cover, caption, and publishing notes.

Do not create a low-effort copy. If the user asks for very high similarity, treat it as reference structure and pacing only: use new visuals, rewritten copy, new captions, and a distinct creative angle.

## Required Tool Order

1. Use `scripts/analyze_reference.py` to extract the reference theme, tags, title direction, storyboard, caption, compliance sources, and originality threshold from the local Douyin parser.
2. After drafting the public caption, subtitles, and voiceover script, run local compliance checks and then check the text with Qingdou sensitivity-word detection at `https://www.qingdou.vip/pctool/sensitivity-word`. Use the user's current authorized session or credentials provided in the current conversation only; never write credentials into files, skills, logs, or GitHub.
3. If Qingdou or local checks report sensitive or risky words, rewrite the text and rerun the check until the script is clean enough to proceed. Do not start image generation, TTS, or rendering before this check passes.
4. Use image generation for needed visual assets. Prefer `gpt-image-2`/built-in image generation. Save final assets inside the project output folder.
5. Use the HyperFrames by HeyGen skills:
   - `hyperframes` for composition authoring rules.
   - `hyperframes-cli` for `npx hyperframes init`, `lint`, `inspect`, `preview`, and `render`.
6. Package the final deliverables: MP4, cover JPG/PNG, caption TXT, production notes, source HyperFrames project, and ZIP when useful.

## Workflow

### 0. Daily AI Publishing Automation

Use this workflow when the user asks for daily or scheduled Douyin publishing about AI tools and advanced usage.

Schedule default:

- Run every day at Beijing time 19:00 when configured as an automation.

Daily topic selection:

- Browse/search current and recent hot AI topics before writing.
- Allowed topic pool: Codex, Gemini, ChatGPT, AI video tools, AI coding tools, AI automation workflows, and advanced productivity techniques.
- Choose exactly one practical, high-value topic per day.
- Prefer fresh, high-interest, tutorial-friendly topics over generic introductions.
- Do not invent trend claims. If using a trend, base it on browsed sources and summarize the source signal in notes.

Daily production rules:

- Produce an original short video, not a copied reference.
- Title, voiceover, subtitles, publish caption, and hashtags must be written before generation.
- Hashtags must include `#gtp` and `#codex`, plus exactly three safe AI-related hashtags unless the user changes the rule.
- Keep the public caption short and clean.
- Run local compliance and Qingdou sensitivity-word checks before TTS, rendering, or publishing.
- If Qingdou flags a word, rewrite and recheck until clean or stop for user acceptance.
- Generate final video with natural Chinese voice, approximately `1.2x` speed, synchronized captions, premium varied visuals, and no internal labels such as `remake` or `重创重做版本`.
- Keep the delivery folder clean; user-facing output should contain only the approved final MP4 unless additional assets are requested.

Daily publishing authorization:

- The user authorizes routine steps without asking again: web research, copywriting, Qingdou checking, video generation, file cleanup, Chrome upload, filling title/caption/hashtags, selecting public/immediate publishing defaults, clicking publish, and using non-SMS verification methods that the current safety rules allow.
- SMS verification is not authorized and cannot be bypassed. If Douyin or another service requires a phone SMS code, stop and tell the user exactly what is needed.
- Do not guess, store, or reuse SMS codes, passwords, cookies, or account secrets.
- If a page requires a CAPTCHA or slider verification, follow the active browser safety rules; ask for user confirmation when required.
- If login expires or the platform requires a user-only action, stop with a short status and keep the relevant tab open when possible.

Daily publish report:

- Selected topic and why it was chosen.
- Source/trend summary.
- Final title, caption, and hashtags.
- Qingdou result.
- Final video folder.
- Douyin publish result or the exact blocker.

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

### 2.5. Mandatory Sensitivity-Word Check

Before generating images, TTS, subtitles, or final video, prepare the exact text that will be public-facing:

- voiceover script
- on-screen captions/subtitles
- title or cover text
- publish caption
- hashtags

Run the local compliance check first, then use Qingdou:

```text
https://www.qingdou.vip/pctool/sensitivity-word
```

Rules:

- Log in only with the user's authorized session or credentials provided in the current conversation.
- Never store the username, password, cookies, or screenshots containing private account details in the project, skill, notes, GitHub, or generated deliverables.
- Paste the full public-facing text into Qingdou before production.
- If Qingdou reports sensitive words, rewrite those phrases, then check again.
- Do not proceed to TTS, HyperFrames, or rendering until the final text has passed or the remaining risks are explicitly documented and accepted by the user.
- Record the final check status in `production-notes.md` as `Qingdou sensitivity check: passed` or include a short summary of unresolved items.

### 3. Generate Image Assets

Create 5-8 distinct scene prompts from the storyboard. Do not let the final video feel like one static image with minor variations. Each prompt should specify:

- 9:16 vertical composition
- subject and scene
- visual style derived from the reference category
- no text baked into the image unless absolutely necessary
- no platform logo, watermark, phone UI, celebrity likeness, or copied source-frame composition

Use image generation once per scene. Save assets in:

```text
<work-dir>/assets/scene-01.png
<work-dir>/assets/scene-02.png
...
```

If the subject is high-risk or fact-sensitive, generate abstract/editorial visuals rather than fake real evidence.

Before rendering, check a contact sheet or several still frames. If the scenes look too similar, generate or design more varied visuals before continuing.

### 3.5. Premium Visual System

Before writing HyperFrames HTML or generating final assets, create a premium visual direction in `DESIGN.md`.

Required visual decisions:

- Define a mature 4-6 color palette with named roles: background, surface, primary accent, secondary accent, text, muted text.
- Avoid cheap template palettes: pure neon cyan on dark teal, one-note blue-green screens, heavy purple-blue gradients, flat black backgrounds, or random rainbow accents.
- Use restrained contrast. Prefer deep charcoal, ink, graphite, off-white, warm gray, muted cobalt, silver, glass, or subtle amber accents when appropriate for AI topics.
- Use 1-2 accent colors only. Accent colors should guide attention, not flood the whole page.
- Use layered depth: subtle grain/noise, soft shadows, thin keylines, translucent panels, or editorial lighting. Do not use generic glow blobs, bokeh circles, or decorative orbs.
- Typography must feel editorial or product-grade: clear hierarchy, generous line height, no cramped text, no tiny labels, no negative letter spacing.
- UI diagrams should look like a polished product demo or premium keynote slide, not a rough wireframe.
- Do not let all scenes share the same background color and layout. Vary composition through diagrams, close-up panels, comparison tables, process flows, code/editor-inspired screens, and abstract system maps.
- Captions should sit in a deliberate safe-area container with enough padding and contrast; avoid large low-quality boxes that look pasted on.

Low-quality visual patterns to reject:

- Oversaturated gradients covering the whole frame.
- Excessive glow, blur, bloom, or fake glass effects.
- Random line diagrams without alignment, spacing, or visual hierarchy.
- Repeated dark teal backgrounds with white text on every scene.
- Large empty areas with one small diagram unless the emptiness is intentionally designed.
- Stock-looking AI brain/robot/circuit imagery unless it is transformed into a coherent visual system.

Validation:

- Extract 5-6 keyframes and judge color quality before final delivery.
- If the frame looks like a generic AI template, redesign the palette and layout before rendering.
- If the user complains that the page color or visual quality is low, treat it as a design failure and rerender with a stronger visual system.

### 4. Build HyperFrames Project

Read `references/hyperframes_delivery.md` before authoring. Use the HyperFrames CLI:

```bash
npx hyperframes init <project-name> --non-interactive
```

Requirements:

- 1080x1920 root composition.
- Use `DESIGN.md` before writing HTML. If no explicit style is supplied, derive a minimal style from the reference analysis.
- `DESIGN.md` must include the premium visual system: palette roles, typography, materials, layout rules, and explicit anti-patterns.
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
- Prefer a stable Mandarin voice such as `Tingting` when using macOS `say`; avoid voices that read Chinese with unstable pronunciation. Slow the speaking rate slightly when clarity matters.
- Prefer a natural online Mandarin TTS provider when available. For the user's local workflow, `edge-tts` with a Mandarin neural voice is the default free option before falling back to macOS `say`.
- Default final narration speed is approximately `1.2x` unless the user asks for slower or faster delivery. Apply speed changes after render or through scene audio timing, then verify the final duration and sync.
- Keep one source of truth for timing. Best practice: split narration by scene, generate one audio file per scene, read the real audio duration, and use those durations to drive scene cuts.
- Do not use one full narration track with hand-guessed subtitle timings unless you verify the sync by inspection.

Caption and motion requirements:

- Captions must match the current scene's spoken idea. They can be concise summaries, but they must not drift away from the voiceover.
- Keep subtitle lines inside the 9:16 safe area. If a line is long, rewrite it or split it before rendering.
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
- Confirm 1080x1920 vertical output and audio presence.
- Extract at least 5-6 keyframes across the full video. Verify that visuals change by scene, captions are not clipped, and the frame does not appear to shake.
- Check that voice, caption, and scene topic are aligned at those keyframes.
- Check at least one early keyframe and one late keyframe for unwanted bottom/footer labels, watermarks, draft notes, or internal production text. Remove them before delivery.
- If multiple output filenames exist, copy the approved final render over the commonly opened path so the user does not accidentally review an old render.

### 6. Publish Package

Production archive can include:

- `final.mp4`
- `cover.jpg` or `cover.png`
- `caption.txt`
- `production-notes.md`
- `reference-analysis.json`
- HyperFrames project source

User-facing delivery defaults:

- The final clickable output folder should contain only the approved finished MP4 unless the user explicitly asks for source files, images, ZIP, cover, or notes.
- After the user confirms the final version, remove temporary render files, sampled reference frames, generated working images, old video versions, ZIPs, and draft media from the delivery folder.
- Keep the final filename stable so the user can reopen the same path without wondering which render is current.
- In the final response, provide a direct clickable folder link first. Do not make the user hunt through nested project folders.

The production notes must include:

- what was referenced
- what was changed
- reference duration and final duration
- generated asset list
- Douyin risk checks
- Qingdou sensitivity-word check result
- whether any parsing limitation occurred
- a clear note that platform review is not guaranteed

## Quality Bar

The final video should feel like the same content genre and pacing logic, but not a copy. Aim for a high-quality original remake: new visuals, rewritten narration, distinct layout, and safe publish copy.

If the user asks for “90% similar,” respond with a safer interpretation: same category, beat structure, rhythm, and information hierarchy; original assets and copy.

Never deliver a remake that is only one image with narration, has obvious TTS pronunciation issues, has mismatched voice/subtitles, or uses shaky image movement. Fix these before final delivery.

Never silently compress a long reference into a short video. Match the source duration by default, or explicitly confirm and label the output as a condensed cut.
