# Checkin 
from base64即可解出
# Hidenworld
修改图片高度即可
![[Pasted image 20250830101735.png]]
![[Pasted image 20250830101802.png]]


# PyArmor
在破解过程中，遇到了几个关键障碍：
1. **PyArmor 动态加载机制**：无法通过静态分析直接获取源代码，必须在运行时进行解包。
2. **CPU 架构不匹配**：最核心的障碍。题目提供的 PyArmor 动态库 (`.dylib`) 是为 `x86_64` (Intel) 架构的 macOS 编译的，而我们的运行环境是 `arm64` (Apple M4) 架构的 macOS，导致本地环境无法直接加载该库。
3. **环境依赖与隔离**：尝试使用 `amd64` Docker (Linux) 环境解决了 CPU 架构问题，但又引入了新的操作系统不匹配问题（Linux 需要 `.so` 库而非 `.dylib`）。


#### **解题思路**

最终的成功路径是放弃 Docker 环境，回归 macOS 原生系统，通过模拟一个完全兼容的 Intel 环境来解决问题。

#####  1：环境搭建

- **核心工具**: Apple 的 **Rosetta 2** 转译层。
- **主要命令**:
    1. **安装 Intel 版本的 Homebrew** :
    `arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

    2. **使用 Intel 版 Homebrew 安装 Intel 版 Python 3.9**:
        ```
        arch -x86_64 /usr/local/bin/brew install python@3.9
        ```
        
    3. **创建并激活一个纯净的 x86_64 虚拟环境**:
        ```
        /usr/local/opt/python@3.9/bin/python3.9 -m venv venv-x86
        source venv-x86/bin/activate
        ```

##### **2：静态解包  获取纯净的 `.pyc` 文件**

在兼容的环境中，我们使用开源的 `PyArmor-Unpacker` 工具（Method 3）来执行静态解包，拦截 PyArmor 在内存中解密的代码。

- **核心工具**: `Svenskithesource/PyArmor-Unpacker` 项目中的 `bypass.py` 脚本。
- **主要命令**:
    ```
    # 在激活的 venv-x86 环境中执行
    python3 bypass.py aaa.py
    ```
    
    此命令成功运行后，会在 `dump/` 目录下生成 `aaa.pyc` 和 `hello.pyc`。
    
##### 步骤3 反汇编.pyc文件 
通过在线反汇编网站
https://pylingual.io/view_chimera?identifier=1d555d91a0597dafa25585797b6963c2b46b86589b7621a8780090401fa88a26
加入得到的aaa.pyc
得到
![[Pasted image 20250830121134.png]]
```python
# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: <frozen aaa>
# Bytecode version: 3.9.0beta5 (3425)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import hello
import base64
flag = b'WkpVQ1RGe3B5dGhvbl90cjRjM18xU19mdV5eeX0='
your_flag = input('please input your flag: ')
if your_flag.encode() == base64.b64decode(flag):
    print('success!')
else:
    print('wrong!')
