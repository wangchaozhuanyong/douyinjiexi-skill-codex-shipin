# Douyin AI Video Skills

本仓库已经从单体 AI 视频导演 Skill 重构为三个专业内容 Skill 和一个共享生产底座。当前创作原则是“完全自由导演”：每条视频重新决定视觉语言，不再从固定黑底、卡片、银河背景或模块编号中选模板。

## 项目结构

```text
skills/
  douyin-ai-tool-explainer/
  douyin-ai-news-explainer/
  douyin-ai-list-video/
  douyin-video-production-core/
research/
  protocol.md
  sample_registry.json
  rule_candidates.json
  findings.md
scripts/
  sync_skills.py
  audit_legacy_removal.py
tests/
```

三个内容 Skill 分别负责工具实操、AI 新闻和榜单清单。`douyin-video-production-core` 提供参考视频分析、证据绑定、供应商预检、连续旁白、文本合规、音视频技术 QA 和发布保护。

最终时间线统一由 Remotion 管理。HyperFrames 只在单个场景确实适合网页动效时作为可选子渲染器，不能接管成片时间线，也不能决定全片视觉风格。

## AI 视频分类

所有项目一级分类统一为 `AI类视频`：

| 二级分类 | 内部代码 | 对应 Skill |
| --- | --- | --- |
| AI工具实操讲解类 | `ai_tool_explainer` | `douyin-ai-tool-explainer` |
| AI新闻与产品更新解读类 | `ai_news_explainer` | `douyin-ai-news-explainer` |
| AI榜单、推荐与对比类 | `ai_list_video` | `douyin-ai-list-video` |

三级分类根据题材继续细分。项目名统一使用 `<二级分类短名>-<主题短名><两位序号>`，例如 `AI工具实操讲解-自由导演样片01`。完整路由与命名规则见 `skills/douyin-video-production-core/references/video_taxonomy.md`。

## 六产物接口

每个新项目只要求：

```text
source_brief.json
script.json
storyboard.json
asset_manifest.json
qa_report.json
publish_package.json
```

渲染帧、contact sheet、平台检查和临时技术报告可以附加，但不能重新变成创作前必须补齐的复杂门禁链。

## 研究边界

18 个样本已经完成：工具、新闻、榜单各 6 个，每类包含 4 个 `high_visible` 和 2 个 `control_visible`。只有取得本地可播放视频本体、完成 ffprobe、抽帧和人工检查的样本才能标记为 `analyzed`。只有达到三个独立高表现样本加一个普通对照样本的规则，才能进入稳定创作 Skill。

```bash
python3 research/validate_registry.py --allow-incomplete
python3 research/validate_registry.py
```

第二条命令会在 18 个有效样本和表现分组未完成时保持阻塞，避免把占位记录或用户口述流量当作已验证研究。

## 自由导演首版样片

首版先完成工具实操类样片：

- 工程：`samples/free-director-tool`
- 成片：`samples/free-director-tool/render/final.mp4`
- 封面：`samples/free-director-tool/render/cover.png`
- 完整画面表：`samples/free-director-tool/review/contact_sheet.jpg`
- 前五秒检查：`samples/free-director-tool/review/first-five-seconds.jpg`

这条样片用真实的 `BLOCKED → PASSED` 预检记录演示“任务 → 输入 → 执行 → 结果”。六个场景采用六种不同的信息结构，Remotion 统一连续旁白、短语字幕、视觉和音频时间线。

旧 `pilots/` 目录中的 HyperFrames 样片已经被本方案取代，不再作为当前 Skill 的验收证据。

本地 QA 已通过，但 `platform_text_check.status` 保持 `not_observed`，所以 `publish_package.json` 按设计阻止发布。该状态不能改写成“平台已通过”。

```bash
python3 scripts/build_tool_director_pilot.py --voice-provider edge-tts
cd samples/free-director-tool
npm install
npm run typecheck
npm run render
python3 ../../skills/douyin-video-production-core/scripts/run_core_qa.py \
  --project . \
  --video render/final.mp4
```

## 安装

```bash
python3 scripts/sync_skills.py
```

该命令同步四个新 Skill 到：

- `~/.agents/skills`
- `~/.codex/skills`

并删除旧的两个活动目录，不保留兼容别名。

## 检查

```bash
python3 scripts/audit_legacy_removal.py
python3 /Users/wangchao/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/douyin-video-production-core
python3 /Users/wangchao/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/douyin-ai-tool-explainer
python3 /Users/wangchao/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/douyin-ai-news-explainer
python3 /Users/wangchao/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/douyin-ai-list-video
python3 -m py_compile skills/douyin-video-production-core/scripts/*.py research/*.py scripts/*.py
python3 -m pytest -q
```

## 本机工具路径

SAU 默认优先读取环境变量 `DOUYIN_SAU_BIN`，然后检查：

```text
/Users/wangchao/Desktop/抖音解析/local_tools/social-auto-upload/.venv/bin/sau
```

真实上传仍需显式传入 `--execute`，且 `publish_package.json`、本地文字检查和真实可见平台文字检查必须通过。
