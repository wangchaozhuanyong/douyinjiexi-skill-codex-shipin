# AI 视频唯一新脚本线

目标：以后 AI 类视频只给人暴露一个入口脚本，旧脚本全部降级为内部子命令，避免旧渲染、旧封面、旧 QA 路线回流。

## 用户可读执行步骤最新版

这版是日常做 AI 类视频时真正照着走的步骤。

工作边界：这份流程只保留日常执行需要看的正向步骤。以前犯过的旧问题不再作为制作时反复思考或对用户播报的清单；旧路线只放在脚本自动回归门里拦截。

全流程表达规则：生产执行时只写正向动作，比如今天扫了哪些来源、选了哪个题、用了哪个标题、调用哪个声音、选哪张背景、哪个转场 recipe、哪个封面模板、哪个检查报告通过。旧问题、失败词和禁止项只放在 QA、合规、测试和失败报告里。如果检查通过，下一步只引用“某报告通过”，不要反复复述旧问题。

### 1. 先扫当天热点

先查今天的 AI、Codex、ChatGPT、Gemini 热点。

如果今天没有强信号，再扩大到最近 7 天，并在报告里写明原因。

没完成这一步，不能写脚本、不能做图、不能配音、不能渲染、不能上传。

### 2. 选一个主题清晰的题

至少列 3 个候选题。

最后只选一个最适合短视频讲解的实用高级技巧题。

主题必须清晰，一条视频只讲一个明确问题或一个明确技巧。

不能凭感觉编热点，不能做泛泛介绍，不能把多个方向硬塞到一条视频里。

### 3. 写完整文案

写中文短视频脚本、字幕、标题、发布文案和话题。

文案必须让小白客户能听懂，用大白话讲清楚。

要求：

- 少用专业黑话。
- 不堆术语。
- 每句都要像在给普通用户解释。
- 先讲用户遇到的问题，再讲怎么做，最后讲保存哪几个步骤。

话题先建立一个 20 个左右的安全话题池。

最终发布话题最多 5 个，必须包含：

- `#gtp`
- `#codex`
- `#我在抖音聊科技`

另外从话题池里随机调用 2 个 AI 相关、安全、优雅的话题。

### 4. 一次性做文字合规

先本地检查所有会出现的文字：

- 标题
- 发布文案
- 话题
- 字幕
- 封面文字
- 画面里出现的所有文案

再用青豆检查发布时要填的标题、文案、话题。

第三步确定的发布文案和话题如果不再改，后面发布前不重复青豆；只核对文字是否和已通过版本完全一致。

如果后面任何文字变了，必须重新本地检查和青豆检查。

每次发现违规词、敏感词或青豆命中的词，都要写入本地禁词学习库，后面写文案时优先避开：

```bash
python3 scripts/update_forbidden_terms.py \
  --report <project>/internal/compliance_report.json \
  --report <project>/internal/qingdou_keyword_check.json \
  --out <project>/internal/forbidden_terms_update_report.json
```

长期词库是：

```text
references/forbidden_terms_learning_bank.jsonl
```

没通过合规前，不能生成最终视频，更不能发布。

### 5. 定视频风格

先确定这条视频用什么背景、画面结构、转场、动态效果和声音反馈。

默认可采用科技金属风格设计：

- 深色科技金属背景
- 数据光轨
- 玻璃/钛金属质感
- 青色、银白、琥珀色、信号绿点缀
- 画面干净、硬朗、有高级感

背景文件里已经有 10 张固定高级背景。

每次按视频尺寸和主题随机选择一张合适背景，不需要重新制作背景图片。

背景只负责高级氛围、材质、光线、景深和留白。

讲解内容每次都要重新设计，因为每条文案不同。

所有信息结构都放在前景层，按本条文案动态现做现用。

前景模块只从本条内容需要出发，比如：

- 来源证据
- 步骤清单
- 操作演示
- 测试结果
- 对比结果
- 字幕安全区

### 6. 做分镜

把视频拆成每个镜头。

