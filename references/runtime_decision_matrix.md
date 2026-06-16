# Runtime Decision Matrix

Use this before choosing Remotion, HyperFrames, FFmpeg, MoviePy, OpenMontage, Video-Use, Manim, or any render path.

## Codex Plugins Vs Video Runtimes

Use `references/codex_plugin_integration.md` when the task mentions Codex plugins, the six plugins, Browser, GitHub, Hugging Face, HyperFrames, OpenAI Developers, or HeyGen. This runtime matrix classifies video engines and adapters; the plugin integration reference classifies Codex plugin availability, auth/cost boundaries, and proof requirements.

## Six-Tool Codex Video Stack

Classify every named tool before planning or claiming production evidence:

| Tool | Current role in this skill | Availability class | Use it when | Evidence required |
| --- | --- | --- | --- | --- |
| HyperFrames | Final HTML/GSAP timeline, Chinese captions, safe zones, proof cards, SFX cues, inspect, render, and delivery. | Codex plugin/runtime when available; CLI may be invoked through `npx hyperframes`. | A finished publish-ready video, animated proof wall, caption-heavy tutorial, or premium QA render is requested. | Version/command output, composition path, inspect/contact sheet, rendered MP4, and QA report. |
| FFmpeg / ffprobe | Probe, trim, stitch, transcode, remux, loudness, audio mix, subtitle burn-in, frame extraction, and delivery checks. | Local CLI capability, not a Codex plugin. | Media operations are mechanical and no design/layout/animation decision is being made. | `ffmpeg`/`ffprobe` command output, stream metadata, duration comparison, and final codec/audio proof. |
| OpenMontage | Optional agentic production workflow reference or adapter for timeline/task decomposition. | External open-source project; not installed unless a local repo or explicit install approval exists. | The task needs multi-step production planning, shot/task graph ideas, or the user explicitly asks to use OpenMontage. | Local repo path or approved install, command/log evidence, output timeline/artifact, and license boundary note. |
| Remotion | React component motion, charts, data visuals, reusable caption templates, frame-accurate sequences, screen-recording composition, and clip generation. | Codex skill guidance is available; runtime is local only when a Remotion project/dependency or `npx remotion` command is used. | A scene needs React logic, reusable components, data visualization, or frame-accurate component clips. | Component/source path, preview/render command, still/frame check, rendered clip, and handoff to final timeline. |
| Video-Use | Optional agentic editing adapter for rough cuts from raw footage and open-source editing workflows. | External open-source project; not installed unless a local repo or explicit install approval exists. | The user provides raw footage or asks for agentic editing/rough cut workflows instead of pure generated scenes. | Local repo path or approved install, input footage manifest, edit command/log, output MP4, and QA pass. |
| Manim | Optional math/science/diagram animation clip generator. | External Python runtime; not installed unless local environment contains Manim or install approval exists. | A scene needs formula animation, geometry, process diagrams, graph motion, or precise technical explainer visuals. | Manim version/env, scene source file, render command, output clip, and assembly proof in HyperFrames or Remotion. |

Do not describe OpenMontage, Video-Use, or Manim as installed Codex plugins unless this session has real tool, file, command, or UI evidence. They can still be written into the plan as optional adapters with a blocked/needs-install status.

Payment rule: Codex features already available inside the user's paid Codex session are allowed. If any external runtime path requires paid credits, a paid subscription, a paid API key, or paid cloud rendering, do not use it. Record the path as `blocked_paid_feature` and switch to a Codex-included, free, local, or open-source route.

## Runtime Roles

- HyperFrames: final editorial timeline, HTML/CSS/GSAP motion, Chinese captions, proof cards, safe zones, SFX cues, inspect, render, and delivery.
- FFmpeg/MoviePy: trim, stitch, transcode, remux, loudness, subtitle burn-in, frame extraction, and media probes only.
- Remotion: React component motion, charts, data visuals, reusable caption templates, frame-accurate sequences, screen-recording composition, and clip generation.
- OpenMontage: optional production-planning adapter/reference for timeline JSON, task graph, and agentic production structure.
- Video-Use: optional raw-footage editing adapter/reference for rough cuts, timeline edits, and final MP4 workflows.
- Manim: optional formula, geometry, graph, and technical explainer animation clip generator.

## Decision Rules

Choose Remotion when a scene needs:

- frame-accurate React logic
- reusable subtitle/caption components
- screen-recording or data visualization composition
- a component clip later assembled in HyperFrames

Choose optional OpenMontage when:

- a local OpenMontage repo already exists or the user approves installing/cloning it
- the workflow needs task/timeline decomposition beyond this skill's native storyboard
- its output will still pass this skill's compliance, asset, frame, audio, and QA gates

Choose optional Video-Use when:

- the user provides raw footage, screen recordings, or interview/source clips
- the job is editing footage into a rough cut or final MP4, not generating proof from scratch
- its output will be checked with ffprobe/frame review and packaged through this skill's QA flow

Choose optional Manim when:

- the scene is mathematical, scientific, diagrammatic, or formula-heavy
- a precise generated clip is more valuable than a generic animated card
- the rendered clip can be assembled into HyperFrames or Remotion without breaking caption/audio sync

Choose HyperFrames when a scene needs:

- final layout and typography
- proof-card assembly
- Chinese caption synchronization
- GSAP-driven reveal/focus motion
- inspect/render QA

Choose FFmpeg/MoviePy only when:

- the task is mechanical media processing
- no design/layout/animation decision is being made

## Forbidden Runtime Workarounds

Do not use runtime tricks to hide thin content:

- page shaking
- random camera drift
- Ken Burns zoom as the main motion
- transition spam
- loop pulse with no information change
- claiming an optional external adapter was used without local evidence
- using FFmpeg/MoviePy as a substitute for visual direction or premium motion design
- using paid credits, paid subscriptions, paid asset libraries, or paid cloud generation to complete the scene

Instead, split the content into more scenes, enrich the proof, add designed steps, or use a better caption/focus cue.
