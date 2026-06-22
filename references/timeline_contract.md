# Timeline Contract

Use this before storyboard validation and before any render work.

## Required Timeline Fields

Every scene must define:

- one idea
- voice line
- proof or support asset
- asset source class: `proof`, `support`, `generated`, or `free_stock`
- caption template
- focus cue
- motion purpose
- premium motion craft: entrance, stagger, keyword motion, camera motion, layering, transition, caption motion, glow, audio response, and negative constraints
- transition recipe: scene-type motion recipe such as `source_focus_lens_reveal`, `citation_rail_wipe`, `comparison_split_handoff`, `operation_node_relay`, `terminal_scan_proof_tray`, `template_lift_settle`, or `final_controlled_zoom`
- narration continuity plan: root narration track, transition audio policy, maximum transition audio gap, and audio bridge
- voice direction plan: provider, voice id, gender/persona, rate, speed, sample path, and approval note when speed is outside the normal `0.95-1.03` range
- SFX cue or explicit no-SFX reason. Exception: animated icons/status feedback cannot use a no-SFX reason. Animated icon, status node, cursor click, lock pulse, checklist mark, proof-tray lock, and similar UI feedback require `sfx_cues`/`audio_cues`/`icon_audio_cues` with timestamp, visual event, sound character, and a note that the cue stays 12dB-18dB below narration without masking voice.
- safe-zone plan
- runtime choice

## Caption Template Library

Use multiple caption templates in publish-ready videos:

- `word_highlight`: phrase-level emphasis tied to spoken words.
- `side_label`: small side label for a proof detail or UI area.
- `proof_callout`: arrow/box/marker tied to real proof.
- `terminal_code_caption`: compact caption for terminal/code/file scenes.
- `chapter_card`: chapter title or numbered step.
- `final_takeaway`: clean recap or save-value frame.
- `bottom_light_caption`: restrained bottom caption when the frame already has strong proof.
- `comparison_label`: before/after or option comparison.

Avoid using one bottom caption style for the entire video unless the user explicitly requests a minimal style.

## Split Dense Images

If one image contains multiple steps, split it:

- 2 steps -> 2 scenes or 2 strong beats.
- 4 steps -> 4 scenes or 4 distinct visual reveals.
- Each split must add explanation, proof, callout, or design detail.

Do not rely on camera shake, zoom, or hard cuts to make a dense static image feel alive.

## Acceptance

The timeline passes only when:

- every scene has one clear idea
- generated/free-stock visuals are not treated as proof
- caption templates match scene type
- motion reveals information or guides attention
- every scene describes premium HyperFrames motion with executable values, such as `0.6s fade-up`, `0.12s-0.18s stagger`, restrained `1.03x` keyword pulse, `100%-103% camera push`, and `8%-18% glow`
- every scene chooses a named advanced transition recipe; ordinary fade, blur crossfade, hard cut, simple slide, push slide, or zoom are not acceptable as the main transition
- the full video uses varied advanced transition recipes rather than one repeated transition; publish-ready AI videos need at least 3 distinct advanced transition recipes
- every scene documents continuous narration fields: `narration_track`, `transition_audio_policy`, `max_audio_gap_ms <= 120`, and `audio_bridge`
- any `tts_speed > 1.03` is allowed only up to `1.10` with explicit user approval, a truthful voice sample, metadata, and audio-locked timings
- visual transitions do not pause, restart, mute, fade, or gap the voice
- animated icons/status feedback have synchronized SFX cues; the cues stay below narration and do not affect the human voice
- critical content stays inside safe zones
- scene changes occur because the idea changes, not because the frame felt static
