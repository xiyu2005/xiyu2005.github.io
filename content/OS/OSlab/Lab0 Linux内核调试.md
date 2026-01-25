# Part 1 环境搭建
首先
```
docker pull git.zju.edu.cn:5050/zju-cs-lab/tool/sys:latest
```
在校外需要atrust连接

需要
```
(base) kaisenye@kaisendeMacBook-Air oslab % ssh-keygen -t ed25519 -C "3230100127@zju.edu.cn"
```
生成pubkey后复制到zjugit里面
```
(base) kaisenye@kaisendeMacBook-Air oslab % ssh -T git@git.zju.edu.cn
Welcome to GitLab, @3230100127!
```
这样就可以git clone了

```
(base) kaisenye@kaisendeMacBook-Air code % docker compose up -d
[+] Running 2/2
 ✔ Network code_default          Created                                                                 0.0s 
 ✔ Container code-zju-os-code-1  Started                                                                 0.3s 
(base) kaisenye@kaisendeMacBook-Air code % docker compose exec -it zju-os-code
requires at least 2 arg(s), only received 1
(base) kaisenye@kaisendeMacBook-Air code % docker compose exec -it zju-os-code fish
Welcome to fish, the friendly interactive shell
Type help for instructions on how to use fish
root@zju-os /z/code (lab5)# ls
autograder/  CODEOWNERS  compose.yml  gdbinit  gdbinit.py  kernel/  LICENSE  Makefile  openocd.cfg  README.md

root@zju-os /z/code (lab5)# exit
(base) kaisenye@kaisendeMacBook-Air code % docker ps                               
CONTAINER ID   IMAGE                                            COMMAND            CREATED              STATUS              PORTS     NAMES
5e8530be919a   git.zju.edu.cn:5050/zju-cs-lab/tool/sys:latest   "sleep infinity"   About a minute ago   Up About a minute             code-zju-os-code-1
(base) kaisenye@kaisendeMacBook-Air code % docker compose down
[+] Running 2/2
 ✔ Container code-zju-os-code-1  Removed                                                                 0.1s 
 ✔ Network code_default          Removed   
```


考点：
- 拉取的 `git.zju.edu.cn:5050/zju-cs-lab/tool/sys:latest` 是「镜像」：包含 RISC-V 交叉编译工具链、QEMU、GDB 等实验必需环境，是固定不变的模板；
- 用 `docker run` 或 `docker compose up` 启动的 `zju-os-code` 是「容器」：基于上述镜像创建的运行实例，你在里面编译内核、调试代码的操作，都在容器这个「动态环境」中进行。
概念	本质
镜像（Image）	静态的、只读的「环境模板」，包含运行应用所需的所有资源（系统内核、工具链、代码、依赖等）。
容器（Container）	镜像的「动态运行实例」，是镜像加载到内存后形成的可读写运行环境，具备独立的文件系统、进程空间。



我发现vscode的devcontainer打开才可以在容器内拆分终端，如果是docker exec进入的则不能拆分。这个大家可以注意一下。
# Part 1
## Part 2 Linux 内核调试
### 2.1 交叉工具链

用 C 写一个 Hello World 程序，然后执行下面的步骤：
- 生成它的 RISC-V 汇编代码
```sh
root@zju-os /z/c/lab0 (lab0)# riscv64-linux-gnu-gcc -S hello.c -o hello.s
root@zju-os /z/c/lab0 (lab0)# cat hello.s
        .file   "hello.c"
        .option pic
        .attribute arch, "rv64i2p1_m2p0_a2p1_f2p2_d2p2_c2p0_zicsr2p0_zifencei2p0_zmmul1p0_zaamo1p0_zalrsc1p0_zca1p0_zcd1p0"
        .attribute unaligned_access, 0
        .attribute stack_align, 16
        .text
        .section        .rodata
        .align  3
.LC0:
        .string "Hello RISC-V!"
        .text
        .align  1
        .globl  main
        .type   main, @function
main:
.LFB0:
        .cfi_startproc
        addi    sp,sp,-16
        .cfi_def_cfa_offset 16
        sd      ra,8(sp)
        sd      s0,0(sp)
        .cfi_offset 1, -8
        .cfi_offset 8, -16
        addi    s0,sp,16
        .cfi_def_cfa 8, 0
        lla     a0,.LC0
        call    puts@plt
        li      a5,0
        mv      a0,a5
        ld      ra,8(sp)
        .cfi_restore 1
        ld      s0,0(sp)
        .cfi_restore 8
        .cfi_def_cfa 2, 16
        addi    sp,sp,16
        .cfi_def_cfa_offset 0
        jr      ra
        .cfi_endproc
.LFE0:
        .size   main, .-main
        .ident  "GCC: (Debian 15.2.0-4) 15.2.0"
        .section        .note.GNU-stack,"",@progbits
```
- 将其编译为 RISC-V 可执行程序
```sh
root@zju-os /z/c/lab0 (lab0)# riscv64-linux-gnu-gcc hello.c -o hello
root@zju-os /z/c/lab0 (lab0)# file hello
hello: ELF 64-bit LSB pie executable, UCB RISC-V, RVC, double-float ABI, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-riscv64-lp64d.so.1, BuildID[sha1]=6e8972e2c0c9b14562399e260c882034be55eaca, for GNU/Linux 4.15.0, not stripped
```
- 将 RISC-V 可执行程序反汇编

