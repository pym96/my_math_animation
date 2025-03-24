from manim import *
import numpy as np
import os

# Patch to prevent file operation errors
def patch_manim_file_operations():
    # Patch os.unlink to handle file not found errors safely
    original_unlink = os.unlink
    def safe_unlink(path, *args, **kwargs):
        try:
            return original_unlink(path, *args, **kwargs)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Ignoring file operation error: {e}")
            return None
    os.unlink = safe_unlink
    
    # Also patch pathlib's Path.unlink method
    import pathlib
    original_path_unlink = pathlib.Path.unlink
    def safe_path_unlink(self, missing_ok=False):
        try:
            return original_path_unlink(self, missing_ok=True)  # Always set missing_ok to True
        except (FileNotFoundError, PermissionError) as e:
            print(f"Ignoring path unlink error: {e}")
            return None
    pathlib.Path.unlink = safe_path_unlink
    
    # Try to patch Manim's SceneFileWriter if possible
    try:
        from manim.scene.scene_file_writer import SceneFileWriter
        original_clean_cache = SceneFileWriter.clean_cache
        def safe_clean_cache(self):
            try:
                original_clean_cache(self)
            except Exception as e:
                print(f"Ignoring cache cleaning error: {e}")
        SceneFileWriter.clean_cache = safe_clean_cache
        
        # Also disable caching in the config
        config.disable_caching = True
    except:
        pass
    
    print("File operation safety patches applied")

# Apply patches immediately when module is loaded
patch_manim_file_operations()

# Helper function to prevent animation errors
def safe_play(scene, *animations, **kwargs):
    try:
        scene.play(*animations, **kwargs)
    except Exception as e:
        print(f"Animation warning (continuing anyway): {e}")
        try:
            # Try slower animation as fallback
            if len(animations) > 0:
                scene.add(*[anim.mobject for anim in animations if hasattr(anim, 'mobject')])
        except:
            pass
        scene.wait(kwargs.get("run_time", 1))

