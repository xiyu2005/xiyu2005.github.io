## Euler Algorithm
Damped Oscillator
$$
m \frac{d^2 x}{d t^2}+\beta \frac{d x}{d t}+k x=0
$$
$x^{\prime \prime}+2 \gamma x^{\prime}+\omega_0{ }^2 x=0 \quad$ with $\beta / m=2 \gamma, k / m=\omega_0{ }^2$
Critically Damped
$$
\begin{aligned}
& \gamma^2=\omega_0^2, \text { i.e. } \beta^2=4 k m \\
& x=e^{-\gamma t}(A+B t)
\end{aligned}
$$

Forced Vibrations, $F(t)=F_0 \cos \alpha t$
$$
\begin{aligned}
& x^{\prime \prime}+2 \gamma x^{\prime}+\omega_0^2 x=f_0 \cos \alpha t \\
& \text { with } \beta / m=2 \gamma, k / m=\omega_0^2, F_0 / m=f_0 \\
& \text { General solution of } x^{\prime \prime}+2 \gamma x^{\prime}+\omega_0^2 x=f_0 \cos \alpha t \\
& =\text { general solution of } x^{\prime \prime}+2 \gamma x^{\prime}+\omega_0^2 x=0 \\
& \quad(\text { transient/homogeneous solution }) \\
& + \text { a particular solution of } x^{\prime \prime}+2 \gamma x^{\prime}+\omega_0^2 x=f_0 \cos \alpha t \\
& \quad(\text { steady-statelinhomogeneous solution }) \\
& \quad x=\frac{f_0}{\sqrt{\left(\alpha^2-\omega_0^2\right)^2+4 \gamma^2 \alpha^2}} \cos (\alpha t-\phi) \\
& \quad \text { where } \tan \phi=\frac{2 \gamma \alpha}{\alpha^2-\omega_0^2}, \quad 0 \leq \phi \leq \pi
\end{aligned}
$$