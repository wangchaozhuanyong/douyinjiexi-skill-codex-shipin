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

Before writing public rows, build `internal/skill_source_manifest.json` and run:

```bash
python3 scripts/check_skill_source_manifest.py --manifest internal/skill_source_manifest.json --scheme-id scheme_1_skill_recommendation_no_voice
```

The manifest must prove the row names, left icons, and public introduction copy are real:

- `skill_name` must come from an actual `SKILL.md` frontmatter name or a documented curated source.
- `display_name` should come from `agents/openai.yaml` when present.
- `icon_source` must point to a real local icon asset when the video renders a left icon; if no icon exists, the row must use a clearly labeled generic symbol and record `icon_strategy=generic_symbol`.
- `source_path_or_url` must be internal evidence only; do not place URLs or link prompts in public text.
- `copy_mode` must be `source_quoted_or_source_paraphrase`.
- `source_description` must match the actual `SKILL.md` frontmatter description or `agents/openai.yaml` `short_description`.
- `public_note` is the only row-introduction field intended for video text. It must be an exact source quote or a conservative Chinese paraphrase.
- `claim_evidence` must include one entry for `public_note` with `claim_text`, `source_field`, exact `source_text`, and `derivation=direct_quote` or `derivation=conservative_paraphrase`.
- Do not require or invent `input`, `purpose`, `output`, or `usage_note`. If any of those legacy fields appear, each field must have its own `claim_evidence`; otherwise the manifest fails.

Required headline pattern:

- `Codex 值得先装的 10 个 Skill`
- `新手值得先装的 8 个 AI 工具`
- `这 5 个插件先学会`

Required row pattern:

```text
number pill | icon tile | Skill/tool name | divider | source-backed public_note
```

Beginner-safe row semantics:

```text
Skill/tool name | exact source description or conservative Chinese paraphrase
```

For 7-10 second vertical videos, compress the source description into one readable Chinese public note. The note must stay inside the source boundary. Do not add a workflow, result, or promise that is not present in the source description.

Acceptable row note examples only when `claim_evidence` records the original `short_description` or `SKILL.md` description:

- `Skill Creator：创建或更新一个 Skill。`
- `Skill Installer：从 curated 列表或其他仓库安装 Skill。`
- `OpenAI Docs：查 OpenAI 文档、Codex 自身说明和模型迁移信息。`
- `Image Gen：生成或编辑网站、游戏等图片素材。`
- `GitHub：查看 PR、Issue、CI 和发布流程。`

Avoid:

- generic slogans such as `提高效率`
- broad action rows such as `读项目 / 改代码 / 跑检查` unless the reference is explicitly about use cases, not Skill recommendation
- rows with only names and no viewer-use reason
- invented names or invented left icons that do not exist in `SKILL.md`, `agents/openai.yaml`, local assets, or documented source scan
- real names/icons with inferred public copy such as invented `输入什么/输出什么/达到什么效果` claims that cannot be traced to `claim_evidence`
- public copy that asks viewers to provide, copy, open, visit, download, scan, message, or claim something through a website, URL, QR code, private message, or contact path
- words and phrases such as `网址`, `链接`, `URL`, `复制链接`, `打开网站`, `打开某站`, `访问官网`, `扫码`, `私信`, `领取`, `下载`, `加群`, `加我`, `联系方式`

Internal evidence may still store source URLs, tool docs, or local proof paths. The ban above applies to on-screen text, subtitles, cover text, title, caption, topics, and prepared comments.

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

## Current Runtime Rule

The original corrected run used a local poster renderer, but that route is now retired because it can drift back into low-grade card/PIL output. Current Scheme 1 videos must be authored as a controlled HyperFrames timeline and pass `scripts/produce_ai_video.py --mode visual-gate` before any promotion.

Required current tools:

- `scripts/analyze_reference.py`: extracts reference metadata and reference artifacts.
- HyperFrames: final timeline, controlled text layers, row motion, music bed, and render.
- FFmpeg/ffprobe: mechanical probing, muxing, frame extraction, and technical QA only.
- `scripts/video_technical_qa.py`, `scripts/frame_review.py`, `scripts/check_public_copy.py`, and `scripts/produce_ai_video.py`: technical, visual, text, and regression gates.

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
3. Create the row list before rendering. Every row needs a Skill/tool name and a source-backed `public_note`; do not render until `claim_evidence` passes.
4. Write `reference_originality_plan.md`: learn rhythm and row structure, do not copy original frames/wording/icons.
5. Render with HyperFrames. Do not fall back to a local PIL/ImageDraw/rawvideo full-frame renderer.
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
