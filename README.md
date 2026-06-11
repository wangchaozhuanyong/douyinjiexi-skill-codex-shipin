# 抖音全能解析

本项目是一个本地桌面版抖音解析工具，支持从抖音分享文本或链接中解析可下载资源，并按需要下载 MP3、视频或图片。项目也包含用于短视频原创重做流程的 TTS 配置能力。

> 仅用于下载、处理你拥有版权、获得授权或依法允许使用的内容。请遵守平台规则和版权要求。

## 功能

- 本地桌面软件界面，默认只在本机运行。
- 支持粘贴抖音分享文本或链接解析资源。
- 支持 MP3、视频、图片资源按需下载。
- 保存路径会记住用户上次设置。
- 解析记录保留最近 20 条，方便复制旧链接。
- 支持 macOS 打包成 `.app`。
- 支持 `edge-tts` 免费中文神经语音，用于视频重做配音流程。

## 环境要求

- macOS
- Python 3.9+
- 网络可访问抖音和相关媒体资源

## 安装依赖

```bash
python3 -m venv .douyin-mp3-venv
.douyin-mp3-venv/bin/python -m pip install --upgrade pip
.douyin-mp3-venv/bin/python -m pip install -r requirements.txt
```

## 本地运行

网页版本：

```bash
.douyin-mp3-venv/bin/python douyin_media_server.py
```

桌面 WebView 版本：

```bash
.douyin-mp3-venv/bin/python douyin_media_webview.py
```

命令行提取 MP3：

```bash
.douyin-mp3-venv/bin/python douyin_to_mp3.py "抖音分享文本或链接"
```

## 打包 macOS 桌面 App

```bash
./build_desktop_app.sh
```

打包完成后会生成：

```text
~/Desktop/抖音全能解析.app
```

## TTS 配置

复制 `.env.example` 为 `.env` 后可以配置 TTS。免费方案推荐：

```bash
TTS_PROVIDER=edge_tts
EDGE_TTS_VOICE=zh-CN-YunxiNeural
EDGE_TTS_RATE=+0%
EDGE_TTS_VOLUME=+0%
EDGE_TTS_PITCH=+0Hz
```

更多说明见 `docs/TTS_PROVIDERS.md`。

## 不上传的内容

仓库不会上传以下本地文件：

- `.env` 私人配置
- 虚拟环境 `.douyin-mp3-venv/`
- 打包产物 `build/`、`dist/`
- 下载内容 `mp3/`、`导出/`
- 视频生成素材和成品 `hyperframes-remakes/`
- 日志、缓存、测试输出
