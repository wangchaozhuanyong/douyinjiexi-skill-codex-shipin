# Topic Selection Rules

The first quality gate is topic quality. Do not write copy before topic research.

## Mode Requirement

Use the right topic source for the user input:

- If the user provides a reference video/link/share text/local video, topic research starts from that reference. Extract the reference's topic angle, hook, structure, audience pain, visual rhythm, and comment/save trigger before proposing an original version.
- If the user only asks to "use the skill to make a video" and gives no reference, topic research must start from current AI-circle hot topics and high-quality source material. Do not default to a stale evergreen explanation or a Codex-only topic.

For self-researched videos, collect current material before scoring candidates:

- Search across the broad AI industry, not only Codex: OpenAI, ChatGPT, Anthropic, Claude, Google Gemini/Veo, Meta AI, xAI/Grok, AI agents, AI video generation, coding agents, enterprise AI, AI search, AI hardware, AI safety/regulation, and creator tools.
- Prefer sources with visible dates and clear evidence: official posts, docs, release notes, reputable tech/business media, demo pages, real product screens, terminal/code output, or public benchmark pages.
- Every candidate must name why the topic is timely, what source supports each important claim, and what visual evidence can appear on screen.
- If no current topic is strong enough, research again instead of falling back to a generic lesson.

## Beginner Task Source

For beginner-facing AI videos, research must start from tasks before tools. Build candidates from common tasks such as writing short-video copy, making covers, editing scripts, summarizing meetings, writing daily or weekly reports, building PPT outlines, analyzing tables, writing Douyin/Xiaohongshu titles, drafting customer-service replies, polishing resumes, summarizing contracts, or collecting industry materials.

Then match the task to an AI tool, update, or workflow. The topic direction is:

```text
beginner task -> real pain -> AI action -> visible result -> three-step tutorial
```

Reject candidates that start and end as `AI tool -> feature -> trend` without a concrete beginner action.

## Candidate Requirements

Produce at least 5 candidates in `topic_candidates.json`. Each candidate must include:

- `topic_id`
- `title_direction`
- `core_angle`
- `content_format`
- `format_reason`
- `target_viewer`
- `beginner_task`
- `visible_result`
- `first_action`
- `time_saving_claim`
- `viewer_pain`
- `why_now`
- `curiosity_gap`
- `save_reason`
- `comment_trigger`
- `visual_potential`
- `proof_assets_needed`
- `main_claims`
- `sources`
- `risk_flags`
- `scores`

AI news candidates must include source titles, URLs or local notes, visible dates when available, and which claim each source supports.

AI tool tutorial candidates must name what real UI, real recording, terminal output, product result, or official documentation can appear on screen.

## Topic Title Standard

The final topic must let viewers immediately know what the video is about before they hear the tutorial angle. Do not use an abstract method headline as the topic.

`title_direction` must follow this shape:

```text
object/source + latest event/feature/news/official source + practical takeaway
```

Where `object/source` is a concrete software, website, company, model, product feature, official release, or news source, such as ChatGPT, Codex, Gemini, Google AI, OpenAI release notes, a named AI website, or a named AI coding/video tool.

Where `latest event/feature/news/official source` names what happened or what concrete source is being explained, such as released, updated, launched, added, changed, opened, removed, tested, compared, became available, was reported, official documentation, a release note, a product feature page, or a named tool page.

Good examples:

- `ChatGPT 新增应用调用确认：用 Codex 前先写三层边界清单`
- `Gemini Pixel Drop 加入 AI 视频编辑：普通人先学这 3 个提示词`
- `Codex 0.141.0 更新远程执行：新手怎么区分可看、可改、要确认`
- `最近 AI 一则大新闻：OpenAI 某功能更新后，工作流要这样改`

Bad examples:

- `用 ChatGPT 和 Codex 前先写边界清单`
- `AI 工具提效技巧`
- `新手必须知道的 AI 工作流`
- `三步让 Agent 更安全`

If the topic title does not name the software, website, product, company, model, feature, release, official source, or news event, reject it before copywriting.

## Scoring

Use `scripts/score_topic.py`.

When `references/learning_bank.md` has prior post-publish lessons, run scoring with:

```bash
python scripts/score_topic.py --input topic_candidates.json --learning-bank references/learning_bank.md
```

The output must keep `learning_bank_adjustment` so the choice is auditable.

Beginner-weighted score:

```text
total_score =
beginner_usefulness_score * 0.30 +
visible_result_score * 0.20 +
time_saving_score * 0.15 +
pain_score * 0.15 +
novelty_score * 0.10 +
visual_score * 0.07 +
compliance_safety_score * 0.03
```

Legacy `save_score` and `comment_score` may be kept for auditing, but they must not outrank beginner usefulness, visible result, and saved steps.

## Gates

- Total score must be at least 8.0.
- If no topic scores at least 8.0, research again.
- Do not choose generic topics such as `AI 工具推荐`, `AI 很厉害`, or `这个工具很好用`.
- Do not choose method-only topic titles. The selected `title_direction` must name the concrete object/source and the event/feature/news/official source being discussed.
- Choose topics with a clear beginner task, visible result, saved step, pain, fresh angle, visual proof, and low compliance risk.
- `content_format` must be one of the formats in `references/content_formats.md`.
