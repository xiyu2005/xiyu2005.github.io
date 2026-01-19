---
title: CTFRevLab1
draft: false
tags:
  - CTF
---

# Lab1reverse

## challenge 1复现hello.c的编译执行流程

**实验环境:**

- **操作系统**：macOS
  - **编译器**：`clang`
- **目标文件格式**：macOS 使用 **Mach-O** 格式
- **分析工具**：
  - `file`: 用于识别文件类型。
  - `otool`: macOS 原生的目标文件分析工具，功能类似于Linux上的 `readelf`。
  - **关于 `readelf`**：`readelf` 是GNU Binutils的一部分，用于分析ELF格式文件，因此**无法**直接在macOS上分析其原生的Mach-O格式文件。本报告将使用 `otool` 作为替代工具。

------



### **第0步：准备源代码**

首先，我们创建一个名为 `hello.c` 的C语言源文件。

**操作命令：**

```
# 使用文本编辑器创建 hello.c 文件
vim hello.c
```

**`hello.c` 文件内容：**

```C
#include <stdio.h>
int main() {
    printf("Hello, World!\n");
    return 0;
}
```

**使用 `file` 查看源文件类型：**

```sh
kaisenye@192 lab1rev % file hello.c
hello.c: c program text, ASCII text
```

输出显示 `hello.c` 是一个C语言源文件，采用ASCII文本编码。

### **第一步：预处理 (Preprocessing)**

**目标：** 此阶段处理源代码中以 `#` 开头的预处理指令，主要工作包括：宏替换、头文件内容展开、注释移除和条件编译处理。

**操作命令：** 使用 `clang` 的 `-E` 选项执行预处理，并将结果输出到 `hello.i` 文件。

```sh
clang -E hello.c -o hello.i
```

- `-E`: 指示 `clang` 仅执行预处理阶段。
- `-o hello.i`: 指定输出文件名为 `hello.i`。

**分析输出文件 `hello.i`：** `hello.i` 文件内容会非常多，因为它包含了 `<stdio.h>` 头文件展开后的所有声明。我们自己编写的 `main` 函数位于文件的末尾，并且所有注释都已被移除。


![[image-20250705103007659.png]]
**使用 `file` 查看文件类型：**

```shell
kaisenye@192 lab1rev % file hello.i
hello.i: c program text, ASCII text
```

输出表明 `hello.i` 仍然是一个可以被编译器直接处理的C语言源文件。

### **第二步：编译 (Compilation)**

**目标：** 此阶段接收预处理后的文件 (`hello.i`)，通过一系列分析和优化，将其翻译成对应CPU架构的**汇编代码**。

**操作命令：** 使用 `clang` 的 `-S` 选项执行编译，并将结果输出到 `hello.s` 文件。

```sh
clang -S hello.c -o hello.s
```

- `-S`: 指示 `clang` 在预处理和编译后停止，不进行汇编。
- `-o hello.s`: 指定输出的汇编文件名为 `hello.s`。

**分析输出文件 `hello.s`：** `hello.s` 是一个文本文件，包含了 `main` 函数的汇编语言指令。在macOS上，默认使用AT&T汇编语法。


![[image-20250705103052186.png]]
**使用 `file` 查看文件类型：**

```sh
kaisenye@192 lab1rev % file hello.s
hello.s: assembler source text, ASCII text
```

输出确认了 `hello.s` 是一个汇编源文件。

### **第三步：汇编 (Assembly)**

**目标：** 汇编器 (assembler) 将汇编代码 (`hello.s`) 翻译成机器语言指令，并打包成一种称为**可重定位目标文件 (Relocatable Object File)** 的格式。

**操作命令：** 使用 `clang` 的 `-c` 选项执行汇编，生成 `hello.o` 文件。

```sh
clang -c hello.s -o hello.o
```

- `-c`: 指示 `clang` 执行预处理、编译和汇编，但不要链接。
- `-o hello.o`: 指定输出的目标文件名为 `hello.o`。

**分析输出文件 `hello.o`：** `hello.o` 是一个二进制文件，包含了未经链接的机器码。

**使用 `file` 查看文件类型：**

```sh
kaisenye@192 lab1rev % file hello.o
hello.o: Mach-O 64-bit object arm64
```

输出明确指出这是一个 **Mach-O 64位目标文件**

