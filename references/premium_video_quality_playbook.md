# Premium Video Quality Playbook

Use this before storyboard, asset generation, HyperFrames authoring, rendering, and final QA whenever the user asks for a high-quality, polished, reference-level, premium, or publish-ready AI-circle short video.

Also read `references/premium_ai_video_source_to_hyperframes_rule.md`, `references/visual_description_language_reference.md`, and `references/ai_generated_asset_prompt_system.md`. Premium AI videos must start from proof sources, then turn plain-language copy into sentence-level visual tasks before HyperFrames authoring. Any AI-generated visual asset must start from a prompt pack, not a one-line prompt.

## Quality Principle

High quality is not motion on top of weak content. High quality means:

- the first frame looks like a designed poster
- Proof-heavy AI knowledge videos and AI explainers use 16:9 `1920x1080`; do not switch to 9:16 for Douyin if the content is AI/tool/tutorial proof. Reference-driven lightweight guide/list/card/poster explainers may use 9:16 only under `references/reference_driven_production_rules.md`.
- every AI video starts with topic-bound descriptive background art direction before storyboard or render work
- every named claim is supported by visible proof
- every important sentence has a visual task, not just a caption over a card
- every scene has foreground, middle-ground, and background hierarchy
- the background is a designed stage with spatial depth, material, lighting, text-safe zones, and a visible relationship to the selected topic
- screenshots and cards are readable on a phone
- movement explains a step, reveals a detail, or guides attention
- page/scene switching never cuts the speaker mid-sentence
- sound effects are subtle but present when UI/proof cards switch
- final export is crisp enough for platform recompression

## Required `quality_spec`

Every publish-ready storyboard and metadata package must document `quality_spec`.

```json
{
  "quality_spec": {
    "target_quality_level": "high_quality",
    "visual_system": "blackboard-grid proof tutorial",
    "motion_policy": "useful motion only; no shake, no random drift, no Ken Burns as main motion",
    "still_image_policy": "split dense images into steps; reveal one point per voice beat",
    "evidence_policy": "real UI / source / output proof first; generated visuals support but do not replace proof",
    "sfx_policy": "subtle click, whoosh, card insert, marker sweep below narration",
    "render_policy": "HyperFrames quality high plus high-bitrate H.264 pass when needed",
    "cover_policy": "standalone poster cover, not a random frame grab",
    "frame_review_policy": "first 5 seconds, full contact sheet, and crowded detail frames must be reviewed",
    "provider_policy": "free_first_local_or_authorized_openai_only",
    "runtime_choice": "HyperFrames final timeline; Remotion component clips when needed; FFmpeg only for mechanical media",
    "caption_template_plan": "mix word_highlight, proof_callout, side_label, chapter_card, and final_takeaway as scene type changes",
    "timeline_contract_ref": "internal/timeline_contract.md"
  }
}
```

## Scene-Level Design Contract

Every scene must document:

- `visual.design_layers`: at least 3 layers, such as background grid, framed screenshot, callout marker, subtitle rail, cursor/highlight.
- `visual.quality_checks.source_resolution_ok`: the screenshot/generated asset is not a low-res upscale.
- `visual.quality_checks.text_safe`: titles, subtitles, proof cards, and CTA do not collide.
- `visual.quality_checks.not_template_like`: the frame does not look like a generic template or empty stock background.
- `visual.quality_checks.not_static_dump`: one image is not carrying several points without reveal/focus/split.
- `visual.asset_source_type`: `proof`, `support`, `generated`, or `free_stock`.
- `visual.caption_template`: the scene's caption component, matched to scene type.

If any of these cannot be truthfully set to `true`, the scene is not ready.

## Minimum Premium Structure

For a 60-90 second AI/Codex tutorial:

- 0-3s: poster-grade hook with a proof/result hint.
- 3-8s: proof wall or before/after, not a slow intro.
- 8-12s: promise/setup in plain Chinese.
- Body: each chapter shows entry/source, operation, result, and viewer value.
- Final 3-5s: recap formula, save reason, and clean end frame.

## Asset Quality Rules

- Do not scale a 1280x720 screenshot to fill a 1920x1080 proof frame.
- For 1920x1080 output, large screenshots should be captured at 1920x1080 or higher.
- For non-AI 1080x1920 output, screenshots/cards must be readable in the central safe area. AI knowledge output should remain 1920x1080.
- If a proof frame looks soft, recapture the source, crop less aggressively, or render with higher bitrate.
- If generated images contain pseudo-Chinese, malformed text, random English filler, fake UI, fake logos, or unreadable labels, reject them.
- Before storyboard, assets, TTS, HyperFrames, render, or upload, create `internal/visual_style_decision.json`, `internal/visual_style_plan.json`, and `internal/background_prompt_pack.md` with 3-5 descriptive background directions and selected/generated text-free `1920x1080` background plate(s).
- `visual_style_decision.json` must make Codex's director choice from topic type, copy mood, evidence density, and reference rhythm when present. It must record `style_intent`, selected brightness/palette/material/layout, `why_this_style`, and `why_not_other_styles`. `daylight_productivity` and light tutorial cards are candidates only, never defaults.
- `visual_style_plan.json` must match the decision before individual prompts: `scene_function`, `visual_archetype`, `brightness_grade`, `palette_family`, `material_family`, `layout_family`, dark/light rhythm, and diversity limits. Do not let every scene collapse into dark, cold, glass-card tech wallpaper or repeated light productivity cards without a content reason.
- Register every generated background in `asset_manifest.json` as `asset_role=background_plate`, `type=generated_visual`, `asset_source_type=generated`, `is_evidence=false`, `model`, `prompt_id`, `prompt_path`, `unique_prompt=true`, `evidence_boundary`, `visual_thesis`, `topic_binding`, `beginner_usefulness`, `information_job`, `background_role`, and the complete visual director fields required by `references/ai_generated_asset_prompt_system.md`.
- Before generating any AI-made asset, write `internal/ai_asset_prompt_pack.md` or equivalent production notes using `references/ai_generated_asset_prompt_system.md`.
- Every generated asset needs a unique prompt card with scene ID, narration line, scene function, visual archetype, brightness grade, palette/material/layout family, beginner usefulness, viewer takeaway, foreground/midground/background design, camera/lens, lighting, material/texture, color system, depth/layering, text-safe zones, HyperFrames motion usage, animation affordance, primary animated object, dark/light motion rule, negative prompt, regeneration criteria, and diversity check.
- Each generated asset prompt must score at least 9/10 before generation.
- Run `scripts/validate_visual_tone.py` on generated/support visuals and block over-dark L4/L5 frames, crushed dark scenes, insufficient bright proof surfaces, or teal/blue-only palette bias.
- Generated images and free-stock assets cannot be counted as product proof.
- Paid providers and scraping sources are blocked unless the user explicitly approves them for the current job.

