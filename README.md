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
-> ai_hot_rank_top5 when scheme_7_ai_hot_rank_top5
-> director_selection + style_recipe + hook_variants + hook_score_report + reference_overfit_audit
-> fixed_template_selection
-> copy_package + script_score + semantic_review + content_alignment_report + beginner_value_review
-> compliance_report
-> reference_analysis when needed
-> visual_style_decision + visual_style_plan + background_prompt_pack + asset_prompt_validation
-> storyboard + storyboard_validation + content_alignment_report refresh
-> foreground_module_plan + foreground_module_plan_check
-> foreground_module_render_manifest + foreground_module_render_check
-> asset_manifest + visual_tone_report + asset_validation
-> storyboard.audio_locked + continuous narration bed + visual beat lock
-> hyperframes_render_profile + HyperFrames PNG sequence + leading_frame_repair_report
-> draft.mp4 + metadata
-> audio_continuity_report + video_technical_qa + frame_review
-> render_text_manifest + screen_text_proofread + empty_frame_report + visual_review
-> qa_report + production_postmortem
-> publish_cover_report + on_screen_and_publish_text_compliance_report
-> visual_regression_gate
-> provider_usage_audit + qingdou_keyword_check
-> publish_contract + pre_publish_gate
-> promote_final
-> final/final.mp4
-> optional douyin_sau_upload_report when user authorizes SAU upload
```

几个不可破坏的口径：

- 没有 `topic_candidates.json` 和 `selected_topic.json`，不要写完整文案。
- 没有 `director_selection.json`、`style_recipe.json`、`hook_variants.json`、`hook_score_report.json` 和 `reference_overfit_audit.json`，不要写完整文案、分镜、出图、TTS、渲染或上传。参考视频只能进入候选池，不能自动变成下一条视频的固定模板。
- 没有 `fixed_template_selection.json`，不要进入视觉计划、背景提示词、组件分镜、转场或男声混音；先锁定背景模板、转场/组件包、前景组件包和男声混音 profile。音频默认只走干净人声；如需背景音乐，只能用已授权音乐库或明确授权的同平台参考音乐。
- 前景动态内容必须先写 `internal/foreground_module_plan.json`，每个镜头选择一个 M01-M20 母模块，再嵌入 2-5 个 C01-C30 微组件，运行 `scripts/check_foreground_module_plan.py`；然后用 `scripts/render_foreground_module_pack.py` 生成 HyperFrames 可嵌入 HTML/CSS/JS 前景包，再用 `scripts/check_foreground_module_render_pack.py` 检查。两个检查都通过后再写正式 HyperFrames；生产记录写选中的模块、锚点、阶段、文字槽位、转场和 render pack 路径，不把旧问题当作工作步骤反复描述。
- 热点扫描必须覆盖 AI、Codex/OpenAI、ChatGPT/OpenAI、Gemini/Google AI 四个方向。先扫当天；当天信号不足时只扩大到最近 7 天并在报告里说明。超过 7 天的资料只能做背景，不算当前热点覆盖。
- `AI 热榜 TOP5`、`TOP5`、`榜单`、`排行`、`排名` 这类当前 AI 新闻/热点需求必须走 `scheme_7_ai_hot_rank_top5`：先写 `internal/hot_rank_scan_report.md` 和 `internal/ai_hot_rank_top5.json`，按 `templates/ai_hot_rank_top5.template.json` 锁 5 条真实来源、可见日期、打分和排序，不能凭感觉编热榜。
- 面向小白的竖版 AI 清单视频默认优先讲 Skill，而不是泛泛讲 AI 新闻。用户说 `Skill`、`新手`、`清单`、`推荐`、`插件`，或指出要讲 skill 能达到什么目的时，走 `scheme_1_skill_recommendation_no_voice`：先搜索/核对真实来源，写 `internal/skill_source_manifest.json`，锁真实 `SKILL.md` 名称、`agents/openai.yaml` 展示名、左侧图标文件和来源依据，并运行 `scripts/check_skill_source_manifest.py`。不能自己编 `页面整理 Skill` 这类不存在的名字，也不能只拿真实名字再编“输入/目的/产出”。清单必须设置 `copy_mode=source_quoted_or_source_paraphrase`，每行公开视频文案用 `public_note` 表达，并在 `claim_evidence` 里记录对应的来源字段、来源原文和改写方式。公开视频和发布文案不得出现 `网址`、`链接`、`打开某站`、`复制链接`、`扫码`、`私信`、`领取`、`下载` 等导流表达；来源 URL 只允许留在内部证据字段。
- 45-75 秒 AI 视频不要让同款大矩形面板成为默认视觉；场景数量允许时至少使用 4 种信息结构。高级转场必须完成来源、步骤、结果或清单状态的交接，不能只靠抽象斜线、空轨道或节点扫过。
- 没有 `copy_package.md` 和 `copy_package.json`，不要做分镜。
- `script_score.json`、`semantic_review.json`、`content_alignment_report.json`、`beginner_value_review.json` 没 passed，不要进入生产。
- `content_alignment_report.json` 必须证明每条核心 claim 有来源/证据绑定、每个场景只承担一个新增信息任务、每个视觉任务对应当前中文文案和 claim，非必要英文不会出现在公开视频文字里。
- `problem_example_score < 8.5` 时不要继续；提到 `不会`、`问题`、`错误`、`空话`、`套话`、`乱`、`反复改` 等痛点时，必须给具体例子。
- `compliance_report.json` 没 passed，不要生成图片、TTS、视频或发布动作。
- AI 证明型视频默认 16:9：`1920x1080`。只有轻量清单/卡片/海报式竖版参考可走 9:16 信息海报例外。
- `visual_style_decision.json` 必须先于 `visual_style_plan.json` 生成，由 Codex 按选题类型、文案情绪、证据密度和参考视频节奏选择色系；`daylight_productivity` 只是候选，不是默认。
- 发布级配音必须真实记录来源并通过样音批准；macOS `say`、Apple/system voice、`Tingting` 或 scratch TTS 不能伪装成自然发布级音频。
- 背景声音硬规则：只允许两种模式。第一，用音乐，且必须来自用户音乐库、已授权本地音乐、或明确授权的同平台抖音参考音乐；不得自己生成、合成、仿造或替换音乐。第二，不用任何背景声，只保留干净人声讲解。不要制作或混入 `sfx-bed.wav` 这类连续音效床、噪声床、电流声、环境纹理、whoosh 床或任何自制“氛围声”。知识类口播默认 `voice_only_clean`。
- `qa_report.json`、`visual_regression_gate.json`、`provider_usage_audit.json`、`qingdou_keyword_check.json`、`publish_cover_report.json` 和本地文本合规都满足后，才允许 `publish_contract.json` 的 `gate.status` 变成 `passed`。
- `promote_final.py` 只认已通过的 `publish_contract.json`，不再直接拼散落报告。
- `repair_hyperframes_leading_frames.py` 在 HyperFrames PNG sequence 后、FFmpeg 编码前运行，保证第 1 帧已经是正片内容；第 0 帧仍留给后续一帧封面叠加。
- `write_hyperframes_render_profile.py` 在 HyperFrames PNG sequence 前写入稳定渲染 profile，默认 1920x1080、30fps、单 worker、`protocol_timeout_ms=900000`，让截图序列走同一条可复用路线。
- `produce_ai_video.py` 会检查 `storyboard.audio_locked.json` 里的长口播镜头是否有足够视觉节拍；超过 5 秒的锁定音频必须拆出对应 `beat_map`，让画面按口播推进。
- `promote_final.py` 晋级后 `final/` 只保留 `final.mp4`；封面、metadata、发布文案、合约等证据留在 `internal/`，同时清理图片序列、中间 MP4 和临时音频，并写出 `internal/cleanup_report.json`。
- 唯一生产入口是 `scripts/produce_ai_video.py`。`scripts/run_pipeline.py` 只保留为内部 QA 顺序兼容工具，不作为出片或晋级入口。
- 默认不自动发布。用户明确授权后，仍要先过 QA 和 Qingdou。只有当轻抖只命中用户指定必须保留的官方/平台活动话题，且用户看过失败结果后明确接受风险，才允许记录 manual override 后继续；不要把这种情况写成轻抖通过。
- 抖音自动上传可选走第三方 `social-auto-upload` 的 `sau` CLI，但只能通过 `scripts/douyin_sau_publish.py` 包装层进入。该脚本先检查 `publish_contract.gate=passed`、`final/final.mp4`、封面、Qingdou、`video_technical_qa.json` 和 `audio_continuity_report.json`，默认只 dry-run 写 `internal/douyin_sau_upload_report.json`；真正上传必须显式传 `--execute`，并优先使用 `--schedule`。

## 常用命令

基础健康检查：

```bash
python3 scripts/doctor.py
python3 -m py_compile scripts/*.py
python3 -m pytest -q
python3 scripts/check_golden_project.py
```

唯一入口，只跑 QA 和视觉回归门禁：

```bash
python3 scripts/produce_ai_video.py --project outputs/demo --mode qa-only
```

QA 通过后尝试推广到 `final/`：

```bash
python3 scripts/produce_ai_video.py --project outputs/demo --mode qa-promote
```

旧兼容命令 `scripts/run_pipeline.py` 不再作为生产入口；它不能替代 `visual_regression_gate.json`，也不能直接把项目推进发布级。

单独执行最终推广：

```bash
# 文案阶段先写好 outputs/demo/internal/publish_cover_text.txt，再和发布文案、字幕一起完成本地合规。
python3 scripts/check_public_copy.py \
  outputs/demo/internal/render_text_manifest.json \
  outputs/demo/internal/publish_cover_text.txt \
  outputs/demo/internal/publish_copy.txt \
  --out outputs/demo/internal/on_screen_and_publish_text_compliance_report.json
# 再按视频尺寸从 10 套固定纯背景中顺序选择一张，并把已过检封面文字合成到第一帧。
python3 scripts/select_fixed_cover_template.py \
  --project outputs/demo \
  --video-width 1920 \
  --video-height 1080 \
  --require-checked-cover-text
python3 scripts/produce_ai_video.py --project outputs/demo --mode visual-gate
python3 scripts/build_publish_contract.py --project outputs/demo
python3 scripts/pre_publish_gate.py --contract outputs/demo/internal/publish_contract.json
python3 scripts/promote_final.py --project outputs/demo --contract outputs/demo/internal/publish_contract.json
```

SAU 抖音上传 dry-run：

```bash
python3 scripts/douyin_sau_publish.py \
  --project outputs/demo \
  --account <sau_douyin_account> \
  --sau-bin /Users/wangchao/Desktop/social-auto-upload/.venv/bin/sau \
  --schedule "2026-07-01 21:30"
```

确认 `internal/douyin_sau_upload_report.json` 后才执行真实上传：

```bash
python3 scripts/douyin_sau_publish.py \
  --project outputs/demo \
  --account <sau_douyin_account> \
  --sau-bin /Users/wangchao/Desktop/social-auto-upload/.venv/bin/sau \
  --schedule "2026-07-01 21:30" \
  --execute
```

固定封面轮换规则：

```bash
# 16:9 视频走 T01-T10 的横版背景，9:16 视频走 T01-T10 的竖版背景；各自按顺序轮换。
python3 scripts/select_fixed_cover_template.py \
  --project outputs/demo \
  --video-width 1920 \
  --video-height 1080 \
  --require-checked-cover-text
```

固定生产模板选择：

```bash
python3 scripts/select_fixed_ai_templates.py \
  --project outputs/demo \
  --director-selection outputs/demo/internal/director_selection.json \
  --style-recipe outputs/demo/internal/style_recipe.json \
  --video-width 1920 \
  --video-height 1080
```

该命令会把固定背景图路径写入 `internal/fixed_template_selection.json` 的 `background_template.fixed_asset_path`。后续 HyperFrames 必须直接使用 `assets/ai_background_templates_fixed/` 中的固定背景资产，不要每条视频临时重画背景。

前景模块计划检查：

```bash
python3 scripts/check_foreground_module_plan.py --project outputs/demo
python3 scripts/render_foreground_module_pack.py --project outputs/demo
python3 scripts/check_foreground_module_render_pack.py --project outputs/demo
```

这组命令读取 `internal/foreground_module_plan.json`，检查母模块、微组件、锚点、文字槽位、转场、视觉权重和动画并发，然后生成 `internal/foreground_module_render_pack.html`、`assets/hyperframes/foreground_modules/` 和 `internal/foreground_module_render_manifest.json`，最终报告写入 `internal/foreground_module_render_check.json`。

参考视频分析：

```bash
python3 scripts/analyze_reference.py \
  --input "<本地参考视频路径；抖音链接/分享文本需先下载成可播放视频>" \
  --out outputs/demo/internal/reference_analysis.json
```

如果用户给的是抖音链接或分享文本，先下载/取得可播放的视频本体并自己看过，再把本地视频路径传给脚本。只看标题、封面、分享文案、URL 元信息、音乐页或作者页不算参考视频分析。

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
- 参考视频原创边界：`references/reference_driven_production_rules.md`、`references/codex_operation_micro_tutorial_style.md`
- 小白文案：`references/beginner_copywriting_rules.md`、`references/script_quality_rules.md`
- 抖音合规和 Qingdou：`references/global_douyin_text_compliance_rule.md`、`references/douyin_compliance_rules.md`
- 固定生产模板：`references/fixed_ai_production_templates.md`
- 视觉描述和生成图：`references/visual_description_language_reference.md`、`references/visual_prompt_motion_phrasebook.md`、`references/ai_generated_asset_prompt_system.md`
- HyperFrames：`references/premium_ai_video_source_to_hyperframes_rule.md`、`references/hyperframes_delivery.md`
- 多插件证据：`references/codex_plugin_integration.md`
- 学习复盘：`references/learning_bank.md`、`references/failed_case_library.md`、`references/director_decision_patterns.md`

## 维护规则

- 入口文件只放导演口径和导航；详细规则放进 `references/`。
- 新增硬门时同步改 `scripts/`、`schemas/`、`tests/`、`examples/golden_ai_prompt_case/` 和 `doctor.py`。
- 修改后先跑完整检查，再同步安装副本。
- 不要把 `outputs/`、`build/`、`dist/`、`mp3/`、日志、缓存或下载素材同步进 skill。
