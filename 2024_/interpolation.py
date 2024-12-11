from manim import *
import numpy as np

class Utils(VMobject):
    @staticmethod
    def linear_interpolation(A: Vector, B: Vector, t: float) -> Vector:
        """
        线性插值，返回点C = t * A + (1 - t) * B
        参数：
        - A, B: 两个三维向量（表示点A和点B）
        - t: 插值参数，0 <= t <= 1
        返回：插值结果点C
        """
        return t * A + (1 - t) * B

    @staticmethod
    def bezier_interpolation(control_points: list, t: float) -> Vector:
        """
        计算一个四点贝塞尔曲线上的点
        参数：
        - control_points: 控制点列表，包含4个控制点
        - t: 插值参数，0 <= t <= 1
        返回：贝塞尔曲线上的点
        """
        # 进行两次线性插值，首先计算线段的中间点
        interp_1 = Utils.linear_interpolation(control_points[0], control_points[1], t)
        interp_2 = Utils.linear_interpolation(control_points[1], control_points[2], t)
        interp_3 = Utils.linear_interpolation(control_points[2], control_points[3], t)

        # 计算更高阶的插值点
        interp_4 = Utils.linear_interpolation(interp_1, interp_2, t)
        interp_5 = Utils.linear_interpolation(interp_2, interp_3, t)

        # 最终贝塞尔曲线上的点
        return Utils.linear_interpolation(interp_4, interp_5, t)


class BezierInterpolationScene(Scene):
    def construct(self):
        # 使用 Axes 作为坐标系
        grid = NumberPlane(
            x_range=(-10, 10),   # 设置 x 轴范围
            y_range=(-10, 10),   # 设置 y 轴范围
            axis_config={"color": BLUE},
        ).add_coordinates()  # 显示坐标轴上的数值

        self.camera.frame_width = 20
        self.camera.frame_height = 20
        
        # 定义四个控制点
        control_points = [
            [-5, -5, 0],   # 左上角
            [0, 7, 0],     # 左下
            [5, -5, 0],    # 右上
            [8, 5, 0]      # 右下
        ]

        # 将控制点投影到坐标系
        projected_control_points = [grid.coords_to_point(point[0], point[1]) for point in control_points]

        self.play(Create(grid))
        self.wait(1)

        # 创建控制点的 Dot 对象（用红色表示原始控制点）
        dots = [Dot(point, color=RED) for point in projected_control_points]
        self.play(*[Create(dot) for dot in dots], run_time=2)

        # 创建控制线
        line_1 = Line(projected_control_points[0], projected_control_points[1], color=WHITE)
        line_2 = Line(projected_control_points[1], projected_control_points[2], color=WHITE)
        line_3 = Line(projected_control_points[2], projected_control_points[3], color=WHITE)
        self.play(Create(line_1), Create(line_2), Create(line_3))

        # 贝塞尔曲线的插值动画
        previous_dot_3 = None  # 保存上一个贝塞尔点
        moving_dot_3 = Dot(projected_control_points[0], color=YELLOW)  # 初始动态点

        # 动态插值动画：让点在插值的线段上移动
        for t in np.linspace(0, 1, num=200):  # 更平滑的插值
            bezier_point = Utils.bezier_interpolation(projected_control_points, t)
            moving_dot_3 = Dot(bezier_point, color=GREEN)  # 贝塞尔曲线上的动态点

            # 添加新的贝塞尔点到场景
            self.add(moving_dot_3)

            # 如果历史点已经存在，移除它们
            if previous_dot_3:
                self.remove(previous_dot_3)

            # 更新历史点
            previous_dot_3 = moving_dot_3

            # 等待一小段时间，保持平滑的视觉效果
            self.wait(0.02)

        self.wait(1)

        # 第二部分动画：绘制完整的贝塞尔曲线（线段）
        second_part_anims = []
        lines = []
        for t in np.linspace(0, 1, 10):  # 使用较小步长生成更平滑的曲线
            bezier_point = Utils.bezier_interpolation(projected_control_points, t)
            if t < 1:
                line_c = Line(projected_control_points[0], bezier_point, color=WHITE)
                lines.append(line_c)
                second_part_anims.append(Create(line_c))  # 显示线段

        # 第二部分动画：绘制贝塞尔曲线的完整线段
        self.play(*second_part_anims, run_time=4)  # 延长时间，平滑显示完整轨迹
        
        # 使用 FadeOut 动画移除线段
        self.play(*[FadeOut(line) for line in lines], run_time=2)
        self.wait(2)

        # 第三部分动画：绘制完整的贝塞尔曲线（线段）
        third_part_anims = []

        for t in np.linspace(0, 1, 100):  # 使用较小步长生成更平滑的曲线
            bezier_point = Utils.bezier_interpolation(projected_control_points, t)
            if t < 1:
                line_c = Line(projected_control_points[0], bezier_point, color=WHITE)
                third_part_anims.append(Create(line_c))  # 显示线段

        # 第三部分动画：绘制贝塞尔曲线的完整线段
        self.play(*third_part_anims, run_time=4)  # 延长时间，平滑显示完整轨迹

        self.wait(2)
