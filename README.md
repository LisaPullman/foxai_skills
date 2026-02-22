# FoxAI Skills

歪爪的 AI 技能集合，包含自建和系统内置的 Skills。

## 📊 统计概览

| 分类 | 数量 | 说明 |
|------|------|------|
| **自建 Skills** | 4 | foxai_skills 仓库 |
| **系统 Skills** | 53 | OpenClaw 内置 |
| **总计** | **57** | 全部 Skills |

---

## 📦 自建 Skills (4)

来自 [foxai_skills](https://github.com/LisaPullman/foxai_skills) 仓库

### 🎨 AI 图像 (1)

| Skill | 功能 |
|-------|------|
| pic-foxai-image-generator | FoxAI 文生图 |

### 🎬 AI 视频 (2)

| Skill | 功能 |
|-------|------|
| tutor | 数学讲解视频（Manim + Edge TTS） |
| remotion | React 视频生成 |

### 📺 设备控制 (1)

| Skill | 功能 |
|-------|------|
| dlna | DLNA/UPnP 投屏控制 |

---

## ⚙️ 系统 Skills (53)

OpenClaw 内置技能

### 🔐 安全 (1)

| Skill | 功能 |
|-------|------|
| healthcheck | 主机安全加固 |

### 💻 开发 (4)

| Skill | 功能 |
|-------|------|
| coding-agent | 代码开发代理 |
| skill-creator | 技能创建 |
| github | GitHub 操作 |
| gh-issues | GitHub Issues |

### 📱 消息 (4)

| Skill | 功能 |
|-------|------|
| discord | Discord 消息 |
| slack | Slack 消息 |
| whatsapp | WhatsApp 消息 |
| telegram | Telegram 消息 |

### ☁️ 云服务 (4)

| Skill | 功能 |
|-------|------|
| notion | Notion 笔记 |
| obsidian | Obsidian 笔记 |
| apple-notes | Apple Notes |
| bear-notes | Bear Notes |

### 🎵 媒体 (6)

| Skill | 功能 |
|-------|------|
| video-frames | 视频帧提取 |
| spotify-player | Spotify 控制 |
| songsee | 音乐搜索 |
| sonoscli | Sonos 音响 |
| sag | 语音合成 |
| sherpa-onnx-tts | 本地 TTS |

### 🌤️ 生活 (1)

| Skill | 功能 |
|-------|------|
| weather | 天气查询 |

### 🔧 工具 (33)

其他工具技能：apple-reminders, bear-notes, blogwatcher, blucli, bluebubbles, camsnap, canvas, clawhub, eightctl, food-order, gemini, gifgrep, gog, goplaces, himalaya, imsg, mcporter, model-usage, nano-banana-pro, nano-pdf, openai-image-gen, openai-whisper, openai-whisper-api, openhue, oracle, ordercli, peekaboo, session-logs, slack, summarize, things-mac, tmux, trello, voice-call, wacli, xurl

---

## 🚀 快速开始

### 安装自建 Skill

```bash
# 克隆仓库
git clone https://github.com/LisaPullman/foxai_skills.git

# 复制到 OpenClaw skills 目录
cp -r foxai_skills/* ~/.openclaw/skills/
```

### 使用示例

```bash
# 生成图片
foxai_generator.cjs "cute cat" --count 1

# 查询天气
weather 苏州

# 安全检查
healthcheck
```

---

## 📝 贡献指南

欢迎提交自建 Skills！请确保：
1. 包含 `SKILL.md` 文档
2. 包含使用示例
3. 不包含大型媒体文件

---

## License

MIT
