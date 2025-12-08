# Computational Physics Homework Assignment \#2 <br> Derivative, Integration, Matrix, and Coupled Oscillators 

March 23, 2021; Due April 12, 2021

## Reading Assignment

1. Read lecture notes and references;
2. Study sample programs and prepare your own programs with any languages you prefer.

Laboratory Assignments (Total Points $125=30+30+30+35$ ), on March 29, 2021

1. Derivatives (30 Points: 15, 15)
(a) Consider the function $f(x)=x \cosh (x)$ at $x=1$ Calculate its first and second derivatives for $h=0.50,0.45, \ldots, 0.05$, using the forward and central difference formulae. Plot the log error versus $\log (h)$. Compare your results with that of Richardson extrapolation.
(b) Use the two-point, three-point, and five-point formulae to estimate the first five derivatives of $f(x)$ at $x=0$,

$$
f(x)=\frac{e^{x}}{\sin ^{3}(x)+\cos ^{3}(x)}
$$

As a check, $f^{(v)}(x=0)=-164$. You are recommended to change the value of in the fashion of $h=1 / 2^{n}, n=1,2, \ldots$.
2. Integration (30 Points: 10, 10, 10)

Using the asymptotic error formulae for the Trapezoid and the Simpson's rules, estimate the number of subdivisions $n$ for the following integrals to the given accuracy $\epsilon$.

$$
\begin{aligned}
& I_{1}=\int_{1}^{3} d x \log (x), \quad \epsilon=10^{-8} \\
& I_{2}=\int_{-1}^{1} d x e^{-x^{2}}, \quad \epsilon=10^{-10} \\
& I_{1}=\int_{1 / 2}^{5 / 2} \frac{d x}{1+x^{2}}, \quad \epsilon=10^{-12}
\end{aligned}
$$

## 3. Hilbert Matrix (30 Points)

Study the Hilbert Matrix

$$
H_{n}=\left(\begin{array}{ccccc}
\frac{1}{1} & \frac{1}{2} & \frac{1}{3} & \cdots & \frac{1}{n} \\
\frac{1}{2} & \frac{1}{3} & \frac{1}{4} & \cdots & \frac{1}{n+1} \\
\cdots & \cdots & \cdots & \cdots & \cdots \\
\frac{1}{n} & \frac{1}{n+1} & \frac{1}{n+2} & \cdots & \frac{1}{2 n-1}
\end{array}\right)
$$

Diagonalizing $H_{n}$ and calculate the ratio of the largest eigenvalue to the smallest eigenvalue, $\log (\max |\lambda| / \min |\lambda|)$, and plot it as a function of $n$ for $n=2,3, \cdots, 8$. Discuss your results. Do the problem for both single and double precisions. Indicate which diagonalization routine you are using.
4. Coupled Oscillators ( 35 Points: 10,10,15)

Use program similar to Oscillators to solve the dynamics equation of motion for $N=12$ oscillators with the initial conditions $u_{j}(t=0)=0, v_{3}(t=0)=1$. Compare numerical results of $u_{j}(t)$ with the analytic one.
(a) What is the maximum deviation of $u_{j}(t)$ ?
(b) How well is the total energy conserved as function of $\Delta t$ ?
(c) How well is the total energy conserved as function of $\Delta t$ if one uses Runge-Kutta 4th order algorithm?

