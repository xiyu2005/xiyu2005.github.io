# 代码拉取

# Part1 启动工作

## 1.1RISCV汇编
```

```
![[Pasted image 20260120101217.png]]


RISC-V 整数寄存器的 ABI（应用二进制接口）约定表格
![[Pasted image 20260120101857.png]]

 问题 1：每个函数的开头都操作了 sp，是在干什么？
 开辟栈帧。
addi sp, sp, -32 是将栈指针向低地址移动，从而在内存中预留出一段空间。
目的：
1. **保存寄存器**：为了防止当前函数修改了调用者以后还要用的寄存器，需要把这些寄存器（如返回地址 ra、帧指针 s0 等）存入这段预留的栈空间。

2. **存储局部变量**：C 语言中的局部变量（如 main 中的 int r）如果无法完全放在寄存器里，就会存放在栈帧中。
3. **支持嵌套调用**：如果函数 A 调用了函数 B，A 必须在跳转前把自己的返回地址 ra 存在栈里，否则执行完 B 以后，ra 被覆盖，A 就找不到回家的路了。


问题 2：为什么 sp 的差值总是 16 的倍数？
这是为了遵守 RISC-V ABI 的栈对齐（Stack Alignment）规范。
RISC-V 的调用约定要求栈指针 sp 在进入任何过程时都必须保持 **16 字节对齐**。
- **目的**：
    1. **兼容性**：支持 RISC-V 的“Q”扩展（128 位浮点数指令）。如果栈不对齐到 16 字节，处理 128 位数据时可能会触发内存访问异常或降低性能。
    2. **性能优化**：现代 CPU 访问对齐的内存地址速度更快。
- 即使没用到 128 位数据：编译器依然会强制执行此规则，以确保不同开发者编写的代码库可以互相调用而不出错。


---

 考点 3：调用函数前后做了什么？
可以分为“调用者（Caller）”和“被调用者（Callee）”两个视角来看：
1. 调用函数前（Caller 的工作）：
- **传参**：将参数放入寄存器 a0-a7（如例子中的 li a0, 10）。如果参数超过 8 个，多余的压入栈中。
- **保存返回地址**：执行 call 指令，这会自动将下一条指令的地址存入 ra 寄存器。
- (可选)：如果 t0-t6 等调用者保存寄存器中有重要数据，需要先存入栈。
1. 函数开头（Callee 的序言 - Prologue）：
- **分配空间**：addi sp, sp, -X。
- **保存现场**：将 ra 和 s0 (fp) 等寄存器存入栈（sd ra, 24(sp)）。
- **更新帧指针**：addi s0, sp, X（方便通过固定偏移量访问局部变量）。

1. 函数执行后（Callee 的尾声 - Epilogue）：
- **设置返回值**：将结果放入 a0（如 mv a0, a5）。
- **恢复现场**：从栈里读回原来的 ra 和 s0（ld ra, 24(sp)）。
- **释放空间**：addi sp, sp, X。
- **返回**：执行 jr ra（跳转回 ra 指向的地址）。

### 额外补充：

在例子中：

- func 开头的 sd ra, 24(sp) 是为了保护 ra，因为即便 func 目前没调用别人，编译器通常也会生成标准的序言。
- main 中的 call func 是一条伪指令，它等价于 auipc + jalr，会将跳转位置后的指令地址存入 ra。



根据手册表格，这些伪指令对应的真实指令序列如下（假设为 64 位非 PIC 环境）：

| 伪指令               | 对应的真实指令                                              | 说明                                            |
| ----------------- | ---------------------------------------------------- | --------------------------------------------- |
| **la rd, symbol** | auipc rd, offset[31:12]<br>addi rd, rd, offset[11:0] | 加载符号地址。auipc 结合 addi 可以实现相对于当前 PC ±2GB 范围的寻址。 |
| **nop**           | addi x0, x0, 0                                       | 不执行任何操作，仅占用一个指令周期。                            |
| **li rd, imm**    | lui / addi / slli 等组合                                | 根据立即数的大小，汇编器会将其拆解为多条指令。                       |
| **mv rd, rs**     | addi rd, rs, 0                                       | 将寄存器 rs 的值加 0 后存入 rd，实现寄存器拷贝。                 |
| **j offset**      | jal x0, offset                                       | 无条件跳转。将 link 寄存器设为 x0 表示不保存返回地址。              |
| **ret**           | jalr x0, x1, 0                                       | 从子程序返回。跳转到 x1 (ra) 指向的地址，不保存 link。            |
| **call symbol**   | auipc x1, offset[31:12]<br>jalr x1, x1, offset[11:0] | 远程过程调用。将返回地址保存在 x1 (ra)。                      |
| **tail symbol**   | auipc x6, offset[31:12]<br>jalr x0, x6, offset[11:0] | 尾调用。不保存返回地址，直接跳转。                             |


call 与 tail 的区别与工作原理
1. call 伪指令做了什么？
- **功能**：用于调用一个远处的函数。
- **工作机制**：
    - 它由两条指令组成：首先用 auipc 计算目标地址的高 20 位，然后用 jalr 跳转到低 12 位。
    - **关键点**：它会将跳转指令下一条指令的地址（返回地址）保存到 **ra (x1)** 寄存器中。
- **用途**：当你期望函数执行完后能回到当前位置继续执行时，使用 call。

 2. tail 伪指令做了什么？
- **功能**：用于“尾调用优化”（Tail Call Optimization）。
- **工作机制**：
    - 同样通过 auipc 和 jalr 跳转，但它的 **link 寄存器是 x0**。
    - **关键点**：它**不保存**当前的返回地址。它会直接跳转到目标函数，并复用当前的 ra 寄存器值。
- **用途**：当一个函数的最后一步是调用另一个函数，且调用完后不需要再回到当前函数处理任何逻辑时，使用 tail。
核心区别：

| 特性       | call                    | tail                          |
| -------- | ----------------------- | ----------------------------- |
| **返回地址** | 保存到 ra                  | **不保存**（丢弃或复用旧的 ra）           |
| **控制流**  | 调用者 $\to$函数 $\to$ 回到调用者 | 调用者 $\to$函数 $\to$ 直接回到调用者的调用者 |
| **栈帧开销** | 会在调用链中增加一层              | 节省了一层函数返回的开销                  |

## 1.3arch/riscv/kernel/vmlinux.lds链接脚本与内存布局分析


```c
OUTPUT_ARCH("riscv")

ENTRY(_start)

PHY_START    = 0x80000000;
PHY_SIZE     = (128 * 1024 * 1024);
PHY_END      = (PHY_START + PHY_SIZE);
PGSIZE       = 0x1000;
OPENSBI_SIZE = (0x200000);

MEMORY {
    ram  (wxa!ri): ORIGIN = PHY_START + OPENSBI_SIZE, LENGTH = PHY_SIZE - OPENSBI_SIZE
}

BASE_ADDR = PHY_START + OPENSBI_SIZE;

SECTIONS
{
    . = BASE_ADDR;

    _skernel = .;

    .text : ALIGN(0x1000) {
        _stext = .;

        *(.text.init)
        *(.text.entry)
        *(.text .text.*)

        _etext = .;
    } AT>ram

    .rodata : ALIGN(0x1000) {
        _srodata = .;

        *(.rodata .rodata.*)

        _erodata = .;
    } AT>ram

    .data : ALIGN(0x1000) {
        _sdata = .;

        *(.data .data.*)
        *(.got .got.*)

        _edata = .;

        . = ALIGN(0x1000);
    } AT>ram

    .bss : ALIGN(0x1000) {
        *(.bss.stack)
        . = ALIGN(0x1000);
        _sbss = .;

        *(.sbss .sbss.*)
        *(.bss .bss.*)

        _ebss = .;
    } AT>ram

    . = ALIGN(0x1000);
    _ekernel = .;
}

```


#### 1.内核内存布局
*   **起始位置**：
    从脚本中的 `BASE_ADDR` 开始。
    计算公式：`BASE_ADDR = PHY_START + OPENSBI_SIZE = 0x80000000 + 0x200000 = 0x80200000`。
    所以，内核的内存布局起始于物理地址 **`0x80200000`**。
*   **大小**：
    内核的总大小由脚本中定义的两个符号决定：从 `_skernel` 到 `_ekernel`。
    在运行时，它占用的内存空间大小为：**`_ekernel - _skernel`**。
    *注：由于使用了 `ALIGN(0x1000)`，内核的总大小会是 4KB（页面大小）的整数倍。*

---

#### 2. 各个段（.text, .rodata, .data, .bss）存放什么数据？

*   **`.text` (代码段)**：
    存放编译后的**机器指令**。脚本中特意排列了 `*(.text.init)` 和 `*(.text.entry)`，确保初始化代码和中断入口代码排在最前面。
*   **`.rodata` (只读数据段)**：
    存放**常量数据**，例如 C 语言中的 `const` 变量、字符串常量（如 `printk("Hello")` 中的 "Hello"）。
*   **`.data` (数据段)**：
    存放**已初始化的全局变量和静态变量**（例如 `int a = 10;`）。还包括了 `.got`（全局偏移表），用于处理重定位。
*   **`.bss` (未初始化数据段)**：
    存放**未初始化的全局变量**（例如 `int a;`）。根据脚本，**内核栈（.bss.stack）**也存放在这里。

---

#### 3. `_skernel` 等符号是什么？如何使用？

这些符号是**地址标签**。它们本身不占用任何内存空间，只是链接器在合并各个段时，记录下的一个**位置标记**。
*   **在汇编中使用**：
    通常用 `la` (Load Address) 指令获取它们的地址：
    ```assembly
    la sp, boot_stack_top  # 加载栈顶符号的地址到栈指针寄存器
    ```
*   **在 C 代码中使用**：
    需要先声明为外部符号，然后**取其地址**使用：
    ```c
    extern char _skernel[]; // 声明为字符数组
    extern char _ekernel[];
    
    uint64_t kernel_size = _ekernel - _skernel; // 计算内核长度
    ```
    *注意：在 C 语言中，`_skernel` 的“值”就是那个地址，不需要解引用。*

---

#### 4. 栈空间在哪里定义？为什么选 `.bss`？

*   **定义位置**：
    在 `.bss` 节的最开始处：
    ```ld
    .bss : ALIGN(0x1000) {
        *(.bss.stack)  /* 这里就是定义栈空间的地方 */
        . = ALIGN(0x1000);
        _sbss = .;
        ...
    }
    ```
    这说明链接器会去所有目标文件中找名为 `.bss.stack` 的输入节并放在这里。在你的 `head.S` 中，应该能找到对应的 `.section .bss.stack` 定义。

*   **为什么选 `.bss` 段而不是 `.data` 段？**
    1.  **减小镜像大小**：`.data` 段的数据是需要保存到磁盘镜像（`Image`）里的。如果你在 `.data` 定义一个 16KB 的栈，`Image` 文件就会平白无故多出 16KB 的 0。
    2.  **按需分配**：`.bss` 段在 `Image` 镜像中**不占空间**。内核启动时，只需要知道 `.bss` 的起始和结束地址，由软件（或加载器）在内存里划出一块地方清零即可。栈初始状态不需要特定值，因此放在 `.bss` 最节省磁盘空间。

