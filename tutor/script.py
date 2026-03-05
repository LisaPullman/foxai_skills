"""
割圆术 - Manim动画视频 (修复语音重叠)
"""

from manim import *
import json
import os

class MathScene(Scene):
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_rate = 60

    COLORS = {
        'background': '#1a1a2e',
        'primary': '#4ecca3',
        'secondary': '#e94560',
        'highlight': '#ffc107',
        'text': '#ffffff',
    }

    # 音频时长
    SCENES = {
        1: {"name": "开场", "audio": "audio_001_开场.wav", "duration": 4.75},
        2: {"name": "原理", "audio": "audio_002_原理.wav", "duration": 14.64},
        3: {"name": "公式", "audio": "audio_003_公式.wav", "duration": 8.95},
        4: {"name": "数值", "audio": "audio_004_数值.wav", "duration": 19.97},
        5: {"name": "刘徽", "audio": "audio_005_刘徽.wav", "duration": 16.78},
        6: {"name": "总结", "audio": "audio_006_总结.wav", "duration": 11.52},
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_dir = "audio"

    def play_scene(self, scene_num, *animations, **kwargs):
        """播放一幕，等待音频结束"""
        audio_duration = self.SCENES[scene_num]["duration"]
        
        audio_file = self.SCENES[scene_num]["audio"]
        audio_path = os.path.join(self.audio_dir, audio_file)
        if os.path.exists(audio_path):
            self.add_sound(audio_path)
        
        if animations:
            self.play(*animations, **kwargs)
        
        wait_time = max(0, audio_duration - kwargs.get("run_time", 1))
        self.wait(wait_time + 0.5)

    def construct(self):
        # ==================== 幕1: 开场 ====================
        title = Text("割圆术", font_size=60, color=YELLOW).shift(UP * 0.5)
        subtitle = Text("刘徽计算圆周率", font_size=36, color=WHITE)
        self.play_scene(1, Write(title), Write(subtitle), run_time=2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # ==================== 幕2: 原理 ====================
        # 画圆
        circle = Circle(radius=2, color=self.COLORS['secondary'])
        self.play_scene(2, Create(circle), run_time=2)
        
        # 正六边形
        hex_points = [2 * np.array([np.cos(a), np.sin(a), 0]) 
                      for a in np.arange(-PI/2, 3*PI/2 + 0.01, PI/3)]
        polygon = Polygon(*hex_points, color=self.COLORS['primary'])
        self.play(Create(polygon), run_time=2)
        
        # 边数增加动画
        for n in [12, 24, 48]:
            pts = [2 * np.array([np.cos(a), np.sin(a), 0]) 
                   for a in np.arange(-PI/2, 3*PI/2 + 0.01, 2*PI/n)]
            new_poly = Polygon(*pts, color=self.COLORS['primary'])
            self.play(Transform(polygon, new_poly), run_time=1.5)
        
        self.wait(2)

        # ==================== 幕3: 公式 ====================
        self.play(FadeOut(circle), FadeOut(polygon), run_time=1)
        
        formula = MathTex(r"a_{2n} = \sqrt{2 - \sqrt{4 - a_n^2}}", 
                        font_size=48, color=YELLOW)
        formula_label = Text("半角公式", font_size=40, color=WHITE).to_edge(UP)
        
        self.play_scene(3, Write(formula_label), Write(formula), run_time=3)
        self.wait(2)
        self.play(FadeOut(formula_label), FadeOut(formula))

        # ==================== 幕4: 数值 ====================
        # 表头
        headers = ["边数", "边长", "周长", "π≈"]
        header_mobs = []
        for i, h in enumerate(headers):
            t = Text(h, font_size=24, color=YELLOW).move_to(LEFT * 3 + RIGHT * i * 2)
            header_mobs.append(t)
        
        self.play_scene(4, *[Write(t) for t in header_mobs], run_time=2)
        
        # 数据
        data = [
            ("6", "1.000000", "6.000000", "3.000000"),
            ("12", "0.517638", "6.211657", "3.105828"),
            ("24", "0.261052", "6.265257", "3.132628"),
            ("48", "0.130806", "6.278708", "3.139354"),
            ("96", "0.065403", "6.282064", "3.141032"),
        ]
        
        # 在音频播放时逐步显示
        for row_idx, row in enumerate(data):
            for col_idx, val in enumerate(row):
                t = Text(val, font_size=18, color=WHITE).move_to(
                    LEFT * 3 + RIGHT * col_idx * 2 + DOWN * (row_idx + 1) * 0.4
                )
                self.add(t)  # 立即添加，不等待
        self.wait(2)

        # ==================== 幕5: 刘徽 ====================
        self.play(FadeOut(*self.mobjects), run_time=1)
        
        name = Text("刘徽", font_size=60, color=YELLOW).shift(UP * 1.5)
        book = Text("《九章算术》", font_size=40, color=WHITE)
        year = Text("公元263年", font_size=36, color=GRAY)
        
        self.play_scene(5, Write(name), Write(book), Write(year), run_time=4)
        self.wait(2)

        # ==================== 幕6: 总结 ====================
        self.play(FadeOut(*self.mobjects), run_time=1)
        
        # 圆和多边形
        circle = Circle(radius=2, color=self.COLORS['secondary'])
        pts_96 = [2 * np.array([np.cos(a), np.sin(a), 0]) 
                  for a in np.arange(-PI/2, 3*PI/2 + 0.01, 2*PI/96)]
        polygon = Polygon(*pts_96, color=self.COLORS['primary'])
        
        self.play(Create(circle), Create(polygon), run_time=2)
        
        title = Text("数学的魅力", font_size=48, color=YELLOW).to_edge(UP)
        pi_text = MathTex(r"\pi \approx 3.1415926\cdots", font_size=56, color=WHITE)
        
        self.play_scene(6, Write(title), Write(pi_text), run_time=4)
        self.wait(2)
