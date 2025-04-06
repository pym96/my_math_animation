from manim import *
import numpy as np

class RotationMatrixIntro(Scene):
    """基础旋转矩阵介绍 - 2D平面上的旋转"""
    def construct(self):
        # 标题
        title = Text("旋转矩阵：让物体转起来的数学魔法", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # 创建一个坐标系
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": BLUE},
        ).scale(0.8)
        
        # 手动创建轴标签
        x_label = Text("x", font_size=24).next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("y", font_size=24).next_to(axes.y_axis.get_end(), UP)
        
        # 创建一个点
        point = Dot(color=RED).move_to(axes.c2p(2, 0))
        point_label = Text("P(2,0)", font_size=24).next_to(point, RIGHT, buff=0.1)
        
        # 在坐标系中显示点
        self.play(Create(axes), Create(x_label), Create(y_label))
        self.play(Create(point), Write(point_label))
        self.wait()
        
        # 解释什么是旋转
        explanation = Text("旋转是什么？就是点围绕原点转动", font_size=28)
        explanation.to_edge(DOWN)
        self.play(Write(explanation))
        self.wait()
        
        # 演示旋转
        rotation_arc = Arc(start_angle=0, angle=PI/2, radius=2, color=YELLOW)
        angle_label = Text("90°").move_to(axes.c2p(1, 1)) 
        
        self.play(Create(rotation_arc), Write(angle_label))
        self.wait()
        
        # 点旋转
        rotated_point = Dot(color=GREEN).move_to(axes.c2p(0, 2))
        rotated_label = Text("P'(0,2)", font_size=24).next_to(rotated_point, UP, buff=0.1)
        
        self.play(
            Transform(point.copy(), rotated_point),
            FadeIn(rotated_point),
            FadeIn(rotated_label)
        )
        self.wait()
        
        # 清除前面的解释
        self.play(FadeOut(explanation))
        
        # 引入矩阵的概念
        matrix_intro = Text("如何用矩阵来表示旋转？", font_size=28).to_edge(DOWN)
        self.play(Write(matrix_intro))
        self.wait()
        
        # 展示旋转矩阵
        rotation_matrix = Text(
            "旋转矩阵(θ = 90°):\n" +
            "[[cos(θ), -sin(θ)],\n [sin(θ), cos(θ)]] = \n" +
            "[[0, -1],\n [1, 0]]", 
            font_size=24
        ).to_edge(LEFT)
        
        self.play(Write(rotation_matrix))
        self.wait()
        
        # 展示矩阵乘法
        matrix_operation = Text(
            "[[0, -1],   [[2],    [[0],\n" +
            " [1,  0]] ×  [0]]  =  [2]]", 
            font_size=24
        ).next_to(rotation_matrix, RIGHT, buff=1)
        
        self.play(Write(matrix_operation))
        self.wait(2)
        
        # 清除当前所有内容
        self.play(
            FadeOut(axes), FadeOut(x_label), FadeOut(y_label), 
            FadeOut(point), FadeOut(point_label),
            FadeOut(rotation_arc), FadeOut(angle_label),
            FadeOut(rotated_point), FadeOut(rotated_label),
            FadeOut(matrix_intro), FadeOut(rotation_matrix),
            FadeOut(matrix_operation)
        )
        
        # 介绍不同角度的旋转矩阵
        angle_intro = Text("不同角度的旋转矩阵", font_size=32).next_to(title, DOWN)
        self.play(Write(angle_intro))
        
        # 展示通用旋转矩阵
        general_matrix = Text(
            "旋转θ角度的矩阵:\n" +
            "[[cos(θ), -sin(θ)],\n [sin(θ), cos(θ)]]", 
            font_size=28
        )
        self.play(Write(general_matrix))
        self.wait()
        
        # 展示几个特殊角度的旋转矩阵
        special_angles = VGroup(
            Text("θ = 0°: [[1, 0], [0, 1]] (不旋转)", font_size=24),
            Text("θ = 90°: [[0, -1], [1, 0]]", font_size=24),
            Text("θ = 180°: [[-1, 0], [0, -1]]", font_size=24),
            Text("θ = 270°: [[0, 1], [-1, 0]]", font_size=24),
            Text("θ = 360°: [[1, 0], [0, 1]] (转一圈回到原位)", font_size=24)
        ).arrange(DOWN, buff=0.3).next_to(general_matrix, DOWN, buff=0.5)
        
        for angle in special_angles:
            self.play(Write(angle))
            self.wait(0.5)
        
        self.wait()
        
        # 清除当前所有内容
        self.play(
            FadeOut(angle_intro), FadeOut(general_matrix),
            *[FadeOut(angle) for angle in special_angles]
        )
        
        # 过渡到3D旋转
        transition_text = Text("从2D到3D：当我们有了第三个维度", font_size=32).next_to(title, DOWN)
        self.play(Write(transition_text))
        self.wait()
        
        # 解释在3D空间中，旋转变得更复杂
        d3_explanation = Text(
            "在3D空间中，我们可以围绕三个不同的轴旋转：\n" +
            "X轴、Y轴和Z轴", 
            font_size=28
        ).next_to(transition_text, DOWN)
        
        self.play(Write(d3_explanation))
        self.wait(2)
        
        # 清除并结束
        self.play(
            FadeOut(title), FadeOut(transition_text), 
            FadeOut(d3_explanation)
        )
        
        # 进入3D演示的提示
        final_text = Text("接下来，让我们进入3D空间，看看更神奇的旋转矩阵！", font_size=36)
        self.play(Write(final_text))
        self.wait(2)


