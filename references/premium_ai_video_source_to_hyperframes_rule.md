# Premium AI Video Source-to-HyperFrames Rule

This is the hard rule for making high-quality AI explainer videos. Do not start rendering from a generic script or repeated information cards.

## Required Order

1. Source research first.
2. Topic decision second.
3. Plain-language copy third.
4. Format decision fourth.
5. Rough duration estimate fifth.
6. Visual director script sixth.
7. Director gates seventh.
8. Read `references/visual_description_language_reference.md` eighth.
9. Read `references/visual_prompt_motion_phrasebook.md` and `references/ai_generated_asset_prompt_system.md` ninth.
10. Create `visual_style_decision.json` with Codex's style choice tenth.
11. Create `visual_style_plan.json` with brightness, palette, material, layout, dark/light rhythm, and diversity sequence eleventh.
12. Background, motion, asset, and evidence prompt plan twelfth.
13. Validate asset prompts, manifest, and visual tone thirteenth.
14. TTS/root narration and timeline lock fourteenth.
15. HyperFrames design system and composition fifteenth.
16. Render/remux, final text proofread, empty-frame check, visual diversity actual check, technical QA, visual review, provider audit, then promote final.

If any step is missing, the output is a draft and must not be called final.

## Visual Director Before HyperFrames

HyperFrames is the executor, not the director. Do not ask HyperFrames to invent the video from a script and generic premium style words. Before any HTML composition, create `storyboard.director_shots` and validate it.

The director script must answer:

- what the viewer sees in this shot
- the primary visual subject
- the camera scale and camera motion
- the operation or evidence action on screen
- the layout family
- whether it differs from the previous shot
- which on-screen text is approved for final render

Required machine-checkable shape:

```json
{
  "shot_id": "S01",
  "duration_sec": 3.0,
  "shot_type": "hook_conflict",
  "layout_family": "workspace_ui",
  "camera_scale": "macro_closeup",
  "camera_motion": "push_in",
  "visual_subject": "vague_task_brief_in_codex_like_workspace",
  "primary_action": "task_dropped_and_warning_badges_appear",
  "viewer_focus": "vague task text",
  "operation_elements": ["task_brief_panel"],
  "evidence": {
    "type": "none"
  },
  "on_screen_text": {
    "primary": "帮我改项目",
    "secondary": ["范围不清", "没有测试", "没有证据"]
  },
  "forbidden_risks": [
    "same_glass_card_layout",
    "tiny_unreadable_text",
    "empty_frame"
  ]
}
```

Reject storyboard plans that only describe "what is said" but not what the camera shows. Reject repeated card explainers even if the motion language is premium.

## Visual System Selector

Before writing background or support-image prompts, first lock a video-level style decision in `internal/visual_style_decision.json`, then write the matching visual system in `internal/visual_style_plan.json`.

`visual_style_decision.json` is the director judgment layer. It must read the selected topic, copy mood, evidence density, and reference-video rhythm/color/layout/music atmosphere when a reference exists. Learn reference rhythm and taste only; never copy the reference footage, people, subtitles, assets, or full sequence.

Required decision fields:

- `style_intent`
- `selected_brightness_grade`
- `selected_palette_family`
- `selected_material_family`
- `selected_layout_family`
- `why_this_style`
- `why_not_other_styles`

Allowed style intents include light tutorial, dark evidence, news editorial, blackboard grid, product launch, warning comparison, and vertical list. If rule matching is unclear, Codex must make the director call from the script and document the reason. Do not continue with `daylight_productivity`, light cards, dark graphite, or any previously successful style merely because it worked last time.

Required selectors:

- `scene_function`: hook, source_proof, tutorial_step, comparison, workflow, result, final_template.
- `visual_archetype`: for example bright productivity desk, source evidence newsroom, warm workshop board, editorial paper system, code lab bench, or cinematic product walkthrough.
- `brightness_grade`: L1 dark proof, L2 controlled dark, L3 balanced editorial, L4 bright tutorial, or L5 daylight result.
- `palette_family`: daylight productivity, warm paper cobalt, graphite ivory teal, amber result lab, or calm newsroom blue.
- `material_family`: paper acrylic, matte metal, editorial paper, browser chrome, code terminal, canvas board, or soft product plastic.
- `layout_family`: hero result center, before/after split, three-step ladder, evidence rail, timeline map, modular grid, or final checklist.

