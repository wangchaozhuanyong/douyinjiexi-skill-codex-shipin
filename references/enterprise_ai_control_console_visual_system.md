# Enterprise AI Control Console Visual System

Use this for AI knowledge videos that should feel high-end, technological, precise, and unified. This is a visual system, not a pile of effects. It governs background inheritance, foreground components, captions, motion, transitions, sound effects, and QA.

## Core Positioning

The video uses a unified `enterprise AI computing console x cinematic data space` visual system.

Backgrounds provide depth, compute scale, network structure, particles, light flow, chips, circuits, neural nodes, and future atmosphere. Foreground HTML/CSS or vector layers present trustworthy information with precision, hierarchy, and readable logic. Motion expresses loading, analysis, verification, focus, and output.

The final image should feel like a live intelligent console inside a high-end AI product launch. Background depth creates the atmosphere; foreground modules carry the actual source, step, proof, comparison, caption, or state-change job for the current scene.

## One Style Per Video

At project start, select exactly one main background style from `references/ai_background_random_style_pool.md`. The selected style becomes the video's visual seed. Do not randomly switch among quantum blue, black-gold, silver lab, digital city, or other style families between scenes.

The entire video must inherit the selected style's:

- palette direction
- light source direction
- material family
- background depth behavior
- foreground panel language
- glass transparency profile and local readability treatment
- caption treatment
- transition language
- SFX character

Different shots may change camera scale, layout, information density, and focus state, but not the art direction system.

## Base Visual Tokens

Default enterprise AI console tokens:

```text
base_background: #050B18
deep_background: #081326
glass_shell: rgba(7, 18, 36, 0.08-0.16)
glass_reading_layer: rgba(3, 10, 18, 0.16-0.28)
glass_proof_layer: rgba(6, 18, 28, 0.12-0.24)
glass_caption_layer: rgba(3, 8, 14, 0.20-0.34)
primary_accent: #55DFFF
secondary_accent: #8F7CFF
tertiary_accent: #32E2C2
body_text: #F2F7FF
secondary_text: #A6B6C8
emphasis_or_warning: #FFC36B
panel_border: 1px ice-blue, 35%-55% opacity
panel_top_highlight: 1px white, 8%-12% opacity
panel_glow: 12px-22px blur, 12%-20% opacity
panel_backdrop_blur: 12px-18px
panel_radius: 8px-14px
spacing_grid: 8px
```

Glass Transparency v2 hard rule: foreground modules are transparent information layers, not solid cards. Large module fills must stay at or below alpha `0.34`, with the main shell normally at `0.08-0.16`. Do not use `rgba(..., 0.60+)`, opaque black plates, white boards, solid matte panels, or thick "safe" rectangles for fixed modules, captions, proof frames, checklist rows, source cards, or micro-components.

Adjust these tokens to the selected background family, but keep the same structural logic. For black-gold styles, increase champagne/amber accents and reduce cyan. For silver-white lab styles, raise silver/ice-blue surfaces and prevent overexposure. For emerald tunnel or bio-neural styles, use green as the active accent while keeping readable text neutral.

The technology feel comes from precision, layer hierarchy, material, light, and restrained motion. Accent colors support the selected background family instead of dominating the frame.

## Background And Foreground Fusion

Complex full-frame backgrounds are allowed, but every foreground text or content panel must create a local readability treatment underneath it.

When a foreground component appears:

- duplicate or sample the underlying background region
- apply 12px-20px Gaussian blur to that region
- reduce brightness by 18%-30%
- reduce saturation by 10%-18%
- add a soft feathered mask with 30px-60px feather
- place the transparent foreground glass or data panel above it
- keep the dynamic background visibly moving through the glass shell

The local quieting layer must never look like a hard black rectangle. It should feel like the console is temporarily damping the background behind active information. When the panel leaves, restore the local quieting layer over 180ms-260ms.

Local readability treatment is not a fallback to opaque cards. If text is hard to read, first tune blur, feather, text weight, shadow, and a small local reading layer. Do not darken the entire module or cover the background with a large solid plate.

Background motion policy:

- slow push-in: 100% to 102.5%
- duration: 4s-8s
- drift: 2px-8px horizontally or vertically
- subtle parallax between depth layers
- stable camera language with no attention-stealing movement

## Foreground Component Families

Components must match information function instead of repeating one card shape for every content type.

## Current-Scene Component Jobs

Every visible foreground structure must have a current-scene job. A card, frame, rail, divider, checkbox lane, connector line, source wall, terminal pane, or proof slot is created when it carries one of these:

- real proof or source content
- readable title, step text, checklist text, comparison text, or caption support
- active state such as current/completed/upcoming step
- a documented motion event such as scan, assemble, lock, focus, or converge
- local readability treatment under an active foreground element

If the scene does not need a foreground structure, use atmospheric depth, material, light, subtle particles, controlled vignette, and negative space. Historical empty-structure terms are checked by automated regression gates, not by repeating them during storyboard planning.

Every foreground structure that does appear must use the transparent glass system: shell, local reading layer, proof layer, or caption layer. Thick opaque panels, solid source cards, large white/cream boards, and black rectangles fail the visual system even when the text is readable.

### Opening Title: System Boot Module

Use for hooks and chapter starts.

Structure:

- one thin light line
- one small status node
- large Chinese title
- precise divider line below the title
- optional small system label only if it does not create fake terminal clutter

Motion:

- status node appears: 120ms
- divider line expands left to right: 220ms
- main title enters from y=12px with opacity 0: 260ms
- final lock pulse on node: 100ms

Rules:

- title width <= 65% of frame
- one to two lines only
- use a clean modern Chinese font
- no decorative sci-fi font
- do not stack many ornaments around the title

### Official Source And Evidence Screenshot: Data Archive Frame

Use for official docs, product screenshots, terminal proof, source pages, or file evidence.

Rules:

- preserve original screenshot colors, ratio, and sharpness
- do not put filters, scanlines, color shifts, glow, or fake overlays inside the screenshot content
- place the screenshot inside a dark data archive frame
- use a 1px ice-blue border and four short corner locator marks outside the screenshot
- optional small status node near the frame edge, never over evidence content

Motion:

- low-opacity scan light sweeps across the outer frame only: 180ms-260ms
- frame brightness increases once after scan
- then returns to stable state
- no persistent `SOURCE LOCKED` flashing

### Steps And Process: Modular Data Nodes

Use for step-by-step teaching, workflows, and prompt construction.

Structure:

- each step is an independent deep glass module
- a glowing connection port sits on the left edge
- modules connect through thin fiber lines
- lines route around captions and body text

State:

- current step: 100% brightness
- completed step: 65% brightness
- upcoming step: 38% brightness

Motion:

- content assembles from the connection port toward the right
- duration: 220ms-380ms
- do not pop the whole card in at once

### Comparison: Dual-Channel Analysis Panel

Use for before/after, wrong/right, manual/AI, or risky/safe comparisons.

Structure:

- left and right panels are symmetrical
- center axis uses a fine line, energy node, or scanning axis
- active side border lights up
- inactive side dims but remains readable

Rules:

- do not rely on giant red/green cards
- use layout, hierarchy, and focus state as the main contrast
- color is only a supporting cue

### Checklist And Conclusion: Node-Line Summary

Use for saveable lists, final takeaways, and recap frames.

Structure:

- each item = node + short connector + text
- completed state uses a stable light dot
- no oversized checkmark animation

Motion:

- node emits one small energy pulse
- connector extends right
- text fades in after the connector
- final scene may connect all nodes to a central core
- central core emits one low-frequency pulse only

## Caption System

Captions should feel technological but still belong to a professional explainer, not a game UI.

Rules:

- bottom safe area, 6%-8% above frame bottom
- low-opacity black-blue frosted glass capsule
- very weak ice-blue outline
- soft shadow
- max two lines
- line length must remain phone-readable
- normal text: warm white
- keywords: ice blue, cyan-green, or rare amber
- overall caption enters with 120ms-180ms fade
- keyword hit uses one brightness pulse or 1.02x-1.04x scale, not both
- no word-by-word bouncing
- no persistent flicker
- caption readability beats background and ornament layers

## Motion Vocabulary

Use only these five core technology motions unless a scene has a documented special reason.

### Scan

Purpose: evidence, screenshots, and key module verification.

- low-opacity scan light moves left to right
- duration: 180ms-260ms
- border briefly strengthens after scan
- never repeat at high frequency

### Assemble

Purpose: prompts, steps, modules, and data rows.

- content grows from a port or connector line
- duration: 220ms-380ms
- avoid whole-card pop-in

### Lock

Purpose: confirmed source, key point, final answer.

- status node tightens quickly
- border emits one brightness pulse
- duration: 80ms-140ms
- no continuous blinking

### Focus

Purpose: screenshot detail or key explanation.