class RotationMatrix3D(ThreeDScene):
    """3D空间中的旋转矩阵演示"""
    def construct(self):
        # 设置场景
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # 创建标题
        title = Text("3D空间中的旋转矩阵", font_size=40)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # 创建坐标轴
        axes = ThreeDAxes()
        self.add(axes)
        
        # 添加轴标签
        x_label = Text("X轴", font_size=24).next_to(axes.get_x_axis(), direction=RIGHT)
        y_label = Text("Y轴", font_size=24).next_to(axes.get_y_axis(), direction=UP)
        z_label = Text("Z轴", font_size=24).next_to(axes.get_z_axis(), direction=OUT+UP)
        
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)
        
        # 创建一个简单的立方体
        cube = Cube(side_length=2, fill_opacity=0.7, stroke_width=2)
        cube.set_stroke(BLUE, 2)
        cube.set_fill(BLUE_D, opacity=0.5)
        
        self.play(Create(cube))
        self.wait()
        
        # 解释三个旋转轴
        explanation = Text("在3D空间中，我们有三个旋转轴", font_size=28)
        explanation.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        self.wait()
        
        # 展示绕X轴旋转
        self.play(FadeOut(explanation))
        x_rot_text = Text("绕X轴旋转 (Roll)", font_size=28, color=RED)
        x_rot_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(x_rot_text)
        self.play(Write(x_rot_text))
        
        rx_matrix = Text(
            "Rx(α) = [[1, 0, 0], [0, cos(α), -sin(α)], [0, sin(α), cos(α)]]", 
            font_size=24
        )
        rx_matrix.next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(rx_matrix)
        self.play(Write(rx_matrix))
        
        # 演示X轴旋转
        self.play(Rotating(cube, axis=RIGHT, radians=PI, run_time=3))
        self.wait()
        
        # 展示绕Y轴旋转
        self.play(FadeOut(x_rot_text), FadeOut(rx_matrix))
        y_rot_text = Text("绕Y轴旋转 (Pitch)", font_size=28, color=GREEN)
        y_rot_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(y_rot_text)
        self.play(Write(y_rot_text))
        
        ry_matrix = Text(
            "Ry(β) = [[cos(β), 0, sin(β)], [0, 1, 0], [-sin(β), 0, cos(β)]]", 
            font_size=24
        )
        ry_matrix.next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(ry_matrix)
        self.play(Write(ry_matrix))
        
        # 演示Y轴旋转
        self.play(Rotating(cube, axis=UP, radians=PI, run_time=3))
        self.wait()
        
        # 展示绕Z轴旋转
        self.play(FadeOut(y_rot_text), FadeOut(ry_matrix))
        z_rot_text = Text("绕Z轴旋转 (Yaw)", font_size=28, color=BLUE)
        z_rot_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(z_rot_text)
        self.play(Write(z_rot_text))
        
        rz_matrix = Text(
            "Rz(γ) = [[cos(γ), -sin(γ), 0], [sin(γ), cos(γ), 0], [0, 0, 1]]", 
            font_size=24
        )
        rz_matrix.next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(rz_matrix)
        self.play(Write(rz_matrix))
        
        # 演示Z轴旋转
        self.play(Rotating(cube, axis=OUT, radians=PI, run_time=3))
        self.wait()
        
        # 展示组合旋转
        self.play(FadeOut(z_rot_text), FadeOut(rz_matrix))
        combined_text = Text("组合旋转：将三个旋转矩阵相乘", font_size=28)
        combined_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(combined_text)
        self.play(Write(combined_text))
        
        combined_matrix = Text("R = Rz · Ry · Rx", font_size=28)
        combined_matrix.next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(combined_matrix)
        self.play(Write(combined_matrix))
        
        # 演示组合旋转
        self.play(
            Rotating(cube, axis=RIGHT, radians=PI/4, run_time=2),
            Rotating(cube, axis=UP, radians=PI/4, run_time=2),
            Rotating(cube, axis=OUT, radians=PI/4, run_time=2),
        )
        self.wait()
        
        # 结束文本
        self.play(FadeOut(combined_text), FadeOut(combined_matrix))
        
        final_text = Text("旋转顺序很重要：Rz·Ry·Rx ≠ Rx·Ry·Rz", font_size=28)
        final_text.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(final_text)
        self.play(Write(final_text))
        
        application_text = Text("这些矩阵在3D游戏、动画和机器人技术中至关重要", font_size=24)
        application_text.next_to(final_text, UP)
        self.add_fixed_in_frame_mobjects(application_text)
        self.play(Write(application_text))
        
        self.wait(2)
        
        # 开始环绕相机移动来展示3D效果
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()


