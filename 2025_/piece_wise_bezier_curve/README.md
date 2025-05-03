# Piecewise Bezier Curves for Autonomous Driving Animation

This project contains a Manim animation tutorial that explains piecewise Bezier curves and their application in autonomous driving.

## Overview

The animation covers:
1. Introduction to Bezier curves
2. Piecewise Bezier curves and continuity constraints
3. Application in autonomous driving path planning
4. Benefits and summary

## Requirements

- Manim: https://docs.manim.community/en/stable/installation.html
- Python 3.7+
- NumPy

## How to Run

To render the animation in low quality (faster):

```bash
manim -ql ps_bezier.py PiecewiseBezierTutorial
```

To render the animation in high quality:

```bash
manim -qh ps_bezier.py PiecewiseBezierTutorial
```

To render a specific section only (for development):

```bash
# Example: Render only the introduction
manim -ql ps_bezier.py PiecewiseBezierTutorial.introduction
```

## Customization

You can customize the animation by modifying:
- Colors and styles
- Duration of waits
- Bezier curve control points
- Text content and explanations

## Animation Structure

The animation is structured into the following sections:

1. `introduction()`: Introduces the topic
2. `bezier_basics()`: Explains what Bezier curves are
3. `piecewise_bezier()`: Demonstrates piecewise Bezier curves
4. `autonomous_driving_application()`: Shows application in autonomous driving
5. `conclusion()`: Summarizes key points

## Troubleshooting

### TeX-related errors

If you encounter TeX-related errors such as:
```
FileNotFoundError: [Errno 2] No such file or directory: 'media/Tex/._ad72b6d871aefab8.log'
```

The script includes two fixes:
1. A custom TeX template configuration at the top of the file
2. A try/except block for the Bezier formula that falls back to regular Text if MathTex fails

If you still encounter issues, you can try:
- Ensuring your LaTeX installation is complete with all required packages
- Running with the `--tex_template` flag to specify a custom template:
  ```bash
  manim -ql --tex_template=custom_template.tex ps_bezier.py PiecewiseBezierTutorial
  ```
- Creating a `.manim.cfg` file in your project directory with appropriate TeX configuration

## Output

The rendered video will be saved in the `media` folder. 