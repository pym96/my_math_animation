from manim import *
import numpy as np

class AutonomousDrivingScene(Scene):
    def construct(self):
        # 创建车道（两条实线和中间虚线）
        road_left = Line(start=[-3, -3.5, 0], end=[-3, 3.5, 0], color=WHITE, stroke_width=4)
        road_right = Line(start=[3, -3.5, 0], end=[3, 3.5, 0], color=WHITE, stroke_width=4)
        road_center = DashedLine(start=[0, -3.5, 0], end=[0, 3.5, 0], color=GRAY, stroke_width=2, dash_length=0.3)

        # 将车道添加到场景中
        self.play(Create(road_left), Create(road_right), Create(road_center))
        self.wait(1)

        # 创建障碍车辆（矩形）
        car_1 = Rectangle(width=1, height=2, color=BLUE, fill_opacity=0.8).move_to([-1.5, 2, 0])
        car_2 = Rectangle(width=1, height=2, color=RED, fill_opacity=0.8).move_to([1.5, -1, 0])
        self.play(FadeIn(car_1), FadeIn(car_2))
        self.wait(1)

        # 创建自动驾驶车辆（绿色矩形）
        self_car = Rectangle(width=1, height=2, color=GREEN, fill_opacity=0.8).move_to([-1.5, -3, 0])
        self.play(FadeIn(self_car))
        self.wait(1)

        # 生成 Bézier 曲线路径
        start = np.array([-1.5, -3, 0])  # 起点
        control_1 = np.array([-2, -1, 0])  # 第一个控制点
        control_2 = np.array([2, 2.5, 0])  # 第二个控制点
        end = np.array([1.5, 3, 0])  # 终点

        bezier_curve = CubicBezier(start, control_1, control_2, end).set_color(YELLOW)

        # 显示 Bézier 曲线
        self.play(Create(bezier_curve), run_time=2)
        self.wait(1)

        # 模拟自动驾驶车辆沿 Bézier 曲线移动
        self.play(MoveAlongPath(self_car, bezier_curve), run_time=4)
        self.wait(2)

        # 清理场景
        self.play(FadeOut(self_car), FadeOut(car_1), FadeOut(car_2), FadeOut(bezier_curve),
                  FadeOut(road_left), FadeOut(road_right), FadeOut(road_center))
