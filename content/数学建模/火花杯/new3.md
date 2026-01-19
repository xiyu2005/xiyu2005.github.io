### 模型建立

本文提出的调度方案基于一个精确的数学模型，该模型旨在捕捉网络拓扑、S2GL（Sensor-to-Ground Link）动态性以及移动信号车覆盖范围演进的核心特征。

**1. 问题分析与模型演进**

为实现有效的调度，模型必须精确刻画系统的动态演化。核心在于S2GL带宽函数与车辆移动规则的数学表达。

*S2GL带宽动态性分析：*
问题的设计旨在创造一个沿x轴移动的带宽“波峰”。这是通过一个依赖于时间和列坐标 $x$ 的相位函数 $\phi_x(t)$ 实现的。在公式 $\phi_x(t) = 5 + \lfloor t/3 \rfloor - x$ 中，$\lfloor t/3 \rfloor$ 项使相位随时间平移，而 $-x$ 项则在不同列间制造相位差。两者结合，便在x方向上形成了行进的波。带宽函数 $b_{x,y}(t)$ 本身是一个标准的三角波（或倒V形）函数，其峰值由 $\pmod{10}$ 运算的中心点决定。当时间 $t$ 变化时，相位 $\phi_x(t)$ 的变化使得这个带宽峰值点在不同的列之间移动，从而驱动车辆的覆盖决策。

*移动信号车覆盖范围演进：*
根据赛题澄清，三辆车的运动与覆盖范围选择是一种**“中心匀速，边缘动态”**的混合模式。车辆的几何中心 $x_{\text{pos}}(t)$ 沿x轴（从第1列到第20列）匀速运动，其位置仅依赖于时间。而完整的覆盖区域（共3列）则围绕这个中心动态调整：其中两列紧随中心，第三列则根据S2GL带宽和历史位置进行自适应选择，以捕捉最优的传输机会。这种设计既保证了车辆的总体行进趋势，又赋予了其局部寻优的灵活性。

**2. 核心数学模型**

基于以上分析，我们构建如下的数学模型：

* **集合与核心参数**:
    * 传感器节点集合: $S = \{(x, y) | 1 \le x \le 20, 1 \le y \le 30\}$
    * 数据流集合: $F = \{f_1, f_2, \ldots, f_{1800}\}$
    * 移动接收车集合: $V = \{v_1, v_2, v_3\}$
    * 时间步集合: $T = \{0, 1, \ldots, 89\}$
    * Mesh网络容量与时延: $B_{\text{sensor}} = 10$ Mbps, $t_{\text{sensor}} = 50$ ms
    * 单车接收总带宽: $B_{\text{receive}} = 100$ Mbps
    * 数据流属性: 总数据量 $s_i=10$ Mb（可拆分为1024B的数据包），固定传输速率 $r_i = 5$ Mbps