```


from base64即可得到
ZJUCTF{python_tr4c3_1S_fu^^y}

参考项目
https://github.com/Svenskithesource/PyArmor-Unpacker


bypass.py的主要思路为
1.  **注册审计钩子 (Registering the Audit Hook)**
    脚本利用 `sys.addaudithook` 建立一个针对 `marshal.loads` 事件的全局回调函数。PyArmor 在执行加密脚本时，会使用 `marshal.loads` 将其主代码块从字节流加载到内存中，这为我们提供了一个稳定且精确的初始拦截点。

2.  **拦截并修改引导代码 (Intercepting and Modifying the Bootstrap Code)**
    当钩子被触发时，回调函数会接收到 PyArmor 的顶层代码对象（Top-level Code Object）。此代码对象是 PyArmor 的一个保护性包装层（Protective Wrapper），其任务是调用原生解密函数 `__armor_enter__`。脚本在内存中对此代码对象的字节码（`co_code`）进行篡改：它精确定位到调用 `__armor_enter__` 后的 `POP_TOP` 操作码，并将其替换为 `RETURN_VALUE` 操作码。

3.  **执行篡改代码并捕获载荷 (Executing the Tampered Code and Capturing the Payload)**
    篡改后的代码对象被临时执行。当 `__armor_enter__` 函数在原生层解密出真正的应用程序代码（Payload Code Object）并将其推送到解释器栈顶时，原应执行的 `POP_TOP`（丢弃）操作被替换为了 `RETURN_VALUE`（返回）。通过这种方式，我们劫持了正常的执行流，使得**解密后的核心代码对象**被作为函数的返回值捕获，而非被直接执行。

4.  **代码对象重构与持久化 (Code Object Refactoring and Persistence)**
    成功捕获核心代码对象后，脚本会对其进行“净化处理”。这包括：
    * **剥离包装层**：移除所有 PyArmor 添加的包装字节码，例如 `SETUP_FINALLY` 块。
    * **修正跳转偏移**：由于代码长度发生改变，脚本会遍历所有绝对跳转指令（如 `JUMP_ABSOLUTE`），重新计算并修正其操作数（oparg），以保证代码的逻辑完整性。
    * **持久化存储**：最终，这个完全净化和修复的代码对象被重新序列化，并按照标准的 `.pyc` 文件格式（包含魔数和时间戳）写入磁盘，以便后续进行静态分析。

5.  **终止执行 (Terminating Execution)**
    在将干净的 `.pyc` 文件成功写入磁盘后，脚本会调用 `os.kill` 立即终止当前进程。这是一个关键步骤，旨在防止原始的、受保护的代码逻辑在我们的载荷提取操作完成后继续执行。


# babysteg
打开到最后
![[Pasted image 20250830125212.png]]
frombase64得到 CSACTF{1T_SEeMs_L1kE_4_fL49}
但是这个是错的，一下没思路最后没时间解了（（））



## ezCrypto
### 问题分析

目标是解密密文 `c` 以获得原始信息 `secret`。我们先来梳理一下给出的信息和加密过程：

1.  **目标**: 找到 `secret`，它被转换成了一个大整数 `m`。所以我们的核心任务是求出 `m`。
2.  **加密函数 `encrypt`**:
    * 生成两个512位的素数 `p` 和 `q`。
    * 计算模数 `N = p * q`。这是标准的 RSA 模数。
    * 生成了两个特殊的密文 `c1` 和 `c2`：
        * `c1 = pow((7 * p + 2 * q), e1, N)`
        * `c2 = pow((5 * p + 3 * q), e2, N)`
        这里的底数是 `p` 和 `q` 的线性组合，指数 `e1` 和 `e2` 是两个给定的非常大的数。
    * 对明文 `m` 进行标准的 RSA 加密：
        * `c = pow(m, e, N)`，其中 `e = 65537` 是一个常见的公钥指数。
    * 函数返回了 `c, c1, c2, N`。

3.  **我们拥有的数据**: `c`, `c1`, `c2`, `N`, 以及两个大指数 `e1`, `e2` 和公钥指数 `e`。

4.  **核心障碍**: 要解密 `c`，我们需要私钥 `d`。为了计算 `d`，我们需要欧拉函数 `phi(N) = (p-1)(q-1)`。而要计算 `phi(N)`，我们必须知道 `p` 和 `q`。因此，整个问题的关键就变成了：**如何利用给定的 `c1`, `c2`, `N`, `e1`, `e2` 来求出 `p` 和 `q`？**

### 思路
突破口在于 `c1` 和 `c2` 的特殊构造。它们包含了关于 `p` 和 `q` 的信息。直接从 `c1` 和 `c2` 的表达式中求解 `p` 和 `q` 是非常困难的，因为它们被包裹在模幂运算中，并且指数 `e1`, `e2` 不同。

这里的关键技巧是利用模运算的性质，在 `mod p` 或 `mod q` 的环下简化表达式。

**第一步：在 `mod p` 环下分析**

我们知道 `N = p * q`，所以 `N` 可以被 `p` 整除，即 $N \equiv 0 \pmod{p}$。
同时，任何数乘以 `p` 在模 `p` 下也为 0，即 $kp \equiv 0 \pmod{p}$。

将这个性质应用到 `c1` 和 `c2` 的底数上：
* $7p + 2q \equiv 7 \cdot 0 + 2q \equiv 2q \pmod{p}$
* $5p + 3q \equiv 5 \cdot 0 + 3q \equiv 3q \pmod{p}$

现在，`c1` 和 `c2` 的原始定义（在 `mod N` 下）也自然地在 `mod p` 下成立：
* $c_1 \equiv (7p + 2q)^{e_1} \equiv (2q)^{e_1} \equiv 2^{e_1} \cdot q^{e_1} \pmod{p}$
* $c_2 \equiv (5p + 3q)^{e_2} \equiv (3q)^{e_2} \equiv 3^{e_2} \cdot q^{e_2} \pmod{p}$

**第二步：消去未知量 `q`**

我们现在有两个关于未知量 `q` 的同余方程。为了消去 `q`，我们需要让 `q` 的指数变得相同。一个直接的方法是：
1.  将第一个同余方程两边取 `e2` 次方。
2.  将第二个同余方程两边取 `e1` 次方。

得到：
* $c_1^{e_2} \equiv (2^{e_1} \cdot q^{e_1})^{e_2} \equiv 2^{e_1 e_2} \cdot q^{e_1 e_2} \pmod{p}$
* $c_2^{e_1} \equiv (3^{e_2} \cdot q^{e_2})^{e_1} \equiv 3^{e_1 e_2} \cdot q^{e_1 e_2} \pmod{p}$

现在两个方程中都含有 $q^{e_1 e_2}$ 项。我们可以通过代换来消去它。从第一个方程，我们可以得到 $q^{e_1 e_2} \equiv c_1^{e_2} \cdot (2^{e_1 e_2})^{-1} \pmod{p}$。代入第二个方程会比较复杂。

一个更简洁的方法是交叉相乘来构造一个等式：
我们将第一个方程乘以 $3^{e_1 e_2}$，第二个方程乘以 $2^{e_1 e_2}$：
* $c_1^{e_2} \cdot 3^{e_1 e_2} \equiv (2 \cdot 3)^{e_1 e_2} \cdot q^{e_1 e_2} \pmod{p}$
* $c_2^{e_1} \cdot 2^{e_1 e_2} \equiv (3 \cdot 2)^{e_1 e_2} \cdot q^{e_1 e_2} \pmod{p}$

由于两个方程的右边完全相同，因此它们的左边在模 `p` 意义下也必然相等：
$$c_1^{e_2} \cdot 3^{e_1 e_2} \equiv c_2^{e_1} \cdot 2^{e_1 e_2} \pmod{p}$$
将所有项移到一边：
$$c_1^{e_2} \cdot 3^{e_1 e_2} - c_2^{e_1} \cdot 2^{e_1 e_2} \equiv 0 \pmod{p}$$

**第三步：利用最大公约数（GCD）求出 `p`**

上面这个同余式告诉我们，整数 $K = c_1^{e_2} \cdot 3^{e_1 e_2} - c_2^{e_1} \cdot 2^{e_1 e_2}$ 是 `p` 的一个倍数。
我们同时还知道，`N` 也是 `p` 的一个倍数 ($N=p \cdot q$)。

因此，`p` 是 `K` 和 `N` 的一个公因子。因为 `p` 是一个大素数，我们有很大概率可以通过计算最大公约数（GCD）来找到它：
$$p = \text{gcd}(K, N)$$

然而，`K` 的值会非常巨大，直接计算是不可行的。这里需要运用 GCD 的一个重要性质： $\text{gcd}(a, n) = \text{gcd}(a \pmod{n}, n)$。
所以，我们可以先计算 `K` 对 `N` 取模的结果，然后再求 GCD：
$$p = \text{gcd}(K \pmod{N}, N)$$

$K \pmod{N}$ 是可以高效计算的。我们可以使用模幂运算（`pow(base, exp, mod)`）来计算它的各个部分：
$K \pmod{N} = ( (c_1^{e_2} \pmod{N}) \cdot (3^{e_1 e_2} \pmod{N}) - (c_2^{e_1} \pmod{N}) \cdot (2^{e_1 e_2} \pmod{N}) ) \pmod{N}$

其中，像 $3^{e_1 e_2} \pmod{N}$ 这样的项可以分步计算以防止指数溢出：$3^{e_1 e_2} = (3^{e_1})^{e_2}$，所以可以先算 `t = pow(3, e1, N)`，再算 `pow(t, e2, N)`。

**第四步：完成解密**

一旦我们通过 GCD 计算出了 `p`，后续步骤就水到渠成了：
1.  计算另一个素因子：$q = N / p$。
2.  计算欧拉函数：$\phi(N) = (p-1)(q-1)$。
3.  计算私钥 `d`，即 `e` 在模 $\phi(N)$ 下的乘法逆元：$d = e^{-1} \pmod{\phi(N)}$。
4.  使用私钥 `d` 解密密文 `c`：$m = c^d \pmod{N}$。
5.  将大整数 `m` 转换回字节形式，即可得到 `secret`。

至此，我们已经拥有了破解此密码的完整数学思路。


### ezrsa
part1
**问题分析**：典型的RSA，提供了模数 $N$、公钥指数 $e$、以及一个密文 $c$。常规的RSA解密需要私钥 $d$ 或者 $p$ 和 $q$ 的值。此题的关键在于给出了一个非常规的线索：`d - p` 的值。这里的 $d$ 是私钥指数，$p$ 是构成 $N$ 的其中一个素数因子。我们的目标就是利用 $N, e, c$ 以及 $d-p$ 这个泄露的信息来分解 $N$，从而求得私钥并解密。

**求解思路**：
我们拥有以下已知信息和关系：
1.  泄露值：$L = d - p$
2.  RSA基本关系：$e \cdot d \equiv 1 \pmod{\phi(N)}$，即存在一个整数 $k$，使得 $e \cdot d - k \cdot \phi(N) = 1$。
3.  欧拉函数：$\phi(N) = (p-1)(q-1) = N - p - q + 1$。
4.  模数定义：$N = p \cdot q$，因此 $q = N/p$。

我们的策略是将这些关系式联立起来，构造一个只包含一个未知数（比如 $p$）的方程。
从 $L = d - p$ 我们可以得到 $d = L + p$。将这个表达式代入到关系式(2)中：
$e \cdot (L + p) - k \cdot \phi(N) = 1$
接着，将 $\phi(N)$ 的表达式代入：
$e \cdot (L + p) - k \cdot (N - p - q + 1) = 1$
为了消去变量 $q$，我们使用 $q = N/p$ 代入：
$e \cdot (L + p) - k \cdot (N - p - N/p + 1) = 1$
这个方程中现在只剩下两个未知数：$p$ 和 $k$。$p$ 是一个1024位的素数，直接求解非常困难。但是，我们可以观察到 $k$ 的性质。由于 $e \cdot d \approx k \cdot N$ 且 $e$ 相对较小 ($e = 65537$)，$k$ 的值通常也会是一个小整数，并且很有可能小于 $e$。因此，我们可以通过遍历一个合理范围内的 $k$ 值来求解 $p$。

我们将上述方程整理成关于 $p$ 的一元二次方程。首先，将方程两边同乘以 $p$ 以消除分母：
$p \cdot (e(L+p)) - k \cdot (Np - p^2 - N + p) = p$
展开并整理各项，得到 $A p^2 + B p + C = 0$ 的形式：
$(e+k)p^2 + (eL - 1 - k(N+1))p + kN = 0$
现在，我们可以遍历 $k$（从1开始），对于每一个 $k$，计算出二次方程的系数 $A, B, C$。然后，利用求根公式 $p = \frac{-B \pm \sqrt{B^2 - 4AC}}{2A}$ 求解 $p$。我们需要检查判别式 $\Delta = B^2 - 4AC$ 是否为一个完全平方数。如果找到了一个 $k$ 使得 $\Delta$ 是完全平方数，我们就能计算出 $p$ 的整数解。得到 $p$ 后，通过 $N \pmod p == 0$ 来验证其是否为 $N$ 的一个因子。一旦找到正确的 $p$，就能计算出 $q=N/p$，进而求得 $\phi(N)$ 和私钥 $d$，最终解密密文。
```python

