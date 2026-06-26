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

- Proof-heavy AI knowledge videos must use a 1920x1080 horizontal root composition.
- Do not create a 1080x1920 AI knowledge composition just because the video may be posted to Douyin. Exception: if `references/reference_driven_production_rules.md` routes a vertical reference into lightweight AI guide/list/card/poster mode, use a 1080x1920 root composition with mobile safe zones and the same originality/text QA gates.
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
- For this user's recurring AI knowledge / daily AI tip videos, use the standing male-voice direction unless the user says otherwise: firm, energetic, professional Chinese male lecturer; preferred free-first Edge voice `zh-CN-YunyangNeural`, provider rate around `+10%`, and metadata/audit fields documenting the male voice choice and approval basis.
- If an automation prompt, old note, or copied instruction still says `1.2x` or `约 1.2 倍语速`, ignore that legacy speed request and follow the current hard gate: provider rate may be around `+10%`, but metadata `tts_speed` must stay `<= 1.10` with approval fields and real audio lock evidence.
- After each scene TTS is generated, run `ffprobe` or `scripts/media_probe.py` to read the real duration.
- Write the real duration back to `storyboard.audio_locked.json` and to the source `storyboard.json` scene/director-shot timing.
- `storyboard.director_shots[*].duration_sec` and scene `duration_target` must match the real TTS timing within 0.3s before HyperFrames composition.
- HyperFrames scene durations must use the real audio durations.
- Do not hand-fill approximate scene timing.
- After the lock, every narrated scene must expose enough `beat_map`, `visual_beats`, or equivalent timing records for the locked audio. Use one visible information beat per 5 seconds at minimum.
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

## Male Voice Thickness And Voice/SFX Mix

For this user's AI knowledge videos, the default spoken narration should sound like a firm, energetic Chinese male lecturer. It must be audible, thick enough, and clean. Do not treat "powerful voice" as only louder audio.

When the user says the voice is too small, not thick enough, or SFX disappeared, rebuild the root audio mix instead of only raising MP4 volume.

Required principles:

- Keep narration as the first-priority track.
- Keep SFX as tactile support; it should be audible on transitions and module locks, but below speech.
- Animated icons/status feedback must not be silent. Cursor clicks, lock pulses, checklist ticks, status nodes, and proof-tray locks need synchronized short SFX cues, scheduled on a root-level SFX track and mixed below narration.
- Do not use FFmpeg `amix` default normalization for voice plus SFX. Default `normalize=1` can make narration quieter and make SFX feel missing. Use `normalize=0` with explicit gains.
- Do not attach SFX or narration to visual scene containers.
- Keep a real QA report with source voice level, SFX level, final mix level, audio/video durations, blackdetect result, and silencedetect result.

Default thick male recipe for Edge TTS `zh-CN-YunyangNeural`:

- Generate with provider rate around `+10%`.
- If the user asks for a deeper or thicker voice, generate with a slightly lower pitch such as `-8Hz`.
- Post-process the continuous narration with:
  - highpass at `65Hz` to remove rumble
  - `120Hz +4.2dB` for chest/body
  - `220Hz +2.5dB` for warmth
  - `3200Hz +1.2dB` for intelligibility
  - light compression around `threshold=-20dB`, `ratio=2.8`, `attack=8`, `release=95`, `makeup=2.2`
  - limiter around `0.88-0.90`
- Mix narration and SFX with explicit gains. A good starting point is narration `1.35-1.55`, SFX `0.45-0.60`, `amix normalize=0`, limiter `0.88`.
- Do not accept a mix where SFX only exists on paper. Run an audibility check: `source_sfx_max_volume + 20log10(sfx_gain)` must be at least `-15dBFS`. If it is lower, raise SFX gain, rebuild the SFX bed, or preserve the approved final voice/video and overlay the root-level SFX bed with a limiter.
- If the user likes the video and voice but says transition SFX is missing, do not rebuild the full video. Copy the approved final MP4 to a backup, overlay the fixed SFX bed on the existing final audio with `amix normalize=0`, verify no clipping, then replace `final/final.mp4`.

Expected QA targets:

- Final video audio duration must match video duration within the normal audio continuity threshold.
- `volumedetect max_volume` should usually land around `-3dB` to `-1dB`, never clipping.
- `silencedetect=n=-45dB:d=0.75` should not find unintended narration gaps.
- `blackdetect` should not find visual black gaps.
- If SFX is inaudible, raise SFX gain before raising full mix volume.
- `voice_mix_report.json.sfx_audibility.status` or `sfx_audibility_report.json.status` must be `passed`; checking only cue metadata is not enough.
- If speech becomes boomy or muddy, reduce the `120Hz` and `220Hz` boosts before lowering narration gain.
- If speech is thick but hard to understand, add a small `3000-3600Hz` clarity boost rather than increasing speed.

Reusable command path:

```bash
python3 scripts/mix_voice_sfx.py \
  --video outputs/demo/internal/draft_voice_timing_render.mp4 \
  --voice outputs/demo/assets/audio/narration-continuous.wav \
  --sfx outputs/demo/assets/audio/dynamic_metal_sfx_bed.wav \
  --preset thick-male \
  --voice-gain 1.38 \
  --sfx-gain 0.50 \
  --out outputs/demo/internal/draft_with_thick_voice.mp4 \
  --report outputs/demo/internal/voice_mix_report.json
```

## SFX-Only Dynamic Audio

When the user asks for "配音的音效" on transitions or dynamic moments, do not interpret that as a full narration request. Build an SFX-only bed unless the user explicitly asks for spoken voiceover.

- SFX can mark transitions, cursor clicks, module lock, proof tray settle, scanner pass, output reveal, and final convergence.
- If a dynamic icon/status node/lock pulse/check mark is visible, it needs an event-level cue in the cue sheet; do not ship silent animated icon feedback.
- Use one root-level SFX audio bed or root-level SFX clips; never attach audio to visual scene containers in a way that restarts during transitions.
- Keep SFX short, tactile, and meaningful. One visual event should usually get one sound cue.
- If narration exists, SFX stays 12dB-18dB below the voice and must not mask Chinese speech.
- If narration does not exist, SFX still stays restrained; do not replace missing narration with loud game-style effects.
- Avoid explosion sounds, electric buzz, harsh glitch noise, high-frequency beeps, repeated whoosh spam, or heavy bass drops.
- Record a cue sheet with time, event type, sound character, and whether the project has narration.

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
python3 scripts/write_hyperframes_render_profile.py --project outputs/demo
npx hyperframes lint
npx hyperframes inspect --samples 15
npx hyperframes render --format png-sequence --fps 30 --protocol-timeout 900000 --workers 1 --output internal/hf_frames
```

For the stable production route, use the generated profile values and export PNG sequence before FFmpeg encoding:

```bash
cd outputs/demo
npx --yes hyperframes render \
  --format png-sequence \
  --fps 30 \
  --protocol-timeout 900000 \
  --workers 1 \
  --output internal/hf_frames

cd -
python3 scripts/repair_hyperframes_leading_frames.py --project outputs/demo
```

Do not render by passing `index.html` or `assets/hyperframes/index.html` as the CLI target. The generated `hyperframes_render_profile.json` must use `render_target=project_directory` and `command_cwd=<project>`.

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
