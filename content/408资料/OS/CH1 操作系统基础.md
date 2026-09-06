# 操作系统分类
## 无OS的计算机系统
人工操作
大部分时间计算机在等待输入，**cpu利用率极低**。
 脱机输入输出
程序和数据在外围机的控制下完成。外围控制机<->快速设备<->主机

## 批处理系统
**单道和多道的特点：无交互功能**
用户将一批作业提交给OS后就不再干预。分为单道批处理系统和多道批处理系统。
单道程序设计：一次只允许一个程序在内存中运行。
多道程序设计：多个程序驻留内存，CPU在不同程序间切换执行。
### 单道批处理
**内存中仅有一道程序**，<span style="color:rgb(255, 0, 0)">需要实现把程序执行顺序规划好，启动后自动完成</span>。但是仍然<span style="color:rgb(255, 0, 0)">CPU和IO利用率低，吞吐率小。不过系统开销小</span>。
### 多道批处理
选择若干作业进入内存，共享CPU和系统中的各种资源。<span style="color:rgb(255, 0, 0)">提升了CPU的效率，也提高了IO效率，提高了吞吐率但是系统开销大。</span>。

<div style="display:flex;gap:30px;font-family:SimHei,sans-serif;">
<!-- 左侧：单道批处理 -->
<div style="width:48%;">
<div style="text-align:center;font-size:20px;color:#c82423;font-weight:bold;margin-bottom:12px;">单道批处理系统</div>
<!--图例-->
<div style="display:flex;gap:12px;justify-content:flex-end;margin-bottom:8px;">
<span style="display:flex;align-items:center;"><span style="width:24px;height:12px;background:#e07030;margin-right:4px;"></span>输入</span>
<span style="display:flex;align-items:center;"><span style="width:24px;height:12px;background:#4068c8;margin-right:4px;"></span>计算</span>
<span style="display:flex;align-items:center;"><span style="width:24px;height:12px;background:#80c840;margin-right:4px;"></span>输出</span>
</div>
<svg width="460" height="258" viewBox="0 0 460 258">
  <!--坐标轴-->
  <line x1="40" y1="200" x2="430" y2="200" stroke="#333"/>
  <line x1="40" y1="20" x2="40" y2="200" stroke="#333"/>
  <!--时间刻度 - 精确对齐t=3,6,9-->
  <line x1="166" y1="200" x2="166" y2="205" stroke="#333"/><text x="160" y="220">3</text>
  <line x1="292" y1="200" x2="292" y2="205" stroke="#333"/><text x="286" y="220">6</text>
  <line x1="418" y1="200" x2="418" y2="205" stroke="#333"/><text x="412" y="220">9</text>
  <text x="420" y="218">时间</text>
  <!--作业1：t0-t3-->
  <text x="8" y="52">作业1</text>
  <rect x="40" y="35" width="42" height="24" fill="#e07030"/>
  <rect x="82" y="35" width="42" height="24" fill="#4068c8"/>
  <rect x="124" y="35" width="42" height="24" fill="#80c840"/>
  <line x1="166" y1="59" x2="166" y2="200" stroke="#666" stroke-dasharray="3 3"/>
  <!--作业2：t3-t6，从166开始-->
  <text x="8" y="92">作业2</text>
  <rect x="166" y="75" width="42" height="24" fill="#e07030"/>
  <rect x="208" y="75" width="42" height="24" fill="#4068c8"/>
  <rect x="250" y="75" width="42" height="24" fill="#80c840"/>
  <line x1="292" y1="99" x2="292" y2="200" stroke="#666" stroke-dasharray="3 3"/>
  <!--作业3：t6-t9，从292开始-->
  <text x="8" y="132">作业3</text>
  <rect x="292" y="115" width="42" height="24" fill="#e07030"/>
  <rect x="334" y="115" width="42" height="24" fill="#4068c8"/>
  <rect x="376" y="115" width="42" height="24" fill="#80c840"/>
  <line x1="418" y1="139" x2="418" y2="200" stroke="#666" stroke-dasharray="3 3"/>
  <!--底部文字-->
  <text x="40" y="242" font-size="16">CPU、I/O设备利用率低，系统开销小</text>
</svg>
</div>

