# Codex Three Skill Video Playbook

Use this when a user provides a polished Codex/Skill/Agent reference video, asks to learn its production method, or asks for a video about multiple Codex skills or plugins.

## Reference Learning Summary

The provided reference is a 16:9, about 77-second Codex skill tutorial. Its useful pattern is not camera shake or decorative transitions. Its strength is proof-first teaching:

- 0-3s: result/status hook, such as "高手不会告诉你的三个 Skill".
- 3-8s: immediate proof that the tools exist and produce results.
- Body: each Skill chapter follows the same evidence chain: name -> where it exists -> one operation -> output proof -> why it matters.
- Ending: clear save reason and workflow recap.

Learn this structure, pacing, proof density, and screen hierarchy. Do not copy the reference frames, subtitles, voice, exact wording, creator identity, or full sequence. For user-provided Douyin references intended for Douyin publishing, use the same reference music under the same-platform music rule when technically possible.

## Skill Value Proof Montage Adapter

Use this adapter when the reference or requested topic is a horizontal, voice-led video such as `三个 Codex 神级 Skill`, where the purpose is not just to list Skill names but to make the viewer believe each Skill is worth using.

Content job lock:

```text
recommend or teach multiple Codex Skills by proving where each one exists,
what operation it performs, what output it creates, and why the viewer should care
```

Do not route this format to `方案1: Skill 推荐无人声`. This adapter is for 16:9, 60-90 second, proof-heavy, narration-led production stack explainers.

Recommended structure:

1. `Authority Hook`: bold Chinese headline with one information-gap promise. Avoid copying the reference wording.
2. `Existence Proof`: GitHub, official page, plugin list, local folder, docs, or source UI appears within the first 8 seconds.
3. `Output Proof Wall`: 2-4 concrete outputs appear before long explanation, so the viewer sees the payoff early.
4. `Skill Chapter 1`: entry/source proof -> one operation -> output proof -> viewer value.
5. `Skill Chapter 2`: entry/source proof -> one operation -> output proof -> viewer value.
6. `Skill Chapter 3`: entry/source proof -> one operation -> output proof -> viewer value.
7. `Industry Task Compare`: ordinary workflow vs Skill-assisted workflow, with a visible before/after or time-saving contrast.
8. `Workflow Promise Lock`: final line compresses the stack into one memorable workflow promise.

Every named Skill needs a `SkillValueProofChain`:

```json
{
  "skill_name": "Tool or Skill name",
  "entry_or_source": "official page, GitHub, plugin list, local folder, or command output",
  "operation_or_step": "visible prompt, command, install, upload, edit, render, or file generation",
  "output_or_result": "image, video frame, page, folder, code artifact, dashboard, or rendered file",
  "viewer_value": "one plain Chinese sentence explaining when to use it"
}
```

Motion rules for this adapter:

- Every 3-5 seconds must introduce a new proof, output, comparison, operation, or chapter card.
- Output proof should enter as cards, grids, split screens, or slide-scale reveals; do not use one long static screenshot.
- Bottom subtitles stay short, thick, and high-contrast; they support the voice, not replace the visual proof.
- Use cursor highlights, page snap-ins, card insertion, proof-wall assembly, light sweeps, and controlled zooms.
- Avoid decorative shaking, random drift, repeated glow pulses, and generic AI robot/circuit stock.

Audio rules:

- This adapter is usually voice-led. Use a continuous narration bed.
- For this user's recurring AI videos, keep the approved strong male lecturer direction unless the user says otherwise.
- SFX should mark page changes, proof card landings, cursor clicks, and final lock moments, always below narration.

Originality rules:

- Learn the sequence logic, not the actual sequence.
- Do not copy the reference subtitles, case images, hand footage, product screenshots, exact examples, creator brand, or voice. For user-provided Douyin references intended for Douyin publishing, use the same reference music under the same-platform music rule when technically possible.
- If the same public tool names are used, capture fresh source/proof assets and write new Chinese explanations.
- The final video must have an original topic angle, original wording, new proof assets, and a new storyboard.

## Three Tool Roles

For videos that teach or use `Remotion`, `HyperFrames`, and `ImageGen`, document the production stack in `storyboard.json`.

- `ImageGen`: create cover/poster concepts, example result cards, abstract transitions, visual metaphors, and image-rich proof panels. It must not fake official UI, fake analytics, fake reviews, or fake product screenshots.
- `Remotion`: create code-driven animation, reusable React components, dynamic data visuals, frame-accurate sequences, and previewable motion graphics. Use `Sequence`, `useCurrentFrame()`, `interpolate()`, `Easing`, `staticFile()`, and real assets in `public/` when building Remotion projects.
- `HyperFrames`: assemble the final timeline, Chinese captions, safe-zone layout, proof cards, SFX, voice synchronization, QA frames, and final render.

If one tool is not actually used in production, still explain its role only when the video teaches it, and show truthful evidence. Do not imply an installed or executed tool was used when it was only discussed.

## Six-Tool Plugin Stack

For videos that teach the screenshot-style "Codex must-have video tools" list, use `references/runtime_decision_matrix.md` and classify all six tools before writing the script:

- `HyperFrames`: installed/available Codex video runtime when this session exposes the HyperFrames skill or `npx hyperframes` works.
- `FFmpeg`: local CLI capability for media processing, not a Codex plugin.
- `OpenMontage`: optional external open-source production workflow adapter; only claim usage with local repo/install evidence.
- `Remotion`: Codex skill guidance plus optional local React video runtime; only claim rendering when a project or `npx remotion` command is actually used.
- `Video-Use`: optional external open-source editing adapter; only claim usage with local repo/install evidence.
- `Manim`: optional Python animation runtime for math/diagram clips; only claim usage when the environment contains Manim or setup is approved and completed.

The teaching angle must be honest: "哪些已经能直接用，哪些只是可选安装，哪些适合什么场景." Do not present optional adapters as already installed plugins.

For videos that teach actual Codex plugins, also read `references/codex_plugin_integration.md` and add `codex_plugin_plan` to `storyboard.json`. If the video says "six plugins", the plan must classify Browser, GitHub, Hugging Face, HyperFrames, OpenAI Developers, and HeyGen separately. HeyGen must be marked approval-required unless the user already approved the specific generation path.

## Required Storyboard Stack

For Codex/Skill/plugin tutorials, add top-level `production_stack`:

```json
{
  "production_stack": {
    "reference_learning_applied": true,
    "reference_pattern": "three_skill_reference",
    "workflow_order": [
      "ImageGen creates visual material",
      "Remotion creates component-level animation when needed",
      "HyperFrames assembles final timeline and render",
      "FFmpeg verifies and packages the final media"
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
