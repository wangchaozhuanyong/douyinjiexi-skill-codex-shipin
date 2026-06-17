# Douyin AI Video Director Skill

`douyin-hyperframes-remake` V3 是一个 Codex skill，用于制作原创、合规、高质量的 AI 圈知识类抖音短视频。

它不是简单“重做参考视频”的提示词集合，而是一条可执行、可验收、可复盘的生产流水线：选题、定题、文案、合规、参考分析、分镜、素材、TTS、HyperFrames、QA、最终交付。

## 多插件导演模式

这个 skill 不是只调用 HyperFrames。HyperFrames 是最终成片引擎，负责时间线、字幕、动效、inspect、render 和交付；前面的研究、证据、素材、官方查证和可视化片段应该按任务调用多个插件/运行时。

默认分工：

- `Browser`：抓真实网页、产品 UI、官方文档、预览截图和画面检查。
- `GitHub`：查仓库、issue、PR、源码、release、CI 或开源证据。
- `Hugging Face`：查模型、数据集、论文、Spaces 和开源生态证据。
- `OpenAI Developers`：核对 OpenAI 官方文档、Agents/App SDK/API 相关说法。
- `ImageGen`：做背景板、封面、辅助视觉，不能伪造产品证据。
- `Remotion / Manim`：在确实需要组件动画、数据图表、公式/流程动画时生成片段。
- `HyperFrames`：最终包装、字幕、动效、时间线、渲染和交付。
- `FFmpeg / ffprobe`：音视频探测、抽帧、转码、remux、码率和音频时长检查。
- `HeyGen`：只在你明确授权数字人、头像、口型或账号/积分路径时使用。

AI 工具、Codex、插件、开源项目、模型/数据集、API 或官方文档类视频，必须先写 `storyboard.codex_plugin_plan`，再进入 HyperFrames。`provider_usage_audit.json` 会检查这条视频是不是只靠 HyperFrames 糊过去。

## 适合什么内容

- AI 新闻和 AI 工具解读。
- ChatGPT、Codex、Agent、自动化、AI 视频工具教程。
- 有参考视频但只学习结构、节奏、信息密度的原创短视频。
- 需要真实 UI、真实截图、真实结果证明的知识型视频。
- 需要小白能听懂、有收藏价值、合规安全的中文口播视频。

## 不适合什么内容

- 搬运原视频画面、字幕、声音、音乐或完整文案。
- 直接做“必火”“保证涨粉”“全网最强”这类违规承诺视频。
- 单图配音、低质图片轮播、无声、卡帧、音画不同步的视频。
- 冒充官方截图、用户评价、数据证明或权威认证的内容。

## 安装方式

全局用户级安装：

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/wangchaozhuanyong/douyinjiexi-skill-codex-shipin.git \
  ~/.agents/skills/douyin-hyperframes-remake
```

项目级安装：

```bash
mkdir -p .agents/skills
git clone https://github.com/wangchaozhuanyong/douyinjiexi-skill-codex-shipin.git \
  .agents/skills/douyin-hyperframes-remake