Hard rule: do not produce more than two consecutive dark scenes, do not let L4/L5 scenes render like charcoal glass cards, and do not use teal/blue as the only accent family across the whole video. Generated/support visuals must pass `scripts/validate_visual_tone.py` before HyperFrames composition.

## Pre-HyperFrames Director Gates

These gates run before composition:

- `Director Shot Schema Gate`: every shot has enum-like fields, a non-empty primary action, approved text, and a declared evidence type.
- `Visual Diversity Gate`: at least 4 shot types; no more than 2 consecutive shots with the same `layout_family`; at least 3 camera scales/motions combined.
- `Real Operation Feel Gate`: AI tool/tutorial videos need at least 2 operation shots and must cover at least two of `task_brief_panel`, `repo_or_file_tree`, `risk_list`, `test_or_check_output`, `evidence_result_card`.
- `Evidence Authenticity Gate`: source proof must be `real_source_crop`, `clean_citation_card`, or `abstract_non_official_diagram`; fake official screenshots and tiny unreadable source panels are blocked.

## Post-Render Gates

These gates run after render/remux:

- `On-screen Text Proofread Gate`: compare `render_text_manifest.json` against the storyboard-approved text. Large unapproved text is blocking.
- `Empty Frame Gate`: block accidental empty frames longer than 0.5s or frames without a primary subject.
- `Visual Diversity Actual Check`: the rendered contact sheet must still show the promised shot variety, not just one repeated layout.
- `Technical QA`: audio, duration, black/white/freeze, bitrate, resolution, and metadata consistency.

## Format Rule

AI knowledge videos must use 16:9 horizontal `1920x1080`. This includes AI news, AI tools, ChatGPT, Gemini, OpenAI, Codex, Agent, automation, AI coding, AI workflow, plugin, and Skill tutorials.

Do not switch proof-heavy AI knowledge videos to 9:16 just because the destination is Douyin. The output should remain a 16:9 proof-first master so source pages, code, browser screenshots, timeline diagrams, tool comparisons, and QA evidence stay readable.

Reference exception: if the user supplies a vertical reference and asks to match that style, and the result is a lightweight guide/list/card/poster explainer instead of proof-heavy screen teaching, use `references/reference_driven_production_rules.md` and allow a 9:16 `1080x1920` AI information-poster mode. Keep originality, source/evidence notes for factual claims, text accuracy <= 10%, safe zones, compliance, Qingdou, and QA gates.

Use 16:9 when the video needs:

- source pages, dashboards, code, browser screenshots, timeline diagrams, or tool comparisons
- a premium keynote / documentary / course-like feel
- large readable proof panels
- smoother scene continuity with fewer hard page cuts

Use 9:16 only for non-AI vertical-native work routed to another owning skill, or for the reference-driven lightweight AI information-poster exception above. Do not use 9:16 for proof-heavy AI knowledge/tutorial work under this skill.

## Source Standard

Every AI video needs at least three proof sources before copywriting. Prefer official product pages, docs, launch notes, demos, real screenshots, terminal logs, repo files, and local output artifacts.

Classify every source:

- `proof`: real official page, product UI, terminal, code, file output, log, QA result.
- `support`: generated background, metaphor image, diagram, abstract illustration.
- `generated`: ImageGen concept visual. It must never pretend to be a real UI, review, document, certification, or official screenshot.

AI videos without proof assets become card explainers and cannot meet the premium bar.

## Copy Rule

Write for ordinary viewers first. A good AI copy has:

- one clear topic
- one problem the viewer already feels
- one plain-language explanation
- one reusable checklist or method
- every important claim tied to proof

Avoid vague claims such as `AI is powerful`, `this changes everything`, `efficiency is higher`, or `agent era is here` unless the next scene proves the claim visually.

## Sentence-to-Visual Rule

Every sentence in the voiceover must become a visual task:

- explain a term
- reveal a source
- show a real operation
- compare before and after
- highlight a risk boundary
- build a checklist
- verify an output

Do not place the same card layout under different narration. If two adjacent sentences use the same structure, redesign one scene.

## ImageGen Prompt Quality Rule

Before generating any AI-made visual, read `references/ai_generated_asset_prompt_system.md` and create `internal/ai_asset_prompt_pack.md` or an equivalent production-notes section.

Use ImageGen only for cover, concept background, metaphor, or support visuals. Prompts must specify:

- exact video use case
- subject and visual metaphor
- 16:9 horizontal proof-first composition
- foreground, midground, background hierarchy
- material, lighting, lens, texture, and negative space
- color role and typography boundary
- what to avoid