from Crypto.Util.number import long_to_bytes

# --- Part 1 ---
print("--- Solving Part 1 ---")

# Provided values from the first challenge
d_minus_p = 2551756296230556455153461142256558662892670316950235756205055813974596327809845104526723991103791519643650309481773430116596445056621314003219883178059757998882818276435859354707327583130042659575327825768326628051521469996692935342698707595506169488367250369701727437051651180572487178040011110411554700942787226887828691419928759312983854249497569715361729302927781514981880654479059321530075054979991662440146179410101287675885973372091690923001774040638576268604000902523671010492732048209337569176535938725020523648350397601225455506699505240572770233601345289329527790660324779363188244080506367846538941254260
c1 = 15971309396256835362531485951128166983206687537714027537858621542505837518266962953113283078076889299992766766084018288988406699208913051384679790264007098624219450206475206014672536932788204025908959226423862863105445190794751238955057213166812828836859124836604576681535267728522357997298297456365207788184878644031601919916837973507434190104725947258940723229288878807644645051813848097692257981034447284379832096671294140741904947037566307085602107241375721489415120904300455359620297677533606229298114263489015021336257788565359759312693790170999715775553831478938083873456866209473156243356364882697055947038033
N1 = 17154010912510203959523272425896818657297869993021602292995255193399642992683743831712781844801434487935779088368754260903824107054650841709818595121602457685176250013619541956042068706082019261523054643284318619613556526738461883634674858927755444636283155962574839577603247863491547049667474422304037381854670052998349971200044078692166792550323925980836302324144231971216224668698971348394532478457497878076908606080048700669391473735992839985369965723367504239067817263161028103823044373957891549372409108859137498344836594151291454836621683376821160950429180536440623985341901524194163420366533633759132239742143

