# Douyin HyperFrames Remake Skill

这是一个 Codex skill，用于把用户提供的抖音链接或分享文本分析成原创短视频制作流程，并配合图片生成、TTS 和 HyperFrames 输出可发布的视频素材。

## 适用场景

- 用户发送抖音链接，希望参考其主题、节奏和信息结构重新制作原创短视频。
- 需要把参考视频拆成分镜、文案、配音、图片素材、字幕和成片交付流程。
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
- 静态图禁止明显抖动，优先用切换、淡入淡出和轻量动效。
- 默认优先使用 `edge-tts` 等更自然的中文 TTS，默认语速约 `1.2x`。
- 最终视频里不能显示 `重创重做版本`、`重做版本`、`remake`、`reference remake` 等内部制作说明。
- 最终交付文件夹默认只保留成品 MP4，并直接给用户可点击文件夹链接。

## 文件结构

```text
SKILL.md
agents/openai.yaml
references/douyin_rules.md
references/hyperframes_delivery.md
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