---



### Makefile构建
```cmake
# 先通过链接脚本生成 ELF 格式的 vmlinux
$(LD) -T arch/riscv/kernel/vmlinux.lds \
		arch/riscv/kernel/*.o \
		lib/*.o \
		-o vmlinux
		
	mkdir -p arch/riscv/boot
	
	# 将 vmlinux 转换为纯二进制的 Image
	$(OBJCOPY) -O binary vmlinux arch/riscv/boot/Image
```
根据 objcopy 官方文档，当使用 `-O binary` 生成原始二进制文件时，objcopy 会执行以下操作：
 1. 本质：生成内存数据 Dump。- 比如 vmlinux 中 `.text` 段（0x80200000 开始）、`.rodata` 段、`.data` 段、`.bss` 段（注：`.bss` 段本身无数据，会被填充为 0），会按地址顺序拼接成连续的二进制数据。
2. 丢弃所有「非执行 / 非数据」的元数据，符号表（比如 _skernel、_etext 等地址符号，仅用于调试 / 链接）；重定位信息（链接阶段已完成重定位，运行时无需）；ELF 段头 / 节头（描述段信息的元数据）；调试信息（-ggdb 生成的 GDB 调试数据）；其他辅助节（如 .comment、.note 等）。
3. 从「最低加载地址」开始 Dump。Image 的第一个字节，对应物理内存 0x80200000 地址的内容；Image 的后续字节，按内存地址递增顺序排列，直到内核最后一个段（.bss）的结束地址

make后
![[Pasted image 20260120113626.png]]


ElfPreview查看vmlinux
![[Pasted image 20260120114940.png]]
发现内核的入口地址为 0x80200000。这与链接脚本 vmlinux.lds 中 BASE_ADDR = 0x80200000 以及 OpenSBI 跳转的目标地址一致。
查看readelf -S vmlinux输出
![[Pasted image 20260120115817.png]]

.bss 段的类型为 NOBITS，且标志（Flags）包含 WA (Write, Allocate)。
NOBITS 说明该段在磁盘文件（vmlinux）中不占用实际存储空间，仅记录了大小和位置。
WA 说明该段在程序运行时需要被加载到内存，并且是可写的
这解释了为什么 Image 文件的大小远小于内核在内存中的实际占用空间。
####  关于 `Image` 文件大小的补充
![[Pasted image 20260120120301.png]]
如图所示，vmlinux 大小为 68,560 字节，而 Image 大小为 15,104 字节。
为什么 Image 变小了这么多。这需要结合之前 readelf 的结果来分析。
原因一：移除调试信息与符号表 (Strip)。vmlinux 包含了大量的辅助信息，用于调试和链接。
ELF 头与程序头：readelf -h 显示头部占用了空间。
调试段：readelf -S 显示了 .debug_info, .debug_line 等段，这些占据了大量空间。
符号表：.symtab 和 .strtab 也占用空间。
结论：objcopy -O binary（以及 Makefile 中的 -S 选项）剔除所有这些运行时不需要的“元数据”，只保留了机器码和数据。
原因二：.bss 段的处理 
在之前的 readelf -S 中，我们看到 .bss 段标记为 NOBITS，大小为 0x1008 (4KB多)。
在 vmlinux 的 ELF 结构中，.bss 仅仅是一个描述符，不占用文件偏移量。
在生成的 Image 二进制文件中，由于 .bss 存放的是未初始化的全局变量（以及本实验中的栈），其初始值默认为 0。
结论：Image 文件完全丢弃了 .bss 段。
OpenSBI 将 Image 加载到内存后，内核启动代码（或加载器）会负责根据记录的地址（_sbss 到 _ebss），在内存中划出一块区域并手动清零，重新“变”出 .bss 段。因此，这部分空间不需要存储在磁盘上的 Image 文件中。

$Image \approx .text + .rodata + .data +$ 对齐填充
根据之前的 readelf，.text 约 8KB (0x2064)，.rodata 约 1KB (0x4f6)，.data 为 0。
加上链接脚本中 ALIGN(0x1000) 带来的 4KB 页对齐填充（Section 之间的空隙）。
计算结果接近 15KB，与 Image 的 15,104 字节 相符。


## 1.4OpenSBI调试

### 第四步：完成“动手做”任务
依次输入
 make debug KERNEL_PATH=kernel
make gdb KERNEL_PATH=kernel

GDB 连接成功后，请依次执行以下操作来回答文档的问题：

#### 1. 查看 sp 寄存器

codeGdb

```
# 在内核入口打断点
b *0x80200000
# 继续运行
c
# 停住后，查看 sp
i r sp
```

- **记录下sp 0x80046eb0**
![[Pasted image 20260120132851.png]]
#### 2.特权级的权限
回到 **终端 1（QEMU）** 的输出，找到刚才打印的 Domain0 Region... 表。
-  sp 值落在Domain0 Region03            : 0x0000000080040000-0x000000008005ffff M: (R,W) S/U: ()
M (Machine Mode): 拥有读写 (Read, Write) 权限。OpenSBI 自己运行在 M 模式，所以它用这个栈没问题。
S/U (Supervisor/User Mode): 权限为空 ()。也就是说，S 模式和 U 模式既不能读也不能写这段内存。


这意味着
OpenSBI 在跳转到内核之前，打印了一行：
Domain0 Next Mode : S-mode
这就构成了矛盾：
OpenSBI 把 CPU 切到了 S 模式。
OpenSBI 把控制权交给了内核（PC = 0x80200000）。
但是，寄存器 sp 仍然指向 0x80046eb0（Region 03）。
后果：
如果你的内核第一条指令不去修改 sp，而是直接尝试使用栈（比如 sd ra, 0(sp)），CPU 的 PMP（物理内存保护）硬件检查机制会立刻发现：“当前是 S 模式，但你试图访问只有 M 模式才能访问的 Region 03”。
在 head.S 中，利用 la 和 mv 指令，立刻把 sp 移到我们自己在 .bss 段准备好的、S 模式有权访问的安全区域（Region07 覆盖的范围）。

#### 3. 栈的定义位置

文档让你去 vmlinux.lds 里找栈定义。

- 打开 kernel/arch/riscv/kernel/vmlinux.lds。
- 找到 .bss 段。
    ```c
        .bss : ALIGN(0x1000) {
        *(.bss.stack)
        . = ALIGN(0x1000);
        _sbss = .;

        *(.sbss .sbss.*)
        *(.bss .bss.*)

        _ebss = .;
    } AT>ram
    ```
- 看到 *(.bss.stack)。这说明栈被定义在 BSS 段中。
    - *(.bss.stack) 这行指令告诉链接器：去所有的输入目标文件（主要是 head.o）中寻找名为 .bss.stack 的段，并将它们放在最终输出文件的 .bss 段的起始位置。
    
- 这就意味着 skernel + .text大小 + .rodata大小 + .data大小 之后的地址，就是栈的底部（低地址）。boot_stack = .bss段起始地址 = 0x80204000

 **思考回答**：为什么在 .bss？
原因一：减小磁盘镜像（Image）的大小（最核心原因）
.data 段：存放的是已初始化的数据（例如 int a = 10;）。这些数据必须原封不动地保存在二进制镜像文件（Image）中，以便程序启动时读取。
如果把 4KB 的栈放在 .data 段，Image 文件就会实打实地增大 4KB（里面填充的全是 0 或垃圾值）。
.bss 段：存放的是未初始化的数据。它在镜像文件中标记为 NOBITS（不占位）。
如果把 4KB 的栈放在 .bss 段，Image 文件的大小完全不会增加。它只需要在文件头里记录一句：“这里需要 4KB 的内存，请在加载时预留出来”。
原因二：栈不需要“初始值”
栈（Stack）是用来当作“草稿纸”的，用于在函数调用时临时保存寄存器和局部变量。
程序刚启动时，我们并不关心栈里原本存的是什么（反正马上就会被 push 进来的数据覆盖）。
既然不需要特定的初始值，就没必要浪费磁盘空间去存储它，使用“运行时自动清零分配”的 .bss 段是最逻辑的选择。



## 1.5Task1
原来head.s为

```
#include "private_kdefs.h"

    .section .text.init
    .globl _start
_start:

    /* Lab1 Task1 */

    /* Lab1 Task3 */

    tail start_kernel

    .section .bss.stack
    .space PGSIZE

```
修改为
```
#include "private_kdefs.h"

    .section .text.init
    .globl _start
_start:

    /* Lab1 Task1 */
    /* 1. 加载栈顶地址到 sp 寄存器 */
    /* 此时 sp 指向我们自己在 .bss 段定义的堆栈顶部 */
    la sp, boot_stack_top

    /* Lab1 Task3 */
    /* (Task3 时再来填这里) */

    /* 2. 跳转到 C 语言入口 */
    tail start_kernel

    .section .bss.stack
    /* 3. 栈对齐：确保栈从 4KB (2^12) 边界开始，这是良好的习惯 */
    .align 12
    
    .globl boot_stack
boot_stack:
    /* 分配 4KB (PGSIZE) 的空间 */
    .space PGSIZE
    
    /* 4. 定义栈顶符号 */
    /* 因为栈向下增长，所以栈顶在 allocated space 的末尾 */
    .globl boot_stack_top
boot_stack_top:
```

```
# 1. 在 printk 打断点 (printk 是 C 语言函数，说明已经跳进去了)
b printk
# 2. 继续执行
c
# 3. 如果程序停在了 printk，说明栈设置成功了！
# (如果栈没设置好，程序会在 tail start_kernel 后立刻崩溃，永远到不了 printk)

# 4. 检查异常状态 (根据题目要求)
i r scause
```
![[Pasted image 20260120141815.png]]
可以从截图中解读出以下成功的关键证据：
1. 成功进入了 C 语言环境
证据：GDB 显示 Breakpoint 1, printk (...) at printk.c:14。
含义：代码流已经顺利执行了 head.S 中的 la sp, ... 和 tail start_kernel，并且从 start_kernel 函数中成功调用了 printk。这证明你的汇编代码逻辑是通的。
2. 没有发生异常 (Crash)
证据：scause = 0x0。
含义：如果你的栈指针设置错误（例如仍然指向 OpenSBI 的保护区），CPU 在执行压栈指令（如 sd）时会立即抛出异常，scause 会变成 0xd (Load Access Fault) 或 0xf (Store Access Fault)。现在是 0，说明栈访问合法。
3. 栈指针位置正确
证据：sp = 0x80204f80。
分析：
之前我们在 OpenSBI 看到旧的 sp 是 0x8004xxxx。
现在的 0x8020xxxx 正是我们链接脚本中定义的 .bss 段所在的区域（内核数据区）。
你看汇编窗口的第一行：addi sp, sp, -128。如果你定义的栈顶是 0x80205000 左右，减去 128 正好是 0x80204f80。这证明你成功切换到了自己的栈。



