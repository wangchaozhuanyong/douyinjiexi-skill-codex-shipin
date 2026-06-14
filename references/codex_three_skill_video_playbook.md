# Codex Three Skill Video Playbook

Use this when a user provides a polished Codex/Skill/Agent reference video, asks to learn its production method, or asks for a video about multiple Codex skills or plugins.

## Reference Learning Summary

The provided reference is a 16:9, about 77-second Codex skill tutorial. Its useful pattern is not camera shake or decorative transitions. Its strength is proof-first teaching:

- 0-3s: result/status hook, such as "高手不会告诉你的三个 Skill".
- 3-8s: immediate proof that the tools exist and produce results.
- Body: each Skill chapter follows the same evidence chain: name -> where it exists -> one operation -> output proof -> why it matters.
- Ending: clear save reason and workflow recap.

Learn this structure, pacing, proof density, and screen hierarchy. Do not copy the reference frames, subtitles, voice, music, exact wording, creator identity, or full sequence.

## Three Tool Roles

For videos that teach or use `Remotion`, `HyperFrames`, and `ImageGen`, document the production stack in `storyboard.json`.

- `ImageGen`: create cover/poster concepts, example result cards, abstract transitions, visual metaphors, and image-rich proof panels. It must not fake official UI, fake analytics, fake reviews, or fake product screenshots.
- `Remotion`: create code-driven animation, reusable React components, dynamic data visuals, frame-accurate sequences, and previewable motion graphics. Use `Sequence`, `useCurrentFrame()`, `interpolate()`, `Easing`, `staticFile()`, and real assets in `public/` when building Remotion projects.
- `HyperFrames`: assemble the final timeline, Chinese captions, safe-zone layout, proof cards, SFX, voice synchronization, QA frames, and final render.

If one tool is not actually used in production, still explain its role only when the video teaches it, and show truthful evidence. Do not imply an installed or executed tool was used when it was only discussed.

## Required Storyboard Stack

For Codex/Skill/plugin tutorials, add top-level `production_stack`:

```json
{
  "production_stack": {
    "reference_learning_applied": true,
    "reference_pattern": "three_skill_reference",
    "workflow_order": [
      "ImageGen creates visual material",
      "Remotion creates component-level animation",
      "HyperFrames assembles final timeline and render"
    ],
    "primary_tools": [
      {
        "name": "Remotion",
        "role": "component animation and data-driven visuals",
        "evidence_chain": {
          "entry_or_source": "official docs, GitHub, installed skill, or local project",
          "operation_or_step": "one visible command, component, preview, or render step",
          "output_or_result": "rendered clip, still frame, component output, or file",
          "viewer_value": "why this helps the creator"
        }
      }
    ]
  }
}
```

Every scene that names a primary tool must include `visual.proof_chain` with:

- `entry_or_source`
- `operation_or_step`
- `output_or_result`
- `viewer_value`

## Scene Formula

Use this for each named Skill:

1. Chapter card: `1. Remotion` or the current tool name.
2. Entry proof: official page, GitHub repo, Codex skill list, plugin list, local folder, or command output.
3. Operation proof: a visible prompt, command, component, timeline, file, upload, or render action.
4. Result proof: generated image, rendered frame, MP4, output folder, side-by-side comparison, or proof wall.
5. Viewer value: one plain Chinese sentence explaining when to use it.

Do not spend a whole chapter on a static screenshot. Split one image into more scenes or reveal one callout per spoken point.

## Motion Rules

- Use useful motion: card insertion, cursor-led highlight, mask reveal, split-screen slide, proof-wall assembly, component timeline, or word highlight.
- Do not use page shaking, random camera drift, loop pulse, or Ken Burns zoom to hide weak content.
- Every 3-5 seconds needs a new proof, reveal, operation, output, or decision rule.
- Every 6-8 seconds needs a retention beat: new tool reveal, before/after, result grid, mistake correction, or saveable checklist.

## Evidence Minimum

For three-Skill tutorials:

- At least 60% of runtime should be evidence or output proof.
- Each primary tool needs at least one entry/source proof and one output/result proof.
- Generated images can support the visual system, but real screenshots, local files, terminal output, docs, or rendered artifacts carry trust.

## Remotion Integration Notes

Use the installed `remotion-best-practices` skill when building or reviewing Remotion code.

Key rules to carry into this skill's planning:

- Use `Sequence`/`Series` to split timeline steps.
- Drive animation with `useCurrentFrame()` and `interpolate()`; do not rely on CSS transitions for Remotion rendering.
- Use `staticFile()` and `public/` for assets.
- Use frame-accurate still checks for crowded UI or title frames.
- Keep Remotion as a motion-graphics/component provider, then let HyperFrames handle final Chinese tutorial packaging unless the user explicitly asks for a pure Remotion render.
