from manim import *

class BezierWeightAnimation(Scene):
    def construct(self):
        # 设置标题
        title = Text("Cubic Bezier Curve Weights", font_size=36)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))
        
        # 创建公式
        cubic_formula = MathTex(
            r"P(t) = (1 - t)^3 P_0 + 3(1 - t)^2 t P_1 + 3(1 - t) t^2 P_2 + t^3 P_3",
            font_size=32
        ).next_to(title, DOWN)
        self.play(Write(cubic_formula))
        self.wait(1)

        # 展开后的公式
        expanded_formula = MathTex(
            r"P(t) = \big(1 - 3t + 3t^2 - t^3\big)P_0 +",
            r"\big(3t - 6t^2 + 3t^3\big)P_1 +",
            r"\big(3t^2 - 3t^3\big)P_2 +",
            r"\big(t^3\big)P_3",
            font_size=28
        ).next_to(cubic_formula, DOWN, buff=0.5)

        # 定义权重函数
        weight_functions = {
            "P_0": lambda t: (1 - t)**3,
            "P_1": lambda t: 3 * (1 - t)**2 * t,
            "P_2": lambda t: 3 * (1 - t) * t**2,
            "P_3": lambda t: t**3,
        }
        
        colors = {"P_0": RED, "P_1": BLUE, "P_2": GREEN, "P_3": YELLOW}

        # 不同项的颜色
        expanded_formula[0].set_color(RED)    # P_0 系数
        expanded_formula[1].set_color(BLUE)   # P_1 系数
        expanded_formula[2].set_color(GREEN)  # P_2 系数
        expanded_formula[3].set_color(YELLOW) # P_3 系数
        
        self.play(Transform(cubic_formula, expanded_formula))
        self.wait(1)

        # 动态展示各系数
        weights = VGroup(
            MathTex(r"1 - 3t + 3t^2 - t^3", color=RED, font_size=23),
            MathTex(r"3t - 6t^2 + 3t^3", color=BLUE, font_size=23),
            MathTex(r"3t^2 - 3t^3", color=GREEN, font_size=23),
            MathTex(r"t^3", color=YELLOW, font_size=23)
        )
        
        weights.arrange(DOWN, buff=0.5).to_edge(LEFT)

        # 显示权重
        for weight in weights:
            self.play(FadeIn(weight, shift=DOWN))
            self.wait(0.5)
        
        # 动态演示 t 变化
        # t_label = MathTex(r"t = 0.0", font_size=28)

        # 初始化 t_tracker 在此时
        t_tracker = ValueTracker(0)

       
        # self.play(FadeIn(t_label))
        self.wait(1)

        # 曲线图动态变化
        graph_axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 1.2, 0.1],
            axis_config={"font_size": 20},
            tips=False
        ).scale(0.7).to_edge(DOWN)

        # 设置较小的坐标轴标签字体大小
        graph_labels = VGroup(
            MathTex("t", font_size=20).next_to(graph_axes.x_axis, RIGHT),
            MathTex("Weight", font_size=20).next_to(graph_axes.y_axis, UP)
        )

        # 绘制坐标系和标签
        self.play(Create(graph_axes), Write(graph_labels))
        
        # 各系数的曲线
        weight_graphs = {
            "P_0": graph_axes.plot(lambda t: (1 - t)**3, color=RED, x_range=[0, 1]),
            "P_1": graph_axes.plot(lambda t: 3 * (1 - t)**2 * t, color=BLUE, x_range=[0, 1]),
            "P_2": graph_axes.plot(lambda t: 3 * (1 - t) * t**2, color=GREEN, x_range=[0, 1]),
            "P_3": graph_axes.plot(lambda t: t**3, color=YELLOW, x_range=[0, 1])
        }

        dynamic_weights = VGroup(*[
            DecimalNumber(0, color=color, font_size=28).add_updater(
                lambda m, func=func: m.set_value(func(t_tracker.get_value()))
            ) for func, color in zip(weight_functions.values(), colors.values())
        ])
        dynamic_weights.arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=1.5)

        for key, graph in weight_graphs.items():
            self.play(Create(graph), run_time=2)
        
        self.wait(1)

        # 动态点展示
        dynamic_points = VGroup(*[
            Dot(color=color, radius=0.1).move_to(
                graph_axes.c2p(0, func(0))
            ).add_updater(
                lambda m, func=func: m.move_to(
                    graph_axes.c2p(t_tracker.get_value(), func(t_tracker.get_value()))
                )
            ) for func, color in zip(weight_functions.values(), colors.values())
        ])

        # 将动态点添加到场景中
        self.play(FadeIn(dynamic_points, dynamic_weights))

        # 更新 t_tracker 的值
        self.play(
            t_tracker.animate.set_value(1),
            run_time=5, rate_func=linear
        )

        # 最终停留的时间
        self.wait(2)

        self.clear()

        self.wait(1)