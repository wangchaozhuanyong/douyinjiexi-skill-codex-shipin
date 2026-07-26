# 完全自由导演契约

自由导演意味着每条视频重新建立视觉语言，不意味着取消事实、可读性和技术边界。

## 创意决策

在 `storyboard.json.creative_direction` 记录：

- `visual_thesis`：一句话说明这条视频的视觉核心。
- `reason_for_topic`：为什么该视觉方式适合当前工具、新闻或清单。
- `evidence_strategy`：真实界面、输入、过程和结果怎样成为画面主体。
- `motion_logic`：运动由哪些信息事件触发。
- `continuity_devices[]`：贯穿全片但不构成固定皮肤的连续线索。
- `rejected_defaults[]`：本次主动排除的惯性模板或无意义装饰。

至少提出两个实质不同的候选再选择。候选差异必须体现在构图、镜头关系或证据呈现，而不是只换颜色。

## 镜头契约

每个 scene 写清：

- `visual_mode`：例如真实录屏、结果特写、并列比较、来源文件、过程可视化或环境镜头；允许自由命名。
- `evidence_display`：观众具体能看到哪条 proof。
- `motion_intent`：运动帮助读取什么。
- `change_reason`：为什么在这里发生镜头或构图变化。

不规定固定切镜秒数。变化必须来自新信息、新证据、比较关系、执行状态或必要的阅读停顿。

## 禁止项

- 不维护固定黑板、银河、玻璃卡片、演播室或表格皮肤。
- 不恢复旧模块编号和转场注册表。
- 不让同一张卡片反复换字覆盖整条视频。
- 不把 ImageGen、抽象动画或仿制界面标成事实 proof。
- 不以镜头数、动效数、JSON 数量或评分数字代替人工审片。

## 人工审片

`review/manual_review.json.checks` 必须逐项记录：

- `first_five_seconds`
- `claim_proof_sync`
- `proof_legibility`
- `creative_direction_fit`
- `visual_repetition`
- `narrative_rhythm`
- `caption_readability`
- `subtitle_sync`
- `voice_naturalness`
- `safe_area`
- `safe_area_overlay`
- `cover_text_overlap`
- `black_or_empty_frames`
- `full_contact_sheet`

任一项不是 `passed`，成片不得晋级。审片结论必须来自实际成片和 contact sheet，不得在渲染前预填。
