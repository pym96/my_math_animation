from manim import *
import numpy as np

class BezierWithVelocityAndNormal(Scene):
    def construct(self):
        # 设置控制点
        control_points = [
            np.array([-3, -2, 0]),
            np.array([-1, 2, 0]),
            np.array([2, -1, 0]),
            np.array([4, 3, 0])
        ]
        P0, P1, P2, P3 = control_points

        # 绘制控制点和连线
        control_points_group = VGroup(
            *[Dot(p, color=RED) for p in control_points]
        )
        control_labels = VGroup(
            *[
                MathTex(f"P_{i}").next_to(p, DOWN)
                for i, p in enumerate(control_points)
            ]
        )
        control_lines = VGroup(
            *[Line(control_points[i], control_points[i + 1], color=WHITE) for i in range(len(control_points) - 1)]
        )

        self.play(FadeIn(control_points_group), Write(control_labels), Create(control_lines), run_time=2)

        # 动态生成 Bézier 曲线
        bezier_curve = ParametricFunction(
            lambda t: (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3,
            t_range=[0, 1],
            color=GREEN
        )
        self.play(Create(bezier_curve), run_time=2)
        self.wait(2)
        
        # 动态显示 velocity arrows
        previous_velocity_arrow = None
        for t in np.linspace(0, 1, 300):
            # Bézier 曲线上的点
            point = (1 - t) ** 3 * P0 + 3 * (1 - t) ** 2 * t * P1 + 3 * (1 - t) * t ** 2 * P2 + t ** 3 * P3
            # 一阶导数（速度方向）
            derivative = (
                3 * (1 - t) ** 2 * (P1 - P0) +
                6 * (1 - t) * t * (P2 - P1) +
                3 * t ** 2 * (P3 - P2)
            )

            # 创建速度方向箭头
            velocity_arrow = Arrow(start=point, end=point + derivative / 5, color=RED, buff=0)

            # 动态更新箭头
            if previous_velocity_arrow:
                self.remove(previous_velocity_arrow)
            self.add(velocity_arrow)
            previous_velocity_arrow = velocity_arrow

            self.wait(0.02)

        # 移除所有 velocity arrows
        if previous_velocity_arrow:
            self.remove(previous_velocity_arrow)
        self.wait(5)

  
        # 动态显示 velocity 和 normal arrows
        previous_velocity_arrow = None
        previous_normal_arrow = None
        for t in np.linspace(0, 1, 300):
            # Bézier 曲线上的点
            point = (1 - t) ** 3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3
            # 一阶导数（速度方向）
            derivative = (
                3 * (1 - t) ** 2 * (P1 - P0) +
                6 * (1 - t) * t * (P2 - P1) +
                3 * t ** 2 * (P3 - P2)
            )
            # 法向量（旋转90度）
            normal_vector = np.array([-derivative[1], derivative[0], 0])
            
            # 归一化箭头长度
            derivative_unit = derivative / np.linalg.norm(derivative) * 0.5  # 设置统一长度为 0.5
            normal_unit = normal_vector / np.linalg.norm(normal_vector) * 0.5  # 设置统一长度为 0.5

            # 创建箭头
            velocity_arrow = Arrow(start=point, end=point + derivative_unit, color=RED, buff=0)
            normal_arrow = Arrow(start=point, end=point + normal_unit, color=BLUE, buff=0)

            # 动态更新箭头
            if previous_velocity_arrow:
                self.remove(previous_velocity_arrow)
            if previous_normal_arrow:
                self.remove(previous_normal_arrow)

            self.add(velocity_arrow, normal_arrow)
            previous_velocity_arrow = velocity_arrow
            previous_normal_arrow = normal_arrow

            self.wait(0.02)

        self.wait(2)
        
        # 移除所有箭头
        if previous_velocity_arrow:
            self.remove(previous_velocity_arrow)
        if previous_normal_arrow:
            self.remove(previous_normal_arrow)

        self.wait(2)

        # 清理场景
        self.play(FadeOut(control_points_group), FadeOut(control_labels), Uncreate(control_lines),
                  Uncreate(bezier_curve))

        self.wait(2)