* **时变函数与状态变量**:
    * **S2GL带宽 $b_{x,y}(t)$**: 传感器 $(x,y)$ 的峰值带宽为 $B_{\text{peak}} = 20$ Mbps。其瞬时带宽由一个与时间`t`和列坐标`x`相关的时变相位函数 $\phi_x(t)$ 决定。由于带宽函数与行坐标`y`无关，后文简记为 $b_x(t)$。
        $$
        \begin{gather}
            \phi_x(t) = 5 + \lfloor t/3 \rfloor - x \\
            b_x(t) = 20 \times \left(1 - \frac{|((t + \phi_x(t)) \pmod{10}) - 5|}{5}\right)
        \end{gather}
        $$
    
    * **移动信号车中心列坐标 $x_{\text{pos}}(t)$**: 三辆车运动同步，其几何中心在t=0时从第1列出发，在t=100时到达第20列，因此其中心列坐标 $x_{\text{pos}}(t)$ 为：
        $$
        \begin{gather}
            x_{\text{pos}}(t) = 1 + \left( \frac{19}{100} \right) t
        \end{gather}
        $$
    
    * **移动信号车覆盖列坐标集合 $X_{\text{cov}}(t)$**: 在时刻 $t$，每辆车覆盖三列。因此$X_{\text{cov}}(t) = \{x_1(t), x_2(t), x_3(t)\}$其中$x_1(t), x_2(t)$两列固定跟随车辆中心，第三列 $x_3(t)$ 动态选择。令中心基准列为 $x_c(t) = \lfloor x_{\text{pos}}(t) \rfloor$。
    
        固定的两列为 $x_1(t) = x_c(t)$ 和 $x_2(t) = x_c(t)+1$。
    
        第三列 $x_3(t)$ 从候选列 $\{x_c(t)-1, x_c(t)+2\}$ 中根据以下规则选出：
        * 比较候选列的S2GL带宽：$B_{\text{cand1}} = b_{x_c(t)-1}(t)$ 和 $B_{\text{cand2}} = b_{x_c(t)+2}(t)$。
        * 定义上一时刻的最末列（编号最小的覆盖列）为 $x_{\text{rear}}(t-1) = \min(X_{\text{cov}}(t-1))$。
    
        $x_3(t)$ 的计算公式为：
        $$
        \begin{gather}
        x_3(t) = 
        \begin{cases} 
        x_c(t)+2 & \text{if } B_{\text{cand2}} > B_{\text{cand1}} \\
        x_c(t)-1 & \text{if } B_{\text{cand1}} \ge B_{\text{cand2}} \text{ and } (x_c(t)-1) \ge x_{\text{rear}}(t-1) \\
        x_c(t)+2 & \text{if } B_{\text{cand1}} \ge B_{\text{cand2}} \text{ and } (x_c(t)-1) < x_{\text{rear}}(t-1)
        \end{cases}
        \end{gather}
        $$
        最终，时刻 $t$ 的覆盖列坐标集合为 $X_{\text{cov}}(t) = \{x_1(t), x_2(t), x_3(t)\}$。
    
    * **状态变量**: 每个流 $f_i$ 维护 \texttt{current\_position}, \texttt{path}, \texttt{transmission\_timer}, \texttt{remaining\_data} 等状态。$L_{uv}(t)$ 和 $L_{v_j}(t)$ 分别记录Mesh链路和车辆在时刻 $t$ 已被分配的负载。

* **决策变量**:
    对于每个处于空闲状态的流 $f_i$，在时刻 $t$ 的决策是为其选择一条路径 $P_i(t)$ 并分配一个5 Mbps的信道。这可以表示为一个布尔决策变量 $\delta_i(t) \in \{0, 1\}$，其中1代表成功分配。
    
* **约束条件**:
    所有信道分配必须满足Mesh链路和车辆接收带宽的容量限制：
    $$
    \begin{align}
        \sum_{f_i \text{ using } (u,v)} 5 \cdot \delta_i(t) &\le B_{\text{sensor}}, && \forall (u,v) \in E_{\text{mesh}}, \forall t \in T \\
        \sum_{f_i \text{ to } v_j} 5 \cdot \delta_i(t) &\le B_{\text{receive}}, && \forall v_j \in V, \forall t \in T
    \end{align}
    $$
    
* **优化目标**:
    本模型旨在实现双重优化目标：最小化丢包率和最小化平均传输时延。
    1.  **最小化丢包率 ($P_{loss}$)**: 等价于最大化移动信号车接收到的总数据量。设 $s_i$ 为流 $f_i$ 的总数据量，$s_{rem,i}(T)$ 为在仿真结束时流 $f_i$ 的剩余数据量。
        $$
        \min P_{loss} = \frac{\sum_{i \in F} s_{rem,i}(T)}{\sum_{i \in F} s_i}
        $$
            
    2.  **最小化平均传输时延 ($\bar{T}_{delay}$)**: 对于所有成功完成传输的流集合 $F_{completed}$，计算从其产生到完成传输的平均时间。
        $$
        \min \bar{T}_{delay} = \frac{1}{|F_{completed}|} \sum_{i \in F_{completed}} (t_{end,i} - t_{start,i})
        $$