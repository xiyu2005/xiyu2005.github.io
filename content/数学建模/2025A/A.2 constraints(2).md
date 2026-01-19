设真目标的下底面圆心为 $R(0, 200, 0)$

设无人机的出发位置为 $(x_0, y_0, z_0)$，起爆点的时空坐标 $(x,y,z,t)$ 与决策向量 $(v_{FY_j}, \alpha_j, t_{drop,j,k}, t_{fuse,j,k})$ 之间满足：
$$
\begin{cases}
	x &= x_0 + (t_{drop,j,k} + t_{fuse,j,k}) v_{FY_j} \cos \alpha_j \\[0.5em]
	y &= y_0 + (t_{drop,j,k} + t_{fuse,j,k}) v_{FY_j} \sin \alpha_j \\[0.5em]
	z &= z_0 - \frac{1}{2} g t_{fuse,j,k}^2 \\[0.5em]
	t &= t_{drop,j,k} + t_{fuse,j,k}
\end{cases}
$$


基础物理约束：
$$
\begin{cases}
	70 \leqslant v_{FY_j} \leqslant 140 \\
	0 \leqslant \alpha_j < 2\pi \\
	t_{drop,j,k} \geqslant 0 \\
    t_{fuse,j,k} \geqslant 0 \\
    z_{det,j,k}(X) > 0
\end{cases}
$$



启发式约束：
$$
\begin{cases}
	0 \leqslant \alpha_1 \leqslant \pi \enspace (\text{针对第二问}) \\[0.5em]
	\frac{y_m}{x_m} x \leqslant y \leqslant \frac{y_m - y_t}{x_m} x + y_t \\[0.5em]
	x \tan \theta_i - \frac{r_t}{\cos \theta} \leqslant z \leqslant x \tan \theta_i + \frac{r_t}{\cos \theta} + v_{drop} t_{life}
\end{cases}
$$
其中 $\theta_i = \arctan \dfrac{z_{m_i}}{x_{m_i}}$ 为面 $ROM_i$ 与 $xOy$ 平面的锐二面角，$v_{drop} = 3 \,m/s$ 为烟幕云团下降的速度，$t_{life} = 20 \, s$ 为烟幕弹爆炸后的有效遮蔽时间，$y_t = 200 \, m$ 为真目标的纵坐标



第一个不等式：由于导弹在 $xOz$ 平面内运动，而真目标位于 $y$ 轴正半轴，故烟幕起爆位置 $y \geqslant 0$ 更优，由此可得 $0 \leqslant \alpha_1 \leqslant \pi$

第二个不等式：烟幕起爆位置在 $xOy$ 平面上的投影位于 $\triangle ROM_i$ 在 $xOy$ 平面上的投影内部

第三个不等式：存在 $t \in [t_{drop,j,k} + t_{fuse,j,k}, t_{drop,j,k} + t_{fuse,j,k} + t_{life}]$，使得烟幕云团在 $t$ 时刻与 $\triangle ROM_i$ 存在交点



对上述约束进行展开后，得到
$$
\begin{cases}
	(x_m v_y - y_m v_x + y_t v_x)(t_d + t_e) \leqslant v_m x_0 - x_m y_0 - y_t (x_m - x_0) \\[0.5em]
	(x_m v_y - y_m v_x)(t_d + t_e) \geqslant y_m x_0 - x_m y_0 \\[0.5em]
	z_0 - x_0 \tan \theta - \frac{r}{\cos \theta} - v_{drop} t_{life} \leqslant v_x (t_d + t_e) \tan \theta + \frac{1}{2} g t_e^2 \leqslant z_0 - x_0 \tan \theta + \frac{r}{\cos \theta}
\end{cases}
$$
全部用决策向量的元素表示，得到：
$$
\begin{cases}
	v_{FY_j} [x_m \sin \alpha_j + (y_t - y_m) \cos \alpha_j](t_{drop,j,k} + t_{fuse,j,k}) \leqslant v_{m_i} x_0 - x_{m_i} y_0 - y_t (x_{m_i} - x_0) \\[0.5em]
	v_{FY_j} (x_{m_i} \sin \alpha_j - y_{m_i} \cos \alpha_j)(t_{drop,j,k} + t_{fuse,j,k}) \geqslant y_{m_i} x_0 - x_{m_i} y_0 \\[0.5em]
	z_0 - x_0 \tan \theta_i - \frac{r}{\cos \theta_j} - v_{drop} t_{life} \leqslant v_{FY_j} (t_{drop,j,k} + t_{fuse,j,k}) \cos \alpha_j \tan \theta_i + \frac{1}{2} g t_e^2 \leqslant z_0 - x_0 \tan \theta_i + \frac{r}{\cos \theta_i}
\end{cases}
$$










