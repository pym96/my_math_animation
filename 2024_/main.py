from manim import *
import numpy as np
from scipy.special import comb
from typing import List


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
        point_1 = A
        point_2 = B
        return t * A + (1 - t) * B

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
    

class BezierScene(Scene):
    def construct(self):
        # 使用 Axes 作为坐标系
        grid = NumberPlane(
            x_range=(-10, 10),   # 设置 x 轴范围
            y_range=(-10, 10),   # 设置 y 轴范围
            axis_config={"color": BLUE},
        ).add_coordinates()  # 显示坐标轴上的数值
        

        interpolation_demo_points = [
            [-2, 0, 0],
            [2, 0, 0]
        ]

        # 定义更复杂的控制点
        control_points = [
            [-3, -3, 0],   # 左上角
            [0, 2, 0],  # 左下
            [3, -3, 0],    # 右上
        ]

        # 将控制点投影到坐标系
        projceted_interpolation_demo_points = [grid.coords_to_point(point[0], point[1]) for point in interpolation_demo_points]
        projected_control_points = [grid.coords_to_point(point[0], point[1]) for point in control_points]

        # 创建BezierPath对象，使用 4 个可视化点和 100 个采样点
        bezier_path = BezierPath(projected_control_points, dot_num=4, resolution=100)

        intro_words = Text("""
            什么是Bezier曲线？
        """)
        # intro_words.to_edge(UP)

        self.play(Write(intro_words))
        self.wait(2)    
        
        intro_words_1 = Text("插值公式")

        self.play(FadeOut(intro_words), TransformFromCopy(intro_words, intro_words_1))
        self.wait(3)

        interpolation_intro = VGroup(
            MathTex(r"\text{l e r p:}", font_size=40).to_edge(LEFT), 
            MathTex(r"{C = t * A + (1 - t) * B}")
        )

        interpolation_intro.arrange(RIGHT)
        interpolation_intro.to_edge(UP)
        interpolation_intro.set_stroke(BLACK, 10, background=True)
        self.play(Create(grid), FadeTransform(intro_words_1, interpolation_intro))
        self.wait(3)


        # Create separate Text and MathTex objects
        linear_transform_words = VGroup(
            Text("选取3个点：", font_size=20),
            MathTex(r"{P_0}, {P_1}, {P_2}", font_size = 22)  # This is now separate
        )
        
        linear_transform_words.arrange(RIGHT)
        linear_transform_words.to_edge(UP)
        linear_transform_words.set_stroke(BLACK, 10, background=True)

        # Create points
        # 创建控制点的 Dot 对象（用红色表示原始控制点）
        interpolation_dots = [Dot(point, color=RED) for point in projceted_interpolation_demo_points]
        dots = [Dot(point, color=RED) for point in projected_control_points]
        
        interpolation_labels = [
            MathTex(r"A", font_size=24).next_to(interpolation_dots[0], DOWN),
            MathTex(r"B", font_size=24).next_to(interpolation_dots[1], DOWN)
        ]

        labels = [
            MathTex(r"P_0", font_size=24).next_to(dots[0], DOWN),
            MathTex(r"P_1", font_size=24).next_to(dots[1], DOWN),
            MathTex(r"P_2", font_size=24).next_to(dots[2], DOWN),
        ]

        interpolation_dot_animations = [Create(dot) for dot in interpolation_dots]
        interpolation_label_animations = [Write(interpolation_labels[i]) for i in range(len(interpolation_labels))]

        dot_animations = [Create(dot) for dot in dots]
        label_animations = [Write(labels[i]) for i in range(len(labels))]

        self.wait(3)
        self.play(AnimationGroup(*interpolation_dot_animations, *interpolation_label_animations), run_time = 2)
       
        # Show interpolation animation then disappear
        moving_dot_1 = Dot(projceted_interpolation_demo_points[0], color=YELLOW)
        
        interpolation_anims = []
        for t in np.arange(0, 1, 1):
            # 第一段线插值点
            interp_point_1 = Utils.linear_interpolation(projceted_interpolation_demo_points[0], projceted_interpolation_demo_points[1], t)
            interpolation_anims.append(moving_dot_1.animate.move_to(interp_point_1))
        
        interpolation_line = Line(projceted_interpolation_demo_points[0], projceted_interpolation_demo_points[1], color = WHITE)
        self.play(Create(interpolation_line), run_time = 2)
        self.wait(4)
        self.play(*interpolation_anims, run_time=4)  # 将总的动画时间延长，平滑过渡
        self.wait(4)
        
        # Wrap all the objects in VGroup
        # 使用包含的对象而不是动画对象
        fade_out_group = VGroup(*interpolation_dots, *interpolation_labels, *interpolation_line)
        self.play(FadeOut(fade_out_group, moving_dot_1), run_time=2)
        # self.play(FadeOut(moving_dot_1), run_time=2)


        # Create the grid and show the annotation
        self.play(FadeTransform(interpolation_intro, linear_transform_words))
        self.wait(2)
        self.play(AnimationGroup(*dot_animations, *label_animations), run_time=2)
        
        # Create lines
        line1 = Line(projected_control_points[0], projected_control_points[1], color=WHITE)
        line2 = Line(projected_control_points[2], projected_control_points[1], color=WHITE)

        self.play(Create(line1), Create(line2))
        self.wait(2)
        self.play(FadeOut(linear_transform_words))
 
        # 动态插值的点（开始时在P0）
        moving_dot_1 = Dot(projected_control_points[0], color=YELLOW)
        moving_dot_2 = Dot(projected_control_points[1], color=YELLOW)
        self.play(Create(moving_dot_1), Create(moving_dot_2))

        # 在第一段线（P0 -> P1）和第二段线（P1 -> P2）插值
        anims = []
        for t in np.arange(0, 1, 1):
            # 第一段线插值点
            interp_point_1 = Utils.linear_interpolation(projected_control_points[0], projected_control_points[1], t)
            anims.append(moving_dot_1.animate.move_to(interp_point_1))

            # 第二段线插值点
            interp_point_2 = Utils.linear_interpolation(projected_control_points[1], projected_control_points[2], t)
            anims.append(moving_dot_2.animate.move_to(interp_point_2))

        # 同时播放两段线插值的动画，增加 run_time 使动画更平滑
        self.play(*anims, run_time=4)  # 将总的动画时间延长，平滑过渡
        
        # 消去Moving_point, 之后进行插值
        self.play(FadeOut(moving_dot_1, moving_dot_2), run_time = 3)

        # 贝塞尔曲线的插值动画
        previous_line_c = None  # 保存上一个线段
        previous_dot_3 = None  # 保存上一个贝塞尔点
        moving_dot_3 = Dot(projected_control_points[0], color=YELLOW)  # 初始动态点


        # 第二部分动画：绘制完整的贝塞尔曲线（线段）
        second_part_anims = []
        lines = []
        for t in np.linspace(0, 1, 10):  
            # 第一段线插值点
            interp_point_1 = Utils.linear_interpolation(projected_control_points[0], projected_control_points[1], t)
            # 第二段线插值点
            interp_point_2 = Utils.linear_interpolation(projected_control_points[1], projected_control_points[2], t)
            # 计算贝塞尔曲线上的点
            bezier_point = Utils.linear_interpolation(interp_point_1, interp_point_2, t)
            # 生成线段
            if t < 1:
                line_c = Line(interp_point_1, interp_point_2, color=WHITE)
                lines.append(line_c)
                second_part_anims.append(Create(line_c))  # 显示线段

        # 第二部分动画：绘制贝塞尔曲线的完整线段
        self.play(*second_part_anims, run_time=6)  # 延长时间，平滑显示完整轨迹
        
        self.wait(4)
        # 使用 FadeOut 动画移除线段
        self.play(*[FadeOut(line) for line in lines], run_time=2)
        self.wait(2)

        # 第三部分动画：绘制完整的贝塞尔曲线（线段）
        third_part_anims = []
        lines = []
        for t in np.linspace(0, 1, 100):  # 使用较小步长生成更平滑的曲线
            # 第一段线插值点
            interp_point_1 = Utils.linear_interpolation(projected_control_points[0], projected_control_points[1], t)
            # 第二段线插值点
            interp_point_2 = Utils.linear_interpolation(projected_control_points[1], projected_control_points[2], t)
            # 计算贝塞尔曲线上的点
            bezier_point = Utils.linear_interpolation(interp_point_1, interp_point_2, t)
            # 生成线段
            if t < 1:
                line_c = Line(interp_point_1, interp_point_2, color=WHITE)
                lines.append(line_c)
                third_part_anims.append(Create(line_c))  # 显示线段

        # 第二部分动画：绘制贝塞尔曲线的完整线段
        self.play(*third_part_anims, run_time=4)  # 延长时间，平滑显示完整轨迹
        self.wait(4)

        self.play(*[FadeOut(line) for line in lines], run_time=4)
        self.wait(2)

        # 动态插值动画：让点在插值的线段上移动
        line_c = None
        for t in np.linspace(0, 1, num=200):  # 更平滑的插值
            # 计算线段插值点
            interp_point_1 = Utils.linear_interpolation(projected_control_points[0], projected_control_points[1], t)
            interp_point_2 = Utils.linear_interpolation(projected_control_points[1], projected_control_points[2], t)

            # 连接这两个插值点，构成line_c
            line_c = Line(interp_point_1, interp_point_2, color=WHITE)

            # 计算贝塞尔曲线上的点：再做一次线性插值
            bezier_point = Utils.linear_interpolation(interp_point_1, interp_point_2, t)
            moving_dot_3 = Dot(bezier_point, color=GREEN)  # 贝塞尔曲线上的动态点

            # 添加新的线段和贝塞尔点到场景
            self.add(line_c, moving_dot_3)

            # 如果历史线段和点已经存在，移除它们
            if previous_line_c:
                self.remove(previous_line_c)
            if previous_dot_3:
                self.remove(previous_dot_3)

            # 更新历史点和线段
            previous_line_c = line_c
            previous_dot_3 = moving_dot_3

            # 等待一小段时间，保持平滑的视觉效果
            self.wait(0.03)

        self.remove(line_c)
        self.wait(3)

        # 随着t的变化，两个连线的变化
        # 连接完所有的点后，绘制完整的贝塞尔曲线（用绿色表示完整曲线）
        bezier_curve = bezier_path.generate_bezier_curve()
        bezier_curve.set_color(GREEN)
        self.play(Create(bezier_curve), run_time=2)

        # 获取可视化点，并创建相应的 Dot 对象（用蓝色表示贝塞尔点）
        bezier_points = bezier_path.get_uniformly_sampled_points()

        # 将贝塞尔点投影到坐标系
        projected_bezier_points = [grid.coords_to_point(point[0], point[1]) for point in bezier_points]
        # bezier_dots = [Dot(point, color=BLUE) for point in projected_bezier_points] 

        # 逐个显示贝塞尔曲线上的点，使用 LaggedStart 来避免阻塞
        # self.play(LaggedStart(*[Create(dot) for dot in bezier_dots], lag_ratio=0.05), run_time=3)
        
        Quaratic_bezier_text = VGroup(
            Text("Quartic Bezier curve： 二次型贝塞尔曲线", font_size = 33)
        )

        Quaratic_bezier_text.to_edge(UP)
        Quaratic_bezier_text.set_stroke(BLACK, 5, background=True)
        self.play(FadeIn(Quaratic_bezier_text))
        self.wait(5)
        # 逐段连接线
        # self.play(*[Create(line) for line in lines], run_time=2)

        quadratic_formula = MathTex(
            r"A &= \text{lerp}(P_0, P_1, t) \\",
            r"B &= \text{lerp}(P_1, P_2, t) \\",
            r"Moving(t) &= \text{lerp}(A, B, t) \\",
            r"Moving(t) &= (1 - t)^2 P_0 + 2(1 - t)t P_1 + t^2 P_2",
            font_size=30
        ).to_edge(UL, buff=1)

        quadratic_formula.set_stroke(BLACK, 5, background=True)
        
        self.play(FadeOut(Quaratic_bezier_text), run_time=2)
        self.play(Write(quadratic_formula), run_time=3)

        self.wait(10)

        self.play(FadeOut(quadratic_formula))

        # 在显示四个点之前，先清空之前的所有内容
        self.play(FadeOut(*dots, *labels, bezier_curve), run_time = 1)
        self.play(FadeOut(line1, line2))

        # 四个控制点的设置
        control_points_4 = [
            [-3, -3, 0],   # 左上角
            [-1, 2, 0],  # 左下
            [2, -3, 0],    # 右上
            [4, 2, 0]  # 新增的右下控制点
        ]

        # 投影四个点到坐标系
        projected_control_points_4 = [grid.coords_to_point(point[0], point[1]) for point in control_points_4]
        bezier_path_4 = BezierPath(projected_control_points_4, dot_num=10, resolution=100)

        # 创建 4 个控制点的 Dot 对象（用红色表示）
        dots_4 = [Dot(point, color=RED) for point in projected_control_points_4]
        labels_4 = [
            MathTex(r"P_0", font_size=24).next_to(dots_4[0], DOWN),
            MathTex(r"P_1", font_size=24).next_to(dots_4[1], DOWN),
            MathTex(r"P_2", font_size=24).next_to(dots_4[2], DOWN),
            MathTex(r"P_3", font_size=24).next_to(dots_4[3], DOWN),
        ]

        # 动画：显示 4 个点
        self.play(AnimationGroup(*[Create(dot) for dot in dots_4], *[Write(label) for label in labels_4]))
        self.wait(3)
        
        # 连接控制点
        lines_4 = [
            Line(projected_control_points_4[i], projected_control_points_4[i+1], color=WHITE)
            for i in range(len(projected_control_points_4) - 1)
        ]
        self.play(AnimationGroup(*[Create(line) for line in lines_4]))

        # 创建动态插值的点
        moving_dot = Dot(projected_control_points_4[0], color=YELLOW)
        moving_dot_2 = Dot(projected_control_points_4[1], color=YELLOW)
        moving_dot_3 = Dot(projected_control_points_4[2], color=YELLOW)
        moving_dot_4 = Dot(projected_control_points_4[3], color=YELLOW)

        # 插值动画
        self.play(Create(moving_dot), Create(moving_dot_2), Create(moving_dot_3), Create(moving_dot_4))

        # 生成插值线
        line_p0_p1_old = Line(projected_control_points_4[0], projected_control_points_4[1], color=BLUE)
        line_p1_p2_old = Line(projected_control_points_4[1], projected_control_points_4[2], color=BLUE)
        line_p2_p3_old = Line(projected_control_points_4[2], projected_control_points_4[3], color=BLUE)

        self.play(Create(line_p0_p1_old), Create(line_p1_p2_old), Create(line_p2_p3_old))

        # 插值动画：让动态点在各个控制点间插值
        previous_dot_1, previous_dot_2, previous_dot_3 = None, None, None
        previous_line_p0_p1, previous_line_p1_p2= None, None
        moving_dot, previous_moving_dot = None, None
        line_c, previous_line_c= None, None

        for t in np.linspace(0, 1, num=400):  # 动画使用100个插值步骤，使其平滑
            # 插值计算
            interp_point_1 = Utils.linear_interpolation(projected_control_points_4[0], projected_control_points_4[1], t)
            interp_point_2 = Utils.linear_interpolation(projected_control_points_4[1], projected_control_points_4[2], t)
            interp_point_3 = Utils.linear_interpolation(projected_control_points_4[2], projected_control_points_4[3], t)

            # 创建新的动态点
            moving_dot_1 = Dot(interp_point_1, color=YELLOW)
            moving_dot_2 = Dot(interp_point_2, color=YELLOW)
            moving_dot_3 = Dot(interp_point_3, color=YELLOW)

            # 创建插值线
            line_p0_p1 = Line(interp_point_1, interp_point_2, color=WHITE)
            line_p1_p2 = Line(interp_point_2, interp_point_3, color=WHITE)

            interp_line_point_1 = Utils.linear_interpolation(interp_point_1, interp_point_2, t)
            interp_line_point_2 = Utils.linear_interpolation(interp_point_2, interp_point_3, t)

            
            line_c = Line(interp_line_point_1, interp_line_point_2, color = WHITE)
            # 最终插值点，生成最终的轨迹点
            final_interpolated_point = Utils.linear_interpolation(interp_line_point_1, interp_line_point_2, t)

             # 创建一个动态点表示最终的插值点
            moving_dot = Dot(final_interpolated_point, color=GREEN)

            # 添加新的点和线到场景
            self.add(line_p0_p1, line_p1_p2, moving_dot_1, moving_dot_2, moving_dot_3, line_c, moving_dot)

            # 如果历史线段和点已经存在，移除它们
            if previous_line_p0_p1:
                self.remove(previous_line_p0_p1)
            if previous_line_p1_p2:
                self.remove(previous_line_p1_p2)
            if previous_dot_1:
                self.remove(previous_dot_1)
            if previous_dot_2:
                self.remove(previous_dot_2)
            if previous_dot_3:
                self.remove(previous_dot_3)
            if previous_moving_dot:
                self.remove(previous_moving_dot)
            if previous_line_c:
                self.remove(previous_line_c)

            # 更新历史点和线段
            previous_line_p0_p1 = line_p0_p1
            previous_line_p1_p2 = line_p1_p2
            previous_dot_1 = moving_dot_1
            previous_dot_2 = moving_dot_2
            previous_dot_3 = moving_dot_3
            previous_line_c = line_c
            previous_moving_dot = moving_dot
            
            # 适当的等待，控制帧与帧之间的间隔
            self.wait(0.03)  # 控制动画播放速度，保持平滑效果

        self.wait(3)
        # 最后，显示贝塞尔曲线的最终路径
        bezier_curve_4 = bezier_path_4.generate_bezier_curve()
        bezier_curve_4.set_color(GREEN)
        self.play(Create(bezier_curve_4), run_time=3)
        self.wait(4)
        self.remove(line_p0_p1, line_p1_p2, previous_line_c, line_c, line_p0_p1_old, line_p1_p2_old, line_p2_p3_old)
        
        # TODO: Change one points among 4 point
        # 更新最后一个控制点的坐标
        control_points_4[3] = [control_points_4[3][0] + 1, control_points_4[3][1], 0]  # 更新P3坐标

        # 重新投影并更新贝塞尔曲线
        projected_control_points_4 = [grid.coords_to_point(point[0], point[1]) for point in control_points_4]

        # 确保生成的贝塞尔路径是有效的
        bezier_path_4 = BezierPath(projected_control_points_4, dot_num=10, resolution=100)
        bezier_curve_4_new = bezier_path_4.generate_bezier_curve()
        bezier_curve_4_new.set_color(GREEN)

        # 更新控制点的Dot位置
        dots_4[3].move_to(projected_control_points_4[3])  # Move the dot to the new control point
        # 创建新的线段（通过控制点2和3）
        new_line = Line(projected_control_points_4[2], projected_control_points_4[3])
        new_label = MathTex(r"P_3", font_size=24).next_to(projected_control_points_4[3], DOWN)

        # 动态更新贝塞尔曲线
        self.play(
            FadeOut(moving_dot_4, labels_4[3], lines_4[2]),
            Write(new_label),
            FadeIn(new_line),  # Fade in the new line
            FadeTransform(dots_4[3], dots_4[3]),  # Transform the Dot position to the new position
            FadeTransform(bezier_curve_4, bezier_curve_4_new),  # Update the bezier curve
            run_time=5
        )

        # self.remove(dots_4[3])

        self.wait(4)

        # TODO: Add two changed point_4 animation
        control_points_4[3] = [0, -3, 0]  # 更新P3坐标
        projected_control_points_4 = [grid.coords_to_point(point[0], point[1]) for point in control_points_4]

        bezier_path_4 = BezierPath(projected_control_points_4, dot_num=10, resolution=100)
        bezier_curve_4_new_1 = bezier_path_4.generate_bezier_curve()
        bezier_curve_4_new_1.set_color(GREEN)

        dots_4[3].move_to(projected_control_points_4[3])  # Move the dot to the new control point

        new_line_1 = Line(projected_control_points_4[2], projected_control_points_4[3])
        new_label_1 = MathTex(r"P_3", font_size=24).next_to(projected_control_points_4[3], DOWN)

        self.remove(bezier_curve_4_new)
        # 动态更新贝塞尔曲线
        self.play(
            FadeOut(new_line, new_label),
            Write(new_label_1),
            FadeIn(new_line_1,),  # Fade in the new line
            FadeTransform(dots_4[3], dots_4[3]),  # Transform the Dot position to the new position
            FadeTransform(bezier_curve_4_new, bezier_curve_4_new_1),  # Update the bezier curve
            run_time=5
        )

        self.wait(4)

        # Second animation
        control_points_4[2] = [1, 2, 0]  # 更新P2坐标
        control_points_4[3] = [2, -3, 0]  # 更新P3坐标
        
        projected_control_points_4 = [grid.coords_to_point(point[0], point[1]) for point in control_points_4]
        bezier_path_4 = BezierPath(projected_control_points_4, dot_num=10, resolution=100)
        bezier_curve_4_new_2 = bezier_path_4.generate_bezier_curve()
        bezier_curve_4_new_2.set_color(GREEN)

        dots_4[2].move_to(projected_control_points_4[2])  # Move the dot to the new control point
        dots_4[3].move_to(projected_control_points_4[3])  # Move the dot to the new control point

        new_line_2_1 = Line(projected_control_points_4[1], projected_control_points_4[2])
        new_label_2_1 = MathTex(r"P_2", font_size=24).next_to(projected_control_points_4[2], DOWN)

        new_line_2_2 = Line(projected_control_points_4[2], projected_control_points_4[3])
        new_label_2_2 = MathTex(r"P_3", font_size=24).next_to(projected_control_points_4[3], DOWN)

        self.remove(bezier_curve_4_new_1)
         # 动态更新贝塞尔曲线
        self.play(
            FadeOut(moving_dot_3, lines_4[1], labels_4[2], new_line_1, new_label_1),
            FadeTransform(dots_4[2], dots_4[2]),  # Transform the Dot position to the new position
            FadeTransform(dots_4[3], dots_4[3]),  # Transform the Dot position to the new position
            Write(new_label_2_1),
            Write(new_label_2_2),
            FadeIn(new_line_2_1, new_line_2_2),  # Fade in the new line
            FadeTransform(bezier_curve_4_new_1, bezier_curve_4_new_2),  # Update the bezier curve
            run_time=5
        )

        self.wait(4)

        # 动态更新控制点并绘制贝塞尔曲线
        Cubic_bezier_text = VGroup(
            Text("Cubic Bezier curve： 三次型贝塞尔曲线", font_size = 33)
        )  
        Cubic_bezier_text.to_edge(UP)
        Cubic_bezier_text.set_stroke(BLACK, 5, background=True)
        self.play(FadeIn(Cubic_bezier_text))
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
        ).to_edge(UL, buff=1)

        
        quadratic_formula.set_stroke(BLACK, 5, background=True)
        cubic_formula.set_stroke(BLACK, 5, background=True)

        self.play(FadeOut(Cubic_bezier_text), run_time=2)
        self.play(Write(cubic_formula), run_time=3)
        self.wait(10)
        self.play(FadeOut(cubic_formula))

        self.clear()
        
        self.wait(5)
        
        # TODO: 总结性质，下期预告
        summary_text = VGroup(
            Text("贝塞尔曲线的局限性：", font_size=30),
            Text("1. local control", font_size=24),
            Text("2. High-order complexity", font_size=24),
        )

        preview_text = Text("下集预告：How to slove it?", font_size=30, color=WHITE)

        summary_text.arrange(DOWN, aligned_edge=LEFT)
        summary_text.to_edge(LEFT, buff=1)
        summary_text.set_stroke(BLACK, 5, background=True)
        
        # 动画化显示总结文本
        self.play(FadeIn(summary_text[0]), run_time=3)
        self.wait(6)
        self.play(FadeIn(summary_text[1]), run_time=3)
        self.wait(6)
        self.play(FadeIn(summary_text[2]), run_time=3)
        self.wait(3)
        
        # 淡出总结文本
        self.play(FadeOut(summary_text), run_time=2)
        self.wait(2)

        self.play(FadeIn(preview_text), run_time=3)

        self.wait(5)
