from manim import *
import numpy as np
import os

# Configure to handle the file not found error
config.tex_template = TexTemplate()
config.tex_template.add_to_preamble(r"\usepackage{amsmath}")
# Workaround for macOS hidden file issue during TeX cleanup
config["no_latex_cleanup"] = True

# Helper function for linear interpolation
def lerp(p0, p1, t):
    return (1 - t) * p0 + t * p1

class PiecewiseBezierTutorial(Scene):
    def construct(self):
        # Introduction
        self.introduction()
        
        # What are Bezier curves
        self.bezier_basics()
        
        # Piecewise Bezier curves
        self.piecewise_bezier()
        
        # Application in autonomous driving
        self.autonomous_driving_application()
        
        # Conclusion
        self.conclusion()

    def introduction(self):
        title = Text("Piecewise Bezier Curves", font_size=48)
        subtitle = Text("for Autonomous Driving", font_size=36, color=BLUE)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(1)
        
        group = VGroup(title, subtitle)
        self.play(group.animate.scale(0.6).to_corner(UL))
        self.wait(1)
        
        intro_text = Text(
            "Smooth trajectories for vehicles",
            font_size=32
        ).next_to(group, DOWN, aligned_edge=LEFT, buff=1)
        
        self.play(Write(intro_text))
        self.wait(1)
        self.play(FadeOut(intro_text))
        self.play(FadeOut(title, subtitle))

    def bezier_basics(self):
        section_title = Text("What are Bezier Curves?", font_size=36).to_edge(UP)
        self.play(Write(section_title))
        self.wait(1)

        # --- 1. Linear Interpolation (Lerp) ---
        lerp_intro = Text("Let's start with Linear Interpolation (Lerp)", font_size=28).next_to(section_title, DOWN, buff=0.5)
        self.play(Write(lerp_intro))

        pA = Dot(point=[-4, 0, 0], color=RED)
        pB = Dot(point=[4, 0, 0], color=RED)
        pA_label = MathTex("P_A").next_to(pA, DOWN)
        pB_label = MathTex("P_B").next_to(pB, DOWN)
        line_AB = Line(pA.get_center(), pB.get_center(), color=WHITE, stroke_width=2)

        self.play(Create(pA), Write(pA_label), Create(pB), Write(pB_label))
        self.play(Create(line_AB))

        lerp_formula = MathTex("P(t) = (1-t)P_A + t P_B", font_size=32).next_to(lerp_intro, DOWN, buff=0.5)
        self.play(Write(lerp_formula))

        t_tracker = ValueTracker(0)
        moving_dot = Dot(color=YELLOW).add_updater(
            lambda m: m.move_to(lerp(pA.get_center(), pB.get_center(), t_tracker.get_value()))
        )
        t_label = MathTex("t = ").next_to(moving_dot, UP)
        t_value = DecimalNumber(
            t_tracker.get_value(),
            num_decimal_places=2
        ).next_to(t_label, RIGHT)
        t_value.add_updater(lambda d: d.set_value(t_tracker.get_value()))
        t_group = VGroup(t_label, t_value).add_updater(lambda m: m.next_to(moving_dot, UP))

        self.play(Create(moving_dot), Create(t_group))
        self.play(t_tracker.animate.set_value(1), run_time=3)
        self.wait(1)
        self.play(FadeOut(pA), FadeOut(pB), FadeOut(pA_label), FadeOut(pB_label),
                  FadeOut(line_AB), FadeOut(moving_dot), FadeOut(t_group),
                  FadeOut(lerp_intro), FadeOut(lerp_formula))
        self.wait(0.5)

        # --- 2. Quadratic Bezier Curve ---
        quad_intro = Text("Quadratic Bezier: Lerp of Lerps", font_size=28).next_to(section_title, DOWN, buff=0.5)
        self.play(Write(quad_intro))
        self.wait(1)
        self.play(Unwrite(quad_intro))

        p0 = Dot(point=[-4, -2, 0], color=RED)
        p1 = Dot(point=[0, 2, 0], color=GREEN)
        p2 = Dot(point=[4, -2, 0], color=RED)
        p0_label = MathTex("P_0").next_to(p0, DOWN)
        p1_label = MathTex("P_1").next_to(p1, UP)
        p2_label = MathTex("P_2").next_to(p2, DOWN)
        dots = VGroup(p0, p1, p2)
        labels = VGroup(p0_label, p1_label, p2_label)

        line01 = Line(p0.get_center(), p1.get_center(), color=YELLOW, stroke_width=2)
        line12 = Line(p1.get_center(), p2.get_center(), color=YELLOW, stroke_width=2)
        lines = VGroup(line01, line12)

        self.play(Create(dots), Write(labels))
        self.play(Create(lines))
        self.wait(1)

        quad_formula = MathTex(
            r"P_A(t) &= (1-t)P_0 + t P_1 \\",
            r"P_B(t) &= (1-t)P_1 + t P_2 \\",
            r"B(t) &= (1-t)P_A(t) + t P_B(t)",
            font_size=32
        ).next_to(quad_intro, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(quad_formula))

        t_tracker = ValueTracker(0) # Reset t_tracker

        # Interpolation points
        dot_A = Dot(color=BLUE).add_updater(lambda m: m.move_to(lerp(p0.get_center(), p1.get_center(), t_tracker.get_value())))
        dot_B = Dot(color=BLUE).add_updater(lambda m: m.move_to(lerp(p1.get_center(), p2.get_center(), t_tracker.get_value())))

        # Line connecting interpolation points
        line_AB_interp = Line(color=WHITE, stroke_width=2).add_updater(
            lambda m: m.put_start_and_end_on(dot_A.get_center(), dot_B.get_center())
        )

        # Final Bezier point
        bezier_dot = Dot(color=GREEN).add_updater(
            lambda m: m.move_to(lerp(dot_A.get_center(), dot_B.get_center(), t_tracker.get_value()))
        )

        # Path trace
        bezier_path = TracedPath(bezier_dot.get_center, stroke_color=GREEN, stroke_width=4)

        self.add(bezier_path) # Add the path tracer to the scene
        self.play(Create(dot_A), Create(dot_B), Create(line_AB_interp), Create(bezier_dot))
        self.play(t_tracker.animate.set_value(1), run_time=5, rate_func=linear)
        self.wait(1)

        # Remove updaters to freeze the final state
        dot_A.clear_updaters()
        dot_B.clear_updaters()
        line_AB_interp.clear_updaters()
        bezier_dot.clear_updaters()

        self.play(FadeOut(dot_A), FadeOut(dot_B), FadeOut(line_AB_interp), FadeOut(bezier_dot),
                  FadeOut(quad_intro), FadeOut(quad_formula))
        self.wait(0.5)
        # Keep the quadratic curve, control points, lines for a moment before cubic
        self.play(FadeOut(bezier_path)) # Fade out trace, keep dots/lines for cubic transition

        # --- 3. Cubic Bezier Curve ---
        cubic_intro = Text("Cubic Bezier: Lerp of Lerp of Lerps", font_size=28).next_to(section_title, DOWN, buff=0.5)
        # Fade out quadratic elements before showing cubic intro
        self.play(FadeOut(dots), FadeOut(labels), FadeOut(lines))
        self.play(Write(cubic_intro))
        self.wait(1)
        self.play(Unwrite(cubic_intro))

        # Define points for cubic Bezier
        p0 = Dot(point=[-5, -2, 0], color=RED); p0_label = MathTex("P_0").next_to(p0, DOWN)
        p1 = Dot(point=[-3, 2, 0], color=GREEN); p1_label = MathTex("P_1").next_to(p1, UP)
        p2 = Dot(point=[3, 2, 0], color=GREEN); p2_label = MathTex("P_2").next_to(p2, UP)
        p3 = Dot(point=[5, -2, 0], color=RED); p3_label = MathTex("P_3").next_to(p3, DOWN)
        dots = VGroup(p0, p1, p2, p3)
        labels = VGroup(p0_label, p1_label, p2_label, p3_label)

        line01 = Line(p0.get_center(), p1.get_center(), color=YELLOW, stroke_width=2)
        line12 = Line(p1.get_center(), p2.get_center(), color=YELLOW, stroke_width=2)
        line23 = Line(p2.get_center(), p3.get_center(), color=YELLOW, stroke_width=2)
        lines = VGroup(line01, line12, line23)

        self.play(Create(dots), Write(labels))
        self.play(Create(lines))
        self.wait(1)

        # Show cubic formula briefly
        try:
            cubic_formula = MathTex(
                r"B(t) = (1-t)^3 P_0 + 3(1-t)^2t P_1 + 3(1-t)t^2 P_2 + t^3 P_3"
            ).scale(0.7).next_to(cubic_intro, DOWN, buff=0.5).to_edge(LEFT)
        except Exception:
            cubic_formula = Text(
                "B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃",
                font_size=24
            ).next_to(cubic_intro, DOWN, buff=0.5).to_edge(LEFT)
        self.play(Write(cubic_formula))
        self.wait(1.5)
        self.play(FadeOut(cubic_formula)) # Fade out formula to reduce clutter during animation

        # De Casteljau visualization for Cubic
        t_tracker = ValueTracker(0) # Reset t_tracker

        # Level 1 Lerp
        dot_A = Dot(color=BLUE).add_updater(lambda m: m.move_to(lerp(p0.get_center(), p1.get_center(), t_tracker.get_value())))
        dot_B = Dot(color=BLUE).add_updater(lambda m: m.move_to(lerp(p1.get_center(), p2.get_center(), t_tracker.get_value())))
        dot_C = Dot(color=BLUE).add_updater(lambda m: m.move_to(lerp(p2.get_center(), p3.get_center(), t_tracker.get_value())))
        line_AB = Line(color=WHITE, stroke_width=2).add_updater(lambda m: m.put_start_and_end_on(dot_A.get_center(), dot_B.get_center()))
        line_BC = Line(color=WHITE, stroke_width=2).add_updater(lambda m: m.put_start_and_end_on(dot_B.get_center(), dot_C.get_center()))

        # Level 2 Lerp
        dot_D = Dot(color=ORANGE).add_updater(lambda m: m.move_to(lerp(dot_A.get_center(), dot_B.get_center(), t_tracker.get_value())))
        dot_E = Dot(color=ORANGE).add_updater(lambda m: m.move_to(lerp(dot_B.get_center(), dot_C.get_center(), t_tracker.get_value())))
        line_DE = Line(color=WHITE, stroke_width=2).add_updater(lambda m: m.put_start_and_end_on(dot_D.get_center(), dot_E.get_center()))

        # Level 3 Lerp (Final Bezier point)
        bezier_dot = Dot(color=GREEN).add_updater(
            lambda m: m.move_to(lerp(dot_D.get_center(), dot_E.get_center(), t_tracker.get_value()))
        )

        # Path trace
        bezier_path = TracedPath(bezier_dot.get_center, stroke_color=GREEN, stroke_width=4)

        self.add(bezier_path) # Add the path tracer to the scene
        self.play(
            Create(dot_A), Create(dot_B), Create(dot_C),
            Create(line_AB), Create(line_BC),
            Create(dot_D), Create(dot_E),
            Create(line_DE),
            Create(bezier_dot)
        )
        self.play(t_tracker.animate.set_value(1), run_time=7, rate_func=linear)
        self.wait(1)

        # Remove updaters
        dot_A.clear_updaters(); dot_B.clear_updaters(); dot_C.clear_updaters()
        line_AB.clear_updaters(); line_BC.clear_updaters()
        dot_D.clear_updaters(); dot_E.clear_updaters()
        line_DE.clear_updaters()
        bezier_dot.clear_updaters()

        # Keep final curve, control points, labels, cage lines
        # Fade out the intermediate construction
        self.play(
            FadeOut(dot_A), FadeOut(dot_B), FadeOut(dot_C),
            FadeOut(line_AB), FadeOut(line_BC),
            FadeOut(dot_D), FadeOut(dot_E),
            FadeOut(line_DE),
            FadeOut(bezier_dot),
            FadeOut(cubic_intro) # Fade out the title
        )
        # bezier_path (TracedPath) is still on screen here
        self.wait(1)

        # Create the initial static Bezier curve based on the final state of the trace
        initial_bezier_curve = CubicBezier(
            p0.get_center(), p1.get_center(), p2.get_center(), p3.get_center(),
            color=GREEN, stroke_width=4
        )

        # Remove the TracedPath and add the static curve
        self.remove(bezier_path)
        self.add(initial_bezier_curve)
        self.wait(0.1) # Small pause

        # --- 4. Control Point Influence (Keep similar to original) ---
        explanation = Text(
            "Control points determine the curve's shape",
            font_size=24
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(explanation))
        self.wait(1)

        # Move p1 (the first handle)
        new_p1_pos = p1.get_center() + UP * 1.5
        # Define the target shape for the transformation
        target_bezier_curve = CubicBezier(
            p0.get_center(), new_p1_pos, p2.get_center(), p3.get_center(), color=GREEN, stroke_width=4
        )
        new_line01 = Line(p0.get_center(), new_p1_pos, color=YELLOW, stroke_width=2)
        new_line12 = Line(new_p1_pos, p2.get_center(), color=YELLOW, stroke_width=2)

        # Transform the STATIC initial_bezier_curve
        self.play(
            p1.animate.move_to(new_p1_pos),
            p1_label.animate.next_to(new_p1_pos, UP),
            Transform(initial_bezier_curve, target_bezier_curve), # Transform the static curve
            Transform(line01, new_line01),
            Transform(line12, new_line12) # Also update line connected to p1
        )
        # Keep track of the current curve state (Transform modifies in-place)
        current_bezier_curve = initial_bezier_curve
        self.wait(1.5)

        # Clean up for next section
        self.play(
            FadeOut(dots), FadeOut(labels),
            FadeOut(lines), # Original control cage
            FadeOut(line01), FadeOut(line12), # Transformed lines
            FadeOut(current_bezier_curve), # Fade out the final curve
            FadeOut(explanation), FadeOut(section_title)
        )
        self.wait(0.5)

    def piecewise_bezier(self):
        section_title = Text("Piecewise Bezier Curves", font_size=36)
        section_title.to_edge(UP)
        
        self.play(Write(section_title))
        self.wait(1)
        
        explanation = Text(
            "Joining multiple Bezier curves with continuity constraints",
            font_size=24
        ).next_to(section_title, DOWN)
        
        self.play(Write(explanation))
        self.wait(1.5)
        
        # Create multiple Bezier curves connected together
        # First curve
        p0 = Dot(point=[-5, -1, 0], color=RED)
        p1 = Dot(point=[-4, 1, 0], color=GREEN)
        p2 = Dot(point=[-2, 1, 0], color=GREEN)
        p3 = Dot(point=[-1, -1, 0], color=RED)
        
        # Second curve - starts at p3
        p4 = Dot(point=[0, 1, 0], color=GREEN)
        p5 = Dot(point=[2, 1, 0], color=GREEN)
        p6 = Dot(point=[3, -1, 0], color=RED)
        
        # Third curve - starts at p6
        p7 = Dot(point=[4, 1, 0], color=GREEN)
        p8 = Dot(point=[5, 0, 0], color=GREEN)
        p9 = Dot(point=[5, -2, 0], color=RED)
        
        # Create curves
        bezier1 = CubicBezier(
            start_anchor=p0.get_center(),
            start_handle=p1.get_center(),
            end_handle=p2.get_center(),
            end_anchor=p3.get_center(),
            color=BLUE
        )
        
        bezier2 = CubicBezier(
            start_anchor=p3.get_center(),
            start_handle=p4.get_center(),
            end_handle=p5.get_center(),
            end_anchor=p6.get_center(),
            color=BLUE
        )
        
        bezier3 = CubicBezier(
            start_anchor=p6.get_center(),
            start_handle=p7.get_center(),
            end_handle=p8.get_center(),
            end_anchor=p9.get_center(),
            color=BLUE
        )
        
        # Create the curves sequentially
        self.play(Create(p0), Create(p3), Create(p6), Create(p9))
        self.wait(0.5)
        
        self.play(
            Create(p1), Create(p2),
            Create(p4), Create(p5),
            Create(p7), Create(p8)
        )
        self.wait(0.5)
        
        self.play(Create(bezier1))
        self.wait(0.5)
        self.play(Create(bezier2))
        self.wait(0.5)
        self.play(Create(bezier3))
        self.wait(1)
        
        # Highlight continuity
        continuity_text = Text(
            "To ensure smoothness, we need position and velocity continuity",
            font_size=24
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(continuity_text))
        self.wait(1)
        
        # Highlight the junction points
        junction1 = Circle(radius=0.2, color=YELLOW).move_to(p3.get_center())
        junction2 = Circle(radius=0.2, color=YELLOW).move_to(p6.get_center())
        
        self.play(Create(junction1), Create(junction2))
        self.wait(1)
        
        # Add tangent vectors to show continuity
        tangent1_start = Line(
            p2.get_center(), p3.get_center(), color=YELLOW_A, stroke_width=3
        )
        tangent1_end = Line(
            p3.get_center(), p4.get_center(), color=YELLOW_A, stroke_width=3
        )
        
        tangent2_start = Line(
            p5.get_center(), p6.get_center(), color=YELLOW_A, stroke_width=3
        )
        tangent2_end = Line(
            p6.get_center(), p7.get_center(), color=YELLOW_A, stroke_width=3
        )
        
        self.play(
            Create(tangent1_start), Create(tangent1_end),
            Create(tangent2_start), Create(tangent2_end)
        )
        self.wait(1)
        
        # Clean up
        self.play(
            FadeOut(p0), FadeOut(p1), FadeOut(p2), FadeOut(p3),
            FadeOut(p4), FadeOut(p5), FadeOut(p6), FadeOut(p7),
            FadeOut(p8), FadeOut(p9),
            FadeOut(bezier1), FadeOut(bezier2), FadeOut(bezier3),
            FadeOut(junction1), FadeOut(junction2),
            FadeOut(tangent1_start), FadeOut(tangent1_end),
            FadeOut(tangent2_start), FadeOut(tangent2_end),
            FadeOut(continuity_text), FadeOut(explanation),
            FadeOut(section_title)
        )
        self.wait(0.5)

    def autonomous_driving_application(self):
        section_title = Text("Application: Symmetric Concave Curve", font_size=36).to_edge(UP) # 更新标题
        self.play(Write(section_title))
        self.wait(1)

        # 道路和车道线设置
        road = Rectangle(height=2, width=12, color=GRAY, fill_opacity=0.5)
        road.center()
        lane_divider = DashedLine(
            start=road.get_left(), end=road.get_right(),
            dash_length=0.25, color=YELLOW
        ).move_to(road.get_center())
        self.play(Create(road), Create(lane_divider))
        self.wait(0.5)

        # 障碍物放在中心 (x=0)
        obstacle = Rectangle(height=0.8, width=0.8, color=DARK_GRAY, fill_opacity=1).move_to(ORIGIN)
        self.play(Create(obstacle))
        self.wait(0.5)

        # 车辆设置
        car = Rectangle(height=0.6, width=1, color=RED, fill_opacity=1)
        side_x = 5.0 # 稍微拉开点距离
        top_y = 0.5
        bottom_y = -0.5
        car_start_pos = LEFT * side_x + UP * top_y
        car.move_to(car_start_pos)
        self.play(Create(car))
        self.wait(0.5)

        # 解释文字
        explanation = Text(
            "Planning a symmetric concave curve", # 更新解释
            font_size=24
        ).next_to(section_title, DOWN)
        self.play(Write(explanation))
        self.wait(1)

        # --- 定义3个关键点 ---
        wp1 = LEFT * side_x + UP * top_y      # 起点 (左上)
        wp2 = ORIGIN + DOWN * bottom_y * 1.5  # 最低点 (障碍物正下方, y值可以调整深度)
        wp3 = RIGHT * side_x + UP * top_y     # 终点 (右上)

        # --- 定义控制点handle的偏移量以实现对称 ---
        # 控制起点/终点handle的水平偏移（影响曲线起始/结束的坡度）
        handle_x_offset_outer = 2.5
        # 控制起点/终点handle的垂直偏移（影响曲线的弯曲程度）
        handle_y_offset_outer = -2.0 # 负值表示向下拉
        # 控制最低点wp2两边handle的水平偏移（影响底部曲线的平坦度）
        handle_x_offset_inner = 1.8

        # --- 定义2段贝塞尔曲线 (对称设计) ---

        # Segment 1: 向下转弯 (wp1 -> wp2)
        path1 = CubicBezier(
            start_anchor=wp1,
            start_handle=wp1 + RIGHT * handle_x_offset_outer + UP * handle_y_offset_outer, # 注意y偏移方向
            end_handle=wp2 + LEFT * handle_x_offset_inner, # 控制到达最低点的曲线
            end_anchor=wp2,
            color=BLUE
        )

        # Segment 2: 向上转弯 (wp2 -> wp3)
        # G1/C1 continuity: 使第二个handle与第一个handle相对于wp2点对称
        handle2_start = wp2 + RIGHT * handle_x_offset_inner # 水平距离相等，方向相反
        path2 = CubicBezier(
            start_anchor=wp2,
            start_handle=handle2_start,
            end_handle=wp3 + LEFT * handle_x_offset_outer + UP * handle_y_offset_outer, # 与path1的start_handle对称
            end_anchor=wp3,
            color=BLUE
        )

        # 显示完整路径
        full_path = VGroup(path1, path2)
        self.play(Create(full_path), run_time=2)
        self.wait(1)

        # 高亮连接点 (wp2)
        junction2 = Dot(wp2, color=YELLOW, radius=0.1)
        junctions = VGroup(junction2) # 只有一个连接点

        continuity_highlight = Text("Symmetric Smooth Join", font_size=20).next_to(junctions, DOWN)
        self.play(Create(junctions), Write(continuity_highlight))
        self.wait(1.5)
        self.play(FadeOut(junctions), FadeOut(continuity_highlight))

        # 动画：车辆沿路径行驶
        self.play(MoveAlongPath(car, path1), run_time=1.5) # 第一段曲线
        self.play(MoveAlongPath(car, path2), run_time=1.5) # 第二段曲线
        self.wait(1)

        # 保留优点列表部分代码不变
        benefits_items = [
            "Smooth transitions between path segments",
            "Continuous steering avoids jerky movements",
            "Safe navigation around the obstacle",
        ]
        benefits = VGroup()
        for i, item_text in enumerate(benefits_items):
             bullet = Dot(color=BLUE).scale(0.8)
             text = Text(item_text, font_size=24)
             bullet_point = VGroup(bullet, text)
             text.next_to(bullet, RIGHT, buff=0.2)
             bullet_point.arrange(RIGHT, aligned_edge=LEFT)
             if i == 0:
                 bullet_point.next_to(road, UP, buff=0.5)
             else:
                 bullet_point.next_to(benefits[-1], DOWN, aligned_edge=LEFT, buff=0.3)
             benefits.add(bullet_point)
        for item in benefits:
            self.play(FadeIn(item, shift=UP*0.2), run_time=0.5)
            self.wait(0.3)
        self.wait(1)

        # 清理现场
        self.play(
            FadeOut(benefits), FadeOut(explanation),
            FadeOut(full_path),
            FadeOut(car), FadeOut(road), FadeOut(lane_divider),
            FadeOut(obstacle),
            FadeOut(section_title)
        )
        self.wait(0.5)

    def conclusion(self):
        title = Text("Summary", font_size=48)
        self.play(Write(title))
        self.wait(1)
        
        # Custom bullet points implementation
        summary_items = [
            "Bezier curves provide smooth mathematical curves",
            "Piecewise Bezier curves connect multiple segments",
            "They ensure continuity in position, velocity and acceleration",
            "Perfect for autonomous vehicle path planning"
        ]
        
        # Create a VGroup to hold all bullet points
        summary = VGroup()
        
        # Create each bullet point with a dot and text
        for i, item_text in enumerate(summary_items):
            bullet = Dot(color=BLUE).scale(0.8)
            text = Text(item_text, font_size=28)
            bullet_point = VGroup(bullet, text)
            text.next_to(bullet, RIGHT, buff=0.2)
            bullet_point.arrange(RIGHT, aligned_edge=LEFT)
            
            if i == 0:
                bullet_point.next_to(title, DOWN, buff=0.5)
            else:
                bullet_point.next_to(summary[-1], DOWN, aligned_edge=LEFT, buff=0.5)
                
            summary.add(bullet_point)
        
        # Display each bullet point one by one
        for item in summary:
            self.play(Create(item[0]), Write(item[1]))
            self.wait(0.5)
            
        self.wait(1.5)
        
        thanks = Text("Thanks for watching!", font_size=36, color=BLUE)
        thanks.to_edge(DOWN, buff=1)

        self.play(FadeOut(title, summary))
        
        self.play(Write(thanks))
        self.wait(2)

# Make sure to import necessary Manim components like DecimalNumber, ValueTracker, TracedPath
# Add imports if missing: from manim import DecimalNumber, ValueTracker, TracedPath, linear
# The code assumes standard Manim colors like RED, GREEN, BLUE, YELLOW, WHITE, ORANGE are available.
