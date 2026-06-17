# HyperFrames Delivery Checklist

Use this before writing or rendering a HyperFrames remake project.

## Project Structure

Recommended output folder:

```text
<work-dir>/
  reference-analysis.json
  DESIGN.md
  index.html
  assets/
    scene-01.png
    scene-02.png
  renders/
    final.mp4
  publish/
    cover.jpg
    caption.txt
    production-notes.md
```

## Composition Requirements

- AI knowledge videos must use a 1920x1080 horizontal root composition.
- Do not create a 1080x1920 AI knowledge composition just because the video may be posted to Douyin.
- Root composition is a normal `<div data-composition-id="...">` in `index.html`; do not wrap the root in `<template>`.
- Every timed clip needs `id`, `data-start`, `data-duration` when applicable, and `data-track-index`.
- Video must be muted and paired with separate audio if audio is used.
- Timelines must be synchronous and registered in `window.__timelines`.
- Use finite animation loops; never `repeat: -1`.
- Use transitions between all scenes.
- Use entrance animations on every scene.
- Do not use exit animations before scene transitions except at the final scene.

## Visual And Text Requirements

- Create `DESIGN.md` before HTML. Define mood, palette, typography, and what not to do.
- Use generated images as visual scenes, not copied source frames.
- For 1920x1080 AI knowledge renders, design a wide proof-first canvas: large readable proof area, lower-third caption rail, and optional side annotation rail. Keep screenshots, code, cards, titles, subtitles, and CTA away from the frame edges.
- Add captions/subtitles as HTML text so they can be edited.
- Keep text large enough for mobile playback even in 16:9: headline 56px+, body/caption 26px+ in 1920x1080 renders.
- Avoid text overflows. Run inspect before render.
- Do not bake long Chinese text into generated images; keep text in HyperFrames.
- When generating images, prompt for a wide 16:9 stage with clean lower-third and side annotation space. Do not crop key objects, UI evidence, or Chinese labels into frame edges.

## TTS And Duration Lock

- Generate one TTS file per scene.
- Use normal Mandarin speed by default: `tts_speed` 1.0, acceptable default range 0.95-1.03. Do not use 1.1x/1.12x/1.2x to force a script into the target duration. A `1.1x` voice is allowed only when the user explicitly requests that voice style and the approval, provider, sample, metadata, and retimed audio lock are documented.
- After each scene TTS is generated, run `ffprobe` or `scripts/media_probe.py` to read the real duration.
- Write the real duration back to `storyboard.audio_locked.json` and to the source `storyboard.json` scene/director-shot timing.
- `storyboard.director_shots[*].duration_sec` and scene `duration_target` must match the real TTS timing within 0.3s before HyperFrames composition.
- HyperFrames scene durations must use the real audio durations.
- Do not hand-fill approximate scene timing.
- If subtitles do not fit the real audio duration, shorten the subtitle or regenerate that scene's voiceover.
- If voiceover does not fit, split the image into more visual beats or shorten the line. Do not accelerate narration.
- Do not render HyperFrames before `storyboard.audio_locked.json` exists.
- Preferred command:

```bash
python3 scripts/build_narration_bed.py \
  --storyboard outputs/demo/internal/storyboard.json \
  --audio-dir outputs/demo/assets/audio \
  --out-audio outputs/demo/assets/audio/narration-continuous.mp3 \
  --out-lock outputs/demo/internal/storyboard.audio_locked.json
```

## Continuous Narration Bed

Scene transitions must not stop the voice. Treat transitions as visual-only and keep narration independent from scene containers.

- Generate one editable TTS file per scene, then concatenate or remux the locked clips into `assets/audio/narration-continuous.*` for final HyperFrames render.
- Put the final narration as a root `<audio>` clip, not inside a timed scene `<div>` or sub-composition. Use its own track, for example `data-track-index="20"`, `data-start="0"`, `data-duration="<full_video_duration>"`, and `data-volume="1"`.
- If a project cannot use a single continuous file, per-scene audio clips must still be root-level audio clips scheduled back-to-back. The planned gap across scene boundaries must be `<= 120ms`.
- Visual scene clips may overlap, blur, push, or zoom during transitions, but they must never animate, fade, mute, pause, restart, or clip the narration.
- SFX and BGM must use separate audio tracks below the voice. Duck BGM under narration; keep pop/whoosh effects subtle and shorter than the visual event.
- Intentional silence must be written in the script as a pause or breath, not caused by transition timing or missing audio.
- `storyboard.audio_locked.json` must include `sync.narration_track`, `sync.transition_audio_policy`, `sync.max_audio_gap_ms`, and `sync.audio_bridge` for every scene.
- `metadata.quality_spec.narration_continuity_policy` must describe the continuous root narration strategy before technical QA.

Example root narration:

```html
<audio
  id="narration"
  data-start="0"
  data-duration="30"
  data-track-index="20"
  src="assets/audio/narration-continuous.mp3"
  data-volume="1"
></audio>
```

QA requirements:

- Compare final audio and video duration with `ffprobe`; audio must not be shorter than video beyond the configured duration gap.
- If a HyperFrames render cuts the tail or drops audio across transitions, remux the full continuous narration file back into the video and rerun technical QA.
- Reject any project where transition timing causes the voice to restart, duck to silence, or leave a perceptible gap.
- If HyperFrames output contains scene audio or truncated audio, remux the continuous root track:

```bash
python3 scripts/remux_root_audio.py \
  --video outputs/demo/internal/draft_scene_audio.mp4 \
  --audio outputs/demo/assets/audio/narration-continuous.mp3 \
  --out outputs/demo/internal/draft.mp4

python3 scripts/check_audio_continuity.py \
  --video outputs/demo/internal/draft.mp4 \
  --lock outputs/demo/internal/storyboard.audio_locked.json \
  --out outputs/demo/internal/audio_continuity_report.json
```

## Commands

Run from the HyperFrames project directory:

```bash
npx hyperframes lint
npx hyperframes inspect --samples 15
npx hyperframes render --quality standard --output renders/final.mp4
```

If render fails:

```bash
npx hyperframes doctor
```

## Final Package Notes

`production-notes.md` should include:

- reference link or share text
- analysis summary
- generated scene list
- image prompt list
- what changed from the source
- compliance/risk checklist
- final file paths
- note that Douyin review is not guaranteed
