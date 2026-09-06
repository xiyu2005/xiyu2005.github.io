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

执行->就绪：1当前执行的进程时间片用完2就绪态来了个更高优先级的进程，正在执行的进程被更高优先级进程抢占。
<span style="color:rgb(255, 0, 0)">阻塞态不能直接变为执行态，就绪态不能直接变为阻塞态</span>

##### 挂起状态
目的：终端用户、父进程需要，负荷调节，OS需要
引入挂起原语，激活原语；
1活动就绪->静止就绪；2活动阻塞->静止阻塞；3.静止就绪->活动就绪；4精致阻塞->活动阻塞5.创建->静止就绪

#### 引起阻塞的事件
1向系统请求共享资源失败。比如无可分配打印机。2.等待某种操作完成。3.新数据尚未到达4.等待新任务到达。

#### 阻塞过程
使用阻塞原语block阻塞。是进程的自身主动行为。找到PID对应的PCB，保护现场转为阻塞态，停止运行；将该PCB插入阻塞队列。

唤醒过程：用原语wakeup唤醒。即先把阻塞的进程从等待队列移出，再将PCB现行状态改为就绪。




## 线程实现方式
#### 用户级线程
由应用程序创建、调度、管理。OS内核不理解用户级线程存在。
<span style="color:rgb(255, 0, 0)"><b>在内核中，如果有内核级线程，调度的单位就是线程；如果只有用户级线程，调度单位是进程，进程中的所有用户级线程共享这个进程的cpu时间片。</b></span>
用户级线程的TCB：包含所属进程的pid，线程的tid，用户栈，CPU上下文，线程私有数据区。

#### 内核级线程
对应关系：
多对一：多个用户既线程映射到1个内核级线程.优点：用户级线程切换在用户空间可完成，开销小，效率高。缺点：一个用户级线程被阻塞后，整个进程会被阻塞，并发度不高；多个线程不能在多核处理剂并行运行。因为OS只能看见内核级线程，内核级线程才是处理机分配的单位。

一对一，
优点：当一个线程阻塞后，别的线程还可以继续执行，并发能力强。多线程可在多核处理器上并行执行。
缺点：切换由OS内核完成，开销大。

多对多，
优点：克服了并发度不高的缺点和开销大，综合。内核级线程小于用户级线程。

内核级线程和用户级线程都共享进程资源，线程的pid字段=233说明它们都共享pid=233的虚拟地址空间、打开文件表等资源。
## 进程/线程通信方式
进程间通信（IPC）的两种模型：消息传递模型（管道，消息队列，Socket，邮箱），共享内存模型（mmap文件映射，共享内存）。

### 共享内存
在互相通信的进程之间申请建立一块可直接访问的共享存储空间。
共享存储区本身无保证互斥和同步的机制，使用PV操作等方式实现。
#### mmap实现共享内存
两个进程打开同一个文件，建立共享映射，直接读写内存实现通信。**使用mmap内存映射文件的方式实现的共享内存中的数据是可以<span style="color:rgb(255, 0, 0)">持久化</span>到磁盘文件中的**。
mmap的相关知识：https://zhuanlan.zhihu.com/p/665511332
#### POSIX共享内存
纯内存高速IPC，**数据不会落入磁盘，使通信速度更快了**。


### 管道
1.管道本质是一个特殊的<span style="color:rgb(255, 0, 0)">共享文件</span>
<span style="color:rgb(255, 0, 0)">不落在磁盘中，只存在内存缓冲区。</span>
2.<span style="color:rgb(255, 0, 0)">单向性（不支持全双工），先进先出</span>。一个进程在管道尾部写入，另个进程在管道头部读出（<span style="color:rgb(0, 176, 240)">但是这里14年真题D选项有争议</span>）
Linux中有匿名管道和命名管道。
匿名管道：`ls | grep thread`,的`|`是一个匿名管道，将前一个命令的输出作为后一个命令的输入。在这里ls进程会创造grep子进程，通过匿名管道传输。
命名管道：可以用于本机任何多个进程之间通信。进程不需要有父子关系。

