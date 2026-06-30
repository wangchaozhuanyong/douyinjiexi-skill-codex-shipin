# Free-First Open Source Stack

Use this before provider selection, asset planning, subtitle planning, storyboard validation, and QA.

## Default Provider Policy

Default to Codex-included, free, local, open-source, self-captured, or already-authorized tools. Third-party paid features are hard-disabled for this user: if an external provider, model, asset source, renderer, API, or subscription requires payment or credits, mark the step blocked and choose a Codex-included, free, or local alternative.

Allowed by default:

- Codex features already available inside the user's paid Codex session, including installed Codex skills/plugins and built-in generation tools exposed in the current session.
- Browser, GitHub, Hugging Face, HyperFrames, and OpenAI Developers plugin capabilities when they are available in the current Codex session and the operation is read-only, local, or already authorized. Use `references/codex_plugin_integration.md` for the exact boundary.
- FFmpeg and ffprobe for probe, transcode, remux, audio mix, and delivery checks.
- Whisper, faster-whisper, or whisper.cpp for transcription and captions.
- Remotion for component clips, caption templates, data visuals, and screen-recording composition.
- HyperFrames for final HTML/GSAP timeline, Chinese captions, SFX timing, inspect, render, and delivery.
- OpenMontage, Video-Use, and Manim only when already installed locally, present in an approved local repo, or explicitly approved by the user for setup. Treat them as optional adapters, not always-on Codex plugins.
- Self-captured screenshots, screen recordings, terminal output, files, docs, and real UI.
- Free/public sources such as Pexels, Pixabay, Archive, NASA, and Wikimedia only as support material with source/license notes.
- Background music from the local authorized library `~/Desktop/音乐/mp3` first; if no local track fits, use Pixabay Music or Mixkit Music first because they provide free stock music with clear usage terms. Record each selected track's source URL, license page, creator, download date, commercial-use status, attribution requirement, local path, duration, and hash.

Allowed cost exception:

- OpenAI/Codex capabilities already included in the user's paid Codex session are allowed and are not treated as paid blockers. Do not add new paid OpenAI API calls outside the Codex session, third-party AI providers, paid video APIs, or credit-consuming external generation without explicit approval.

Disabled:

- ElevenLabs, Runway, Kling, HeyGen paid generation, Resemble, Veo, paid stock sites, paid design/video platforms, subscription asset services, credit-based renderers, paid TTS, paid image/video generation APIs, Pinterest scraping, and any unapproved paid API.
- HeyGen avatar, presenter, lipsync, or Video Agent generation unless the user explicitly authorizes the account/auth/credit/upload path for the current task.

## Source Classes

Every storyboard visual and asset manifest item must use one of these source classes:

- `proof`: real UI, real recording, terminal output, local file, official doc screenshot, or actual result.
- `support`: diagram, B-roll, concept card, abstract visual, or explanatory design that supports but does not prove a claim.
- `generated`: AI-generated visual or ImageGen asset. Never use as real product proof.
- `free_stock`: free/public material with source, license, and role recorded. Never use as product proof.

## Music Source Boundary

Default BGM source order:

1. User-provided Douyin reference music for Douyin-to-Douyin output when a reference video has BGM.
2. Already-authorized local files in `~/Desktop/音乐/mp3` when this is not a reference-music case.
3. Pixabay Music.
4. Mixkit Music.
5. Other free/public sources only after checking the exact license for the track and recording the usage boundary.

Reject tracks when the source URL is missing, the license is unclear, commercial use is not allowed, attribution cannot be satisfied, the track is a repost of unknown origin, the music competes with narration, or the track is synthesized/generated as a replacement for a user-provided Douyin reference music request. If exact reference music is required but unavailable, stop for user confirmation instead of substituting.

## Learning Boundaries

Open-source projects downloaded under `/Users/wangchao/Desktop/开源视频学习-20260614/repos` are learning references only:

- Learn scene task structure from `short-video-maker`.
- Learn word/phrase caption components from `template-tiktok`.
- Learn local subtitle templates and render job states from `video-wizard`.
- Learn timeline JSON and runtime choice from `vanta` and `OpenMontage`.
- Learn raw-footage agentic editing boundaries from `Video-Use` only when the repo is available locally or the user approves fetching it.
- Learn formula/diagram animation patterns from `Manim`, but keep Manim output as a clip source that still passes this skill's final HyperFrames/QA pipeline.
- Learn screen-recording proof expectations from `coherence-studio`.
- Do not copy AGPL or non-commercial code.
- Do not import scraping behavior such as Pinterest scraping.