Every generated visual prompt must also document:

- asset ID
- scene ID
- narration line supported
- viewer takeaway
- text-safe zones
- HyperFrames overlay/motion usage
- evidence boundary
- regeneration criteria

Prompt template:

```text
Create a premium editorial technology visual for a Chinese AI explainer video.
Subject: [specific AI concept], not a generic robot or neon dashboard.
Visual metaphor: [task enters console / evidence gate / tool network / verification pipeline].
Composition: horizontal 16:9, critical proof content inside a large center-left proof area, with lower-third caption space and a quiet side annotation rail.
Style: high-end product keynote, restrained cinematic lighting, real material depth, clean negative space.
Details: [specific panels, source wall, terminal, browser frame, verification gate], no logos unless provided, no fake UI proof.
Lighting/material: [matte graphite, glass layer, soft rim light, subtle shadow, realistic texture].
Avoid: generic cyber grid, random glowing lines, fake product UI, pseudo text, clutter, unreadable micro-labels, stock-photo look.
```

Generated support visuals must be documented in `asset_manifest.json` with `asset_source_type=generated` and cannot count toward proof runtime. Each generated visual must also record `provider`, `model`, `prompt_id`, `prompt_path`, `unique_prompt=true`, and `evidence_boundary`; valid generation providers are `gpt-image-2` or Codex built-in ImageGen. Local PIL/canvas/HTML placeholders do not satisfy the generated-image gate.

Visual asset director gate: every generated visual must also carry a complete shot brief, not just a style prompt. The prompt card and manifest entry must include `scene_id`, `narration_line_supported`, `visual_thesis`, `topic_binding`, `information_job`, `viewer_takeaway`, `composition`, `foreground`, `midground`, `background`, `camera_lens`, `lighting`, `material_texture`, `color_hierarchy`, `text_safe_zones`, `motion_usage`, `animation_affordance`, `evidence_boundary`, `negative_prompt`, and `regeneration_criteria`. If a prompt only says `高级科技感`, `未来感`, `赛博`, `酷炫`, `震撼`, `4K`, `cinematic`, or `premium tech`, block generation and rewrite the prompt as a visual director brief.

Prompt gate: no AI-generated visual may be generated for publish-ready work unless its prompt scores at least 9/10 by the prompt quality score in `references/ai_generated_asset_prompt_system.md`.

## Premium Background Prompt Rule

Do not describe a background with vague words such as `高级科技感背景`, `未来感`, `赛博`, `炫酷`, or `AI 风`. A premium background prompt must describe a beautiful usable atmosphere, not an unused visual skeleton.

Background prompts must include:

- visual thesis: the exact topic-specific visual idea
- topic binding: which selected AI topic/tool/source/workflow this background supports
- information job: what foreground proof cards, workflow simulation, comparison, checklist, or final template will be layered above it
- background role: how the plate remains text-free, skeleton-free support and never evidence
- scene role: what this background does for the explanation
- spatial structure: foreground, midground, background, negative space; no unused rails, cards, or UI slots
- material: glass, brushed metal, matte graphite, paper, fabric, acrylic, ceramic, etc.
- lighting: key light, rim light, softbox, practical glow, shadow softness
- camera/lens: wide keynote stage, editorial tabletop, documentary control room, macro product detail, etc.
- color hierarchy: base color, accent color, warning color, text-safe neutral zone
- texture/noise: subtle grain, realistic shadow, surface detail, no plastic blur
- text boundary: where subtitles/titles/callouts may appear
- avoid list: no fake UI, no pseudo text, no random grid, no floating line crossing subtitles, no skeleton stage, no unused placeholder framework

For AI/tech backgrounds, write prompts from the concrete formula `use case + core visual subject + 2-4 AI elements + spatial environment + material texture + color scheme + lighting + composition + style + clarity`. Choose only a few AI elements such as abstract neural network, data nodes, glowing particles, flowing data, digital pulse, algorithm trajectory, abstract brain outline, information matrix, holographic atmosphere, quantum network, digital ripple, or intelligent core. Pair them with real material and lighting language such as translucent glass, liquid metal, frosted metal, holographic material, crystal structure, optical-fiber texture, volumetric light, rim light, particle glow, gradient halo, and low-contrast soft light. Always reserve clean negative space for foreground text; never bake readable text into the background.

