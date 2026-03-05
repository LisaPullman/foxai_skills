# Tutor Skill 优化说明

## 已完成的优化

### 1. 一键生成视频脚本
```bash
# 使用
python scripts/generate_video.py --title "割圆术" --script script.py --audio-dir audio
```

### 2. 修复版模板
- 解决 Manim 版本兼容问题（Table 类）
- 内置 `play_scene()` 解决语音重叠
- 添加常用工具函数

### 3. 文件管理
- 按项目分开（audio/、media/）
- 输出到 /tmp 方便发送

---

## 快速开始

### 1. 准备分镜脚本
创建 `分镜.md`，包含：
- 幕结构
- 读白内容
- 画面描述

### 2. 生成音频
```bash
# 创建 CSV 文件
filename,text
audio_001_开场.wav,"开场白内容"
...

# 生成音频
python scripts/generate_tts.py audio_list.csv ./audio --voice xiaoxiao
```

### 3. 创建视频脚本
复制 `templates/script_template_fixed.py` 为 `script.py`

### 4. 渲染视频
```bash
# 方式1: 直接运行
manim -qh -p script.py MathScene

# 方式2: 一键生成
python scripts/generate_video.py --title "视频标题" --script script.py
```

### 5. 发送视频
视频自动保存到 `/tmp/{标题}.mp4`，可直接发送

---

## 常见问题

### Q: 语音重叠
A: 使用 `self.play_scene(幕号, 动画, run_time=秒数)` 确保音频播放完毕

### Q: Manim 报错
A: 确保已安装 LaTeX: `apt-get install texlive-latex-base`

### Q: 表格显示异常
A: 使用 `create_table()` 函数，自动降级兼容

### Q: 渲染太慢
A: 使用 `-ql` 低质量预览，确定无误后用 `-qh` 高质量导出
