# Codex Skill Tutorial Video Mode

Use this reference for Codex, Skill, Agent, HyperFrames, Imagegen, ChatGPT, Gemini, AI coding, and AI productivity tutorial videos, especially when the user provides a polished reference video and asks for the same quality level.

## Goal

Create a creator-grade product tutorial, not an AI ambience video. The viewer should feel:

- the topic is useful within the first 3 seconds
- the tools are real and can be found or installed
- the output quality is proven by visible examples
- the video has one coherent visual identity
- the ending gives a reason to save or share

## Reference Breakdown First

Before scripting or rendering, inspect the reference video and write a shot table in `production-notes.md`.

Minimum fields:

- timestamp range
- visual type: title card, real UI, screen recording, output proof, result grid, abstract transition, logo/brand, recap
- visible text or subtitle summary
- voice beat or narrative job
- motion: push-in, slide, light sweep, cursor move, zoom, grid reveal, hard cut, blur transition
- why it works

Also record:

- duration, resolution, and aspect ratio
- dominant background/material style
- font and subtitle style
- color palette and accent colors
- average shot length
- proof moments that make the video credible

Do not start production from memory or vibes when a local reference video is available.

## Local Video Inspection Fallbacks

When a local `.mp4` reference is provided, extract real metadata and keyframes before making creative decisions.

Preferred order:

- Use `ffprobe`/`ffmpeg` when available.
- If they are not in PATH, use project dependencies such as `imageio-ffmpeg` after installing `requirements.txt`.
- On macOS, use `mdls` for duration/resolution/codecs and Swift/AVFoundation or Quick Look thumbnails for representative frames.
- If only a few thumbnails can be extracted, still record that limitation and inspect the available frames before scripting.

Do not report that reference analysis is impossible just because one video tool is missing.

## Stable Production Layer

Also read `pixelle_pipeline_lessons.md` for storyboard, TTS, template, BGM, and metadata discipline.

For this mode:

- Create `storyboard.json` before asset generation or rendering.
- Default to Edge TTS `zh-CN-YunyangNeural` at `1.12` speed for Mandarin tutorial narration.
- Generate one audio file per scene, read real durations, and drive scene timing from those durations.
- Choose one template preset such as `proof-tutorial-horizontal`, `blackboard-grid`, or `product-demo-proof-wall`.
- Keep BGM at `0.10-0.15` volume or omit it when it weakens voice clarity.
- Create `metadata.json` after render with final path, duration, file size, scene count, voice, speed, template, BGM, resolution, and FPS.

Template stability must not replace evidence. Templates give rhythm and consistency; real UI, real files, and real outputs still carry credibility.

## Evidence-Led Structure

Default 60-90 second structure:

- 0-3s: cold open with one bold claim and a strong motion hook
- 3-8s: proof wall showing multiple outputs or product screens
- 8-12s: setup line that explains the promise
- 12-28s: tool/skill 1, including real UI proof and result proof
- 28-45s: tool/skill 2, including real UI proof and result proof
- 45-62s: tool/skill 3, including real UI proof and result proof
- 62-75s: comparison, recap, or decision rule
- final 2-4s: save/share reason or clean CTA

For each named tool or skill:

- show the name as a chapter card
- show where it exists or how it is installed/opened
- show one actual operation, command, search, upload, or generated file path
- show one concrete output
- say one practical reason the viewer should care

## Evidence Rules

At least 50% of runtime should be evidence:

- real Codex UI
- plugin or skill list/search page
- local folder/output files
- terminal/build/render result
- browser UI with product page or docs
- generated images, video frames, covers, or dashboards created during production
- before/after or four-grid proof wall

Do not fake real interfaces, fake product pages, fake official logos, fake install states, fake analytics, or fake customer results. If access is unavailable, use a clearly labeled concept shot or ask the user for access.

Generated images are allowed for:

- abstract transitions
- cover/poster frames
- stylized result examples when the narration does not claim they are real screenshots
- background texture or editorial atmosphere

Generated images are not enough by themselves for this mode.

## Visual System

A strong Codex Skill tutorial should feel like a premium product-demo lesson.

Reliable style choices:

- dark graphite, blackboard, or subtle grid background
- bold white Chinese headline text with soft shadow or dimensional depth
- one restrained accent color such as electric blue, violet, green, or amber
- product screenshots in clean rounded frames with thin keylines
- bottom subtitles in short, thick, high-contrast lines
- light sweeps, cursor motion, snap-in cards, proof grids, and controlled zooms
- chapter cards that use the same type scale and spacing every time

Avoid:

- random AI robot/circuit stock imagery
- generic neon template backgrounds
- one static image with voiceover
- excessive glow, shake, bounce, or pulsing
- tiny UI screenshots that cannot be read on a phone
- repeating the same layout for every tool

## Script Pattern

Write like a sharp Chinese creator teaching a useful shortcut.

Good patterns:

- `Codex 高手真正拉开差距的，不是提示词，而是这几个 Skill。`
- `第一个负责把网页变成视频，第二个负责把画面做出来，第三个负责把流程自动化。`
- `你不要只听名字，看它实际能产出什么。`
- `如果你每天都要做内容，这一步能省掉最烦的重复劳动。`

Bad patterns:

- `今天给大家介绍三个非常好用的工具。`
- `随着人工智能的发展，越来越多的人开始使用...`
- long feature lists without visible proof
- abstract claims such as `提升效率` without showing the workflow or result

Every 6-8 seconds, add a retention beat:

- a new tool reveal
- a before/after
- a real interface action
- a result grid
- a mistake correction
- a decision rule

## HyperFrames Direction

Choose aspect ratio deliberately:

- Match the reference aspect ratio when the user asks for this style.
- Use 1920x1080 for horizontal reference/tutorial videos unless the user asks for vertical.
- Use 1080x1920 for vertical Douyin feed-native videos.
- Keep all subtitles and key UI readable inside a central safe area.

Scene types to build:

- hook title card with grid, light sweep, and bold white typography
- proof wall with 2x2 or 3-card output grid
- real UI screenshot with cursor highlight and search/install motion
- chapter slate with `1. ToolName`, `2. ToolName`, `3. ToolName`
- before/after or input/output comparison
- generated-output gallery
- final recap strip with three chips and one save/share line

Motion should be restrained:

- fast opening snap or blur reveal
- smooth push-in on UI
- cursor path or highlight ring for real actions
- card slide/reveal for proof grids
- light sweep only on major titles
- no constant shake or decorative motion that does not explain anything

## Quality Gates

Before final render, score these from 1-10:

- Hook: would a viewer stop in the first 3 seconds?
- Evidence: is at least half the runtime real proof or output proof?
- Product clarity: can the viewer identify what tool is being shown and why?
- Visual identity: does the video feel like one designed piece?
- Subtitle readability: are all text lines readable on a phone?
- Rhythm: is there a new proof, reveal, or visual change every 3-5 seconds?
- Save value: does the ending give a repeatable list, rule, or workflow?

Passing threshold:

- Hook at least 9/10.
- Evidence at least 8/10.
- Visual identity at least 8/10.
- Overall at least 8/10.

If the score fails, do not publish. Fix the weak scenes and rerender.

## Production Notes Checklist

Record:

- reference metadata and shot table
- aspect ratio decision
- final structure with timestamps
- `storyboard.json` path and whether scene durations came from real audio
- TTS voice ID, speed, and pronunciation fixes for tool names
- template preset and BGM volume or omission reason
- `metadata.json` path after render
- evidence asset list and source
- missing evidence and how it was handled
- generated asset list
- script score
- evidence score
- visual score
- first-3-second hook review
- simulated viewer review
- Qingdou result when publishing copy is involved