e = 0x10001
L = d_minus_p

# Define the ring of polynomials in variable 'x' over the Integers
P.<x> = PolynomialRing(ZZ)

# Iterate over possible small values of k
for k in range(1, e):
    # Coefficients of the quadratic equation: (e+k)p^2 + (eL - 1 - k(N+1))p + kN = 0
    A = e + k
    B = e*L - 1 - k*(N1 + 1)
    C = k*N1
    
    # Calculate the discriminant
    delta = B^2 - 4*A*C
    
    # Check if the discriminant is a perfect square
    if delta >= 0 and is_square(delta):
        sqrt_delta = isqrt(delta)
        
        # Denominator must not be zero
        if (2*A) != 0:
            # Check the first root
            if (-B + sqrt_delta) % (2*A) == 0:
                p_candidate = (-B + sqrt_delta) // (2*A)
                if p_candidate != 0 and N1 % p_candidate == 0:
                    p1 = p_candidate
                    q1 = N1 // p1
                    phi1 = (p1 - 1) * (q1 - 1)
                    d1 = inverse_mod(e, phi1)
                    m1 = pow(c1, d1, N1)
                    flag1 = long_to_bytes(m1)
                    print(f"Found k = {k}")
                    print(f"p = {p1}")
                    print(f"Flag part 1: {flag1.decode()}")
                    break # Exit loop once solution is found
            
            # Check the second root
            if (-B - sqrt_delta) % (2*A) == 0:
                p_candidate = (-B - sqrt_delta) // (2*A)
                if p_candidate != 0 and N1 % p_candidate == 0:
                    p1 = p_candidate
                    q1 = N1 // p1
                    phi1 = (p1 - 1) * (q1 - 1)
                    d1 = inverse_mod(e, phi1)
                    m1 = pow(c1, d1, N1)
                    flag1 = long_to_bytes(m1)
                    print(f"Found k = {k}")
                    print(f"p = {p1}")
                    print(f"Flag part 1: {flag1.decode()}")
                    break # Exit loop once solution is found
                    
