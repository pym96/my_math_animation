from manim import *
import numpy as np
from scipy.special import comb
from typing import List


class BezierPath(VMobject):
    def __init__(self, points: List[Vector], dot_num:int = 10, resolution: int = 100, **kwargs):
        super().__init__(**kwargs)
        self.points = np.array(points)
        self.resolution = resolution
        self.dot_num = dot_num
        self.path = self.generate_bezier_curve()
        self.add(self.path)

    def generate_bezier_curve(self) -> VMobject:
        bezier_curve = VMobject()
        bezier_curve.set_points_as_corners(self.get_bezier_points())
        return bezier_curve

    def get_bezier_points(self) -> List[Vector]:
        n = len(self.points) - 1
        points = []
        for t in np.linspace(0, 1, self.resolution):
            point = np.zeros(3)
            for k, pt in enumerate(self.points):
                point += comb(n, k) * (1 - t) ** (n - k) * (t ** k) * pt
            points.append(point)
        return points

    def get_visualization_points(self) -> List[Vector]:
        """根据均匀递增的下标选取 dot_num 个点"""
        bezier_points = self.get_bezier_points()
        
        # 计算点的间隔，以确保选择的点均匀分布
        step = len(bezier_points) // self.dot_num
        selected_points = [bezier_points[i] for i in range(0, len(bezier_points), step)]
        
        # 如果选中的点多于 dot_num 个，截取前 dot_num 个
        return selected_points[:self.dot_num]

    def get_uniformly_sampled_points(self) -> List[Vector]:
        """根据曲线的弧长均匀采样 dot_num 个点"""
        # 获取所有贝塞尔曲线的采样点
        bezier_points = self.get_bezier_points()
        
        # 计算每两个连续点之间的距离（弧长）
        arc_lengths = [0]  # 起点的弧长为0
        total_length = 0
        for i in range(1, len(bezier_points)):
            segment_length = np.linalg.norm(bezier_points[i] - bezier_points[i-1])
            total_length += segment_length
            arc_lengths.append(total_length)

        # 计算每个采样点对应的弧长位置
        step_length = total_length / (self.dot_num - 1)
        sampled_points = []

        for i in range(self.dot_num):
            target_length = i * step_length
            # 找到弧长接近目标长度的点
            for j in range(1, len(arc_lengths)):
                if arc_lengths[j] >= target_length:
                    # 插值：返回该点的前后两个采样点
                    p1 = bezier_points[j-1]
                    p2 = bezier_points[j]
                    t = (target_length - arc_lengths[j-1]) / (arc_lengths[j] - arc_lengths[j-1])
                    point = p1 + t * (p2 - p1)  # 插值点
                    sampled_points.append(point)
                    break
        return sampled_points


class ComplexBezierScene(Scene):
    def construct(self):
        # 定义更复杂的控制点
        control_points = [
            [-3, 2, 0],   # 左上角
            [-1, -1, 0],  # 左下
            [1, 2, 0],    # 右上
            [-2, -2, 0],   # 右下
        ]

        # 创建BezierPath对象，使用 4 个可视化点和 100 个采样点
        bezier_path = BezierPath(control_points, dot_num=4, resolution=100)

        # 创建控制点的 Dot 对象（用红色表示原始控制点）
        dots = [Dot(point, color=RED) for point in control_points]
        self.play(*[Create(dot) for dot in dots], run_time=2)

        # 获取可视化点，并创建相应的 Dot 对象（用蓝色表示贝塞尔点）
        bezier_points = bezier_path.get_uniformly_sampled_points()
        # bezier_points = bezier_path.get_visualization_points()
        
        bezier_dots = [Dot(point, color=BLUE) for point in bezier_points]

        # 逐个显示贝塞尔曲线上的点，使用 LaggedStart 来避免阻塞
        self.play(LaggedStart(*[Create(dot) for dot in bezier_dots], lag_ratio=0.05), run_time=3)

        # 逐段连接贝塞尔曲线的点
        lines = []
        for i in range(1, len(bezier_dots)):
            line = Line(bezier_dots[i-1].get_center(), bezier_dots[i].get_center(), color=GREEN)
            lines.append(line)

        # 逐段连接线
        # self.play(*[Create(line) for line in lines], run_time=2)

        # 连接完所有的点后，绘制完整的贝塞尔曲线（用绿色表示完整曲线）
        bezier_curve = bezier_path.generate_bezier_curve()
        bezier_curve.set_color(GREEN)
        self.play(Create(bezier_curve), run_time=2)

        self.wait()  # 等待结束