![[Pasted image 20260120142624.png]]
通过了评测。



### Task1总结
其实我是ai帮忙写的代码，也忘了好多指令集的知识，所以从头重新逐步调试看了一下
![[Pasted image 20260120150838.png]]
这个时候呢，是在_start断点，还未执行la sp, boot_stack_top.
\_start地址是0x80200000,是内核代码的入口地址，在之前的vmlinux.lds中`BASE_ADDR = PHY_START + OPENSBI_SIZE = 0x80000000 + 0x200000 = 0x80200000;`定义。
sp此刻为0x80046eb0，是OpenSBI留给内核的初始sp值，是M-mode，而tail start_kernel跳转c语言使用S-mode不能访问M-mode的sp。会发生什么呢？ai说会抛出 Load/Store Access Fault，但是我们来进行调试：
![[Pasted image 20260120152849.png]]
我们发现没有合法栈导致 C 函数的 “函数序言” 执行失败，CPU 在跳转指令和 C 函数入口之间来回退。但是为什么没显示Load/Store Access Fault？因为代码里完全没有配置异常向量表和 `stvec` 寄存器。这个来回回退是qemu的操作。但是异常是触发了的。

再回到刚刚修改好的head.s，我们做了la sp, boot_stack_top，在head.s
```
boot_stack: .space PGSIZE # 分配0x1000字节 boot_stack_top:
```
=0x80204000+0x1000=0x80205000
![[Pasted image 20260120155200.png]]

我们-exec ni后
![[Pasted image 20260120160456.png]]
sp指到了0x80205000.这就是c语言合法的sp值了。

## 1.6内联汇编

![[Pasted image 20260120164920.png]]


问题：**寄存器分配冲突**：你在汇编模板中使用了硬编码的寄存器名（a0-a3），但你同时告诉编译器输入操作数 [c] 和 [d] 可以使用“任意寄存器”（"r" 约束）。编译器并不知道你在汇编模板内部会修改 a2 或 a3，因此它完全有可能把 a3 分配给 [c]，把 a2 分配给 [d]。
![[68700077810711b7fba87398918216b1.jpg]]
修改：
```
#include <stdint.h>

long correct_function(long a, long b, long c, long d) {
    // 1. 使用局部寄存器变量显式绑定寄存器
    register long a0 asm("a0") = a;
    register long a1 asm("a1") = b;
    register long a2 asm("a2") = c;
    register long a3 asm("a3") = d;

    __asm__ volatile(
        "ecall"
        // 2. 将寄存器变量放入输入/输出列表
        // a0, a1 既是输入（传参）又是输出（返回值），使用 "+" 约束
        : "+r"(a0), "+r"(a1) 
        : "r"(a2), "r"(a3)
        : "memory"
    );

    return a0 + a1;
}
```

## 1.7SBI 和 ECALL

### ECALL
#### 1. ECALL 指令的作用是什么？
向执行环境（如 SBI 固件、调试器）发出服务请求，可用于系统调用、半主机模式、访问特权功能等场景。其功能与编码兼容旧名 `SCALL`，用途覆盖调用操作系统、调试器或其他执行环境服务。
#### 2. 对于我们实现的操作系统来说，服务请求的参数传递由谁定义？
由 **EEI（执行环境接口）** 定义（非特权级手册明确）；具体到本课程的 SBI 环境中，参数传递遵循 SBI 规范的二进制编码约定（即 SBI 手册 Chapter 3 定义的寄存器传递规则）。
### SBI
Chapter 1. Introduction 
#### 3. 什么是 SBI？它为谁提供服务？
- SBI（Supervisor Binary Interface， supervisor 二进制接口）：是定义在特权级软件（S-mode/VS-mode）与更高特权执行环境（SEE）之间的抽象接口；
- 服务对象：S-mode（ supervisor 模式）或 VS-mode（虚拟 supervisor 模式）软件（本课程中即我们实现的 ZJU-OS 内核）。

Chapter 3. Binary Encoding 考点
#### 4. 在本课程中，谁是 Supervisor？谁是 SEE？

- Supervisor：S-mode 运行的 **ZJU-OS 内核**（我们实现的操作系统）；
- SEE（Supervisor Execution Environment）：提供 SBI 接口的更高特权软件，本课程中是 **M-mode（机器模式）的 OpenSBI 固件**。

#### 5. 如何标识一个特定的 SBI 调用？
通过 **EID（扩展 ID）+ FID（功能 ID）** 组合唯一标识：
- EID（Extension ID）：存于 `a7` 寄存器，标识要调用的 SBI 扩展（如 Debug Console 扩展 EID 为 0x4442434E）；
- FID（Function ID）：存于 `a6` 寄存器（SBI v0.2 及以上），标识扩展内的具体功能（如 Debug Console 的写功能 FID 为 0）。

#### 6. SBI 调用的参数和返回值是如何传递的？

- 参数传递：通过 `a0~a5` 寄存器传递（最多支持 6 个参数）；
- 返回值传递：通过 `a0`（错误码）和 `a1`（功能返回值）传递，对应 SBI 规范定义的 `struct sbiret` 结构（`a0=error`，`a1=value/uvalue`）。

#### 7. SBI 调用时，哪些寄存器的值不会被保存？

仅 `a0` 和 `a1` 寄存器的值不保证保留（会被 SEE 修改以返回结果）；其他寄存器（`a2~a5`、`s0~s11` 等）必须被 SEE 保留（即调用后原值不变）。

#### 8. 如何判断 SBI 调用是否成功？

通过返回值 `a0`（`sbiret.error`）判断：

- 若 `a0 = SBI_SUCCESS`（值为 0），表示调用成功；
- 若 `a0` 为非 0 负数（如 `SBI_ERR_NOT_SUPPORTED=-2`、`SBI_ERR_INVALID_PARAM=-3`），表示调用失败，具体错误含义参考 SBI 规范的标准错误码表。


Chapter 12. Debug Console Extension

#### 9. Debug Console Extension 提供了什么功能？

替代 legacy 扩展（EID #0x01 控制台写、#0x02 控制台读），为 supervisor 模式软件提供 **调试控制台的字节读写功能**，支持单次读写多个字节，适用于内核启动阶段打印日志、调试交互等场景。

#### 10. sbi_debug_console_write 函数的参数和返回值分别是什么？

- **参数**（3 个，均通过寄存器传递）：
    1. `num_bytes`：要写入的字节数（`a0` 传递）；
    2. `base_addr_lo`：输入内存的物理地址低 XLEN 位（`a1` 传递）；
    3. `base_addr_hi`：输入内存的物理地址高 XLEN 位（`a2` 传递）；
    
- **返回值**（通过 `a0` 和 `a1` 传递）：
    1. `sbiret.error`（`a0`）：错误码（`SBI_SUCCESS=0` 表示无错误）；
    2. `sbiret.uvalue`（`a1`）：实际写入的字节数（非阻塞调用，可能部分写入或未写入）。



## 1.8Task2:使用 SBI 实现 `printk()`

为了完成 Lab 1 Task 2，你需要修改 `arch/riscv/kernel/sbi.c` 文件。

你需要做两件事：
1.  **实现 `sbi_ecall`**：使用 C 内联汇编，将参数放入指定的寄存器（a0-a7），执行 `ecall` 指令，并获取返回值（a0, a1）。
2.  **补全 `sbi_debug_console_*`**：根据 SBI 规范（DBCN 扩展），传入正确的 Extension ID (EID) 和 Function ID (FID)。

以下是修改后的完整代码逻辑：

### 1. 修改 `sbi_ecall` 函数

找到 `sbi_ecall` 函数，将其修改为如下内容。使用了 GCC 的 `register ... asm("reg")` 语法来强制指定变量对应的寄存器。

```c
struct sbiret sbi_ecall(uint64_t eid, uint64_t fid, uint64_t arg0,
			uint64_t arg1, uint64_t arg2, uint64_t arg3,
			uint64_t arg4, uint64_t arg5)
{
	struct sbiret ret;

	// 1. 将参数绑定到对应的寄存器
	// 根据 RISC-V SBI 规范：
	// a7: Extension ID (EID)
	// a6: Function ID (FID)
	// a0-a5: 参数 arg0-arg5
	register uint64_t a7 asm("a7") = eid;
	register uint64_t a6 asm("a6") = fid;
	register uint64_t a0 asm("a0") = arg0;
	register uint64_t a1 asm("a1") = arg1;
	register uint64_t a2 asm("a2") = arg2;
	register uint64_t a3 asm("a3") = arg3;
	register uint64_t a4 asm("a4") = arg4;
	register uint64_t a5 asm("a5") = arg5;

	// 2. 执行 ecall 指令
	// 输入操作数："r"(register_var) 表示将变量放入寄存器作为输入
	// 输出操作数："+r"(a0), "+r"(a1) 表示 a0 和 a1 既是输入也是输出
	// Memory Clobber: "memory" 告诉编译器汇编代码可能会修改内存，防止指令重排
	asm volatile(
		"ecall"
		: "+r"(a0), "+r"(a1)
		: "r"(a2), "r"(a3), "r"(a4), "r"(a5), "r"(a6), "r"(a7)
		: "memory");

	// 3. 获取返回值
	// SBI 规范规定：a0 返回 error code, a1 返回 value
	ret.error = a0;
	ret.value = a1;

	return ret;
}
```

### 2. 补全 Debug Console 相关函数
根据代码顶部的宏定义和 SBI 规范：
*   **EID**: `SBI_EXT_DEBUG_CONSOLE`
*   **FID**: `SBI_DBCN_WRITE` (0), `SBI_DBCN_READ` (1), `SBI_DBCN_WRITE_BYTE` (2)

修改对应的三个函数如下：

```c
struct sbiret sbi_debug_console_write(unsigned long num_bytes,
				      unsigned long base_addr_lo,
				      unsigned long base_addr_hi)
{
	// EID = SBI_EXT_DEBUG_CONSOLE, FID = SBI_DBCN_WRITE
	// arg0 = num_bytes, arg1 = base_addr_lo, arg2 = base_addr_hi
	return sbi_ecall(SBI_EXT_DEBUG_CONSOLE, SBI_DBCN_WRITE, num_bytes,
			 base_addr_lo, base_addr_hi, 0, 0, 0);
}

struct sbiret sbi_debug_console_read(unsigned long num_bytes,
				     unsigned long base_addr_lo,
				     unsigned long base_addr_hi)
{
	// EID = SBI_EXT_DEBUG_CONSOLE, FID = SBI_DBCN_READ
	return sbi_ecall(SBI_EXT_DEBUG_CONSOLE, SBI_DBCN_READ, num_bytes,
			 base_addr_lo, base_addr_hi, 0, 0, 0);
}

struct sbiret sbi_debug_console_write_byte(uint8_t byte)
{
	// EID = SBI_EXT_DEBUG_CONSOLE, FID = SBI_DBCN_WRITE_BYTE
	// arg0 = byte
	return sbi_ecall(SBI_EXT_DEBUG_CONSOLE, SBI_DBCN_WRITE_BYTE, byte, 0, 0,
			 0, 0, 0);
}
```

