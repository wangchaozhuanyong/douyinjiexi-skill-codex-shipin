# 六产物契约

项目目录只使用六个核心 JSON。允许存在渲染文件、截图、contact sheet 和临时技术报告，但不能要求几十个创作前置报告才能开始。

## 1. source_brief.json

必填：

- `format_type`: `tool_explainer`、`news_explainer` 或 `list_video`
- `project_name`: 符合 `references/video_taxonomy.md` 的规范中文展示名
- `classification`: `level_1`、`level_2`、`level_3`、`category_code`
- `topic`
- `captured_at`
- `sources[]`: `id`、`title`、`source_type`、`locator`、`captured_at`、`supports_claims[]`
- `claims[]`: `id`、`text`、`fact_status`、`source_ids[]`

`fact_status` 只能是 `confirmed`、`inference` 或 `unknown`。

`classification.level_1` 固定为 `AI类视频`。`level_2` 和 `category_code` 必须与 `format_type` 对应；`level_3` 根据具体选题填写。项目文件夹可使用英文 slug，但不能替代 `project_name`。

新闻类还必须记录：

- `published_at`：原始公告或报道的发布日期
- `event_date`：事件实际发生日期；未知时明确写 `unknown`
- `verification_cutoff`：最后核验时间
- `official_channels_checked[]`：为“官方尚未确认”等否定性判断保存核验范围
- `claims[].claim_kind`：`event`、`report_existence`、`reported_fact`、`absence_check`、`analysis` 或 `advice`

`reported` 新闻必须把“媒体确实做过该报道”和“报道中的事实是否成立”拆成两个 claim。任何否定性主张都增加 `negative_assertion: true`、`verification_method` 和 `verification_cutoff`，不能把“没看到”写成“不存在”。

参考视频存在时增加 `reference_video.playable_path`、`sha256`、`duration`、`width`、`height`、`fps`、`has_audio`。只有 URL 或标题时不得标记为已分析。

工具类还必须增加 `topic_selection`：

- `mode`: `user_fixed` 或 `research_selected`
- `interaction_mode`: `step_by_step` 或 `autonomous`
- `material_scan_completed`: 必须为 `true`
- `selection_basis`
- `proof_readiness`: 进入制作时必须为 `passed`
- `confirmation_status`: `user_confirmed` 或 `not_requested`
- `selected_candidate_id`: 研究候选选题时必填

`step_by_step` 必须记录 `user_confirmed`。没有真实输入、执行和结果 proof 时不得把 `proof_readiness` 写成通过。

## 2. script.json

通用必填：

- `format_type`
- `title`
- `hook`
- `beats[]`: `id`、`narration`、`claim_ids[]`、`proof_ids[]`
- `closing_takeaway`

类型字段：

- 工具：`viewer_task`、`input_method`、`execution_process`、`visible_result`、`before_after`、`safety_constraints[]`、`privacy_redactions[]`、`result_acceptance[]`、`risk_review`
- 新闻：`event`、`event_status`、`what_changed`、`affected_audience`、`next_step`
- 清单：`list_type`、`selection_scope`、`ranking_basis`、`comparison_dimensions[]`、`items[]`、`order_is_ranked`、`methodology`

新闻 `event_status` 只能是 `released`、`announced`、`preview`、`rolling_out` 或 `reported`。

清单 `list_type` 只能是 `recommendation_list`、`comparison_list`、`ranked_list` 或 `hot_rank`。`items[]` 至少有 `id`、`name`、`task`、`reason`、`proof_ids[]`、`source_ids[]`；排名类每项再记录 `rank`、`score_inputs`。`hot_rank` 必须增加 `time_window`、`timezone` 和 `tie_breaker`。推荐与对比清单必须明确 `order_is_ranked: false`，避免编号暗示客观名次。

工具类安全约束必须进入结构化字段。声称“未删除、未移动、可编辑”等结果时，在 `result_acceptance[]` 写出实际验收动作；否定性结果用前后清单、路径和必要时哈希证明。

工具类还必须在生成完整旁白前记录：

- `beginner_review`: `status`、`task`、`input`、`process`、`result`、`old_method_difference`、`read_aloud_passed`
- `voice_lock`: `status`、`provider`、`voice_id`、`persona`、`rate`、`pitch`、`confirmation_source`