Before writing `background_prompt_pack.md`, randomly select one style family from `references/ai_background_random_style_pool.md` and record `background_style_pool_id`, `background_style_name`, and `background_style_selection_method`. The available style families are 量子环形反应堆, 芯片峡谷超级计算机, 全息数字孪生都市, 生物神经森林, 晶体张量矩阵, 黑金机械量子引擎, 银白光子实验室, 等离子数据风暴, 翡翠量子隧道, 群体智能轨道网络, AI宇宙意识网络, AI机械文明巨构, 星球环形AI计算都市, 黑金AI恒星引擎, and AI机械天空之城.

The random background style is selected once per video, not once per scene. After selection, read `references/enterprise_ai_control_console_visual_system.md` and make the foreground panels, captions, transitions, and SFX inherit the selected style's palette, light direction, material, and motion character.

The selected style may be visually dense and full-frame, but the production prompt must convert it into a readable video background. Keep dense structures away from title, caption, and proof-card zones; use haze, depth of field, vignette, local darkening, low-detail gradients, and soft light falloff to protect foreground text.

Foreground content over dense backgrounds must use local readability treatment: background blur, brightness reduction, saturation reduction, and feathered masks beneath active panels. Do not solve readability by making the entire video flat, and do not sacrifice readability to keep the background untouched.

Do not ask for robots, robot faces, hands, full-frame circuit boards, dense code, complex HUD dashboards, cheap neon, game UI, repeated patterns, placeholder cards, unused rails, or visual skeletons unless those structures are actually consumed by foreground animation.

16:9 premium AI background prompt template:

```text
Create a premium 16:9 editorial background plate for a Chinese AI explainer video.
Visual thesis: [make the selected topic visible as a concrete metaphor, not a generic AI mood].
Background style pool selection: [BG_STYLE_01-BG_STYLE_15 selected from references/ai_background_random_style_pool.md, with style name and selection method].
Enterprise console system: [foreground UI tokens, local readability treatment, component family plan, caption system, motion vocabulary, transition language, and SFX character from references/enterprise_ai_control_console_visual_system.md].
Topic binding: [name the specific AI topic/tool/source/workflow this background supports].
Information job: [official source proof / operation simulation / comparison cards / checklist / final template zones].
Background role: text-free, skeleton-free generated support atmosphere, never official proof.
Scene role: a calm keynote/control-room atmosphere that supports [specific concept], not a decorative tech wallpaper or unused layout framework.
Spatial structure: wide horizontal composition, clean negative space for foreground overlays, deep but readable background layers, no visible placeholder slots.
Foreground: soft light spill, shallow shadow anchors, subtle material edges, no readable fake text, no empty panels.
Midground: topic metaphor through haze, light bands, blurred architecture, premium material forms, or restrained bokeh; no source-wall skeleton unless foreground uses it exactly.
Background: matte graphite architectural atmosphere with realistic depth, soft gradients from real lighting, controlled vignette, no neon grid.
Lighting: gallery-grade softbox key light, restrained rim light on panel edges, ambient falloff, realistic contact shadows.
Material/texture: matte graphite, smoked-glass haze, brushed metal micro-edge, fine film grain, crisp but not glossy.
Color hierarchy: charcoal base, warm ivory text-safe zones, one accent color [teal/amber/blue] used only for focus.
Camera: 35mm editorial wide shot, straight-on, premium product keynote feel.
Avoid: generic cyber grid, random particles, fake UI, pseudo code, unreadable micro text, white lines crossing captions, clutter, stock-photo look.
```

For non-AI 9:16 work, use the owning vertical-video skill instead of this AI knowledge workflow. For reference-driven lightweight AI guide/list/card/poster work, use the 9:16 exception in `references/reference_driven_production_rules.md`.

## Premium Motion Prompt Rule

Do not describe motion as `加高级动效`, `酷炫转场`, `科技感动画`, or `页面切换快一点`. Motion must explain the information.

Every motion description must include:

- information purpose: reveal, compare, verify, warn, connect, summarize
- actor: what moves, such as source card, cursor, proof rail, risk gate, timeline node
- path: where it moves from/to
- timing: tied to exact voice phrase, sentence, or breath group
- easing: calm, keynote-like, no shake
- continuity: what remains on screen during the transition
- audio bridge: how narration remains continuous while visual transition and subtle SFX happen below the voice

Premium motion prompt examples:

```text
Source wall assembly: when the narrator says "先看四个信号", four proof tiles slide in from the same baseline, 0.18s stagger, soft ease-out. The background stage remains fixed, only the proof tiles and thin focus rail move.
```

