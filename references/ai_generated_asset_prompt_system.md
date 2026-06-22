# AI Generated Asset Prompt System

Use this before generating any AI-made visual asset for AI explainer videos. Read `references/visual_description_language_reference.md` first for description language, then use this file for manifest/provider fields and validation contracts. Good generated footage starts with good visual direction. If the prompt is generic, the video will look generic.

## Hard Rule

Do not ask an image/video model for `高级`, `科技感`, `未来感`, `赛博`, `酷炫`, `真实感`, or `设计感` by themselves.

Translate taste into concrete visual instructions:

- what the asset is for
- what the viewer should understand
- where foreground, midground, background, and empty text zones are
- what camera/lens/viewpoint is used
- what material, lighting, texture, and color hierarchy create the mood
- what must not appear

Every generated asset must be treated as a designed object, not as decoration.

## Visual Asset Director Prompt Contract

This is a hard contract for every generated visual asset. A usable prompt must work like a miniature visual-director brief: it tells the image model what information the asset explains, how the frame is physically staged, and how HyperFrames will animate or layer on top of it.

Before any prompt card is written, create `internal/visual_style_decision.json` and make the prompt inherit that decision. Do not use the example `daylight_productivity` / `L4 bright tutorial` fields below as defaults; they are only valid when the current video's topic, copy mood, evidence density, or reference analysis justifies them.

Do not let a generated image enter production unless its prompt card can answer all of these questions:

- what exact scene and narration line this image supports
- what the viewer should understand within one second
- what is foreground, midground, background, and empty overlay space
- what camera/lens/viewpoint gives the image a deliberate shot language
- what lighting, material, texture, and color hierarchy create the premium feel
- what motion affordance HyperFrames should use, such as parallax layers, reveal zones, rail wipes, proof-lens focus, or card handoffs
- what the image must never pretend to be, especially official proof, real UI, or a screenshot
- when this image should be regenerated

Required prompt/manifest fields for `type=generated_visual`:

```json
{
  "scene_id": "S03",
  "narration_line_supported": "Codex 不该只收到一句模糊任务，而要收到目标、环境、检查点和验收标准。",
  "scene_function": "tutorial_step",
  "visual_archetype": "bright_productivity_desk",
  "brightness_grade": "L4 bright tutorial",
  "palette_family": "daylight_productivity",
  "material_family": "paper_acrylic",
  "layout_family": "three_step_ladder",
  "energy_level": "useful, clear, beginner-friendly",
  "visual_thesis": "A vague task turns into a structured Codex workbench with four verified lanes.",
  "background_style_pool_id": "BG_STYLE_02",
  "background_style_name": "芯片峡谷超级计算机",
  "background_style_selection_method": "random choice from references/ai_background_random_style_pool.md, recorded before prompt writing",
  "topic_binding": "Codex long-running agent workflow; not generic AI mood.",
  "beginner_usefulness": "The viewer should feel this structure can be copied immediately for a real task.",
  "information_job": "Hold task brief, repo/file tree, test output, and evidence package overlays.",
  "background_role": "Topic-bound support stage; text-free and never evidence.",
  "viewer_takeaway": "Good Codex tasks look like an operating desk, not a one-line prompt.",
  "composition": "Wide 16:9 workbench with large center-left operation zone, right evidence tray, lower-third caption-safe band.",
  "foreground": "Soft shadow anchors, glass rail edges, and a clean cursor path with no readable fake text.",
  "midground": "Abstract repo tree blocks, terminal proof tray, and checkpoint lanes with blank labels for HTML overlays.",
  "background": "Matte graphite studio depth with restrained source-wall silhouettes and clean negative space.",
  "camera_lens": "35mm straight-on editorial workspace shot, stable and readable.",
  "lighting": "Soft upper-left key light, restrained rim on glass edges, ambient falloff, realistic contact shadows.",
  "material_texture": "Smoked glass, brushed metal, matte graphite, fine film grain, crisp non-plastic edges.",
  "color_hierarchy": "Charcoal base, warm ivory safe zones, teal focus accent only for proof path.",
  "color_system": "Brightness grade L4; daylight productivity palette; warm ivory base; clean paper surfaces; cobalt active accent; amber result highlight; high readability.",
  "depth_layering": "Foreground rail, midground operation panels, and background source-wall depth are separated by contact shadows and overlap.",
  "text_safe_zones": "Keep center-left and lower third clean for Chinese titles, subtitles, and proof cards.",
  "motion_usage": "HyperFrames will parallax the background slowly, slide in task cards, and focus the evidence tray with a mask reveal.",
  "animation_affordance": "Separate foreground rail, midground operation panels, and background source-wall depth so motion is layered.",
  "primary_animated_object": "Three task cards and the final evidence tray.",
  "dark_light_motion_rule": "Active objects become brighter and larger; dark areas stay behind bright proof surfaces.",
  "evidence_boundary": "Support only; not evidence, not official UI, not a screenshot.",
  "negative_prompt": "No fake UI, pseudo text, neon grid, tiny unreadable labels, random particles, QR code, watermark, stock-photo people.",
  "regeneration_criteria": "Regenerate if it looks like generic tech wallpaper, includes fake text/UI, lacks clean overlay zones, or competes with captions.",
  "diversity_check": "Must not reuse the same visual archetype, palette family, and layout family as the previous scene."
}
```

