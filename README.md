# Douyin AI Video Director Skill

`douyin-hyperframes-remake` V3 是一个 Codex skill，用来制作原创、合规、发布级的 AI 圈知识类抖音短视频。它不是普通“重做参考视频”的提示词集合，而是一条可执行、可验收、可复盘的生产流水线。

当前仓库同时包含两类东西：

- Skill 核心：`SKILL.md`、`agents/`、`references/`、`schemas/`、`templates/`、`scripts/`、`tests/`、`examples/`
- 本地抖音解析/下载工具：`douyin_media_*.py`、`douyin_to_mp3.py`、`build/`、`dist/`、`mp3/`、`导出/`

整理 skill 时默认只动第一类。不要把桌面解析工具、生成视频、下载音频或构建产物混进 skill 规则里。

## 运行边界

默认走最高级发布流程，除非用户明确说只做研究、只做方案、快速草稿或 smoke test。完整生产必须经过选题、文案、小白价值、合规、视觉导演、素材、TTS、HyperFrames、QA、封面、Qingdou、发布合约、最终推广这条链。

核心入口在 [SKILL.md](SKILL.md)。完整硬门和输出结构以 [references/workflow_contract.md](references/workflow_contract.md) 为准。

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

兼容说明：旧版 Codex 环境可能仍使用 `~/.codex/skills`。本机源码更新后，用同步脚本把当前源码同步到 `~/.agents/skills/douyin-hyperframes-remake` 和 `~/.codex/skills/douyin-hyperframes-remake`。

```bash
python3 scripts/sync_installed_skill.py --prune
```

## 标准流程

```text
topic_candidates
-> selected_topic
-> copy_package + script_score + semantic_review + beginner_value_review
-> compliance_report
-> reference_analysis when needed
-> visual_style_decision + visual_style_plan + background_prompt_pack + asset_prompt_validation
-> storyboard + storyboard_validation
-> asset_manifest + visual_tone_report + asset_validation
-> storyboard.audio_locked + continuous narration bed
-> draft.mp4 + metadata
-> audio_continuity_report + video_technical_qa + frame_review
-> render_text_manifest + screen_text_proofread + empty_frame_report + visual_review
-> qa_report + production_postmortem
-> publish_cover_report + on_screen_and_publish_text_compliance_report
-> provider_usage_audit + qingdou_keyword_check
-> publish_contract + pre_publish_gate
-> promote_final
-> final/final.mp4
```

几个不可破坏的口径：

- 没有 `topic_candidates.json` 和 `selected_topic.json`，不要写完整文案。
- 没有 `copy_package.md` 和 `copy_package.json`，不要做分镜。
- `script_score.json`、`semantic_review.json`、`beginner_value_review.json` 没 passed，不要进入生产。
- `problem_example_score < 8.5` 时不要继续；提到 `不会`、`问题`、`错误`、`空话`、`套话`、`乱`、`反复改` 等痛点时，必须给具体例子。
- `compliance_report.json` 没 passed，不要生成图片、TTS、视频或发布动作。
- AI 证明型视频默认 16:9：`1920x1080`。只有轻量清单/卡片/海报式竖版参考可走 9:16 信息海报例外。
- `visual_style_decision.json` 必须先于 `visual_style_plan.json` 生成，由 Codex 按选题类型、文案情绪、证据密度和参考视频节奏选择色系；`daylight_productivity` 只是候选，不是默认。
- 发布级配音必须真实记录来源并通过样音批准；macOS `say`、Apple/system voice、`Tingting` 或 scratch TTS 不能伪装成自然发布级音频。
- `qa_report.json`、`provider_usage_audit.json`、`qingdou_keyword_check.json`、`publish_cover_report.json` 和本地文本合规都满足后，才允许 `publish_contract.json` 的 `gate.status` 变成 `passed`。
- `promote_final.py` 只认已通过的 `publish_contract.json`，不再直接拼散落报告。
- 默认不自动发布。用户明确授权后，仍要先过 QA 和 Qingdou。只有当轻抖只命中用户指定必须保留的官方/平台活动话题，且用户看过失败结果后明确接受风险，才允许记录 manual override 后继续；不要把这种情况写成轻抖通过。

## 常用命令

基础健康检查：

```bash
python3 scripts/doctor.py
python3 -m py_compile scripts/*.py
python3 -m pytest -q
python3 scripts/check_golden_project.py
```

只跑 QA：

```bash
python3 scripts/run_pipeline.py --project outputs/demo --mode qa-only
```

QA 通过后尝试推广到 `final/`：

```bash
python3 scripts/run_pipeline.py --project outputs/demo --mode qa-promote
```

单独执行最终推广：

```bash
python3 scripts/generate_publish_cover.py --project outputs/demo
python3 scripts/check_public_copy.py \
  outputs/demo/internal/render_text_manifest.json \
  outputs/demo/internal/publish_cover_text.txt \
  outputs/demo/internal/publish_copy.txt \
  --out outputs/demo/internal/on_screen_and_publish_text_compliance_report.json
python3 scripts/build_publish_contract.py --project outputs/demo
python3 scripts/pre_publish_gate.py --contract outputs/demo/internal/publish_contract.json
python3 scripts/promote_final.py --project outputs/demo --contract outputs/demo/internal/publish_contract.json
```

参考视频分析：

```bash
python3 scripts/analyze_reference.py \
  --input "<抖音链接/分享文本/本地视频路径>" \
  --out outputs/demo/internal/reference_analysis.json
```

小白文案训练：

```bash
python3 scripts/train_beginner_copy.py \
  --iterations 10 \
  --out-dir outputs/beginner-copy-training-2026-06-17/internal
```

违规词学习：

```bash
python3 scripts/update_forbidden_terms.py \
  --report outputs/demo/internal/compliance_report.json \
  --report outputs/demo/internal/qingdou_keyword_check.json \
  --out outputs/demo/internal/forbidden_terms_update_report.json
```

## 参考文件怎么读

- 总流程和硬门：`references/workflow_contract.md`
- 视频质量：`references/video_quality_contract.md`、`references/premium_video_quality_playbook.md`
- 参考视频原创边界：`references/reference_driven_production_rules.md`
- 小白文案：`references/beginner_copywriting_rules.md`、`references/script_quality_rules.md`
- 抖音合规和 Qingdou：`references/global_douyin_text_compliance_rule.md`、`references/douyin_compliance_rules.md`
- 视觉描述和生成图：`references/visual_description_language_reference.md`、`references/visual_prompt_motion_phrasebook.md`、`references/ai_generated_asset_prompt_system.md`
- HyperFrames：`references/premium_ai_video_source_to_hyperframes_rule.md`、`references/hyperframes_delivery.md`
- 多插件证据：`references/codex_plugin_integration.md`
- 学习复盘：`references/learning_bank.md`、`references/failed_case_library.md`、`references/director_decision_patterns.md`

## 维护规则

- 入口文件只放导演口径和导航；详细规则放进 `references/`。
- 新增硬门时同步改 `scripts/`、`schemas/`、`tests/`、`examples/golden_ai_prompt_case/` 和 `doctor.py`。
- 修改后先跑完整检查，再同步安装副本。
- 不要把 `outputs/`、`build/`、`dist/`、`mp3/`、日志、缓存或下载素材同步进 skill。