```sh
root@zju-os /z/c/lab0 (lab0)# riscv64-linux-gnu-objdump -d hello > hello.d
is
root@zju-os /z/c/lab0 (lab0)# cat hello.dis

hello:     file format elf64-littleriscv


Disassembly of section .plt:

0000000000000590 <.plt>:
 590:   00002397                auipc   t2,0x2
 594:   41c30333                sub     t1,t1,t3
 598:   a603be03                ld      t3,-1440(t2) # 1ff0 <.got.plt>
 59c:   fd430313                addi    t1,t1,-44
 5a0:   a6038293                addi    t0,t2,-1440
 5a4:   00135313                srli    t1,t1,0x1
 5a8:   0082b283                ld      t0,8(t0)
 5ac:   000e0067                jr      t3

00000000000005b0 <__libc_start_main@plt>:
 5b0:   00002e17                auipc   t3,0x2
 5b4:   a50e3e03                ld      t3,-1456(t3) # 2000 <__libc_start_main@GLIBC_2.34>
 5b8:   000e0367                jalr    t1,t3
 5bc:   00000013                nop

00000000000005c0 <puts@plt>:
 5c0:   00002e17                auipc   t3,0x2
 5c4:   a48e3e03                ld      t3,-1464(t3) # 2008 <puts@GLIBC_2.27>
 5c8:   000e0367                jalr    t1,t3
 5cc:   00000013                nop

Disassembly of section .text:

00000000000005d0 <_start>:
 5d0:   022000ef                jal     5f2 <load_gp>
 5d4:   87aa                    mv      a5,a0
 5d6:   00002517                auipc   a0,0x2
 5da:   a0253503                ld      a0,-1534(a0) # 1fd8 <_GLOBAL_OFFSET_TABLE_+0x10>
 5de:   6582                    ld      a1,0(sp)
 5e0:   0030                    addi    a2,sp,8
 5e2:   ff017113                andi    sp,sp,-16
 5e6:   4681                    li      a3,0
 5e8:   4701                    li      a4,0
 5ea:   880a                    mv      a6,sp
 5ec:   fc5ff0ef                jal     5b0 <__libc_start_main@plt>
 5f0:   9002                    ebreak

00000000000005f2 <load_gp>:
 5f2:   00002197                auipc   gp,0x2
 5f6:   21e18193                addi    gp,gp,542 # 2810 <__global_pointer$>
 5fa:   8082                    ret
 5fc:   0001                    nop

00000000000005fe <deregister_tm_clones>:
 5fe:   00002517                auipc   a0,0x2
 602:   a1a50513                addi    a0,a0,-1510 # 2018 <__TMC_END__>
 606:   00002797                auipc   a5,0x2
 60a:   a1278793                addi    a5,a5,-1518 # 2018 <__TMC_END__>
 60e:   00a78863                beq     a5,a0,61e <deregister_tm_clones+0x20>
 612:   00002797                auipc   a5,0x2
 616:   9be7b783                ld      a5,-1602(a5) # 1fd0 <_ITM_deregisterTMCloneTable@Base>
 61a:   c391                    beqz    a5,61e <deregister_tm_clones+0x20>
 61c:   8782                    jr      a5
 61e:   8082                    ret

0000000000000620 <register_tm_clones>:
 620:   00002517                auipc   a0,0x2
 624:   9f850513                addi    a0,a0,-1544 # 2018 <__TMC_END__>
 628:   00002597                auipc   a1,0x2
 62c:   9f058593                addi    a1,a1,-1552 # 2018 <__TMC_END__>
 630:   8d89                    sub     a1,a1,a0
 632:   4035d793                srai    a5,a1,0x3
 636:   91fd                    srli    a1,a1,0x3f
 638:   95be                    add     a1,a1,a5
 63a:   8585                    srai    a1,a1,0x1
 63c:   c599                    beqz    a1,64a <register_tm_clones+0x2a>
 63e:   00002797                auipc   a5,0x2
 642:   9aa7b783                ld      a5,-1622(a5) # 1fe8 <_ITM_registerTMCloneTable@Base>
 646:   c391                    beqz    a5,64a <register_tm_clones+0x2a>
 648:   8782                    jr      a5
 64a:   8082                    ret

000000000000064c <__do_global_dtors_aux>:
 64c:   00002797                auipc   a5,0x2
 650:   9cc7c783                lbu     a5,-1588(a5) # 2018 <__TMC_END__>
 654:   e79d                    bnez    a5,682 <__do_global_dtors_aux+0x36>
 656:   1141                    addi    sp,sp,-16
 658:   e406                    sd      ra,8(sp)
 65a:   00002797                auipc   a5,0x2
 65e:   9867b783                ld      a5,-1658(a5) # 1fe0 <__cxa_finalize@GLIBC_2.27>
 662:   c791                    beqz    a5,66e <__do_global_dtors_aux+0x22>
 664:   00002517                auipc   a0,0x2
 668:   9ac53503                ld      a0,-1620(a0) # 2010 <__dso_handle>
 66c:   9782                    jalr    a5
 66e:   f91ff0ef                jal     5fe <deregister_tm_clones>
 672:   60a2                    ld      ra,8(sp)
 674:   4785                    li      a5,1
 676:   00002717                auipc   a4,0x2
 67a:   9af70123                sb      a5,-1630(a4) # 2018 <__TMC_END__>
 67e:   0141                    addi    sp,sp,16
 680:   8082                    ret
 682:   8082                    ret

0000000000000684 <frame_dummy>:
 684:   bf71                    j       620 <register_tm_clones>

0000000000000686 <main>:
 686:   1141                    addi    sp,sp,-16
 688:   e406                    sd      ra,8(sp)
 68a:   e022                    sd      s0,0(sp)
 68c:   0800                    addi    s0,sp,16
 68e:   00000517                auipc   a0,0x0
 692:   02250513                addi    a0,a0,34 # 6b0 <_IO_stdin_used+0x8>
 696:   f2bff0ef                jal     5c0 <puts@plt>
 69a:   4781                    li      a5,0
 69c:   853e                    mv      a0,a5
 69e:   60a2                    ld      ra,8(sp)
 6a0:   6402                    ld      s0,0(sp)
 6a2:   0141                    addi    sp,sp,16
 6a4:   8082                    ret
```