If a field is blank, shorter than a concrete phrase, or only contains taste words like `高级科技感`, the image is not ready to generate.

## Provider And Prompt Evidence Gate

For AI knowledge videos, generated images must be generated with `gpt-image-2` or Codex built-in ImageGen and documented as such. Do not register local PIL/canvas/HTML renders as AI-generated `generated_visual` assets. Local deterministic rendering can still be used for charts, cover layout, or QA contact sheets, but it does not satisfy the generated-image gate.

Every generated visual in `asset_manifest.json` must include:

```json
{
  "type": "generated_visual",
  "provider": "gpt-image-2 or codex_builtin_imagegen",
  "model": "gpt-image-2",
  "prompt_id": "BG001",
  "prompt_path": "internal/background_prompt_pack.md#BG001",
  "unique_prompt": true,
  "evidence_boundary": "support only; not evidence",
  "visual_thesis": "what topic-specific idea this image makes visible",
  "background_style_pool_id": "BG_STYLE_01 / ... / BG_STYLE_15 when asset_role=background_plate",
  "background_style_name": "one of the 15 names in references/ai_background_random_style_pool.md when asset_role=background_plate",
  "background_style_selection_method": "random selection record when asset_role=background_plate",
  "topic_binding": "which selected topic/source/tool this background supports",
  "scene_function": "hook_result_preview / beginner_problem / tutorial_step / source_proof / news_explain / template_summary / final_takeaway",
  "visual_archetype": "bright_productivity_desk / clean_tutorial_canvas / editorial_proof_stage / result_showcase_gallery / etc.",
  "brightness_grade": "L1-L5 with a concrete label such as L4 bright tutorial",
  "palette_family": "daylight_productivity / cream_cobalt_orange / graphite_ivory_teal / etc.",
  "material_family": "paper_acrylic / whiteboard_marker / desk_stationery / matte_editorial / etc.",
  "layout_family": "before_after_split / three_step_ladder / source_wall_grid / checklist_stack / etc.",
  "energy_level": "calm / useful / urgent / tutorial / reveal / warning / celebratory",
  "beginner_usefulness": "why this frame feels usable, clear, and close to a real task",
  "information_job": "what proof, labels, workflow, or checklist this background must hold",
  "background_role": "how the plate acts as a stage without becoming evidence",
  "scene_id": "which scene or shot owns this generated visual",
  "narration_line_supported": "the exact voice line this visual supports",
  "viewer_takeaway": "the one-second understanding goal",
  "composition": "wide layout and subject hierarchy",
  "foreground": "front-layer visual elements",
  "midground": "middle-layer visual elements",
  "background": "back-layer visual elements",
  "camera_lens": "camera position and lens language",
  "lighting": "key light, rim light, ambient glow, shadows",
  "material_texture": "specific surfaces and tactile quality",
  "color_hierarchy": "base, accent, warning, and text-safe colors",
  "color_system": "brightness, palette, base/surface colors, accents, warm/cool balance, light/dark/accent ratios, contrast target",
  "depth_layering": "foreground/midground/background separation, contact shadows, edge detail, and overlap",
  "text_safe_zones": "where Chinese titles, captions, proof cards, and callouts can sit",
  "motion_usage": "how HyperFrames uses this image in motion",
  "animation_affordance": "which layers or zones can animate separately",
  "primary_animated_object": "which object should visibly move first",
  "dark_light_motion_rule": "how active objects stay readable when the scene is dark or bright",
  "negative_prompt": "what must not appear",
  "regeneration_criteria": "what failure requires a new generation",
  "diversity_check": "how this asset differs from adjacent scenes in archetype, palette, material, or layout"
}
```