<!-- 右侧：多道批处理 -->
<div style="width:48%;">
<div style="text-align:center;font-size:20px;color:#c82423;font-weight:bold;margin-bottom:12px;">多道批处理系统</div>
<div style="display:flex;gap:12px;justify-content:flex-end;margin-bottom:8px;">
<span style="display:flex;align-items:center;"><span style="width:24px;height:12px;background:#e07030;margin-right:4px;"></span>输入</span>
<span style="display:flex;align-items:center;"><span style="width:24px;height:12px;background:#4068c8;margin-right:4px;"></span>计算</span>
<span style="display:flex;align-items:center;"><span style="width:24px;height:12px;background:#80c840;margin-right:4px;"></span>输出</span>
</div>
<svg width="460" height="258" viewBox="0 0 460 258">
  <!--坐标轴-->
  <line x1="40" y1="200" x2="430" y2="200" stroke="#333"/>
  <line x1="40" y1="20" x2="40" y2="200" stroke="#333"/>
  <!--时间刻度 - 精确对齐t=1,2,5-->
  <line x1="82" y1="200" x2="82" y2="205" stroke="#333"/><text x="76" y="220">1</text>
  <line x1="124" y1="200" x2="124" y2="205" stroke="#333"/><text x="118" y="220">2</text>
  <line x1="250" y1="200" x2="250" y2="205" stroke="#333"/><text x="244" y="220">5</text>
  <text x="420" y="218">时间</text>
  <!--作业1：输入t0-t1，计算t1-t2，输出t2-t3-->
  <text x="8" y="52">作业1</text>
  <rect x="40" y="35" width="42" height="24" fill="#e07030"/>
  <rect x="82" y="35" width="42" height="24" fill="#4068c8"/>
  <rect x="124" y="35" width="42" height="24" fill="#80c840"/>
  <line x1="166" y1="59" x2="166" y2="200" stroke="#666" stroke-dasharray="3 3"/>
  <!--作业2：输入t1-t2（与作业1计算并行），计算t2-t3（与作业1输出并行）-->
  <text x="8" y="92">作业2</text>
  <rect x="82" y="75" width="42" height="24" fill="#e07030"/>
  <rect x="124" y="75" width="42" height="24" fill="#4068c8"/>
  <rect x="166" y="75" width="42" height="24" fill="#80c840"/>
  <line x1="208" y1="99" x2="208" y2="200" stroke="#666" stroke-dasharray="3 3"/>
  <!--作业3：输入t2-t3（与作业2计算并行），计算t3-t4（与作业2输出并行）-->
  <text x="8" y="132">作业3</text>
  <rect x="124" y="115" width="42" height="24" fill="#e07030"/>
  <rect x="166" y="115" width="42" height="24" fill="#4068c8"/>
  <rect x="208" y="115" width="42" height="24" fill="#80c840"/>
  <line x1="250" y1="139" x2="250" y2="200" stroke="#666" stroke-dasharray="3 3"/>
  <!--底部文字-->
  <text x="40" y="242" font-size="16">CPU、I/O设备利用率高，系统开销大</text>
</svg>
</div>
</div>

## 分时操作系统
**核心词：交互性**
是一种<span style="color:rgb(255, 0, 0)">多用户交互式</span>的操作系统。允许多个用户通过各自终端，<span style="color:rgb(255, 0, 0)">以时间片为单位，交互式轮流地使用计算机</span>，共享主机资源。

## 实时操作系统
**核心：操作必须在规定时间内发生，及时性，可靠性**
实时OS强调<span style="color:rgb(255, 0, 0)">系统响应时间短</span>。分<span style="color:rgb(255, 0, 0)">硬实时操作系统</span>（实时控制系统，军事控制）和<span style="color:rgb(255, 0, 0)">软实时操作系统</span>（订票系统，银行管理系统）。


## 网络操纵系统和分布式操作系统
网络操作系统：中间的主机是网络核心，存储所有共享文件、数据、应用程序；周围独立的主机访问。比如ftp服务器。
分布式操作系统：呈现为一台逻辑上的单一计算机。由中心OS，周围硬件结点。比如大规模计算平台。

## 其他操作系统

微处理机操作系统
嵌入式操作系统
集群系统


# 操作系统体系结构
分层法（垂直结构）。底层为硬件，顶层为用户接口，每层只能调用紧邻它的底层功能和服务。单向调用，不允许跨层通信。
### 操作系统模块化
（平行结构）模块之间并列，将操作系统按功能划分为若干具有一定独立性的模块。各模块之间能够通过接口通信。

