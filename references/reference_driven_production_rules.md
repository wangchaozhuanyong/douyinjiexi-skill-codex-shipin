# Reference-Driven Production Rules

Use this whenever the user provides a Douyin link, local video, screenshot set, or says to make a video like a reference. This rule applies across the three video families: AI knowledge, renovation/full-house custom, and beauty portrait choice videos.

## Core Rule

Reference-driven production is not copying. The reference is used to learn the style system, pacing, scene rhythm, typography hierarchy, music/voice relationship, filter mood, and motion language. The final video must be independently planned, independently written, independently generated/rendered, and independently QA'd.

## Video Body First Rule

When the user provides a video reference by Douyin link, share text, local MP4, screenshots paired with a video request, or natural language such as "参考这个视频" / "做得像这个视频", do not begin copywriting, storyboard, HyperFrames authoring, rendering, or final delivery from metadata alone. First obtain the playable reference video body when technically possible: download the video, use the provided local file, or otherwise create a local playable analysis file under the project reference folder.

After obtaining it, actually inspect the video body with ffprobe plus contact sheets, detail frames, timeline scrubbing, or manual viewing. The analysis must record duration, resolution/aspect, fps, first 3-5 seconds, shot rhythm, layout family, typography hierarchy, text density, motion language, music/voice relationship, and what must not be copied.

Title text, cover image, share caption, URL metadata, author page, music page, or hashtags alone are not a reference-video analysis. If the video body cannot be obtained, stop before production with a blocker and ask for the local video file, another downloadable reference, screenshots-only approval, or explicit approval to proceed without video-reference matching. If the user supplies only screenshots, label the run as screenshot-only reference and do not claim video pacing, duration, audio, or motion were learned from the original video.

Do not reuse original frames, original screenshots, original people, original room photos, original subtitles, original written copy, creator identity, logo, watermark, or a highly similar full sequence. Do not trace the reference shot-for-shot. Music has a user-specific Douyin rule: when the user provides a Douyin reference video and the final output is also for Douyin publishing, treat the reference music as user-authorized for same-platform Douyin use and use the reference video's own music or same Douyin music-page track when technically possible. Do not synthesize or generate replacement BGM. If the same reference music cannot be obtained or used, record a blocker and ask for the music file, platform same-music selection, or explicit approval to proceed without BGM. For non-Douyin publishing, cross-platform reuse, commercial use outside Douyin, or references not supplied by the user, use the same music only with explicit authorization; otherwise use authorized local/free-stock music.

## Required Order

1. Ingest the reference: Douyin link, share text, local MP4, screenshots, or extracted frames.
2. Obtain the playable video body for video references. Save the downloaded/provided video under the project's reference folder and record the local path, duration, hash, and any blocker. Do not treat title/share/music metadata as sufficient video analysis.
3. Extract or create reference evidence when technically possible:
   - `reference_source_video.mp4`, `reference_playwm.mp4`, or another local playable video path
   - `reference_contact_sheet.jpg`
   - detail frames from the first 3-5 seconds and representative scene boundaries
   - `reference_shot_table.md`
   - `reference_style_profile.json`
   - `reference_fingerprint.json`
   - `reference_pacing_curve.json`
   - `reference_visual_patterns.json`
   - `reference_frames/metadata.json`
4. Classify the video family before scripting:
   - AI/tool/tutorial/productivity/Codex/plugin/automation -> AI workflow.
   - Renovation/interior/cabinet/room/material/walkthrough/home ad -> renovation workflow.
   - Beauty/portrait/four-choice/fashion woman/TikTok selection -> beauty workflow.
5. Analyze the reference:
   - format, resolution, duration, fps, aspect ratio
   - hook frame and first 3-5 seconds
   - scene count and average shot length
   - page/card/list/image/portrait/space layout family
   - typography scale, text density, line breaks, title hierarchy
   - palette, lighting, filter, grain, blur, contrast, saturation
   - motion recipes, entrance timing, stagger, easing, hold frames
   - caption rhythm and whether the reference has narration
   - music/BGM energy, BPM feel, beat cuts, SFX style
   - safe-zone behavior and platform UI avoidance
   - why the reference feels good
   - what must not be copied