If a video needs 10 or dozens of generated pictures, each picture needs a distinct prompt card and a distinct `prompt_id`; do not generate a batch from one generic style prompt.

## Required Prompt Pack

Before generating assets, create `internal/ai_asset_prompt_pack.md` or an equivalent section in the production notes.

For every AI knowledge video, create `internal/visual_style_decision.json`, `internal/visual_style_plan.json`, and `internal/background_prompt_pack.md` before storyboard, assets, TTS, HyperFrames, render, or upload. The decision must record Codex's selected brightness, palette, material, layout, and why this style fits the script. The prompt pack must contain 3-5 descriptive background directions and at least one selected/generated text-free `1920x1080` background plate. Do not start video production from a generic gradient, template wallpaper, neon grid, blank color field, or repeated light-card default.

Each asset prompt must include:

```text
Asset ID:
Scene ID:
Narration line supported:
Asset role: background_plate / hero_poster / metaphor_visual / transition_plate / diagram_base / cover / texture / support_card
Scene function:
Visual archetype:
Brightness grade:
Palette family:
Material family:
Layout family:
Energy level:
Visual thesis:
Background style pool selection: [BG_STYLE_01-BG_STYLE_15, name, and random selection method when asset_role=background_plate]
Topic binding:
Beginner usefulness:
Information job:
Background role:
Viewer takeaway:
Format: 16:9 1920x1080 for all AI knowledge videos
Composition:
Foreground:
Midground:
Background:
Camera/lens:
Lighting:
Material/texture:
Color hierarchy:
Color system:
Depth/layering:
Text-safe zones:
Motion usage in HyperFrames:
Animation affordance:
Primary animated object:
Dark/light motion rule:
Evidence boundary:
Negative prompt:
Regeneration criteria:
Provider/model:
Prompt ID/path:
Unique prompt:
Diversity check:
```

If any field is missing, do not generate the image. The visual-system selector fields (`scene_function`, `visual_archetype`, `brightness_grade`, `palette_family`, `material_family`, `layout_family`) are hard gates because they prevent every AI explainer from collapsing into the same dark glass-card style.

## 16:9 AI Explainer Asset Roles

For proof-heavy AI explainers and AI knowledge videos, generated assets must be 16:9 `1920x1080`. Do not generate 9:16 assets for AI knowledge/tutorial work under this skill unless `references/reference_driven_production_rules.md` has routed the project into a vertical lightweight guide/list/card/poster information mode.

### Background Plate

Purpose: create the premium stage behind proof panels and captions.

This is mandatory for AI knowledge videos. The background plate must be generated from descriptive language with `gpt-image-2` or Codex built-in ImageGen, saved as a project asset, and registered in `asset_manifest.json` with `asset_role=background_plate`, `type=generated_visual`, `asset_source_type=generated`, `is_evidence=false`, `resolution=1920x1080`, `model`, `prompt_id`, `prompt_path`, `unique_prompt=true`, `evidence_boundary`, `visual_thesis`, `topic_binding`, `information_job`, `background_role`, and the complete Visual Asset Director fields above.