## 宏内核和微内核
宏内核；内核大，性能高，扩展性差，不安全不稳定。不需要频繁切换。
微内核：内核小，性能低，扩展性好，安全稳定。频繁切换。

# 虚拟机
虚拟机（VM）
虚拟机监控器（VMM）
VMM也叫Hypervisor，是虚拟化技术的核心组件，负责创建、管理和监控虚拟机，并协调虚拟机与物理硬件之间的资源分配。
VMM的分类：
Type1裸金属类：直接运行于OS，不依赖其他OS，<span style="color:rgb(255, 0, 0)">效率更高</span>。
资源分配方式：VMM<span style="color:rgb(255, 0, 0)">在原本的硬盘</span>上自行分配存储空间。
<span style="color:rgb(255, 0, 0)">可迁移性差</span>。特权级：第一类VMM>OS
Type2宿主类：作为应用程序运行在物理机OS，依赖宿主OS管理物理资源。客户OS拥有自己的虚拟磁盘。实际上是宿主OS FS中的一个文件。<span style="color:rgb(255, 0, 0)">性能比第一类差</span>，但<span style="color:rgb(255, 0, 0)">可迁移性好</span>。特权级宿主OS>第二类VMM>客户OS

|          | 第一类VMM             | 第二类VMM               |
| -------- | ------------------ | -------------------- |
| 运行       | 运行在硬件之上            | 运行在宿主OS之上            |
| 资源分配方式   | VMM在原本的硬盘上自行分配存储空间 | 硬盘是虚拟硬盘，是宿主OS中的一个文件  |
| 性能       | 性能更好               | 性能更差                 |
| 虚拟机的可迁移性 | 更差                 | 更好                   |
| 运行模式     | 第一类VMM > 普通操作系统    | 宿主OS > 第二类VMM > 客户OS |

# 操作系统引导
1.<span style="color:rgb(255, 0, 0)">CPU通电（开机）</span>，自动读取特定地址，即内存ROM中的引导程序(<span style="color:rgb(255, 0, 0)">BIOS固件</span>)
2.<span style="color:rgb(255, 0, 0)">自检程序构建中断向量表</span>（临时性），<span style="color:rgb(255, 0, 0)">硬件自检</span>。

| 中断类型号 | 中断向量地址 | 中断向量（中断服务程序的入口地址） |
| ----- | ------ | ----------------- |
| 0     | 0x1234 | 0x1232            |
| 1     | 0x1276 | 0x3768            |
3.自举装入程序确定启动设备优先级，选择首个有效的启动设备。
4.<span style="color:rgb(255, 0, 0)">加载主引导程序（MBR</span>）。BIOS将所选启动设备的<span style="color:rgb(255, 0, 0)">首扇区（主引导扇区）盘分区表</span>，硬盘的主引导扇区分为：<span style="color:rgb(255, 0, 0)">1.主引导记录（磁盘引导程序）（MBR）</span>，用于解析分区表，识别活动分区（包含OS的分区），<span style="color:rgb(255, 0, 0)">2.分区表</span>，给出每个分区的起始和终止地址<span style="color:rgb(255, 0, 0)">3.结束标志</span>
5.定位<span style="color:rgb(255, 0, 0)">活动分区</span>并加载分区引导记录<span style="color:rgb(255, 0, 0)">（分区引导程序）（PBR）</span>。MBR中的引导代码解析分区表，识别标记为“活动”的分区，并加载其<span style="color:rgb(255, 0, 0)">首扇区（分区引导记录，PBR）</span>
6.PBR负责加载OS内核。启动管理器<span style="color:rgb(255, 0, 0)">将用户选定的OS内核映像加载到内存中</span>，并跳转执行，<span style="color:rgb(255, 0, 0)">内核随即完全接管系统控制权，重建中断处理机制</span>，不再依赖BIOS提供的服务。
7.内核初始化与用户环境启动。内核完成核心子系统初始化：
内存管理模块：内核页表构建，用户进程地址空间框架
进程调度模块：初始化PCB链表，就绪队列与阻塞队列
设备驱动模块：建立设备控制块，设备分配表，IO缓冲区管理结构。
初始化完成后，内核启动首个用户态进程，由此逐步构建完整的用户操作环境。

记忆：1.ROM中的引导程序执行BIOS：选择最高优先级磁盘启动
2.主引导记录（磁盘引导程序）（MBR）执行：解析分区表，选择活动分区
3.加载分区引导记录（PBR）：加载活动分区内的启动管理器
4.加载OS内核。