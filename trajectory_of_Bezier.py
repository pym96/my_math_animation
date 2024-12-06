from manim import *

class CoordsToPointExample(Scene):
    def construct(self):
       # 使用 Axes 作为坐标系
        grid = NumberPlane(
            x_range=(-5, 5),   # 设置 x 轴范围
            y_range=(-5, 5),   # 设置 y 轴范围
            axis_config={"color": BLUE},
        ).add_coordinates()  # 显示坐标轴上的数值


        intro_words = Text("""
            The original motivation for manim was to
            better illustrate mathematical functions
            as transformations.
        """)
        intro_words.to_edge(UP)

        self.play(Write(intro_words))
        self.wait(2)

        matrix = [[1, 1], [0, 1]]
        linear_transform_words = VGroup(
            Text("This is what the matrix"),
            IntegerMatrix(matrix, include_background_rectangle=True),
            Text("looks like")
        )
        
        linear_transform_words.arrange(RIGHT)
        linear_transform_words.to_edge(UP)
        linear_transform_words.set_stroke(BLACK, 10, background=True)

        # self.add(plane, dot_scene, ax, dot_axes, lines)
        self.play(Create(grid),FadeTransform(intro_words, linear_transform_words))
        self.wait(1)

        point1 = Dot(grid.coords_to_point(-1, -1), color=WHITE)
        point2 = Dot(grid.coords_to_point(0, 2), color=WHITE)
        point3 = Dot(grid.coords_to_point(1, 1), color=WHITE)

        # Create the points one by one
        self.play(Create(point1))
        self.play(Create(point2))
        self.play(Create(point3))

        line1 = Line(point1.get_center(), point2.get_center(), color=WHITE)
        line2 = Line(point3.get_center(), point2.get_center(), color=WHITE)

        self.play(Create(line1))
        self.play(Create(line2))

        self.wait(2)