The background must be topic-bound and atmospheric. In one second, the viewer should sense the topic's world through atmosphere, material, light, color, depth, and visual metaphor. If foreground cards, proof panels, or captions will be added later, reserve clean negative space and local quiet zones for those foreground layers.

Global background plates act as reusable atmosphere, not the information layer. If a scene needs readable words, numbers, labels, source notes, or checklist copy, put them in HTML/CSS/Remotion foreground layers or in a separate foreground proof/support card.

Every AI knowledge video background plate must first randomly select one style from `references/ai_background_random_style_pool.md`: `BG_STYLE_01 量子环形反应堆`, `BG_STYLE_02 芯片峡谷超级计算机`, `BG_STYLE_03 全息数字孪生都市`, `BG_STYLE_04 生物神经森林`, `BG_STYLE_05 晶体张量矩阵`, `BG_STYLE_06 黑金机械量子引擎`, `BG_STYLE_07 银白光子实验室`, `BG_STYLE_08 等离子数据风暴`, `BG_STYLE_09 翡翠量子隧道`, `BG_STYLE_10 群体智能轨道网络`, `BG_STYLE_11 AI宇宙意识网络`, `BG_STYLE_12 AI机械文明巨构`, `BG_STYLE_13 星球环形AI计算都市`, `BG_STYLE_14 黑金AI恒星引擎`, or `BG_STYLE_15 AI机械天空之城`. Record the selected ID/name/method in the prompt pack and manifest. The selected style is a visual family, not a raw prompt; adapt it to the current topic, narration, proof layout, and safe zones.

If the selected style's source wording says `full-frame` or `no blank area`, rewrite it for video as rich full-frame atmosphere with controlled low-detail title/caption/proof-safe zones. Dense structures may fill the world, but not the reading surface behind foreground text.

For AI/tech background plates, use the user's premium background formula instead of generic tech words:

```text
use case + core visual subject + 2-4 AI elements + spatial environment + material texture
+ color scheme + lighting effect + composition requirement + visual style + clarity requirement.
```

AI elements should be chosen deliberately, usually only 2-4 at a time: abstract neural network, data nodes, glowing particles as texture, flowing data, digital pulse, algorithm trajectory, abstract brain silhouette, information matrix, holographic interface atmosphere, quantum network, digital ripple, or intelligent core. Do not use the full list in one prompt.

Material and lighting should do the premium work: translucent glass, liquid metal, frosted metal, holographic material, crystal structure, optical-fiber texture, transparent acrylic, micro-particle material, mirror reflection, fine mesh, soft neon light, volumetric light, rim light, low ambient light, light passing through material, particle glow, gradient halo, cinematic lighting, low-contrast soft light, or high-contrast dramatic light.

Choose one restrained color direction per background: dark premium tech (deep sea blue, indigo, violet, cyan glow), clean enterprise AI (white, silver gray, ice blue, light cyan), carefully controlled cyber future (black, neon blue, magenta, electric purple), or premium warm AI (deep black, champagne gold, amber orange, warm white light). The prompt must also name where the clean title/caption/proof negative space sits.

Preferred premium background language: cinematic editorial depth, atmospheric gradient, gallery-grade softbox lighting, shallow architectural shadow, matte mineral texture, brushed graphite, smoked-glass haze, subtle film grain, restrained bokeh, premium keynote lighting, controlled vignette, and clean negative space. These are acceptable only when combined with concrete composition, lighting, material, color hierarchy, and text-safe zones; do not use empty taste words alone.

Prompt skeleton:

```text
Create a 16:9 premium editorial background plate for a Chinese AI explainer about [topic].
Scene function: [hook_result_preview / tutorial_step / source_proof / template_summary].
Visual archetype: [bright_productivity_desk / clean_tutorial_canvas / editorial_proof_stage / result_showcase_gallery].
Brightness grade: [L2 dark with bright proof surfaces / L4 bright tutorial / L5 cover/result bright].
Palette family: [daylight_productivity / cream_cobalt_orange / graphite_ivory_teal / newsroom_white_red / amber_warning_compare], chosen from `visual_style_decision.json`, not as a default.
Material family: [paper_acrylic / matte_editorial / newsroom_panel].
Layout family: [before_after_split / three_step_ladder / source_wall_grid].
Visual thesis: [one exact visual idea that makes the topic visible, such as "streaming speech becomes chunked waveform packets moving through a latency gate"].
Background style pool selection: [BG_STYLE_01-BG_STYLE_15 selected from references/ai_background_random_style_pool.md, with style name and random selection method].
Topic binding: [the specific tool/source/workflow/topic this background supports, not generic AI].
Beginner usefulness: [why the frame feels copyable, clear, or close to real work].
Information job: create a beautiful atmospheric stage that leaves clean negative space for foreground proof cards, captions, and source overlays.
Background role: topic-bound premium atmosphere; text-free, skeleton-free, and never evidence.
Viewer takeaway: the frame should feel expensive, focused, and editorial, not like a decorative tech wallpaper or unused UI framework.
Composition: wide horizontal layout with calm negative space for overlays; no visible placeholder cards, rails, grids, or empty UI slots unless foreground elements will exactly use them.
Foreground: soft light spill, subtle material edges, atmospheric shadow anchors, no readable fake text and no unused panels.
Midground: abstract topic metaphor through light, depth, particles-as-texture only, glass haze, or blurred architectural forms; no workflow skeleton.
Background: cinematic editorial depth with realistic falloff, matte mineral or graphite texture, controlled vignette, and clean breathing room.
Camera/lens: 35mm or 50mm straight-on editorial wide shot, stable keynote framing, shallow depth cues.
Lighting: gallery-grade softbox key light, restrained rim light, warm/cool falloff, realistic contact shadows, no harsh neon.
Material/texture: matte graphite, smoked-glass haze, brushed metal micro-edge, fine film grain, soft paper/acrylic texture, no plastic shine.
Color hierarchy: [base, surface, text-safe neutral, active accent, result/warning accent] with restrained premium contrast.
Color system: [brightness grade, palette family, base/surface colors, warm/cool balance, light/dark/accent ratios, contrast target, forbidden color failure].
Depth/layering: [foreground/midground/background separation, soft contact shadows, edge detail, overlap].
Text-safe zones: keep [center-left/right/lower third] clean and dark for Chinese captions and proof panels.
Avoid: fake UI, pseudo text, readable letters, numbers, watermark, brand logo, people, robots, hands, dense code, circuit-board wallpaper, complex HUD, random particles, neon grid, white crossing lines, clutter, harsh colors, blurry stock look, overexposed highlights, cartoon/game UI, repeated patterns, over-sharpening, skeleton stage, unused rails, placeholder cards, empty UI slots.
```

### Hero Poster

Purpose: make the first frame look like a premium cover.

Prompt skeleton:

```text
Create a 16:9 premium hero poster background for a Chinese AI explainer.
Subject: [one exact concept], not a robot mascot.
Visual metaphor: [AI task becomes verified output / tool network enters evidence gate / browser action becomes checklist].
Composition: one dominant focal object, strong negative space for a large Chinese title, no small text baked into the image.
Foreground: [object or metaphor] with tactile material and realistic shadows.
Midground: subtle supporting panels or rails that point toward the focal object.
Background: quiet editorial stage with depth, not a decorative wallpaper.
Camera/lens: product-keynote shot, 35mm or 50mm, straight and stable.
Lighting: cinematic but restrained, one key light, one rim light, soft shadow.
Material/texture: describe exact surfaces: matte metal, glass, paper, screen glow, fabric, acrylic.
Color hierarchy: base neutral plus one accent. Do not use rainbow gradients.
Text-safe zone: leave clean area for title and subtitle.
Avoid: fake UI, pseudo Chinese, random charts, robot face, stock photo people, messy cables, cyberpunk city.
```