每个镜头都要写清楚：

- 画面内容
- 字幕
- 动态效果
- 高级转场
- 音效

动态图标、勾选、状态节点、光标点击、锁定效果，都必须配轻音效。

可以设计科技感十足的动态图标、状态节点、光标路径和信息交接动效，目的必须是让当前信息更清楚、更高级。

QA 拦截清单只给脚本和报告使用，不写进分镜执行句：

- 斜线扫光
- 横向小光条乱跑
- 普通淡入淡出
- 普通左右滑入
- 简单箭头连接线
- 空导轨扫过
- 无信息作用线条
- 旧卡片轮播

分镜执行时只写正向 recipe 和信息交接动作。默认调用高级动效库：

- 金属舱门信息交接 `metal_aperture_handoff`
- 玻璃棱镜折射切换 `glass_prism_refraction`
- 语义节点接力 `semantic_node_relay`
- 来源证据聚焦锁定 `source_evidence_focus`
- 信息层级装配 `layered_information_assembly`
- 光标路径操作 `cursor_path_operation`
- 任务状态锁定 `state_lock_microinteraction`
- 清单矩阵装配 `checklist_matrix_assembly`
- 证明放大镜切换 `proof_lens_magnification`
- 结论模板收束 `final_template_convergence`

每个高级动效必须承担信息交接任务，比如来源到结论、结论到步骤、步骤到结果、旧任务到新任务。只好看但不传递信息的动效一律不用。

禁止一个图片讲解很久不动。

如果一句话要讲 8 到 10 秒，画面不能只停在一张大图上。

正确做法：

- 先给一张总览图。
- 随着讲解进度，把总览拆成小块。
- 讲到哪一块，就切换或放大哪一块。
- 用 2 到 3 张分步图跟着口播变化。
- 让画面跟着讲解推进，而不是一张图从头停到尾。

### 7. 生成/调用默认男声

默认男声固定为：

```text
voice_id: zh-CN-YunyangNeural
rate: +10%
tts_speed: <= 1.10
```

声音要求：

- 厚
- 有力
- 自然中文
- 专业讲师感

不能用软塌塌的默认声音。

如果已经有合格的本地默认男声音色/处理链，就优先调用本地固定配置，不每次重新试声音。

但每条视频仍要按本次文案生成新的旁白音频，因为文案内容不同。

### 8. 固定混音规则

人声和动态音效必须混在一起。

音效固定从本地 3 到 5 款轻音效里选，不每次临时乱调。

建议固定混音策略：

- 人声走厚男声处理链
- SFX 低于旁白约 `12dB-18dB`
- SFX 有声音，但不能盖住人声
- SFX 不能只写在分镜或报告里；必须做真实可听性检测。混入后的有效 SFX 峰值 `source_sfx_max + gain_db` 不得低于 `-15dBFS`，否则视为听不到，必须提高 SFX gain、重建 SFX bed，或在最终 MP4 上保留人声后叠加 root-level SFX。
- 如果画面和人声已经通过，只是 SFX 太小，优先保留最终视频画面和已验收人声，只重混/叠加 SFX 音轨；不要为了音效把整条视频重做。
- 人声从头到尾连续
- 切镜头时人声不能断、不能重启、不能被转场盖住

### 9. 做 HyperFrames 动态画面

用 HyperFrames 做高级动态画面。

固定准备 10 个高级转场方式，本地直接调用。

固定准备 10 个其他动态方式，本地随机或按场景调用。

执行方式：

- 直接调用固定高级转场包。
- 前景模块跟着口播做真实状态变化。
- 证据、步骤、测试、结果和字幕安全区各自有明确视觉职责。
- 动态图标、节点、勾选、锁定和光标点击同步触发轻 SFX。
- 动效描述只写选中的高级 recipe、当前信息从哪里交接到哪里、对应轻 SFX，不把 QA 拦截词当成工作步骤反复描述。
- 三列清单必须调用固定组件 `three_column_aligned_checklist`，不能手工随便摆三个圆点和三段文字。

