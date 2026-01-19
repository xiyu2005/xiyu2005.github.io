设真目标的下底面圆心为 $R(0, 200, 0)$

设无人机的出发位置为 $(x_0, y_0, z_0)$，起爆点的时空坐标 $(x,y,z,t)$ 与决策向量 $(v_{FY_1}, \alpha_1, t_{drop,1,1}, t_{fuse,1,1})$ 之间满足：
$$
\begin{cases}
	x &= x_0 + (t_{drop,1,1} + t_{fuse,1,1}) v_{FY_1} \cos \alpha_1 \\[0.5em]
	y &= y_0 + (t_{drop,1,1} + t_{fuse,1,1}) v_{FY_1} \sin \alpha_1 \\[0.5em]
	z &= z_0 - \frac{1}{2} g t_e^2 \\[0.5em]
	t &= t_d + t_e
\end{cases}
$$


基础物理约束：
$$
\begin{cases}
	70 \leqslant v_{FY_1} \leqslant 140 \\
	0 \leqslant \alpha_1 < 2\pi \\
	t_{drop,1,1} \geqslant 0 \\
    t_{fuse,1,1} \geqslant 0 \\
    z_{det,1,1}(X) > 0
\end{cases}
$$



启发式约束：
$$
\begin{cases}
	0 \leqslant \alpha_1 \leqslant \pi \\[0.5em]
	y \leqslant -\frac{x}{100} + 200 \\[0.5em]
	\frac{1}{10} x - 10 \cos \theta \leqslant z \leqslant \frac{1}{10} x + 10 \cos \theta + v_{drop} t_{life}
\end{cases}
$$
其中 $\theta = \arctan \dfrac{1}{10}$ 为面 $ROM_1$ 与 $xOy$ 平面的锐二面角，$v_{drop} = 3 \,m/s$ 为烟幕云团下降的速度，$t_{life} = 20s$ 为烟幕弹爆炸后的有效遮蔽时间



第一个不等式：由于导弹在 $xOz$ 平面内运动，而真目标位于 $y$ 轴正半轴，故烟幕起爆位置 $y \geqslant 0$ 更优，由此可得 $0 \leqslant \alpha_1 \leqslant \pi$

第二个不等式：烟幕起爆位置在 $xOy$ 平面上的投影位于 $\triangle ROM_1$ 在 $xOy$ 平面上的投影内部

第三个不等式：存在 $t \in [t_{drop,1,1} + t_{fuse,1,1}, t_{drop,1,1} + t_{fuse,1,1} + t_{life}]$，使得烟幕云团在 $t$ 时刻与 $\triangle ROM_1$ 存在交点