### Metaphor Visual

Purpose: explain an abstract AI idea without faking proof.

Prompt skeleton:

```text
Create a 16:9 visual metaphor for [AI concept].
The image must explain: [plain-language idea].
Metaphor: [specific metaphor], for example "model as dispatcher", "MCP as socket", "risk gate as approval lock".
Composition: simple readable shapes, one idea only, enough empty space for labels added later in HyperFrames.
Foreground: the main metaphor object.
Midground: two or three supporting objects showing relationship.
Background: quiet stage with depth and no readable fake text.
Lighting/material/color/text-safe/avoid: [same level of detail as background plate].
Evidence boundary: this is conceptual support, not official UI, not a screenshot, not data proof.
```

### Diagram Base

Purpose: create a clean non-text diagram plate; labels will be added in HyperFrames.

Prompt skeleton:

```text
Create a 16:9 clean diagram base for an AI explainer.
Diagram idea: [pipeline / comparison / risk matrix / checklist].
Do not generate readable text. Use blank nodes, rails, panels, and placeholders only.
Composition: [left-to-right / top-to-bottom / radial], large shapes, no tiny labels.
Leave safe zones for Chinese labels and captions added later.
Use premium materials and lighting, not flat clipart.
Avoid: pseudo text, fake logos, dense lines, random icons, clutter.
```

### Transition Plate

Purpose: bridge one proof scene to the next without cutting the voice mid-sentence.

Prompt skeleton:

```text
Create a 16:9 transition plate for moving from [scene A] to [scene B].
Continuity anchor: [same rail / same cursor / same source tag / same chapter marker] stays visible.
Composition: old idea fades into background while new idea enters from [direction].
Motion plan: old panel remains for 8-14 frames while new panel slides over it in HyperFrames.
Background: same stage style as previous scene.
Avoid: full-screen flash, random wipe, unrelated new background, hard visual reset.
```

## Negative Prompt Library

Use these negative constraints by default:

```text
Avoid fake product UI, fake official screenshots, fake analytics, fake reviews, pseudo Chinese, unreadable small text, random English filler, generic robot, neon cyber grid, floating particles, white lines crossing caption zones, over-complex dashboards, low-resolution screenshot look, stock-photo people, blurry gradients, plastic shine, cluttered icons, harsh glow, watermark, QR code, contact info.
```

## Prompt Quality Score

Score each generated-asset prompt before running it:

- 2 points: exact asset role and scene/narration purpose
- 2 points: strong composition with foreground/midground/background
- 2 points: material, lighting, lens, texture, and color hierarchy are specific
- 2 points: text-safe zones and HyperFrames overlay plan are clear
- 2 points: negative prompt and evidence boundary are explicit

Minimum score: 9/10 for publish-ready generation.

If a prompt scores below 9, rewrite it before generating.

Hard fail regardless of score:

- one prompt is reused across multiple generated images
- the prompt cannot identify the scene, narration line, and viewer takeaway
- the prompt has no foreground/midground/background plan
- the prompt has no `motion_usage` or `animation_affordance` for HyperFrames
- the prompt looks like a style tag list instead of a shot brief

## Regeneration Criteria

Regenerate the asset if it has:

- fake or unreadable text
- random UI that looks like false proof
- no clear place for captions or proof panels
- flat wallpaper look
- noisy grid/particles
- overexposed or muddy background
- weak foreground/midground/background hierarchy
- inconsistent style with the rest of the video
- any artifact that competes with subtitles

## HyperFrames Handoff

Generated assets must not carry the whole scene alone. The HyperFrames scene must add:

- real text, labels, captions, and callouts as HTML
- motion that explains the narration
- proof panels or source cards when claims need evidence
- stable lower-third caption position
- transition boundaries locked to sentence or breath pauses

Generated visual assets are the stage. HyperFrames is the performance.
