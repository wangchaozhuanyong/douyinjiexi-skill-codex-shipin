# 固定 AI 封面成图轮换规则

本规则用于 AI 知识类视频第一帧和发布封面。当前封面不再每次重新生成，也不从视频中随机截帧；默认使用已经完成本地检查和 Qingdou 检查的 10 张固定安全模板。

## 固定素材

- 素材目录：`assets/ai_cover_templates_fixed/`
- 轮换清单：`references/fixed_ai_cover_template_rotation.json`
- Qingdou 通过记录：`outputs/cover-template-audit-2026-06-20/qingdou/final-passed.json`
- 最终可见文字清单：`references/ai_cover_template_public_text_manifest.txt`

## 选择规则

- 先按视频尺寸选池，不允许 10 张全局随机。
- 16:9 / 1920x1080 / 证明型 AI 视频：使用 `horizontal_16x9`，顺序为 H01 -> H02 -> H03 -> H04 -> H05 -> H01。
- 9:16 / 1080x1920 / 轻量信息海报视频：使用 `vertical_9x16`，顺序为 V01 -> V02 -> V03 -> V04 -> V05 -> V01。
- 每次选择后必须记录 `template_id`、`template_rotation_index`、`selection_method=sequential_by_size_pool`、`template_path`、`template_aspect` 和 `state_file`。
- 轮换状态默认写入 `outputs/.ai_cover_template_rotation_state.json`；单测或 golden 检查可传入项目内临时 state，避免污染真实轮换状态。

## 第一帧要求

- 选中的模板必须作为视频 timeline 的 scene 0 / 第一帧封面使用。
- 第一帧封面的默认目的只是让抖音抓取发布封面，不是给观众看的长开场；默认只能覆盖第 0 帧，30fps 时约 `0.033s`。除非用户明确要求封面开场，否则不得做 0.5 秒、1 秒或更长的静态封面停留。
- 如果 HyperFrames/Remotion 时间线难以精确做到单帧封面，允许在最终成片后用 FFmpeg 后处理把 `internal/first_frame_cover.png` 只 overlay 到 `eq(n,0)`，不得插入静音段、不得延长总时长、不得移动原口播。
- 同一个文件也必须写成发布封面来源：`internal/cover.png`。
- 同步输出 `internal/first_frame_cover.png`，供 HyperFrames/Remotion 在渲染时放到最前面。
- `metadata.quality_spec` 必须记录 `first_frame_cover_overlay_frames=1` 和约 `first_frame_cover_overlay_sec=0.033`，或等价字段；如果用户明确要求长封面开场，必须记录用户批准原因。
- 最终 QA 必须抽取并保存至少两张证据图：`internal/actual_frame_000_cover.png` 必须是封面，`internal/actual_frame_001_after_cover.png` 必须已经回到视频正文/原时间线。没有这两个证据，不得声称第一帧封面已正确接入。
- 不允许用随机视频帧、旧玻璃卡片预览图或临时截图替代发布封面。

## 合规要求

- 默认使用固定模板内已经通过 Qingdou 的文字，不额外叠加当期动态标题。
- 如果当期必须改封面文字，必须先写 `internal/publish_cover_text.txt`，再和标题、发布文案、话题一起重新做本地合规和 Qingdou 检查；未通过前不得渲染、推广或发布。
- `publish_cover_report.json` 必须证明 `frame_grab_used=false`、`template_from_fixed_library=true`、`fixed_safe_asset=true`、`cover_text_written=true`。

## 推荐命令

```bash
python3 scripts/select_fixed_cover_template.py \
  --project outputs/demo \
  --video-width 1920 \
  --video-height 1080
```
