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


这意味着什么？（实验核心考点）
OpenSBI 在跳转到内核之前，打印了一行：
Domain0 Next Mode : S-mode
这就构成了一个致命的矛盾：
OpenSBI 把 CPU 切到了 S 模式。
OpenSBI 把控制权交给了内核（PC = 0x80200000）。
但是，寄存器 sp 仍然指向 0x80046eb0（Region 03）。
后果：
如果你的内核第一条指令不去修改 sp，而是直接尝试使用栈（比如 sd ra, 0(sp)），CPU 的 PMP（物理内存保护）硬件检查机制会立刻发现：“当前是 S 模式，但你试图访问只有 M 模式才能访问的 Region 03”。
于是，CPU 会立刻抛出一个 Load/Store Access Fault 异常，内核直接崩溃。
这就是为什么 Task 1 要求你做的第一件事就是：
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
    
- 这就意味着 skernel + .text大小 + .rodata大小 + .data大小 之后的地址，就是栈的底部（低地址）。

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
之前我们在 OpenSBI 看到旧的 sp 是 0x8004xxxx（高危区域）。
现在的 0x8020xxxx 正是我们链接脚本中定义的 .bss 段所在的区域（内核数据区）。
你看汇编窗口的第一行：addi sp, sp, -128。如果你定义的栈顶是 0x80205000 左右，减去 128 正好是 0x80204f80。这证明你成功切换到了自己的栈。



![[Pasted image 20260120142624.png]]
通过了评测。