**使用 `otool` 查看目标文件头信息：** `otool -h` 命令可以显示Mach-O文件的头部信息，类似于 `readelf -h`。

```
kaisenye@192 lab1rev % otool -h hello.o
hello.o:
Mach header
      magic  cputype cpusubtype  caps    filetype ncmds sizeofcmds      flags
 0xfeedfacf 16777228          0  0x00           1     4        440 0x00002000
```

### **第四步：链接 (Linking)**

**目标：** 链接器 (linker) 将一个或多个目标文件（如 `hello.o`）与它们所需的库（如包含了 `printf` 函数实现的系统库）结合起来，创建最终的**可执行文件**。

**操作命令：** 直接使用 `clang` 将目标文件链接成可执行文件 `hello`。

Bash

```
clang hello.o -o hello
```

**分析输出文件 `hello`：**

**使用 `file` 查看文件类型：**

Bash

```sh
kaisenye@192 lab1rev % file hello
hello: Mach-O 64-bit executable arm64
```

输出显示 `hello` 现在是一个 **Mach-O 64位可执行文件**。

**使用 `otool` 查看可执行文件头信息：**

Bash

```
kaisenye@192 lab1rev % otool -h hello
hello:
Mach header
      magic  cputype cpusubtype  caps    filetype ncmds sizeofcmds      flags
 0xfeedfacf 16777228          0  0x00           2    17       1056 0x00200085
```

**使用 `otool` 查看动态链接库依赖：** `otool -L` 命令可以列出程序运行时需要依赖的动态库，类似于Linux上的 `ldd`。

```
kaisenye@192 lab1rev % otool -h hello
hello:
Mach header
      magic  cputype cpusubtype  caps    filetype ncmds sizeofcmds      flags
 0xfeedfacf 16777228          0  0x00           2    17       1056 0x00200085
kaisenye@192 lab1rev % otool -L hello
hello:
        /usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1351.0.0)
```

输出显示，我们的程序依赖于 `/usr/lib/libSystem.B.dylib`。在macOS上，`printf` 等标准C库函数都包含在这个核心系统库中。

### **第五步：执行程序**

最后一步是运行我们生成的可执行文件。

**操作命令：**

```sh
./hello
```

**输出：**

```sh
Hello, World!
```

### **任务2.1 操作报告：静态分析工具 IDA**

**目的：** 熟悉静态分析与反汇编工具IDA (Interactive Disassembler) 的基本操作，掌握其核心功能与常用快捷键，并记录对未来使用有帮助的技巧。

**分析对象：** 一个简单的C程序 `example_ida`，它接受一个命令行参数并打印欢迎语。

```c
// example.c
#include <stdio.h>
#include <string.h>

// 一个易受攻击的函数
void unsafe_greet(const char* name) {
    char buffer[64];
    strcpy(buffer, "Hello, "); // 使用危险的strcpy
    strcat(buffer, name);
    printf("Welcome: %s\n", buffer);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: %s <name>\n", argv[0]);
        return 1;
    }
    unsafe_greet(argv[1]);
    return 0;
}
```

编译命令：`gcc -o example_ida example.c`

------



#### **一、IDA 核心功能与操作流程**

1. **加载文件与初识界面**

   - 打开 IDA，将可执行文件 `example_ida` 拖入窗口或通过 `File -> Open` 打开。
   - IDA 会弹出加载配置窗口，通常直接点击 `OK` 使用默认设置即可。IDA会自动识别文件类型（如ELF, Mach-O, PE）并进行反汇编。
   - 加载完成后，IDA 默认会定位到程序的入口点 `_start`，并以 **图形视图 (Graph View)** 显示。

   ![[image-20250705104627970.png]]

2. **图形视图与文本视图切换**

   - **图形视图**：以流程图的形式展示代码块（Basic Blocks）和它们之间的跳转关系（如 `if-else` 分支、循环），非常直观。
     - 绿色的箭头表示条件不成立时的跳转。
     - 蓝色的箭头表示条件成立时的跳转。
     - 黑色的箭头表示无条件跳转。
   - **文本视图**：传统的线性反汇编列表，适合查看连续的代码。
   - **快捷键 `Spacebar`**：在图形视图和文本视图之间快速切换。这是最常用的快捷键之一。