管道原理：**消息传递模型，由内核维护一个内核缓冲区，两个进程基于这个内存缓冲区通信**
注意点：
1.**管道如果满了，写数据阻塞；管道如果空的，读数据阻塞；**
2.匿名管道（pipe）是单向的：数据只能从写端流向读端。如果要实现双向通信，通常需要创建两个管道。命名管道（FIFO）本质上也是单向的，但有些系统支持读写端同时打开（14年争议题？），不过逻辑上仍建议单向使用。
多个进程同时读写管道的情况：
多个写者：内核保证当一次写入的数据量不超过 PIPE_BUF（通常为 4096 字节）时，写操作是**原子**的，即不会出现数据交叉。超过该大小则不保证原子性。
多个读者：多个进程同时读同一个管道会导致数据竞争，每个数据只会被一个进程读到，但哪个进程读到不确定，通常需要外部同步机制来协调，管道本身不提供锁机制。

3.管道只能用于本机进程通信，socket可用于本机也可用于不同机器进程通信。

信箱通信：send发送消息**原语**，receive接受消息**原语**。

### 信号
1.在内核中传递一个信号（整数）2不同值信号量不同3.允许用户自定义
发送信号：内核修改**PCB**中的信号队列；发送信号可能因为1内核检测到系统事件，比如除0错误或子进程终止2一个进程调用了kill函数
一个进程可以发信号给自己。
接收信号：目的进程被内核强迫以某种方式对发送的信号做出反应。

信号处理函数是用户态代码，一般不信任，不在内核态直接运行。所以：
<span style="color:rgb(255, 0, 0)"><b>进程收到信号后，不会立马处理，而是等到异常处理程序执行完，然后从内核态切换到用户态这个时间点才去查看标记</b></span>
###### 以除0异常为例：
```c
int main() {
    signal(SIGFPE, handler);   // 用户注册了 SIGFPE 的处理函数
    int a = 10, b = 0;
    int c = a / b;             // 执行除法指令，b = 0，触发除 0 异常
    printf("c = %d\n", c);     // 如果信号处理函数未终止进程，则最终回到这里继续执行
    return 0;
}

void handler(int sig) {
    printf("Caught SIGFPE!\n");
    // 处理函数返回，或者调用 exit()
}
```
内核态伪代码流程：
1.硬件触发异常，陷入内核
```
CPU 执行除法指令时检测到除数为 0
硬件自动完成：
    保存用户态现场（寄存器、PC 等）到内核栈
    切换到内核态
    跳转到除 0 异常处理程序入口（IDT 中的 0 号向量）
```
2.转内核异常处理程序
```c
void divide_error_handler() {
    // 此时处于内核态，当前进程为触发异常的进程
    current->trap_frame = 保存的用户态寄存器;  // 硬件已保存

    // 向当前进程发送 SIGFPE 信号
    send_signal(current, SIGFPE);
    // 这个函数只做：设置 current->pending 中 SIGFPE 对应的位

    // 异常处理结束，准备返回用户态
    // 在返回前检查是否有待处理信号
    do_signal(current->trap_frame);
}
```
3.检查并处理信号
```c
void do_signal(trap_frame *regs) {
    int sig;

    // 从 current->pending 中找到第一个未被阻塞且未忽略的信号
    sig = get_next_pending_signal(current);

    if (sig == SIGFPE) {
        // 用户注册了自定义处理函数
        if (current->sighand[SIGFPE].handler != SIG_DFL &&
            current->sighand[SIGFPE].handler != SIG_IGN) {

            // 在用户态栈上构造信号帧，保存原用户态上下文
            setup_user_sigframe(current, regs, sig);

            // 修改用户态返回地址为信号处理函数入口
            regs->user_ip = current->sighand[SIGFPE].handler;

            // 同时可能设置其他寄存器（如参数 sig）
            regs->user_arg1 = sig;

            // 返回后 CPU 将切换到用户态，并跳转到 handler 执行
        }
        // 如果是默认处理（SIG_DFL），通常会终止进程，这里略
    }
}

```

4.内核态返回用户态
```
执行 iret / sysret 指令
CPU 切换到用户态
根据修改后的 user_ip 跳转到 handler 函数入口
```
用户态处理函数执行：
```c
void handler(int sig) {
    // 此时在用户态运行
    printf("Caught SIGFPE!\n");
    // 函数返回时，会调用 sigreturn 系统调用（由 C 库自动插入）
}
```
5.handler触发，触发sigreturn系统调用
```
handler 执行 ret 指令
实际上编译器会在 handler 末尾插入调用 sigreturn()
sigreturn 陷入内核态
内核根据用户栈上保存的信号帧恢复原 trap_frame
再次返回用户态，回到原被中断的除法指令之后的位置继续执行
```


