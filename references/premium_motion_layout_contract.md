# Premium Motion and Layout Contract

Use this contract for every publish-ready AI knowledge video after fixed template selection and before final visual QA. It upgrades motion taste and layout safety without changing topic scan, copywriting, Qingdou, TTS, render, or publishing gates.

## Default Motion Library

Only these named recipes may be used as main transitions or dominant dynamic effects:

1. `metal_aperture_handoff` - current information compresses into a titanium chip, then hands off into the next scene.
2. `glass_prism_refraction` - a glass prism reveals the next information state without distorting readable text.
3. `semantic_node_relay` - a real keyword or status node moves from the old scene into the next information slot.
4. `source_evidence_focus` - source, date, and conclusion lock before the conclusion becomes the next step.
5. `layered_information_assembly` - title, proof, and action layers assemble in the order spoken.
6. `cursor_path_operation` - a cursor follows a real operation path and lands on a real input or result target.
7. `state_lock_microinteraction` - task states lock with small audible feedback.
8. `checklist_matrix_assembly` - checklist items land on fixed grid coordinates with low checklist ticks.
9. `proof_lens_magnification` - a proof lens focuses on a real source, command, file, or result area.
10. `final_template_convergence` - source, steps, and result converge into a saveable final template.

These effects are not decoration. Every transition must carry one of these information jobs:

- source -> conclusion
- conclusion -> step
- step -> result
- old task -> new task
- problem -> checklist
- proof -> template

If an effect does not move information forward, remove it.

## Banned Default Effects

Do not use these as default or fallback motion:

- diagonal line sweep / 斜线扫光
- random horizontal light streak / 横向小光条乱跑
- plain fade / ordinary crossfade / 普通淡入淡出
- simple slide / push slide / 普通左右滑入
- decoration-only connector line / 无信息作用线条
- empty rail sweep / 空导轨扫过
- old card carousel / 旧卡片轮播
- one large static card for a long narration section

If a render contact sheet shows decoration-only diagonal lines, empty rails, or moving lines that do not connect source, step, result, or cursor operation, it is a blocking issue.

## Three-Column Component Rule

Three-column layouts must use `three_column_aligned_checklist`. They are not hand-placed.

Required measurements:

- Equal column widths.
- Same icon center `y` for all columns.
- Same title baseline `y` for all columns.
- Same body text box `y` for all columns.
- Body copy max two lines per column.
- Bottom summary line at least `48px` away from the card border.
- Card inner padding at least `24px`; title area padding at least `36px`.
- Maximum baseline delta `<= 4px`.

If copy does not fit, shorten copy first. Do not let text spill outside the box. Do not lower readability to solve layout.

## Text Fit Rule

Every visible text object must be measured before render:

1. Put text into a fixed text box.
2. Wrap naturally.
3. If it still exceeds the box, reduce within the approved readable size.
4. If it still exceeds the box, rewrite shorter copy.
5. Record the result in `internal/render_layout_manifest.json`.

Forbidden text failures:

- text outside its box
- text touching borders
- text overlapping subtitle/caption/cover text
- decorative line crossing readable text
- text hidden under glow, connector, cursor path, or transition layer
- Chinese text compressed until it looks cheap or hard to read

## Glass Transparency Rule

Every fixed foreground module must preserve dynamic background visibility while keeping text readable.

Required:

- Main module shell alpha normally `0.08-0.16`.
- Local reading/proof/caption layer alpha must stay `<= 0.34`.
- Use feathered `backdrop-filter` / `-webkit-backdrop-filter` plus soft text shadow for readability.
- Stage-level foreground HTML must be transparent; it must not paint a full-frame gradient over the dynamic MP4 background.
- Record the glass profile in `internal/foreground_module_render_manifest.json` as `glass_transparency.profile=glass_transparency_v2`.

Forbidden:

- solid black module cards
- large white, cream, or matte boards
- full-card fills above alpha `0.34`
- hard rectangular dim layers
- baking transparent modules into the background video or support image

## Required Layout Manifest

Before `visual_regression_gate`, write:

```text
internal/render_layout_manifest.json
internal/layout_motion_contract_report.json
```

`render_layout_manifest.json` must include:

- `components[]`
- each component's `text_boxes[]`
- `text_overflow`
- `collision` or `text_collision`
- `min_padding_px`
- `title_padding_px`
- `three_column_groups[]` when a three-column layout appears
- `decorative_paths[]` with `crosses_text=false`
- `glass_transparency` with dynamic background visibility, maximum fill alpha, and backdrop-filter evidence

Then run:

```bash
python3 scripts/check_motion_layout_contract.py --project <project>
```

The report must be `status: "passed"` before final delivery.

## Non-Blocking Workflow Rule

This contract is a visual QA layer only. It must not reorder or replace:

- current-topic scan
- topic scoring
- copy package
- local compliance
- Qingdou
- TTS lock
- voice/SFX mix
- HyperFrames frame-sequence render
- first-frame cover
- publish contract

If this contract fails, only the visual layout/motion stage is reworked.