三个步骤对应的工具及作用：
1. **生成 RISC-V 汇编代码**：用 `riscv64-linux-gnu-gcc`，加 `-S` 参数，将 C 代码转为 RISC-V 汇编指令；
2. **编译为可执行程序**：用 `riscv64-linux-gnu-gcc`，完成完整编译流程，生成 RISC-V 架构的二进制可执行文件；
3. **反汇编**：用 `riscv64-linux-gnu-objdump`，加 `-d` 参数，把二进制程序还原为 RISC-V 汇编代码，便于分析执行逻辑。


### 2.2 编译本地架构内核
```
root@zju-os /zju-os# cd /opt/linux-source-6.16
make defconfig
make -j$(nproc)
```
![[Pasted image 20260118192723.png]]
![[Pasted image 20260118193603.png]]
编译成功。

defconfig含义：- 基于指定的 CPU 架构（ARCH），生成该架构下的「默认内核配置文件」（`.config`），这个文件是内核编译的核心配置（决定编译哪些功能、支持哪些硬件）。
distclean含义：mrproper + remove editor backup and patch files（`mrproper` 会删除所有编译产物 + 配置文件，`distclean` 在此基础上删编辑器备份 / 补丁文件）

### 2.3  交叉编译 RISC-V 架构内核
**使用哪两个变量来指定目标架构？**
ARCH：指定目标 CPU 架构（如 riscv、arm、x86）。
CROSS_COMPILE：指定交叉编译工具链的前缀（如 riscv64-linux-gnu-）。
**这两个变量的值在哪里找？**
ARCH 的值：查看内核源码根目录下的 arch/ 子目录名。本实验中目标是 RISC-V，所以值是 riscv。
CROSS_COMPILE 的值：在系统终端输入 riscv64- 然后按补全键，看工具链的名字。在本实验容器中，前缀是 riscv64-linux-gnu-。
**如何在命令行中为 make 指定变量的值？**
在 make 命令后面直接以 变量名=值 的形式跟上，例如：make ARCH=riscv CROSS_COMPILE=riscv64-linux-gnu-。