`beginner_review.status` 必须为 `passed`，`read_aloud_passed` 必须为 `true`。`voice_lock.status` 必须为 `locked`。声音改变后必须重新生成旁白、字幕时间和依赖时长的分镜。

发布文字 `publish.title`、`publish.caption`、`publish.topics[]` 与脚本同阶段定稿。

`risk_review` 必填：

- `level`: `low`、`medium` 或 `high`
- `sensitive_domains[]`
- `demo_environment`: `sanitized_local`、`test_sandbox`、`simulated_data`、`pre_recorded_redacted` 或 `real_environment`
- `real_action_policy`: `not_applicable`、`read_only` 或 `blocked`
- `stop_conditions[]`

涉及 `credentials`、`otp`、`financial_account`、`financial_transaction`、`government_id`、`medical_private`、`legal_privileged`、`api_key` 或 `secrets` 时必须是 `high`，真实动作必须为 `blocked`，且只能使用 `test_sandbox`、`simulated_data` 或 `pre_recorded_redacted`。任务和旁白会自动推断这些领域，未知值或漏报都会阻塞。

高风险再增加：

- `blocked_actions[]`：明确列出不得执行的真实动作
- `visible_disclosure`：成片必须原样出现的边界说明
- `boundary_proof_ids[]`：证明沙箱、模拟或脱敏状态的 proof

边界说明必须进入旁白或 storyboard 字幕，证据 ID 必须同时存在于 storyboard 和 proof 资产。渲染后人工审查必须标记 `checks.high_risk_boundary: passed`。遮挡敏感画面不能替代执行前停止。

## 3. storyboard.json

必填：

- `format_type`
- `width`、`height`、`fps`
- `creative_direction`: `visual_thesis`、`reason_for_topic`、`evidence_strategy`、`motion_logic`、`continuity_devices[]`、`rejected_defaults[]`
- `render_plan`: `canonical_renderer`、`composition_id`、`optional_subrenderers[]`
- `safe_area`: `top`、`left`、`right`、`bottom`、`caption_bottom`；允许放在顶层或 `design_system` 内
- `scenes[]`: `id`、`start`、`end`、`beat_ids[]`、`claim_ids[]`、`proof_ids[]`、`visual_mode`、`visual`、`evidence_display`、`motion_intent`、`change_reason`、`caption`

每个核心 claim 必须在同一场景绑定 proof。`visual` 必须描述可见对象和信息任务，不能只写“高级、科技、炫酷”。

`canonical_renderer` 固定为 `remotion`，用于统一时间轴、声音、字幕和最终输出。`optional_subrenderers[]` 只能记录局部素材工具；使用 HyperFrames 时必须说明输出文件及它解决的局部问题，不能把两套渲染器同时当作最终时间轴。

`creative_direction` 不规定皮肤。它只证明本条视频的构图、证据、运动和题材之间存在明确关系。`rejected_defaults[]` 记录本次主动放弃的惯性方案，防止同一模板换字。

1080×1920 抖音竖屏默认至少预留上 120、左 84、右 180、下 360 px，字幕基线离底部至少 380 px；其他分辨率按比例缩放。关键文字和 proof 标签不得越界。

## 4. asset_manifest.json

`assets[]` 必填：`id`、`role`、`source_kind`、`path`、`source_locator`、`supports_claims[]`。承担 proof 的资产还必须有 `captured_at`。

- `role`: `proof`、`support`、`audio`、`cover`
- `source_kind`: `real_capture`、`official_source`、`user_provided`、`generated_support`、`licensed_media`

只有前三种可以承担事实 proof；`generated_support` 只能解释。

## 5. qa_report.json

由 core QA 生成，至少包括：

- `status`
- `content_mapping`
- `technical`
- `audio`
- `frames`
- `public_text`
- `blocking_issues[]`
- `warnings[]`

人工审片同时记录：前五秒、claim-proof 同步、proof 可读性、导演方向适配、视觉重复度、节奏、字幕同步、声音自然度、安全区、安全区覆盖层、封面文字重叠和完整 contact sheet。

## 6. publish_package.json

QA 通过后生成：

- `gate.status`
- `video`
- `cover`
- `title`
- `caption`
- `topics[]`
- `qa_report`
- `text_check`
- `platform_check`
- `input_fingerprints`

真实上传只读取此文件。`platform_check.status` 不是可见通过结果时不得执行上传。