6. Produce a making plan before rendering:
   - owning style and reason
   - independent topic/angle/copy plan
   - original asset plan
   - visual design prompt language
   - motion recipe plan
   - audio plan
   - QA plan
   - originality and similarity-risk plan
7. Then make the video from the plan. Do not skip analysis and jump directly to HyperFrames, ImageGen, FFmpeg, or publishing.

## Originality Contract

The final video must have:

- a new topic, example, product angle, room/design story, or beauty concept
- new on-screen text written for the user's video
- independently generated or user-provided legal assets
- independently authored HyperFrames/Remotion/FFmpeg timeline
- no original reference frames or watermarks
- no copied subtitle lines
- no copied creator/person identity
- no copied room/person/product evidence
- no copied full sequence structure when it creates high similarity

Allowed to learn:

- pacing
- composition pattern
- typography hierarchy
- color/filter mood
- scene density
- motion vocabulary
- cut rhythm
- caption timing
- music mood/BPM
- hook logic
- CTA placement

## Text Accuracy Rule

All final on-screen text must come from the approved copy package, storyboard, title card plan, or generated card text plan. The rendered video must be checked with `render_text_manifest.json`, OCR, manual proofread, or an equivalent text audit.

Gate: final on-screen text deviation from the approved text must be <= 10% by character-level edit distance for each major text block. Minor punctuation, spacing, and line-break differences are acceptable when meaning and readability are preserved. Wrong Chinese characters, hallucinated letters, garbled AI image text, or missing key words count as deviation.

If the reference contains text, do not copy it unless it is a generic product/tool name, public brand name, or user-approved quote. The 10% rule compares final text to our approved original text, not to the reference's original subtitles.

Avoid baking text into generated images unless the image is a finished poster and the text can be proofread. Prefer HTML/CSS/HyperFrames text layers for all readable Chinese.

## Audio Rule

- If the reference has no narration, default to no narration unless the user's topic requires voice.
- If the reference has narration, learn the speaking density and pause rhythm, but write and generate a new voiceover.
- If the reference uses only music, make a music-led edit.
- For user-provided Douyin reference videos intended for Douyin publishing, use or extract the same reference music, or use the same Douyin music-page track when technically possible, and record it as `user_authorized_douyin_reference_music`.
- If the same reference music cannot be extracted or cannot be used technically, stop with a blocker and ask for the music file, platform same-music selection, or explicit approval to proceed without BGM; do not silently match the same music feeling with generated, stock, or local substitute audio.
- For non-Douyin or cross-platform publishing, use the same music only when rights/authorization are clear or user provides that exact track for use.
- Record selected music source, authorization boundary, duration, local path, hash, and whether the audio came from the reference video file or Douyin music page in production notes or metadata.

## Filter And Visual Style Rule

Learn the reference's filter family, not its actual pixels:

- brightness level
- contrast curve
- saturation
- black point
- highlight softness
- blur/glow amount
- grain/noise level
- background separation
- skin/space/material treatment

Create a new style profile and implement it with CSS, generated image prompts, color grading, or FFmpeg filters. Do not reuse the reference video as a background, overlay, LUT source, or direct visual asset unless the user owns it and explicitly asks for reuse.

## Motion Mimic Rule

Motion can imitate the reference's language but must be recreated:

- copy the rhythm category, not the exact frame path
- recreate easing, stagger, card reveal, mask reveal, beat cuts, list build, focus pull, parallax, swipe, or dissolve with new assets
- keep readable hold frames after each reveal
- do not use one repeated fade/slide if the reference's strength is progressive structured movement
- do not hide weak content with shaking, random drift, aggressive zoom, or generic transitions

