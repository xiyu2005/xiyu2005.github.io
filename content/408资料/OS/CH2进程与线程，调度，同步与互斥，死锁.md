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

fork系统调用：创建新进程。只被调用一次，却会返回两次：一次在调用进程（父进程）中，一次在新创建的子进程中。
fork的写时复制：每个进程有自己的虚拟地址空间，fork后初始内容相同并共享只读物理页，通过**写时复制**在修改时分配新页，逐渐形成各自不同的内容”。
exec系统调用：例execlp修改子进程虚拟地址空间。

PTBR（页表基址寄存器）中的页表存储在进程虚拟地址空间mm_struct中PTBA这个变量中，因此不需要将PTBR的值写到PCB。

##### 进程的终止
终止的方式：1从主程序返回2调用exit函数3收到信号，其默认行为是终止进程。
##### 子进程回收
进程终止时，不是被清除，而是处于终止状态，等待父进程回收。
例题：
```c
int main(){
	if(Fork()==0){
		printf("a");fflush(stdout);
	}else{
		printf("b");fflush(stdout);
		waitpid(-1,NULL,0);
	}
	printf("c");fflush(stdout);
	exit(0);
}
```
所有可能的输出序列？
<div style="display:flex;justify-content:center;font-family:sans-serif;">
  <svg width="700" height="220" viewBox="0 0 700 220" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L8,3 z" fill="#000" />
      </marker>
      <marker id="arrow-dashed" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L8,3 z" fill="#000" />
      </marker>
    </defs>

    <!-- 主分支节点（父进程） -->
    <circle cx="50" cy="60" r="5" fill="#000" />
    <text x="50" y="45" text-anchor="middle" font-size="14">main</text>

    <circle cx="150" cy="60" r="5" fill="#000" />
    <text x="150" y="45" text-anchor="middle" font-size="14">fork</text>

    <circle cx="260" cy="60" r="5" fill="#000" />
    <text x="260" y="45" text-anchor="middle" font-size="14">printf b</text>

    <circle cx="380" cy="60" r="5" fill="#000" />
    <text x="380" y="45" text-anchor="middle" font-size="14">waitpid</text>

    <circle cx="500" cy="60" r="5" fill="#000" />
    <text x="500" y="45" text-anchor="middle" font-size="14">printf c</text>

    <circle cx="620" cy="60" r="5" fill="#000" />
    <text x="620" y="45" text-anchor="middle" font-size="14">exit</text>

    <!-- 子分支节点（子进程） -->
    <circle cx="260" cy="160" r="5" fill="#000" />
    <text x="260" y="185" text-anchor="middle" font-size="14">printf a</text>

    <circle cx="340" cy="160" r="5" fill="#000" />
    <text x="340" y="185" text-anchor="middle" font-size="14">printf c</text>

    <circle cx="380" cy="160" r="5" fill="#000" />
    <text x="380" y="185" text-anchor="middle" font-size="14">exit</text>

    <!-- 主分支实线箭头 -->
    <line x1="57" y1="60" x2="143" y2="60" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />
    <line x1="157" y1="60" x2="253" y2="60" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />
    <line x1="267" y1="60" x2="373" y2="60" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />
    <line x1="387" y1="60" x2="493" y2="60" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />
    <line x1="507" y1="60" x2="613" y2="60" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />

    <!-- fork 向下分支虚线（折线：先下后右到 printf a） -->
    <path d="M150,65 L150,160 L253,160" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrow-dashed)" />

    <!-- 子分支实线箭头 -->
    <line x1="267" y1="160" x2="333" y2="160" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />
    <line x1="347" y1="160" x2="373" y2="160" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />

    <!-- 子进程 exit 向上虚线指向 waitpid -->
    <line x1="380" y1="155" x2="380" y2="68" stroke="#000" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrow-dashed)" />
  </svg>
</div>
如上图，可以知道有acbc，abcc，bacc三种可能。

##### 进程终止的步骤
1根据被终止进程pid从内核管理的pcb中检索出该进程pcb，读取状态。
2若被终止进程处于执行状态，终止执行，置调度标识为真，用于指示该进程被终止后应重新进行调度。所以**除了时钟中断会进行进程调度，在进程终止的时候也可能进行进程调度。**
3将被终止进程所拥有的全部资源或归还给父进程，或归还给OS。
（1）内核直接回收的资源：内存资源（代码段、数据段、堆、栈、通过页表清理实现），打开的文件描述符（关闭文件，释放文件指针，包括设备文件即回收IO设备）；信号量、管道等内核对象
（2）需要父进程配合回收的资源：进程的PCB。父进程需要通过waitpid系统调用
（3）特殊情况：孤儿进程的资源回收
总结：内核负责释放大部分运行资源，父进程（或领养进程）负责回收进程退出状态和PCB



#### 父进程和子进程
父进程可以有多个子进程，子进程只有一个父进程。子进程继承了父进程的一些属性和资源，并可以执行不同的代码。

父进程终止，子进程可能终止，也可能作为孤儿进程，看具体系统实现。
线程

闲逛进程（idle进程，0号进程）：负责在系统没有其他任务执行的时候占据cpu，最低优先级，无实际业务逻辑，不可终止。**所有进程的祖先**。
1号进程：init进程，**所有用户进程的祖先**。2号进程：**所有内核进程的祖先**。

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

##### 引起进程创建的事件
用户登录，作业调度，系统提供服务，用户应用请求。
##### 引起进程终止的时机点
正常结束；异常结束：越界，保护，非法指令，特权指令，运行超时，等待超时，算术运算（除0），IO故障。；外界干预：人员，OS干预，父进程请求。

#### 五种基本进程状态
1.新建状态：保证进程调度必须在创建工作后进行，确保PCB操作完整性。
2.就绪状态：进程已分配到除CPU以外的所有必需资源，只要获得CPU，就可以立即执行。
3.运行状态
4.阻塞态/等待态：排成阻塞队列。
例如：read系统调用，键盘数据未到达，进程阻塞在键盘等待队列；wait系统调用，父进程阻塞，PCB放到等待子进程状态变化的等待队列；互斥锁、信号量、都有等待队列。
5.终止状态

##### 挂起状态
目的：终端用户、父进程需要，负荷调节，OS需要
引入挂起原语，激活原语；
1活动就绪->静止就绪；2活动阻塞->静止阻塞；3.静止就绪->活动就绪；4精致阻塞->活动阻塞5.创建->静止就绪

#### 引起阻塞的事件
1向系统请求共享资源失败。比如无可分配打印机。2.等待某种操作完成。3.新数据尚未到达4.等待新任务到达。

#### 阻塞过程
使用阻塞原语block阻塞。是进程的自身主动行为。

唤醒过程：用原语wakeup唤醒。即先把阻塞的进程从等待队列移出，再将PCB现行状态改为就绪。

## 线程实现方式

## 进程/线程通信方式




# CPU调度

# 同步与互斥


# 死锁