from manimlib import *
from scipy.integrate import solve_ivp
import numpy as np

# Lorenz 系统微分方程
def lorenz_system(t, state, sigma=10, rho=28, beta=8 / 3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# 使用 solve_ivp 求解微分方程
def solve_lorenz_system():
    state0 = [1.0, 0.0, 0.0]  # 初始条件
    t_span = (0, 25)  # 时间区间
    t_eval = np.linspace(t_span[0], t_span[1], 5000)  # 增加计算点数来提高轨迹光滑度
    solution = solve_ivp(lorenz_system, t_span, state0, t_eval=t_eval, method='RK45')
    return solution

class LorenzScene(ThreeDScene):
    def construct(self):
        # 获取 Lorenz 系统的解
        solution = solve_lorenz_system()

        # 创建 3D 坐标系
        axes = ThreeDAxes(
            x_range=(-50, 50, 5),
            y_range=(-50, 50, 5),
            z_range=(-0, 50, 5),
            width=16,
            height=16,
            depth=8
        )

        # 设置相机角度
        self.camera.frame.set_euler_angles(phi=30 * DEGREES, theta=30 * DEGREES)
        self.camera.frame.set_field_of_view(90)

        # 创建轨迹
        trajectory = VGroup()
        end_points = VGroup()

        for i in range(1, len(solution.t)):
            # 通过 c2p（坐标转化）将 (x, y, z) 转换为 3D 空间中的坐标
            point = axes.c2p(solution.y[0][i], solution.y[1][i], solution.y[2][i])

            # 使用 GlowDot 创建发光点
            glow_dot = GlowDot(point, color=BLUE, radius=0.1)  # Adjust radius as needed
            end_points.add(glow_dot)

            # 连接前一个点和当前点，形成一条线
            if i > 1:
                prev_point = axes.c2p(solution.y[0][i-1], solution.y[1][i-1], solution.y[2][i-1])
                trajectory.add(Line(prev_point, point, color=BLUE))

        # 将坐标轴和轨迹添加到场景中
        self.add(axes)
        self.add(trajectory)

        # 设置相机初始位置
        self.camera.position = 20 * RIGHT + 50 * UP + 2000 * OUT
        self.camera.frame.shift(UP * 2)

        # 播放动画：显示坐标轴和轨迹
        self.play(ShowCreation(axes))

        # for i in trajectory:
        #     end_points = trajectory[i].get_end()
        # 将相机移动到轨迹的中心
        # self.play(self.camera.frame.move_to(trajectory.get_center()))

        self.play(ShowCreation(trajectory))
        
        # self.play(ShowCreation(end_points))
        self.wait(2)