每个镜头都要有真实动态变化。

### 9.1 版式和文字 QA

渲染前后必须检查版式和文字。

三列、清单、步骤、证据、模板类画面必须使用固定组件和网格：

- 三列同宽
- 数字/图标圆心同一 `y`
- 标题同一基线
- 正文文字框同一 `y`
- 每列正文最多 2 行
- 文字框内边距至少 `24px`
- 标题区域边距至少 `36px`
- 底部总结离边框至少 `48px`
- 装饰线、光效、连接线、光标路径不能穿过文字

所有可见文字必须先测量：

1. 先放入固定文字框。
2. 超宽先自动换行。
3. 超高再在安全范围内缩小字号。
4. 还放不下就改短文案。
5. 不允许文字溢出文字框、贴边、重叠或被光效压住。

每条视频必须生成：

```text
internal/render_layout_manifest.json
internal/layout_motion_contract_report.json
```

然后运行：

```bash
python3 scripts/check_motion_layout_contract.py --project <project>
```

没通过前不能进入 visual_regression_gate，不能交付 final.mp4。

### 10. 走稳定渲染路线

固定采用稳定路线：

```text
HyperFrames 先导出图片序列
再用 FFmpeg 合成 MP4
```

不再直接相信 HyperFrames 直出 MP4，因为曾经出现视频流 13.4 秒、音频 72 秒的问题。

### 11. 做第一帧封面

第一帧封面也固定准备 10 张高级主题封面模板，轮流调用。

封面不是每次从零生成。

规则：

- 第一帧必须是主题封面
- 第一帧只占 1 帧
- 作用是让抖音抓封面
- 第二帧马上进入正式视频
- 封面不能跑题
- 封面不能用通用旧模板
- 封面文字必须来自已通过合规的安全文案

### 12. 跑 QA 检查

前期每条都跑 QA，检查：

- 画质
- 音画同步
- 字幕
- 空帧
- 首帧封面
- 视觉质量
- 旧逻辑回流
- 无用模块
- SFX 是否压人声

如果连续 10 条作品都稳定无问题，后续可以把部分重型 QA 降频。

但低成本硬检查不能取消，包括：

- 最终 MP4 能否 ffprobe
- 视频/音频时长是否一致
- 首帧是否匹配封面
- 第二帧是否回到正式画面
- 全项目是否只剩最终 MP4

### 13. 清理文件

删除：

- 图片序列
- 中间 MP4
- HyperFrames work 缓存
- 临时抽帧目录

最后只保留一个最终视频：

```text
final/final.mp4
```

QA 报告、合规报告、选题报告、堵点记录可以保留。

### 14. 发布前核对

发布前不再重复做已经通过的青豆检测。

只核对：

- 发布标题是否和已通过版本一致
- 发布文案是否和已通过版本一致
- 话题是否和已通过版本一致
- 封面文字是否和已通过版本一致
- 发布合同是否完整

如果第三步之后文字有任何变化，必须重新检测。

如果自定义封面需要你确认，就停下来等你看。

### 15. 发布

只有用户明确要求发布，才进入发布。

发布时：

- 复用用户当前已登录 Chrome
- 不新开浏览器窗口
- 如果不得不开新 tab/window，结束前关闭
- 不保存账号密码、Cookie、验证码

遇到短信验证码、实名、必须本人验证，立刻停止并告诉用户。

## 唯一入口

```bash
python3 scripts/ship_ai_video.py \
  --date 2026-06-21 \
  --theme ai \
  --project outputs/2026-06-21-<topic-slug> \
  --mode make-final \
  --voice-id zh-CN-YunyangNeural \
  --voice-rate +10% \
  --no-publish
```

发布必须单独显式执行：

```bash
python3 scripts/ship_ai_video.py \
  --project outputs/2026-06-21-<topic-slug> \
  --mode publish \
  --reuse-current-chrome
```

默认 `make-final` 只做成片，不上传、不发布。

## 模式定义

