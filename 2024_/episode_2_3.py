from manim import *
import numpy as np

class BezierDerivativeScene(Scene):
    def create_control_points(self, points: list, labels: list, color=RED) -> VGroup:
        """
        创建控制点和标签。
        """
        dots = [Dot(point, color=color) for point in points]
        tex_labels = [MathTex(label, font_size=24).next_to(dot, DOWN) for dot, label in zip(dots, labels)]
        return VGroup(*dots, *tex_labels)

    def connect_control_points(self, points: list, color=WHITE) -> VGroup:
        """
        连接控制点形成线段。
        """
        lines = [Line(points[i], points[i + 1], color=color) for i in range(len(points) - 1)]
        return VGroup(*lines)

    def construct(self):
        # 三次贝塞尔曲线控制点
        control_points = [
            np.array([-1, -1, 0]),
            np.array([-2, 2, 0]),
            np.array([4, -1, 0]),
            np.array([6, 3, 0])
        ]

        P0, P1, P2, P3 = control_points

        # 贝塞尔曲线公式
        cubic_formula = MathTex(
            r"B_3(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3",
            font_size=32
        ).to_edge(UP).set_color(GREEN)
        self.play(Write(cubic_formula), run_time=2)

        # 显示控制点和连线
        control_points_group = self.create_control_points(control_points, ["P_0", "P_1", "P_2", "P_3"], color=RED)
        control_lines_group = self.connect_control_points(control_points, color=WHITE)
        self.play(FadeIn(control_points_group), Create(control_lines_group), run_time=2)

        # 绘制三次贝塞尔曲线
        bezier_curve = ParametricFunction(
            lambda t: (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3,
            t_range=[0, 1],
            color=GREEN
        )
        self.play(Create(bezier_curve), run_time=4)
        self.wait(1)

        # 导数公式
        derivative_formula = MathTex(
            r"B_3'(t) = 3(1-t)^2 (P_1 - P_0) + 6(1-t)t (P_2 - P_1) + 3t^2 (P_3 - P_2)",
            font_size=32
        ).next_to(cubic_formula, DOWN).set_color(RED)
        self.play(Write(derivative_formula), run_time=2)

  
        # 设置坐标系
        graph_axes = Axes(
            x_range=[0, 1, 0.1],  # t 范围 [0, 1]
            y_range=[0, 10, 2],  # y 值范围（根据计算结果微调）
            axis_config={"font_size": 20},
            tips=False
        ).scale(0.5).to_edge(DL)

        # 坐标系标签
        labels = graph_axes.get_axis_labels(x_label="t", y_label="B'_3(t)")
        self.play(Create(graph_axes), Write(labels))

        # 绘制导数曲线（y 分量 velocity）
        derivative_curve_y = graph_axes.plot(
            lambda t: 3 * (1 - t)**2 * (P1[1] - P0[1]) + 
                      6 * (1 - t) * t * (P2[1] - P1[1]) + 
                      3 * t**2 * (P3[1] - P2[1]),
            color=RED,
            x_range=[0, 1]
        )

        # 绘制导数曲线（x 分量 velocity）
        derivative_curve_x = graph_axes.plot(
            lambda t: 3 * (1 - t)**2 * (P1[0] - P0[0]) + 
                      6 * (1 - t) * t * (P2[0] - P1[0]) + 
                      3 * t**2 * (P3[0] - P2[0]),
            color=BLUE,
            x_range=[0, 1]
        )   

        # 添加曲线标签
        label_y = Tex("y-velocity", font_size=24, color=RED).next_to(derivative_curve_y, RIGHT, buff=0.5)
        label_x = Tex("x-velocity", font_size=24, color=BLUE).next_to(derivative_curve_x, RIGHT, buff=0.5)

        self.play(
            Create(derivative_curve_x),
            Create(derivative_curve_y),
            Write(label_y),
            Write(label_x),
            run_time = 3
        )

        self.wait(5)

        # 清理场景
        self.play(
            FadeOut(control_points_group),
            Uncreate(control_lines_group),
            Uncreate(bezier_curve),
            Uncreate(derivative_curve_y),
            Uncreate(derivative_curve_x),
            Uncreate(graph_axes),
            FadeOut(labels),
            FadeOut(cubic_formula),
            FadeOut(derivative_formula)
        )
