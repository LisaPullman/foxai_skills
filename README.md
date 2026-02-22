# FoxAI Skills

歪爪的 AI 技能集合，包含自建和社区贡献的 Skills。

## 📊 统计概览

| 分类 | 数量 | 说明 |
|------|------|------|
| **AI 图像** | 1 | AI 图片生成 |
| **AI 视频** | 2 | Manim 动画 / React 视频 |
| **设备控制** | 1 | DLNA 投屏 |
| **系统工具** | - | OpenClaw 内置 |
| **总计** | **4** | 自建 Skills |

---

## 🎨 AI 图像 (1)

| Skill | 功能 | 来源 |
|-------|------|------|
| pic-foxai-image-generator | FoxAI 文生图 | 自建 |

---

## 🎬 AI 视频 (2)

| Skill | 功能 | 来源 |
|-------|------|------|
| tutor | 数学讲解视频（Manim + Edge TTS） | 自建 |
| remotion | React 视频生成 | 社区 |

---

## 📺 设备控制 (1)

| Skill | 功能 | 来源 |
|-------|------|------|
| dlna | DLNA/UPnP 投屏控制 | 社区 |

---

## 🚀 快速开始

### 安装 Skill

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

# 生成数学视频
cd tutor
python scripts/generate_tts.py audio_list.csv ./audio
manim -qh -p script.py MathScene
```

---

## 📝 贡献指南

欢迎提交 PR！请确保：
1. 包含 `SKILL.md` 文档
2. 包含使用示例
3. 不包含大型媒体文件

---

## License

MIT