- `research-only`：只做热点扫描，产出候选主题和来源报告。
- `make-final`：从选题扫描一直做到 `final/final.mp4`，不发布。
- `prepublish-check`：只复核 Qingdou、本地合规、发布合同和封面审批。
- `publish`：只在全部门禁通过后，复用当前已登录 Chrome 发布。

不再给人使用 `run_pipeline.py`、`produce_ai_video.py --mode qa-promote`、`select_fixed_cover_template.py`、手写 FFmpeg overlay 命令或 HyperFrames 直出 MP4 命令。

## 总流程

```text
00 init_project_and_blocker_log
01 topic_scan_gate
02 select_one_topic
03 copy_and_compliance_gate
04 visual_director_contract
05 storyboard_and_audio_lock
06 hyperframes_timeline_source
07 render_frames_with_hyperframes
08 encode_mp4_atomically
09 topic_cover_first_frame
10 qa_gate_stack
11 prepublish_gate_stack
12 promote_final_or_stop
13 optional_publish
14 cleanup_and_blocker_report
```

## 00 init_project_and_blocker_log

脚本启动后第一件事：

- 创建 `outputs/<date-topic>/internal/production_blockers.md`。
- 写入运行参数、日期、主题、是否允许发布、是否复用 Chrome。
- 创建 `internal/run_state.json`，记录当前阶段。
- 每个外部命令都必须写入 `internal/commands.log`。

遇到任何堵点都追加到 `production_blockers.md`，不能只打印在终端。

## 01 topic_scan_gate

硬规则：未完成当天热点扫描，不允许进入文案、图片、TTS、视频或上传。

内部子命令：

```bash
python3 scripts/research_topic.py \
  --theme ai \
  --date <YYYY-MM-DD> \
  --out <project>/internal/topic_candidates.json
```

新脚本必须额外生成：

- `internal/topic_scan_report.md`
- `internal/selected_topic.json`

扫描必须覆盖：

- AI 通用新闻
- Codex/OpenAI
- ChatGPT/OpenAI
- Gemini/Google AI

当天信号不足时，扩大到最近 7 天，并在 `topic_scan_report.md` 写明。

## 02 select_one_topic

只能选择一个主题。

选择标准：

- 热度高
- 信息新
- 有来源链接和可见日期
- 能变成高级实用技巧
- 适合短视频讲清楚

禁止：

- 凭记忆制造热点
- 做泛泛介绍
- 同类题连续重复

## 03 copy_and_compliance_gate

必须产出：

- `internal/copy_package.md`
- `internal/copy_package.json`
- `internal/publish_copy.txt`
- `internal/script_score.json`
- `internal/semantic_review.json`
- `internal/beginner_value_review.json`
- `internal/compliance_report.json`

标题、文案、话题规则：

- 话题最多 5 个
- 必须包含 `#gtp`
- 必须包含 `#codex`
- 另外 3 个使用安全、优雅、AI 相关话题

Qingdou 规则：

- 本地合规先过。
- Qingdou 检查 `title + caption + topics`。
- Qingdou 输入、粘贴、点击检测、普通滑块/图片验证等常规检测链路由 Codex 自己执行，不能把文本交回给用户手动粘贴或检测。
- 优先复用用户当前已登录的 Chrome/当前标签页；如果必须临时打开新标签或窗口，任务结束后关闭。
- 可以使用当前环境允许的安全浏览器自动化方式完成页面输入和读取可见结果，但不得提取、保存或复用账号密码、Cookie、验证码、短信码、验证数据。
- 固定话题 `#我在抖音聊科技` 是用户长期强制保留话题；如果 Qingdou 只命中这个话题里的 `抖音`，且标题、正文、字幕、封面、画面文字和其它话题没有命中，直接记录 `status: "user_override_accepted"` 并继续，不再询问用户。这个 override 不能写成 Qingdou passed，也不能扩展到其它命中词或其它字段。
- 如果公开文案变了，必须重新 Qingdou。
- 没有 Qingdou visible passed evidence，不允许发布。
- 短信验证码、实名、账号本人验证直接停止。

