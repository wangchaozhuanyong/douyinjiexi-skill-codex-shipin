---
name: douyin-video-production-core
description: 为抖音视频提供不参与题材和美术决策的共享生产底座，包括可播放参考视频分析、来源与主张证据绑定、自由导演契约、声音提供商预检、Remotion 总时间轴、可选 HyperFrames 局部素材、公开文字合规、字幕与画面核对、技术质量检查、成片晋级与 SAU 上传保护。仅在专业视频 Skill 明确调用或用户要求检查、验收、打包、发布保护时使用。
---

# Douyin Video Production Core

把本 Skill 当作技术、证据和验收底座，不要让它替上层 Skill 选择题材或固定视觉皮肤。

## 工作边界

- 接受上层 Skill 已确定的内容方向和视觉方案。
- 保证来源真实、主张有证据、音画对应、技术输出可播放、公开文字经过检查。
- 不提供固定背景、固定卡片、固定转场、固定换镜间隔或“高级感”模板。
- 只验证自由导演是否解释了题材、证据和运动之间的关系。
- 不把生成图、仿制界面或装饰动画当成事实证据。
- 不把本地检查写成轻抖或抖音平台已经通过。
- 不自动上传或发布。真实上传必须有用户明确授权，并通过发布保护。

## 六个核心产物

按 `references/artifact_contract.md` 维护：

1. `source_brief.json`
2. `script.json`
3. `storyboard.json`
4. `asset_manifest.json`
5. `qa_report.json`
6. `publish_package.json`

不要恢复旧体系的方案编号、导演选择器、固定皮肤、固定模板、前景模块注册表或复杂工作流门禁链。

## 执行顺序

1. 先读 `references/video_taxonomy.md`，确定一级、二级、三级分类和项目展示名，再选择唯一一个专业 Skill。
2. 有参考视频时，读 `references/reference_and_evidence.md`，取得可播放本体并运行 `scripts/analyze_reference.py`。
3. 读 `references/free_director_contract.md`，把本条视频的独立视觉命题写进 `storyboard.json`，不要选择固定皮肤。
4. 在生产前运行 `scripts/validate_project.py --phase preproduction`，检查分类、前四个产物、自由导演说明和逐句证据绑定。
5. 运行 `scripts/preflight_providers.py`。Remotion 必须拥有最终时间轴；HyperFrames 只在确有必要时输出透明或普通局部视频素材。
6. 按 `references/voice_and_renderer.md` 生成一条连续旁白与字幕时间戳，再用 Remotion 合成。
7. 渲染后运行 `scripts/run_core_qa.py`，生成 `qa_report.json`。
8. 公开文字按 `references/compliance_and_delivery.md` 做本地检查；平台检查必须记录真实可见结果。
9. 只有 QA 通过时才能运行 `scripts/build_publish_package.py`。
10. 只有用户明确授权时才能调用 `scripts/douyin_sau_publish.py --execute`。

## 证据原则

- 旁白提出事实主张时，当前画面立即提供对应证据。
- 每条 `claim_id` 必须绑定一个真实存在的 `proof_id`。
- 真实界面、官方文档、真实操作、真实输出优先。
- 支撑图可以解释抽象概念，但必须标记为 `support`，不能标记为 `proof`。
- 没有可见平台数据时，写 `not_observed`，不要推测播放、完播或转化。

## 必读参考

- 分类、路由与项目命名：`references/video_taxonomy.md`
- 产物字段与阶段：`references/artifact_contract.md`
- 自由导演与审片：`references/free_director_contract.md`
- 参考视频和证据：`references/reference_and_evidence.md`
- 声音与渲染：`references/voice_and_renderer.md`
- 合规、音频和交付：`references/compliance_and_delivery.md`

## 完成检查

```bash
python3 scripts/validate_project.py --project <project> --phase preproduction
python3 scripts/preflight_providers.py --project <project>
python3 scripts/run_core_qa.py --project <project> --video <project>/render/final.mp4
python3 scripts/build_publish_package.py --project <project>
python3 scripts/validate_project.py --project <project> --phase publish
```