Every motion recipe must name:

- information purpose
- actor
- path
- timing
- easing
- hold duration
- audio/SFX relationship
- safe-zone and readability risk

## Style Adapters

### AI / Tool / Codex Videos

Default AI knowledge videos remain 16:9 proof-first when the video depends on readable documents, code, browser screenshots, terminal output, or workflow proof.

Exception: when the user provides a vertical reference and asks to match that style, and the content is a lightweight guide/list/card/poster explainer rather than proof-heavy screen teaching, the AI workflow may use a 9:16 `1080x1920` reference-led information-poster mode. It must still keep original copy, source/evidence notes when factual claims are made, safe zones, text accuracy <= 10%, and no copied reference frames.

Good use cases: `10 tools`, `10 skills`, `3 steps`, `5 mistakes`, `before/after prompt checklist`, `AI workflow cheat sheet`.

#### Codex Operation Micro Tutorial Adapter

When the reference is a short Codex/AI tutorial built around cursor clicks, folder/file reveals, screenshot cards, dense narration, and bottom captions, load `references/codex_operation_micro_tutorial_style.md` before making the production plan.

Apply this adapter only to the motion grammar, not the reference skin. The final video should keep the user's selected visual system, usually the enterprise titanium AI control console for current AI videos, while borrowing the operational rhythm:

- result-first hook in the first 3-5 seconds
- one meaningful operation every 1-2 seconds
- `CursorTraceClick` for visible action
- `FileMemoryReveal` for rules, memory, AGENTS.md, checklist, or prompt files
- `ProofCardSnap` for screenshots, editor states, terminal output, or source cards
- subtle click, panel pop, whoosh, and lock SFX below narration

Do not copy the reference's original subtitles, file graphics, Codex icon path, screenshots, voice, creator identity, watermark, or full shot sequence. Do not turn all future AI videos into the same black-blue template; the adapter is for operation feel and pacing only.

### Renovation / Full-House Custom Videos

Learn camera pacing, shot order, music rhythm, color grade, spatial reveal, material close-ups, subtitle placement, and transition style. Do not copy the original room photos, floor plans, designer identity, project name, client details, or exact visual sequence.

Truthfulness levels still apply. A reference with a continuous walkthrough does not allow us to claim L3/L4 unless the user provides a valid continuous source video or a validated professional render. Without that, create an original L1/L2-style video and name it honestly.

### Beauty Portrait Videos

Learn opening rhythm, portrait entrance style, badge position, music/beat pattern, filter mood, and choice-card structure. Do not copy the original person's identity, pose sequence, face, clothing set, subtitles, or creator style exactly.

The beauty skill's safety rules still apply: Chinese adult women age 25+, tasteful fully clothed commercial fashion direction, no minors, no celebrity likeness, no explicit or vulgar content, and required safe-zone review.

## Deliverables

Reference-driven production should save:

- `reference_analysis.json`
- local playable reference video path or a recorded blocker explaining why it could not be obtained
- `reference_shot_table.md`
- `reference_style_profile.json`
- `reference_originality_plan.md`
- `reference_driven_production_plan.md`
- `reference_contact_sheet.jpg` when available
- first 3-5 second detail frames and representative scene-boundary frames when a video body is available
- final contact sheet and detail frames
- `render_text_manifest.json` or OCR/text audit
- QA report proving no copied original media and text deviation <= 10%

## Stop Conditions

Stop or redesign before rendering if:

- the user asks to reuse original frames, watermark, creator identity, or non-music copyrighted material without ownership/authorization
- the plan depends on copying the reference's exact wording or full sequence
- the user gave a video reference but the playable video body cannot be downloaded, opened, or otherwise inspected, and the user has not approved a screenshot-only or no-video-reference fallback
- text accuracy cannot be checked
- generated images contain unreadable or hallucinated text
- the reference route conflicts with safety, truthfulness, publishing, or domain rules
- similarity risk is high after the originality plan
