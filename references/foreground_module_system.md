# Foreground Module System

This is the execution contract for premium AI knowledge foreground motion. It does not replace the topic, copy, compliance, voice, cover, render, Qingdou, or publish gates.

## Source Files

Read the foreground system in this order:

1. `references/foreground_art_module_library_v1.md` for M01-M20 artistic direction, material language, object structure, motion cause/effect, SFX, and slot vocabulary.
2. `references/foreground_art_module_library_v2.md` for M01-M20 layout, aspect adaptation, text hard limits, implementation notes, QA failures, and transition pairing.
3. `references/foreground_art_module_library_v2.json` for machine-readable M01-M20 selection, slots, bounds, transitions, and ready-gate values.
4. `references/foreground_micro_component_library_v1.md` for C01-C30 embedded component design and execution rules.
5. `references/foreground_micro_component_library_v1.json` for machine-readable C01-C30 compatibility, anchors, budgets, text limits, and ready-gate values.

The fixed mapping is `01=M01` through `20=M20`. The v2 files are additive; never use them to delete or flatten the v1 art direction.

Runtime notes must describe the selected construction, not the historical problem list. Use phrasing such as `S03 uses M01 + C01/C03/C08/C27/C30, TR04 in, TR06 out, passed foreground_module_plan_check.json`. Keep failure vocabulary inside validator output, QA reports, tests, or blocked audit notes.

## Required Planning Artifact

Before HyperFrames authoring, create:

```text
internal/foreground_module_plan.json
```

Each planned scene must select exactly one parent module `M01`-`M20`, inherit its v1 art direction, apply the v2 execution fields, then select two to five micro-components `C01`-`C30` only when they carry real scene information.

The plan must record:

- `scene_id`
- `aspect_ratio`
- `layout_mode`
- `parent_module_id`
- parent module `text_slots`
- `micro_components[]` with `component_id`, `anchor`, `phase`, and `text_slots`
- `transition_in`
- `transition_out`
- budget signals used by QA

Validate the plan with:

```bash
python3 scripts/check_foreground_module_plan.py --project outputs/demo
python3 scripts/render_foreground_module_pack.py --project outputs/demo
python3 scripts/check_foreground_module_render_pack.py --project outputs/demo
```

## Selection Rule

Use the copy and storyboard intent to choose modules:

```text
copy / narration beat
-> choose one M01-M20 parent module
-> read v1 art description
-> apply v2 layout and execution rules
-> choose 2-5 C01-C30 micro-components
-> check anchors, text limits, visual budgets, motion concurrency, and ready gate
-> enter HyperFrames
```

Micro-components are precision parts inside a parent module. They must originate from parent slots, rails, pins, locks, lenses, tracks, or mounts. They must not become standalone pages, floating labels, decorative badges, or separate cards.

## Scene Budget

- 9:16 scenes normally use 2-4 micro-component types.
- 16:9 scenes normally use 2-5 micro-component types.
- Hard maximum: 5 component types, 9 visible instances, 3 text-bearing micro-components.
- Portrait visual weight maximum: 7.
- Landscape visual weight maximum: 9.
- Component animation concurrency maximum: 2.
- During the parent module core `process` action, add at most one lightweight micro-component with `motion_weight <= 1`.

If the selected copy exceeds a parent slot or micro-component text limit, rewrite shorter copy or split the beat into another shot. Do not shrink fonts, compress glyphs, hide overflow, or turn the scene into a generic card.

## Render Contract

HyperFrames implementation must use HTML, CSS, inline SVG, and GSAP. The foreground system forbids WebGL, Three.js, real 3D model files, or offline 3D render dependencies for core readable information.

The parent module remains the main visual object. Micro-components add parameters, status, evidence, metrics, boundaries, verification, or conclusions in the correct parent phase. When a micro-component has no matching information job, do not render it.

## QA Gate

`foreground_module_plan.json` is not proof by itself. It is the design construction plan. It must pass `scripts/check_foreground_module_plan.py`, then produce `foreground_module_render_pack.html`, `foreground_module_render_manifest.json`, and `foreground_module_render_check.json` with `scripts/render_foreground_module_pack.py` and `scripts/check_foreground_module_render_pack.py`. The final rendered video still must pass `render_layout_manifest.json`, `layout_motion_contract_report.json`, `visual_review.json`, and `visual_regression_gate.json`.

Blocking failures include:

- missing parent module selection
- unknown M/C ids
- micro-component incompatible with the selected parent module
- anchor not provided by the parent module adapter
- text slot overflow
- visual budget overflow
- too many component types or visible instances
- standalone or floating micro-components
- component motion that does not follow the parent timeline
- render pack missing scene/module/component DOM
- render pack missing runtime CSS/JS or parent-module render contract