3. **导航与识别关键函数**

   - **Functions 窗口**：通过 `Shift + F7` 打开函数窗口，这里列出了IDA识别出的所有函数。我们可以双击 `main` 或 `unsafe_greet` 直接跳转到对应函数的代码。

   ![[image-20250705104706798.png]]

   - **跳转到地址/符号**：按 **快捷键 `G`**，输入函数名（如 `main`）或地址，可以快速跳转。



#### **二、常用功能与快捷键**

1. **交叉引用 (Cross-References / Xrefs)**

   - 这是IDA最强大的功能之一。它能告诉你一个函数被谁调用，或者一个数据被谁使用。

   - **操作**：在函数名 `unsafe_greet` 上单击，然后按 **快捷键 `X`**。

   - **结果**：IDA会弹出一个窗口，显示 `main` 函数在 `_main+58` 地址处调用了 `unsafe_greet`。双击该条目即可跳转到调用处。通过查看交叉引用，我们可以轻松地追踪程序的调用链。

     ![[image-20250705104905923.png]]

2. **字符串 (Strings)**

   - **快捷键 `Shift + F12`**：打开字符串窗口，列出程序中所有硬编码的字符串。

 ![[image-20250705104940215.png]]

3. **重命名与注释 (提高可读性)**

   - IDA自动生成的变量名和标签名（如 `var_50`, `loc_118A`）可读性很差。
   - **重命名**：选中变量或标签，按 **快捷键 `N`**，即可输入一个有意义的新名字。例如，可以将栈上的 `var_50` 重命名为 `buffer`。
![[image-20250705105126696 1.png]]
   

   ![[image-20250705105134257.png]]

   - **添加注释**：
     - **快捷键 `;`**：在当前行添加普通注释。
     - **快捷键 `:`**：在当前行添加可重复注释（当多处代码引用该地址时，注释会同步显示）。

4. **伪代码反编译器 (Decompiler)**

   - **快捷键 `F5`**：在反汇编窗口中按 `F5`，IDA会将当前函数的汇编代码转换成可读性极高的C伪代码。

   - **优势**：通过伪代码可以快速了解函数逻辑，即使是初学者也能快速理解程序的核心行为。下图就是 `unsafe_greet` 函数的 `F5` 结果，对比源代码和反汇编结果，逻辑一目了然。
![[image-20250705105328397.png]]
     
![[image-20250705105404636.png]]
​	



### **任务2.2 操作报告：动态调试工具 GDB (配合 Pwndbg)**



**目的：** 学习和掌握命令行动态调试工具 GDB 的核心命令，并利用 `pwndbg` 插件提升调试效率和体验。

**调试对象：** 一个有栈溢出漏洞的程序 `example_gdb`。为了方便调试，使用以下命令编译： `gcc -g -fno-stack-protector -o example_gdb example.c`

- `-g`: 加入调试信息，方便GDB关联源码。
- `-fno-stack-protector`: 关闭栈保护 (canary)，让溢出更容易复现。

**插件安装 (Pwndbg):** `pwndbg` 极大地美化了GDB的界面，并增加了许多便利的命令。

Bash

```
git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh
```

------



#### **一、GDB 基础命令与 Pwndbg 界面**

在linux下将example.c编译为example

用一个易被攻击的函数示范

```c
// 文件名: challenge.c
#include <stdio.h>
#include <string.h>
#include <unistd.h>

void vulnerable_function(char* input) {
    char buffer[100];
    printf("输入的数据地址: %p\n", input);
    strcpy(buffer, input); // 核心漏洞点：不检查长度，直接复制
    printf("缓冲区内容: %s\n", buffer);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("用法: %s <你的输入>\n", argv[0]);
        return 1;
    }
    printf("主函数 main 的地址: %p\n", main);
    printf("vulnerable_function 的地址: %p\n", vulnerable_function);
    vulnerable_function(argv[1]);
    printf("程序正常结束。\n");
    return 0;
}
```





**2. 编译示例程序**

为了方便调试，我们在编译时加入调试符号 (`-g`) 并关闭一些安全保护。sh

```
# -g: 包含调试信息 (函数名、行号等)
# -fno-stack-protector: 关闭栈保护(canary)，让溢出更容易复现
# -z execstack: 允许栈上的数据被当作代码执行 
# -o challenge: 指定输出文件名为 challenge
gcc -g -fno-stack-protector -z execstack -o challenge challenge.c
```

**3. 安装 Pwndbg**

`Pwndbg` 的安装过程非常简单。