```text
Risk gate: when the narrator says "必须先让你确认", a translucent red approval gate grows horizontally across the existing page, then locks. Do not cut away. Keep the previous proof panel dimmed behind it so the viewer understands this is a boundary, not a new topic.
```

```text
Process rail: during "计划、执行、看证据", three nodes light up one by one on the same horizontal rail. The camera does not jump. Captions stay in the same lower-third position.
```

Reject motion if it only makes the frame busier.

## Reusable Professional Male Voice Template

Use this when the user asks for a stronger male voice, professional lecturer tone, or `1.1x` narration. For this user's recurring AI knowledge / daily AI tip videos, treat this as the standing default unless the user says otherwise. Do not apply it silently to unrelated video categories; this is a scoped voice-direction override.

```text
Voice direction:
Use a powerful professional Chinese male lecturer voice.
The tone is firm, precise, and energetic, like a senior instructor explaining a real workflow.
It must not sound like a weak tutorial voice, a shouting sales host, or an exaggerated radio announcer.
Use short breath groups and clear emphasis on tool names, proof moments, and checklist words.
Speed: 1.1x / provider rate around +10%, only because the user explicitly requested it.
Do not interpret `+10%` provider rate as permission to write `tts_speed=1.2`. Any legacy automation wording such as `约 1.2 倍语速` is invalid for publish-ready metadata.
Metadata must record the real provider, voice id, male voice, rate, sample path, user approval, and source narration path.
After generating audio, rebuild the continuous root narration bed and retime every scene from real audio duration.
Transitions are visual-only; the voice must never restart, fade, mute, or gap during page changes.
```

Recommended free-first Edge TTS choice when available:

```json
{
  "provider": "edge_tts",
  "voice_id": "zh-CN-YunyangNeural",
  "voice_persona": "professional reliable male lecturer",
  "rate": "+10%",
  "tts_speed": 1.1,
  "voice_speed_policy": "user_approved_1_1x",
  "voice_speed_approval": "user explicitly requested male professional lecturer voice at 1.1x"
}
```

If this voice is unavailable or sounds wrong in the 10-15 second sample, stop and choose a better approved male voice instead of shipping a weak voice as final.

## Reusable Premium Transition System Template

Use this before writing HyperFrames HTML when the user says the page switching is too plain, monotonous, or not premium enough. The goal is not more chaos. The goal is more information-rich visual choreography.

```text
Transition direction:
The video must not use one repeated page fade or one repeated slide for every scene.
Create a scene-type transition recipe map.
Each transition has a visible information job: reveal proof, compare choices, pass a workflow packet, expose a risk gate, verify terminal output, or settle a final template.
Keep one shared anchor across transitions: background stage, proof rail, cursor, chapter marker, or lower-third caption position.
Narration remains a continuous root audio bed; transitions are visual-only and include 8-14 frames of overlap when a sentence continues.
SFX stays subtle: soft whoosh, UI tick, marker sweep, or proof pop below the voice.
```

Default recipe map:

```json
{
  "source_focus_lens_reveal": {
    "purpose": "verify",
    "use_for": "official source crop, browser proof, status page proof",
    "motion": "source frame enters with clip-path mask reveal, proof lens scales from left, source callout fades in 0.1s later",
    "transition": "focus-lens zoom through or blur crossfade",
    "avoid": "tiny fake screenshots, whole source page shaking, unreadable micro text"
  },
  "citation_rail_wipe": {
    "purpose": "verify",
    "use_for": "source/date/signal citation cards",
    "motion": "citation card does 0.6s cinematic fade-up, thin rail wipes left-to-right, key date/signal appears with 0.12s stagger",
    "transition": "mask wipe tied to the source rail",
    "avoid": "generic card swap with no proof hierarchy"
  },
  "comparison_split_handoff": {
    "purpose": "compare",
    "use_for": "wrong vs right prompt, bad workflow vs recoverable workflow",
    "motion": "left panel enters from -54px, right panel from +54px, risk chips stagger in after both panels settle",
    "transition": "split-panel handoff",
    "avoid": "both panels bouncing, too many labels moving at once"
  },
  "operation_node_relay": {
    "purpose": "connect",
    "use_for": "workflow timeline, task packet, agent steps",
    "motion": "nodes light up sequentially, packet/cursor slides along the same rail, final node gets subtle 1.08x pop",
    "transition": "smooth push slide with rail continuity",
    "avoid": "random node movement or decorative timeline unrelated to the voice"
  },
  "terminal_scan_proof_tray": {
    "purpose": "verify",
    "use_for": "terminal output, tests passed, changed files, evidence package",
    "motion": "terminal settles in, command/output reveals as a readable block, evidence tray slides from right, pass cues pop softly",
    "transition": "terminal scan wipe",
    "avoid": "moving terminal while the viewer needs to read"
  },
  "template_lift_settle": {
    "purpose": "summarize",
    "use_for": "checklist, reusable prompt template, final save card",
    "motion": "template rows lift in one by one with 0.12s stagger, then hold still long enough to read",
    "transition": "template lift-and-settle",
    "avoid": "empty template frames or rows appearing too fast to read"
  },
  "final_controlled_zoom": {
    "purpose": "summarize",
    "use_for": "final CTA only",
    "motion": "one restrained dramatic zoom, no glitch spam, CTA holds stable",
    "transition": "final dramatic zoom once",
    "avoid": "repeating dramatic zoom throughout the video"
  }
}
```