步骤：
之前编译过一次本地（ARM64）架构的内核，需要清理
```
make distclean
```
生成 RISC-V 的默认配置文件
```
make ARCH=riscv defconfig
```
交叉编译
```
make ARCH=riscv CROSS_COMPILE=riscv64-linux-gnu- -j$(nproc)
```
![[Pasted image 20260118194946.png]]
![[Pasted image 20260118195031.png]]
### 2.4用 QEMU 运行 RISC-V 内核
因为我之前的linux内核在另个文件夹所以目录要改一下
```
make run KERNEL_PATH=/opt/linux-source-6.16 ROOTFS_PATH=/opt/rootfs.ext2
```
成功，并测试
![[Pasted image 20260118195739.png]]


按住ctrl+A 然后一起松开，再按C，提示词变成了（qemu）![[Pasted image 20260118200719.png]]
qemu monitor就类似资源监视器，可以查看信息，也可以进行暂停虚拟机，强制重启，安全退出等等。
打印寄存器的值
```
(qemu) info registers

CPU#0
 V      =   0
 pc       ffffffff80b59100
 mhartid  0000000000000000
 mstatus  0000000a000000a0
 hstatus  0000000200000000
 vsstatus 0000000a00000000
 mip      0000000000000000
 mie      000000000000022a
 mideleg  0000000000001666
 hideleg  0000000000000000
 medeleg  0000000000f4b509
 hedeleg  0000000000000000
 mtvec    00000000800004f8
 stvec    ffffffff80b65394
 vstvec   0000000000000000
 mepc     ffffffff8001c9d4
 sepc     ffffffff8005c17a
 vsepc    0000000000000000
 mcause   0000000000000009
 scause   8000000000000005
 vscause  0000000000000000
 mtval    0000000000000000
 stval    0000000000000000
 htval    0000000000000000
 mtval2   0000000000000000
 mscratch 0000000080047000
 sscratch 0000000000000000
 satp     a006e00000082e03
 x0/zero  0000000000000000 x1/ra    ffffffff80b5ab38 x2/sp    ffffffff81803dd0 x3/gp    ffffffff81a19d88
 x4/tp    ffffffff8180e0c0 x5/t0    ff20000000063c38 x6/t1    ffffffffc0000050 x7/t2    ffffffff9308b9a4
 x8/s0    ffffffff81803de0 x9/s1    0000000000000000 x10/a0   00000000000061ac x11/a1   0000000000000000
 x12/a2   ffffffff80e43dc8 x13/a3   0000000000000000 x14/a4   ff60000087199000 x15/a5   ff60000007fdcdc8
 x16/a6   ff60000007fdcdc8 x17/a7   4000000000000000 x18/s2   ffffffff81a1f240 x19/s3   0000000000000000
 x20/s4   0000000000000000 x21/s5   ffffffff81a1f018 x22/s6   0000000000000000 x23/s7   0000000000000001
 x24/s8   0000000000002000 x25/s9   0000000080043700 x26/s10  0000000000000000 x27/s11  0000000000000000
 x28/t3   0000000000000001 x29/t4   0000000000000000 x30/t5   ffffffff8100e0f0 x31/t6   0000000000000377
 fcsr     0000000000000000
 f0/ft0   0000000000000000 f1/ft1   0000000000000000 f2/ft2   0000000000000000 f3/ft3   0000000000000000
 f4/ft4   0000000000000000 f5/ft5   0000000000000000 f6/ft6   0000000000000000 f7/ft7   0000000000000000
 f8/fs0   0000000000000000 f9/fs1   0000000000000000 f10/fa0  0000000000000000 f11/fa1  0000000000000000
 f12/fa2  0000000000000000 f13/fa3  0000000000000000 f14/fa4  0000000000000000 f15/fa5  0000000000000000
 f16/fa6  0000000000000000 f17/fa7  0000000000000000 f18/fs2  0000000000000000 f19/fs3  0000000000000000
 f20/fs4  0000000000000000 f21/fs5  0000000000000000 f22/fs6  0000000000000000 f23/fs7  0000000000000000
 f24/fs8  0000000000000000 f25/fs9  0000000000000000 f26/fs10 0000000000000000 f27/fs11 0000000000000000
 f28/ft8  0000000000000000 f29/ft9  0000000000000000 f30/ft10 0000000000000000 f31/ft11 0000000000000000
```
查看内存映射info mem
![[Pasted image 20260118201248.png]]
查看设备树info tree
![[Pasted image 20260118201546.png]]
bus: main-system-bus是系统总线，
riscv.hart_array是RISC-V CPU 核心
```
dev: riscv.hart_array, id ""
  num-harts = 1 (0x1)          # 模拟1个RISC-V硬件线程（单核）
  hartid-base = 0 (0x0)        # 核心ID从0开始
  cpu-type = "rv64-riscv-cpu"  # 64位RISC-V CPU（实验用的架构）
  resetvec = 4096 (0x1000)     # 复位向量地址：CPU启动时先执行0x1000处的代码（OpenSBI的入口）
  rnmi-interrupt-vector = <null>
  rnmi-exception-vector = <null>
```
riscv.aclint.mtimer是时钟中断核心(定时器)
```
dev: riscv.aclint.mtimer, id ""
  gpio-out "" 1                # 定时器产生中断时，通过这条中断线通知CPU
  hartid-base = 0 (0x0)
  num-harts = 1 (0x1)
  timecmp-base = 0 (0x0)
  time-base = 32760 (0x7ff8)
  aperture-size = 32768 (0x8000)
  timebase-freq = 10000000 (0x989680)  # 定时器频率：10MHz（1秒产生1000万次脉冲）
  mmio 0000000002004000/0000000000008000  # 定时器的内存映射地址
```
riscv.sifive.plic（PLIC）中断控制器
```
dev: riscv.sifive.plic, id ""
    gpio-in "" 96
    gpio-out "" 2
    hart-config = "MS"
    hartid-base = 0 (0x0)
    num-sources = 96 (0x60)  # 支持96个中断源（定时器、网卡、硬盘等都算一个中断源）
    num-priorities = 7 (0x7)
    priority-base = 0 (0x0)
    pending-base = 4096 (0x1000)
    enable-base = 8192 (0x2000)
    enable-stride = 128 (0x80)
    context-base = 2097152 (0x200000)
    context-stride = 4096 (0x1000)
    aperture-size = 6291456 (0x600000)
    mmio 000000000c000000/0000000000600000 # PLIC的内存映射地址
```
虚拟硬盘：virtio-blk-device
drive = "hd0" # 对应QEMU挂载的根文件系统（rootfs.ext2） logical_block_size = 512 (512 B) # 硬盘扇区大小（和真实硬盘一致）
虚拟网卡virtio-net-device
dev: virtio-net-device, id "" mac = "52:54:00:12:34:56" # 网卡的MAC地址（虚拟） netdev = "net0" # 对应QEMU的网络设备，实现NAT联网