综上所述，
<div style="display:flex;justify-content:center;font-family:sans-serif;">
  <svg width="920" height="280" viewBox="0 0 920 280" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L8,3 z" fill="#000" />
      </marker>
      <marker id="arrow-dashed" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L8,3 z" fill="#000" />
      </marker>
    </defs>
    <!-- 用户态第一行 -->
    <circle cx="60" cy="50" r="5" fill="#000" />
    <text x="60" y="32" text-anchor="middle" font-size="13">用户态：除法指令</text>
    <circle cx="180" cy="50" r="5" fill="#000" />
    <text x="180" y="32" text-anchor="middle" font-size="13">异常触发</text>
    <!-- 内核态中间行 -->
    <circle cx="180" cy="130" r="5" fill="#000" />
    <text x="180" y="112" text-anchor="middle" font-size="13">内核：异常处理程序</text>
    <circle cx="340" cy="130" r="5" fill="#000" />
    <text x="340" y="112" text-anchor="middle" font-size="13">发送SIGFPE置pending</text>
    <circle cx="490" cy="130" r="5" fill="#000" />
    <text x="490" y="112" text-anchor="middle" font-size="13">do_signal检查信号</text>
    <circle cx="630" cy="130" r="5" fill="#000" />
    <text x="630" y="112" text-anchor="middle" font-size="13">构造信号帧改IP=handler</text>
    <!-- 用户态第二行 -->
    <circle cx="630" cy="210" r="5" fill="#000" />
    <text x="630" y="192" text-anchor="middle" font-size="13">用户态：执行signal handler</text>
    <circle cx="770" cy="210" r="5" fill="#000" />
    <text x="770" y="192" text-anchor="middle" font-size="13">sigreturn系统调用</text>
    <!-- 内核恢复节点 -->
    <circle cx="770" cy="130" r="5" fill="#000" />
    <text x="770" y="112" text-anchor="middle" font-size="13">内核：恢复原上下文</text>
    <!-- 回到原程序终点 -->
    <circle cx="880" cy="50" r="5" fill="#000" />
    <text x="880" y="32" text-anchor="middle" font-size="13">用户态：继续原程序</text>

    <!-- 用户态顶部横向实线 -->
    <line x1="67" y1="50" x2="173" y2="50" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />
    <!-- 除法异常向下进入内核 虚线 -->
    <path d="M180,55 L180,123" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrow-dashed)" />
    <!-- 内核横向流程实线 -->
    <line x1="187" y1="130" x2="333" y2="130" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />
    <line x1="347" y1="130" x2="483" y2="130" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />
    <line x1="497" y1="130" x2="623" y2="130" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />
    <!-- 内核向下切回用户态执行handler 虚线 -->
    <path d="M630,137 L630,203" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrow-dashed)" />
    <!-- handler横向到sigreturn实线 -->
    <line x1="637" y1="210" x2="763" y2="210" stroke="#000" stroke-width="1.5" marker-end="url(#arrow)" />
    <!-- sigreturn向上陷入内核恢复上下文 虚线 -->
    <path d="M770,203 L770,137" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrow-dashed)" />
    <!-- 内核恢复上下文斜向回到顶部用户态原程序 虚线 -->
    <path d="M777,130 L873,50" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#arrow-dashed)" />
  </svg>
</div>

```
用户态：除法指令 → 异常 → 陷入内核
内核态：异常处理程序 → 发送 SIGFPE（设置 pending 位）→ do_signal 检查信号
         → 构造信号帧，修改用户态 IP = handler
返回用户态：直接执行 handler
用户态：handler 执行 → sigreturn 系统调用
内核态：恢复原上下文
返回用户态：继续执行原程序（若未退出）
```



（同一进程内部的）线程通信：共享内存