print("\n" + "="*40 + "\n")
```



part2**问题分析**：
这道题同样是RSA密码体制，但提供了不同的线索。这次没有直接泄露私钥信息，而是在素数 $p$ 和 $q$ 的生成过程中给出了一个强关联。具体来说，$q$ 是 `p ^ ((1 << 900) - 1)` 之后紧邻的下一个素数。这里的 `^` 是异或操作，`(1 << 900) - 1` 是一个由900个二进制1组成的数。这意味着 $p$ 和 $q$ 的关系非常特殊：$p$ 和 $q$ 的高位比特是相同的。$p$ 是一个1024位的素数，异或操作只影响了其低900位，因此它们的前 $1024 - 900 = 124$ 位是完全相同的。利用这个“高位比特共享”的特性，我们可以有效地分解模数 $N$。

**求解思路 ：

我们的核心策略是利用 $p$ 和 $q$ 之间的精确代数关系，而不是进行模糊的近似估算。

1.  **分解素数结构**
    我们知道 $p$ 和 $q$ 共享高124位。设 $K = 2^{900}$，我们可以将 $p$ 和 $q$ 表示为：
    $p = A \cdot K + B_p$
    $q = A \cdot K + B_q$
    其中 $A$ 是共享的124位高位部分，$B_p$ 和 $B_q$ 是各自的、小于 $K$ 的900位低位部分。

2.  **确定高位 A**
    我们将 $p$ 和 $q$ 的表达式代入 $N = p \cdot q$ 并展开：
    $N = (A \cdot K + B_p)(A \cdot K + B_q) = A^2 K^2 + AK(B_p + B_q) + B_p B_q$
    由于 $A^2 K^2$ 是绝对主导项，我们可以通过 $A \approx \sqrt{N / K^2} = \sqrt{N \gg 1800}$ 来估算 $A$。因为整数开方会向下取整，真实的 $A$ 只可能是 $A_{guess} = \text{isqrt}(N \gg 1800)$ 或 $A_{guess} + 1$。
    我们可以通过一个简单验证来确定正确的 $A$：由于 $A, K, B_p, B_q$ 均为正数，那么 $N - A^2 K^2 = AK(B_p + B_q) + B_p B_q$ 的结果也必须为正。如果一个候选的 $A$ 值导致 $N - A^2 K^2 < 0$，则该 $A$ 值过大，可以排除。

3.  **建立低位部分 (B_p, B_q) 的精确关系**
    这是解题的关键。我们不能像之前那样忽略 $B_p B_q$ 项，而是要利用题目给出的素数生成方式：
    $q = \text{next prime}(p \oplus (K-1))$
    这意味着 $q$ 非常接近 $p \oplus (K-1)$。令这个微小的差值为 $\delta$ (prime gap)，则：
    $q \approx p \oplus (K-1) = (A \cdot K + B_p) \oplus (K-1) = A \cdot K + (B_p \oplus (K-1))$
    所以 $q = A \cdot K + (B_p \oplus (K-1)) + \delta$。
    对比 $q = A \cdot K + B_q$，我们得到 $B_q = (B_p \oplus (K-1)) + \delta$。

    $B_p \oplus (K-1)$ 是对 $B_p$ 的低900位进行按位取反（我们记作 $\sim B_p$）。而一个数与它按位取反的结果相加，恒等于全1的掩码，即 $B_p + (\sim B_p) = K-1$。
    因此，我们可以得到 $B_p$ 和 $B_q$ 之和 $S_B$ 的精确表达式：
    $S_B = B_p + B_q = B_p + (\sim B_p + \delta) = (B_p + \sim B_p) + \delta = (K-1) + \delta$

4.  **求解 B_p 和 B_q**
    现在我们有两个关于 $B_p, B_q$ 的方程：
    (a) $N - A^2 K^2 = A \cdot K \cdot S_B + P_B$  (其中 $S_B = B_p+B_q, P_B = B_p B_q$)
    (b) $S_B = (K-1) + \delta$

    我们的求解步骤如下：
    * 首先确定正确的 $A$。
    * 由于 $\delta$ 是一个很小的整数，我们可以从 $\delta=0, 1, 2, ...$ 开始进行迭代搜索。
    * 对于每一个 $\delta$，我们计算出候选的 $S_B = (K-1) + \delta$。
    * 将 $A$ 和 $S_B$ 代入方程(a)，解出候选的 $P_B = (N - A^2 K^2) - A \cdot K \cdot S_B$。
    * 现在我们同时知道了 $B_p$ 和 $B_q$ 的和 ($S_B$) 与积 ($P_B$)，它们是二次方程 $y^2 - S_B \cdot y + P_B = 0$ 的两个根。
    * 我们计算该方程的判别式 $\Delta = S_B^2 - 4P_B$，如果 $\Delta$ 是一个完全平方数，我们就能解出整数 $B_p$ 和 $B_q$。

5.  **验证和解密**
    得到 $B_p$ 后，重构 $p = A \cdot K + B_p$，并验证 $N \pmod p == 0$。验证成功即表明分解完成，之后就可以计算私钥并解密密文了。
```python
# Sagemath v9.0+
# (请确保第一部分的变量 flag1 仍然在环境中)

