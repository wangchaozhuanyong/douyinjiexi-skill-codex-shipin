# Scheme 1: Skill Recommendation, No Voice

Canonical label: `方案1: Skill 推荐无人声`

Use this when the AI video is a short vertical recommendation list for Codex Skills, plugins, AI tools, or workflow modules, especially when the reference video is music-led and has no narration.

## What Went Wrong In The First Attempt

The first draft failed because the reference was analyzed too much as a visual style and not enough as a content job.

- Reference content job: recommend/install/understand `10 个 Skill`
- Wrong first draft content job: generic `Codex 10 个用法`
- Error type: content-task drift
- Root cause: the row schema was not locked before rendering; style was copied as a poster/list, but the semantic object changed from `Skill recommendation` to `general workflow actions`
- Prevention: before any render, write a one-line `content_job_lock` and a row schema. For Scheme 1, each row must be `Skill/tool name + concrete usage note`.

## Correct Content Contract

Required headline pattern:

- `Codex 值得先装的 10 个 Skill`
- `新手值得先装的 8 个 AI 工具`
- `这 5 个插件先学会`

Required row pattern:

```text
number pill | icon tile | Skill/tool name | divider | Chinese usage note
```

Good row note examples:

- `把想法变成可评审的产品界面。`
- `自动访问网页、采集内容，整理资料并截图。`
- `把经验封装成 Skill，让 Codex 按常用流程工作。`

Avoid:

- generic slogans such as `提高效率`
- broad action rows such as `读项目 / 改代码 / 跑检查` unless the reference is explicitly about use cases, not Skill recommendation
- rows with only names and no viewer-use reason

## Visual Description Words Used

Use these words as production language, not as vague taste adjectives:

- `vertical AI information poster`
- `clean lavender/white guide surface`
- `large left-aligned Skill headline`
- `numbered recommendation rows`
- `colored number pills`
- `soft icon tiles`
- `Skill name column`
- `thin vertical divider`
- `right-column Chinese usage note`
- `rounded white row cards`
- `soft shadow`
- `subtle background flow`
- `shimmer sweep`
- `readable hold`
- `music-led edit`
- `no narration`

## Motion Description Words Used

- `title lift`
- `row-by-row slide/fade`
- `staggered easing`
- `ease-out reveal`
- `shimmer reveal`
- `subtle row emphasis`
- `no text distortion`
- `no shake`
- `no random drift`
- `no hard page cuts`
- `continuous music bed`

## Negative Prompt / Avoid Rules

- Do not reuse original reference frames, watermark, creator identity, exact row wording, or original icon assets.
- Do not change the content category from Skill recommendation to generic Codex tips.
- Do not add narration if the reference is no-voice and the topic can be understood visually.
- Do not bake unreadable Chinese into AI-generated images; use controlled text layers.
- Do not deliver without `render_text_manifest.json`, contact sheet, technical QA, and Douyin text compliance.

## Tools Used In The Successful Run

- `scripts/analyze_reference.py`: extracted reference metadata and reference artifacts.
- `scripts/render_vertical_skill_guide.py`: deterministic local PIL renderer for text-safe vertical poster frames.
- Pillow/PIL: drew background, title, row cards, icons, and editable Chinese text.
- FFmpeg: encoded H.264, extracted user-provided Douyin reference music, muxed the final candidate, and generated contact sheets.
- ffprobe: verified resolution, fps, duration, bitrate, and audio/video gap.
- `scripts/video_technical_qa.py`: checked 1080x1920, 30fps, audio stream, black/white/freeze events.
- `scripts/frame_review.py`: generated review contact sheets.
- `scripts/check_public_copy.py`: checked all on-screen text and publish text against local Douyin risk rules and the learned term bank.

## Required Artifacts

For every Scheme 1 output, save:

- `internal/reference_analysis.json`
- `internal/reference_driven_production_plan.md`
- `internal/reference_originality_plan.md`
- `internal/copy_package.json`
- `internal/storyboard.json`
- `internal/render_text_manifest.json`
- `internal/text_accuracy_report.json`
- `internal/video_technical_qa.json`
- `internal/frame_review_report.json`
- `internal/on_screen_and_publish_text_compliance_report.json`
- `internal/forbidden_terms_update_report.json`
- `delivery/final_candidate.mp4` or `final/final.mp4` only after all publish gates pass

## Production Steps

1. Classify the reference as `方案1: Skill 推荐无人声`.
2. Lock `content_job_lock = recommend Skills/tools and explain what each does`.
3. Create the row list before rendering. Every row needs a Skill/tool name and concrete usage note.
4. Write `reference_originality_plan.md`: learn rhythm and row structure, do not copy original frames/wording/icons.
5. Render with HyperFrames if available; if not, use the deterministic poster renderer only for this narrow format.
6. Extract or match reference music under the user's Douyin-to-Douyin reference music rule.
7. Generate `render_text_manifest.json`; compare final text to the approved copy, target 0% deviation.
8. Run technical QA, contact-sheet review, full on-screen text compliance, publish text compliance, and forbidden-term update.
9. Do not publish until exact title/caption/topics pass Qingdou together, except for the documented user-approved official/platform topic override in `douyin_compliance_rules.md`.

## Reuse Decision

This is now one of the main AI video production directions. Use it as a primary option when:

- the reference is a short vertical no-voice list/poster
- the topic is Codex Skills, plugins, AI tools, or creator workflow modules
- the goal is quick save/share value rather than proof-heavy teaching

Do not use it when:

- the viewer must read docs, code, terminal output, or UI proof
- the topic needs a narrated explanation
- the reference is a horizontal tutorial, news explainer, or operation proof video