# CPU调度
## 调度层次与联系
**高级调度**：作业调度，对象是作业。选择外存队列中的作业进入内存。用于多道批处理系统，在分时和实时系统不设置高级调度。
**中级调度**：内存调度。为了提高内存利用率和吞吐量。把内存中暂时阻塞的进程调到外存，把进程状态修改为挂起状态。（此时为静止就绪或者静止阻塞）
**低级调度**：叫进程调度或短程调度。对象是进程（或内核级线程）。决定就绪队列哪个进程获得处理机。
调度的概念：
1批处理任务，周期性任务；2交互式任务，用户需要在很短时间获得响应；3实时处理任务，任务必须在规定的时间内完成相应功能；几乎所有的任务（进程）的IO请求（磁盘或网络）和CPU计算都是交替发生的。
## 调度的实现
进程的调度必需使用中断处理程序，因为只有中断才能让CPU从用户态切换到内核态。
#### 调度的时机：
非抢占式调度：只有一个进程完成或者阻塞后，才能分配cpu给别的。用于<span style="color:rgb(255, 0, 0)">早期批处理系统</span>。
抢占式调度：允许暂停正在执行的进程，分配个更为重要的进程。适用于<span style="color:rgb(255, 0, 0)">分时和实时系统</span>



<span style="color:rgb(255, 0, 0)">非抢占式调度中，调度必然发生在退出执行态。除非cpu空闲这一特殊情况。</span>

1.一个进程从运行切换到等待（阻塞态）
进程发出IO请求，进程调用wait系统调用，进程等待进入临界区。
2.一个进程从运行态切换为就绪态，比如时钟中断（时间片完）。
3.一个进程从等待切换到就绪状态时，比如IO完成时。
4.一个进程终止时。
如果一个调度只能发生在1，4情况；则为非抢占的。如果都能发生，则为抢占的。
除了以上4个，还有一个是系统调用完成并返回用户态时进行处理机调度。为了让cpu检查有没有高优先级进程到达。系统调用的高频性和内核态权限强制cpu在继续执行低优先级用户进程继续前，能够检查就绪队列确保高优先级不会被饿死。


总结一些：
##### 允许调度的时机
进程主动放弃cpu的情况：运行->阻塞、终止、就绪
外部事件导致调度：时间片完，更高进程优先级就绪（IO完成，信号量释放），新进程创建或用户登录（抢占式），阻塞进程被唤醒，中断或系统调用返回
特殊情况：cpu空闲，就绪队列空，新进入的立马调度。

##### 不允许调度的时机
**原子操作，原语**（信号量操作、关中断、修改 PCB）；**处于内核态临界区**（进程持有自旋锁、访问共享内核数据结构（如就绪队列、文件表、页表等））；**中断服务程序执行期间**；**进程切换过程中**（ 在保存/恢复现场、切换内核栈等操作期间，不允许再发生调度，否则会破坏现场）；**修改关键内核数据时**（更新页表、内存管理数据结构等，必须保证原子性，不可调度。）

注意⚠️- **进程处于用户态临界区时，不影响处理机调度；进程处于内核态临界区时，通常不能进行调度。**



以打印机为例子
[[用户态临界区和内核态临界区在调度上区别]]








##### 调度程序（调度器）
排队器+分派器+上下文切换器
排队器：就绪队列
分派器：从就绪队列取出，从分排期到新选进程间上下文切换，以分配cpu。
上下文切换器：把当前进程cpu寄存器内容保存到该进程pcb内相应单元。
上下文：用户级上下文（用户程序段、数据段
、堆栈），系统级上下文（PCB，系统内核栈），寄存器上下文（通用寄存器，程序计数器PC，程序状态字PSW、页表基地址寄存器）

#### 调度目标与指标
cpu利用率（$CPU利用率 = \frac{cpu有效工作时间}{cpu有效工作时间+cpu空闲等待时间}$），公平性，平衡性。
**批处理系统目标**：1平均周转时间短。$任务周转时间 = 任务完成时间-任务提交时间$
平均周转时间为n个作业周转时间的均值
2等待时间尽可能短3系统吞吐量高

**分时系统目标**：1响应时间快2均衡性

**实时系统目标**：1截止时间保证2可预测性

带权周转时间：$W_i = \frac{作业i周转时间}{作业i实际运行时间}$
平均带权周转时间，Wi求平均
	