---

### 验证结果


![[Pasted image 20260120185908.png]]

### Task2调试回顾
在sbi_call函数打断点，si到asm volatile处，此时a7的值为0x4442434e这是 ASCII 码的 "DBCN")。这证明 register uint64_t a7 asm("a7") = eid; 生效了。
![[Pasted image 20260120192249.png]]

查看a6=0,a0,a1,a2分别代表a0为要打印的字节数0x14， a1: 字符串的低位地址0x80203000。a2: 字符串的高位地址0x0。
-exec x/s $a1查看a1指向的内容为"Hello, ZJU OS 2025!\n"
![[Pasted image 20260120192538.png]]

此时继续si，此时CPU 暂停了内核，跳到了 OpenSBI（M 模式），把字符打印到屏幕上，然后又跳回了下一行代码。
![[Pasted image 20260120193010.png]]
- a0为 0 (SBI_SUCCESS)。a1是实际写入的字节数。
- **理解**：这对应了代码里的 ret.error = a0; ret.value = a1;（1.7 Q6）。

然后看一下pc，pc理论上在执行ecall后会从0x8020...跳到0x8000..，但是gdb没有显示可能是因为略过了？
![[Pasted image 20260120202229.png]]
但是查看mepc的保存值和mcause=9是可以确认内核发起的 ecall 触发的陷入。

![[Pasted image 20260120202627.png]]


# Part2：时钟中断及其处理
### 2.1、特权级、Exception、Interrupt、Trap 考点解答

#### 1. 特权级是用来干什么的？
特权级（Privilege Levels）的核心作用是**为软件栈的不同组件提供权限隔离与保护**：
- 区分应用程序、操作系统、底层固件等不同软件的访问权限（比如硬件资源、内存、特殊指令 / CSR 寄存器）；
- 防止低特权级代码（如应用程序）越权操作高特权级资源（如硬件寄存器），降低错误 / 恶意代码对整个系统的破坏风险；
- 实现 “分层执行”，不同特权级对应不同软件层级的执行环境。

#### 2. 执行当前特权级不允许的操作会发生什么？
会**触发异常（exception）**，该异常通常会导致**陷阱（trap）** —— 即控制流转移到更高特权级的底层执行环境（如 M-mode 的 OpenSBI、S-mode 的操作系统陷阱处理程序），由高特权级代码处理该越权行为（比如报错、终止程序、模拟执行等）。
#### 3. M、U、S 模式分别是为了什么设计的？

| 模式                | 编码  | 设计目的                          | 核心特征                                                                                  |
| ----------------- | --- | ----------------------------- | ------------------------------------------------------------------------------------- |
| M（Machine，机器态）    | 11  | 为**底层固件 / 硬件管理**设计（如 OpenSBI） | ① 最高特权级，唯一必选的特权级；② 可无限制访问所有硬件资源、CSR 寄存器；③ 代码天生受信任，用于管理安全执行环境                          |
| S（Supervisor，监管态） | 10  | 为**类 Unix 操作系统内核**设计          | ① 隔离操作系统与应用程序；② 可执行操作系统所需的特权指令（如内存管理、中断处理）；③ 需通过 M-mode 授权访问部分硬件资源                    |
| U（User，用户态）       | 00  | 为**普通应用程序**设计                 | ① 最低特权级，限制访问硬件 / 内核资源；② 保护系统免受应用程序的错误 / 恶意操作影响；③ 需通过系统调用（如 ecall）陷入 S/M-mode 才能访问特权资源 |

#### Exception、Interrupt、Trap 考点解答
#### 1. RISC-V 中 exception、interrupt 有何异同？
##### 相同点：
- 都会导致 RISC-V 硬件线程（hart）发生**意外的控制流转移**；
- 最终都会触发 **trap（陷阱）**，使控制流转向陷阱处理程序。
##### 不同点：

| 维度  | Exception（异常）                | Interrupt（中断）                            |
| --- | ---------------------------- | ---------------------------------------- |
| 触发源 | 运行时与**当前指令相关**的 “异常条件”（同步）   | 外部**异步事件**（与当前执行的指令无关）                   |
| 例子  | 执行特权指令（如 ecall）、访问无权限内存、算术溢出 | 定时器中断、外设 IO 中断（如 UART / 网卡）、软件触发的 IPI 中断 |
| 时序  | 与指令执行同步（指令执行时立即触发）           | 异步（可在任意指令间隙触发）                           |
（这一段其实也可以结合专业课学过的微机理解了）
#### 2. Trap 是什么意思？举两个 Trap 的例子
##### Trap（陷阱）的定义：
指**因 exception（异常）或 interrupt（中断）导致的控制流转移**—— 即 hart 停止执行当前代码，转而跳转到 “陷阱处理程序（trap handler）” 执行的过程。
##### Trap 的典型例子：
1. **系统调用触发的 Trap**：应用程序（U-mode）执行 `ecall` 指令发起 SBI / 系统调用（属于 exception），触发 Trap 到 S/M-mode 的陷阱处理程序（如 OpenSBI 的 SBI 调用处理逻辑）；
2. **定时器中断触发的 Trap**：外设定时器产生异步中断（interrupt），触发 Trap 到 S/M-mode 的中断处理程序（如操作系统的定时器中断处理逻辑）；
3. **越权访问触发的 Trap**：U-mode 程序访问 S-mode 专属内存（属于 exception），触发 Trap 到 S-mode 的异常处理程序（如操作系统的内存保护处理）。


## 2.2 CSR寄存器
Chapter 2. Control and Status Registers (CSRs) 的章节导言
- **读取、修改、写入 CSR 的指令定义在哪个扩展？**
    定义在 **Zicsr** 扩展中。
- **S 模式的 CSR 能被 M 模式访问吗？反之呢？**
    - S 模式的 CSR **能被 M 模式访问**。因为 RISC-V 特权架构规定，与某一特权级关联的 CSR 可以被**所有更高特权级**访问，M 模式特权高于 S 模式。
    - M 模式的 CSR **不能被 S 模式访问**。S 模式特权低于 M 模式，不具备访问更高特权级 CSR 的权限。
3.1.6.1. Privilege and Global Interrupt-Enable Stack in mstatus register
- **mstatus 寄存器的作用是什么？**
    `mstatus` 是 RISC-V 核心的**控制与状态寄存器**，核心作用是**反映和控制 CPU 当前的特权状态、全局中断使能状态**，并通过内置的两级中断使能位（`xPIE`）和特权模式堆栈（`xPP`），**支持嵌套陷阱的处理**，保障中断处理程序的原子性和上下文恢复的正确性。
    
- **xIE bit 的作用是什么？**
    `xIE`（如 `MIE` 对应 M 模式、`SIE` 对应 S 模式）是特权模式 `x` 的**全局中断使能位**，作用如下：
    - 当 hart 在特权模式 `x` 下执行时，`xIE=1` 表示该模式的中断全局启用，`xIE=0` 表示该模式的中断全局禁用。
    - 对于**更低特权模式** `w < x`，无论 `wIE` 取值如何，该模式中断始终全局禁用；对于**更高特权模式** `y > x`，无论 `yIE` 取值如何，该模式中断始终全局启用。
    
- **运行在 S 模式且 mstatus.SIE=0，mstatus.MIE=0 时，发生中断会进入哪个模式？**
    会进入 **M 模式**。
    
    原因：中断的处理规则是**陷入到更高的特权级**，S 模式的更高特权级是 M 模式；且更高特权级的中断使能状态（`MIE`）不影响更低特权级中断的处理路径，无论 `MIE` 是否为 0，S 模式的中断都会触发 M 模式的陷阱处理。
    
- **从特权级 y 陷入到更高的特权级 x 时，xPIE、xIE 和 xPP 会如何变化？**
    陷入发生时，三个字段的变化规则如下：
    
    - `xPIE`：被设置为**陷入前 `xIE` 的值**（保存原中断使能状态）。
    - `xIE`：被设置为 **0**（进入陷阱后全局禁用当前特权级中断，保障处理程序原子性）。
    - `xPP`：被设置为 **陷入前的特权级 y**（保存原特权级上下文）。
    
- **xRET 指令返回时，特权级和中断使能位会如何恢复？xPP 会设置为什么？**
    执行 `xRET`（如 `mret`/`sret`）指令返回时，恢复与重置规则如下：
    
    - 特权级：切换为 `xPP` 字段保存的原特权级 `y`。
    - 中断使能位：`xIE` 被恢复为 `xPIE` 中保存的陷入前的值。
    - 其他字段：`xPIE` 被设置为 **1**；`xPP` 被设置为**系统支持的最低特权级**（有 U 模式则为 U，否则为 M）；若返回的特权级 `y ≠ M`，`MPRV` 位会被清零。
3.1.9. Machine Interrupt (mip and mie) Registers
- **mip 和 mie 寄存器的作用分别是什么？**
    - **`mip`（机器中断挂起寄存器）**：核心作用是**记录当前处于待处理状态的中断**，是一个 MXLEN 位的寄存器。每一位对应一个中断源，某一位被置 1 表示对应的中断已经发生且等待处理。其中部分位为只读（如机器外部中断 `MEIP`、机器定时器中断 `MTIP`），由硬件或平台控制器设置 / 清除；部分位可写（如管理级软件中断 `SSIP`），支持软件主动触发中断。
    - **`mie`（机器中断使能寄存器）**：核心作用是**控制各个中断源的使能开关**，是与 `mip` 位布局完全对应的 MXLEN 位寄存器。某一位被置 1 表示对应的中断被允许触发，置 0 则表示该中断被屏蔽。只有 `mie` 中对应位为 1，且 `mip` 中对应位为 1 时，中断才有可能被响应。
    
- **在什么条件下，中断会陷入 M 模式？**
    只有同时满足以下 **3 个条件**时，中断 `i` 才会触发 M 模式陷阱：
    (a) 当前特权模式为 M 且 `mstatus.MIE=1`（M 模式全局中断使能），**或者** 当前特权模式的等级低于 M 模式（如 S/U 模式）；
    (b) `mip` 寄存器的第 `i` 位（中断 `i` 待处理）和 `mie` 寄存器的第 `i` 位（中断 `i` 已使能）**同时被置 1**；
    (c) 如果 `mideleg`（机器中断委托寄存器）存在，其第 `i` 位**未被置 1**（即该中断没有被委托给更低特权级处理）。
    