```
# 1. 克隆仓库
git clone https://github.com/pwndbg/pwndbg

# 2. 进入目录并运行安装脚本
cd pwndbg
./setup.sh
```

安装完成后，下次启动GDB时，`Pwndbg` 将会自动加载。

------



#### **第二步：核心调试流程**

**1. 启动 Pwndbg**

使用 `pwndbg` (或 `gdb`) 命令加载我们编译好的程序。

```
pwndbg ./challenge
```

程序加载后，`Pwndbg` 会立刻呈现一个非常强大的**上下文信息界面 (Context Display)**，包含：

- **REGISTERS**: 关键寄存器的值 (如 `RAX`, `RDI`, `RSP`, `RIP`)。
- **DISASM**: 即将执行的汇编指令。
- **STACK**: 栈顶的数据预览，并智能地解析指针。
- **BACKTRACE**: 当前的函数调用栈。

**2. 设置断点 (Breakpoints)**

断点是调试的灵魂，它能让程序在指定位置暂停。



```
# 在 main 函数入口处设置断点
pwndbg> b main

# 在 vulnerable_function 函数入口处设置断点
pwndbg> b vulnerable_function

# 也可以在 strcpy 函数被调用的地方设置断点
# 首先用 astyle-c <vulnerable_function> 查看函数汇编
pwndbg> disassemble vulnerable_function
```


![[image-20250705115912434.png]]
**常用命令**: `break` (可缩写为 `b`)。

**3. 运行与流程控制**

- `run <参数>` 或 `r <参数>`: 启动程序。
- `continue` 或 `c`: 继续执行直到下一个断点。
- `next` 或 `n`: 执行下一行代码（**不进入**函数内部）。
- `step` 或 `s`: 执行下一行代码（**进入**函数内部）。

我们先运行到 `main` 函数的断点：

```
pwndbg> r
```


![[image-20250705120021986.png]]
**4. 实战演练：分析栈溢出**

现在，我们让程序继续运行，并传入一个超长字符串来触发漏洞。

1. 使用一个超长字符串作为参数运行程序，并持续执行直到程序停在`vulnerable_function`。

   - **操作命令**:

     ```
     pwndbg> r $(python -c 'print("A"*120)')
     pwndbg> c
     ```

   - **关键输出**:

     ![[image-20250705123032740.png]]

2. **单步执行，观察溢出** 这是实验最核心的环节。通过`n`命令单步执行，观察`strcpy`前后堆栈的变化。

   - **步骤 3.1: strcpy 执行前**

     - **操作命令**: `pwndbg> n` (执行第8行的`printf`)

       ![[image-20250705123812530.png]]

     以看到 `buffer` 所在的内存区域 (`0x7fffffffdaa0`) 被一长串 `A` 填满了。

     ```
     02:0010│ rax 0x7fffffffdaa0 ◂— 'AAAAAAAAAAAAAAAAA...'
     ```

   - **步骤 3.2: strcpy 执行后 (关键时刻)**

     - **操作命令**: `pwndbg> n` (执行第9行的`strcpy`)

     - **效果**

       ![[image-20250705123654377.png]]

       ![[image-20250705123716716.png]]

3. **最终崩溃** 让程序继续执行，观察最终的崩溃。

   - **操作命令**: `pwndbg> c`

   - **关键输出**:

     ![[image-20250705124117832.png]]

------

**核心证据分析：**

1. **`RBP` 彻底损坏**  `REGISTERS` 窗口：

   ```
   *RBP  0x4141414141414141 ('AAAAAAAA')
   ```

   返回地址被覆盖，连储存的 **`RBP` 堆叠基址指针** 也被彻底换成了 `0x4141...`。这导致堆叠结构完全错乱。

2. **执行流程失控** 当 `vulnerable_function` 试图返回时，因为 `RBP` 和返回地址都已损坏，它没有像我们预期的那样地跳转到 `0x4141...`。相反，错误地跳转到了另一个地址 `0x555555555200`。

3. **非法指令 (`SIGILL`)** CPU 以为 `0x555555555200` 是一个合法的指令位址，于是尝试执行那里的内容。但那的数据并不是一条有效的 CPU 指令，所以 CPU 无法识别，触发了 **`SIGILL, Illegal instruction.`** 的信号。 `DISASM` 窗口也证实了这一点：

   ```
   Invalid instructions at 0x555555555200
   ```

