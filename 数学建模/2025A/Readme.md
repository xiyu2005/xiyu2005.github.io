main.py & 项目的主入口和优化器,包括各个问题的求解 \\

cover.py & 包含了判断目标是否被烟幕遮蔽的核心逻辑 \\

objects.py & 定义了模拟中的核心实体，包括无人机、导弹、烟幕弹和目标 \\

common.py & 问题三程序代码 \\

constant.py & 存储了整个模拟过程中使用的物理常量 \\

在main.py的主流程：
![[Pasted image 20250907171014.png]]
prblem1-4都是封装好的函数。我们一个个取消注释跑是ok的，但没有试过连续跑problem的稳定性

simulate_multi_bomb和simulate_multi_bomb_test为第三问测试函数。输入为vx，vy，三个烟幕弹的t_drop列表与t_fuse列表。

三四问算法可视化绘图程序在画图程序文件夹中；要测试的话要把q4_log1.2,2.2,3.2都移到和它一个文件夹。

plot_trace为绘制飞行轨迹示意图代码。