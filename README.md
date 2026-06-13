# Douyin AI Video Director Skill

`douyin-hyperframes-remake` V2 是一个 Codex skill，用于制作原创、合规、高质量的 AI 圈知识类抖音短视频。

它不是简单“重做参考视频”的提示词集合，而是一条可执行、可验收、可复盘的生产流水线：选题、定题、文案、合规、参考分析、分镜、素材、TTS、HyperFrames、QA、最终交付。

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

兼容说明：旧版 Codex 环境可能仍使用 `~/.codex/skills`，但 V2 README 以当前 `$HOME/.agents/skills` 和 `.agents/skills` 为主。

安装后重启 Codex，在 CLI/IDE 中运行 `/skills`，确认能看到 `douyin-hyperframes-remake`。也可以显式输入 `$douyin-hyperframes-remake` 调用。

## 标准流程

V2 必须按下面顺序执行：

```text
topic_candidates
-> selected_topic
-> copy_package
-> compliance_report
-> reference_analysis
-> storyboard
-> asset_manifest
-> storyboard.audio_locked
-> draft.mp4 + metadata
-> qa_report
-> final.mp4
```

硬规则：

- 没有 `topic_candidates.json`，不准写完整文案。
- 没有 `selected_topic.json`，不准进入文案包。
- 没有 `copy_package.md` 和 `copy_package.json`，不准做分镜。
- `compliance_report.json` 没 passed，不准生成图片、TTS、视频。
- `storyboard.audio_locked.json` 不存在，不准渲染 HyperFrames。
- `qa_report.json` 没 passed，不准生成或交付 `final/final.mp4`。

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

用户只看 `final/`。`internal/` 用于复盘和调试。

## 常用命令

```bash
python scripts/doctor.py
python -m py_compile scripts/*.py
pytest -q
```

If the `pytest` executable is not on PATH but the Python module is installed, use:

```bash
python3 -m pytest -q
```

选题评分：

```bash
python scripts/score_topic.py --input outputs/demo/internal/topic_candidates.json
```

文案合规：

```bash
python scripts/check_public_copy.py \
  --copy outputs/demo/internal/copy_package.md \
  --out outputs/demo/internal/compliance_report.json
```

参考分析：

```bash
python scripts/analyze_reference.py \
  --input "<抖音链接/分享文本/本地视频路径>" \
  --out outputs/demo/internal/reference_analysis.json
```

分镜校验：

```bash
python scripts/validate_storyboard.py \
  --storyboard outputs/demo/internal/storyboard.json \
  --out outputs/demo/internal/storyboard_validation.json
```

最终 QA：

```bash
python scripts/qa_gate.py \
  --project outputs/demo \
  --out outputs/demo/internal/qa_report.json
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
请使用 $douyin-hyperframes-remake 制作一条原创、合规、高质量的 AI 圈知识类抖音视频。必须按 topic_candidates -> selected_topic -> copy_package -> compliance_report -> storyboard -> assets -> TTS -> HyperFrames -> qa_report -> final.mp4 的顺序执行。QA 不通过不要交付 final.mp4。
```

## 合规说明

V2 默认关闭自动发布：`allow_auto_publish: false`。

只有用户明确授权，并且当前作品已经通过 `qa_report.json`，才可以进入发布动作。平台审核结果无法保证。该 skill 会尽量规避绝对化表达、保证效果、虚假权威、诱导互动、站外引流、二维码、联系方式、低质内容和搬运风险。

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
