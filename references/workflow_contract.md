# Workflow Contract

This is the hard production contract for V3. Do not treat it as guidance. It defines what may happen next.

## Artifact Gates

0. Decide input mode first. Reference provided -> Reference Mode. No reference -> Self-Research Mode with current AI-topic/source research.
1. `topic_candidates.json` does not exist -> do not write full copy.
2. `selected_topic.json` does not exist -> do not create copy package.
3. `copy_package.md` and `copy_package.json` do not exist -> do not create storyboard.
4. `script_score.json` is missing or not strong enough -> do not create storyboard.
5. `semantic_review.json` is missing or not `passed` -> do not create storyboard.
6. `compliance_report.json` is missing or not `passed` -> do not generate images, TTS, HyperFrames scenes, or video.
7. `reference_analysis.json` is required when the user provides a reference video/link/share text.
8. `storyboard.json` does not exist -> do not generate TTS or assets.
9. `storyboard_validation.json` is missing or not `passed` -> do not generate TTS or assets. Storyboard validation must include phone-safe margins and normal TTS speed metadata.
10. `asset_manifest.json` does not exist -> do not build HyperFrames.
11. `asset_validation.json` is missing or not `passed` -> do not build HyperFrames.
12. `storyboard.audio_locked.json` does not exist -> do not render HyperFrames.
13. `metadata.json` does not exist or has accelerated `tts_speed` -> do not run final QA.
14. `draft.mp4` is missing or empty -> do not run final QA.
15. `video_technical_qa.json` is missing or not `passed` -> do not create `final/final.mp4`.
16. `frame_review_report.json` is missing -> do not create `final/final.mp4`.
17. `visual_review.json` is missing or not `passed` -> do not create `final/final.mp4`.
18. `qa_report.json` is missing or not `passed` -> do not create `final/final.mp4`, do not publish, and do not present the video as final.
19. Only `scripts/promote_final.py` may copy QA-passed draft artifacts into `final/`.

## Phone-Safe Canvas And Voice Speed

- In 1080x1920 vertical videos, critical content must stay inside top >= 240px, bottom >= 360px, left >= 72px, and right >= 180px.
- Generated images must include this top/bottom breathing room before text is added; do not rely on later overlays to hide cropped content.
- Default narration speed is normal `tts_speed: 1.0`; allowed range is 0.95-1.03.
- If a line is too long, split the scene or shorten the copy. Do not use accelerated TTS to force timing.

## Ten-Step Flow

0. Input Mode Routing -> reference analysis when provided, or current AI hot-topic research when no reference is provided
1. Topic Research -> `topic_candidates.json`
2. Topic Decision -> `selected_topic.json`
3. Copy Package -> `copy_package.md`, `copy_package.json`, `script_score.json`
4. Semantic Review -> `semantic_review.json`
5. Compliance Check -> `compliance_report.json`
6. Reference Analysis -> `reference_analysis.json` when applicable
7. Storyboard -> `storyboard.json`, `storyboard_validation.json`
8. Assets -> `asset_manifest.json`
9. Asset Validation -> `asset_validation.json`
10. TTS + Duration Lock -> `storyboard.audio_locked.json`
11. HyperFrames Production -> `draft.mp4`, `metadata.json`
12. Technical QA + Frame Review -> `video_technical_qa.json`, `frame_review_report.json`
13. Visual Review -> `visual_review.json`
14. QA Gate -> `qa_report.json`
15. Promote Final -> `final/final.mp4` only if QA passed

## Output Layout

```text
outputs/<date-topic>/
  final/
    final.mp4
    cover.png
    publish_copy.txt
    metadata.json
  internal/
    topic_candidates.json
    selected_topic.json
    copy_package.md
    copy_package.json
    script_score.json
    semantic_review.json
    compliance_report.json
    reference_analysis.json
    storyboard.json
    storyboard_validation.json
    storyboard.audio_locked.json
    asset_manifest.json
    asset_validation.json
    draft.mp4
    cover.png
    publish_copy.txt
    video_technical_qa.json
    frame_review_report.json
    visual_review.json
    qa_report.json
    production_notes.md
  assets/
    screenshots/
    generated/
    audio/
    subtitles/
    hyperframes/
```

## Auto-Publish

`allow_auto_publish: false`

Auto-publishing stays off until all conditions are true:

- 5 consecutive videos have `qa_report.status = passed`.
- 5 consecutive videos have no compliance warnings.
- 5 consecutive videos have no audio/visual sync issue.
- 5 consecutive videos are not single-image narration.
- At least 3 videos have clear save-value structure.
- The user explicitly authorizes publishing for the current video.