- **为什么软件中断的优先级高于定时器中断？**
    主要有两个核心原因：
    - **功能优先级差异**：软件中断（如 MSI/SSI）主要用于**处理器间通信**，这类通信通常是高优先级的同步任务（如核间信号传递、任务调度指令）；而定时器中断（如 MTI/STI）一般用于**时间片轮转、定时计数**等场景，对响应的实时精度要求相对较低。
    - **硬件操作便利性**：软件中断对应的位位于 `mip` 寄存器的**最低 4 位**，可以直接使用带 5 位立即数的 CSR 指令（如 `csrrs`/`csrrc`）进行快速的读 - 修改 - 写操作，无需额外指令辅助，硬件实现和软件调用的效率更高。

3.1.7. Machine Trap-Vector Base-Address (mtvec) Register
- **mtvec 寄存器的作用是什么？**
    `mtvec`（机器陷阱向量基地址寄存器）的核心作用是**配置机器模式下陷阱的向量地址和处理模式**，直接决定陷阱发生时 CPU 程序计数器（`PC`）的跳转目标。
    它包含两个关键字段：
    - **BASE 字段**：存储陷阱向量的基地址，该地址必须按 4 字节边界对齐。
    - **MODE 字段**：定义陷阱的处理模式，分为 `Direct`（直接模式，值为 0）和 `Vectored`（向量模式，值为 1）两种，≥2 的值为保留。
    
- **为什么这个寄存器的低两位可以分配给 MODE 字段？**
    核心原因是 **BASE 字段要求 4 字节对齐**。
    4 字节对齐的地址其低两位二进制值必然是 `00`，这两位对 BASE 的地址定位没有任何意义。因此，RISC-V 架构直接复用这两个闲置的 bit 作为 `MODE` 字段，用于标识陷阱处理模式。这种设计既节省了寄存器空间，又不会影响 BASE 地址的有效性。
    补充：当 `mtvec` 用作地址时，低两位会被填充为 0，保证 BASE 地址的 4 字节对齐属性。
    
- **向量中断模式下，发生中断后 PC 会被设置成多少？**
    向量中断模式对应 `MODE=1`，此时 **同步异常** 和 **异步中断** 的 PC 设置规则不同：
    - **同步异常**：无论异常原因是什么，`PC` 都会被设置为 `mtvec.BASE` 的值（所有同步异常共用同一个处理入口）。
    - **异步中断**：`PC` 会被设置为 **`BASE + 4 × 中断原因值`**。
        举例：若机器定时器中断的原因值对应数值为 7，则跳转地址为 `BASE + 4×7 = BASE + 0x1C`。
3.1.8. Machine Trap Delegation (medeleg and mideleg) Registers
- **为什么需要委派机制？**
    核心目的是 **提升系统性能** 并 **实现特权级分层处理**。
    - 性能层面：默认所有特权级的陷阱都由 M 模式处理，会导致大量的 M 模式与低特权级（S/U）的上下文切换开销。通过委派机制，将 S/U 模式下的部分异常和中断直接交给 S 模式处理，减少 M 模式的介入次数，降低切换成本。
    - 分层层面：符合操作系统 “特权级隔离” 的设计思想，让 S 模式内核可以自主管理自身的异常与中断，无需完全依赖 M 模式固件（如 OpenSBI），提升系统的模块化和独立性。
    
- **medeleg 和 mideleg 寄存器的作用分别是什么？**
    两者都是 M 模式用于配置**陷阱委派规则**的读 / 写寄存器，仅在支持 S 模式的 hart 中存在：
    - **`medeleg`（机器异常委派寄存器）**：负责**同步异常**的委派控制。每一位对应一个同步异常（位索引等于该异常在 `mcause` 中的值），置 1 表示将 S/U 模式下发生的对应同步异常，委派给 S 模式陷阱处理程序处理。
    - **`mideleg`（机器中断委派寄存器）**：负责**异步中断**的委派控制。位布局与 `mip` 寄存器完全匹配，置 1 表示将 S/U 模式下发生的对应中断，委派给 S 模式陷阱处理程序处理。
    
- **当一个 trap 被委派到 S 模式后，指定寄存器 / 字段的值会如何变化？**
    根据 RISC-V 规范，委派后仅更新 **S 模式相关的状态寄存器**，M 模式相关寄存器不会被修改，具体变化如下：
 
寄存器 / 字段	变化规则
scause	写入当前陷阱的原因（对应异常或中断的编号）
stval	写入与该异常相关的特定数据（如非法指令异常时存储指令内容）
sepc	写入触发陷阱的指令的虚拟地址
mstatus.SPP	写入陷阱发生时的有效特权级（如 S 模式或 U 模式）
mstatus.SPIE	写入陷阱发生时 mstatus.SIE 字段的原始值（保存中断使能状态）
mstatus.SIE	被清零（进入 S 模式陷阱处理时，全局禁用 S 模式中断，保障处理原子性）
    
- **如果一个 trap 是在 M 模式下发生的，但它在 medeleg 中已被设置委派给 S 模式，会在哪里处理？**
    会在 **M 模式下处理**，不会被委派到 S 模式。
    原因是 RISC-V 规范明确规定：**陷阱不会从更高特权级转移到更低特权级**。委派规则仅对 **S/U 模式下发生的陷阱** 生效，M 模式自身发生的陷阱，无论 `medeleg` 是否配置，都由 M 模式自行处理。
    
- **mideleg 中的某一位被设置后，这个中断在 M 模式下会被触发吗？**
    **不会被触发**。
    规范指出，**被委派的中断会在委派者特权级（M 模式）被屏蔽**。例如，若将管理定时器中断（STI）通过 `mideleg[5]` 委派给 S 模式，那么当 CPU 运行在 M 模式时，该中断不会被触发；只有当 CPU 运行在 S/U 模式时，该中断才会触发并由 S 模式处理。

3.1.14. Machine Exception Program Counter (mepc) Register 和 3.1.15. Machine Cause (mcause) Register 和 3.1.16. Machine Trap Value (mtval) Register

1. **mepc、mcause、mtval 寄存器的作用分别是什么？**
    这三个寄存器是 RISC-V M 模式**陷阱处理的核心状态寄存器**，在陷阱进入 M 模式时由硬件自动更新，用于记录陷阱的关键上下文，辅助软件完成处理和恢复。
    - **`mepc`（机器异常程序计数器寄存器）**
        核心作用是 **保存陷阱发生时被中断 / 触发异常的指令的虚拟地址**，是陷阱返回时恢复程序执行的关键。
        额外特性：低 1 位固定为 0；若仅支持 32 位指令对齐（`IALIGN=32`），低 2 位固定为 0；它是 WARL 寄存器，只需能存储有效虚拟地址，无需支持所有无效地址。
        只有陷阱进入 M 模式时硬件会自动写入，其他场景需软件显式修改。
    - **`mcause`（机器原因寄存器）**
        核心作用是 **标识触发陷阱的具体类型和原因**。
        包含两个关键部分：
        1. **Interrupt 位**：最高位，值为 `1` 表示陷阱由**中断**触发，值为 `0` 表示由**同步异常**触发；
        2. **Exception Code 字段**：剩余低位，存储具体的原因编号（如非法指令对应 `2`、M 模式环境调用对应 `11`、机器定时器中断对应 `7`）。
            同样仅在陷阱进入 M 模式时硬件自动写入，软件可显式修改。
        
    - **`mtval`（机器陷阱值寄存器）**
        核心作用是 **提供陷阱相关的额外上下文信息**，辅助软件定位和处理陷阱，具体存储内容与异常类型强相关。
        典型场景：
        - 地址不对齐、访问故障、页故障等异常：存储**错误的虚拟地址**；
        - 非法指令异常：可选存储**故障指令的二进制内容**；
        - 断点异常：可选存储断点指令的虚拟地址或 0；
            硬件平台会规定哪些异常必须填充有效信息，哪些可设为 0，若平台不支持该功能则 `mtval` 为只读 0。
        
    
1. **mcause 寄存器中，中断和异常的区别是什么？**
    两者的核心区别通过 `mcause` 的 **Interrupt 位**和**触发机制**划分，具体差异如下：

特性：	中断（Interrupt 位 = 1）	异常（Interrupt 位 = 0）
触发时机：	异步触发，与当前执行的指令无关（如定时器到期、外部设备请求）	同步触发，由当前执行的指令直接引发（如非法指令、地址不对齐）
原因类型：	属于外部 / 硬件事件（如软件中断、定时器中断、外部中断）	属于指令执行错误或特殊请求（如环境调用、断点、页故障）
Exception Code 范围：	对应表 17 中 Interrupt=1 的编号（如机器软件中断 3、机器定时器中断 7）	对应表 17 中 Interrupt=0 的编号（如非法指令 2、环境调用 8/9/11）
处理优先级：	由硬件预设固定优先级（如外部中断 > 软件中断 > 定时器中断）	同步异常有明确的优先级排序（如指令地址断点 > 页故障 > 地址不对齐）



