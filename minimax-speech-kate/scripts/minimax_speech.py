#!/usr/bin/env python3
"""
MiniMax Speech Generator - 使用 speech-2.8-hd 模型生成中文语音
支持多角色音频合成、语气词标记、发音词典、自动发送到当前窗口

用法:
    # 单段语音（添加 --send 自动生成并发送到当前窗口）
    python minimax_speech.py --text "要合成的文本" --voice male-qn-jingying --output output.mp3 --send
    
    # 带语气词的语音
    python minimax_speech.py --text "真的吗？(gasps) 太棒了(laughs)！" --voice female-yujie --output output.mp3 --send
    
    # 多角色合成（通过 JSON 文件，添加 --send 自动发送）
    python minimax_speech.py --multi roles.json --output story.mp3 --send
    
    # JSON 格式示例:
    # [
    #   {"role": "旁白", "voice": "male-qn-jingying", "text": "从前有一座山..."},
    #   {"role": "小明", "voice": "clever_boy", "text": "我要去探险(laughs)！"},
    #   {"role": "小红", "voice": "female-shaonv", "text": "我也要去！", 
    #    "pronunciation_dict": {"tone": ["探险/adventure"]}}
    # ]
"""

import argparse
import os
import sys
import json
import requests
import subprocess
import tempfile
import shutil


def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_api_key(api_key_arg=None):
    """获取 API Key，优先级：参数 > 环境变量 > 配置文件"""
    if api_key_arg:
        return api_key_arg
    
    env_key = os.environ.get("MINIMAX_API_KEY")
    if env_key:
        return env_key
    
    config = load_config()
    if config.get("api_key"):
        return config["api_key"]
    
    return None


