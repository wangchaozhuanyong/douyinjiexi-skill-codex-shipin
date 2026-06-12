# Douyin HyperFrames Remake Skill

这是一个 Codex skill，用于把用户提供的抖音链接、分享文本或本地参考视频分析成原创短视频制作流程，并配合图片生成、真实证据素材、稳定 TTS 和 HyperFrames 输出可发布的视频素材。

## 适用场景

- 用户发送抖音链接，希望参考其主题、节奏和信息结构重新制作原创短视频。
- 需要把参考视频拆成分镜、文案、配音、图片素材、字幕和成片交付流程。
- 需要制作 AI/Codex/Skill/Agent 教程类视频，要求真实 UI、真实输出证明和高级产品演示感。
- 需要避免低原创、搬运、画面抖动、字幕不同步、TTS 不自然等问题。

## 安装方式

把本仓库克隆或复制到 Codex skills 目录，例如：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/wangchaozhuanyong/douyinjiexi-skill-codex-shipin.git ~/.codex/skills/douyin-hyperframes-remake
```

重启 Codex 后即可使用。

## 使用方式

在 Codex 中发送类似：

```text
请使用 $douyin-hyperframes-remake 分析这个抖音链接，并用 HyperFrames 重做一个原创短视频：<链接或分享文本>
```

## 当前核心规则

- 默认参考原视频的主题、节奏、场景数量、信息层级和大致时长。
- 不使用原视频画面、原字幕、原声音、原音乐和完整原文案。
- 长视频默认按接近原时长制作，不偷工减料压缩成几十秒。
- 不允许最终视频只是一张图配音。
- 字幕、画面和配音必须同步。
- 发布级作品必须先创建 `storyboard.json`，记录场景文案、字幕、模板、配音、BGM、媒体路径和真实音频时长。
- 默认中文教程/日更配音使用 Edge TTS `zh-CN-YunyangNeural`，速度 `1.10-1.12x`，一场景一段音频。
- 视频剪辑时长必须由真实音频时长驱动，不用手猜字幕和场景时间。
- 必须选择一个统一模板预设，例如 `proof-tutorial-horizontal`、`daily-ai-vertical`、`blackboard-grid` 或 `product-demo-proof-wall`。
- BGM 默认音量 `0.10-0.15`，必须低于人声，影响听清就降低或取消。
- 发布级作品必须生成 `metadata.json`，记录最终视频路径、时长、大小、场景数、配音、语速、模板、BGM、分辨率和 FPS。
- 重复/日更制作前要检查最近作品的 `metadata.json`、`storyboard.json` 和 `production-notes.md`，复用好的配音、模板、BGM 和渲染参数，但不能复用旧选题和事实 claims。
- 静态图禁止明显抖动，优先用切换、淡入淡出、分层 reveal 和轻量产品演示动效。
- 最终视频里不能显示 `重创重做版本`、`重做版本`、`remake`、`reference remake` 等内部制作说明。
- 最终交付文件夹默认只保留成品 MP4，并直接给用户可点击文件夹链接。

## 文件结构

```text
SKILL.md
agents/openai.yaml
references/douyin_rules.md
references/hyperframes_delivery.md
references/codex_skill_tutorial_video.md
references/pixelle_pipeline_lessons.md
scripts/analyze_reference.py
```

## 依赖说明

该 skill 默认复用用户本地的抖音解析项目：

```text
/Users/wangchao/Desktop/抖音解析
```

如果项目移动，需要在运行 `scripts/analyze_reference.py` 时通过 `--project-dir` 指定新的路径。

## 合规提醒

本 skill 的目标是制作原创短视频，不是帮助照搬或隐藏搬运。可以参考结构和节奏，但最终内容应使用新的视觉、新文案、新配音和不同的表达角度。平台审核结果无法保证。
