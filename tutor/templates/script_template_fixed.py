"""
数学教学视频模板 - 修复版
解决 Manim 版本兼容性问题

使用说明：
1. 复制此文件为 script.py
2. 修改 SCENES 中的音频时长（从 audio_info.json 获取）
3. 修改 construct() 中的动画内容
4. 运行: manim -qh -p script.py MathScene
"""

from manim import *
import json
import os
import numpy as np

class MathScene(Scene):
    # ==================== 配置 ====================
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    # 颜色主题
    COLORS = {
        'background': '#1a1a2e',
        'primary': '#4ecca3',      # 青色
        'secondary': '#e94560',    # 红色
        'highlight': '#ffc107',    # 黄色
        'text': '#ffffff',
    }

    # ==================== 幕信息 ====================
    # 必须从 audio_info.json 获取准确时长
    SCENES = {
        1: {"name": "开场", "audio": "audio_001_开场.wav", "duration": 5.0},
        2: {"name": "讲解", "audio": "audio_002_讲解.wav", "duration": 10.0},
        # 添加更多幕...
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_dir = "audio"

    # ==================== 音频同步 ====================
    def play_scene(self, scene_num, *animations, **kwargs):
        """
        播放一幕，自动等待音频结束
        解决语音重叠问题
        """
        if scene_num not in self.SCENES:
            log.warning(f"未知幕号: {scene_num}")
            if animations:
                self.play(*animations, **kwargs)
            return

        scene_info = self.SCENES[scene_num]
        audio_duration = scene_info["duration"]
        
        # 添加音频
        audio_file = scene_info["audio"]
        audio_path = os.path.join(self.audio_dir, audio_file)
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
        
        # 播放动画
        if animations:
            self.play(*animations, **kwargs)
        
        # 等待音频结束
        run_time = kwargs.get("run_time", 1)
        wait_time = max(0, audio_duration - run_time)
        self.wait(wait_time + 0.3)  # 留0.3秒缓冲

    # ==================== 几何计算 ====================
    def calculate_geometry(self):
        """
        计算几何元素（可重写）
        返回: dict 包含 points, lines, circles, polygons
        """
        return {
            'points': {},
            'lines': {},
            'circles': {},
            'polygons': {},
        }

    def assert_geometry(self, geometry):
        """验证几何正确性"""
        # 画布范围检查
        for key, data in geometry.get('points', {}).items():
            x, y = data
            assert -7 <= x <= 7, f"{key} x超出范围: {x}"
            assert -6 <= y <= 6, f"{key} y超出范围: {y}"

    # ==================== 工具函数 ====================
    def create_axes(self, x_range=(-1, 10), y_range=(-5, 5)):
        """创建坐标轴"""
        return Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=12,
            y_length=8,
            axis_config={
                "include_tip": True,
                "numbers_to_exclude": [],
            }
        ).shift(RIGHT * 0.5)

    def create_table(self, data, colors=None):
        """
        创建表格（兼容旧版本）
        data: [[row1], [row2], ...]
        """
        if colors is None:
            colors = self.COLORS
        
        # 使用 Table 类（Manim 0.18+）
        try:
            table = Table(
                [[str(cell) for cell in row] for row in data],
                include_background_rectangle=True,
            )
            table.scale(0.6)
            return table
        except Exception as e:
            # 降级为简单文本
            log.warning(f"Table创建失败: {e}")
            return None

    # ==================== 主场景 ====================
    def construct(self):
        """主动画内容 - 必须重写"""
        raise NotImplementedError("请在子类中实现 construct() 方法")

# ==================== 日志 ====================
import logging
logging.basicConfig(level=logging.WARNING)
log = logging.getLogger("MathScene")