def generate_speech(text: str, voice_id: str, output_path: str = "output.mp3", api_key: str = None,
                   pronunciation_dict: dict = None, voice_modify: dict = None, audio_setting: dict = None):
    """
    调用 MiniMax speech-2.8-hd 模型生成语音
    
    支持语气词标记：(sighs), (laughs), (coughs), (gasps), (clears throat), (sneezes), (applause)
    
    Args:
        text: 要合成的文本（支持语气词标记）
        voice_id: 音色ID
        output_path: 输出文件路径
        api_key: MiniMax API Key（如不提供则从环境变量或配置文件读取）
        pronunciation_dict: 发音词典配置，如 {"tone": ["危险/dangerous"]}
        voice_modify: 声音修饰配置，如 {"pitch": 0, "intensity": 0, "timbre": 0, "sound_effects": "spacious_echo"}
        audio_setting: 音频设置配置，如 {"audio_sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 2}
    
    Returns:
        生成的音频文件路径，音频时长（秒）
    """
    api_key = get_api_key(api_key)
    if not api_key:
        raise ValueError("请提供 API Key、设置 MINIMAX_API_KEY 环境变量，或在 config.json 中配置")
    
    # MiniMax API 端点
    url = "https://api.minimaxi.com/v1/t2a_v2"
    
    # 请求体
    payload = {
        "model": "speech-2.8-hd",
        "text": text,
        "language_boost": "auto",
        "voice_setting": {
            "voice_id": voice_id,
            "speed": 1.0,
            "vol": 1.0,
            "pitch": 0
        },
        "audio_setting": audio_setting or {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1
        }
    }
    
    # 添加发音词典（如果提供）
    if pronunciation_dict:
        payload["pronunciation_dict"] = pronunciation_dict
    
    # 添加声音修饰（如果提供）
    if voice_modify:
        payload["voice_modify"] = voice_modify
    
    # 请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 发送请求
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    
    if response.status_code != 200:
        raise RuntimeError(f"API 请求失败: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # 检查响应
    if data.get("base_resp", {}).get("status_code") != 0:
        error_msg = data.get("base_resp", {}).get("status_msg", "未知错误")
        raise RuntimeError(f"MiniMax API 错误: {error_msg}")
    
    # 解码音频数据
    audio_hex = data.get("data", {}).get("audio")
    if not audio_hex:
        raise RuntimeError("响应中未找到音频数据")
    
    # 保存音频文件
    audio_bytes = bytes.fromhex(audio_hex)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    
    # 获取音频信息
    audio_info = data.get("data", {})
    duration = audio_info.get("audio_duration", 0)
    
    return output_path, duration


def merge_audio_files(audio_files: list, output_path: str):
    """
    使用 ffmpeg 合并多个音频文件
    
    Args:
        audio_files: 音频文件路径列表
        output_path: 输出文件路径
    """
    if not audio_files:
        raise ValueError("音频文件列表不能为空")
    
    if len(audio_files) == 1:
        # 只有一个文件，直接复制
        shutil.copy(audio_files[0], output_path)
        return output_path
    
    # 创建临时文件列表
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        list_file = f.name
        for audio_file in audio_files:
            f.write(f"file '{os.path.abspath(audio_file)}'\n")
    
    try:
        # 使用 ffmpeg 合并
        cmd = [
            "ffmpeg",
            "-y",  # 覆盖输出文件
            "-f", "concat",
            "-safe", "0",
            "-i", list_file,
            "-acodec", "libmp3lame",
            "-q:a", "2",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg 合并失败: {result.stderr}")
        
        print(f"✅ 音频合并成功: {output_path}")
        return output_path
        
    finally:
        # 清理临时文件
        os.unlink(list_file)


def generate_multi_role_audio(json_file: str, output_path: str = "output.mp3", api_key: str = None):
    """
    根据 JSON 文件生成多角色音频并合并
    
    Args:
        json_file: 包含多角色信息的 JSON 文件路径
        output_path: 最终输出文件路径
        api_key: MiniMax API Key
    
    JSON 格式:
    [
        {
            "role": "旁白", 
            "voice": "male-qn-jingying", 
            "text": "从前有一座山...",
            "pronunciation_dict": {"tone": ["危险/dangerous"]},
            "voice_modify": {"sound_effects": "spacious_echo"}
        },
        {
            "role": "小明", 
            "voice": "clever_boy", 
            "text": "我要去探险(laughs)！"
        }
    ]
    
    支持语气词标记：
    - (sighs) - 叹息
    - (laughs) - 笑声
    - (coughs) - 咳嗽
    - (gasps) - 倒吸气
    - (clears throat) - 清嗓子
    - (sneezes) - 打喷嚏
    - (applause) - 掌声
    """
    # 读取 JSON
    with open(json_file, "r", encoding="utf-8") as f:
        segments = json.load(f)
    
    if not isinstance(segments, list):
        raise ValueError("JSON 文件必须是数组格式")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    audio_files = []
    
    try:
        print(f"🎙️ 开始生成多角色音频，共 {len(segments)} 段...\n")
        
        for i, segment in enumerate(segments):
            role = segment.get("role", "未知")
            voice = segment.get("voice", "male-qn-jingying")
            text = segment.get("text", "")
            pronunciation_dict = segment.get("pronunciation_dict")
            voice_modify = segment.get("voice_modify")
            audio_setting = segment.get("audio_setting")
            
            if not text:
                print(f"⚠️  跳过第 {i+1} 段（文本为空）")
                continue
            
            # 生成临时音频文件
            temp_audio = os.path.join(temp_dir, f"segment_{i:03d}.mp3")
            
            print(f"[{i+1}/{len(segments)}] {role} ({voice}): {text[:30]}...")
            
            try:
                audio_path, duration = generate_speech(
                    text, voice, temp_audio, api_key,
                    pronunciation_dict=pronunciation_dict,
                    voice_modify=voice_modify,
                    audio_setting=audio_setting
                )
                audio_files.append(audio_path)
                print(f"      ✅ 时长: {duration}秒\n")
            except Exception as e:
                print(f"      ❌ 生成失败: {e}\n")
                continue
        
        if not audio_files:
            raise RuntimeError("没有成功生成任何音频段")
        
        # 合并音频
        print(f"🔄 正在合并 {len(audio_files)} 个音频片段...")
        merge_audio_files(audio_files, output_path)
        
        print(f"\n✅ 多角色音频生成完成!")
        print(f"   文件: {output_path}")
        
        return output_path
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir, ignore_errors=True)


def print_send_instructions(file_path: str):
    """
    输出发送文件的指示
    由于脚本无法直接调用 OpenClaw 的 message 工具，这里输出文件路径和提示
    """
    abs_path = os.path.abspath(file_path)
    print(f"\n📤 音频文件已生成: {abs_path}")
    print(f"\n💡 发送到当前窗口的方法:")
    print(f"   方式1: 请将此文件手动发送给 OpenClaw")
    print(f"   方式2: 对 OpenClaw 说 '把刚才生成的音频发给我'")
    print(f"\n📝 文件路径: {abs_path}")


def main():
    # 加载配置获取默认值
    config = load_config()
    default_voice = config.get("default_voice", "male-qn-jingying")
    
    parser = argparse.ArgumentParser(description="MiniMax 中文语音合成工具")
    parser.add_argument("--text", "-t", help="要合成的文本")
    parser.add_argument("--file", "-f", help="包含文本的文件路径")
    parser.add_argument("--voice", "-v", default=default_voice, help=f"音色ID (默认: {default_voice})")
    parser.add_argument("--output", "-o", default="output.mp3", help="输出文件路径 (默认: output.mp3)")
    parser.add_argument("--api-key", help="MiniMax API Key（可选，优先使用 config.json 或环境变量）")
    parser.add_argument("--multi", "-m", help="多角色 JSON 文件路径")
    parser.add_argument("--send", "-s", action="store_true", help="生成后自动发送到当前窗口")
    
    args = parser.parse_args()
    
    # 多角色模式
    if args.multi:
        try:
            output_path = generate_multi_role_audio(args.multi, args.output, args.api_key)
            # 如果指定了 --send，输出发送指示
            if args.send:
                print_send_instructions(output_path)
        except Exception as e:
            print(f"❌ 错误: {e}")
            sys.exit(1)
        return
    
    # 单段语音模式
    # 获取文本
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        print("错误: 请提供 --text、--file 或 --multi 参数")
        parser.print_help()
        sys.exit(1)
    
    # 生成语音
    try:
        output_path, duration = generate_speech(text, args.voice, args.output, args.api_key)
        # 如果指定了 --send，输出发送指示
        if args.send:
            print_send_instructions(output_path)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
