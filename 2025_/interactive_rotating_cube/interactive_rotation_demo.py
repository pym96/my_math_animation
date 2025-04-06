from manim import *

class InteractiveRotationDemo(Scene):
    def construct(self):
        # Title
        title = Text("Interactive Rotation Matrices", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create interactive elements
        slider_x = Rectangle(height=0.2, width=4).set_fill(RED, opacity=0.5)
        slider_y = Rectangle(height=0.2, width=4).set_fill(GREEN, opacity=0.5)
        slider_z = Rectangle(height=0.2, width=4).set_fill(BLUE, opacity=0.5)
        
        # Labels for sliders
        label_x = Text("X Rotation (α)", font_size=24).next_to(slider_x, LEFT)
        label_y = Text("Y Rotation (β)", font_size=24).next_to(slider_y, LEFT)
        label_z = Text("Z Rotation (γ)", font_size=24).next_to(slider_z, LEFT)
        
        # Group sliders
        slider_group = VGroup(
            VGroup(label_x, slider_x),
            VGroup(label_y, slider_y),
            VGroup(label_z, slider_z),
        ).arrange(DOWN, buff=0.5).to_edge(LEFT)
        
        self.play(Create(slider_group))
        
        # Adding instructions
        instructions = Text(
            "In an interactive application, you could:\n"
            "• Drag these sliders to change rotation angles\n"
            "• See the rotation matrices update in real-time\n"
            "• Watch the cube rotate according to your inputs",
            font_size=24
        ).to_edge(RIGHT)
        
        self.play(Write(instructions))
        
        # Animate sliders to show the concept
        dot_x = Dot().move_to(slider_x.get_left())
        dot_y = Dot().move_to(slider_y.get_left())
        dot_z = Dot().move_to(slider_z.get_left())
        
        self.play(
            Create(dot_x),
            Create(dot_y),
            Create(dot_z),
        )
        
        # Animate the dots moving along the sliders
        self.play(
            dot_x.animate.move_to(slider_x.get_right()),
            dot_y.animate.move_to(slider_y.get_right()),
            dot_z.animate.move_to(slider_z.get_right()),
            run_time=3
        )
        
        self.wait()
        
        # Show example rotation matrix changing
        matrix_title = Text("Rotation Matrix:", font_size=24)
        matrix_title.next_to(instructions, DOWN, buff=1)
        matrix_title.to_edge(RIGHT)
        self.play(Write(matrix_title))
        
        # Display a rotation matrix that updates
        matrix_text = Text(
            "[[1, 0, 0],\n [0, 1, 0],\n [0, 0, 1]]", 
            font_size=24
        ).next_to(matrix_title, DOWN)
        self.play(Write(matrix_text))
        
        # Animate the matrix changing
        self.play(
            matrix_text.animate.become(
                Text(
                    "[[0.7, 0, 0.7],\n [0, 1, 0],\n [-0.7, 0, 0.7]]", 
                    font_size=24
                ).next_to(matrix_title, DOWN)
            )
        )
        
        self.play(
            matrix_text.animate.become(
                Text(
                    "[[0.7, -0.7, 0],\n [0.7, 0.7, 0],\n [0, 0, 1]]", 
                    font_size=24
                ).next_to(matrix_title, DOWN)
            )
        )
        
        self.play(
            matrix_text.animate.become(
                Text(
                    "[[0.5, -0.5, 0.7],\n [0.5, 0.5, 0.7],\n [-0.7, 0, 0.5]]", 
                    font_size=24
                ).next_to(matrix_title, DOWN)
            )
        )
        
        # Final note
        final_note = Text(
            "A complete interactive application would connect these sliders\n"
            "to the 3D cube rotation and matrix calculations in real-time.",
            font_size=24
        ).to_edge(DOWN)
        
        self.play(Write(final_note))
        self.wait(2)

if __name__ == "__main__":
    scene = InteractiveRotationDemo()
    scene.render() 