```

兼容说明：旧版 Codex 环境可能仍使用 `~/.codex/skills`，但 V3 README 以当前 `$HOME/.agents/skills` 和 `.agents/skills` 为主。

安装后重启 Codex，在 CLI/IDE 中运行 `/skills`，确认能看到 `douyin-hyperframes-remake`。也可以显式输入 `$douyin-hyperframes-remake` 调用。

## 标准流程

V3 必须按下面顺序执行：

```text
topic_candidates
-> selected_topic
-> copy_package
-> script_score + semantic_review
-> compliance_report
-> codex_plugin_plan / production_stack when tool or plugin workflow is involved
-> reference_analysis
-> background_prompt_pack
-> storyboard
-> asset_manifest
-> asset_validation
-> storyboard.audio_locked
-> draft.mp4 + metadata
-> audio_continuity_report
-> video_technical_qa + frame_review
-> visual_review
-> qa_report
-> production_postmortem
-> provider_usage_audit
-> promote_final
-> final.mp4
```

硬规则：

- 没有 `topic_candidates.json`，不准写完整文案。
- 没有 `selected_topic.json`，不准进入文案包。
- 没有 `copy_package.md` 和 `copy_package.json`，不准做分镜。
- `script_score.json` 或 `semantic_review.json` 没 passed，不准进入合规后生产。
- `compliance_report.json` 没 passed，不准生成图片、TTS、视频。
- `asset_validation.json` 没 passed，不准进入最终 QA。
- `storyboard.audio_locked.json` 不存在，不准渲染 HyperFrames。
- `audio_continuity_report.json` 不存在或没 passed，不准运行最终 QA、不准交付 `final/final.mp4`。
- `video_technical_qa.json`、`frame_review_report.json` 和 `visual_review.json` 不存在，不准运行最终 QA。
- `qa_report.json` 没 passed，不准生成或交付 `final/final.mp4`。
- `provider_usage_audit.json` 没 passed，不准生成或交付 `final/final.mp4`。
- `production_postmortem.json` 用于复盘和学习，不允许覆盖失败 QA，也不允许自动改硬规则。
- `qa_gate.py` 检查的是 `internal/draft.mp4`，只写 QA 报告。
- `promote_final.py` 只有在 QA 和 provider usage audit 都 passed 后才复制到 `final/final.mp4`。
- AI 知识/AI 工具/Codex/Agent/Skill 教程默认且强制使用 16:9：1920x1080。
- AI 类视频必须先写 `background_prompt_pack.md`，用描述语言设计并生成无文字 `1920x1080` 背景板，再进入分镜、资产、TTS、HyperFrames 和渲染。
- 非 AI 9:16 视频不能把内容顶到画面上下边缘：1080x1920 默认关键内容区必须保留 top >= 240px、bottom >= 360px、left >= 72px、right >= 180px。
- 口播默认正常语速 `tts_speed: 1.0`，允许范围 0.95-1.03；不准用 1.1x、1.12x、1.2x 解决时长问题。

## 输出目录

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
    background_prompt_pack.md
    storyboard.json
    storyboard.audio_locked.json
    audio_continuity_report.json
    asset_manifest.json
    asset_validation.json
    draft.mp4
    cover.png
    publish_copy.txt
    video_technical_qa.json
    frame_review_report.json
    visual_review.json
    qa_report.json
    production_postmortem.json
    provider_usage_audit.json
    provider_usage_audit.md
    production_notes.md
  assets/
    screenshots/
    generated/
    audio/
    subtitles/
    hyperframes/
```

用户只看 `final/`。`internal/` 用于复盘和调试。

## 自主学习机制

这个 skill 的学习不是“自动训练模型”，而是可控的生产复盘闭环：

- 每条视频 QA 后生成 `internal/production_postmortem.json`。
- 复盘记录：有效做法、失败点、拥堵点、下次决策、建议新增规则。
- `references/learning_bank.md` 保存被确认的经验，影响下次选题和分镜判断。
- `references/failed_case_library.md` 保存常见失败模式，例如 PPT 感、假证据、小字看不清、空帧。
- `references/director_decision_patterns.md` 帮助下一条视频先做导演判断，再进入 HyperFrames。
- 复盘里的 `proposed_rule_changes` 只是建议，必须用户确认后才能写成硬规则。

## 常用命令

```bash
python3 scripts/doctor.py
python3 -m py_compile scripts/*.py
python3 -m pytest -q
python3 scripts/check_golden_project.py
```

If the `python` executable is not on PATH, use `python3` as shown above.

选题评分：

```bash
python3 scripts/score_topic.py --input outputs/demo/internal/topic_candidates.json
```

学习库反哺选题：

```bash
python3 scripts/score_topic.py \
  --input outputs/demo/internal/topic_candidates.json \
  --learning-bank references/learning_bank.md

python3 scripts/apply_learning_bank.py \
  --input outputs/demo/internal/topic_candidates.json \
  --bank references/learning_bank.md \
  --out outputs/demo/internal/topic_candidates.learned.json
```

生产复盘：

```bash
python3 scripts/generate_production_postmortem.py \
  --project outputs/demo \
  --out outputs/demo/internal/production_postmortem.json \
  --user-feedback "画面像PPT，操作感不足"

python3 scripts/update_learning_bank.py \
  --review outputs/demo/internal/production_postmortem.json \
  --bank references/learning_bank.md
```

语义审稿：

```bash
python3 scripts/evaluate_copy_semantic.py \
  --copy outputs/demo/internal/copy_package.md \
  --copy-json outputs/demo/internal/copy_package.json \
  --out outputs/demo/internal/semantic_review.json
```

文案合规：

```bash
python3 scripts/check_public_copy.py \
  --copy outputs/demo/internal/copy_package.md \
  --out outputs/demo/internal/compliance_report.json
```

参考分析：

```bash
python3 scripts/extract_reference_frames.py \
  --input reference.mp4 \
  --out outputs/demo/internal/reference_frames \
  --interval 1.0

python3 scripts/analyze_reference.py \
  --input "<抖音链接/分享文本/本地视频路径>" \
  --out outputs/demo/internal/reference_analysis.json
```