#### 临界资源和临界区
临界资源是一个时间段内只允许一个进程使用的资源。
内核临界资源：PCB，打印机，就绪/阻塞队列，信号量，页表，系统级文件打开表，索引结点等。
用户临界资源：多线程共享的全局变量，用户缓冲区
## 调度算法

#### FCFS先来先服务
非抢占的

#### 短作业优先SJF
非抢占式短作业优先，抢占式短作业优先（最短剩余时间优先）
优点：平均等待时间和平均周转时间均最小；
缺点：长进程饥饿

#### 高响应比优先(HRRN)调度算法
$响应比 = \frac{等待时间+执行时间}{执行时间}$
规则:选响应比最高的进程上cpu
优点:综合考虑等待时间和运行时间
**属于非抢占式**
#### 时间片轮转(RR)调度算法
优点：公平，响应快，适用于分时操作系统；
缺点：有一定开销，不区分任务紧急程度；
**完全不会导致饥饿**

#### 优先级调度
每一个进程或任务都有一个优先级与其关联，具有最高优先级的进程会优先分配给cpu。具有相同优先级的进程按照FCFS调度。
##### 静态优先级
在创建进程的时候确定，在进程整个运行期间保持不变。
1.系统进程>用户进程；
2.交互进程>非交互进程；
3.IO进程>计算型进程；
4.用户要求；
5.进程对资源的需求少的优先，减少所有进程的平均等待时间和平均周转时间；
##### 动态优先级
优先级会随着进程推进或者等待时间增加改变。

#### 时钟中断处理流程
时钟中断的作用：进程调度，时间管理，超时处理；
预先设置时间间隔，到期时向CPU发送中断请求（IRQ）。时钟中断时可屏蔽中断。

#### 多CPU调度
CPU亲和性：即一个进程对它运行的处理器具有亲和性。
软亲和：OS试图保持进程运行在同一处理器，但不强制
硬亲和：通过syscall允许某个进程运行在某个cpu而不会迁移到其他cpu

负载均衡：
推迁移：一个特定任务周期性地检查每个cpu负载，如果不平衡，把进程从超载cpu推到空闲一点的。
拉迁移：当空闲cpu从一个忙cpu里拉一个等待任务。
### 多级队列调度算法

多个就绪队列，可采用不同调度算法。
每个队列的优先级都高于更低层队列。进程进入系统时被永久分配到某个队列。
### 多级反馈队列调度算法

目标：如果不知道任务长短，一开始假设是短任务，赋予其最高优先级，如果确实是短，那么很快执行完；否则慢慢移到低优先级队列，则认为是长任务。
考虑因素：队列数量，每个队列调度算法，升级，降级时机，确定进程需要服务时进入到哪个队列的方法
缺点：可能产生饥饿，一个任务可能在不同时间所属不同类型
解决方法：低优先级队列任务周期性扔到高优先级队列。
# 同步与互斥
同步：直接制约，A,B有先后关系；
互斥：间接制约，A,B不能访问临界资源。
## 互斥
### 并发安全问题
只有读-读不需要互斥，读-写和写-写操作都需要互斥！
### 临界资源
系统资源，不同进程通过互斥访问临界资源。
### 临界区
访问临界资源的代码
多个线程交替执行临界区，就会发生并发安全问题。
#### 临界区问题
实现进程互斥时，应遵循的**四条重要原则**：
1.空闲让进
2.忙则等待：确保互斥访问临界资源
3.有限等待：不能饿死
4.让权等待：避免忙等。但不是必须的，比如自旋锁


例题:
（2016）进程 P1 和 P2 均包含并发执行的线程，部分伪代码描述如下所示。

```c
//进程 P1
int x=0; 
Thread1()
{
    int a;
    a=1;  x += 1;
}
Thread2()
{
    int a;
    a=2;  x += 2;
}

//进程 P2
int x=0;
Thread3()
{
    int a;
    a=x;  x += 3;
}
Thread4()
{
    int b;
    b=x;  x += 4;
}
```

下列选项中，需要互斥执行的操作是（）。
A. `a=1`与`a=2` B. `a=x`与`b=x` C. `x+=1`与`x+=2` D. `x+=1`与`x+=3`