## 16:9 AI Knowledge Rule

For AI explainers, AI news, AI tools, ChatGPT, Gemini, OpenAI, Codex, Agent explainers, automation, AI coding, AI workflow, plugin tutorials, Skill tutorials, code/product walkthroughs, and source-heavy AI videos, use `1920x1080` 16:9.

16:9 scene structure should usually be:

- left or center proof stage: large browser/source/code/product panel
- right annotation rail: 1-3 short labels or checklist items
- lower-third caption: stable position, no jumping between scenes
- background plate: quiet spatial environment, no random grid or unreadable pseudo text
- chapter rail: small top/side marker that remains stable across transitions

Do not use 9:16 for proof-heavy AI knowledge videos under this skill. If a task is genuinely vertical-native and non-AI, route it to the owning vertical-video skill instead of this AI workflow. If a vertical reference is supplied and the result is a lightweight AI guide/list/card/poster explainer, use the reference-driven 9:16 exception and keep originality, text accuracy, safe-zone, compliance, and QA gates.

## Premium Background Description

A premium background is not a decorative wallpaper. It is a stage for information.

Weak prompt:

```text
高级科技感 AI 背景，炫酷，未来感，蓝色光效。
```

Good prompt:

```text
Create a 16:9 premium editorial control-room background for an AI Agent explainer.
The frame has a wide matte-graphite stage, a large empty proof area in the center-left, and a quiet right-side annotation rail.
Use smoked glass panels, brushed metal edges, soft upper-left key light, restrained teal rim light, realistic contact shadows, and fine film grain.
Keep all text zones clean and dark enough for ivory Chinese captions.
No fake UI, no pseudo text, no random neon grid, no particles, no linework crossing captions.
```

The background prompt must specify role, space, material, lighting, camera, palette, texture, text-safe areas, and avoid rules.

The prompt must also explain how the generated image will become a moving scene: what layer can parallax, where HyperFrames should reveal cards, which rail or proof tray can move, and what should remain stable for subtitles. If no motion handoff exists, the image is only a wallpaper and should be rewritten.

It must also specify:

- `visual_thesis`: the exact topic-specific visual idea, not just a mood.
- `topic_binding`: the selected AI topic/tool/source/workflow the background is built for.
- `information_job`: what proof cards, operation simulation, comparison, checklist, or final template it must support.
- `background_role`: how it acts as a text-free stage and not fake evidence.

Reject the background if it looks like a decorative showroom, empty skeleton, generic cyber wallpaper, or a beautiful stage that could be reused for any topic.

## Motion Craft Rules

Allowed useful motion:

- cursor-led highlight
- card insertion
- mask wipe
- split-screen slide
- proof-wall assembly
- timeline rail draw
- marker sweep
- component/frame reveal
- localized parallax between layers

Every motion note must say what information the motion explains. Use this structure:

```text
Purpose: [reveal / compare / verify / warn / connect / summarize]
Actor: [source card / cursor / risk gate / proof rail / node / caption]
Path: [from where to where]
Timing: [exact voice phrase or sentence boundary]
Easing: [calm ease-out / keynote reveal / mechanical snap]
Continuity: [what stays on screen while the visual changes]
Audio bridge: [none / soft click / low whoosh below narration]
```

Scene/page changes must happen only at sentence end, breath pause, chapter pause, or documented visual handoff. If narration continues, overlap old and new visuals for 8-14 frames and keep a stable anchor on screen.

Rejected motion:

- page shaking
- full-screen random drift
- Ken Burns zoom as the main motion
- repeated pulse glow
- transition spam with no information change
- hard replacement cut while narration is mid-sentence

## Sound And Export Rules

- Use restrained SFX when cards land, pages switch, proof frames insert, or marker sweeps happen.
- Keep SFX below narration and never mask Chinese speech.
- Use normal Mandarin speed only.
- Render HyperFrames with `--quality high` for publish-ready work.
- If HyperFrames audio is truncated, remux the full source audio and re-run QA.
- `metadata.quality_spec.min_bitrate` should normally be at least `3500000`; raise it for screenshot-heavy or horizontal proof-wall videos.

## Final Review

Before `pre_publish_gate.py` and `promote_final.py`:

- inspect the first 5 seconds
- inspect the standalone publish cover at full size
- confirm `publish_cover_text.txt` was included in local text compliance
- inspect the full contact sheet
- inspect crowded proof/detail frames at original size
- confirm no title/subtitle/card collision
- confirm no low-res upscaled proof frame
- confirm SFX policy is documented
- confirm final MP4 duration, audio duration, resolution, fps, and bitrate