Gate: a 45-75 second AI video should use at least five distinct recipes. If contact sheets show the same layout and same page transition more than twice in a row, redesign before final render.

## Dynamic SFX Is Not Narration

When the user asks for a sound on transitions or dynamic effects, treat it as SFX design, not spoken voiceover. Do not generate TTS, retime the narration bed, or add a full narrator unless the user explicitly asks for voice.

SFX-only rule:

- Map each sound to a meaningful visual event: transition handoff, module settle, data packet travel, scanner pass, clean lock, or final energy pulse.
- Use an independent root SFX bed or root-level SFX clips.
- Keep the sound tactile and short; one cue per event is usually enough.
- If narration is present later, SFX must stay 12dB-18dB below the voice.
- If narration is absent, SFX must still be restrained and should not become a music track.
- Avoid game-style whoosh spam, explosions, harsh glitch noise, electric buzzing, repeated beeps, or heavy bass drops.
- Save an SFX cue report with timestamp, visual event, effect type, and mix policy before calling the video final.

## Paid-Grade Transition Variety Gate

When the user asks for transitions that feel like premium editor effects, do not answer with one repeated light sweep, one fixed blur wipe, one generic slide, or one simple glow pass. The video must still keep one visual world, palette, material family, and proof readability system, but the transition mechanism should vary by scene purpose.

Required transition plan:

- Use at least five transition mechanisms in a 45-75 second AI explainer when scene count allows.
- Do not repeat the same transition mechanism on adjacent scene changes.
- Do not let the transition become the main content; it must finish quickly and leave a readable hero frame.
- Keep captions stable or end captions before the transition covers the lower third.
- Use premium-feeling material motion: optical refraction, metallic aperture, liquid-metal sweep, magnetic rail handoff, prism scan shutter, depth lens pass, proof-tray scan, or core convergence.
- Avoid cheap effects: full-screen white flash, random glitch spam, harsh neon streaks, low-resolution blur, whole-page wobble, default fade, default slide, and one identical light bar used through the whole video.

Example premium transition map for black-gold AI mechanism videos:

```json
{
  "T01": {
    "name": "lens_aperture_refract",
    "use_for": "comparison scene into explanation scene",
    "mechanism": "the current comparison frame compresses into a glass lens; the next scene opens through a circular aperture with refraction and soft edge blur"
  },
  "T02": {
    "name": "liquid_metal_sweep",
    "use_for": "one teaching module into a process rail",
    "mechanism": "a champagne-gold and cyan liquid-metal ribbon sweeps diagonally, distorting the old frame while revealing the new rail"
  },
  "T03": {
    "name": "magnetic_rail_handoff",
    "use_for": "process node into operation simulation",
    "mechanism": "a data packet travels along the rail and pulls the next scene in, preserving workflow continuity"
  },
  "T04": {
    "name": "prism_scan_shutter",
    "use_for": "operation simulation into proof scene",
    "mechanism": "multiple translucent prism shutters pass over the frame while the proof tray resolves behind them"
  },
  "T05": {
    "name": "quantum_core_converge",
    "use_for": "proof scene into final recap",
    "mechanism": "proof elements dim toward a central core, then the recap opens from the core pulse"
  }
}
```

## No First-Paint Or Transition Landing Jump Gate

When HyperFrames or a custom capture script manually seeks CSS/Web Animations, the scene must not be visible until every visible animation has been paused and assigned the target `currentTime`.