打印物理内存要用xp指令。（x是虚拟内存。）
![[Pasted image 20260118202838.png]]
# gdb
分屏
```
make debug KERNEL_PATH=/opt/linux-source-6.16 ROOTFS_PATH=/opt/rootfs.ext2


make gdb KERNEL_PATH=/opt/linux-source-6.16
```
``
ctrl+O X切换
![[Pasted image 20260118205019.png]]![[Pasted image 20260118205004.png]]
继续执行c
![[Pasted image 20260118205423.png]]
单步汇编 si
![[Pasted image 20260118205848.png]]
单步c语言 n（next，不进入函数） s（step 进入函数）
查看寄存器- i r (查看所有) 或 i r a0 a1 a2 (查看特定寄存器)
![[Pasted image 20260118210352.png]]

#### . 探究 OpenSBI 启动时

在 GDB 中输入以下命令：

1. 删除所有断点：del
2. 在 OpenSBI 起点打断点：b *0x80000000
    
3. 调试：输入 c
    
4. 当程序停在 0x80000000 时：
    
    - **查看 a2 寄存器**：执行 i r a2。
![[Pasted image 20260118211024.png]]
    - **查看内存内容**：执行 x/8gx $a2。
        ![[Pasted image 20260118211039.png]]
    - **原理复习**：QEMU 会把一个名为 struct fw_dynamic_info 的结构体地址放在 a2 里，OpenSBI 通过它知道下一步该跳到哪里（比如跳到 0x80200000）。