动手做
断点打在内核第一条指令处，使用 QEMU Monitor 查看此时 CSR 寄存器的状态。解释本节学习的所有 M、S 模式 CSR 寄存器的值的含义。你会发现有些 S 模式寄存器没有在 QEMU 中展示，这并不是一个 Bug，请查看 RISC-V sstatus register is missing in qemu console / gdb (#1260) · Issue · qemu-project/qemu 了解原因。
![[Pasted image 20260121112655.png]]
1. 基础运行状态 (PC & GPR)
*   **`pc` (Program Counter): `0x0000000080200000`**
    *   **含义**：当前执行的指令地址。
    *   **解读**：这正是 `vmlinux.lds` 定义的内核入口地址。说明 OpenSBI 成功完成了跳转，现在控制权在内核手中。
*   **`x10/a0`: `0`**
    *   **含义**：Hart ID (Hardware Thread ID)。
    *   **解读**：根据 RISC-V 启动协议，`a0` 寄存器存放核心编号。`0` 表示这是 0 号核心。
*   **`x11/a1`: `0x0000000087e00000`**
    *   **含义**：Device Tree Blob (DTB) 地址。
    *   **解读**：这是 Task 1 验证过的，OpenSBI 将设备树的地址放在了 `a1` 传给内核。
*   **`x2/sp`: `0x0000000080046eb0` **
    *   **含义**：栈指针。
    *   **解读**：这个地址位于 `0x8004xxxx` 区间。我们之前分析过，这是 OpenSBI 内部受 PMP 保护的内存区域。
    *   **结论**：**内核现在的栈是不安全的！** 这验证了 Task 1 必须立刻修改 `sp` 指向 `.bss` 段的必要性。


1. M 模式 CSR (遗留现场与权限移交)
这些寄存器展示了 OpenSBI (M-Mode) 是如何配置环境并把权力移交给内核 (S-Mode) 的。
*   **`mepc`: `0x0000000080200000`**
    *   **含义**：Machine Exception PC。
    *   **解读**：这是 OpenSBI 执行 `mret` 时跳转的目标地址。它被设置成了内核入口，证明了跳转路径。
*   **`mtvec`: `00000000800004f8`**
    *   **含义**：M 模式的异常入口基址。
    *   **解读**：如果系统发生严重错误（如物理硬件故障），CPU 会跳回到 `0x800004f8`，让 OpenSBI 来处理。
*   **`medeleg`: `0000000000f4b509` **
    *   **含义**：Machine Exception Delegation (异常委派)。
    *   **二进制解析**：`... 1111 0100 1011 0101 0000 1001`
    *   **关键位**：
        *   Bit 8 (Environment call from S-mode): **0** (注意：这里是0，意味着 S 模式的 ecall 默认是陷入 M 模式的，这解释了为什么 Task 2 中 `sbi_ecall` 会跳进 OpenSBI)。
        *   Bit 12, 13, 15: **Page Faults**。OpenSBI 把缺页异常委派给了 S 模式（内核），这样内核才能实现虚拟内存管理。

*   **`mideleg`: `0000000000001666` **
    *   **含义**：Machine Interrupt Delegation (中断委派)。
    *   **二进制解析**：`... 0001 0110 0110 0110`
    *   **关键位**：
        *   Bit 1 (**SSIP**): S 模式软件中断 -> 委派给内核。
        *   Bit 5 (**STIP**): S 模式时钟中断 -> 委派给内核。
        *   Bit 9 (**SEIP**): S 模式外部中断 -> 委派给内核。
    *   **结论**：OpenSBI 已经把中断处理的权力下放给了操作系统。

*   **`mip`: `0000000000000020`**
    *   **含义**：Machine Interrupt Pending。
    *   **解读**：`0x20` 即二进制 `0010 0000`，第 5 位置 1。
    *   **STIP (Supervisor Timer Interrupt Pending)**：说明此时此刻，已经有一个 **时钟中断** 在排队等待内核处理了(只是内核还没开中断 `sie`，所以没触发)。

---
 3. S 模式 CSR (内核当前状态)
*   **`stvec`: `0000000080200000`**
    *   **含义**：S 模式异常入口。
    *   **解读**：目前它指向内核入口。这是一个初始状态（或者未定义状态）。在 Task 3 中，你需要把它修改为 `_traps` 的地址，否则一旦发生异常，CPU 又跳回开头重新启动，造成死循环。
*   **`scause`, `sepc`, `stval`: `0`**
    *   **含义**：S 模式的异常原因、现场地址、附加值。
    *   **解读**：全为 0，说明 S 模式下还没有发生过任何异常。一切都很干净。
*   **`sstatus` (未直接显示，但隐藏在 mstatus 中)**
    *   **`mstatus`: `8000000a00006080`**
    *   其中 Bit 8 (**SPP**) 决定了上一级特权级。
    *   其中 Bit 5 (**SPIE**) 和 Bit 1 (**SIE**) 决定了 S 模式的中断状态。目前看 `...80` (Bit 7 MPIE=1)，说明 M 模式中断是开过的。而 S 模式的中断通常在内核初始化代码中才会手动开启。
 总结 
这张快照展示了内核启动最原初的状态：
1.  **控制权交接完成**：`pc` 和 `mepc` 均指向内核入口 `0x80200000`。
2.  **环境初始化就绪**：`medeleg` 和 `mideleg` 显示 OpenSBI 已经将页表异常、时钟中断等关键事件的处理权委派给了 S 模式。
3.  **栈处于危险状态**：`sp` 仍指向 OpenSBI 的保护区，必须立即切换。
4.  **中断状态**：`mip` 显示有一个时钟中断挂起，等待内核在 Task 4 中开启中断 (`sie`) 后进行处理。


移除你在 Task1 做的工作，然后：

- 在 `_start()` 打断点，然后单步调试，进入 `start_kernel()` 后程序能顺利跳转到 `printk()` 吗？如果不顺利，检查合适的 CSR 寄存器，看看发生了什么异常？
![[Pasted image 20260121120429.png]]
- 删掉在 `_start()` 打的断点，在 `printk()` 入口处打断点，然后继续运行（continue），你会发现最终能够到达 `printk()` 停下来，这是为什么？
![[Pasted image 20260121120558.png]]

这是为什么？（核心考点）
这是一个由“未初始化的异常向量表”导致的“无限重启死循环”。逻辑链条如下：
内核启动，sp 是坏的。
进入 start_kernel。注意：调用函数本身（jal）不需要用栈，只有保存寄存器时才用。
编译器生成的代码可能是：先准备参数 a0 (字符串地址)，然后 call printk。此时还没用到 sp，或者崩溃点在 printk 内部。
程序流执行到了 printk 入口 -> 触发 GDB 断点（你看到了这一幕）。
如果你输入 c 继续运行：printk 内部试图压栈 -> 触发 Store Access Fault (异常 7)。
CPU 发生异常，需要跳转到异常处理入口（由 stvec 寄存器决定）。
![[Pasted image 20260121120713.png]]
关键点：此时还没做 Task 3，stvec 的值通常默认为 0x80200000（内核入口）或者 0。
如果是 0x80200000：CPU 跳回 \_start -> 重新执行 start_kernel -> 重新调用 printk -> 再次触发断点。
结论：看到的“能到达”，其实是内核在“崩溃 -> 重启 -> 崩溃 -> 重启”的死循环中，每次重启都刚好路过这里。

### 2.3 特权指令
#### xRET 指令的核心作用（考点 1）
xRET 是 **MRET（Machine 模式陷阱返回）** 和 **SRET（Supervisor 模式陷阱返回）** 的统称，是 RISC-V 特权架构中专门用于**从陷阱（Trap）处理程序返回** 的特权指令，核心作用可拆解为 3 点：
1. **上下文恢复**：从陷阱处理程序退出，恢复陷阱触发前处理器的执行上下文（中断使能状态、特权级等）；
2. **特权级切换**：将处理器特权级切回「陷阱触发前的原始特权级」（比如从 S-mode 陷阱处理程序切回 U-mode 应用程序，或从 M-mode 切回 S-mode）；
3. **指令流恢复**：让程序从触发陷阱的指令位置继续执行，完成 “陷阱处理→正常执行” 的闭环。
#### 补充细节：
- MRET 是**必选指令**（所有 RISC-V 实现都必须支持），对应 M-mode 陷阱返回；
- SRET 仅当处理器支持 S-mode 时提供，若不支持 S-mode 却执行 SRET，会触发**非法指令异常**；
- 执行权限限制：xRET 只能在「x 特权级或更高特权级」执行（比如 SRET 可在 S/M-mode 执行），若在低于 x 的特权级执行（如 U-mode 执行 SRET），会触发非法指令异常；
- 特殊限制：若 mstatus 寄存器的 TSR 位 = 1 时执行 SRET，也会触发非法指令异常。
#### xRET 执行后 CSR 寄存器 & PC 的变化w
#### 1. CSR 寄存器的变化
xRET 核心操作 `xstatus` 类 CSR 寄存器（MRET 对应 `mstatus`，SRET 对应 `sstatus`），具体变化：
- **特权模式栈恢复**：xRET 会「弹出」`xstatus` 寄存器中保存的「低特权级特权模式栈」（privilege mode stack），恢复陷阱触发前的**特权级标记**（如 SRET 恢复 `sstatus.SPP` 位，标记返回后的特权级）；
- **中断使能恢复**：同时恢复 `xstatus` 中保存的「低特权级中断使能位」（如 SRET 恢复 `sstatus.SIE` 位，恢复 S-mode 中断使能状态）；
- 其他：若处理器支持 A 扩展，xRET 可（非强制）清除未完成的 LR 地址预留（陷阱处理程序也可通过 dummy SC 指令显式清除）。
#### 2. PC 程序计数器的变化
xRET 执行后，**PC 会被直接设置为 `xepc` 寄存器（MRET 对应 `mepc`，SRET 对应 `sepc`）中存储的值**：
- `xepc` 寄存器的核心作用是「记录触发陷阱的指令地址」（比如你调试 SBI 调用时，`sepc` 保存的是 `ecall` 指令的地址）；
- 因此 xRET 执行后，PC 会跳回「触发陷阱的那条指令的地址」，程序从陷阱触发的位置继续执行（完成 “陷阱处理→回到原执行流” 的逻辑）。

### 2.4Zicsr扩展
- 掌握四个标准 CSR 指令的用法：
    - RW: Read/Write
    - RS: Read and Set bits
    - RC: Read and Clear bits
    - RWI/RSI/RCI: Immediate versions
- 掌握四个 CSR 伪指令的用法：
    - R: Read
    - W: Write
    - S: Set bits
    - C: Clear bits
    - WI/SI/CI: Immediate versions


1. 核心考点解答
Q1: 为什么需要保存现场？哪些内容需要保存？
为什么：中断发生时，硬件只自动保存了极少的信息（sepc 记了回去的路，scause 记了原因，sstatus 记了之前的状态）。处理中断的代码（Trap Handler）也是程序，它运行需要使用通用寄存器（a0, t0, sp 等）。如果不保存，Trap Handler 就会覆盖掉原本正在运行的程序的寄存器数据，中断返回后程序逻辑就全乱了。
保存哪些：通常保存 所有通用寄存器 (x1-x31) 以及 关键 CSR (sepc, scause, sstatus)。
保存到哪里：保存到内核栈上。所以在 entry.S 开头第一件事就是把 sp 减去一大块空间（开辟栈帧）。
Q2: \_traps 非得用汇编写吗？直接指向 C 函数可以吗？
必须用汇编。
原因：C 语言函数编译后，编译器会自动生成“函数序言（Prologue）”，这部分代码会修改寄存器（如 sp, s0 等）来建立栈帧。如果在跳转到 C 之前没有手动保存所有寄存器，C 语言自动生成的代码就会破坏现场。只有汇编能精确控制“在修改任何寄存器之前，先把它存起来”。
Q3: 传递给 trap_handler 哪些参数？
根据 RISC-V 调用约定（ABI），前两个参数通过 a0, a1 传递。
为了方便 C 语言处理，汇编代码通常会将 scause (异常原因) 读取到 a0，将 sepc (异常指令地址) 读取到 a1，然后调用 call trap_handler。

### Task3: Trap Handler
### 1. 修改 `arch/riscv/kernel/main.c`
main.c的功能：
(1) 设置 stvec (2) 开启 sie/sstatus (3) 写 sip = 1 
**位置**：`start_kernel` 函数中间的 `/* Lab1 Task3 */` 处。
**逻辑**：打印 CSR 初始值 -> 开启软件中断使能 -> 开启全局中断 -> 手动触发软件中断。

```c
	/* Lab1 Task3 */
	// 1. 打印初始值
	printk("Initial sstatus: 0x%lx\n", csr_read(sstatus));
	printk("Initial sie: 0x%lx\n", csr_read(sie));
	printk("Initial sip: 0x%lx\n", csr_read(sip));

	// 2. 设置 sie：使得只有软件中断被使能
	// SIE_SSIE = 1 << 1
	csr_write(sie, SIE_SSIE);

	// 3. 设置 sstatus：使能 S 模式全局中断
	// SSTATUS_SIE = 1 << 1
	csr_set(sstatus, SSTATUS_SIE);

	// 4. 设置 sip：立刻触发一个软件中断
	// SIP_SSIP = 1 << 1
	printk("Triggering software interrupt...\n");
	csr_set(sip, SIP_SSIP);
	
	printk("Back from software interrupt!\n");
```

---

##### 2. 修改 `arch/riscv/include/sbi.h`

**位置**：补全 `csr_read`, `csr_write`, `csr_set` 宏定义。建议同时补上 `csr_clear`，后面清除中断要用。

```c
#define csr_read(csr)                           \
	({                                      \
		uint64_t __v;                   \
		asm volatile("csrr %0, " #csr : "=r" (__v) : : "memory"); \
		__v;                            \
	})

#define csr_write(csr, val)                     \
	({                                      \
		uint64_t __v = (uint64_t)(val); \
		asm volatile("csrw " #csr ", %0" : : "r" (__v) : "memory"); \
	})

#define csr_set(csr, val)                       \
	({                                      \
		uint64_t __v = (uint64_t)(val); \
		asm volatile("csrs " #csr ", %0" : : "r" (__v) : "memory"); \
	})

#define csr_clear(csr, val)                     \
	({                                      \
		uint64_t __v = (uint64_t)(val); \
		asm volatile("csrc " #csr ", %0" : : "r" (__v) : "memory"); \
	})
```


#### 3. 修改 `arch/riscv/kernel/head.S`

**位置**：`_start` 标签下，跳转 `start_kernel` 之前。
**逻辑**：将 `stvec` 寄存器指向中断入口 `_traps`。

```asm
    /* Lab1 Task3 */
    la t0, _traps       # 加载 _traps 标签的地址
    csrw stvec, t0      # 将地址写入 stvec 寄存器
```

---

#### 4. 修改 `arch/riscv/kernel/entry.S`

**位置**：`_traps` 标签下。
**逻辑**：需要保存所有通用寄存器 + CSR，调用 C 处理函数，然后恢复。

用以下代码覆盖 `_traps` 部分：

```asm
_traps:
    /* Lab1 Task3 */
    # 1. 保存现场
    # 分配栈空间：32个通用寄存器 + 4个CSR，预留 288 字节足够且对齐
    addi sp, sp, -288

    # 保存通用寄存器 (x1, x3-x31)
    sd x1, 8(sp)    # ra
    sd x3, 24(sp)   # gp
    sd x4, 32(sp)   # tp
    sd x5, 40(sp)   # t0
    sd x6, 48(sp)   # t1
    sd x7, 56(sp)   # t2
    sd x8, 64(sp)   # s0
    sd x9, 72(sp)   # s1
    sd x10, 80(sp)  # a0
    sd x11, 88(sp)  # a1
    sd x12, 96(sp)  # a2
    sd x13, 104(sp) # a3
    sd x14, 112(sp) # a4
    sd x15, 120(sp) # a5
    sd x16, 128(sp) # a6
    sd x17, 136(sp) # a7
    sd x18, 144(sp) # s2
    sd x19, 152(sp) # s3
    sd x20, 160(sp) # s4
    sd x21, 168(sp) # s5
    sd x22, 176(sp) # s6
    sd x23, 184(sp) # s7
    sd x24, 192(sp) # s8
    sd x25, 200(sp) # s9
    sd x26, 208(sp) # s10
    sd x27, 216(sp) # s11
    sd x28, 224(sp) # t3
    sd x29, 232(sp) # t4
    sd x30, 240(sp) # t5
    sd x31, 248(sp) # t6

    # 保存 CSR
    csrr t0, sepc
    csrr t1, sstatus
    csrr t2, scause
    csrr t3, stval
    
    sd t0, 0(sp)    # sepc 保存在最开头
    sd t1, 256(sp)
    sd t2, 264(sp)
    sd t3, 272(sp)

    # 2. 调用 C 语言处理函数
    # void trap_handler(uint64_t sepc, uint64_t scause, uint64_t stval)
    # 根据 RISC-V 调用约定：a0=arg0, a1=arg1, a2=arg2
    mv a0, t0       # a0 <- sepc
    mv a1, t2       # a1 <- scause
    mv a2, t3       # a2 <- stval
    
    call trap_handler

    # 3. 恢复现场
    # 恢复 CSR
    ld t0, 0(sp)    # 恢复 sepc
    ld t1, 256(sp)  # 恢复 sstatus
    
    csrw sepc, t0
    csrw sstatus, t1

    # 恢复通用寄存器
    ld x1, 8(sp)
    ld x3, 24(sp)
    # ... 中间省略的寄存器按顺序恢复 ...
    # 偷懒写法：如果你不想手写上面那一长串，可以把上面的 sd 全部改成 ld
    # 务必保证 sd 和 ld 的偏移量完全一致！
    ld x4, 32(sp)
    ld x5, 40(sp)
    ld x6, 48(sp)
    ld x7, 56(sp)
    ld x8, 64(sp)
    ld x9, 72(sp)
    ld x10, 80(sp)
    ld x11, 88(sp)
    ld x12, 96(sp)
    ld x13, 104(sp)
    ld x14, 112(sp)
    ld x15, 120(sp)
    ld x16, 128(sp)
    ld x17, 136(sp)
    ld x18, 144(sp)
    ld x19, 152(sp)
    ld x20, 160(sp)
    ld x21, 168(sp)
    ld x22, 176(sp)
    ld x23, 184(sp)
    ld x24, 192(sp)
    ld x25, 200(sp)
    ld x26, 208(sp)
    ld x27, 216(sp)
    ld x28, 224(sp)
    ld x29, 232(sp)
    ld x30, 240(sp)
    ld x31, 248(sp)

    # 恢复栈指针
    addi sp, sp, 288

    sret
```

---

#### 5. 修改 `arch/riscv/kernel/trap.c`

**位置**：补全 `clear_ssip` 和 `trap_handler`。
**逻辑**：在 `trap_handler` 中识别软件中断，调用 `clear_ssip` 消除中断信号，否则会死循环。

```c
void clear_ssip(void)
{
	/* Lab1 Task3 */
	// 清除 sip 寄存器中的 SSIP 位 (Bit 1)
	csr_clear(sip, SIP_SSIP);
}

void trap_handler(uint64_t sepc, uint64_t scause, uint64_t stval)
{
	switch (scause) {
	/* Lab1 Task3 */
	case SCAUSE_SSI: // Supervisor software interrupt
		printk("Supervisor software interrupt detected!\n");
		clear_ssip(); // 必须清除，否则返回后立马又触发
		break;
	
	/* Lab1 Task4 (后面再写) */
	
	default:
		// ... 保持原有代码 ...
```
测试通过
![[Pasted image 20260122203651.png]]

调试复盘：
中断触发需要满足 3 个条件 → `sip`（中断挂起）+ `sie`（该类型中断使能）+ `sstatus.SIE`（全局中断使能）
执行代码的顺序，先在head.S的start_,然后跳转main.c后，顺序执行，到
csr_set(sip, SIP_SSIP);调用entry.S的_traps,顺序执行到call trap_handler跳到trap.c，再顺序执行。
b  \_teaps 断点然后c，p/x $sepc，这个输出的地址是触发这次中断的指令地址。
![[Pasted image 20260122201251.png]]
![[Pasted image 20260122234914.png]]
我们看这个sepc的值就是csr_set(sip, SIP_SSIP)这条指令的地址。



### 2.5时钟中断
阅读 [3.2.1. Machine Timer **(mtime and mtimecmp)** Registers](https://zju-os.github.io/doc/spec/riscv-privileged.html#_machine_timer_mtime_and_mtimecmp_registers)，了解 RISC-V 的时钟中断机制：
#### 1. mtime 和 mtimecmp 寄存器的作用分别是什么？

| 寄存器      | 核心作用                      | 关键特性                                                                                                                                           |
| -------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| mtime    | **实时时钟计数器**：作为系统全局的实时时间基准 | ① 内存映射的 M-mode 读写寄存器；② 所有 RV32/RV64 系统均为 64 位精度；③ 以**固定频率**递增（与 CPU 主频无关），溢出后会回绕；④ 用于记录 “挂钟时间（wall-clock time）”，而非 CPU 周期；⑤ 全局共享（所有 hart 共用一个） |
| mtimecmp | **定时器比较寄存器**：用于触发机器模式时钟中断 | ① 内存映射的 M-mode 64 位寄存器；② 当 `mtime ≥ mtimecmp`（无符号整数比较）时，机器定时器中断进入「挂起态（pending）」；③ 中断会持续挂起，直到 `mtimecmp > mtime`（通常通过写入更大的 mtimecmp 值实现）        |

#### 2. mtime 记录的数值是 CPU 时钟周期吗？
**不是**。
- mtime 记录的是**挂钟时间（wall-clock time）**（实时时间），而非 CPU 时钟周期；
- 设计目的：支持现代处理器的 “动态电压 / 频率调整（DVFS）”——CPU 主频可能动态变化，但 mtime 始终以固定频率递增，保证时间基准的稳定性；
- 补充：CPU 时钟周期通常由 `cycle` CSR 寄存器记录（与 mtime 是两套独立的计数体系）。

#### 3. M 模式时钟中断挂起（pending）的条件是什么？
核心条件：`mtime` 寄存器的数值 **大于或等于** `mtimecmp` 寄存器的数值（按无符号整数比较）。
- 一旦满足 `mtime ≥ mtimecmp`，M 模式时钟中断立即进入 “挂起态”；
- 中断会持续挂起，直到 `mtimecmp` 被写入更大的值（使 `mtimecmp > mtime`），才会解除挂起。

#### 4. 要让 CPU 响应 M 模式时钟中断，需要如何设置 CSR 寄存器？
需同时满足 **2 个 CSR 寄存器配置条件**（缺一不可）：

1. **全局中断使能**：设置 `mstatus` 寄存器的 `MIE` 位（Machine Interrupt Enable，第 3 位）为 1；
    - 作用：打开 M-mode 全局中断总开关，允许 CPU 响应 M-mode 各类中断；
2. **时钟中断类型使能**：设置 `mie` 寄存器的 `MTIE` 位（Machine Timer Interrupt Enable，第 7 位）为 1；
    - 作用：精细化启用 “机器模式时钟中断”（mie 寄存器的其他位控制其他类型中断，如软件中断、外设中断）。


### 一、SBI Timer Extension
#### 1. 该扩展的核心作用
为 **S-mode 内核**提供定时器服务，绕开 M-mode 独占的 `mtime`/`mtimecmp` 寄存器限制，让 S-mode 无需直接操作 M-mode 寄存器就能设置定时器中断。

#### 2. 核心函数 `sbi_set_timer` 详解

| 项目                  | 具体内容                                                                                                                                                                |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 函数原型                | `struct sbiret sbi_set_timer(uint64_t stime_value)`                                                                                                                 |
| Extension ID (EID)  | `0x54494D45`（ASCII 码 "TIME"）                                                                                                                                        |
| Function ID (FID)   | `0`                                                                                                                                                                 |
| 参数 `stime_value` 含义 | **绝对时间值**：表示下一次定时器事件触发的时间点（对应 `mtime` 的计数值，单位由平台时钟频率决定）                                                                                                             |
| 返回值                 | 固定返回 `SBI_SUCCESS`（`sbiret.error = 0`），无其他错误码                                                                                                                       |
| 关键功能                | 1. 编程设置下一次定时器中断的触发时间；<br><br>2. 设置时**自动清除当前挂起的定时器中断**（无论 S-mode 中断是否被屏蔽）；<br><br>3. 若要取消定时器中断：可传入 `(uint64_t)-1`（表示无限延后），或直接清除 `sie` 寄存器的 `STIE` 位（屏蔽 S-mode 定时器中断） |

#### 3. S-mode 使用 SBI 定时器服务的本质

OpenSBI（M-mode 软件）会**复用 `mtimecmp` 寄存器**为 S-mode 实现 “虚拟定时器”：当 S-mode 调用 `sbi_set_timer` 时，OpenSBI 会更新 `mtimecmp` 的值，待 `mtime ≥ mtimecmp` 时触发中断，再将中断转发给 S-mode 内核。

### 二、SSTC 扩展（Supervisor-mode Timer Interrupts）核心考点

#### 1. 该扩展解决的核心问题

解决 SBI 定时器服务**效率低**的痛点：SBI 方式需要从 S-mode 陷入 M-mode 执行，而 SSTC 扩展直接为 S-mode 提供独立的定时器比较寄存器，无需 M-mode 介入。

#### 2. SSTC 扩展的核心改进（新增 / 修改的硬件资源）

| 新增 / 修改项           | 具体作用                                                                                                                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 新增 CSR：`smtimecmp` | S-mode 专属的 64 位定时器比较寄存器，**无需 M-mode 权限即可访问**                                                                                                                                                            |
| S-mode 时钟中断挂起条件    | 当 `time ≥ smtimecmp` 时，S-mode 定时器中断自动挂起（`time` 是 `mtime` 的只读影子寄存器）                                                                                                                                      |
| 寄存器位扩展             | - `mip`/`mie`：新增 `STIP`（S-mode 定时器中断挂起位）、`STIE`（S-mode 定时器中断使能位）；<br><br>- `sip`/`sie`：`STIP`/`STIE` 位直接映射 S-mode 定时器中断状态，无需 M-mode 转发；<br><br>- `mcounteren`：控制 S-mode 是否允许访问 `smtimecmp`（置位则允许，清零则禁止） |
#### 3. SSTC 扩展的使用优势与兼容性建议
- **优势**：S-mode 可直接通过 `csrw smtimecmp, a0` 设置定时器中断，无需陷入 M-mode，大幅提升效率；
- **兼容性建议**：尽管 QEMU 已支持 SSTC 扩展，但为了兼容不支持该扩展的硬件平台，**仍优先使用 SBI 提供的 `sbi_set_timer` 函数**。

#### 对比

| 对比维度   | SBI TIME 扩展             | SSTC 扩展                      |
| ------ | ----------------------- | ---------------------------- |
| 依赖层级   | 依赖 M-mode OpenSBI 转发    | 直接操作 S-mode 专属寄存器，不依赖 M-mode |
| 效率     | 低（需 S-mode → M-mode 陷入） | 高（无陷入开销）                     |
| 兼容性    | 通用（所有支持 SBI 的平台都可用）     | 依赖硬件支持（仅支持 SSTC 扩展的平台可用）     |
| 中断触发本质 | 复用 M-mode `mtimecmp`    | 使用 S-mode 专属 `smtimecmp`     |
### 2.7 Task4: 开启并处理S-Mode时钟中断
```c
/*
 * SPDX-License-Identifier: BSD-2-Clause
 *
 * Copyright (c) 2020 Western Digital Corporation or its affiliates.
 *
 * Authors:
 *   Anup Patel <anup.patel@wdc.com>
 *   Atish Patra <atish.patra@wdc.com>
 */

#include <sbi/sbi_error.h>
#include <sbi/sbi_ecall.h>
#include <sbi/sbi_ecall_interface.h>
#include <sbi/sbi_trap.h>
#include <sbi/sbi_timer.h>

static int sbi_ecall_time_handler(unsigned long extid, unsigned long funcid,
				  struct sbi_trap_regs *regs,
				  struct sbi_ecall_return *out)
{
	int ret = 0;

	if (funcid == SBI_EXT_TIME_SET_TIMER) {
#if __riscv_xlen == 32
		sbi_timer_event_start((((u64)regs->a1 << 32) | (u64)regs->a0));
#else
		sbi_timer_event_start((u64)regs->a0);
#endif
	} else
		ret = SBI_ENOTSUPP;

	return ret;
}

struct sbi_ecall_extension ecall_time;

static int sbi_ecall_time_register_extensions(void)
{
	return sbi_ecall_register_extension(&ecall_time);
}

struct sbi_ecall_extension ecall_time = {
	.name			= "time",
	.extid_start		= SBI_EXT_TIME,
	.extid_end		= SBI_EXT_TIME,
	.register_extensions	= sbi_ecall_time_register_extensions,
	.handle			= sbi_ecall_time_handler,
};
```


在 sbi_ecall_time.c 中，sbi_ecall_time_handler 调用了：
```
sbi_timer_event_start((u64)regs->a0);
```
这个函数定义在 lib/sbi/sbi_timer.c它的工作逻辑如下：


##### 问题 1：当平台支持 SSTC 扩展时，OpenSBI 会如何设置定时器？

**回答：**  
当平台支持 SSTC 扩展时，OpenSBI 会**直接更新 S-mode 专属的 stimecmp (或 vstimecmp 对于虚拟化) 寄存器**，而不再去触碰 M-mode 的 mtimecmp。

**具体实现逻辑：**

1. sbi_timer_event_start 会检查当前硬件是否支持 SSTC。
2. 如果支持，它会直接写入 stimecmp CSR 寄存器。
3. **关键点**：这样做的好处是 OpenSBI 不需要再介入中断的转发。当 time >= stimecmp 时，硬件会自动直接给 S-mode 触发中断，完全绕过了 M-mode，极大地减少了上下文切换的开销。
##### 问题 2：当平台不支持 SSTC 扩展时，OpenSBI 如何进行定时器多路复用？
**回答：**  
当不支持 SSTC 时，OpenSBI 必须使用 **M-mode 的 mtimecmp** 来模拟 S-mode 的定时器。但这就面临一个问题：M-mode 自己也可能需要定时器，S-mode 也需要，如何共用同一个硬件寄存器？这就涉及到了**多路复用（Multiplexing）**。

**具体实现逻辑：**
1. **维护虚拟队列**：OpenSBI 内部维护了一个定时器事件队列（通常是一个 delta list 或 next event 变量），记录了 M-mode 自己的定时任务和 S-mode 请求的定时任务（即 sbi_set_timer 传入的值）。
2. **比较与设置**：
    - S-mode 调用 sbi_set_timer(next_s_time)。
    - OpenSBI 会比较 next_s_time 和 M-mode 自己下一次需要唤醒的时间 next_m_time。
    - 它将硬件的 mtimecmp 设置为这两个时间中**更早的那个**（min(next_s_time, next_m_time)）。
3. **中断分发**：
    - 当 mtime >= mtimecmp 触发 M-mode 中断时，OpenSBI 的 Trap Handler 会被唤醒。
    - 它检查当前时间是否达到了 S-mode 请求的时间。
    - 如果是，它会通过设置 mip.STIP（S-mode Timer Interrupt Pending）位，人工**注入**一个 S-mode 软中断/定时器中断。
    - 然后 S-mode 内核就会收到中断，认为定时器到期了。



trap.c中,1. 实现 clock_set_next_event：读取当前时间，加上 1秒（10^7 cycles），调用 SBI 设置下一次中断。2. 在 trap_handler 中添加 SCAUSE_STI (时钟中断) 的处理分支。
```c
#define TIMEBASE 10000000

void clock_set_next_event(void) {
	/* Lab1 Task4 */
	// 1. 获取当前时间 (读取 time CSR)
	uint64_t current_time;
	asm volatile("csrr %0, time" : "=r"(current_time) : : "memory");

	// 2. 计算下一秒的时间点 = 当前时间 + TIMEBASE
	uint64_t next_time = current_time + TIMEBASE;

	// 3. 调用 SBI 设置定时器
	sbi_set_timer(next_time);
}

...


void trap_handler(uint64_t sepc, uint64_t scause, uint64_t stval)
{
	switch (scause) {
	/* Lab1 Task3 */
    case SCAUSE_SSI: // Supervisor software interrupt
        printk("Supervisor software interrupt detected!\n");
        clear_ssip(); // 清除中断标志
        break;
		
	/* Lab1 Task4 */
	case SCAUSE_STI: // Supervisor timer interrupt
		printk("Supervisor timer interrupt detected!\n");
		// 设置下一次时钟中断，否则中断只会触发一次或一直触发
		clock_set_next_event();
		break;

	default:
	...
	}
```


然后clock.c 读取 time 寄存器,将 CPU 周期数（10MHz）转换为 POSIX 标准（1MHz）。
```c
#include <time.h>
#include <stdint.h>

// QEMU 频率 10MHz, POSIX CLOCKS_PER_SEC 1MHz
// 比例关系: 10
#define TIME_TO_CLOCK_RATIO 10

clock_t clock(void)
{
	/* Lab1 Task4 */
	uint64_t cycles;
	// 读取 time CSR 寄存器
	asm volatile("csrr %0, time" : "=r"(cycles) : : "memory");
	
	// 返回值需要除以比率，以符合 CLOCKS_PER_SEC 的定义
	return cycles / TIME_TO_CLOCK_RATIO;
}
```
修改main.c
```
/* Lab1 Task4 */
	printk("Initializing timer interrupt...\n");
    
    // 1. 开启时钟中断使能 (STIE)
    // SIE_STIE = 1 << 5
    csr_set(sie, SIE_STIE);

    // 2. 立刻触发一次时钟中断
    // 设置时间为 0，这代表“过去的时间”，会立即触发
    sbi_set_timer(0);
```
![[Pasted image 20260123171251.png]]
Task3，4调试复盘
在_traps打断点，scause最高位1，低位1，为软件中断。sstatus的SPP（bit8） = 1说明中断发生前，CPU 处于 S -Mode；SPIE (Bit 5) = 1：Previous Interrupt Enable 是开启的。说明中断发生前，内核允许中断，且SIE (Bit 1) = 0：Current Interrupt Enable 是关闭的。
![[Pasted image 20260123164245.png]]

然后在trap_handler设断点，跑到task4的csr_set(sie,SIE_STIE)后 查看scause变化，(1,1)变成了（1,5）说明正确的触发了时钟中断。
![[Pasted image 20260123170210.png]]