Required implementation behavior:

- Start the composition in a hidden pre-seek state.
- Make only the target scene renderable but still hidden.
- Pause and seek all subtree animations for the target scene.
- Set transition overlay variables while the overlay is hidden.
- Reveal the prepared scene and transition overlay only after the state is locked.
- If the next scene is partially animated during a transition, the first non-transition frame of that next scene must inherit the transition landing time. Do not reset it to `0ms`, or the viewer will see the component appear, jump back, and animate again.
- Export a flash-guard contact sheet with each scene-boundary frame and the next frame. Reject black frames, white flashes, one-frame blank stages after a transition, or any component that restarts from hidden after it was already visible during the transition.

This gate is mandatory for premium motion previews and final AI explainer renders.

## Premium HyperFrames Animation Language

For AI knowledge videos, premium motion means restraint, layers, smoothness, and rhythm. Do not write vague animation goals such as `高级一点`, `酷一点`, `震撼一点`, `炫酷`, `crazy`, `explosive`, `flashy`, `excessive`, or `chaotic`. Translate taste into executable HyperFrames/GSAP language before authoring HTML.

Preferred motion feel words:

- `smooth`: default premium movement
- `dramatic`: use for a reveal or final proof moment
- `subtle`: use for text emphasis, glow, parallax, and audio response
- `cinematic`: use for slow title entrances and camera push-in
- `premium`, `clean`, `restrained`: use as design constraints
- `snappy`: use only for short social-video emphasis, not for every element

Timing defaults:

- Main title: `0.6s cinematic fade-up`, from `y=20px`, opacity `0 -> 1`.
- Subtitle: `0.15s` after title, smooth fade-in.
- Keyword: `0.25s subtle scale-pop`, max scale `1.08x`.
- Cards: `0.4s medium smooth slide-in`, stagger `0.12s-0.18s`.
- Background camera: slow push-in from `100%` to `103%` across the scene.
- Ambient glow: opacity breathes slowly between `8%` and `18%`.
- Text audio response: scale pulse only `3%-5%`.
- Background glow audio response: `10%-15%`.

Scene motion must be structured in storyboard JSON:

```json
{
  "purpose": "reveal / compare / verify / warn / connect / summarize",
  "background_motion": "very slow 100%-103% camera push-in with subtle parallax",
  "foreground_motion": "0.6s cinematic fade-up from y=20px opacity 0",
  "callout_motion": "keyword subtle scale-pop max 1.08x for 0.25s",
  "transition": "blur crossfade / smooth push slide / final dramatic zoom only",
  "entrance": "0.6s cinematic fade-up from y=20px opacity 0",
  "stagger": "0.12s-0.18s between title/cards",
  "keyword_motion": "subtle scale-pop max 1.08x for 0.25s",
  "camera_motion": "background push-in 100% to 103%, foreground stable",
  "layering": "background parallax + foreground stable + callout reveal",
  "caption_motion": "keyword highlight only, no every-word bouncing",
  "glow": "ambient glow opacity 8%-18%, no flicker",
  "audio_reactive": "text 3%-5%, background glow 10%-15%",
  "negative_motion": "no excessive bounce, no chaotic movement, no glitch spam"
}
```

Scene sync must also document continuous narration:

```json
{
  "narration_track": "continuous_root_audio",
  "transition_audio_policy": "visual-only transition; narration continues with no restart or mute",
  "max_audio_gap_ms": 80,
  "audio_bridge": "continuous narration bed under visual transition; SFX stays below voice"
}
```

HyperFrames prompt block for premium AI videos:

```text
Animation direction:
clean, premium, smooth, cinematic, restrained.
No cheap neon, no frequent glitch, no excessive bounce, no text flying from every direction.

Every scene must design:
1. Main title: 0.6s cinematic fade-up from y=20px.
2. Subtitle: 0.15s delayed smooth fade-in.
3. Cards: 0.12s-0.18s staggered reveal.
4. Keywords: max 1.08x subtle scale-pop for 0.25s.
5. Background: 100%-103% slow push-in and subtle parallax.
6. Ambient glow: 8%-18% slow breathing.
7. Transitions: blur crossfade for calm scenes, smooth push slide for steps, final dramatic zoom at most once.
8. Chinese captions: keyword highlight only, no every-word bouncing.
9. SFX: soft whoosh and subtle pop below narration.
10. Narration: use one root-level continuous audio track for the full video; visual scene transitions must never restart, mute, fade, or gap the voice.
11. Motion explains information instead of making the frame busier.
```

