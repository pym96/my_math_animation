from manim import *
import numpy as np
from scipy.special import comb
from typing import List

class Utils:
    @staticmethod
    def linear_interpolation(A: np.ndarray, B: np.ndarray, t: float) -> np.ndarray:
        """
        线性插值，返回点 C = t * A + (1 - t) * B
        参数：
        - A, B: 两个三维向量（表示点 A 和点 B）
        - t: 插值参数，0 <= t <= 1
        返回：插值结果点 C
        """
        A = np.array(A)  # 确保 A 是 numpy.ndarray 类型
        B = np.array(B)  # 确保 B 是 numpy.ndarray 类型
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
        """
        创建控制点及其标签。
        参数：
        - points: 控制点列表
        - labels: 标签名称列表
        返回：包含控制点和标签的 VGroup
        """
        dots = [Dot(point, color=RED) for point in points]
        tex_labels = [MathTex(label, font_size=24).next_to(dot, DOWN) for dot, label in zip(dots, labels)]
        return VGroup(*dots, *tex_labels)

    def connect_control_points(self, points: List[np.ndarray]) -> VGroup:
        """
        连接控制点以形成多边形。
        参数：
        - points: 控制点列表
        返回：包含线段的 VGroup
        """
        lines = [Line(points[i], points[i + 1], color=WHITE) for i in range(len(points) - 1)]
        return VGroup(*lines)

     
    def animate_interpolation(self, control_points: List[np.ndarray], resolution: int = 100):
        """
        动态插值动画。
        参数：
        - control_points: 控制点列表
        - resolution: 动画的插值分辨率
        """
        prev_dots = VGroup()  # 存储上一帧的所有点
        prev_lines = VGroup()  # 存储上一帧的所有线

        for t in np.linspace(0, 1, resolution):
            # 层级插值
            interp_points = control_points.copy()
            current_dots = VGroup()
            current_lines = VGroup()

            while len(interp_points) > 1:
                new_points = []
                for i in range(len(interp_points) - 1):
                    new_point = Utils.linear_interpolation(interp_points[i], interp_points[i + 1], t)
                    new_points.append(new_point)
                    # 创建当前点和线
                    current_dots.add(Dot(new_point, color=YELLOW, radius=0.05))
                    current_lines.add(Line(interp_points[i], interp_points[i + 1], color=BLUE))
                interp_points = new_points

            # 最终插值点
            final_point = interp_points[0]
            current_dots.add(Dot(final_point, color=GREEN, radius=0.08))

            # 添加当前点和线，移除上一帧的点和线
            self.add(current_dots, current_lines)
            self.remove(prev_dots, prev_lines)

            # 更新上一帧的点和线
            prev_dots = current_dots
            prev_lines = current_lines

            # 等待一小段时间以实现动画效果
            self.wait(0.02)

        # 移除最后的插值点和线
        self.remove(prev_dots, prev_lines)
    

    def construct(self):
        # 设置坐标系
        grid = NumberPlane(
            x_range=(-100, 100),
            y_range=(-100, 100),
            axis_config={"color": BLUE},
        ).add_coordinates()
        

        # 初始化控制点
        control_points = [
            np.array([-3, -3, 0]),
            np.array([-1, 2, 0]),
            np.array([2, -3, 0]),
            np.array([4, 2, 0])
        ]
        labels = ["P_0", "P_1", "P_2", "P_3"]

        Cubic_bezier_text = VGroup(
            Text("Cubic Bezier curve： 三次型贝塞尔曲线", font_size = 33)
        )  
        Cubic_bezier_text.to_edge(UP)
        Cubic_bezier_text.set_stroke(BLACK, 5, background=True)
        self.wait(5)

        cubic_formula = MathTex(
            r"A &= \text{lerp}(P_0, P_1, t) \\",
            r"B &= \text{lerp}(P_1, P_2, t) \\",
            r"C &= \text{lerp}(P_2, P_3, t) \\",
            r"D &= \text{lerp}(A, B, t) \\",
            r"E &= \text{lerp}(B, C, t) \\",
            r"Moving(t) &= \text{lerp}(D, E, t) \\",
            r"Moving(t) &= (1 - t)^3 P_0 + 3(1 - t)^2 t P_1 + 3(1 - t) t^2 P_2 + t^3 P_3",
            font_size=28
        )

        cubic_formula.set_stroke(BLACK, 5, background=True)

        self.play(
            FadeIn(Cubic_bezier_text), 
            Write(cubic_formula), 
            run_time=3
        )
        self.wait(5)

        self.play(
            FadeOut(Cubic_bezier_text), 
            Unwrite(cubic_formula), 
            run_time=3
        )


        self.play(Create(grid))

        # 创建控制点和线段
        control_points_group = self.create_control_points(control_points, labels)
        lines_group = self.connect_control_points(control_points)
        self.play(FadeIn(control_points_group))
        self.play(Create(lines_group), run_time=3)

        # 动态插值动画
        self.animate_interpolation(control_points, resolution=300)

        # 显示贝塞尔曲线
        bezier_path = BezierPath(control_points, resolution=300)
        bezier_curve = bezier_path.generate_bezier_curve()
        bezier_curve.set_color(GREEN)
        self.play(Create(bezier_curve))
        self.wait(2)

        self.play(
            FadeOut(control_points_group),
            Uncreate(lines_group), 
            Uncreate(bezier_curve)
        )
    
        self.wait(2)

        # 更新控制点并重新生成线段
        control_points[3] = [control_points[3][0] + 1, control_points[3][1], 0]  # 更新P3坐标
        control_points_group = self.create_control_points(control_points, labels)
        lines_group = self.connect_control_points(control_points)  # 重新生成线段
        self.play(FadeIn(control_points_group))
        self.play(Create(lines_group), run_time=3)

        self.animate_interpolation(control_points, resolution=300)

        # 显示贝塞尔曲线
        bezier_path = BezierPath(control_points, resolution=300)
        bezier_curve = bezier_path.generate_bezier_curve()
        bezier_curve.set_color(GREEN)
        self.play(Create(bezier_curve))
        self.wait(2)

        self.play(
            FadeOut(control_points_group),
            Uncreate(lines_group), 
            Uncreate(bezier_curve)
        )

        self.wait(2)

        # 再次更新控制点并重新生成线段
        control_points[3] = [0, -3, 0]  # 更新P3坐标
        control_points_group = self.create_control_points(control_points, labels)
        lines_group = self.connect_control_points(control_points)  # 重新生成线段
        self.play(FadeIn(control_points_group))
        self.play(Create(lines_group), run_time=3)

        self.animate_interpolation(control_points, resolution=300)

        # 显示贝塞尔曲线
        bezier_path = BezierPath(control_points, resolution=300)
        bezier_curve = bezier_path.generate_bezier_curve()
        bezier_curve.set_color(GREEN)
        self.play(Create(bezier_curve))
        self.wait(2)

        self.play(
            FadeOut(control_points_group),
            Uncreate(lines_group), 
            Uncreate(bezier_curve)
        )

        self.wait(2)

        # 最后一次更新控制点并重新生成线段
        control_points[2] = [1, 2, 0]  # 更新P2坐标
        control_points[3] = [2, -3, 0]  # 更新P3坐标

        control_points_group = self.create_control_points(control_points, labels)
        lines_group = self.connect_control_points(control_points)  # 重新生成线段
        self.play(FadeIn(control_points_group))
        self.play(Create(lines_group), run_time=3)

        self.animate_interpolation(control_points, resolution=300)

        # 显示贝塞尔曲线
        bezier_path = BezierPath(control_points, resolution=300)
        bezier_curve = bezier_path.generate_bezier_curve()
        bezier_curve.set_color(GREEN)
        self.play(Create(bezier_curve))
        self.wait(2)

        self.play(
            FadeOut(control_points_group),
            Uncreate(lines_group), 
            Uncreate(bezier_curve)
        )

        self.wait(2)

        control_points = [
            np.array([-9.25022948, -7.63971539, 0.0]),
            np.array([-8.34718798, -3.85702015, 0.0]),
            np.array([-6.44273847, 1.84924187, 0.0]),
            np.array([-4.22809547, 3.38918432, 0.0]),
            np.array([-2.5530847, 4.45029476, 0.0]),
            np.array([1.60865438, 4.22455137, 0.0]),
            np.array([3.73213269, 4.84129941, 0.0]),
            np.array([5.92741951, 4.23576259, 0.0]),
            np.array([5.24784548, 3.42459428, 0.0]),
            np.array([7.76412388, 1.85394291, 0.0]),
            np.array([8.87520961, -3.22331868, 0.0]),
            np.array([9.64804735, -7.67892869, 0.0]),
        ]

        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=grid.width * 0.18))

        control_points_group = self.create_control_points(control_points, labels)
        lines_group = self.connect_control_points(control_points)  # 重新生成线段
        self.play(FadeIn(control_points_group))
        self.play(Create(lines_group), run_time=3)

        # 显示贝塞尔曲线
        bezier_path = BezierPath(control_points, resolution=300)
        bezier_curve = bezier_path.generate_bezier_curve()
        bezier_curve.set_color(GREEN)

        self.play(Create(bezier_curve))
        self.wait(2)

        self.animate_interpolation(control_points, resolution=300)

        self.wait(3)
        
        self.play(
            FadeOut(control_points_group),
            Uncreate(lines_group), 
            Uncreate(bezier_curve)
        )

        self.wait(2)