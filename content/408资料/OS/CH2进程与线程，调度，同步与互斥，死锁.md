# 进程与线程
## 进程与线程基本概念
### 进程：
运行着的程序。“活的”程序。程序的一次动态执行过程。
特性：<span style="color:rgb(255, 0, 0)">动态性，并发性，独立性，异步性</span>。
#### 进程的实体（映像）
1.进程控制块PCB ：创建后常驻内存，进程终止后删除。
PCB包含了进程标识符，CPU上下文（进程可以走走停停的前提），进程调度信息，进程控制信息
<table style="border-collapse:collapse;width:100%;font-size:13px;line-height:1.3;">
  <thead>
    <tr style="background:#f0f0f0;">
      <th style="border:1px solid #aaa;padding:4px;text-align:center;">进程标识符</th>
      <th style="border:1px solid #aaa;padding:4px;text-align:center;"></th>
      <th style="border:1px solid #aaa;padding:4px;text-align:center;"></th>
    </tr>
    <tr>
      <td style="border:1px solid #aaa;padding:3px;text-align:center;">PID<br/>进程标识符</td>
      <td style="border:1px solid #aaa;padding:3px;text-align:center;">UID<br/>用户标识符</td>
      <td style="border:1px solid #aaa;padding:3px;text-align:center;"></td>
    </tr>
    <tr style="background:#f7f7f7;">
      <th style="border:1px solid #aaa;padding:4px;text-align:center;">处理机状态<br/><small>便于实现进程切换</small></th>
      <th style="border:1px solid #aaa;padding:4px;text-align:center;">进程调度信息<br/><small>便于实现进程调度</small></th>
      <th style="border:1px solid #aaa;padding:4px;text-align:center;">进程控制信息</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid #aaa;padding:3px;">通用寄存器值</td>
      <td style="border:1px solid #aaa;padding:3px;">进程当前状态</td>
      <td style="border:1px solid #aaa;padding:3px;">程序和数据的地址</td>
    </tr>
    <tr>
      <td style="border:1px solid #aaa;padding:3px;">地址寄存器值</td>
      <td style="border:1px solid #aaa;padding:3px;">进程优先级</td>
      <td style="border:1px solid #aaa;padding:3px;">进程同步和通信机制</td>
    </tr>
    <tr>
      <td style="border:1px solid #aaa;padding:3px;">指令计数器</td>
      <td style="border:1px solid #aaa;padding:3px;">代码运行入口地址</td>
      <td style="border:1px solid #aaa;padding:3px;">资源清单</td>
    </tr>
    <tr>
      <td style="border:1px solid #aaa;padding:3px;">程序状态字 PSW</td>
      <td style="border:1px solid #aaa;padding:3px;">程序的外存地址</td>
      <td style="border:1px solid #aaa;padding:3px;">链接指针</td>
    </tr>
    <tr>
      <td style="border:1px solid #aaa;padding:3px;">用户栈指针</td>
      <td style="border:1px solid #aaa;padding:3px;">进入内存时间</td>
      <td style="border:1px solid #aaa;padding:3px;"></td>
    </tr>
    <tr>
      <td style="border:1px solid #aaa;padding:3px;"></td>
      <td style="border:1px solid #aaa;padding:3px;">处理机占用时间</td>
      <td style="border:1px solid #aaa;padding:3px;"></td>
    </tr>
    <tr>
      <td style="border:1px solid #aaa;padding:3px;"></td>
      <td style="border:1px solid #aaa;padding:3px;">信号量使用</td>
      <td style="border:1px solid #aaa;padding:3px;"></td>
    </tr>
  </tbody>
</table>

⚠️注意：<span style="color:rgb(0, 176, 240)"><b>信号量是进程同步专用数据结构，不属于PCB本身内容，PCB只记录进程使用的同步资源，不存放信号量本体</b></span>

2.程序段：程序代码
3.数据段：可以是进程对应加工程序的原始数据，也可以是程序执行产生的结果

PCB的作用1.作为独立运行基本单位的标志。2.实行间断性运行方式3.提供进程管理所需要的信息。4.提供进程调度所需要的信息。5.实现与其他进程同步和通信。

fork()：创建新进程。

PTBR（页表基址寄存器）中的页表存储在进程虚拟地址空间mm_struct中PTBA这个变量中，因此不需要将PTBR的值写到PCB。
#### 父进程和子进程
父进程可以有多个子进程，子进程只有一个父进程。子进程继承了父进程的一些属性和资源，并可以执行不同的代码。

父进程终止，子进程可能终止，也可能作为孤儿进程，看具体系统实现。
线程

闲逛进程：负责在系统没有其他任务执行的时候占据cpu，最低优先级，无实际业务逻辑，不可终止。

##### 作业
作业：用户提交给系统的任务，可划分为多个进程；（进程可划分为多个线程）
作业调度：外村到内存里，进入就绪队列。
进程调度：就绪进程队列的cpu分配。

### 线程
把进程看作容器，线程就是容器里干活的人。
进程有自己的内存空间。
线程是独立调度的基本单位。可并发执行，共享该进程所拥有的资源（栈和寄存器包括PC不共享），轻型实体，线程通信的方式是共享内存。
而资源拥有的基本单位是进程。
（进程类比蜜雪冰城整个店的东西资源，线程就是里面的员工）

#### 进程上下文切换
定义：切换CPU到另一个进程需要保存当前进程状态和恢复另一个进程的状态。

进程上下文切换开销 大于 同一进程内的 线程切换开销。

中断响应中现场保存和恢复通常分开，而<span style="color:rgb(255, 0, 0)">进程的旧进程上下文保存和新进程上下文恢复是连续的</span>。如果没有其他进程了也必须安排一个闲逛进程，维持cpu的稳定。


#### 内核栈和用户栈
每个普通进程都可以运行在用户态和内核态，再用户态执行函数调用时的函数栈是用户栈；如果发生中断或异常，陷入内核，切入到内核态，进程接下来就会在内核态运行。
内核态执行系统调用前，需要保存用户态CPU上下文，包括PC，程序状态、通用寄存器、用户态栈顶指针。并不需要切换页表，因为仍然是同一个进程。
执行系统调用时，在内核函数栈（进程创立时分配的）为本次内核态创立栈帧。执行内核态函数。
结束后，内核态切换回用户态之前，先恢复用户态CPU上下文，然后执行特权指令，从内核态切回用户态。
综上，一次系统调用、中断、异常处理需要两次CPU上下文切换，且过程都位于同一个进程。
## 进程/线程状态转化

## 线程实现方式

## 进程/线程通信方式




# CPU调度

# 同步与互斥


# 死锁