#!/usr/bin/env python3
"""
Tutor Skill - 一键生成视频
自动完成：数学分析 → HTML → 分镜 → TTS → 视频渲染

用法：
    python generate_video.py --title "割圆术" --script script.py --audio-dir audio
"""

import argparse
import os
import subprocess
import shutil
import json
from pathlib import Path

# 颜色
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def log(msg, color=GREEN):
    print(f"{color}{msg}{RESET}")

def run_cmd(cmd, cwd=None):
    """运行命令"""
    log(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        log(f"错误: {result.stderr}", RED)
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Tutor视频一键生成")
    parser.add_argument("--title", "-t", required=True, help="视频标题")
    parser.add_argument("--script", "-s", required=True, help="Manim脚本路径")
    parser.add_argument("--audio-dir", default="audio", help="音频目录")
    parser.add_argument("--quality", "-q", default="h", choices=["l", "m", "h", "p"], help="渲染质量")
    parser.add_argument("--output", "-o", default="/tmp", help="输出目录")
    
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, args.script)
    audio_dir = os.path.join(script_dir, args.audio_dir)
    
    # 检查文件
    log("📋 检查文件...")
    if not os.path.exists(script_path):
        log(f"脚本不存在: {script_path}", RED)
        return
    if not os.path.exists(audio_dir):
        log(f"音频目录不存在: {audio_dir}", RED)
        return
    
    # 检查音频
    audio_info_file = os.path.join(audio_dir, "audio_info.json")
    if os.path.exists(audio_info_file):
        with open(audio_info_file) as f:
            info = json.load(f)
            log(f"✅ 找到 {len(info['files'])} 个音频文件")
    
    # 渲染视频
    log("🎬 开始渲染视频...")
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    
    # 构建命令
    cmd = f"manim -q{args.quality} -p {script_path} MathScene"
    log(f"运行: {cmd}")
    
    result = subprocess.run(cmd, shell=True, cwd=script_dir, capture_output=True, text=True)
    
    if result.returncode != 0:
        log(f"渲染失败: {result.stderr}", RED)
        return
    
    # 查找生成的文件
    media_dir = os.path.join(script_dir, "media", "videos")
    video_file = None
    
    for root, dirs, files in os.walk(media_dir):
        for f in files:
            if f.endswith(".mp4") and "MathScene" in f:
                video_file = os.path.join(root, f)
                break
    
    if not video_file:
        log("未找到视频文件", RED)
        return
    
    # 复制到输出目录
    output_file = os.path.join(output_dir, f"{args.title}.mp4")
    shutil.copy(video_file, output_file)
    
    log(f"✅ 视频生成完成: {output_file}")
    log(f"📤 文件大小: {os.path.getsize(output_file) / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    main()
