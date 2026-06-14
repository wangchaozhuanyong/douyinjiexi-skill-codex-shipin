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
- Critical content stays inside phone-safe margins in 1080x1920 renders: top >= 240px, bottom >= 360px, left >= 72px, right >= 180px. Generated images must have real top/bottom breathing room, not just a later overlay mask.
- Narration uses normal speed (`tts_speed` 0.95-1.03, default 1.0). Accelerated TTS is a blocking quality failure.
- `storyboard.json` and `metadata.json` include `quality_spec` for publish-ready work.
- Every scene includes at least 3 `visual.design_layers` and passing `visual.quality_checks`.
- `qa_gate.py` must output `quality_level`.

## High Quality

A high-quality video is worth publishing with confidence.

- The first 3 seconds show a pain point, result, or counterintuitive claim.
- The first 5 seconds include at least 2 meaningful visual changes.
- A visual change happens every 3-5 seconds.
- A retention beat happens every 6-8 seconds.
- Dense steps are split into more images/cards instead of held as one crowded frame or compressed through fast speech.
- Named tools or skills have a complete proof chain: entry/source, visible operation, output/result, and viewer value.
- Codex Skill/plugin tutorial storyboards include `production_stack` and scene-level `visual.proof_chain` for every named primary tool.
- The visual system is documented in `quality_spec` and reused across cover, hook, proof scenes, captions, and recap.
- SFX policy is documented and the final mix is checked for voice clarity.
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
- The comment section has natural prompts such as "template?", "how do I do this?", or "does this work for my case?"
- The save reason is obvious.
- The visual system feels like a product demo, not a text slideshow.
- The golden project still passes `scripts/check_golden_project.py`.
