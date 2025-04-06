# 交互式旋转矩阵演示


旋转矩阵演示:
<img width="1509" alt="Screenshot 2025-04-06 at 13 12 32" src="https://github.com/user-attachments/assets/235eb06e-89a1-4407-9cc9-8e8420ccadd9" />


## 项目描述

本项目包含多种旋转矩阵的可视化演示：

1. **交互式网页演示** - Three.js实现的3D交互演示，可实时拖动调整旋转角度
2. **Python ASCII艺术演示** - Python实现的命令行旋转立方体
3. **教学动画** - 使用Manim制作的旋转矩阵教学视频

## 文件结构

- `index.html` - 交互式旋转矩阵网页演示
- `rotation_cube.py` - Python版ASCII艺术旋转立方体
- `rotation_matrix_animation.py` - Manim教学动画脚本
- `interactive_rotation_demo.py` - Manim交互概念演示

## 功能特点

### 交互式网页演示 (index.html)

这是一个基于Three.js的交互式3D演示，功能包括：

- 实时调整X、Y、Z三个轴的旋转角度
- 动态显示各轴的旋转矩阵及组合旋转矩阵
- 多角度视图切换（正视图、俯视图、侧视图、等轴测视图）
- 彩色坐标轴和标签，便于识别

### Manim教学动画 (rotation_matrix_animation.py)

这是一系列使用Manim制作的教学动画，包含三个场景：

1. **RotationMatrixIntro** - 2D旋转矩阵基础
   - 从简单的2D坐标系和点的旋转开始
   - 解释如何用矩阵表示旋转
   - 展示不同角度的旋转矩阵
   
2. **RotationMatrix3D** - 3D旋转矩阵
   - 展示3D坐标系和立方体
   - 依次演示绕X轴、Y轴和Z轴的旋转
   - 展示组合旋转和旋转顺序的重要性
   
3. **RotationMatrixSummary** - 总结与进阶
   - 总结旋转矩阵的关键概念
   - 提供进一步学习的方向

## 如何使用

### 网页演示

1. 启动本地服务器：
   ```
   python -m http.server
   ```

2. 在浏览器中访问：
   ```
   http://localhost:8000
   ```

3. 使用滑块调整X、Y、Z轴的旋转角度，观察立方体的旋转和矩阵的变化。

4. 点击视角按钮切换不同的观察角度。

### Manim动画

运行各个教学动画场景：

```bash
# 2D旋转矩阵基础
python -m manim -p -ql rotation_matrix_animation.py RotationMatrixIntro

# 3D旋转矩阵
python -m manim -p -ql rotation_matrix_animation.py RotationMatrix3D

# 旋转矩阵总结
python -m manim -p -ql rotation_matrix_animation.py RotationMatrixSummary

# 交互概念演示
python -m manim -p -ql interactive_rotation_demo.py
```

### Python旋转立方体

运行ASCII艺术旋转立方体：

```bash
python rotation_cube.py
```

## 技术栈

- **Web**: HTML, CSS, JavaScript, Three.js, Math.js
- **Python动画**: Manim (Mathematical Animation Engine)
- **Python 3D**: NumPy

## 教学应用

本项目适用于：

- 线性代数教学
- 计算机图形学入门
- 3D游戏开发基础
- 机器人学旋转表示介绍

## 延伸阅读

若要深入了解旋转矩阵和3D变换，推荐探索：

- 四元数(Quaternions)
- 欧拉角(Euler Angles)
- 罗德里格斯旋转公式(Rodrigues' Rotation Formula)