4. - **堆叠全毁的旁证**
     - **回溯失败 (`BACKTRACE`)**：正常的 `BACKTRACE` 会显示完整的函数呼叫链。你的结果只剩下一帧，说明堆叠被破坏得无法回溯了。
     - **变数读取失败**：GDB 尝试读取 `argc` 和 `argv` 变数时出错，因为它也依赖堆叠指标来定位变数，而现在堆叠已经全乱了。

#### 

#### **第三步：Pwndbg 常用辅助命令**

除了核心的调试流程，`Pwndbg` 还提供了大量便利的命令。

- `checksec`: 检查二进制文件的安全措施，非常有用！

  ```
  pwndbg> checksec
  ```

  ![[image-20250705124947995.png]]

- `vmmap`: 查看程序的虚拟内存映射，了解各个段（代码、数据、堆、栈）的地址和权限。

  ![[image-20250705125054247.png]]

- `telescope <地址>`: 智能地显示一块内存区域的内容，比GDB原生的 `x` 命令更强大。

  ```
  pwndbg> telescope $rsp 20 # 显示栈顶向下20个单位的内容
  ```

  ![[image-20250705125110838.png]]

- `search <内容>`: 在内存中搜索指定内容。

  ```
  pwndbg> search "printf" # 搜索字符串
  ```

  ![[image-20250705125155540.png]]

- `hexdump <地址>`: 以十六进制和ASCII格式显示内存。

------



通过本次实验，我们成功地在Linux环境下使用 `Pwndbg` 完成了对一个C程序的动态调试。我们掌握了设置断点、控制程序流程、观察内存和寄存器状态的核心技能。

`Pwndbg` 强大的上下文显示和辅助命令，极大地提升了GDB的可用性和调试效率，将原本枯燥的命令行调试变成了一个直观、高效的分析过程。尤其在栈溢出分析中，`Pwndbg` 对关键数据（如返回地址）的自动高亮和解析，使得漏洞的成因和后果一目了然。

------



### **总结**

- **IDA (静态)** 和 **GDB (动态)** 是逆向工程和漏洞分析中相辅相成的两大神器。
- **IDA** 负责在不运行程序的情况下，从宏观上（伪代码）和微观上（汇编）理解程序的架构和逻辑。其强大的交叉引用和反编译功能是分析的基石。
- **GDB + Pwndbg** 负责在程序运行时，验证静态分析的猜想，观察内存和寄存器的实时变化，是调试和漏洞利用的利器。
- **工作流**：通常先用IDA进行静态分析，对程序行为有一个大致的了解，找到可疑点；然后用GDB动态调试，在可疑点下断点，观察实际运行情况，最终确认程序的行为或漏洞。熟练掌握这两套工具，将极大地提升分析和解决问题的能力。

## Challenge3

### 3.1例2

ida逆向的c伪代码为

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  _BYTE v3[30]; // [esp+14h] [ebp-3Ch] BYREF
  _BYTE v4[26]; // [esp+32h] [ebp-1Eh] BYREF
  unsigned int i; // [esp+4Ch] [ebp-4h]

  qmemcpy(v4, "MMMwjau`S]]S}ybS?4:;5:<4<q", sizeof(v4));
  printf("Please input flag: ");
  scanf("%s", v3);
  for ( i = 0; i < 0x1A; ++i )
  {
    if ( (v3[i] ^ 0xC) != v4[i] )
    {
      printf("Your flag is not right.");
      exit(0);
    }
  }
  printf("You are right!");
  exit(0);
}
```





### **代码分析**

程序的关键逻辑在于这个 `for` 循环：

```c
for ( i = 0; i < 0x1A; ++i )
{
   if ( (v3[i] ^ 0xC) != v4[i] )
   {
      printf("Your flag is not right.");
      exit(0);
   }
}
```

1. 程序将输入（`v3`）的每一个字符与一个十六进制数 `0xC` 进行**异或（XOR）**运算。

2. 然后，它将运算结果与内置的加密字符串 `v4`比较

   ```
   MMMwjau`S]]S}ybS?4:;5:<4<q
   ```

   如果一致，就会输出you are right。

   为了找到正确的flag，我们需要逆转这个过程。异或运算有一个特性：如果 `A ^ B = C`，那么 `C ^ B = A`。

   因此，我们只需要将加密字符串 `v4` 的每一个字符与 `0xC` 进行一次异或运算，就可以得到原始的 flag（`v3`）。

   编写脚本求解如下xor.py

   ```python3
   encrypted_string = "MMMwjau`S]]S}ybS?4:;5:<4<q"
   key = 0xC
   
   original_flag = "".join([chr(ord(char) ^ key) for char in encrypted_string])
   
   print(f"\n 解密结果: {original_flag}")
   ```

   ![[image-20250705132426401.png]]

### 3.2例3

ida反汇编得到代码

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int v4; // [rsp+24h] [rbp-44h] BYREF
  void *Buf1; // [rsp+28h] [rbp-40h] BYREF
  _BYTE v6[56]; // [rsp+30h] [rbp-38h] BYREF

  sub_401770(argc, argv, envp);
  printf("please input the flag:");
  scanf("%s", v6);
  Buf1 = 0;
  sub_401570(v6, &Buf1, &v4);

  if ( !memcmp(Buf1, a5mc58bphliax7j, v4) )
    printf("\nsuccess!");
  else
    printf("\nfailed!");
  if ( Buf1 )
    free(Buf1);
  return 0;
}
```



