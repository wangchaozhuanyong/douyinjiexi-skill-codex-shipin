# Video Quality Contract

V3 grades videos by evidence, clarity, sync, and replay value. Do not treat visual polish as a substitute for proof.

## Publishable

A publishable video is safe to release.

- `topic_score >= 8`
- `first_3_seconds_score >= 9.2`
- `first_5_seconds_score >= 9`
- `script_score >= 8.5`
- `semantic_review.status = passed`
- `semantic_score >= 8.5`
- `beginner_value_review.status = passed`
- `beginner_value_score >= 8.8`
- `save_value_score >= 8.5`
- `proof_score >= 8.5`
- `compliance_score >= 9.5`
- `empty_talk_ratio <= 0.18`
- `visual_score >= 8`
- `visual_review.status = passed`
- `aesthetic_score >= 8.2`
- `sync_score >= 9`
- `evidence_runtime_ratio >= 0.5`
- No black screen, white screen, no-audio output, frozen-frame section, or audio/visual sync failure.
- Captions stay readable and do not cover the UI, title, CTA, or important buttons.
- AI knowledge videos use a 1920x1080 proof-safe canvas with readable proof panels and lower-third captions. For non-AI 1080x1920 renders, critical content stays inside phone-safe margins: top >= 240px, bottom >= 360px, left >= 72px, right >= 180px. Generated images must have real breathing room, not just a later overlay mask.
- Backgrounds and foreground components must not contain unused frames, empty rails, blank cards, placeholder panels, decorative dividers, or layout skeletons. A visible frame is allowed only when it carries real proof, text, step state, comparison, checklist content, or a documented motion event in that scene. Empty "future content" structures are a blocking visual failure.
- Designed support cards and source-summary cards must not bake large blank highlight plates, empty glass slabs, decorative white/gold boards, or ornamental frames into the image. These cards are content sources only; readable labels, proof rows, checklist rows, callouts, and status modules must be rendered as controlled foreground HTML/CSS/GSAP layers. Any baked decoration that hides, washes out, or competes with text is a blocking visual failure.
- Fixed foreground modules, premium modules, captions, proof frames, source cards, checklist rows, and micro-components must use Glass Transparency v2. They must remain transparent enough for the selected dynamic MP4 background to stay visibly alive behind the content while text remains readable. Large background fills over alpha `0.34`, opaque black rectangles, white boards, solid cards, and thick matte safety plates are blocking visual failures.
- Readability must be created with local feathered backdrop blur, restrained dim/desaturate, text shadow, and measured type hierarchy. Do not solve readability by hiding the dynamic background under a full-card solid layer.
- Animated icons, status nodes, lock pulses, cursor clicks, checklist marks, proof-tray locks, and similar dynamic UI feedback must have synchronized short SFX cues in the storyboard. Silent dynamic icons are a blocking sound-design failure. These cues must sit 12dB-18dB below narration and must not mask, duck, restart, thin, or damage the Chinese voice.
- Narration uses normal speed by default (`tts_speed` 0.95-1.03, default 1.0). Accelerated TTS is a blocking quality failure unless the user explicitly requested that voice style for the current video, the speed stays `<= 1.10`, and provider/sample/approval/timeline metadata are documented.
- Narration metadata truthfully identifies the voice source and has an approved natural voice sample. macOS `say`, Apple/system voices, scratch timing previews, or relabeled local providers are not publish-ready unless the user explicitly accepts lower quality for that video.
- `storyboard.json` and `metadata.json` include `quality_spec` for publish-ready work.
- Every scene includes at least 3 `visual.design_layers` and passing `visual.quality_checks`.
- `qa_gate.py` must output `quality_level`.

## High Quality

A high-quality video is worth publishing with confidence.

- The first 3 seconds show a pain point, result, or counterintuitive claim.
- The first 5 seconds include at least 2 meaningful visual changes.
- A visual change happens every 3-5 seconds.
- A retention beat happens every 6-8 seconds.
- Transitions use named advanced recipes and show variety. Ordinary fade, blur crossfade, hard cut, simple slide, push slide, or plain zoom cannot be used as the main transition, and one repeated transition style across the whole video is a blocking quality issue.
- Dense steps are split into more images/cards instead of held as one crowded frame or compressed through fast speech.
- Named tools or skills have a complete proof chain: entry/source, visible operation, output/result, and viewer value.
- Codex Skill/plugin tutorial storyboards include `production_stack` and scene-level `visual.proof_chain` for every named primary tool.
- The visual system is documented in `quality_spec` and reused across cover, hook, proof scenes, captions, and recap.
- SFX policy is documented at event level, including icon/status cue timing, visual event, sound character, and voice-safe mix policy. The final mix is checked for voice clarity.
- Final render policy records `--quality high` or an equivalent high-quality H.264 pass.
- `evidence_runtime_ratio >= 0.6`
- At least one before/after comparison is shown.
- At least one reusable template, checklist, workflow, or decision rule is included.
- The cover is designed as a standalone poster, not a random frame grab.

## Breakout Potential

A breakout-potential video deserves extra production effort.

- The topic is painful enough that a beginner can explain why it matters in one sentence.
- The title promises a clear, non-exaggerated gain or correction.
- The video proves claims with real UI, real output, real commands, real files, or official documentation.
- Multi-tool videos show how the tools cooperate instead of presenting three isolated name cards.
- The copy is simple enough for a beginner to repeat.
- The viewer can act immediately after watching.
- The first action and saved step are concrete enough for a beginner to try without extra explanation.
- The comment section has natural prompts such as "template?", "how do I do this?", or "does this work for my case?"
- The save reason is obvious.
- The visual system feels like a product demo, not a text slideshow.
- The golden project still passes `scripts/check_golden_project.py`.

## Blocking Runtime Downgrades

Publish-ready AI videos must use HyperFrames as the actual final timeline. Do not accept wording such as `HyperFrames-compatible`, `compatible visual contract`, `FFmpeg-generated frame timeline`, `PIL+FFmpeg`, `card-only`, or `text-card slideshow` as a substitute. FFmpeg is allowed for mechanical encoding, probing, remuxing, and concat support after the real timeline is authored, but it must not be the visible full-frame card renderer.

If the contact sheet looks like repeated static white cards over a brown/orange or generic gradient background, repeated full-frame summary cards, or a PIL/canvas presentation rather than an enterprise AI control-console system with real layered proof surfaces, mark the video as `draft` or `failed`; do not run Qingdou or publish.

If a contact sheet shows decorative empty boxes, large blank cards, horizontal placeholder lines, unused rails, or background/foreground frameworks that are not actively used by the scene's information, mark the video as `failed`. Do not excuse these as "tech style", "future UI", or "layout atmosphere"; remove them and use atmosphere, material, light, depth, and negative space instead.

If `visual_regression_gate.support_card_blank_blocks.status` fails, the project must be restaged before final promotion. Do not fix it by lowering opacity, adding more glow, or hiding text with another overlay. Rebuild the support card as a clean content source or convert it into native HyperFrames foreground modules.

If foreground module render checks report `glass_transparency` failure, the project must be restaged before final promotion. Do not bypass this by marking the module as a support image or by baking the module into the background; fix the foreground CSS/DOM glass layers and rerun the render pack checks.
