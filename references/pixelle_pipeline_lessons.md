# Pixelle-Inspired Production Discipline

Use this reference when a video should feel stable, listenable, repeatable, and less improvised. Borrow workflow ideas, not Pixelle source code.

## Contents

- Core Upgrade
- Borrowed Strengths Checklist
- Task Folder Contract
- Script And Storyboard Gate
- Stable TTS Defaults
- Timing Rule
- Template And Segment Pattern
- BGM Rule
- History Reuse
- Metadata
- Online Rule Publishing
- Acceptance Gates

## Core Upgrade

Before TTS, asset generation, HyperFrames authoring, or rendering, create a production contract:

```json
{
  "title": "video title",
  "config": {
    "task_id": "unique folder name",
    "target_width": 1920,
    "target_height": 1080,
    "fps": 30,
    "voice_id": "zh-CN-YunyangNeural",
    "tts_speed": 1.12,
    "template_id": "proof-tutorial-horizontal",
    "bgm_path": "assets/bgm.mp3",
    "bgm_volume": 0.12
  },
  "scenes": [
    {
      "index": 1,
      "voice": "spoken narration for this scene",
      "caption": "short on-screen subtitle",
      "visual_type": "real_ui | proof_grid | chapter_card | diagram | generated_transition",
      "evidence_source": "screenshot, recording, generated asset, or concept note",
      "audio_path": "audio/scene-01.mp3",
      "audio_duration": 3.2,
      "image_path": "assets/scene-01.png",
      "video_segment_path": "renders/segment-01.mp4",
      "duration": 3.2
    }
  ],
  "final_video_path": "delivery/final.mp4",
  "total_duration": 64.8
}
```

Store this as `<work-dir>/storyboard.json` and update it as assets are produced. Do not keep timing only in notes or in the renderer.

## Borrowed Strengths Checklist

When the user says to reference Pixelle, absorb these strengths into the current production:

- Task-level configuration: keep voice, speed, template, aspect ratio, FPS, BGM, and output paths in structured JSON, not scattered across notes.
- Storyboard-first workflow: approve scene count, scene purpose, voice line, caption, visual type, and evidence source before rendering.
- Stable voice defaults: use one known-good Mandarin neural voice and speed for a full production unless testing proves another voice is better.
- Real-duration editing: generated audio controls timing; video does not rely on guessed durations.
- Template discipline: choose a reusable visual preset for the whole piece, then vary scenes within that preset.
- Segment-based rendering: make scene-level assets and segments so weak parts can be replaced without rebuilding the whole film.
- BGM discipline: treat music as support for voice, not decoration that competes with narration.
- Metadata/history reuse: inspect prior successful outputs and reuse good production settings while still changing topics, evidence, captions, and factual claims.
- Final artifact traceability: the final MP4 should be traceable back to storyboard, scene audio, rendered segments, metadata, and production notes.

## Task Folder Contract

Use a predictable folder layout for publish-ready work:

```text
<work-dir>/
  DESIGN.md
  copy.md
  production-notes.md
  storyboard.json
  metadata.json
  qingdou-check-text.txt
  assets/
  audio/
  frames/
  renders/
  delivery/
```

If a quick draft skips any file, write that exception in `production-notes.md`. For final or publish-ready work, do not skip `storyboard.json`, `metadata.json`, per-scene audio, or `delivery/final.mp4`.

## Script And Storyboard Gate

Before TTS:

- The script must be split into scene-level spoken lines.
- Each scene must state why it exists: hook, proof, explanation, transition, comparison, recap, or CTA.
- Each scene must name its visual evidence or mark it as `concept` when no real proof is available.
- Captions must be shorter than the spoken line and readable inside the target safe area.
- The first 3-5 seconds must contain a hook, visual action, and payoff promise.
- For tutorial videos, evidence scenes must be at least half of the runtime target.

Reject the storyboard before TTS if it is only a slide list, if captions repeat the voice word-for-word, or if the visuals cannot prove the claim being narrated.

## Stable TTS Defaults

- Default Mandarin tutorial/daily voice: Edge TTS `zh-CN-YunyangNeural`.
- Default speed: `1.12`; acceptable range is `1.10-1.15` after listening.
- Male energetic fallback: `zh-CN-YunjianNeural`.
- Female clear fallback: `zh-CN-XiaoxiaoNeural` or `zh-CN-XiaoyiNeural`.
- macOS `say` is an offline fallback only. If used, record the reason in `production-notes.md` and check pronunciation carefully.
- Replace hard-to-pronounce English in the spoken text with Chinese or phonetic wording, while keeping display captions clean.

