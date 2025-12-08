$$\frac{dP(t)}{dt} = \frac{E(P(t))}{V \cdot \rho(P(t))} \left( \dot{m}_{in}(t) - \dot{m}_{out}(t) \right)$$

根据**注1**，燃油压力变化量与密度变化量成正比：$\Delta P = \frac{E}{\rho} \Delta \rho$。其微分形式为 $dP = \frac{E(P)}{\rho(P)} d\rho$。
由此可得：
$$\frac{d\rho}{dP} = \frac{\rho(P)}{E(P)}$$
其中 $E(P)$ 是与压力相关的燃油弹性模量（由附件3查表或插值得到）。
$E(P)$可以用二项式拟合得到。


$E(P) = aP^2 + bP + c$
$a=0.0289 (MPa)^{-1},b=3.0765,c=1571.5839MPa$

化为一个有解析解的微分方程。
$$\left\{\left\{\rho(P)\to c_1 \exp \left(\frac{2 \tan ^{-1}\left(\frac{2 a P+b}{\sqrt{4 a c-b^2}}\right)}{\sqrt{4 a c-b^2}}\right)\right\}\right\}$$


代入压力为100 MPa时，燃油的密度为0.850 mg/mm³
$$c_1=0.7764694044298355$$
P=160MPa,$/rho=0.8710293363038369mg/mm^3$


* **高压油管容积 (V):**
    $V = \pi \left(\frac{D}{2}\right)^2 L = \pi \left(\frac{10 \text{ mm}}{2}\right)^2 \cdot 500 \text{ mm} = 12500\pi \text{ mm}^3$

* **入口质量流率 $\dot{m}_{in}(t)$:**
    根据**注2**，$Q = CA\sqrt{\frac{2\Delta P}{\rho}}$。入口的质量流率是体积流率 $Q_{in}$ 乘以高压侧（油泵侧）的燃油密度 $\rho_{pump}$。因为$m=\rho \cdot V$,$\Delta P = P_{pump} - P(t)$.
    $$
    \dot{m}_{in}(t) = I_{in}(t) \cdot C \cdot A \cdot \sqrt{2 \cdot (P_{pump} - P(t)) \cdot \rho(P_{pump})}
    $$
    其中：
    * $I_{in}(t)$ 是一个控制函数，表示单向阀的开关状态。当阀门开启时 $I_{in}(t) = 1$，关闭时 $I_{in}(t) = 0$。该函数的开关由我们要设置的“开启时长 $t_{on}$”和固定的“关闭时长 $10 \text{ ms}$”决定。
    * $C=0.85$ 是流量系数。
    * $A = \pi \left(\frac{d_A}{2}\right)^2 = \pi \left(\frac{1.4 \text{ mm}}{2}\right)^2 = 0.49\pi \text{ mm}^2$ 是入口 A 的面积。
    * $P_{pump} = 160 \text{ MPa}$ 是恒定的供油压力。
    * $P(t)$ 是高压油管内的瞬时压力。
    * $\rho(P_{pump})$ 是压力为160MPa时的燃油密度，通过上述 $\rho(P)$ 的关系计算得出。

**出口质量流率 $\dot{m}_{out}(t)$:**
    出口的体积喷油速率 $Q_{out}(t)$ 由**图2**直接给出，它是一个周期为 $100 \text{ ms}$ (10次/秒) 的分段函数。
    $$
    Q_{out}(t) = 
    \begin{cases} 
    100 t' & 0 \le t' < 0.2 \\
    20 & 0.2 \le t' < 2.2 \\
    -100(t'-2.4) & 2.2 \le t' < 2.4 \\
    0 & 2.4 \le t' < 100
    \end{cases}
    $$
    其中 $t' = t \pmod{100}$ 是在每个喷油周期内的时间。单位为 $\text{mm}^3/\text{ms}$。


出口质量流率是体积流率乘以高压侧（油管内）的燃油密度 $\rho(P(t))$。
    $$
    \dot{m}_{out}(t) = Q_{out}(t) \cdot \rho(P(t))
    $$


注. 进出高压油管的流量为$Q=CA\sqrt{\frac{2\Delta P}{\rho}}$，其中Q为单位时间流过小孔的燃油量（mm³/ms），C=0.85为流量系数，A为小孔的面积（mm²），ΔP为小孔两边的压力差（MPa），ρ为高压侧燃油的密度（mg/mm³）。


计算理论值
在$t_{on}+10$ms内输入质量$13.3774 * t_{on}$,100ms内输出质量37.4mg
$$
\frac{13.3774\cdot t_{on}}{t_{on}+10}=0.374$$
解得$t_{on}=0.288ms$



$$\frac{dP(t)}{dt} = \frac{E(P(t))}{V \cdot \rho(P(t))} \left( \dot{m}_{in}(t) - \dot{m}_{out}(t) \right)$$


# 提炼

$E(P) = aP^2 + bP + c$
$a=0.0289 (MPa)^{-1},b=3.0765,c=1571.5839MPa$

化为一个有解析解的微分方程。
$$\left\{\left\{\rho(P)\to c_1 \exp \left(\frac{2 \tan ^{-1}\left(\frac{2 a P+b}{\sqrt{4 a c-b^2}}\right)}{\sqrt{4 a c-b^2}}\right)\right\}\right\}$$


代入压力为100 MPa时，燃油的密度为0.850 mg/mm³
$$c_1=0.7764694044298355$$
P=160MPa,$/rho=0.8710293363038369mg/mm^3$




喷出流量：一个100ms的周期流量为$44mm^3$
喷出质量：一个100ms的周期质量为$44 \cdot \rho(P)$ mg
喷出质量速率$0.44 \cdot \rho(P)$ mg/ms
喷入质量:一个$t_{on} + 10$ ms周期质量为$0.85 * 0.49 \pi *\sqrt2 * \sqrt{(160-P)*\rho(P)} * t_{on}$
喷入质量速率$$\frac{0.85 * 0.49 \pi *\sqrt2 * \sqrt{(160-P)*\rho(P)} * t_{on}}{t_{on}+10}$$
$$\left\{\left\{\rho(P)\to c_1 \exp \left(\frac{2 \tan ^{-1}\left(\frac{2 a P+b}{\sqrt{4 a c-b^2}}\right)}{\sqrt{4 a c-b^2}}\right)\right\}\right\}$$
$$c_1=0.7764694044298355$$
$a=0.0289 (MPa)^{-1},b=3.0765,c=1571.5839MPa$