**`sub_401570(v6, &Buf1, &v4);`**: 这是 **最关键** 的一步。

- 它接收你的输入 `v6` 作为第一个参数。
- 它接收 `Buf1` 和 `v4` 的地址作为第二和第三个参数。这通常意味着该函数会修改 `Buf1` 和 `v4` 的值。
- 结合上下文推断，`sub_401570` 极有可能是一个加密或编码函数。它将你的输入 `v6` 进行某种变换，将变换后的结果存放在 `Buf1` 指向的内存中，并将结果的长度存入 `v4`。

查看函数sub_401570

```
__int64 __fastcall sub_401570(const char *a1, _QWORD *a2, int *a3)
{
  int v6; // r15d
  int v7; // r12d
  int v8; // r13d
  __int64 v9; // r14
  _BYTE *v10; // rax
  _BYTE *v11; // r9
  __int64 v12; // r8
  char v13; // cl
  char v14; // r11
  char v15; // r10
  __int64 result; // rax
  v6 = strlen(a1);
  v7 = v6 % 3;
  if ( v6 % 3 )
  {
    v8 = 4 * (v6 / 3) + 4;
    v9 = v8;
    v10 = malloc(v8 + 1LL);
    v10[v8] = 0;
    if ( v6 <= 0 )
      goto LABEL_5;
  }
  else
  {
    v8 = 4 * (v6 / 3);
    v9 = v8;
    v10 = malloc(v8 + 1LL);
    v10[v8] = 0;
    if ( v6 <= 0 )
      goto LABEL_8;
  }
  v11 = v10;
  v12 = 0;
  do
  {
    v11 += 4;
    v13 = a1[v12];
    *(v11 - 4) = aQvejafhmuyjbac[v13 >> 2];
    v14 = a1[v12 + 1];
    *(v11 - 3) = aQvejafhmuyjbac[(v14 >> 4) | (16 * v13) & 0x30];
    v15 = a1[v12 + 2];
    v12 += 3;
    *(v11 - 2) = aQvejafhmuyjbac[(v15 >> 6) | (4 * v14) & 0x3C];
    *(v11 - 1) = aQvejafhmuyjbac[v15 & 0x3F];
  }
  while ( v6 > (int)v12 );
LABEL_5:
  if ( v7 == 1 )
  {
    v10[v9 - 2] = 61;
    v10[v9 - 1] = 61;
  }
  else if ( v7 == 2 )
  {
    v10[v9 - 1] = 61;
  }
LABEL_8:
  *a2 = v10;
  result = 0;
  *a3 = v8;
  return result;
}
```

它实现的是 **带有自定义字符表的 Base64 编码**。

**处理方式**: 算法以3个字节（`char`）为一组进行读取，并生成4个字节的输出。这是 Base64 的典型特征（3 * 8位 = 24位 -> 4 * 6位 = 24位）。

**位运算**: 代码中的位移（`>>`, `<<` 隐含在乘法中）和位与（`&`）操作：

- `v13 >> 2` (取第1个字节的前6位)
- `... | (16 * v13) & 0x30` (取第1个字节的后2位和第2个字节的前4位)
- `... | (4 * v14) & 0x3C` (取第2个字节的后4位和第3个字节的前2位)
- `v15 & 0x3F` (取第3个字节的后6位)

