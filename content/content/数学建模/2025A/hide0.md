假设导弹位置为 $O$，烟幕弹起爆后产生的球状烟幕云团中心为 $P$，需要判断是否被遮蔽的点为 $Q$. 若 $O$，$P$，$Q$ 三点满足
$$
|\vec{OP}| \leqslant r \enspace
\text{或} \enspace
\begin{cases}
	\left( \frac{\vec{OP} \cdot \vec{OQ}}{\left| \vec{OQ} \right|} \right)^2 + r^2 \leqslant \left| \vec{OP} \right|^2 , \\
	\vec{OP} \cdot \vec{OQ} \geqslant 0
\end{cases}
$$
推导：

我们将 $O$, $P$, $Q$ 三点的位置关系分为三类：

1. $|\vec{OP}| \leqslant r$

   此情况下，$O$ 位于以 $P$ 为中心的烟幕云团内部，因而不论 $Q$ 位于何处均能被烟幕云团遮蔽

2. $|\vec{OP}| \geqslant r$，并且 $|\vec{OP} \cdot \vec{OQ}| \geqslant 0$

   此情况下，令 $S$ 为面 $QOP$ 内球 $P$ 过 $O$ 的切线，令 $\theta = \angle QOP, \enspace \varphi = \angle SOP$，满足 $\theta \in [0, \pi], \enspace \varphi \in [0, \pi/2]$，则 $Q$ 被烟幕云团遮蔽的充要条件为 $\theta \leqslant \varphi$。由于余弦函数在 $[0, \pi]$ 上单调递减，条件可以转化为
   $$
   \cos \theta \geqslant \cos \varphi.
   $$
    由几何关系可得
   $$
   \begin{cases}
   	\cos \theta = \frac{\vec{OP} \cdot \vec{OQ}}{\left| \vec{OP} \right| \left| \vec{OQ} \right|} \\[1em]
   	\sin \varphi = \frac{r}{\left| \vec{OP} \right|}
   \end{cases}
   $$
   代入，即有
   $$
   \left( \frac{\vec{OP} \cdot \vec{OQ}}{\left| \vec{OQ} \right|} \right)^2 + r^2 \leqslant \left| \vec{OP} \right|^2
   $$
   是该情况下 $Q$ 能被烟幕云团遮蔽的充要条件。

   

3. $|\vec{OP}| \geqslant r$，并且 $|\vec{OP} \cdot \vec{OQ}| < 0$

   此情况下，令线段 $OP$ 与球 $P$ 的交点为 $A$，$\alpha$ 为球 $P$ 在 $A$ 处的切面，则 $O$ 与 $Q$ 位于面 $\alpha$ 的同侧，因而烟幕云团不可能位于 $O$ 与 $Q$ 之间，故 $Q$ 不能被烟幕云团遮蔽