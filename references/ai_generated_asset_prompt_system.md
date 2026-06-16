# AI Generated Asset Prompt System

Use this before generating any AI-made visual asset for AI explainer videos. Good generated footage starts with good visual direction. If the prompt is generic, the video will look generic.

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

## Required Prompt Pack

Before generating assets, create `internal/ai_asset_prompt_pack.md` or an equivalent section in the production notes.

For every AI knowledge video, create `internal/background_prompt_pack.md` before storyboard, assets, TTS, HyperFrames, render, or upload. It must contain 3-5 descriptive background directions and at least one selected/generated text-free `1920x1080` background plate. Do not start video production from a generic gradient, template wallpaper, neon grid, or blank color field.

Each asset prompt must include:

```text
Asset ID:
Scene ID:
Narration line supported:
Asset role: background_plate / hero_poster / metaphor_visual / transition_plate / diagram_base / cover / texture / support_card
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
Text-safe zones:
Motion usage in HyperFrames:
Evidence boundary:
Negative prompt:
Regeneration criteria:
```

If any field is missing, do not generate the image.

## 16:9 AI Explainer Asset Roles

For AI explainers and AI knowledge videos, generated assets must be 16:9 `1920x1080`. Do not generate 9:16 assets for AI knowledge/tutorial work under this skill.

### Background Plate

Purpose: create the premium stage behind proof panels and captions.

This is mandatory for AI knowledge videos. The background plate must be generated from descriptive language, saved as a project asset, and registered in `asset_manifest.json` with `asset_role=background_plate`, `type=generated_visual`, `asset_source_type=generated`, `is_evidence=false`, and `resolution=1920x1080`.

Prompt skeleton:

```text
Create a 16:9 premium editorial background plate for a Chinese AI explainer about [topic].
Viewer takeaway: the frame should feel like a calm, expensive information stage, not a decorative tech wallpaper.
Composition: wide horizontal layout, large clean proof area at [left/center], quiet annotation rail at [right], lower-third caption-safe band.
Foreground: subtle glass/acrylic edge elements and soft shadow anchors, no readable fake text.
Midground: [tool pipeline / source wall / evidence gate / browser frame silhouette] as abstract shapes only, with enough empty space for HTML overlays.
Background: matte graphite architectural depth with realistic falloff, no busy grid.
Camera/lens: 35mm straight-on editorial wide shot, stable keynote framing.
Lighting: soft key light from upper left, restrained rim light on panel edges, low ambient glow, realistic contact shadows.
Material/texture: smoked glass, brushed metal, matte graphite, fine film grain, crisp edges.
Color hierarchy: charcoal base, warm ivory text-safe zones, one accent color [teal/amber/blue/rose] reserved for focus.
Text-safe zones: keep [center-left/right/lower third] clean and dark for Chinese captions and proof panels.
Avoid: fake UI, pseudo text, random particles, neon grid, white crossing lines, clutter, blurry stock look, overexposed highlights.
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