这些操作与标准 Base64 编码的位处理逻辑完全一致。

**查询表**: 每次生成的6位（0-63）索引都用于从一个名为 `aQvejafhmuyjbac` 的表中查找一个字符。这是 Base64 的核心，但它使用的是 **自定义的字符表** 而不是标准的 `A-Z, a-z, 0-9, +, /`。

**填充 (Padding)**: 函数最后检查输入长度除以3的余数（`v7`），并相应地在输出末尾添加一个或两个 `=` 字符（ASCII码 `61`）。这是 Base64 处理非3倍数长度输入的标准填充方法。

变量aQvejafhmuyjbac

```
aQvejafhmuyjbac db 'qvEJAfHmUYjBac+u8Ph5n9Od17FrICL/X0gVtM4Qk6T2z3wNSsyoebilxWKGZpRD',0
```

变量a5mc58bphliax7j

```
a5mc58bphliax7j db '5Mc58bPHLiAx7J8ocJIlaVUxaJvMcoYMaoPMaOfg15c475tscHfM/8==',0
```

编写python脚本解得

NSSCTF{a8d4347722800e72e34e1aba3fe914ae}

## Bonus2

### **程序分析**

#### **2.1 静态分析**

使用 dnSpy 对 `Matrix.exe` 进行反编译，可以清晰地看到其内部结构。程序的核心逻辑位于 `Matrix_Int.Program` 类的 `Main` 方法中。通过分析 `Main` 方法的 C# 代码，我们确定了程序的验证流程分为三个主要部分。

![image-20250718193601365](/Users/kaisenye/Library/Application Support/typora-user-images/image-20250718193601365.png)

#### 2.2 验证逻辑的数学模型

程序的验证逻辑可以抽象为两个独立的数学校验过程，分别作用于 Flag 内容的不同部分。设用户输入的31位有效内容为字符串 $F_{content}$。

1. ##### XOR/Base64 校验 (作用于 $F_{content}$ 的后17个字符)

  此校验过程是一个对称的加密和比较。
- ##### 定义输入:

  设用于校验的子字符串为 $S$，由 $F_{content}$ 的后17个字符组成。记 $S$ 的字符序列为 $(s_1, s_2, \ldots, s_{17})$。
- ##### 密钥生成:

  程序首先根据 $S$ 动态生成一个单字节密钥，记为 $k_{xor}$。该密钥是 $S$ 中所有字符的ASCII码值的异或总和。
  $$
  k_{xor} = \bigoplus_{i=1}^{17} \text{ASCII}(s_i)
  $$

- ##### 加密过程:

  程序使用生成的密钥 $k_{xor}$ 对原字符串 $S$ 进行加密，生成一个17字节的加密数组，记为 $B_{enc}$。

$$
B_{enc}[i] = \text{ASCII}(s_i) \oplus k_{xor} \quad \text{for } i \in [1, 17]
$$

- ##### 最终校验：

程序将加密字节数组 $B_{enc}$ 进行 Base64 编码，并与一个硬编码的目标字符串 $T_{target}$ 进行比较。
$$\text{Base64Encode}(B_{enc}) = T_{target}$$
其中，$T_{target} = "d3l5d3ldRncbEB4fER4YEBg="$。
2. #### 矩阵乘法校验 (作用于 $F_{content}$ 的前14个字符)

  此校验过程是一个在有限域上的线性方程组判定。
- ##### 定义输入：

  设用于校验的子字符串为 $P$，由 $F_{content}$ 的前14个字符组成，记为 $(p_1, p_2, \ldots, p_{14})$。程序将其转换为一个 14x1 的列向量 $V_{input}$。
  $$
  V_{input} = \begin{pmatrix} \text{ASCII}(p_1) \\ \text{ASCII}(p_2) \\ \vdots \\ \text{ASCII}(p_{14}) \end{pmatrix}
  $$

##### 密钥矩阵生成：

程序调用 GetSquare() 方法动态生成一个 14x14 的密钥矩阵$M$。设用于生成矩阵的动态字节

数组为$D$ (长度为195),则矩阵$M$的每个元素$M_{i,j}$由以下公式确定 (其中矩阵和数组索引均从0开始):

$$
M_{i,j}=D[(7\times(i+j\times14))\quad(\mathrm{mod~}195)]\quad(\mathrm{mod~}127)
$$

#####  最终校验：