from Crypto.Util.number import long_to_bytes, bytes_to_long

print("--- 正在求解第二题 (最终修正版) ---")

# --- 第二题的已知数据 ---
n2_hex = "0x979b0d5014e3e0b01091d5cd145c5c62f027da4592f71dbbcf114e9e94d56632832fb57a0e27d581bd86be6ef5a019781edef8e35dab664eb46efa67bdcf1b3abf5de2f21d125d6559493d7b7460f33387fc1c38329fd60c9e69803f74bb645cf11d674585b86ad9c966d0ca6fafdcf8c0c7eaddca396ab5b3a21a8ae261fa7e1915f618593352f2d7efd8eba8d1fd80074fbd66999e86bc8417761daecf2a9c446a9db93e691f277cffe870d2b781c305a9ceb71bd4191cb733f6377b7d123aa7e86e0519b484e347fb0307fc468c8006a66452a5ae90046a43ecb17fe4480aa39ca7674cbd88d837c0902c32a109b67a3d91e5ffa4cd3fbeaf305335fae207"
c2_hex = "0x82f76dce83c5156bfb205e173372c9bc074155f0548975b0bd1ea4b258e2262e8612a29331602f952e598439c6651b27d7d75822040101994fcae8120f3fe5cc2df49f221843dd02c1b14c91ea24ad51cdf7cbcd8e4961c2e03045642257365dfabeb873de2a7ea4c1e1c69e975d644fa015f0dbb149bbe99b7c592465ae5effd3cc0405ebe7dde2ec401d19d73d4c41259fc7823c060af95c20e3f553b075b7a29af786957917a45bcf5ac9196ddb87e3e78bf63f9b9d705676759effe111301b8b23d8f4aeafd8f5a337a7cc982ed306f0fb2132078a8da3de543ad14a15d74c9cc19a4a57818f9611681e023919da1832dc883d1bac97130c4dbb7b60dda"
n2 = ZZ(n2_hex)
c2 = ZZ(c2_hex)
e = 0x10001