解析:一个进程可以包含多个线程，这些线程共享该进程的地址空间中的**全局变量、堆、静态变量**等，但每个线程有自己的**栈**，所以局部变量是线程私有的.

```c
//1.c
// 进程 P1
int x = 0;              // P1 的全局变量，被 P1 内的所有线程共享
Thread1() {
    int a;              // Thread1 的局部变量，线程私有
    a = 1;
    x += 1;             // 修改共享变量 x
}
Thread2() {
    int a;              // Thread2 的局部变量，与 Thread1 的 a 无关
    a = 2;
    x += 2;             // 修改同一个共享变量 x
}

//2.c
// 进程 P2
int x = 0;              // P2 的全局变量，与 P1 的 x 完全不同
Thread3() {
    int a;
    a = x;              // 读 P2 的 x
    x += 3;             // 写 P2 的 x
}
Thread4() {
    int b;
    b = x;              // 读 P2 的 x
    x += 4;             // 写 P2 的 x
}
```

因此A和B的a,b都是线程私有局部变量，无需考虑互斥；C中的x为不同进程私有，也不需要考虑，选D。同一进程内的全局变量x是两个线程的共享变量，需要考虑。

### 互斥的软件实现方式
#### 单一标志法 能实现互斥，但不对
设置一个公用整型变量turn，指示允许进入临界区的进程编号。tur=0允许p0，turn=1允许p1
```c
//process P0
while(turn!=0);//进入区
critical section;//临界区
turn = 1;退出区
remainder section;

//process P1
while(turn!=1);//进入区
critical section;//临界区
turn = 0;退出区
remainder section;

```
缺点:违反了空闲让进，让权等待
#### 双标志先检查 错
```c
//process Pi
while(flag[j]) ;//1别人想进？
flag[i]=TRUE;//3自己想进
critical section;
flag[i] = FALSE;
remainder section;

//process Pj
while(flag[i]) ;//2别人想进？
flag[j]=TRUE;//4自己想进
critical section;
flag[j] = FALSE;
remainder section;
```
1-2-3-4,都会进入临界区。
缺点：违反忙则等待，让权等待

#### 双标志后检查 错
```c
//Pi
flag[i] = TRUE;1
while(flag[j]);3
critical section;
flag[i] = FALSE;
remainder section;

//Pj
flag[j] = TRUE;2
while(flag[i]);4
critical section;
flag[i] = FALSE;
remainder section;
```
1234:(两个进不去，饥饿)：违反空闲让进、有限等待、让权等待

#### Peterson算法（正确的算法）
适用于两个进程/线程交错执行临界区和剩余区
flag标识哪个进程准备进入
```c
int turn = 0;
boolean flag[2] = {FALSE,FALSE}
void P0(){
while (TRUE){
	flag[0] = TRUE;turn=1;
	while(flag[1] && turn==1);
	critical section;
	flag[0] = FALSE;
	}
}
void P1(){
while (TRUE){
	flag[1] = TRUE;turn=0;
	while(flag[1] && turn==1);
	critical section;
	flag[1] = FALSE;
	}
}
```
因为赋值语句由一条store实现，不会被中断，只有一个turn的赋值结果会被保存。因此只有一个进程可以成功写覆盖turn，标志哪个进程允许进入临界区。
缺点：不满足让权等待；


### 互斥的硬件实现方法
#### 中断屏蔽法
```c
while(true){
	关中断;
	critical section;
	开中断;
	remainder;
}
```
缺点：1.将关中断权限交给用户很不明智，要么就只能在内核中用，而不能用于用户程序。2.不适用于多处理器系统。

#### 特殊硬件指令
TestAndSet和swap
不可被打断，不可被拆分。
#### test_and_set指令
功能:原子操作，独户指定标志，设置为真
```c
//共享数据:boolean lock =FALSE;
boolean TestAndSet(Boolean*lock){
	boolean old = *lock;
	*lock = true;
	return old;
}

void Pi(){
	do{
		while(TestAndSet(lock));
		critical section;
		lock=FALSE;
		remainder section;
	}
}
```

没有实现让权等待。但是无法主动释放cpu并不意味着单cpu会死循环，因为时间片到了就有时钟中断，调度程序。

