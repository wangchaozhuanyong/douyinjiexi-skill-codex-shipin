# Workflow Contract

This is the hard production contract for V2. Do not treat it as guidance. It defines what may happen next.

## Artifact Gates

1. `topic_candidates.json` does not exist -> do not write full copy.
2. `selected_topic.json` does not exist -> do not create copy package.
3. `copy_package.md` and `copy_package.json` do not exist -> do not create storyboard.
4. `compliance_report.json` is missing or not `passed` -> do not generate images, TTS, HyperFrames scenes, or video.
5. `reference_analysis.json` is required when the user provides a reference video/link/share text.
6. `storyboard.json` does not exist -> do not generate TTS or assets.
7. `asset_manifest.json` does not exist -> do not build HyperFrames.
8. `storyboard.audio_locked.json` does not exist -> do not render HyperFrames.
9. `metadata.json` does not exist -> do not run final QA.
10. `qa_report.json` is missing or not `passed` -> do not create `final/final.mp4`, do not publish, and do not present the video as final.

## Ten-Step Flow

1. Topic Research -> `topic_candidates.json`
2. Topic Decision -> `selected_topic.json`
3. Copy Package -> `copy_package.md`, `copy_package.json`
4. Compliance Check -> `compliance_report.json`
5. Reference Analysis -> `reference_analysis.json` when applicable
6. Storyboard -> `storyboard.json`
7. Assets -> `asset_manifest.json`
8. TTS + Duration Lock -> `storyboard.audio_locked.json`
9. HyperFrames Production -> `draft.mp4`, `metadata.json`
10. QA Gate -> `qa_report.json`, then `final/final.mp4` only if passed

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
    compliance_report.json
    reference_analysis.json
    storyboard.json
    storyboard.audio_locked.json
    asset_manifest.json
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