Reject the scene if:

- it only says `高级`, `科技感`, `炫酷`, or `震撼`
- every element enters with the same slide/zoom
- every word bounces
- glow flickers, strobes, or feels like nightclub lighting
- motion paths cross caption/title safe zones
- glitch appears more than once or becomes the dominant transition language

## Voice-to-Scene Continuity Rule

Publish-ready narration must use a truthful, approved voice source. Do not relabel macOS `say`, Apple/system voices such as `Tingting`, scratch timing previews, or local system TTS as natural final narration. A `qa_status=passed` metadata field only means a technical check passed; it cannot replace `sample_approved=true` or an explicit user approval for lower-quality audio.

Do not hard-cut the page while a speaker is mid-sentence. This makes the narration feel broken.

Scene changes are allowed only at:

- sentence end
- comma/breath pause explicitly marked in the copy
- chapter title pause
- beat boundary listed in `storyboard.audio_locked.json`

When the visual page changes during the same spoken idea:

- keep a shared background stage
- keep the lower-third caption position stable
- keep narration on the continuous root audio track; use SFX only below the voice
- overlap the old and new visual for 8-14 frames
- keep one anchor object on screen, such as a rail, source label, cursor, or chapter marker

If a scene needs a new page while the narrator continues, use a match cut, crossfade, slide-over panel, or picture-in-picture handoff. Do not use a full replacement cut.

HyperFrames implementation rule:

- Put narration in a root `<audio>` element or root-level scene audio schedule, never inside timed visual scene containers.
- Keep per-scene visual clips on their own tracks and transition them visually; do not animate or trim the narration audio during those transitions.
- Final `metadata.quality_spec.narration_continuity_policy` must explain the continuous narration strategy before QA.

Every storyboard scene must include `sync.transition_boundary` with one of:

- `sentence_end`
- `breath_pause`
- `chapter_pause`
- `visual_handoff`

`visual_handoff` must document the shared anchor and overlap duration.

## HyperFrames Design Rule

Before writing HyperFrames HTML, create a visual identity:

- `DESIGN.md` with style prompt, colors, typography, layout principles, motion rules, and anti-patterns.
- Scene layouts must be native HTML/CSS structures, not one repeated exported PNG card.
- Static PIL/canvas support cards are content sources only. If they are used directly as full-frame visible shots, the scene fails the premium gate.
- Build the hero frame layout first, then animate into it.
- For 16:9 AI explainers, use a stable stage with wide proof panels, side annotation rails, and lower-third captions instead of stacked vertical cards.
- Use at least four distinct scene structures in a 60-second AI video, for example: poster hook, source wall, terminal proof, browser proof, tool-network diagram, risk matrix, process rail, evidence checklist, final takeaway.
- Motion must explain the idea: source lights up, task moves through a pipeline, risk gate blocks an action, evidence tiles are verified.
- For metal/technology art direction, foreground components must be built as designed objects: trays, rails, apertures, hinges, nodes, clamps, focus lenses, output slots, verification seals, and layered glass or metal surfaces. A rounded rectangle with text is not enough.
- Every foreground proof component must declare `material_layer`, `structure_layer`, `motion_actor`, `readability_treatment`, `hold_for_reading_sec`, and `reject_if_ppt_like`.
- If the contact sheet shows flat cards over a background, repeated left-heavy layout, or static proof cards without visible mechanism/motion affordance, restage before storyboard lock or render.

## Plugin Roles

- Browser: collect official pages, screenshots, and proof when live browser capture is needed.
- ImageGen: create cover/concept/support visuals only; never fake proof.
- HyperFrames: own the final timeline, captions, transitions, and synchronized visual system.
- FFmpeg/ffprobe: remux audio, verify duration, bitrate, fps, frame extraction, and contact sheets.
- Hugging Face: use only when the topic needs open-source model/ecosystem proof.
- GitHub: use only when the topic needs real repo, issue, diff, CI, or release proof.
- HeyGen: use only when a presenter/avatar is explicitly authorized and account/credit boundaries are clear.

## Final Visual QA

Before promotion, inspect:

- first five seconds contact sheet
- full-video contact sheet
- crowded/native-size frames
- final cover
- ffprobe output
- provider usage audit

Reject the video if it looks like a generic template, a repeated card deck, a soft screenshot export, or an abstract background with subtitles.
