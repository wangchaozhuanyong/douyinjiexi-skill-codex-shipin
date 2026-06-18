# Visual Description Language Reference

Use this before writing `background_prompt_pack.md`, `ai_asset_prompt_pack.md`, storyboard visual descriptions, or HyperFrames motion descriptions. This file defines the language density and taste standard. `references/ai_generated_asset_prompt_system.md` defines the manifest/provider contract and validation fields.

## Core Rule

Premium description means concrete visual direction, not taste labels.

Do not use these phrases as the main visual direction:

- 高级科技感背景
- 酷炫未来感
- 赛博风
- 电影级质感
- 专业感
- 大气背景
- AI 科技背景
- 炫酷动效
- 震撼开场
- 真实感 UI
- 高端信息流
- premium tech background
- futuristic AI dashboard
- cinematic cyber interface
- abstract digital technology background

Reason: these phrases do not describe composition, information function, material, lighting, hierarchy, evidence boundary, or motion behavior. They usually produce generic wallpaper, fake UI, neon grids, floating particles, and low-trust visual frames.

## Required Visual Description Structure

Every background, support visual, storyboard visual, or motion description must answer:

1. Asset role: what this visual does in the video.
2. Scene function: hook result, beginner problem, tutorial step, source proof, news explain, template summary, or final takeaway.
3. Visual archetype: the chosen visual system such as bright productivity desk, clean tutorial canvas, editorial proof stage, newsroom wall, or result gallery.
4. Brightness grade: L1-L5, with beginner tutorial scenes usually using L3-L5 and dark proof scenes requiring bright proof surfaces.
5. Palette family, material family, layout family, and energy level.
6. Viewer takeaway: what the viewer should understand in one glance.
7. Topic binding: why this visual belongs to this exact topic.
8. Beginner usefulness: why the frame feels copyable, usable, or close to real work.
9. Information job: what overlays, proof panels, captions, screenshots, labels, or diagrams it must support.
10. Composition: where the proof area, annotation rail, title zone, and caption-safe band are.
11. Foreground: closest layer such as panel edges, glass rails, shadows, anchors.
12. Midground: operating layer such as source wall, browser silhouette, workflow rail, checklist base, blank cards.
13. Background: deep stage such as architectural depth, matte surface, soft falloff, negative space.
14. Camera/lens: straight-on editorial 35mm, 50mm product keynote, overhead desk, shallow depth, macro detail.
15. Lighting: key light, fill light, rim light, contact shadow, ambient glow, falloff.
16. Material/texture: paper grain, matte acrylic, desk stationery, brushed aluminum, smoked glass, fine grain, or another explicit family.
17. Color hierarchy and color system: brightness grade, palette family, base/surface colors, text-safe surface, accent ratios, light/dark ratios, contrast target, and forbidden color failure.
18. Depth/layering: how foreground, midground, background, contact shadows, and overlap create tactile separation.
19. Text-safe zones: clean areas for Chinese captions, labels, source panels, or title.
20. Motion usage in HyperFrames: how the visual supports animation without carrying the whole scene.
21. Animation affordance, primary animated object, and dark/light motion rule.
22. Evidence boundary: support art, metaphor, diagram base, transition plate, or real evidence.
23. Negative prompt: what must not appear.
24. Regeneration criteria and diversity check: when to reject and how the scene differs from adjacent scenes.

If a description cannot fill these fields, it is not ready for asset generation or storyboard use.

## Dark / Light Rhythm

Do not default every AI tutorial to a dark graphite proof desk or a light productivity card deck. Start from `internal/visual_style_decision.json`: Codex chooses the brightness and palette from topic type, copy mood, evidence density, and reference rhythm. For beginner-friendly template/tutorial videos, hook/result scenes and final templates often fit `L4 bright tutorial` or `L5 cover/result bright`; for source/code/terminal proof, `L2 dark with bright proof surfaces` or `L3 balanced editorial` may be better.

No more than two dark scenes should appear in a row. If a scene uses a dark background, at least 35% of the frame should be bright proof cards, warm panels, or clean text-safe surfaces. Avoid charcoal-on-charcoal, blue-on-black, teal-only palettes, and full-frame dark gradients.

## Background Plate Description Language

Bad:

```text
高级科技感 AI 背景，未来感，蓝色光效，适合知识讲解。
```

Good:

```text
Create a 16:9 text-free editorial background plate for a Chinese AI explainer about [topic].
The frame should feel like a calm evidence desk where a real source screenshot can be placed on the left and three short explanation chips can be placed on the right.
The background is not the proof; it is a premium support stage for proof panels, captions, and source callouts.

Composition:
A wide horizontal frame with a 1120px proof-safe area on the left, a 360px annotation rail on the right, and a clean 160px lower-third caption-safe band.

Foreground:
Subtle smoked-glass panel edges, brushed metal anchor points, soft contact shadows, no readable text.

Midground:
Abstract browser-frame silhouettes and workflow rails, shaped like a source verification desk, with all labels left blank for HyperFrames HTML overlays.

Background:
Matte graphite editorial room with shallow architectural depth, soft falloff, and restrained negative space. No cyberpunk city, no neon grid, no floating particles.

Camera/lens:
35mm straight-on editorial wide shot, stable keynote framing, no tilted camera.

Lighting:
Soft upper-left key light, restrained teal rim light along panel edges, realistic contact shadows, low ambient glow.

Material/texture:
Smoked glass, matte graphite, brushed aluminum, fine film grain, crisp panel edges, no plastic shine.

Color hierarchy:
Charcoal base, warm ivory text-safe zones, one restrained teal accent for focus.

Motion usage in HyperFrames:
Background only supports a slow 100% to 103% push-in and subtle parallax. The real action comes from proof panels, cursor highlights, annotation chips, and captions.

Evidence boundary:
Generated support background only. Not official UI, not a screenshot, not factual proof.

Negative prompt:
No fake UI, no pseudo Chinese, no random English filler, no logo, no QR code, no neon grid, no particles, no clutter, no text baked into the image, no overexposed highlights, no blurry gradient wallpaper.

Regeneration criteria:
Regenerate if the image looks like a generic tech wallpaper, contains text, has no clean proof zone, competes with captions, lacks material shadows, or feels unrelated to the topic.
```

## Frame And Component Description Language

Bad:

```text
做一个高级信息卡片，带玻璃质感。
```

Why bad: it does not define card purpose, hierarchy, content density, shadow, spacing, or animation state.

Good:

```text
Create a source verification card frame for a 1920x1080 AI explainer.
The card has a 1120px content window, 28px rounded corners, 1px translucent border, soft contact shadow, and a small top-left source badge area.
The inside remains blank because real screenshot content will be inserted by HyperFrames.
The frame should look like a premium editorial proof panel, not a fake app UI.
Leave a lower-third caption-safe band and a right annotation rail.
Motion usage: proof content locks into the frame first, source badge appears 120ms later, annotation chips enter one by one.
Negative prompt: no fake labels, no pseudo interface, no dense micro text, no white lines crossing captions.
```

## Premium Motion Description Language

Bad:

```text
高级动效，卡片飞入，科技感转场，背景动态漂移。
```

Good:

```text
Motion purpose:
Guide the viewer from the opening claim to the real source evidence.

Primary actor:
Left proof screenshot, right annotation rail, cursor highlight, lower-third caption.

Entrance:
At 0.2s, the proof screenshot slides from x=-80 to x=0 over 420ms with cubic ease-out.
At 0.55s, the right annotation rail fades in and moves from x=24 to x=0 over 260ms.
At 0.85s, three evidence chips appear one by one with 120ms stagger.

Keyword motion:
When narration says "先看来源", the cursor draws a soft rectangular highlight around the source title area.
When narration says "这里有一个坑", the risk chip pulses once, turns amber, then locks.

Camera motion:
The root stage performs a slow 100% to 103% push-in across the scene. No rotation, no shaking, no random drift.

Layering:
Background plate remains behind all content. Proof panel casts a soft contact shadow. Caption band always stays above the background and below source callouts.

Caption motion:
Chinese captions fade in over 160ms with no bounce, no typewriter effect for long sentences, and no overlap with proof panels.

Glow:
Use glow only on the active evidence chip. Do not apply glow to all cards.

Audio reactive:
Soft tick when each evidence chip locks. No whoosh spam.

Negative motion:
No infinite pulse, no spinning cards, no random particles, no full-screen flash, no chaotic zoom, no decorative movement unrelated to narration.
```

## Bad Vs Good Examples

### Background

Bad:

```text
AI 科技风背景，蓝色光线，高级质感，适合讲 ChatGPT。
```

Why bad: no information job, no topic binding, no safe zone, no material, no lighting, no proof area.

Good:

```text
A text-free editorial proof desk for a Chinese explainer about ChatGPT agent workflows.
The left side has a large clean proof-safe surface for browser screenshots.
The right side has a narrow annotation rail for three HTML callouts.
The lower third is a dark, quiet caption-safe band.
The visual language should feel like a calm verification workspace, not a tech wallpaper.
```

### Motion

Bad:

```text
卡片炫酷进入，背景有动感。
```

Why bad: no timing, no actor, no relationship to narration, no layering, no negative constraints.

Good:

```text
The source card enters only when the narrator says "先看证据".
It slides from x=-64 to x=0 over 360ms, then locks with a subtle tick.
The annotation rail appears 140ms later so the viewer reads source first, explanation second.
The background stays slow and quiet; only the proof card, cursor, and active chip move.
```