x/8gx $a2 输出：
第一个 64 位值：0x000000004942534f
如果你把这串十六进制按字节转成 ASCII 码：4f='O', 53='S', 42='B', 49='I'。
它合起来就是 "OSBI"。这是 OpenSBI 的魔数，证明了 a2 确实指向了 OpenSBI 的动态信息结构体。
第三个 64 位值：0x0000000080200000
这就是 next_addr。OpenSBI 读到这个值，就知道等会儿自己初始化完了，要跳转到 0x80200000 去执行内核。
然后
1. **在内核起点打断点**：  
    输入：b *0x80200000
    
2. **继续运行**：  
    输入：c  
    (程序会跳过 OpenSBI 的运行，直接停在内核的第一条指令)
    
3. **查看 a1 寄存器**：  
    输入：i r a1  
    这个 a1 存的是 OpenSBI 传给内核的参数（通常是设备树 DTB 的物理地址）。
    
4. **验证设备树魔数**：  
    输入：x/4wx $a1
    
    - **预期结果**：你应该能看到第一个 32 位值是 **0xedfe0dd0**。
        
    - 原理：设备树二进制文件的开头固定是 0xd00dfeed（大端序在内存里看起来就是 ed fe 0d d0）。

#### 2. 探究内核启动时
debug console 调试 用-exec前缀就可以和命令行一样了。
在 GDB 中继续输入：

1. 在内核起点打断点：b *0x80200000
2. 继续运行：c
3. 当程序停在 0x80200000 时：
    ![[Pasted image 20260118211355.png]]
    - 根据文档，OpenSBI 会把 **Next Arg1** 传给内核。在 RISC-V 规范中，第一个参数通常放在 a1 寄存器。
        
    - **查看 a1 寄存器**：执行 i r a1。这个值通常是 **DTB (Device Tree Blob)** 的物理地址，即设备树在内存中的位置。
        左侧日志：Domain0 Next Address : 0x0000000080200000
		右侧 GDB：你的 PC 正好停在 0x80200000。
		结论：OpenSBI 确实按照预期跳转到了内核起点。

		左侧日志：Domain0 Next Arg1 : 0x0000000087e00000
		右侧 GDB：执行 i r a1 得到的值正是 0x87e00000。
		结论：OpenSBI 成功将参数（Next Arg1）通过 a1 寄存器传递给了内核。
    - **查看该地址内容**：设备树验证 (DTB Magic Number)：
		右侧 GDB：执行 x/4wx $a1 看到第一个 32 位字是 0xedfe0dd0。
		原理：这是 Device Tree Blob (DTB) 的魔数 0xd00dfeed 在小端序机器上的内存表现。
		结论：这证明了 a1 指向的确实是设备树。内核会通过这个设备树了解当前机器有多少 CPU、多少内存以及外设的地址。

        

---

### 验收自测小结

- **问**：如何让 QEMU 运行到一半停下来等 GDB？
    
    - **答**：使用 make debug，它背后调用了 QEMU 的 -s -S 参数。
        
- **问**：Linux 内核的第一条指令存放在物理内存的什么位置？
    
    - **答**：0x80200000。
        
- **问**：OpenSBI 运行在什么特权级？内核运行在什么特权级？
    
    - **答**：OpenSBI 运行在 **M-Mode** (Machine)，内核运行在 **S-Mode** (Supervisor)。
        
- **问**：在 GDB 中，我想看当前函数的调用路径，该用什么命令？

    - **答**：bt 或 backtrace。