class RotationMatrixSummary(Scene):
    """旋转矩阵总结"""
    def construct(self):
        title = Text("旋转矩阵总结", font_size=40)
        title.to_edge(UP)
        self.play(Write(title))
        
        summary_points = VGroup(
            Text("1. 旋转矩阵是特殊的正交矩阵，用于描述旋转变换", font_size=28),
            Text("2. 2D旋转只需要一个角度参数θ", font_size=28),
            Text("3. 3D旋转需要围绕三个轴(X, Y, Z)分别旋转", font_size=28),
            Text("4. 旋转的顺序很重要，不同顺序会得到不同结果", font_size=28),
            Text("5. 旋转矩阵的应用广泛：游戏开发、机器人技术、\n   计算机图形学等", font_size=28),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).next_to(title, DOWN, buff=0.5)
        
        for point in summary_points:
            self.play(Write(point))
            self.wait(0.5)
        
        self.wait()
        
        # 扩展学习建议
        next_steps = Text(
            "想深入学习？探索：\n" +
            "- 四元数(Quaternions)\n" +
            "- 欧拉角(Euler Angles)\n" +
            "- 罗德里格斯旋转公式(Rodrigues' Rotation Formula)",
            font_size=28
        ).to_edge(DOWN)
        
        self.play(Write(next_steps))
        self.wait(2)


# 运行动画的主函数
if __name__ == "__main__":
    # 注释/取消注释要渲染的场景
    scene = RotationMatrixIntro()
    # scene = RotationMatrix3D()
    # scene = RotationMatrixSummary()
    scene.render()