"""
对数函数图形理解 - Lg3-1 Manim视频
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

    SCENES = {
        1: {"name": "开场", "audio": "audio_001_开场.wav", "duration": 5.47},
        2: {"name": "什么是对数", "audio": "audio_002_什么是对数.wav", "duration": 14.26},
        3: {"name": "Lg3含义", "audio": "audio_003_Lg3含义.wav", "duration": 16.15},
        4: {"name": "图形展示", "audio": "audio_004_图形展示.wav", "duration": 9.58},
        5: {"name": "图形平移", "audio": "audio_005_图形平移.wav", "duration": 13.30},
        6: {"name": "找交点", "audio": "audio_006_找交点.wav", "duration": 19.87},
        7: {"name": "数值验证", "audio": "audio_007_数值验证.wav", "duration": 16.75},
        8: {"name": "总结", "audio": "audio_008_总结.wav", "duration": 16.37},
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_dir = "audio_lg311"

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
        self.wait(wait_time + 0.3)

    def construct(self):
        # 幕1: 开场
        title = Text("对数函数", font_size=56, color=YELLOW).shift(UP * 0.8)
        subtitle = Text("Lg3 - 1 图形理解", font_size=40, color=WHITE)
        formula = MathTex(r"lg(3) - 1", font_size=48, color=self.COLORS['primary'])
        
        self.play_scene(1, Write(title), Write(subtitle), Write(formula), run_time=2)
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(formula))

        # 幕2: 什么是对数
        eq = MathTex(r"10^x = b", r" \iff ", r"x = \lg(b)", font_size=44)
        self.play_scene(2, Write(eq), run_time=3)
        self.wait(2)
        self.play(FadeOut(eq))

        # 幕3: Lg3-1含义
        formula1 = MathTex(r"lg3 - 1", font_size=50, color=YELLOW)
        formula2 = MathTex(r"= lg3 - lg10", font_size=50, color=YELLOW)
        formula3 = MathTex(r"= lg\frac{3}{10}", font_size=50, color=ORANGE)
        
        self.play_scene(3, Write(formula1), run_time=2)
        self.play(Write(formula2), run_time=2)
        self.play(Write(formula3), run_time=2)
        self.wait(2)
        self.play(FadeOut(formula1), FadeOut(formula2), FadeOut(formula3))

        # 幕4: 图形展示 - y=lg(x)
        # 坐标轴
        axes = Axes(
            x_range=[-1, 15, 1],
            y_range=[-5, 5, 1],
            x_length=12,
            y_length=8,
            axis_config={"include_tip": True}
        ).shift(RIGHT * 0.5)
        
        self.play_scene(4, Create(axes), run_time=2)
        
        # 对数函数曲线
        log_curve = axes.plot(lambda x: np.log10(x) if x > 0 else -10, 
                              x_range=[0.1, 14], color=RED)
        self.play(Create(log_curve), run_time=3)
        
        # 标注点 (1,0)
        point = Dot(axes.c2p(1, 0), color=YELLOW)
        label = Text("A(1,0)", font_size=24, color=WHITE).next_to(point, RIGHT)
        self.play(Create(point), Write(label), run_time=2)
        self.wait(2)

        # 幕5: 图形平移
        # y = lg(x) - 1 曲线
        log_shift = axes.plot(lambda x: np.log10(x) - 1 if x > 0 else -10, 
                              x_range=[0.1, 14], color=BLUE)
        
        self.play_scene(5, Create(log_shift), run_time=3)
        
        # 标注平移
        shift_label = Text("向下平移1单位", font_size=28, color=GRAY).to_corner(UL)
        self.play(Write(shift_label), run_time=2)
        self.wait(3)
        self.play(FadeOut(axes), FadeOut(log_curve), FadeOut(log_shift), 
                  FadeOut(point), FadeOut(label), FadeOut(shift_label))

        # 幕6: 找交点
        axes2 = Axes(
            x_range=[-1, 15, 1],
            y_range=[-5, 5, 1],
            x_length=12,
            y_length=8,
            axis_config={"include_tip": True}
        ).shift(RIGHT * 0.5)
        
        log_shift2 = axes2.plot(lambda x: np.log10(x) - 1 if x > 0 else -10, 
                                 x_range=[0.1, 14], color=BLUE)
        
        self.play_scene(6, Create(axes2), Create(log_shift2), run_time=3)
        
        # 交点 (10, 0)
        intersection = Dot(axes2.c2p(10, 0), color=ORANGE)
        inter_label = Text("B(10,0)", font_size=24, color=ORANGE).next_to(intersection, RIGHT * 1.5)
        
        # 公式
        solve = MathTex(r"lgx - 1 = 0", r" \Rightarrow ", r"x = 10", font_size=36)
        solve.to_edge(DOWN)
        
        self.play(Create(intersection), Write(inter_label), Write(solve), run_time=4)
        self.wait(3)
        self.play(FadeOut(axes2), FadeOut(log_shift2), FadeOut(intersection), 
                  FadeOut(inter_label), FadeOut(solve))

        # 幕7: 数值验证
        title = Text("数值验证", font_size=40, color=WHITE).to_edge(UP)
        
        table_data = [
            ["x", "lg(x)", "lg(x)-1"],
            ["0.3", "-0.523", "-1.523"],
            ["1", "0", "-1"],
            ["3", "0.477", "-0.523"],
            ["10", "1", "0"],
        ]
        
        # 创建表格
        table = Table(
            [[str(cell) for cell in row] for row in table_data],
            include_background_rectangle=True,
        )
        table.scale(0.7)
        
        self.play_scene(7, Write(title), Write(table), run_time=4)
        
        # 标注
        highlight = Text("lg(3) - 1 ≈ -0.523", font_size=32, color=ORANGE).to_edge(DOWN)
        self.play(Write(highlight), run_time=2)
        self.wait(3)
        self.play(FadeOut(title), FadeOut(table), FadeOut(highlight))

        # 幕8: 总结
        final_formula = MathTex(r"lg3 - 1 = lg\frac{3}{10}", font_size=48, color=YELLOW)
        final_point = Text("与 x 轴交点: (10, 0)", font_size=32, color=WHITE)
        
        self.play_scene(8, Write(final_formula), run_time=3)
        self.play(Write(final_point), run_time=2)
        
        self.wait(3)