## 04 visual_director_contract

必须产出：

- `internal/director_selection.json`
- `internal/style_recipe.json`
- `internal/fixed_template_selection.json`
- `internal/hook_variants.json`
- `internal/hook_score_report.json`
- `internal/reference_overfit_audit.json`

活跃正向合约：

- 背景作为固定高级氛围资产使用，负责材质、光线、景深和留白。
- 前景模块服务于来源证据、步骤清单、操作测试、结果证明或字幕安全区。
- 主转场调用高级 named recipes，并承载信息状态变化。
- 动态图标、状态节点、勾选、锁定、光标点击都有同步 SFX。
- SFX 位于旁白下方约 `12dB-18dB`。
- SFX 必须听得见：`internal/sfx_audibility_report.json` 或 `internal/voice_mix_report.json.sfx_audibility.status` 必须为 `passed`。只检查 `sfx_cues` 存在不够，最终音频里必须能检测到有效 SFX 峰值。

## 05 storyboard_and_audio_lock

必须产出：

- `internal/storyboard.json`
- `internal/storyboard_validation.json`
- `internal/storyboard.audio_locked.json`
- `assets/audio/narration-continuous.*`
- `assets/audio/narration-processed-thick.wav`
- `assets/audio/narration-with-voice-safe-sfx.wav`
- `internal/voice_mix_report.json`
- `internal/sfx_audibility_report.json`（或 voice mix report 内的 `sfx_audibility`）

默认旁白：

- provider：`edge_tts`
- voice_id：`zh-CN-YunyangNeural`
- provider rate：约 `+10%`
- metadata `tts_speed <= 1.10`
- 必须记录 `voice_speed_policy`
- 必须记录 `voice_speed_approval`
- 必须记录真实 `voice_id/rate`
- 必须记录音频锁定时长

旁白必须是连续 root narration bed，场景切换不能重启、断开或淡出。

## 06 hyperframes_timeline_source

必须保留 HyperFrames 源：

- `assets/hyperframes/index.html`
- 或 `index.html`
- 或等价 HyperFrames composition source

禁止：

- 用旧 PIL 竖版海报流水线当最终视频源
- 用 rawvideo pipe 当最终视频源
- 用 text-card slideshow 冒充高级视频
- 用 “HyperFrames compatible” 但实际不是 HyperFrames final timeline 的描述

## 07 render_frames_with_hyperframes

固定使用 HyperFrames PNG sequence 作为稳定路线：

```bash
npx --yes hyperframes render <hyperframes-entry> \
  --format png-sequence \
  --fps 30 \
  --protocol-timeout 900000 \
  --output <project>/internal/hf_frames
```

规则：

- 不再默认使用 HyperFrames 直出 MP4。
- 如果直出 MP4 以后修复，也只能作为可选快速路径；最终仍需 ffprobe 验证视频流和音频流时长一致。
- 如果 PNG sequence timeout，要记录 blocker，并降低并发或分段重试。

## 08 encode_mp4_atomically

最终编码只能写临时文件：

```bash
ffmpeg ... <project>/internal/draft.tmp.mp4
ffprobe ... <project>/internal/draft.tmp.mp4
mv <project>/internal/draft.tmp.mp4 <project>/internal/draft.mp4
```

禁止：

- 直接写 `draft.mp4`
- 让坏 MP4 占用正式文件名
- 没有 `moov atom` 或 ffprobe 失败还继续 QA

编码要求：

- 1920x1080
- 30fps
- H.264 yuv420p
- AAC audio
- `-movflags +faststart`
- 目标码率约 8Mbps
- 音频与视频时长差小于 0.3 秒

## 09 topic_cover_first_frame

第一帧封面必须主题匹配。

规则：

- 首帧只占 1 帧，也就是 1/30 秒。
- 第二帧必须回到正式动态画面。
- 不使用跑题的通用固定封面。
- 封面文本必须来自已过检标题/文案/话题的安全子集。
- 封面必须做文本碰撞检查，不能出现标题压卡片、话题压终端卡。