Generate one audio file per scene under `audio/scene-XX.mp3` or `audio/scene-XX.m4a`.

## Timing Rule

After generating scene audio:

- Read each audio file's real duration with `ffprobe`, `ffmpeg`, `imageio-ffmpeg`, or another reliable media probe.
- Write `audio_duration` and final scene `duration` back into `storyboard.json`.
- Use those durations to drive scene cuts, captions, and segment length.
- Do not hand-guess timings when audio exists.
- The final MP4 duration should be within 0.5 seconds of the sum of scene durations unless an intro/outro or transition tail is explicitly documented.

## Template And Segment Pattern

Pick one template preset for the whole video and record it in `storyboard.json` and `DESIGN.md`.

Useful preset names:

- `proof-tutorial-horizontal`: 1920x1080, blackboard/grid, real UI and output proof.
- `daily-ai-vertical`: 1080x1920, premium phone-readable AI tip structure.
- `premium-ai-card`: editorial card-heavy concept explainer.
- `blackboard-grid`: dark chalkboard/grid style for Codex/Skill tutorials.
- `product-demo-proof-wall`: result-grid and UI-evidence heavy structure.

Render scenes as controlled segments when practical:

- `frames/scene-XX.*` for still frames or snapshots.
- `audio/scene-XX.*` for scene voice.
- `renders/segment-XX.mp4` for each scene segment.
- `delivery/final.mp4` for the approved merged output.

Per-scene segments make it easier to fix a weak voice line, bad screenshot, or timing issue without rerendering everything.

## BGM Rule

- Use BGM only when it improves rhythm without hurting voice clarity.
- Default BGM volume: `0.10-0.15`.
- If the content is dense, technical, or the voice is already busy, reduce BGM or omit it.
- Record `bgm_path`, `bgm_volume`, and whether ducking/mixing was used in `metadata.json`.

## History Reuse

For daily or repeated video work, inspect the latest relevant task folder before production:

- `metadata.json`
- `storyboard.json`
- `production-notes.md`
- final MP4 duration and contact sheet if present

Reuse good voice, speed, template preset, BGM level, folder structure, and render settings when they still fit the new topic. Do not reuse stale topics, captions, screenshots, or factual claims.

## Metadata

Create `<work-dir>/metadata.json` after render:

```json
{
  "task_id": "folder name",
  "created_at": "ISO timestamp",
  "reference_source": "local mp4, Douyin link, or daily topic scan",
  "final_video_path": "delivery/final.mp4",
  "duration": 64.8,
  "file_size_bytes": 12345678,
  "scene_count": 8,
  "voice_id": "zh-CN-YunyangNeural",
  "tts_speed": 1.12,
  "template_id": "proof-tutorial-horizontal",
  "bgm_path": "assets/bgm.mp3",
  "bgm_volume": 0.12,
  "target_width": 1920,
  "target_height": 1080,
  "fps": 30
}
```

## Online Rule Publishing

When the user asks to publish these rules online:

- First determine the exact target: existing GitHub repository, private repo to create, public repo to create, Codex/plugin marketplace, or another deployment target.
- Do not assume public visibility. If a repository must be created and visibility is not specified, prefer private.
- Publish only the skill source files and required references/scripts, not generated videos, temporary frames, credentials, cookies, account screenshots, or user-private production outputs.
- If no remote repository, GitHub CLI, or connector capability can create the target, prepare the skill locally and report the missing publishing channel instead of pretending it is online.
- After publishing, verify the online file list includes `SKILL.md`, `agents/openai.yaml`, `references/pixelle_pipeline_lessons.md`, `references/codex_skill_tutorial_video.md`, `references/hyperframes_delivery.md`, `references/douyin_rules.md`, and required scripts.

## Acceptance Gates

Before delivery:

- `storyboard.json` exists and every scene has voice, caption, duration, and media path fields.
- TTS voice and speed are logged.
- Real audio durations are recorded; no scene uses guessed timing if audio was generated.
- Final duration matches the storyboard total within 0.5 seconds, or the difference is explained.
- Keyframe/contact-sheet review confirms each scene is visually distinct.
- BGM is audible but below the voice, or intentionally omitted.
- `metadata.json` records final output path, duration, size, voice, speed, template, and BGM settings.