- camera pushes in 1.5%-2.5%
- non-focus zones dim 8%-15%
- focus border brightens once
- duration: 500ms-900ms

### Converge

Purpose: final recap and summary.

- dispersed nodes connect through thin fibers
- data blocks move slightly toward a central core
- core emits one low-frequency pulse
- no explosive light burst

Use smooth easing:

```text
enter: cubic-bezier(0.22, 1, 0.36, 1)
exit: cubic-bezier(0.4, 0, 1, 1)
```

## Advanced Transitions Only

Ordinary page transitions are not allowed for publish-ready AI knowledge videos. Do not use plain fade, blur crossfade, hard cut, simple slide, push slide, or basic zoom as the main transition.

Use named advanced transition recipes that express a real information-state change:

- `source_focus_lens_reveal`: source/evidence appears through lens aperture, refraction, outer-frame scan, and one lock pulse
- `citation_rail_wipe`: citation rail sweeps the evidence edge and masks the next proof layer
- `comparison_split_handoff`: center axis transfers focus between before/after panels
- `operation_node_relay`: one active node emits a data packet that pulls the next workflow layer forward
- `terminal_scan_proof_tray`: terminal scan line reveals a proof tray or output state
- `template_lift_settle`: reusable template lifts from depth, locks, and settles for readability
- `final_controlled_zoom`: summary nodes converge into the final card with a restrained camera settle
- `prism_layer_refract` or `magnetic_data_rail_wipe`: use only when the scene has layered proof or data movement that justifies it

A full video should use at least three distinct advanced transition recipes. Repeating one effect across the whole video is considered monotonous and fails the high-quality bar.

One shot may have no more than two prominent simultaneous motions.

## Scene Transitions

Each video should choose one main transition and at most one auxiliary transition.

Recommended main transition:

- old scene's main panel dims
- panel compresses into a thin data layer
- a horizontal or diagonal data light rail crosses the frame
- new scene builds behind the light rail in layers

Rules:

- duration: 10-14 frames
- no white flash
- no full-screen blast
- no large rotation
- no transition covering active captions
- narration must continue without restart, mute, fade, or gap
- captions stay stable or end before the light rail enters

## SFX Rules

SFX are tactile feedback, not decoration.

Use:

- module appears: soft panel settle
- data node loads: subtle digital tick
- scan verification: light scanner sweep
- module lock: short clean lock click
- final convergence: low energy pulse

Animated icon audio:

- animated icon/status node: one short synchronized tick or lock click
- cursor click/cursor packet: one soft digital tick aligned to the visible click
- checklist mark/check state: short clean check tick
- proof tray lock or lock pulse: short clean lock click
- do not let any dynamic icon move silently unless it is purely decorative and removed from the scene

Storyboard requirement:

- every animated icon/status feedback event must create `sfx_cues`, `audio_cues`, or `icon_audio_cues`
- each cue needs timestamp, visual event, sound character, and mix role
- mix role must state 12dB-18dB below narration and no masking of Chinese voice

Mixing:

- 12dB-18dB below narration
- no explosion
- no electric noise bed
- no game-style heavy bass
- no exaggerated whoosh
- no high-frequency continuous beeps
- do not attach SFX to every tiny element in one shot

## English And System Labels

Technology feel must come from structure, hierarchy, light, material, and motion, not from piling up English labels.

Small English or system-like labels may appear sparingly as foreground HTML/CSS only, not baked into generated backgrounds. They must never imply fake official status, fake terminal proof, fake analytics, or fake system data.

Prefer Chinese content hierarchy. If English status labels are used, keep them short and rare.

## Required QA Checks

Before final render or promotion, inspect:

- still-frame check: any paused frame still looks like one AI visual system, not PPT over a wallpaper
- mute check: with audio off, title, proof, process, and key point hierarchy remain clear
- phone-size check: text and captions remain readable when scaled down
- grayscale check: foreground and background still have enough luminance contrast without color
- transparency check: text remains readable while the dynamic background is still visible through modules
- opaque-fill check: fixed foreground modules, captions, proof frames, checklist rows, and micro-components do not use large fills above alpha 0.34
- flicker check: fine grids, scanlines, and micro-patterns do not produce moire, jitter, or strobe
- authenticity check: official screenshots and source evidence are not filtered, color-shifted, overlaid, or turned into fake system data
- motion restraint check: no shot has more than two prominent simultaneous motions
- style-inheritance check: all shots keep the selected background style's palette, material, light direction, foreground language, transition language, and SFX character

If any check fails, restage or regenerate before final promotion.
