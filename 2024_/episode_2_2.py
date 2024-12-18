from manim import *
import numpy as np
from scipy.special import comb
from typing import List

class Utils:
    @staticmethod
    def linear_interpolation(A: np.ndarray, B: np.ndarray, t: float) -> np.ndarray:
        A = np.array(A)
        B = np.array(B)
        return t * A + (1 - t) * B

class BezierPath(VMobject):
    def __init__(self, points: List[np.ndarray], resolution: int = 100, **kwargs):
        super().__init__(**kwargs)
        self.points = np.array(points)
        self.resolution = resolution
        self.path = self.generate_bezier_curve()
        self.add(self.path)

    def generate_bezier_curve(self) -> VMobject:
        bezier_curve = VMobject()
        bezier_curve.set_points_as_corners(self.get_bezier_points())
        return bezier_curve

    def get_bezier_points(self) -> List[np.ndarray]:
        n = len(self.points) - 1
        points = []
        for t in np.linspace(0, 1, self.resolution):
            point = np.zeros(3)
            for k, pt in enumerate(self.points):
                point += comb(n, k) * (1 - t) ** (n - k) * (t ** k) * pt
            points.append(point)
        return points

class BezierScene(MovingCameraScene):
    def create_control_points(self, points: List[np.ndarray], labels: List[str]) -> VGroup:
        dots = [Dot(point, color=RED) for point in points]
        tex_labels = [MathTex(label, font_size=24).next_to(dot, DOWN) for dot, label in zip(dots, labels)]
        return VGroup(*dots, *tex_labels)

    def connect_control_points(self, points: List[np.ndarray]) -> VGroup:
        lines = [Line(points[i], points[i + 1], color=WHITE) for i in range(len(points) - 1)]
        return VGroup(*lines)

    def animate_interpolation(self, control_points: List[np.ndarray], t_tracker: ValueTracker, resolution: int = 100):
        prev_dots = VGroup()
        prev_lines = VGroup()

        for t in np.linspace(0, 1, resolution):
            interp_points = control_points.copy()
            current_dots = VGroup()
            current_lines = VGroup()

            while len(interp_points) > 1:
                new_points = []
                for i in range(len(interp_points) - 1):
                    new_point = Utils.linear_interpolation(interp_points[i], interp_points[i + 1], t)
                    new_points.append(new_point)
                    current_dots.add(Dot(new_point, color=YELLOW, radius=0.05))
                    current_lines.add(Line(interp_points[i], interp_points[i + 1], color=BLUE))
                interp_points = new_points

            final_point = interp_points[0]
            current_dots.add(Dot(final_point, color=GREEN, radius=0.08))

            self.add(current_dots, current_lines)
            self.remove(prev_dots, prev_lines)

            prev_dots = current_dots
            prev_lines = current_lines

        self.remove(prev_dots, prev_lines)

    def construct(self):
        control_points = [
            np.array([-1, -1, 0]),
            np.array([-2, 2, 0]),
            np.array([4, -1, 0]),
            np.array([6, 3, 0])
        ]

        # 设置控制点动画
        labels = ["P_0", "P_1", "P_2", "P_3"]
        control_points_group = self.create_control_points(control_points, labels)
        lines_group = self.connect_control_points(control_points)

        # 设置图形
        graph_axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 1.2, 0.1],
            axis_config={"font_size": 20},
            tips=False
        ).scale(0.5).to_edge(DL)

        weight_graphs = {
            "P_0": graph_axes.plot(lambda t: (1 - t)**3, color=RED, x_range=[0, 1]),
            "P_1": graph_axes.plot(lambda t: 3 * (1 - t)**2 * t, color=BLUE, x_range=[0, 1]),
            "P_2": graph_axes.plot(lambda t: 3 * (1 - t) * t**2, color=GREEN, x_range=[0, 1]),
            "P_3": graph_axes.plot(lambda t: t**3, color=YELLOW, x_range=[0, 1])
        }

        weight_functions = {
            "P_0": lambda t: (1 - t)**3,
            "P_1": lambda t: 3 * (1 - t)**2 * t,
            "P_2": lambda t: 3 * (1 - t) * t**2,
            "P_3": lambda t: t**3,
        }

        colors = {"P_0": RED, "P_1": BLUE, "P_2": GREEN, "P_3": YELLOW}
        t_tracker = ValueTracker(0)

        graph_labels = VGroup(
            MathTex("t", font_size=20).next_to(graph_axes.x_axis, RIGHT),
            MathTex("Weight", font_size=20).next_to(graph_axes.y_axis, UP)
        )

        self.play(Create(graph_axes), Write(graph_labels))

        dynamic_weights = VGroup(*[
            DecimalNumber(0, color=color, font_size=28).add_updater(
                lambda m, func=func: m.set_value(func(t_tracker.get_value()))
            ) for func, color in zip(weight_functions.values(), colors.values())
        ])
        dynamic_weights.arrange(DOWN, buff=0.5).to_edge(LEFT, buff=1.5)

        # 创建权重图和动态点
        graph_creations = [Create(graph) for graph in weight_graphs.values()]
        dynamic_points = VGroup(*[
            Dot(color=color, radius=0.1).move_to(
                graph_axes.c2p(0, func(0))
            ).add_updater(
                lambda m, func=func: m.move_to(
                    graph_axes.c2p(t_tracker.get_value(), func(t_tracker.get_value()))
                )
            ) for func, color in zip(weight_functions.values(), colors.values())
        ])

        # 创建贝塞尔曲线
        bezier_path = BezierPath(control_points, resolution=300)
        bezier_curve = bezier_path.generate_bezier_curve()
        bezier_curve.set_color(GREEN)

        self.play(
            FadeIn(control_points_group),
            Create(lines_group),
        )
        
        # 动态插值动画和贝塞尔曲线动画与图形动画一起播放
        self.play(
            *graph_creations,
            FadeIn(dynamic_points),
            FadeIn(dynamic_weights),
            run_time=5
        )

        # 开始同步更新
        self.play(
            Create(bezier_curve),  # 创建贝塞尔曲线
            t_tracker.animate.set_value(1),
            run_time=5, rate_func=linear
        )

        # 动态插值动画
        self.animate_interpolation(control_points, t_tracker, resolution=300)

        # 清除场景
        self.play(
            FadeOut(control_points_group, dynamic_points, dynamic_weights),
            Uncreate(lines_group),
            Uncreate(bezier_curve),
            Uncreate(graph_axes),
            Unwrite(graph_labels), 
            *[Uncreate(graph) for graph in weight_graphs.values()]
        )

   
        self.wait(2)
