# AI Video Director Orchestrator

This is the anti-template layer for AI-circle videos. It prevents Codex from turning the newest reference video into the next fixed style.

## Hard Rule

Before copywriting, storyboard, image prompts, TTS, HyperFrames, render, or upload, every publish-ready AI video must produce these files:

- `internal/director_selection.json`
- `internal/style_recipe.json`
- `internal/hook_variants.json`
- `internal/hook_score_report.json`
- `internal/reference_overfit_audit.json`

If any file is missing or not passed, stop. Do not silently continue with the latest reference style.

## Decision Order

1. Lock the content job first.
2. Classify the AI scheme from `references/ai_video_scheme_library.md`.
3. Select reference cards as candidates, not templates.
4. Select one main visual family for the whole video.
5. Select a reusable fixed production template set with `scripts/select_fixed_ai_templates.py`.
6. Select a component and motion mix from the registry.
7. Generate at least 10 hook variants.
8. Score hooks and select one.
9. Audit reference overfit.
10. Only then write the full script and storyboard.

## Content Job Beats Visual Style

The same background style cannot solve every job. A tutorial, news explainer, tool stack, checklist, and operation proof need different component mixes.

AI 热榜 TOP5 is its own content job. When the user asks for `AI 热榜`, `TOP5`, `榜单`, `排行`, or `排名`, classify it as `scheme_7_ai_hot_rank_top5`, use `references/ai_video_scheme_7_hot_rank_top5.md`, and require five scored source-backed rank items before copywriting. Do not collapse it into a single news explainer or a generic checklist.

Visual selection must cite:

- topic/source type
- viewer task
- proof density
- format
- reference rhythm when present
- why the selected style is better than other schemes

## Reference Pool Rule

Reference videos are stored as reusable style cards. A new reference adds one card to the pool. It must not replace the whole system.

Allowed from a reference:

- pacing category
- layout logic
- motion vocabulary
- density
- music/voice relationship
- hook logic

Forbidden from a reference:

- original frames
- original subtitles or copy
- original voice
- creator identity
- watermark
- full shot sequence
- one-to-one timing path

## Rotation Rule

Each video chooses one main visual direction. Different scenes may change shot scale, proof density, component shape, and foreground layout, but must not switch to a different art system.

The chosen direction controls:

- palette
- material
- background plate
- foreground UI components
- caption system
- transition language
- SFX character
- glow/metal/blur strength

`internal/fixed_template_selection.json` is the execution lock for this direction. It must name the selected dynamic background MP4 asset, transition/SFX pack, component pack, and voice mix profile. The selected background must include `background_template.render_asset_path` pointing to `assets/ai_background_templates_dynamic/`; do not regenerate a new background per video unless the user explicitly asks to replace the fixed library. `background_template.fixed_asset_path` is only a legacy alias to the same dynamic MP4 path. These are fixed templates, but copy, screenshots, evidence, and subtitles remain topic-specific.

## Copy Hook Rule

Do not accept the first hook. Generate at least 10 variants and score them for:

- concrete AI object named
- viewer pain in first 3 seconds
- visible result promised
- proof hint
- save/share value
- low hype and low empty talk
- spoken Chinese rhythm

The selected hook must score at least 8.5. If not, rewrite the hook set before copywriting.

## Anti-Overfit Rule

`reference_overfit_audit.json` must prove:

- the latest reference is not treated as the default
- selected reference cards are limited and justified
- component mix contains more than one pattern
- no original reference text or frame is reused
- cooldown or rotation reason is recorded
- copy and visual system are selected for the current content job