#### compare_and_swap指令
功能：**原子性的**交换两个变量。
```c
int compare_and_swap(int *value, int expected, int new_value){
	int temp = *value;
	if(*value ==expected) *value = new_value;
	return temp;
}

```
# 锁与死锁
## 锁
互斥锁：可以实现让权等待；
自旋锁：违背让权等待,适用于多处理器系统。
以模拟打印机为例，假设多个线程使用单个临界资源打印机。通过给临界区加锁，可以保证临界区只有一个线程活跃，这种锁成为互斥锁。
```c
static lock_t mutex;
init(&mutex);

void simPrint(char *str){
	lock(&mutex); //获取锁，拿到锁的线程可以进入临界区
	while(*str!=0){
		printf("%c",*str++);
		fflush(stdout);
		sleep(1);
	}
	printf("\n");
	unlock(&mutex); //执行完毕，释放锁
}

```
锁的实现


自旋锁:1等待锁达到打开2获得锁并锁上
闭锁的两个操作应该是原子的

TAS指令实现互斥锁
```c
void lock(lock_t *mutex){
	while(test_and_set(&mutex->flag));//自旋等待
}
```

CAS指令实现互斥锁
```c
void lock(lock_t *mutex){
	while(compare_and_swap(&mutex->flag,0,1)==1);
}
```

以上线程等待被持有锁时，采用了自旋等待技术，这种互斥锁称为自旋锁。
单cpu情况下，自旋锁的性能开销很大。但是，多CPU情况下，自旋锁性能良好。
但是不满足有限等待，自旋锁没有公平性，可能导致饿死。

##### 公平的自旋锁（ticket锁）
设计原子指令fetch_and_add():原子地返回特定地址的旧值，并且让该值+1.
```c
void lock(lock_t *mutex){
	//当前线程拿到自己的号码
	int myturn = fetch_and_add(&mutex->ticket);
	//如果可以进入临界区的号码是自己的，则进入
	while(mutex->turn != myturn);//自旋等待

}
void unlock(lock_t *mutex){
	//更新进入临界区的号码
	fetch_and_add(mutex->turn);
}
```

## 死锁
### 死锁的条件
1互斥：至少一个资源处于非共享模式。
2.占有并等待：一个进程应占有至少一个资源，并等待一个被其他进程占有的另一个资源
3.非抢占：资源不能被抢占
4.循环等待

死锁的充要条件即资源分配图有环。
假设进程数n，同类型资源数m，$max[i]$表示进程i的最大资源需求数，i从1到n。则发生死锁的必要条件为$sum(max[i]-1) \ge m$

#### 死锁的预防
**死锁预防从根本上杜绝死锁发生可能**。但是会降低资源利用率。
互斥条件必须成立，一般无法否定。
对于占有和等待：解决方案1每个进程在执行前一次性申请并获得所有资源。（利用率低）
2允许进程仅在没有资源时可以申请。（饥饿）
对于非抢占：可以让如果一个进程A持有资源并申请另一个不能立即分配的自愈暗时，进程A现在占有的资源可以被其他进程抢占。比如处理机和内存都可以被抢占。
但是**不可抢占资源有：光盘，磁带机，打印机，互斥锁，信号量**。
3.对于循环等待，方法是对所有资源类型完全排序，且要求每个进程按递增顺序申请资源。
缺点：降低资源利用率，灵活性差，破坏进程原子性

#### 死锁的避免
##### 安全序列
安全序列是指系统能按一定顺序为进程分配资源来避免死锁，那么系统的状态就是安全的。
安全状态一定能避免死锁，但并不是非安全状态一定导致死锁。

#### 资源分配图和银行家算法
资源分配图适用于每种资源类型只有一个实例检测环。
银行家算法效率不如资源分配图。
死锁避免的有点：资源利用率高，进程灵活性强，避免不必要等待。
缺点：实现复杂，使用场景受限（需预先声明最大资源需求量，仅适用于资源可动态分配，进程较少），可能存在保守决策


#### 死锁检测
不需要提前获得最大资源需求总量。
有点：灵活性高，资源利用率高，使用场景广
缺点：安全性低允许发生死锁，回复成本高，检测频率难以确定

#### 死锁恢复/消除
1.进程终止2.从一个或多个死锁进程抢占资源



# 信号量

## 整形

## 记录型
