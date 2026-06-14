# HyperFrames Components

Use these reusable component patterns before inventing new scene layouts. Each component must keep captions, proof assets, and CTA areas inside the safe zone.

## 1. ColdOpenProofCard

- Purpose: Stop scrolling in the first 3 seconds with a pain line and proof image.
- Inputs: `headline`, `proof_asset`, `caption`, `accent_color`.
- Required assets: real UI screenshot, real output, or result card.
- Recommended duration: 2-3 seconds.
- Motion: fast proof insert, one highlight sweep, short caption reveal.
- Caption safe zone: bottom caption reserved, right action area clear.
- Do not use for: abstract claims without proof.

## 2. ProofWallGrid

- Purpose: Show multiple proof frames quickly.
- Inputs: `proof_assets[]`, `labels[]`, `headline`.
- Required assets: 2-4 real screenshots, outputs, files, or command results.
- Recommended duration: 4-6 seconds.
- Motion: cards assemble into grid, active card scale/focus, light click sounds.
- Caption safe zone: keep labels inside cards, not near right-side buttons.
- Do not use for: fake UI, AI-generated reviews, or unreadable thumbnails.

## 3. UIStepHighlight

- Purpose: Teach one operation on real UI.
- Inputs: `screenshot_or_recording`, `cursor_path`, `highlight_box`, `step_label`.
- Required assets: real UI screenshot or recording.
- Recommended duration: 3-5 seconds.
- Motion: cursor move, highlight box snap, label fade.
- Caption safe zone: subtitle below UI, callout beside highlighted area.
- Do not use for: product UI that is invented or unverified.

## 4. BeforeAfterCompare

- Purpose: Compare wrong method and corrected method.
- Inputs: `before_asset`, `after_asset`, `before_label`, `after_label`, `difference_callout`.
- Required assets: real before/after output or designed comparison cards from real text.
- Recommended duration: 4-7 seconds.
- Motion: split screen slide, divider reveal, after side emphasis.
- Caption safe zone: labels inside top of each panel.
- Do not use for: vague claims without visible difference.

## 5. MistakeCorrectionCard

- Purpose: Correct a common mistake.
- Inputs: `mistake`, `correction`, `why`, `proof_asset`.
- Required assets: error prompt/result or real failed output.
- Recommended duration: 3-5 seconds.
- Motion: mistake strike-through, correction card lands, proof flash.
- Caption safe zone: keep correction large and centered.
- Do not use for: shaming users or absolute claims.

## 6. PromptTemplateCard

- Purpose: Make a reusable prompt or workflow easy to save.
- Inputs: `template_title`, `slots[]`, `example_fill`, `copy_hint`.
- Required assets: template text and one real filled example.
- Recommended duration: 5-8 seconds.
- Motion: slots build one by one, filled example reveal.
- Caption safe zone: template text must stay readable on mobile.
- Do not use for: long paragraphs that cannot be read.

## 7. ChecklistBuild

- Purpose: Turn a method into a saveable checklist.
- Inputs: `items[]`, `proof_map[]`, `title`.
- Required assets: checklist text and optional proof frame per item.
- Recommended duration: 4-7 seconds.
- Motion: checkmarks appear in sync with narration.
- Caption safe zone: do not stack checklist over subtitles.
- Do not use for: more than 5 items in one scene.

## 8. TimelineProcess

- Purpose: Explain a 3-step process.
- Inputs: `steps[]`, `timestamps_or_order`, `proof_assets[]`.
- Required assets: one proof frame or output per step.
- Recommended duration: 5-8 seconds.
- Motion: timeline progress line, step focus, proof pop-in.
- Caption safe zone: timeline stays center-left, captions bottom.
- Do not use for: unrelated tools with no workflow connection.

## 9. ResultReveal

- Purpose: Delay payoff, then reveal the result.
- Inputs: `setup_line`, `masked_result`, `reveal_label`, `proof_asset`.
- Required assets: real output or result screenshot.
- Recommended duration: 3-5 seconds.
- Motion: mask wipe, zoom to result, short sound cue.
- Caption safe zone: reveal label away from UI controls.
- Do not use for: results that are subjective or unverified.

## 10. ClaimProofPair

- Purpose: Bind one spoken claim to one proof frame.
- Inputs: `claim`, `proof_asset`, `source_label`, `risk_note`.
- Required assets: official doc, UI screenshot, command output, or file result.
- Recommended duration: 3-4 seconds.
- Motion: claim card enters, proof locks beside it, source label appears.
- Caption safe zone: source label small but readable.
- Do not use for: unsupported factual claims.

## 11. MiniCaseBreakdown

- Purpose: Break one case into setup, action, and result.
- Inputs: `case_title`, `setup_asset`, `action_asset`, `result_asset`, `lesson`.
- Required assets: three proof frames from the same case or concept design.
- Recommended duration: 6-9 seconds.
- Motion: three-stage stack, current stage spotlight, lesson strip.
- Caption safe zone: lesson strip above bottom captions.
- Do not use for: fake client cases, fake metrics, or unverified outcomes.

## 12. FinalRecapCTA

- Purpose: End with a recap and save reason.
- Inputs: `recap_items[]`, `save_reason`, `next_action`.
- Required assets: recap card and optional final proof thumbnail.
- Recommended duration: 3-5 seconds.
- Motion: recap strip builds, save reason highlights, soft exit.
- Caption safe zone: no heavy bottom panel that hides content.
- Do not use for: forced likes, comments, private contact, QR codes, or guaranteed results.

## Global Rules

- Match the component to the shot type.
- Do not use the same bottom caption card for the whole video.
- Keep UI screenshots readable at phone size.
- Keep every component's critical content inside the phone-safe canvas: top >= 240px, bottom >= 360px, left >= 72px, right >= 180px for 1080x1920. The outer top/bottom bands are background breathing room, not content space.
- Generated images used inside components must be prompted with generous top and bottom negative space; crop or regenerate images that put faces, UI proof, cards, subtitles, or CTA near the 9:16 edges.
- Use normal narration speed only. If a component needs more explanation, split it into additional visual beats instead of speeding up TTS.
- Add light sound effects for page changes, proof wall assembly, cursor clicks, and result reveals. Keep them below narration volume.
- Avoid ordinary Ken Burns zoom as the main motion.