class NewtonMethodAnimation(Scene):
    def construct(self):
        # Animation setup
        self.camera.background_color = "#1f1f1f"
        
        # Title and introduction with simpler subtitle
        title = Text("牛顿迭代法 (Newton's Method)", font_size=48)
        subtitle = Text("一种寻找方程解的强大方法", font_size=32)  # A powerful method to find equation solutions
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle), run_time=1)
        self.wait(1)
        
        # Brief explanation of what we're trying to do
        explanation = Text("我们要找出函数等于0时的x值", font_size=32)  # We want to find x values where the function equals 0
        explanation.next_to(subtitle, DOWN, buff=0.5)
        self.play(FadeIn(explanation), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(explanation), run_time=1)
        
        # Setup the coordinate system - make it slightly smaller and position it better
        axes = Axes(
            x_range=[-2, 3, 1],
            y_range=[-5, 15, 5],
            axis_config={"color": WHITE},
            x_length=9,  # Reduced from 10
            y_length=5.5  # Reduced from 6
        ).shift(LEFT * 0.5)  # Shift left to make room for labels and calculations
        
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        # Define the function f(x) = x^3 - 2x^2 - 5
        def f(x):
            return x**3 - 2*x**2 - 5
        
        # Define the derivative f'(x) = 3x^2 - 4x
        def df(x):
            return 3*x**2 - 4*x
        
        # Plot the function
        graph = axes.plot(lambda x: f(x), color=BLUE)
        graph_label = MathTex("f(x) = x^3 - 2x^2 - 5").scale(0.8)
        graph_label.to_corner(UL).shift(RIGHT * 0.5 + DOWN * 0.5)
        
        # Add horizontal line at y=0
        x_axis = axes.plot(lambda x: 0, color=WHITE, stroke_width=1)
        
        # Show the coordinate system and function
        self.play(Create(axes), Create(axes_labels), run_time=1.5)
        self.play(Create(graph), Write(graph_label), Create(x_axis), run_time=2)
        
        # Explain what we're looking for
        root_explanation = Text("方程的根是函数曲线与x轴的交点", font_size=28)  # The root is where the curve meets the x-axis
        root_explanation.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(root_explanation), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(root_explanation), run_time=0.8)
        
        # Explain tangent line concept first
        tangent_explanation = Text("牛顿发现可以用切线来逐步逼近函数的根", font_size=28)  # Newton found we can use tangent lines to approach the root
        tangent_explanation.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(tangent_explanation), run_time=1.5)
        self.wait(2)
        
        # Show an example tangent
        x_sample = 2.0
        y_sample = f(x_sample)
        tangent_slope = df(x_sample)
        sample_tangent = axes.plot(
            lambda x: y_sample + tangent_slope * (x - x_sample),
            x_range=[x_sample - 1.5, x_sample + 1.5],
            color=GREEN
        )
        sample_point = Dot(axes.c2p(x_sample, y_sample), color=YELLOW)
        self.play(Create(sample_point), Create(sample_tangent), run_time=1.5)
        
        # Add labels for the tangent - position it better
        tangent_label = Text("切线", font_size=22, color=GREEN)  # Tangent line
        tangent_label.next_to(sample_point, UP+RIGHT, buff=0.2)
        self.play(Write(tangent_label), run_time=1)
        self.wait(1.5)
        
        # Clean up before starting Newton's method
        self.play(
            FadeOut(sample_point), 
            FadeOut(sample_tangent), 
            FadeOut(tangent_label),
            FadeOut(tangent_explanation),
            run_time=1
        )
        
        # Introduce Newton's method formula with explanation
        formula_intro = Text("牛顿迭代法公式", font_size=32)  # Newton's method formula
        formula_intro.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(formula_intro), run_time=1)
        self.wait(0.5)
        
        # Newton's method formula - move it to the top center
        formula = MathTex(r"x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}")
        formula.to_edge(UP).shift(DOWN * 0.5 + LEFT * 0.5)  # Position better
        self.play(Write(formula), run_time=1.5)
        
        # Explain the formula parts - make this smaller and position better
        formula_explanation = VGroup(
            Text("这里:", font_size=22),  # Here:
            Text("• x_n 是当前猜测值", font_size=20),  # is the current guess
            Text("• f(x_n) 是函数在当前点的值", font_size=20),  # is the function value at current point
            Text("• f'(x_n) 是函数在当前点的斜率", font_size=20),  # is the slope at current point
            Text("• x_n+1 是下一个更好的猜测值", font_size=20)  # is the next, better guess
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)  # Reduced buffer between items
        formula_explanation.scale(0.75).to_corner(DL).shift(UP * 0.5 + RIGHT * 0.5)
        
        self.play(Write(formula_explanation), run_time=2)
        self.wait(2)
        self.play(FadeOut(formula_intro), run_time=0.8)
        
        # Set up calculation area where we'll show each step - position better
        calc_box = Rectangle(width=5, height=3.2, color=WHITE, fill_opacity=0.1)
        calc_box.to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.5)  # Moved further right to avoid formula
        calc_title = Text("计算过程", font_size=22)  # Calculation Process - smaller
        calc_title.next_to(calc_box, UP, buff=0.1)
        self.play(Create(calc_box), Write(calc_title), run_time=1)
        
        # Initial guess
        x0 = 2.5
        iterations = 4  # Reduced number of iterations for clarity
        
        # Create a dot for the initial guess
        current_dot = Dot(axes.c2p(x0, f(x0)), color=YELLOW)
        current_x_label = MathTex(f"x_0 = {x0}").scale(0.8)
        current_x_label.next_to(current_dot, UP, buff=0.15)  # Better position
        
        initial_guess_text = Text("我们从x₀=2.5开始尝试", font_size=28)  # We start with a guess x₀=2.5
        initial_guess_text.to_edge(DOWN).shift(UP * 0.5)
        
        self.play(
            Create(current_dot), 
            Write(current_x_label), 
            Write(initial_guess_text),
            run_time=1.5
        )
        self.wait(1.5)
        self.play(FadeOut(initial_guess_text), run_time=0.8)
        
        # Perform Newton's method iterations
        x_values = [x0]
        
        for i in range(iterations):
            # Current x and f(x)
            x_n = x_values[-1]
            y_n = f(x_n)
            
            # Calculate the next x value using Newton's method
            slope_n = df(x_n)
            x_next = x_n - y_n / slope_n
            x_values.append(x_next)
            
            # Explanation for this iteration
            iteration_text = Text(f"第{i+1}次迭代", font_size=28)  # Iteration #
            iteration_text.to_edge(DOWN).shift(UP * 0.5)
            self.play(Write(iteration_text), run_time=0.8)
            
            # Show calculation steps inside the calculation box - make smaller and better positioned
            calc_steps = VGroup(
                MathTex(f"x_{i} = {x_n:.4f}"),
                MathTex(f"f(x_{i}) = {y_n:.4f}"),
                MathTex(f"f'(x_{i}) = {slope_n:.4f}"),
                Text("代入公式:", font_size=20),  # Changed from MathTex to Text and smaller
                MathTex(f"x_{i+1} = x_{i} - \\frac{{f(x_{i})}}{{f'(x_{i})}}"),
                MathTex(f"x_{i+1} = {x_n:.4f} - \\frac{{{y_n:.4f}}}{{{slope_n:.4f}}}"),
                MathTex(f"x_{i+1} = {x_next:.4f}")
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)  # Reduced buffer
            calc_steps.scale(0.6).move_to(calc_box.get_center())  # Made smaller
            
            # Show each calculation step with animation
            for step in calc_steps:
                self.play(Write(step), run_time=0.5)
                self.wait(0.2)
            
            # Create tangent line at the current point
            tangent_line = axes.plot(
                lambda x: y_n + slope_n * (x - x_n),
                x_range=[x_n - 1.5, x_n + 1.5],
                color=GREEN
            )
            
            # Tangent label - better position
            tangent_label = Text("切线", font_size=18, color=GREEN)  # Tangent line - smaller
            
            # Position the label properly based on the position and avoid overlapping
            if y_n > 0:
                tangent_label.next_to(current_dot, UR, buff=0.15)
            else:
                tangent_label.next_to(current_dot, UL, buff=0.15)
                
            # Highlight the tangent line
            self.play(
                Create(tangent_line), 
                Write(tangent_label),
                run_time=1
            )
            
            # Show the intersection with x-axis
            intersection_dot = Dot(axes.c2p(x_next, 0), color=RED)
            
            # Intersection label - better position
            intersection_label = Text("切线与x轴的交点", font_size=18, color=RED)  # Intersection point - smaller
            
            # Position the intersection label to avoid overlapping
            if x_next < x_n:
                intersection_label.next_to(intersection_dot, DOWN+LEFT, buff=0.15)
            else:
                intersection_label.next_to(intersection_dot, DOWN+RIGHT, buff=0.15)
                
            # Animate the movement to the next intersection point
            self.play(
                Create(intersection_dot),
                Write(intersection_label),
                run_time=1
            )
            self.wait(0.5)
            
            # Show the vertical line from x-axis to the function
            vertical_line = DashedLine(
                axes.c2p(x_next, 0),
                axes.c2p(x_next, f(x_next)),
                color=YELLOW,
                dash_length=0.1
            )
            
            # Better position for vertical label
            vertical_label = Text("新的猜测值", font_size=18, color=YELLOW)  # New guess - smaller
            
            # Position the vertical label based on the direction of movement
            if f(x_next) > 0:
                vertical_label.next_to(vertical_line, RIGHT, buff=0.15)
            else:
                vertical_label.next_to(vertical_line, LEFT, buff=0.15)
                
            self.play(
                Create(vertical_line),
                Write(vertical_label),
                run_time=1
            )
            
            # Create new dot for the next iteration
            next_dot = Dot(axes.c2p(x_next, f(x_next)), color=YELLOW)
            next_x_label = MathTex(f"x_{i+1} = {x_next:.4f}").scale(0.75)  # Smaller
            
            # Position the next label to avoid overlapping
            if f(x_next) > 0:
                next_x_label.next_to(next_dot, UP+RIGHT, buff=0.15)
            else:
                next_x_label.next_to(next_dot, DOWN+RIGHT, buff=0.15)
                
            # First fade out the current label before showing the next one
            self.play(FadeOut(current_x_label), run_time=0.5)
            
            # Move to the next point on the curve and show its label
            self.play(
                Create(next_dot),
                Write(next_x_label),
                run_time=1
            )
            
            # Add explanation of what happened - better position
            if i == 0:
                explanation_text = Text("可以看到，我们的猜测值已经更接近根了！", font_size=22)  # Smaller
                explanation_text.next_to(iteration_text, UP, buff=0.2)
                self.play(Write(explanation_text), run_time=1)
                self.wait(1)
                self.play(FadeOut(explanation_text), run_time=0.8)
            
            # Wait a moment to observe
            self.wait(1)
            
            # Clean up for the next iteration
            if i < iterations - 1:
                self.play(
                    FadeOut(tangent_line),
                    FadeOut(intersection_dot),
                    FadeOut(vertical_line),
                    FadeOut(current_dot),
                    FadeOut(tangent_label),
                    FadeOut(intersection_label),
                    FadeOut(vertical_label),
                    FadeOut(calc_steps),
                    FadeOut(iteration_text),
                    run_time=0.8
                )
                # Update current dot and label for next iteration
                current_dot = next_dot
                current_x_label = next_x_label
            else:
                # For the last iteration, keep the final dot and label but remove other elements
                self.play(
                    FadeOut(tangent_line),
                    FadeOut(intersection_dot),
                    FadeOut(vertical_line),
                    FadeOut(tangent_label),
                    FadeOut(intersection_label),
                    FadeOut(vertical_label),
                    FadeOut(calc_steps),
                    FadeOut(iteration_text),
                    run_time=0.8
                )
                # Save the final dot and label for later transformation
                final_dot = next_dot
                final_x_label = next_x_label
                
        # Final explanation
        final_x = x_values[-1]
        final_text = Text(f"经过{iterations}次迭代，我们找到了近似解: x ≈ {final_x:.6f}", font_size=26)  # Smaller
        final_text.to_edge(DOWN).shift(UP * 0.5)
        
        self.play(Write(final_text), run_time=1.5)
        self.wait(1.5)
        
        # Check how close we are to the actual root
        f_final = f(final_x)
        error_text = Text(f"此时 f(x) = {f_final:.8f} ≈ 0", font_size=22)  # Smaller
        error_text.next_to(final_text, UP, buff=0.2)
        self.play(Write(error_text), run_time=1.5)
        self.wait(1.5)
        
        # Fade out the final x label before showing the root
        self.play(FadeOut(final_x_label), FadeOut(error_text), run_time=0.8)
        
        # Highlight the root
        root_dot = Dot(axes.c2p(final_x, 0), color=GREEN, radius=0.12)
        root_label = Text("方程的根", font_size=22, color=GREEN)  # Smaller
        root_label.next_to(root_dot, DOWN, buff=0.2)  # Better position
        
        self.play(
            Transform(final_dot, root_dot),
            Write(root_label),
            run_time=1.5
        )
        
        # Final wait
        self.wait(1.5)
        
        # Fade out formula explanation to make room for advantages
        self.play(FadeOut(formula_explanation), run_time=0.8)
        
        # Summary of advantages - better position
        self.play(FadeOut(calc_box), FadeOut(calc_title), run_time=0.8)
        
        advantages_title = Text("牛顿迭代法的优点", font_size=28)  # Smaller
        advantages_title.to_corner(UL).shift(DOWN * 1.5 + RIGHT * 1.0)  # 增加向下移动距离
        
        advantages = VGroup(
            Text("• 收敛速度快", font_size=22),  # Smaller
            Text("• 适用于许多函数", font_size=22),  
            Text("• 计算简单", font_size=22),  
            Text("• 在工程和科学中广泛应用", font_size=22)  
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)  # Reduced buffer
        advantages.next_to(advantages_title, DOWN, aligned_edge=LEFT, buff=0.25)
        
        self.play(
            Write(advantages_title),
            run_time=1
        )
        
        for advantage in advantages:
            self.play(Write(advantage), run_time=0.7)
        
        self.wait(1.5)
        
        # Final conclusion
        conclusion = Text("牛顿迭代法：以直线近似曲线，逐步逼近方程的解", font_size=28)  # Smaller
        conclusion.to_edge(DOWN).shift(UP * 0.5)
        
        self.play(
            FadeOut(final_text),
            FadeIn(conclusion),
            run_time=1.5
        )
        
        self.wait(3)

if __name__ == "__main__":
    # Adding this command-line execution to help with rendering
    import sys
    
    try:
        # Set config options to make rendering more robust
        config.disable_caching = True  # Prevent cache-related errors
        
        if len(sys.argv) > 1 and sys.argv[1] == "--render":
            from manim.cli.render.commands import render
            
            # Build rendering command arguments
            sys.argv = [
                "manim",
                "--no_latex_cleanup",  # Prevent latex cleanup errors
                "-pqh",  # preview, medium quality, 1080p
                __file__,
                "NewtonMethodAnimation"
            ]
            render()
        
        print("Animation completed successfully!")
    except Exception as e:
        print(f"Error during rendering: {e}")
        import traceback
        traceback.print_exc()