# --- 常量定义 ---
low_bits = 900
K = 2**low_bits
M = K - 1 # XOR操作的掩码，即900个1

# --- 求解过程 ---
A_initial_guess = isqrt(n2 >> (2 * low_bits))
found_flag = False

# 依次测试 A 的两种可能性
for A in [A_initial_guess, A_initial_guess + 1]:
    print(f"\n--- 正在尝试 A = {A} ---")
    
    # 验证：R必须为正数，否则这个A就是错的
    R = n2 - (A * K)**2
    if R < 0:
        print("计算出的R为负数，此A值过大，跳过。")
        continue

    # 遍历小的prime gap (delta)，通常不会很大
    for delta in range(2000):
        # 根据 B_p + B_q = (K-1) + delta 计算低位之和 S_B
        S_B = M + delta
        
        # 根据 R = A*K*S_B + P_B 计算低位之积 P_B
        P_B = R - (A * K * S_B)

        # B_p 和 B_q 是二次方程 y^2 - S_B*y + P_B = 0 的根
        # 求解需要判别式为完全平方数
        delta_B = S_B**2 - 4*P_B
        if delta_B >= 0 and is_square(delta_B):
            sqrt_delta_B = isqrt(delta_B)
            # 求解 B_p
            if (S_B - sqrt_delta_B) % 2 == 0:
                B_p = (S_B - sqrt_delta_B) // 2
                
                # 重构 p 并验证
                p2 = A*K + B_p
                if n2 % p2 == 0:
                    q2 = n2 // p2
                    print(f"成功找到因子！delta = {delta}")
                    
                    # 解密
                    phi2 = (p2 - 1) * (q2 - 1)
                    d2 = inverse_mod(e, phi2)
                    m2 = pow(c2, d2, n2)
                    flag2 = long_to_bytes(m2)
                    
                    print(f"第二部分 flag: {flag2.decode()}")
                    
                    # 组合最终flag (假设第一部分的flag1已解出)
                    # 如果flag1不在环境中，你需要先运行第一部分的代码
                    try:
                        flag1_str = flag1.decode()
                        print("\n--- 最终 FLAG ---")
                        print(flag1_str + flag2.decode())
                    except NameError:
                        print("\n错误: 变量 'flag1' 未定义。请先运行第一部分解密代码。")

                    found_flag = True
                    break # 已找到解，跳出delta循环
    
    if found_flag:
        break # 已找到解，跳出A的循环
