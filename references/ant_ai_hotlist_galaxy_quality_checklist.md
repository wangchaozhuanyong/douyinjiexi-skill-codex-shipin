# 蚂蚁AI 热榜银河模板验收清单

每次制作 `ant_ai_hotlist_extended` 视频前，先用这份清单检查模板；每次导出 final 前，再用项目 QA 和 workflow guard 检查成片。

## 视觉验收

- [ ] 输出画幅是 `1080x1920`。
- [ ] 背景底板稳定，没有整图缩放、推近、左右漂移。
- [ ] 银河盘在中部偏上偏右，内部纹理慢速旋转。
- [ ] 银河盘有椭圆透视、倾斜角和羽化边缘。
- [ ] 背景有真实星云质感、暗角、细颗粒、冷暖光和景深。
- [ ] 星尘微闪克制，流星低频，不像网页粒子 demo。
- [ ] 中心阅读区压暗是局部的，不是黑色实心遮罩。

## 玻璃卡片验收

- [ ] 主卡片 alpha 在 `0.24-0.34` 范围内。
- [ ] 默认主卡片 alpha 是 `0.26` 左右。
- [ ] 背景能透过卡片看到。
- [ ] 文字清楚，靠文字阴影和局部 dim 提升可读性。
- [ ] 没有 `rgba(0,0,0,0.7)`、厚黑板、白板或不透明大卡片。

## 文案与信息验收

- [ ] 方案是 `scheme_7_ai_hot_rank_top5`。
- [ ] 变体是 `ant_ai_hotlist_extended`。
- [ ] `internal/ai_hot_rank_top5.json` 正好五条。
- [ ] 每条都有来源、可见日期、评分、`score_breakdown` 和 `viewer_action`。
- [ ] 文案按“具体对象 -> 来源日期 -> 为什么现在重要 -> 用户动作”组织。
- [ ] CTA 是 `关注 蚂蚁AI`。
- [ ] 没有复制 `AI研究所` 账号身份或参考视频原文。

## 音频验收

- [ ] 人声使用固定模板男声：`VOICE_MALE_THICK_YUNYANG_V1` / `zh-CN-YunyangNeural`。
- [ ] 如果使用 BGM，来源是记录过的同平台参考音乐或用户音乐库。
- [ ] 不生成、不仿制、不替换相似 BGM。
- [ ] BGM duck 在人声下面，不能压人声。

## 预览与导出验收

- [ ] 已打开 `templates/ant_ai_hotlist_galaxy/preview.html` 检查动态预览。
- [ ] 已调过卡片透明度，背景仍可见。
- [ ] 已检查封面帧。
- [ ] 导出前运行 `python3 scripts/check_ant_ai_galaxy_template.py`。
- [ ] 成片发布前运行完整方案7 workflow guard、cover、Qingdou 和 publish contract。

## 失败即返工

以下任一项出现，不能称为发布级：

- 整张背景在缩放或推拉。
- 卡片像黑板，背景看不到。
- 银河只是贴纸，没有羽化和景深。
- 画面像低质粒子 demo。
- 只有 MP4，没有预览、质检和发布证据。
- TOP5 内容没有真实来源。