输出：

- `internal/first_frame_cover.png`
- `internal/actual_frame_000_cover.png`
- `internal/actual_frame_001_after_cover.png`
- `internal/publish_cover_text.txt`
- `internal/publish_cover_report.json`

如果使用自定义主题封面：

- `publish_cover_report.cover_type = one_off_custom_reviewed`
- 发布前必须有用户确认或人工审批记录
- 没确认时，允许生成 `final/final.mp4` 给用户看，但不允许发布

## 10 qa_gate_stack

必须依次通过：

```bash
python3 scripts/check_audio_continuity.py ...
python3 scripts/video_technical_qa.py ...
python3 scripts/frame_review.py ...
python3 scripts/export_render_text_manifest.py ...
python3 scripts/check_screen_text.py ...
python3 scripts/check_empty_frames.py ...
python3 scripts/visual_aesthetic_review.py ...
python3 scripts/qa_gate.py ...
python3 scripts/produce_ai_video.py --mode visual-gate ...
python3 scripts/audit_provider_usage.py ...
```

硬门：

- `qa_report.status = passed`
- `quality_level = high_quality`
- `visual_regression_gate.status = passed`
- `provider_usage_audit.status = passed`
- `video_technical_qa.status = passed`
- `audio_continuity_report.status = passed`
- `visual_review.status = passed`
- `frame_review_report.status = passed`

警告可以存在，但必须解释；阻断项必须修完。

## 11 prepublish_gate_stack

发布前必须通过：

```bash
python3 scripts/check_public_copy.py ...
python3 scripts/build_publish_contract.py ...
python3 scripts/pre_publish_gate.py ...
```

要求：

- 本地合规包含 `render_text_manifest + publish_cover_text + publish_copy`
- Qingdou 结果 passed
- 封面报告 passed
- 发布合同 gate passed

如果卡在自定义封面审批：

- 记录 blocker
- 输出 final 给用户看
- 不发布

## 12 promote_final_or_stop

只有 `pre_publish_gate` 通过时，才执行：

```bash
python3 scripts/promote_final.py \
  --project <project> \
  --contract <project>/internal/publish_contract.json
```

如果 `pre_publish_gate` 因用户确认缺失失败：

- 允许手动复制 `internal/draft.mp4` 到 `final/final.mp4` 作为预览成片
- 必须在报告里写明“未通过发布前门禁，不允许上传”

## 13 optional_publish

只有 `--mode publish` 才进入。

规则：

- 复用当前已登录 Chrome。
- 不新开浏览器窗口。
- 如果不得不开新 tab/window，结束前关闭。
- 不保存账号密码、Cookie、验证码。
- 短信验证码、实名、账号本人验证直接停止。

## 14 cleanup_and_blocker_report

成片后清理：

- 删除 `internal/hf_frames`
- 删除 `internal/work-*`
- 删除中间 MP4
- 全项目只保留一个 MP4：`final/final.mp4`

保留：

- QA 报告
- 合规报告
- Qingdou 结果
- 选题报告
- 封面报告
- `production_blockers.md`
- `production_postmortem.json`

## 自动回归门专用旧路线清单

下面只给脚本和 QA 使用，不进入日常制作步骤、不作为工作中反复讨论的提醒。新脚本必须显式拒绝这些路线：

- 旧 PIL/ImageDraw 视频生成器
- rawvideo pipe 直接生成成片
- HyperFrames 直出 MP4 未 ffprobe 就交付
- 直接 overlay 封面到正式 `draft.mp4`
- 通用固定封面跑题仍发布
- 手动封面无文本碰撞检测
- 只跑本地合规不跑 Qingdou 就发布
- 新开浏览器窗口后不关闭
- `run_pipeline.py` 直接晋级或发布

## 后续落地文件

确认这条线后，真正落地只新增一个人用脚本：

```text
scripts/ship_ai_video.py
```

旧脚本保留为内部子命令，但 README、SKILL、自动化任务只允许写这个入口。