```
最终flag{117699abef7d1e592d8cfae5fbb6fe7}







## babyRev

这道题的核心逻辑是对用户输入的16位密码进行加密，然后与一个固定的密文进行比较。要找到正确的密码，我们需要逆向这个加密过程。

### 1\. 主程序逻辑 (`main` 函数)

`main` 函数在 `.text:00000000000014D3` 处。其主要流程如下：

1.  **调用 `sub_1209`**：打印欢迎信息，如 "Welcome to CSACTF 2025\!" 和 "plz input the correct password"。
2.  **调用 `sub_12D3`**：接收用户输入。
      * 此函数使用 `scanf` 以 `"%16s"` 格式读取输入，并存入全局变量 `src`。
      * 接着检查输入长度是否**严格等于16个字符** (`cmp rax, 10h`)。如果长度不符，程序会打印 "password length error" 并退出。
      * 最后，调用 `sub_1241` 处理输入。
3.  **调用 `sub_1439`**：这是核心的验证函数。它对 `sub_1241` 处理后的数据进行校验。
4.  **判断结果**：
      * 如果 `sub_1439` 返回非零值（成功），程序会打印 "password correct"，然后将用户输入的密码作为 flag 内容打印出来，格式为 `CSACTF{%s}`。
      * 如果返回零（失败），则打印 "password error" 并退出。

### 2\. 数据处理 (`sub_1241` 函数)

`sub_1241` 函数在 `.text:0000000000001241` 处。它的作用是将输入的16字节字符串 (`char[16]`) 转换为一个由四个32位无符号整数组成的数组 (`uint32_t[4]`)。转换方式如下（小端序）：

  * `v[0] = str[0] | str[1]<<8 | str[2]<<16 | str[3]<<24`
  * `v[1] = str[4] | str[5]<<8 | str[6]<<16 | str[7]<<24`
  * `v[2] = str[8] | str[9]<<8 | str[10]<<16 | str[11]<<24`
  * `v[3] = str[12] | str[13]<<8 | str[14]<<16 | str[15]<<24`

### 3\. 加密与验证 (`sub_134E` 和 `sub_1439` 函数)
`sub_1439` 函数在 `.text:0000000000001439` 处。
1.  **定义密钥**：函数内部定义了密钥字符串 `"this_isnot_a_key"`。
2.  **分块加密**：它将上一步转换得到的4个整数分成两组（`{v[0], v[1]}` 和 `{v[2], v[3]}`），每组8字节。
3.  **调用 `sub_134E` (加密函数)**：分别对这两个数据块进行加密。
4.  **比较密文**：将加密后的结果与硬编码在程序中的值进行比较。
      * 第一块加密结果应为：`{0xBC8BC8E3, 0x9069C8DB}`
      * 第二块加密结果应为：`{0x0731D6E5, 0x913AEACB}`

`sub_134E` 函数在 `.text:000000000000134E` 处。通过分析其内部结构，特别是循环次数（32次）和使用的魔数 `0x9E3779B9` (delta)，可以确定这是标准的 **TEA (Tiny Encryption Algorithm)** 加密算法。
### 4\. 逆向求解

既然我们知道了加密算法 (TEA)、密钥 (`"this_isnot_a_key"`) 和加密后的目标密文，我们就可以通过编写一个 TEA **解密**脚本来反推出原始的明文，也就是正确的密码。

Python 解密脚本

```python
import struct

def decrypt(v, k):
    """
    TEA (Tiny Encryption Algorithm) decryption function.
    
    Args:
        v (list): A list of two 32-bit unsigned integers (ciphertext).
        k (list): A list of four 32-bit unsigned integers (key).
        
    Returns:
        list: A list of two 32-bit unsigned integers (plaintext).
    """
    v0, v1 = v
    delta = 0x9e3779b9
    # sum_val starts at delta * 32 for decryption
    sum_val = (delta * 32) & 0xFFFFFFFF
    k0, k1, k2, k3 = k

    for _ in range(32):
        # Python integers don't automatically wrap like C unsigned integers,
        # so we use & 0xFFFFFFFF to simulate 32-bit arithmetic.
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + sum_val) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + sum_val) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        sum_val = (sum_val - delta) & 0xFFFFFFFF

    return [v0, v1]

# 1. Prepare the key by packing it into four 32-bit integers
key_str = b"this_isnot_a_key"
key = list(struct.unpack("<4I", key_str))

# 2. Define the target ciphertext blocks from the disassembly
ciphertext1 = [0xBC8BC8E3, 0x9069C8DB]
ciphertext2 = [0x0731D6E5, 0x913AEACB]

# 3. Decrypt each block
plaintext1 = decrypt(ciphertext1, key)
plaintext2 = decrypt(ciphertext2, key)

# 4. Combine the decrypted integers and unpack them back into a string
decrypted_dwords = plaintext1 + plaintext2
password = b"".join(struct.pack("<I", dword) for dword in decrypted_dwords)

# 5. Print the final result
password_str = password.decode('utf-8')
print(f"The correct password is: {password_str}")
print(f"The flag is: CSACTF{{{password_str}}}")

```

运行此脚本，输出结果为：

```
The correct password is: W0w_u_kN0w_t3A!!
The flag is: CSACTF{W0w_u_kN0w_t3A!!}
```