程序在一个有限域$GF(127)$ (即所有运算结果对127取模) 中，校验矩阵乘法的结果是否等于

一个硬编码的结果向量$V_{result}$ 。

$$
M\cdot V_{input}\equiv V_{result}\quad(\mathrm{mod~}127)
$$




#### **3. 逆向破解策略与算法**

针对上述两个独立的验证模型，我们制定了相应的破解算法。

**1. 破解 XOR/Base64 校验**

这是一个典型的“已知密文求明文”问题，由于密钥空间很小，可以采用爆破法。

- 数据准备:
首先对目标字符串 $T_{target}$ 进行 Base64 解码，得到目标加密字节数组 $B_{enc}'$。
$$B_{enc}' = Base64Decode(T_{target})$$
- 逆运算关系:
从加密公式 $B_{enc}[i] = ASCII(s_i) \oplus k_{xor}$ 可推导出逆运算关系:
$$
ASCII(s_i) = B_{enc}'[i] \oplus k_{xor}$$
- 密钥爆破:
由于密钥 $k_{xor}$ 的值域为 [0, 127]，我们可以遍历所有可能的候选密钥 $k' \in [0, 127]$。对于每一个 $k'$，我们都生成一个候选的字符序列 $S'$。
$$s'_i = chr(B_{enc}'[i] \oplus k') \quad for \; i \in [1, 17]$$

正确的密钥 $k_{xor}$ 是唯一那个能使得 $S'$ 中所有字符均为标准可打印ASCII字符（编码值在32到126之间）的 $k'$.



2. ##### 破解矩阵乘法校验

  我们的任务是求解在有限域 $GF(127)$ 上的线性方程组 $M \cdot x = b$。
- 方程组定义：
- $M$：通过动态调试获取的字节数组生成的 14x14 密钥矩阵。
- $x$：未知量，即我们要求解的输入向量 $V_{input}$。
- $b$：从程序中静态提取的 14x1 结果向量 $V_{result}$。
- 失败的尝试（矩阵求逆法）：
最初尝试通过计算 $M$ 在模 127 下的逆矩阵 $M^{-1}$ 来求解：
$$x = M^{-1} \cdot b \pmod{127}$$

此方法失败，因为在计算中发现 $\det(M) \equiv 0 \pmod{127}$，即矩阵 $M$ 在该有限域下是奇异的，不存在逆矩阵。

· 成功的解法(高斯消元法):

采用更通用的高斯消元法直接求解。

1. 构建增广矩阵：将矩阵$M$和向量$b$组合成一个 14x15 的增广矩阵$[M|b]$。
2. 前向消元：通过一系列初等行变换 (行交换、某行乘以一个非零标量、某行加上另一行的
倍数),将增广矩阵的左侧(原$M$的部分)化为上三角矩阵。所有计算，尤其是除法(被
替换为乘以模逆元),都在模 127 下进行。
3. 反向代入：从最后一行开始，逐行向上解出$x_{13},x_{12},\ldots,x_0$的值，最终得到完整的解向
量$x$,即$V_{input}$。

##### 关键数据提取

**a) 静态数据 `V_result`**

通过分析 `Main` 方法反编译后的 C# 代码，可以直接看到结果向量 `V_result` 是以 `new int[,] { {45}, {77}, ... }` 的形式硬编码在程序中的，我们直接将其提取用于解密脚本。


![[image-20250718193025911.png]]
**b) 动态数据 `SERIALIZED_BYTE_ARRAY`**

这是本实验最关键的步骤。我们使用 dnSpy 的调试功能来获取这个数据。

1. **设置断点：** 在 `GetSquare()` 方法的入口处设置方法断点。
2. **启动调试：** 启动程序，并输入一个**格式正确**且能**通过第二关（XOR/Base64校验）**的“半成品”Flag，以确保程序能执行到 `GetSquare()` 方法。
3. **提取数据：** 当程序在断点处暂停时，从“局部变量”窗口中找到 `byte[] array` 变量，其长度为 `0xC3` (195字节)。将其从内存中保存为文件 `array.bin`。




![[image-20250718185959874.png]]
编写脚本求解


![[image-20250718193114736.png]]
AAA{C#_Is_The_BestWYYWY}fW;0>?1>808}


![[image-20250718193253072.png]]


为了做这个bonus，我下载了parallels desktop和windows虚拟机，用我的mac干上了粗活TAT，装环境的痛苦比调试更大大大大
