from manim import *
import numpy as np

class ComplexPathCameraFollow(MovingCameraScene):
    def construct(self):
        # 设置背景颜色为黑色
        self.camera.background_color = BLACK

        # 定义多个三次贝塞尔曲线的控制点，形成复杂路径
        control_points = [
            [LEFT * 6 + DOWN * 2, LEFT * 3 + UP * 3, RIGHT * 2 + DOWN * 4, RIGHT * 6 + UP * 1],
            [RIGHT * 6 + UP * 1, RIGHT * 8 + DOWN * 3, RIGHT * 10 + UP * 0, RIGHT * 12 + DOWN * 2],
            [RIGHT * 12 + DOWN * 2, RIGHT * 14 + UP * 4, RIGHT * 16 + DOWN * 1, RIGHT * 18 + UP * 3],
            [RIGHT * 18 + UP * 3, LEFT * 16 + DOWN * 2, LEFT * 14 + UP * 1, LEFT * 12 + DOWN * 3],
            [LEFT * 12 + DOWN * 3, LEFT * 10 + UP * 4, LEFT * 8 + DOWN * 2, LEFT * 6 + UP * 3],
            [LEFT * 6 + UP * 3, LEFT * 4 + DOWN * 4, LEFT * 2 + UP * 2, LEFT * 0 + DOWN * 0],
            [LEFT * 0 + DOWN * 0, LEFT * 2 + UP * 2, LEFT * 4 + DOWN * 4, LEFT * 6 + UP * 3],
            [LEFT * 6 + UP * 3, LEFT * 8 + DOWN * 2, LEFT * 10 + UP * 1, LEFT * 12 + DOWN * 3]
        ]

        # 生成复杂路径
        full_path = VMobject()
        full_path.set_stroke(WHITE, 2)
        initial_cp = control_points[0][0]
        # 添加起始点重复三次，以满足第一个贝塞尔曲线的要求
        full_path.set_points_as_corners([initial_cp, initial_cp, initial_cp, initial_cp])

        # 添加多个三次贝塞尔曲线到路径中
        for cps in control_points:
            full_path.add_cubic_bezier_curve_to(*cps[1:])

        # 缩放路径，使其更适合屏幕
        scale_factor = 0.2
        full_path.scale(scale_factor)
        self.add(full_path)

        # 创建移动的点
        moving_dot = Dot(color=YELLOW).move_to(full_path.get_start())
        self.add(moving_dot)

        # 创建实时绘制路径的对象
        traced_path = TracedPath(
            moving_dot.get_center,
            stroke_color=YELLOW,
            stroke_width=2
        )
        self.add(traced_path)

        # 定义 ValueTracker 来跟踪动画进度
        alpha_tracker = ValueTracker(0)

        # 定义更新函数，让移动点沿路径移动
        def update_dot(dot):
            alpha = alpha_tracker.get_value()
            new_point = full_path.point_from_proportion(alpha)
            dot.move_to(new_point)

        moving_dot.add_updater(update_dot)

        def update_camera_func(frame):
            target = moving_dot.get_center()
            frame.move_to(target)
            print("Camera func called")

        # 添加更新器，使摄像头始终跟随移动点
        self.camera.frame.add_updater(update_camera_func)

        # 设置摄像头的宽度，确保移动点始终在中央且画面紧凑
        self.camera.frame.set_width(12)  # 根据需要调整此值以实现更紧密的跟随

        # 确保摄像头初始位置与移动点对齐
        self.camera.frame.move_to(full_path.get_start())

        # 播放动画：移动点沿路径移动，绘制路径，摄像头紧密跟随
        self.play(
            alpha_tracker.animate.set_value(1),
            run_time=16,  # 增加运行时间以适应更复杂的路径
            rate_func=linear
        )

        self.wait(2)

        # 移除所有 updater，停止摄像头跟随
        moving_dot.remove_updater(update_dot)
        self.camera.frame.remove_updater(update_camera_func)

        self.wait(2)