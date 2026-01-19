# PID
PID 控制器的公式分为两种形式：理论上的**连续形式**和在计算机中实际应用的**离散形式**。

---

### 1. 连续形式 (理想公式)

这是 PID 控制器在控制理论中的标准数学表达式，它描述了一个连续变化的过程。

$$u(t) = K_p e(t) + K_i \int_0^t e(\tau)d\tau + K_d \frac{de(t)}{dt}$$

其中：
* **$u(t)$**：在时间 `t` 时控制器的输出值（例如，电机的电压、加热器的功率）。
* **$e(t)$**：在时间 `t` 时的误差。它是 **设定点 (Setpoint, SP)** 与 **过程变量 (Process Variable, PV)** 之间的差值，即 $e(t) = SP - PV(t)$。
* **$K_p$**：**比例 (Proportional)** 增益。它决定了控制器对当前误差的反应强度。误差越大，输出也越大。它主要影响响应速度。
* **$K_i$**：**积分 (Integral)** 增益。它累积过去的所有误差。这个项的作用是消除系统稳定后仍然存在的微小静态误差（稳态误差）。
* **$K_d$**：**微分 (Derivative)** 增益。它计算误差的变化速率，可以理解为对未来误差的预测。它的作用是抑制系统的振荡，减少超调，使系统更快稳定。

---

### 2. 离散形式 (代码实现)

在计算机程序中，我们无法进行连续的积分和微分，所以会使用离散的形式，通过在固定的时间间隔（`Δt`）进行计算来逼近连续行为。这也就是我们在 Python 代码中实现的形式。

$$u[k] = K_p e[k] + K_i \sum_{i=0}^{k} (e[i] \cdot \Delta t) + K_d \frac{e[k] - e[k-1]}{\Delta t}$$

其中：
* **$u[k]$**：在第 `k` 个采样时刻的控制器输出。
* **$e[k]$**：在第 `k` 个采样时刻的误差。
* **$\sum_{i=0}^{k} (e[i] \cdot \Delta t)$**：对过去所有误差的累加求和，用来近似**积分项**。
* **$\frac{e[k] - e[k-1]}{\Delta t}$**：用当前误差与上一次误差的差值，来近似**微分项**（误差的变化率）。
* **$\Delta t$**：每次计算之间的时间间隔，也就是我们的仿真步长。

---

PID仿真代码
示例代码：
```python
import time
class PIDController:
    """一个封装好的 PID 控制器类 """

    def __init__(self, Kp, Ki, Kd, setpoint=0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self._integral = 0
        self._previous_error = 0

    def update(self, current_value, dt):
        """
        根据当前值和时间步长(dt)计算 PID 输出。

        :param current_value: 从系统中读取的当前测量值
        :param dt: 仿真或控制循环的时间步长
        :return: 控制器的输出值
        """
        if dt <= 0:
            return 0

        # --- PID 计算核心 ---
        error = self.setpoint - current_value
        self._integral += error * dt
        derivative = (error - self._previous_error) / dt
        output = (self.Kp * error) + (self.Ki * self._integral) + (self.Kd * derivative)
        
        # --- 更新状态以备下次调用 ---
        self._previous_error = error

        return output

    def set_setpoint(self, new_setpoint):
        self.setpoint = new_setpoint
        self.reset()

    def reset(self):
        self._integral = 0
        self._previous_error = 0

```

仿真与绘图函数
```python
import time
import matplotlib.pyplot as plt
from PIDcontroller import PIDController
class SimulatedCar:
    def __init__(self):
        self.position = 0
        self.velocity = 0
        self.mass = 1.0

    def update_state(self, force, dt):
        acceleration = force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt

if __name__ == "__main__":
    pid = PIDController(Kp=0.5, Ki=0.05, Kd=0.2)
    target_position = 100.0
    pid.set_setpoint(target_position)

    car = SimulatedCar()
    time_points = []
    position_history = []
    setpoint_history = []
    output_history = []
    
    simulation_duration_seconds = 100
    simulation_step_interval = 0.1
    
    print("--- 开始 PID 控制仿真 ---")
    
    current_sim_time = 0
    while current_sim_time < simulation_duration_seconds:
        current_pos = car.position
        
        # 使用固定的仿真步长调用 update 方法
        control_force = pid.update(current_pos, simulation_step_interval)
        
        car.update_state(control_force, simulation_step_interval)
        
        time_points.append(current_sim_time)
        position_history.append(car.position)
        setpoint_history.append(target_position)
        output_history.append(control_force)
        
        current_sim_time += simulation_step_interval
        
    print("--- 仿真结束 ---")

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(time_points, position_history, 'b-', label='Car Position')
    ax1.plot(time_points, setpoint_history, 'g--', label='Setpoint')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Position', color='b')
    ax1.tick_params('y', colors='b')
    ax1.grid(True)
    ax2 = ax1.twinx()
    ax2.plot(time_points, output_history, 'r:', label='Control Output (Force)')
    ax2.set_ylabel('Force', color='r')
    ax2.tick_params('y', colors='r')
    fig.suptitle('PID Controller Simulation (Corrected)')
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='lower right')
    plt.show()

```
仿真效果如下
![[Pasted image 20250915101717.png]]