本地参考视频会额外输出 `reference_fingerprint.json`、`reference_pacing_curve.json` 和 `reference_visual_patterns.json`。

分镜校验：

```bash
python3 scripts/validate_storyboard.py \
  --storyboard outputs/demo/internal/storyboard.json \
  --out outputs/demo/internal/storyboard_validation.json
```

素材验收：

```bash
python3 scripts/validate_assets.py \
  --manifest outputs/demo/internal/asset_manifest.json \
  --project outputs/demo \
  --out outputs/demo/internal/asset_validation.json
```

连续口播检测：

```bash
python3 scripts/check_audio_continuity.py \
  --video outputs/demo/internal/draft.mp4 \
  --lock outputs/demo/internal/storyboard.audio_locked.json \
  --out outputs/demo/internal/audio_continuity_report.json
```

技术 QA 和审片图：

```bash
python3 scripts/video_technical_qa.py \
  --video outputs/demo/internal/draft.mp4 \
  --metadata outputs/demo/internal/metadata.json \
  --out outputs/demo/internal/video_technical_qa.json

python3 scripts/frame_review.py \
  --video outputs/demo/internal/draft.mp4 \
  --out-dir outputs/demo/internal/frame_review \
  --report outputs/demo/internal/frame_review_report.json

python3 scripts/visual_aesthetic_review.py \
  --storyboard outputs/demo/internal/storyboard.json \
  --frame-review outputs/demo/internal/frame_review_report.json \
  --metadata outputs/demo/internal/metadata.json \
  --out outputs/demo/internal/visual_review.json
```

最终 QA：

```bash
python3 scripts/qa_gate.py \
  --project outputs/demo \
  --out outputs/demo/internal/qa_report.json

python3 scripts/audit_provider_usage.py \
  --project outputs/demo \
  --phase final \
  --out outputs/demo/internal/provider_usage_audit.json \
  --md-out outputs/demo/internal/provider_usage_audit.md

python3 scripts/promote_final.py \
  --project outputs/demo
```

一键检查：

```bash
python3 scripts/run_pipeline.py --project outputs/demo --mode qa-only
python3 scripts/run_pipeline.py --project outputs/demo --mode qa-promote
python3 scripts/run_pipeline.py --mode golden
```

## 常用提示词

只做选题：

```text
请使用 $douyin-hyperframes-remake 只做 AI 圈抖音选题研究。输出 5 个候选话题，按痛点、收藏价值、评论潜力、视觉证据和合规风险评分。不要写完整文案，不要做视频。
```

做文案：

```text
请使用 $douyin-hyperframes-remake 基于 selected_topic.json 写一版高收藏价值的中文抖音口播文案。必须包含前 5 秒钩子、完整口播、字幕、封面文案、发布文案、标签和 claim ledger。写完后运行本地合规检查。
```

根据参考视频重做：

```text
请使用 $douyin-hyperframes-remake 分析这个参考视频，只学习它的节奏、结构和信息层级，不复制原画面、原字幕、原声音和原文案。先输出 reference_analysis.json、selected_topic.json 和 copy_package.md，不要直接生成视频。
```

做完整视频：

```text
请使用 $douyin-hyperframes-remake 制作一条原创、合规、高质量的 AI 圈知识类抖音视频。必须按 topic_candidates -> selected_topic -> copy_package -> semantic_review -> compliance_report -> storyboard -> asset_validation -> TTS -> HyperFrames -> visual_review -> qa_report -> production_postmortem -> provider_usage_audit -> promote_final -> final.mp4 的顺序执行。QA 或 provider usage audit 不通过不要交付 final.mp4。
```

## 合规说明

V3 默认关闭自动发布：`allow_auto_publish: false`。

只有用户明确授权，并且当前作品已经通过 `qa_report.json`，才可以进入发布动作。平台审核结果无法保证。该 skill 会尽量规避绝对化表达、保证效果、虚假权威、诱导互动、站外引流、二维码、联系方式、低质内容和搬运风险。

如果用户已经明确授权发布链中的常规浏览器操作，则青豆检测、抖音创作者中心上传等流程里出现的图形验证码或滑块验证码默认由 agent 自行处理，不再重复询问。只有短信验证码、必须由用户本人完成的实名/手机校验、或用户明确撤回授权时，才必须停下。

## 文件结构

```text
SKILL.md
README.md
agents/openai.yaml
docs/
references/
schemas/
templates/
scripts/
tests/
```
