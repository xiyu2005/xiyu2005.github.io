---
title: lab2crypto
tags:
  - CTF
draft: false
---

# RSA Adventure

## Challenge1：利用中国剩余定理的广播攻击
```sh

    Hint:
    To get the flag, you need to solve a series of challenges, good luck!
    And please encode your input answers with HEX (remove '0x').
    
    
    [$] challenge 1
    [+] e = 0x3
    [+] n1 = 0x6e391e3924dba84d28ef7ee0b49a5ea9991591fbf3cce913ef4b4111cb3313f22b5f3d05433706617b4819ae205b21d586805628be9348dd27129a01eb91b2ff2d5134b96861789843f429d927bf24b020519c9937177a032d4a3c83686054de85a60a420ce8c9500a9706377f29b204032966e5fc17e7a2110642329e85d373
    [+] c1 = 0x641017a59ecc7dd0bbb89f9554e1354d9351fcc3eb37a1f51d53212cf10e2fed38cb44c028c010722c3a5129873d0d3a7d3d51a6d5a9083594848d7b2172fa5a51233dd54b2c8005a7ad6a302a90c3b896fd6608e72a89eaf8d0a461576de2373d6661b69227f0cdee590fcd107e764a9d3c5b6110df80837e16080a49b4e134
    [+] n2 = 0xdcddcd297c792915ea16fcee4830ca2b25671656816b2beaf459799bf7b4f8433a037519ef3c76610b391eb7ba29d46aaea0e592cb775abd866dcaa15892622640cb8b5ec610854022099374ec90b07a4d1c49e5c413935d812fe580ee1e91c2a0c93ed745f556beebdad54760b917e9ebe1a46a532daeb4aa293ea241bf8aa5
    [+] c2 = 0x334224784555d1e6f18fa758f5676fca7b758eace025f08ce462853efd2c30b69d669a130b3f4a5910b228667940ca2fcff4e7c2d0207a76a999bb6f03fcb955574e0500571177d69ba870ce81018ba8a34ee84e05e4a37753e3b88245560b2cff6fa445dd1e79ab669a2d46e037cc2a4bc87f810f83c6aea157a357962b2d1a
    [+] n3 = 0x8693c6a7c927b35e96a73cef38e9954d0094efbc5e5a94dcb2cb571f9e79341d6f80866917250966362fc1b63c55d23c87effa68120479286964773ec2005f25e1a0db6a4d13c9e3fd33c820ee14c1b5667033326f4537beb11fdb85ec590739b71a10129c918f5c66d637584156327d34bfbb1433f2a23d61b1b38134caf4bf
    [+] c3 = 0x16a35d89afa55f5bb1b738ff59f2a4e0b4a74c64996eeb3f320f67808da9b0fa0976a97889d8789aa1fc4fbc6e5f19b88097fd5ab050eaecf24efe169a1b317bdebca62e1a19a948391de32aeb8bdafb5efe5856311eb5f9917c397c85250250676659f580db6751355a8a30f3c7ceb5495488261d1eba1bf0d8f346673cb4a0
    [+] assert ci == pow(m, e, ni)
    [+] your job: guess m
    [-] m = 
```


### 挑战描述
服务器使用同一个低公钥指数 $e=3$ 对同一个明文 $m$ 进行了三次加密，但每次加密都使用了不同的、两两互质的模数 $n_1, n_2, n_3$。我们获得了三组密文和模数 $(c_1, n_1)$, $(c_2, n_2)$, $(c_3, n_3)$。

### 核心数学思路：哈斯塔德广播攻击 (Håstad's Broadcast Attack)
此攻击利用了中国剩余定理 (CRT)。已知以下同余关系：

$$
\begin{cases}
c_1 \equiv m^3 \pmod{n_1} \\
c_2 \equiv m^3 \pmod{n_2} \\
c_3 \equiv m^3 \pmod{n_3}
\end{cases}
$$

#### 攻击步骤：
1. **设未知数**：将 $m^3$ 视为整体未知数 $x$
2. **应用中国剩余定理**：
   - 计算 $N = n_1 \cdot n_2 \cdot n_3$
   - 通过CRT求解方程组，得到唯一解 $x_0$ 满足 $x_0 \equiv m^3 \pmod{N}$
3. **关键条件分析**：
   - 由于明文 $m$ 通常远小于每个模数 $n_i$，有 $m^3 < N$
   - 此时模运算失效，同余关系退化为整数等式：$m^3 = x_0$
4. **恢复明文**：
   - 计算整数立方根：$m = \sqrt[3]{x_0}$

> **核心条件**：$m < \min(n_1, n_2, n_3)$ 时攻击必然成功

```python
# --- 阶段二: Challenge 1 (CRT) ---
        log.info("解决 Challenge 1...")
        challenge1_data = io.recvuntil(b'[-] m = ', timeout=10).decode()
        c1 = int(re.search(r'c1 = (0x[0-9a-f]+)', challenge1_data).group(1), 16); n1 = int(re.search(r'n1 = (0x[0-9a-f]+)', challenge1_data).group(1), 16)
        c2 = int(re.search(r'c2 = (0x[0-9a-f]+)', challenge1_data).group(1), 16); n2 = int(re.search(r'n2 = (0x[0-9a-f]+)', challenge1_data).group(1), 16)
        c3 = int(re.search(r'c3 = (0x[0-9a-f]+)', challenge1_data).group(1), 16); n3_c1 = int(re.search(r'n3 = (0x[0-9a-f]+)', challenge1_data).group(1), 16)
        m1_cubed = chinese_remainder_theorem([c1, c2, c3], [n1, n2, n3_c1])
        m1, _ = gmpy2.iroot(m1_cubed, 3)
        io.sendline(hex(m1)[2:].encode())
```
## 第二关：e次根攻击

### 挑战描述
服务器给出了一个非标准的RSA加密，其公钥指数为偶数 $e=6$。同时提供了模数 $n$ 的质因子 $p$ 和 $q$，且明文 $m$ 的长度约为510位（远小于模数 $n$ 的1024位）。

### 核心数学思路：e次根攻击 (e-th Root Attack)
标准RSA要求 $e$ 与 $\phi(n)=(p-1)(q-1)$ 互质，但 $e=6$ 与偶数 $\phi(n)$ 不互质，无法计算私钥 $d$。
```sh
    Good!
    [$] challenge 2
    [+] m = getrandbits(510)
    [+] e = 0x6
    [+] p = 0x93583c8f314318f1887e4533d5f1662fad416584cf6c777c4b441af66615c198296a69c5d8943b47762a08eef859cc5264a972621f09e424357e9f7631647903
    [+] q = 0xdd4e2477b3b7446e10e91441422dad64bd9a623fefa64c4a21afe05e4d116c98e7731b40a9e8199821008c9c73042609476320d70f67d2c8069c7e9c9fd84561
    [+] c = 0x447c0179c5635456a7f4e9a3dda4142a0b3589fdbd5e146f7673e3c372e224f31a1bf134d47d14612855b875986c1198106ed47857895753a9a7db046eb8b320741fad6ccf266e6fa1726638c03da4191dffa011781efaee63fc9a8e2d932458e64a0960b4ef757d5c59311edd4aa461c1739a633a8f8c18fb97fd308be2ba15
    [+] assert c == pow(m, e, p*q)
    [+] your job: guess m
    [-] m = 
```
#### 攻击步骤：
1. **问题分解**：  
   将方程 $m^6 \equiv c \pmod{n}$ 分解为：
   $$
   \begin{cases}
   m^6 \equiv c \pmod{p} \\
   m^6 \equiv c \pmod{q}
   \end{cases}
   $$
2. **求解模素数方程**：
   - 模 $p$ 下解的数量：$\gcd(e, p-1)$
   - 模 $q$ 下解的数量：$\gcd(e, q-1)$
   - 计算解集 $S_p = \{m_p \mid m_p^6 \equiv c \pmod{p}\}$ 和 $S_q = \{m_q \mid m_q^6 \equiv c \pmod{q}\}$
3. **中国剩余定理组合**：
   - 遍历所有解对 $(m_p, m_q) \in S_p \times S_q$
   - 对每对解计算 $m \equiv \text{CRT}(m_p, m_q) \pmod{n}$
4. **筛选正确解**：
   - 利用明文长度约束（510位）
   - 保留满足 $2^{509} \leq m < 2^{510}$ 的唯一候选解

> **关键点**：当 $m^e < n$ 时可直接开根，但此处因 $e$ 与 $\phi(n)$ 不互质，必须通过分解模数求解

```python
log.info("解决 Challenge 2...")
        challenge2_data = io.recvuntil(b'[-] m = ', timeout=10).decode()
        p_c2 = int(re.search(r'p = (0x[0-9a-f]+)', challenge2_data).group(1), 16); q_c2 = int(re.search(r'q = (0x[0-9a-f]+)', challenge2_data).group(1), 16)
        e2 = int(re.search(r'e = (0x[0-9a-f]+)', challenge2_data).group(1), 16); c2_val = int(re.search(r'c = (0x[0-9a-f]+)', challenge2_data).group(1), 16)
        roots_p = sympy.nthroot_mod(c2_val, e2, p_c2, all_roots=True)
        roots_q = sympy.nthroot_mod(c2_val, e2, q_c2, all_roots=True)
        found_m2 = False
        for m_p in roots_p:
            for m_q in roots_q:
                candidate_m2 = chinese_remainder_theorem([m_p, m_q], [p_c2, q_c2])
                if 1 < candidate_m2.bit_length() <= 510:
                    io.sendline(hex(candidate_m2)[2:].encode()); found_m2 = True; break
            if found_m2: break
        if not found_m2: log.error("未能找到 Challenge 2 的解!"); io.close(); return
```
## 第三关：特殊模数 $n = p^2 \cdot q$ 攻击
```sh

    Good!
    [$] challenge 3
    [+] e = 0x3
    [+] n = 0x4a471ffda8b4d8d223f6b64884b798a8a8356e6d024f92c46a9171c8841b
    [+] c = 0x400ca790a7b3e90e64f3568bf6786060919d829fb44b7b94cab8c6db2bbb
    [+] assert c == pow(m, e, n)
    [+] your job: guess m
    [-] m = 
```

### 挑战描述
服务器给出了一个看似标准的RSA加密（公钥指数 $e=3$），但模数 $n$ 具有特殊结构 $n = p^2 \cdot q$（非标准的 $p \cdot q$）。
![[Pasted image 20250731143609.png]]
### 核心数学思路：修正欧拉函数 $\phi(n)$
标准 $\phi(n) = (p-1)(q-1)$ 不适用，需使用欧拉函数通用性质：

#### 欧拉函数修正：
| 性质 | 公式 |
|------|------|
| **积性性质** | 若 $a,b$ 互质，则 $\phi(a \cdot b) = \phi(a) \cdot \phi(b)$ |
| **素数幂性质** | $\phi(p^k) = p^k - p^{k-1}$ |

计算正确 $\phi(n)$：
$$
\phi(n) = \phi(p^2 \cdot q) = \phi(p^2) \cdot \phi(q) = (p^2 - p)(q - 1) = p(p-1)(q-1)
$$

#### 解密流程：
1. 计算修正后的欧拉函数：$\phi(n) = p(p-1)(q-1)$
2. 求私钥 $d$：
   $$
   d \equiv e^{-1} \pmod{\phi(n)}
   $$
3. 解密明文：
   $$
   m = c^d \pmod{n}
   $$

> **核心要点**：识别非标准模数结构是攻击成功的关键

```python
log.info("解决 Challenge 3...")
        challenge3_data = io.recvuntil(b'[-] m = ', timeout=10).decode()
        e3 = int(re.search(r'e = (0x[0-9a-f]+)', challenge3_data).group(1), 16); n3 = int(re.search(r'n = (0x[0-9a-f]+)', challenge3_data).group(1), 16)
        c3 = int(re.search(r'c = (0x[0-9a-f]+)', challenge3_data).group(1), 16)
        p3 = 800336709776908303690799; q3 = 800336709776908303691579
        assert n3 == p3 * p3 * q3
        phi3 = p3 * (p3 - 1) * (q3 - 1); d3 = inverse(e3, phi3); m3 = pow(c3, d3, n3)
        io.sendline(hex(m3)[2:].encode())
```

## 第四关：利用泄露的 $dp$ 值分解模数
```sh
Good!
[$] challenge 4
[+] e = 0x10001
[+] n = 0x81a8a5d31d394cf22be1279821b393cf40fc50bfee4720c5a37d4adcca081733d4386a528d156db3c8e9a464c1d16057e656af4fd9b23ec162b2732758646f62c7349ddf384d415b177e7e4f9177d381da8ba389ea19c86baad6d4e18095cdb8221117260d7bb790bc8b5a8902022dc4f4614be72709d382be0f185ed474805b
[+] dp = 0x46b50ee343445e826f0405f22a61902efeed47dd29e69b351ccb0e7d6377981c29dc6277a98934375f50de7309299fe92772110f855ee0d3af948185ee473c17
[+] c = 0x3ea96c823ec07714db8da4f3d8b8cdabf6f4cbb317a60cb4af5901ac01bbe299557dccae797291d63dd72705ef5b0cbc729b795d56559d782c21ae8941bf18de81498558c04098475c194107eaa48b52ce3255109440debf3e22d51132a22ac9e85b0c22ec0dbc464264e603e80dbdf23257a482438908d02d20efbd2958094e
[+] assert dp == d%(p-1)
[+] assert c == pow(m, e, n)
[+] your job: guess m
```

### 挑战描述
服务器提供标准RSA加密（$e = 0x10001$），额外泄露 $dp = d \mod (p-1)$，已知 $n$ 和 $c$。

### 核心数学思路：通过 $dp$ 恢复质因子 $p$
利用 $dp$ 与RSA参数的数学关系分解 $n$：

#### 关键关系推导：
1. **基础同余式**：
   $$
   e \cdot d \equiv 1 \pmod{\phi(n)} \quad \text{且} \quad \phi(n) = (p-1)(q-1)
   $$
2. **模 $p-1$ 约简**：
   - 因 $\phi(n)$ 是 $p-1$ 的倍数
   - 代入 $d \equiv dp \pmod{p-1}$ 得：
   $$
   e \cdot dp \equiv 1 \pmod{p-1}
   $$
3. **存在整数 $k$**：
   $$
   e \cdot dp - 1 = k \cdot (p-1)
   $$

#### 攻击实现：
| 步骤 | 操作 |
|------|------|
| **1. 暴力搜索 $k$** | 从 $k=1$ 开始递增尝试（实践中 $k$ 通常很小） |
| **2. 计算 $p$ 候选值** | $p_{\text{candidate}} = \dfrac{e \cdot dp - 1}{k} + 1$ |
| **3. 验证因子** | 检查 $n \mod p_{\text{candidate}} = 0$ 是否成立 |
| **4. 分解 $n$** | 成功时 $q = n / p$ |

> **实验观察**：在本挑战中 $k = e$ 时即找到有效 $p$

#### 后续解密：
成功分解 $n$ 后，按标准RSA流程解密：
1. 计算 $\phi(n) = (p-1)(q-1)$
2. 求 $d \equiv e^{-1} \pmod{\phi(n)}$
3. 计算 $m = c^d \pmod{n}$
单独的解密脚本为
```python
from Crypto.Util.number import inverse, long_to_bytes

def main():
    # --- 静态加载 Challenge 4 的所有参数 ---
    e_hex = '10001'
    n_hex = '81a8a5d31d394cf22be1279821b393cf40fc50bfee4720c5a37d4adcca081733d4386a528d156db3c8e9a464c1d16057e656af4fd9b23ec162b2732758646f62c7349ddf384d415b177e7e4f9177d381da8ba389ea19c86baad6d4e18095cdb8221117260d7bb790bc8b5a8902022dc4f4614be72709d382be0f185ed474805b'
    dp_hex = '46b50ee343445e826f0405f22a61902efeed47dd29e69b351ccb0e7d6377981c29dc6277a98934375f50de7309299fe92772110f855ee0d3af948185ee473c17'
    c_hex = '4e51c96b8bd862128c125d67588f7d3b9bb32c4ca45d37e4d18e378588d83e7f73b346a483ea89385d5c503d2e4e48d4b1f001c6d4de1ddbd3ddb5289665db64033cf236ed8c2da55e7410411904d8e3f523789871c7a91f145c52ad2e74ab36e59565250946a9fc8bf77d81a0a24a20f8743e4ee84da43d385eed33fe948224'

    e = int(e_hex, 16)
    n = int(n_hex, 16)
    dp = int(dp_hex, 16)
    c = int(c_hex, 16)

    print("[*] Challenge 4: dp 泄露攻击")
    print(f"    e = {e}")
    print(f"    n = {hex(n)}")

    # --- 1. 通过爆破 k 来分解 n ---
    print("\n[*] 正在搜索 k in e*dp - 1 = k*(p-1)...")
    p, q = 0, 0
    multiple = e * dp - 1
    
    # 扩大 k 的搜索范围，一个常见的技巧是 k 可能等于 e
    # 我们搜索到 e+10 确保能覆盖到
    for k in range(1, e + 10):
        if multiple % k == 0:
            p_candidate = (multiple // k) + 1
            # 检查候选p是否为n的因子
            if p_candidate > 1 and n % p_candidate == 0:
                p = p_candidate
                q = n // p
                print(f"[+] 成功找到因子! k = {k}")
                print(f"    p = {p}")
                print(f"    q = {q}")
                break

    if p == 0:
        print("[-] 在扩大的范围内仍然未能分解 n。")
        return

    # --- 2. 标准RSA解密 ---
    print("\n[*] 正在执行标准RSA解密...")
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    m = pow(c, d, n)
    print("[+] 解密成功。")

    # --- 3. 按要求进行双重验证 ---
    print("\n[*] 正在执行最终验证...")
    # 验证 dp
    dp_calculated = d % (p - 1)
    assert dp == dp_calculated, f"dp 验证失败! 得到 {dp_calculated}, 期望 {dp}"
    print("    [✓] assert dp == d%(p-1)  -- 验证通过")

    # 验证明文
    assert pow(m, e, n) == c, "明文验证失败!"
    print("    [✓] assert c == pow(m, e, n) -- 验证通过")

    # --- 4. 输出最终结果 ---
    print("\n" + "="*50)
    print(f"最终明文 m (十进制): {m}")
    m_hex = hex(m)[2:]
    print(f"用于提交的HEX字符串: {m_hex}")
    print("="*50)

if __name__ == '__main__':
    main()
```

```sh
Good!
[$] challenge 5
[+] n = 0xb3eaacc65bf88213e2a641130ae0c382fb2682794e62385f9944f9ff7356bbe2b057226747f38e177cb758888297c7f843f95dda1f5831d2e8ce48256604d11b45fc9010cbd183ee646bf6c687792284bbf029b7abc9e53b87d66a9ef15dd982ac7fa73d99fdd6baaf512bd735b64e2fb2ca29d2bc2e250ae2f9322ece30424b
[+] 1. server's job: print hex(pow(m, k, n) * pow((m+k), k, n) % n) \# k is your input (k>0)
[+] 2. your job: guess m
[-] your choice: 
```

服务器的计算函数为：
$$C(k) = \left( (m(m+k)) \pmod n \right)^k \pmod n$$
我们的目标是在不知道 `m` 和 `n` 的因子的情况下，通过选择 `k` 并分析返回的 `C(k)` 来求解 `m`。


单一的 `k` 值（如 `k=1` 或 `k=n-1`）会导向需要对合数 `n` 进行模平方根或模逆元的计算，而这些计算在 `n` 的因子未知时是不可行的。因此，正确的策略是**使用多个 `k` 值，建立一个方程组，通过代数消元来求解 `m`**。

我们选择最简单的两个正整数 `k=1` 和 `k=2`。

###  建立方程组

#### 情况一：当 $k = 1$

服务器返回 $C₁$。代入公式得到：
$$C_1 \equiv m(m+1) \pmod n$$
$$C_1 \equiv m^2 + m \pmod n \quad \cdots\quad (式 \, 1)$$

#### 情况二：当 $k = 2$

服务器返回 $C₂$。代入公式得到：
$$C_2 \equiv (m(m+2))^2 \pmod n$$
$$C_2 \equiv (m^2 + 2m)^2 \pmod n \quad \cdots\quad (式 \, 2)$$

### 代数求解

### 第一步：定义中间未知数

从 `方程式 2` 中，我们可以看到 $m^2 + 2m$ 是 $C₂$ 的一个模平方根。我们定义一个中间变量 $y$ 来表示这个值：
$$y \equiv \sqrt{C_2} \pmod n$$
于是，`方程式 2` 可以写成：
$$y \equiv m^2 + 2m \pmod n \quad \cdots\quad (式 \, 3)$$
此时，$y$ 对我们来说是未知的，但它成为了连接两个方程的关键桥梁。

### 第二步：用 $y$ 和 $C₁$ 表示 $m$

现在我们有两个形式更简单的方程：
- $m^2 + m \equiv C_1 \pmod n$ (来自 `式 1`)
- $m^2 + 2m \equiv y \pmod n$ (来自 `式 3`)

用后者减去前者：
$$(m^2 + 2m) - (m^2 + m) \equiv y - C_1 \pmod n$$
这给出了 $m$ 的一个简洁表达式：
$$m \equiv y - C_1 \pmod n \quad \cdots\quad (式 \, A)$$

### 第三步：代数求解 $y$

我们已经用 $y$ 表示了 $m$，但 $y$ 本身还是未知的。为了求 $y$，我们需要建立一个只包含 $y$ 和已知数 $C₁$、$C₂$ 的方程。

我们可以通过 $m^2$ 建立这个等式。首先，从 `方程式 1` 移项可得：
$$m^2 \equiv C_1 - m \pmod n$$
将 `求解式 A` ($m \equiv y - C_1$) 代入上式：
$$m^2 \equiv C_1 - (y - C_1) \pmod n$$
$$m^2 \equiv 2C_1 - y \pmod n \quad \cdots\quad (求解式 \, B)$$
现在我们有了 $m$ 和 $m^2$ 的表达式。根据数学基本定律 $(m)^2 = m^2$，我们可以令 `(求解式 A)²` 等于 `求解式 B`：
$$(y - C_1)^2 \equiv 2C_1 - y \pmod n$$
展开左侧的完全平方：
$$y^2 - 2yC_1 + C_1^2 \equiv 2C_1 - y \pmod n$$
根据 $y$ 的定义（$y \equiv \sqrt{C_2}$），我们知道 $y^2 \equiv C_2 \pmod n$。将其代入：
$$C_2 - 2yC_1 + C_1^2 \equiv 2C_1 - y \pmod n$$
现在整理这个方程，把所有包含 $y$ 的项移到一边：
$$C_2 + C_1^2 - 2C_1 \equiv 2yC_1 - y \pmod n$$
$$C_2 + C_1^2 - 2C_1 \equiv y(2C_1 - 1) \pmod n$$
最后，两边同时乘以 $(2C_1 - 1)$ 的模逆元，我们就能直接计算出 $y$ 的值：
$$y \equiv (C_2 + C_1^2 - 2C_1) \times (2C_1 - 1)^{-1} \pmod n$$

### 总结

最终的求解步骤如下：
1. 向服务器请求 $k=1$ 和 $k=2$ 的结果，分别得到 $C₁$ 和 $C₂$。
2. 使用 $C₁$ 和 $C₂$，通过以下公式计算出 $y$（即 $C₂$ 的模平方根）：
    $$
    y = \left( C_2 + C_1^2 - 2C_1 \right) \times \text{pow}(2C_1 - 1, -1, n) \pmod n
    $$
3. 将计算出的 $y$ 和已知的 $C₁$ 代入 `求解式 A`，得到最终的 $m$：
    $$
    m = (y - C_1) \pmod n
    $$
单独的解题脚本如下
```python
import sys
import math

# 设置一个高的整数到字符串转换限制
sys.set_int_max_str_digits(0)

## ----------------------------------------------------------------
## 1. 定义所有已知信息
## ----------------------------------------------------------------
print("--- 1. 定义已知信息 ---")
n_hex = "0xb3eaacc65bf88213e2a641130ae0c382fb2682794e62385f9944f9ff7356bbe2b057226747f38e177cb758888297c7f843f95dda1f5831d2e8ce48256604d11b45fc9010cbd183ee646bf6c687792284bbf029b7abc9e53b87d66a9ef15dd982ac7fa73d99fdd6baaf512bd735b64e2fb2ca29d2bc2e250ae2f9322ece30424b"
c1_hex = " 0xdf975432289097183712b38ac81aae0a369a7aabc2abb2ac6ba33411ce073693e4308a3a4685e49563d55875757a26e6fa6d15552c60e9cb58fecb3ba66a64c8432b36a20e014a96ef126ff9a5d67f605ed7553c6f752c0d605061f3f9aa735d985bae121d12d97fbb818346ec77929ed9e4a8c656aa4aa45b94581f65d1532"
c2_hex = "0xa8d2bd85b3962f2f6160ba8973084e2cd44837d72ca3db9456a6a1edf9ea9246b3765dbc309e9e37eabad16506953c0dccec051ec637fd7bba631b7d868b30b7a4c4f48075a296be1ec1aa5c770f0fb0a881bcd47e36924ecf1c9eeba47afa15ba34e69b4b6ebb704a14d8cd229af3989221d274d498dbe5c79a4fa437b26e79"

n = int(n_hex, 16)
c1 = int(c1_hex, 16)
c2 = int(c2_hex, 16)
print("   n, C₁, C₂ 已加载。\n")

## ----------------------------------------------------------------
## 2. 代数求解 sqrt(C₂)
## ----------------------------------------------------------------
print("--- 2. 代数求解 y = sqrt(C₂) ---")

# 计算 y = (C₂ + C₁² - 2C₁) * inv(2C₁ - 1) mod n
term1 = (c2 + pow(c1, 2, n) - 2 * c1 + n) % n
term2 = pow(2 * c1 - 1, -1, n)
y = (term1 * term2) % n

print(f"   [SUCCESS] 通过代数方法成功计算出 y = sqrt(C₂)!")
print(f"   y = sqrt(C₂) = {hex(y)}\n")

## ----------------------------------------------------------------
## 3. 计算 m
## ----------------------------------------------------------------
print("--- 3. 计算 m = (y - C₁) mod n ---")
m = (y - c1 + n) % n
print(f"   m 已计算。\n")

## ----------------------------------------------------------------
## 4. 显示最终答案
## ----------------------------------------------------------------
print("--- 4. 最终答案 ---")
print(f"[*] m (hex): {hex(m)}")
print(f"[*] m (dec): {m}\n")

## ----------------------------------------------------------------
## 5. 验证
## ----------------------------------------------------------------
print("--- 5. 验证 ---")

# 验证 k=1
print("[*] 正在验证 k=1...")
verify_k1 = (m * (m + 1)) % n
print(f"   计算值: {hex(verify_k1)}")
print(f"   期望值: {hex(c1)}")
if verify_k1 == c1:
    print("   ✅ [SUCCESS] k=1 验证通过！")
else:
    print("   ❌ [FAILURE] k=1 验证失败！")

# 验证 k=2
print("\n[*] 正在验证 k=2...")
base_k2 = (m * (m + 2)) % n
verify_k2 = pow(base_k2, 2, n)
print(f"   计算值: {hex(verify_k2)}")
print(f"   期望值: {hex(c2)}")
if verify_k2 == c2:
    print("   ✅ [SUCCESS] k=2 验证通过！")
else:
    print("   ❌ [FAILURE] k=2 验证失败！")
```


最终flag
![[Pasted image 20250801105042.png]]
![[Pasted image 20250801104422.png]]



## crosswired
问题分析 
 共用模数 N 
 - **关键点**：所有的加密操作（无论是你朋友的还是你自己的）都使用了同一个模数 `N`。
 - **影响**：共用模数可能导致通过已知私钥推导出模数因子，从而破解加密。
 -  连续加密  加密过程 
 1. **多次加密**：FLAG 被朋友的公钥连续加密了五次，形式为： $$ C \equiv ((((M^{e_1})^{e_2})^{e_3})^{e_4})^{e_5} \pmod{N} $$ 2. **简化公式**：利用模幂运算的结合律，可简化为： $$ C \equiv M^{(e_1 \cdot e_2 \cdot e_3 \cdot e_4 \cdot e_5)} \pmod{N} $$ 3. **总指数定义**：定义总的加密指数为： $$ E_{\text{total}} = e_1 \cdot e_2 \cdot e_3 \cdot e_4 \cdot e_5 $$ --- ## 私钥泄露 - **已知信息**：代码中给出了私钥 `my_key = (N, d)`，其中： - `e = 0x10001`（即 65537，常见公钥指数） - `d` 是与 `e` 配对的私钥指数。 - **关键作用**：通过已知的 `(e, d, N)` 可以分解模数 `N`，得到其素因子 `p` 和 `q`。 
 解密思路  
 2. 步骤 1：分解模数 N - **目标**：利用 `(e, d, N)` 分解 `N`，求得素因子 `p` 和 `q`。 - **方法**： 1. 根据 RSA 原理，$e \cdot d \equiv 1 \pmod{\phi(N)}$。 2. 通过已知的 `e` 和 `d`，计算 $k = \frac{e \cdot d - 1}{\phi(N)}$，进而推导出 `p` 和 `q`。 
 3. 步骤 2：计算欧拉函数 - **公式**： $$ \phi(N) = (p - 1)(q - 1) $$ 步骤 3：计算总解密指数 - **目标**：计算 `E_total` 在模 `ϕ(N)` 下的逆元 `D_total`。 - **公式**： $$ D_{\text{total}} = \text{inverse}(E_{\text{total}}, \phi(N)) $$ 步骤 4：解密密文 1. **应用解密公式**： $$ M \equiv C^{D_{\text{total}}} \pmod{N} $$ 2. **结果转换**：将解密后的整数 `M` 转换回字节形式，即可得到 FLAG。
代码：
```python
from Crypto.Util.number import long_to_bytes, inverse
import math
import random
import ast # 用于安全地解析字符串中的Python字面值

def parse_input(filename="output.txt"):
    """从文件中解析 N, d, e, 朋友的公钥和密文"""
    with open(filename, 'r') as f:
        lines = f.readlines()

    # 解析私钥 (N, d)
    private_key_str = lines[0].split('My private key: ')[1].strip()
    N, d = ast.literal_eval(private_key_str)

    # 解析朋友的公钥
    friend_keys_str = lines[1].split("My Friend's public keys: ")[1].strip()
    friend_keys_list = ast.literal_eval(friend_keys_str)
    friend_keys_e = [key[1] for key in friend_keys_list]

    # 解析加密的flag
    cipher_str = lines[2].split('Encrypted flag: ')[1].strip()
    cipher = int(cipher_str)
    
    # 固定的公钥 e
    e = 0x10001
    
    return N, d, e, friend_keys_e, cipher

def factor_N_from_d(N, e, d):
    """利用已知的 e, d, N 来分解 N"""
    k = e * d - 1
    r = k
    s = 0
    while r % 2 == 0:
        r //= 2
        s += 1
    
    while True:
        a = random.randint(2, N - 2)
        x = pow(a, r, N)
        if x == 1 or x == N - 1:
            continue
            
        y = 0
        for _ in range(s):
            y = pow(x, 2, N)
            if y == 1:
                p = math.gcd(x - 1, N)
                q = N // p
                return p, q
            if y == N - 1:
                break
            x = y
        if y == N - 1:
            continue

# --- 主程序 ---
# 步骤 0: 从文件读取数据
print("正在从 output.txt 读取数据...")
N, d, e, friend_keys_e, cipher = parse_input()
print("数据读取成功！")

# 步骤 1: 分解 N 得到 p 和 q
print("正在分解 N ...")
p, q = factor_N_from_d(N, e, d)
print("分解成功！")

# 步骤 2: 计算 phi(N)
phi = (p - 1) * (q - 1)

# 步骤 3: 计算总的加密指数 E_total
E_total = 1
for friend_e in friend_keys_e:
    E_total *= friend_e

# 步骤 4: 计算总的解密密钥 D_total
D_total = inverse(E_total, phi)

# 步骤 5: 解密密文
decrypted_message = pow(cipher, D_total, N)

# 步骤 6: 将结果转换为字节
flag = long_to_bytes(decrypted_message)

print("\n解密成功！")
print(f"Flag: {flag.decode()}")
```
![[Pasted image 20250730164828.png]]

![[Pasted image 20250730175841.png]]


## EvrerythingBig RSA 维纳攻击解密推导

## 1. 漏洞背景：参数选择导致的安全缺陷

在给定的 RSA 实现中：
- 模数 $N = p \times q$，其中 $p$ 和 $q$ 均为 **1024 位大素数**，故 $N$ 为 **2048 位**（$N \approx 2^{2048}$）
- 私钥 $d$ 为 **256 位素数**（$d \approx 2^{256}$），远小于 $N$
- 公钥 $e$ 满足 $e.\text{bit\_length}() = N.\text{bit\_length}()$，即 $e$ 接近 $N$ 的大小（**约 2048 位**，$e \approx N$）

> **安全缺陷**  
> 标准 RSA 要求私钥 $d$ 足够大（通常接近 $\phi(N)$ 的大小）以抵抗攻击。此处 $d$ 过小（256 位）而 $e$ 过大（2048 位），**违反 RSA 安全参数建议**，使系统易受 **维纳攻击（Wiener's Attack）** 影响。该攻击无需分解 $N$，而是通过连分数逼近直接恢复私钥 $d$。

> **核心**
> 小 $d$ 和大 $e$ 导致方程 $e \cdot d \equiv 1 \pmod{\phi(N)}$ 产生可被连分数逼近的数学关系。

---

## 2. 维纳攻击数学原理

### 2.1 建立主要方程
由 RSA 私钥定义，存在整数 $k$ 使得：
$$
e \cdot d = 1 + k \cdot \phi(N) \quad (1)
$$
其中 $\phi(N) = (p-1)(q-1)$ 是欧拉函数。

### 2.2 近似 $\phi(N) \approx N$
由于 $p$ 和 $q$ 均为大素数（$p, q \approx \sqrt{N}$）：
$$
\phi(N) = (p-1)(q-1) = N - p - q + 1
$$
令 $s = p + q - 1$（显然 $s \ll N$，且 $s < 3\sqrt{N}$ 对大 $N$ 成立），则：
$$
\phi(N) = N - s \quad \text{且} \quad s \approx 2\sqrt{N} \quad (2)
$$
代入方程 (1)：
$$
e \cdot d = 1 + k \cdot (N - s) \quad (3)
$$

### 2.3 推导 $\frac{e}{N} \approx \frac{k}{d}$
将方程 (3) 两边同除以 $d \cdot N$：
$$
\frac{e}{N} = \frac{1 + k \cdot (N - s)}{d \cdot N} = \frac{k}{d} - \frac{k \cdot s}{d \cdot N} + \frac{1}{d \cdot N}
$$
移项得误差表达式：
$$
\left| \frac{e}{N} - \frac{k}{d} \right| = \left| -\frac{k \cdot s}{d \cdot N} + \frac{1}{d \cdot N} \right| \leq \frac{k \cdot s}{d \cdot N} + \frac{1}{d \cdot N} \quad (4)
$$

### 2.4 误差界分析与攻击条件
- **估计 $k$**：  
  由方程 (1) 和 $e < N$，有 $k \cdot \phi(N) < e \cdot d < N \cdot d$。  
  因 $\phi(N) > N/2$（对大 $N$)，得 $k < 2d$。实践中 $k \approx d$（因 $e \approx N$）。
  
- **代入误差界**：  
  将 $s < 3\sqrt{N}$ 和 $k < 2d$ 代入 (4)：
  $$
  \left| \frac{e}{N} - \frac{k}{d} \right| < \frac{(2d) \cdot (3\sqrt{N})}{d \cdot N} + \frac{1}{d \cdot N} = \frac{6}{\sqrt{N}} + \frac{1}{d \cdot N} \quad (5)
  $$

- **维纳攻击条件**：  
  数论中，若 $\left| \frac{e}{N} - \frac{k}{d} \right| < \frac{1}{2d^2}$，则 $\frac{k}{d}$ 必为 $\frac{e}{N}$ 的连分数展开的某个**收敛项**（convergent）。  
  由 (5)，当 $d$ 足够小时：
  $$
  \frac{6}{\sqrt{N}} < \frac{1}{2d^2} \implies d < \frac{1}{2\sqrt{3}} N^{1/4} \approx 0.288 \cdot N^{1/4}
  $$
  **维纳定理**：若 $d < \frac{1}{3} N^{1/4}$，则 $\frac{k}{d}$ 一定是 $\frac{e}{N}$ 的连分数收敛项。

### 2.5 条件验证
- $N$ 为 2048 位 → $N \approx 2^{2048}$
- $N^{1/4} = (2^{2048})^{1/4} = 2^{512}$（**512 位**）
- 给定 $d$ 为 256 位 → $d \approx 2^{256}$
- 比较：
  $$
  2^{256} < \frac{1}{3} \cdot 2^{512} \quad \text{（因 } 2^{512} / 2^{256} = 2^{256} \approx 10^{77} \gg 3\text{）}
  $$

> **关键结论**  
> **$\frac{k}{d}$ 必为 $\frac{e}{N}$ 的连分数展开的某个收敛项 $\frac{k_i}{d_i}$**。  
> 攻击目标：通过计算 $\frac{e}{N}$ 的连分数收敛项，恢复正确的 $d_i$。

---

## 3. 解密步骤（攻击实施流程）

### 3.1 计算 $\frac{e}{N}$ 的连分数展开
1. 计算 $\frac{e}{N}$ 的连分数表示：$\frac{e}{N} = [a_0; a_1, a_2, \dots, a_m]$
2. 生成所有收敛项 $\frac{k_i}{d_i}$（通过递推公式）：
   ```
   h_{-2} = 0,  h_{-1} = 1
   l_{-2} = 1,  l_{-1} = 0
   
   for i in range(m):
       h_i = a_i * h_{i-1} + h_{i-2}
       l_i = a_i * l_{i-1} + l_{i-2}
       收敛项 = h_i / l_i  (其中 d_i = l_i)
   ```

### 3.2 筛选候选私钥 $d_i$
- **必要条件**：RSA 私钥 $d$ 必须是**奇数**（因 $\phi(N)$ 为偶数，$e$ 通常选奇数）
- 仅保留分母 $d_i$ 为**奇数**的收敛项

### 3.3 尝试解密并验证明文
对每个候选 $d_i$：
```python
m_prime = pow(c, d_i, N)  # 计算解密消息
plaintext = m_prime.to_bytes((m_prime.bit_length() + 7) // 8, 'big')

if plaintext.startswith(b'crypto{'):
    print("Found valid private key:", d_i)
    print("Decrypted message:", plaintext.decode())
    break
```

> **为什么有效**？  
> 由于 $d < \frac{1}{3} N^{1/4}$，正确 $d$ 必在收敛项中；且 $d$ 为奇数的约束大幅减少候选数量（通常仅需测试少量项）。

---
编写代码求解
```python
#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes

def wiener_attack(e, N, c):
    """
    执行维纳攻击来找到 RSA 私钥 d 并解密。
    e/N 的连分数收敛项之一是 k/d。
    """
    
    # 使用迭代方法计算 e/N 的连分数收敛项 p_n/q_n
    # p_n/q_n 在这里对应 k/d
    
    # 初始化 p 和 q 的前两项
    # p_{-2}=0, p_{-1}=1
    # q_{-2}=1, q_{-1}=0
    p_prev, q_prev = 0, 1
    p_curr, q_curr = 1, 0

    num, den = e, N
    
    print("开始进行维纳攻击...")
    iteration = 0
    while den != 0:
        iteration += 1
        
        # 计算连分数系数 a
        a = num // den
        
        # 计算下一个收敛项的分子和分母 (p_n, q_n)
        p_next = a * p_curr + p_prev
        q_next = a * q_curr + q_prev

        # 候选的 k 和 d
        # 注意：第一个收敛项 p_0/q_0 (k/d) 可能为 0/1 或 1/0，需要跳过无效情况
        k = p_next
        d = q_next

        # 更新 p 和 q 的值以进行下一次迭代
        p_prev, q_prev = p_curr, q_curr
        p_curr, q_curr = p_next, q_next

        # 更新连分数展开的余项
        num, den = den, num % den

        # d 不能为 0，且根据 RSA 定义，d 必须是奇数
        if d == 0 or d % 2 == 0:
            continue
        
        print(f"第 {iteration} 轮尝试: 候选 d = {hex(d)}")

        # 尝试用候选的 d 进行解密
        m_candidate = pow(c, d, N)
        
        try:
            # 将解密出的数字转换为字节
            flag = long_to_bytes(m_candidate)
            # 检查是否是我们寻找的 flag 格式
            if b'crypto{' in flag:
                print("\n成功找到 Flag!")
                return flag.decode('utf-8')
        except (ValueError, OverflowError):
            # 如果 m_candidate 无法正常转换为字节，则继续尝试下一个
            continue
            
    print("\n攻击失败，未找到有效的 d。")
    return None

def main():
    # 从 output.txt 文件中读取 N, e, c
    try:
        with open('output.txt', 'r') as f:
            lines = f.readlines()
            N = int(lines[0].split(' = ')[1], 16)
            e = int(lines[1].split(' = ')[1], 16)
            c = int(lines[2].split(' = ')[1], 16)
    except FileNotFoundError:
        print("错误: output.txt 文件未找到。")
        return
    except (IndexError, ValueError):
        print("错误: output.txt 文件格式不正确。")
        return

    # 执行攻击
    flag = wiener_attack(e, N, c)

    if flag:
        print(f"解密后的 Flag 是: {flag}")

if __name__ == '__main__':
    main()
```
![[Pasted image 20250730180028.png]]
![[Pasted image 20250730180052.png]]


### 本题特殊性
- 公钥 $e$ 极大（$e \approx N$) 加速了 $\frac{e}{N} \approx 1$ 的逼近
- 但推导对**任意 $e$** 成立（只要 $d$ 满足条件）

> **核心公式**  
> $$d < \frac{1}{3} N^{1/4} \quad \text{是维纳攻击成功的充要条件}$$
> $$\frac{e}{N} \approx \frac{k}{d} \quad \text{是连分数逼近的基础}$$

%% 
## 相关笔记
- [[公钥密码体系]]
%%


# Email：RSA广播攻击 Håstad's Broadcast Attack分析与实践

## 1. 实验目的
本实验旨在分析存在实现缺陷的RSA加密过程，通过理论推导与实践验证，从给定的多组密文（output.txt）中恢复原始明文信息。核心目标是理解并应用哈斯塔德广播攻击（Håstad's Broadcast Attack）原理，结合中国剩余定理（Chinese Remainder Theorem）实现明文恢复，同时记录解题过程中的关键决策与调试思路。

## 2. 背景知识与漏洞分析

### 2.1 RSA算法简述
RSA是一种非对称加密算法，其安全性基于大整数分解的困难性。加密过程可表示为：
$$c \equiv m^e \pmod{N}$$
其中 $(N,e)$ 为公钥，$m$ 为明文，$c$ 为密文。

### 2.2 漏洞识别
通过分析johan.py脚本，识别出两个关键实现缺陷：

1. **极小的公钥指数**：脚本硬编码公钥指数 $e = 3$，远低于安全建议值（通常 $e \geq 65537$），使明文立方 $m^3$ 可能小于模数 $N$。

2. **重复明文使用不同模数**：`RSA_encrypt`函数每次加密均生成全新素数 $p$ 和 $q$，导致相同明文产生多组不同模数的密文。题目背景"很多学生都在问同样的问题"表明存在重复明文场景。

### 2.3 攻击原理：哈斯塔德广播攻击
当同一明文 $m$ 被至少 $e$ 组不同公钥 $(N_i,e)$ 加密时，可构建以下方程组：
$$
\begin{cases}
m^3 \equiv c_1 \pmod{N_1} \\
m^3 \equiv c_2 \pmod{N_2} \\
m^3 \equiv c_3 \pmod{N_3}
\end{cases}
$$
由于 $N_i$ 由独立大素数生成，其两两互质概率极高。根据中国剩余定理（CRT），方程组在模 $N_{\text{total}} = N_1 \times N_2 \times N_3$ 下有唯一解 $M$：
$$M \equiv m^3 \pmod{N_{\text{total}}}$$
当 $m^3 < N_{\text{total}}$ 时，有 $M = m^3$，通过计算 $m = \sqrt[3]{M}$ 即可恢复明文。

## 3. 实验过程与解题策略

### 3.1 初步尝试与失败分析
**策略**：假设output.txt中前三组密文对应同一明文，直接应用CRT求解。

**实施**：
1. 选取前3组 $(N_i, c_i)$ 数据
2. 应用中国剩余定理解方程组
3. 计算 $m = \sqrt[3]{M}$ 并转换为字节字符串

**结果**：获得字节序列 `b'\x02\x9f\x8a...'`，解码后为无意义乱码。

**失败原因**：
- 错误假设：前三组数据不对应同一明文
- 未验证 $M$ 是否为完美立方数
- 缺乏对明文格式的合理假设

### 3.2 修正策略：组合遍历
**策略**：从7组数据中找出真正属于同一明文的3组组合。

**实施**：
1. 使用 `itertools.combinations` 生成所有35种可能的3组组合
2. 对每组组合执行CRT求解
3. 自动验证条件：
   - $M$ 为完美立方数（$m^3 = M$）
   - 解密结果可UTF-8解码
   - 解码后字符串可打印（`.isprintable()`）

**结果**：所有35种组合均被判定为失败。

**失败原因**：
- 验证条件过于严格：明文可能包含非打印字符（如换行符）
- UTF-8解码可能失败：明文可能为二进制数据或特定编码格式
- 完美立方数验证存在浮点精度问题

### 3.3 最终策略：人工辅助分析
放宽自动验证条件，由人工审查候选解。

**实施**：
1. 遍历所有35种组合
2. 对每组执行CRT求解
3. 仅保留满足严格数学条件的候选解：
   - $m = \lfloor M^{1/3} + 0.5 \rfloor$
   - $m^3 = M$（精确等式验证）
4. 输出所有候选解的原始字节及多种解码尝试：
   - 原始字节表示
   - UTF-8解码（忽略错误）
   - ASCII解码
   - 十六进制表示
```python
import re
import itertools
from Crypto.Util.number import long_to_bytes

def modinv(a, m):
    try:
        return pow(a, -1, m)
    except ValueError:
        raise Exception('Modular inverse does not exist')

def solve_crt(remainders, moduli):
    N_total = 1
    for n in moduli:
        N_total *= n
    result = 0
    for i in range(len(moduli)):
        c_i, N_i = remainders[i], moduli[i]
        N_prod_i = N_total // N_i
        inv_i = modinv(N_prod_i, N_i)
        result += c_i * N_prod_i * inv_i
    return result % N_total

def integer_cbrt(n):
    if n < 0:
        return -integer_cbrt(-n)
    if n == 0:
        return 0
    low = 1
    high = 1 << ((n.bit_length() + 2) // 3)
    while low <= high:
        mid = (low + high) // 2
        if mid == 0: low = 1; continue
        mid_cubed = mid * mid * mid
        if mid_cubed == n: return mid
        elif mid_cubed < n: low = mid + 1
        else: high = mid - 1
    return high

def parse_output_file(filename="output.txt"):
    with open(filename, 'r') as f:
        content = f.read()
    matches = re.findall(r"n = (\d+)\s+e = 3\s+c = (\d+)", content)
    return [(int(n), int(c)) for n, c in matches]

def main():
    print("[-] 正在从 output.txt 解析加密数据...")
    crypto_data = parse_output_file()
    if len(crypto_data) < 3:
        print("[!] 数据不足，需要至少3组。")
        return

    print(f"[-] 成功解析到 {len(crypto_data)} 组数据。")
    print("[-] 开始遍历所有组合，寻找所有数学上可能的候选消息...")
    
    found_candidates = 0
    
    # enumerate 可以让我们知道这是第几个组合
    for i, combo in enumerate(itertools.combinations(crypto_data, 3)):
        moduli = [data[0] for data in combo]
        remainders = [data[1] for data in combo]

        try:
            m_cubed = solve_crt(remainders, moduli)
            m = integer_cbrt(m_cubed)
            
            # 这是最关键的硬性检查：结果必须是完美的立方数
            if m*m*m == m_cubed:
                found_candidates += 1
                message = long_to_bytes(m)
                
                print(f"\n--- 找到一个候选答案 (来自组合 #{i+1}) ---")
                print(f"  Raw Bytes: {message}")

                try:
                    decoded_utf8 = message.decode('utf-8')
                    print(f"  Decoded (UTF-8): {decoded_utf8}")
                except UnicodeDecodeError as e:
                    print(f"  Decoded (UTF-8): 失败 - {e}")
                
                # Latin-1 编码总能成功，可以让我们看到所有字节的字符表示
                decoded_latin1 = message.decode('latin-1')
                print(f"  Decoded (Latin-1): {decoded_latin1}")
                print("-----------------------------------------")

        except Exception:
            continue
    
    if found_candidates == 0:
        print("\n[!] 遍历了所有组合，但未能找到任何一个完美的立方数解。这很奇怪，请检查 output.txt 文件或脚本。")
    else:
        print(f"\n[+] 完成！共找到 {found_candidates} 个候选答案。请在上面的人工检查哪一个是真正的消息。")


if __name__ == "__main__":
    main()
```
**结果**：在第8组组合中发现有效明文：
![[Pasted image 20250730175807.png]]

**成功关键**：
- 严格数学验证：确保 $m^3 = M$ 为精确等式
- 放宽格式验证：允许非标准字符存在
- 人工审查：识别有意义的文本内容

## 4. 实验结论


1. 当 $e=3$ 且获取至少3组针对同一明文的加密数据时，Håstad's Broadcast Attack可100%恢复明文
2. 实验成功恢复出原始邮件内容，验证了理论分析的正确性


## 5. 实验反思
1. **理论局限性**：Håstad's Broadcast Attack要求 $k \geq e$，当 $e$ 增大时攻击难度指数级上升
2. **数据特征影响**：明文长度与模数大小的比例关系直接影响攻击可行性
3. **验证方法优化**：未来可设计更智能的明文特征检测（如语言模型验证）
![[Pasted image 20250730175821.png]]



# EZDLP
![[Pasted image 20250801120342.png]]
### 离散对数问题 (EZDLP) 求解过程与算法汇总

 1. 问题背景

本次任务的核心是解决一个名为 `EZDLP.py` 的密码学挑战。该挑战的目标是求解一个离散对数问题 (Discrete Logarithm Problem, DLP)，从而获取一个用于 AES 加密的密钥，并最终解密出隐藏的 Flag。

给定的核心问题是求解在有限域 $\mathbb{Z}_p$ 上的方程：
$$g^x \equiv c \pmod{p}$$
其中 `p`, `g`, `c` 均为已知，我们需要求解 `x`。之后，通过以下方式获得 Flag：
$$\text{key} = \text{MD5}(\text{str}(x))$$
$$\text{Flag} = \text{AES-ECB-Decrypt}(\text{key}, \text{ct})$$

---

2. 核心算法与数学公式  
2.1 离散对数问题 (DLP)  
基础方程: 给定 $g,c,p$，找到 $x$ 使得 $g^x \equiv c \pmod{p}$。

2.2 部分 Pohlig-Hellman 攻击 (Partial Pohlig-Hellman Attack)  
此方法适用于群的阶 $n = p-1$ 可以被分解为一个“可解”部分和一个“困难”部分的场景。在本题中，我们发现 $p-1$ 具有以下特殊结构：

**阶的分解 (Order Factorization)**  
$p-1$ 可以被分解为 $p-1 = q \cdot r$，其中：
- $q = 2^{518}$（一个巨大的2的幂，其对应的DLP问题是高效可解的）
- $r = 1119326809698249181662206673457$（一个巨大的素数，其对应的DLP问题是困难的）

**向子群的映射 (Mapping to the Subgroup)**  
我们的目标是消除困难部分 $r$ 的影响，只在阶为 $q$ 的子群中解决问题。

从基础方程开始：
$$g^x \equiv c \pmod{p}$$
将等式两边同时取 $r$ 次幂：
$$(g^x)^r \equiv c^r \pmod{p}$$
根据幂运算法则，这等价于：
$$(g^r)^x \equiv c^r \pmod{p}$$

定义新的基 $g'$ 和新的值 $c'$：
$$g' = g^r \pmod{p}$$
$$c' = c^r \pmod{p}$$
这样，原问题被转换成一个新的、在阶为 $q$ 的子群中的DLP：
$$g'^x \equiv c' \pmod{p}$$

**高效求解幂次阶DLP (Solving DLP in power-of-2 order group)**  
上述新DLP的解为 $x_q = x \mod q$。  
由于子群的阶 $q = 2^{518}$ 是2的幂，存在一种非常高效的算法（Pohlig-Hellman算法的特例）来求解它。SageMath的 `discrete_log` 函数对此有内置的高度优化实现。

2.3 利用 $x$ 的约束确定唯一解  
这是本题解法的关键。在得到 $x_q = x \mod q$ 后，我们利用x的范围约束。

**问题约束**  
源码中 $x = \text{getPrime}(500)$ 告诉我们 $x$ 是一个500位的素数。这意味着 $x$ 的范围是：
$$2^{499} \le x < 2^{500}$$

**关键不等式**  
我们将 $x$ 的范围与我们在上一步中使用的模数 $q$ 进行比较：
$$x < 2^{500} < 2^{518} = q$$

**确定唯一解**  
我们已经计算出 $x_q = x \mod q$。  
这个方程的通解是 $x = x_q + k \cdot q$（其中 $k$ 是某个整数）。  
但由于我们已经确定 $0 < x < q$，这使得唯一的可能性是 $k=0$。  
因此，我们可以直接得出结论：
$$x = x_q$$

这个步骤巧妙地将一个同余方程的解，通过一个范围约束，直接锁定为了一个确定的整数解。

3. 最终解法流程总结  
4. **分析阶的结构**：对 $p-1$ 进行因数分解，发现其具有 $p-1 = q \cdot r$ 的特殊形式，其中 $q = 2^{518}$。  
5. **降维攻击**：将原始DLP方程两边取 $r$ 次幂，从而将问题映射到阶为 $q$ 的子群中，得到一个新的、更简单的DLP：$g'^x \equiv c' \pmod{p}$。  
6. **求解子群DLP**：利用 SageMath 的 `discrete_log` 高效求解这个阶为 $2^{518}$ 的DLP，得到 $x_q = x \mod q$。  
7. **应用约束**：结合题目给出的 $x$ 是500位素数的条件，推导出 $x < q$，从而直接确定 $x = x_q$。  
8. **密钥生成与解密**：计算 $\text{MD5}(\text{str}(x))$ 作为 AES 密钥，并用它解密密文 `ct`，最终获得 Flag。

```python

# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from hashlib import md5

# --- 已知参数 ---
p = 960494008017250155494739990397196249930200062145145133132556398221074529657304218221253517153928380265486339083177542201148993799925721673833333778621388110957986908045712612233794551809
g = 3
c = 505527904713564983625416248872210831215228354175257237841602581321675204643681129570897695080321118656513647239718859773976453054734892142640867733520305568808093022238369199760987416665
ct = b'qBS\x84\xfc"\xee$\xb2d\xba\xeb\x00\xf7\xf4\xa4\x91\x90<N\x1a\xb0\xa5>\xdc^\xe3I\xc3\xecc\x1e'

# --- 步骤 1: p-1 的正确因子分解 ---
# p-1 = q * r
q = 2^518
r = 1119326809698249181662206673457
print(f"[*] Correct factorization p-1 = q * r")
print(f"q = 2^518")
print(f"r = {r} (large prime)")

# --- 步骤 2: "部分"Pohlig-Hellman攻击 ---
# 将DLP问题转换到阶为 q 的子群中
print("\n[*] Transforming DLP to a subgroup of order q...")
g_prime = power_mod(g, r, p)
c_prime = power_mod(c, r, p)

# 解决阶为 q = 2^518 的新DLP问题
# c_prime = (g_prime)^x mod p
print("[*] Solving the new DLP for x mod q...")
# The order of the new group is q
x_mod_q = discrete_log(c_prime, Mod(g_prime, p), ord=q)

# --- 步骤 3: 确定 x ---
# 因为 x 是 500-bit 素数, 所以 x < 2^500 < 2^518 = q
# 因此, x_mod_q 就是 x 本身
x = x_mod_q
print(f"[+] Found x: {x}")
print(f"[*] Bit length of x: {x.nbits()}")
print(f"[*] Is x prime? {is_prime(x)}")

# --- 步骤 4: 派生密钥并解密 🔑 ---
print("\n[*] Deriving AES key and decrypting...")
key = md5(str(x).encode()).digest()
cipher = AES.new(key, AES.MODE_ECB)
padded_flag = cipher.decrypt(ct)

# 去除填充
flag = padded_flag.rstrip(b'\x00')

print(f"\n[+] Decrypted Flag: 🚩 {flag.decode()}")
```

![[Pasted image 20250801160951.png]]
![[Pasted image 20250801161029.png]]


# Bonus ECC exploration
#ECC
## 概述
ECC（Elliptic Curve Cryptography）是一种基于椭圆曲线数学的公钥密码系统。其核心优势在于**在相同安全性下使用更短的密钥长度**，相较于传统基于大整数分解的RSA算法，ECC在资源受限设备上具有显著性能优势。

当前主要采用的有限域类型：
- **素数域 GF(p)**：适合通用处理器运算
- **二进制扩展域 GF(2^m)**：便于硬件电路设计

---

## 基本知识

### 1. 有限域椭圆曲线定义
有限域上的椭圆曲线由以下方程定义：
$$y^2 + axy + by = x^3 + cx^2 + dx + e$$
其中所有系数 $a, b, c, d, e \in \mathrm{GF}(p)$，且 $p$ 为大素数。

> ⚠️ 实际加密中常用简化形式：
$$y^2 = x^3 + ax + b$$
需满足判别式条件：$4a^3 + 27b^2 \mod p \ne 0$

### 2. 椭圆曲线群结构
集合 $E(\mathrm{GF}(p))$ 包含：
- 所有满足方程的点 $(x, y) \in \mathrm{GF}(p)^2$
- 一个特殊点 "无穷远点" O（零元）

该集合在定义的加法运算 $\oplus$ 下构成**阿贝尔群**。

---

## 一般定义条件

椭圆曲线密码系统需满足：
1. **群结构封闭性**：任意两点 $P, Q \in E(\mathrm{GF}(q))$，其加法 $P \oplus Q$ 仍在群中
2. **周期性要求**：存在最小正整数 $t$ 使得 $t \cdot P = O$
   - 定义 $t$ 为点 $P$ 的**周期**
3. **离散对数问题**：对于 $Q = m \cdot P$，求 $m$ 的计算是困难的
   - 记为 $m = \log_P Q$

>  生成元 $G$ 是满足 $n \cdot G = O$ 的最小正整数 $n$ 生成的点，$n$ 称为**阶**

---

## ECC中的ElGamal加密

### 密钥生成（用户A）
1. 选择椭圆曲线 $E_q(a, b)$ 及生成元 $G$（阶为 $n$）
2. 选取私钥 $n_a \in [1, n-1]$
3. 计算公钥 $P_a = n_a \cdot G$

> 公开信息：$E_q(a, b), q, G, P_a$

---

### 加密过程（用户B发送消息 $m$）
1. 获取A的公钥信息
2. 随机选择 $k \in (1, q-1)$
3. 计算：
   - $(x_1, y_1) = k \cdot G$
   - $(x_2, y_2) = k \cdot P_a$（若结果为O则重选 $k$）
4. 加密：$C = m \oplus (x_2, y_2)$
5. 发送密文对 $( (x_1, y_1), C )$

---

### 解密过程（用户A）
1. 计算 $n_a \cdot (x_1, y_1) = n_a \cdot k \cdot G = k \cdot P_a = (x_2, y_2)$
2. 解密：$m = C \oplus -(x_2, y_2)$




## 一道ECC例题
```
已知椭圆曲线加密Ep(a,b)参数为
p = 15424654874903
a = 16546484
b = 4548674875
G(6478678675,5636379357093)
私钥为
k = 546768
求公钥K(x,y)
flag格式为cyberpeace{x+y的值}

```
椭圆曲线密码学的核心操作是标量乘法，即计算 $K = k \cdot G$，其中 $k$ 为私钥，$G$ 为生成元，$K$ 为公钥。直接进行 $k$ 次加法效率极低，因此采用高效的 **Double-and-Add** 算法。该算法利用私钥 $k$ 的二进制表示形式，通过点倍增和点相加运算加速计算：

1. 将私钥 $k$ 转换为二进制形式（如 $k=13$ 对应 `1101`）  
2. 从最高位开始初始化结果 $K=G$  
3. 遍历剩余二进制位：  
   - 每次倍增当前结果 $K = K + K$  
   - 若当前位为 '1'，则额外与 $G$ 相加  

椭圆曲线上的两种基本运算规则为：  

**点相加**（$P \ne Q$）：  
- 斜率 $m = (y_2 - y_1) \cdot (x_2 - x_1)^{-1} \pmod p$  
- $x_3 = (m^2 - x_1 - x_2) \pmod p$  
- $y_3 = (m(x_1 - x_3) - y_1) \pmod p$  

**点倍增**（$P = Q$）：  
- 切线斜率 $m = (3x_1^2 + a) \cdot (2y_1)^{-1} \pmod p$  
- $x_3 = (m^2 - 2x_1) \pmod p$  
- $y_3 = (m(x_1 - x_3) - y_1) \pmod p$  

通过 Python 脚本实现 Double-and-Add 算法后，计算得到公钥 $K(x, y)$ 的具体值为：  
- $x = 13957031351290$  
- $y = 5520194834100$  

最终结果 $x + y = 19477226185390$，对应的 Flag 为：  
`cyberpeace{19477226185390}`

```python
import sys

# --- 椭圆曲线参数 ---
# 素数域的模数 p
p = 15424654874903
# 曲线方程 y^2 = x^3 + ax + b 的系数 a
a = 16546484
# 曲线方程的系数 b
b = 4548674875
# 基点 (生成元) G
G = (6478678675, 5636379357093)
# 私钥 k
private_key = 546768

# 定义无穷远点 O (群的单位元)
O = None

def modular_inverse(n, modulus):
    """
    计算 n 在模 modulus 下的乘法逆元。
    该函数使用了 Python 3.8+ 中 pow(n, -1, modulus) 的高效实现。
    """
    # 检查 Python 版本，为旧版本提供备用方案
    if sys.version_info < (3, 8):
        # 使用扩展欧几里得算法为旧版本 Python 计算模逆元
        g, x, y = egcd(n, modulus)
        if g != 1:
            raise Exception('模逆元不存在')
        return x % modulus
    return pow(n, -1, modulus)

def egcd(a, b):
    """扩展欧几里得算法"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def point_add(P, Q):
    """
    在椭圆曲线上执行点相加操作 (P + Q)。
    """
    # 处理无穷远点的情况
    if P == O:
        return Q
    if Q == O:
        return P

    x1, y1 = P
    x2, y2 = Q

    # 如果两个点的 x 坐标相同但 y 坐标不同，它们互为逆元，结果是无穷远点
    if x1 == x2 and y1 != y2:
        return O

    # 如果两个点相同，则执行点倍增
    if x1 == x2:
        return point_double(P)
    
    # --- P != Q 的情况 ---
    # 计算斜率 m = (y2 - y1) / (x2 - x1)
    # 分子
    m_num = (y2 - y1) % p
    # 分母的模逆元
    m_den = modular_inverse((x2 - x1) % p, p)
    # 斜率 m
    m = (m_num * m_den) % p

    # 计算新点的坐标
    # x3 = m^2 - x1 - x2
    x3 = (m * m - x1 - x2) % p
    # y3 = m(x1 - x3) - y1
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)

def point_double(P):
    """
    在椭圆曲线上执行点倍增操作 (2 * P)。
    """
    if P == O:
        return O

    x1, y1 = P

    # 如果 y1 是 0，切线是垂直的，结果是无穷远点
    if y1 == 0:
        return O

    # --- 计算切线斜率 m = (3*x1^2 + a) / (2*y1) ---
    # 分子
    m_num = (3 * x1 * x1 + a) % p
    # 分母的模逆元
    m_den = modular_inverse((2 * y1) % p, p)
    # 斜率 m
    m = (m_num * m_den) % p

    # 计算新点的坐标
    # x3 = m^2 - 2*x1
    x3 = (m * m - 2 * x1) % p
    # y3 = m(x1 - x3) - y1
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)

def scalar_multiply(k, P):
    """
    执行标量乘法 (k * P)，也称点乘。
    采用从左到右的 "Double-and-Add" 算法。
    """
    # 获取 k 的二进制表示，并去掉 '0b' 前缀
    k_bin = bin(k)[2:]
    
    # 初始化结果为基点 P
    current_point = P
    
    # 从二进制的第二位开始遍历
    for bit in k_bin[1:]:
        # 对当前点进行倍增
        current_point = point_double(current_point)
        # 如果当前位是 '1'，则再与基点 P 相加
        if bit == '1':
            current_point = point_add(current_point, P)
            
    return current_point

# --- 主计算流程 ---
if __name__ == "__main__":
    print("正在计算公钥 K = k * G ...")
    
    # 调用标量乘法函数计算公钥
    public_key = scalar_multiply(private_key, G)

    if public_key is not None:
        Kx, Ky = public_key
        print("\n计算完成！")
        print("="*30)
        print(f"公钥 K(x, y):")
        print(f"  x = {Kx}")
        print(f"  y = {Ky}")
        
        # 计算 flag 需要的值
        flag_value = Kx + Ky
        print(f"\nflag 值 (x + y): {flag_value}")
        
        # 格式化输出最终的 flag
        flag = f"cyberpeace{{{flag_value}}}"
        print(f"\n最终 Flag: {flag}")
        print("="*30)
    else:
        print("计算错误：结果为无穷远点。")
    
```
![[Pasted image 20250801153342.png]]

参考
https://ciphersaw.me/ctf-wiki/crypto/asymmetric/discrete-log/ecc/
https://blog.csdn.net/weixin_51555115/article/details/113200495



### **Williams's p+1 算法**

Williams's p+1 算法是一种整数分解算法，当待分解数 $N$ 的某个素因子 $p$ 满足 $p+1$ 是一个B-光滑数（即其所有素因子都小于一个常数B）时，该算法非常有效。

#### **核心思想 (基于费马小定理的 p-1 算法变体)**

作为对比和引入，经典的 Pollard's p-1 算法利用了 $p-1$ 是光滑数的特性。如果 $p$ 是 $N$ 的一个素因子，且 $p-1$ 是光滑的，即 $p-1 = \prod_{i=1}^k q_i^{\alpha_i}$，其中 $q_i$ 都是小素数。

1.  选择一个合适的平滑界 $B_1$。
2.  对每个素数 $q_i \le B_1$，找到最大的指数 $\beta_i$ 使得 $q_i^{\beta_i} \le B_1$。
3.  计算 $R = \prod_{i=1}^k q_i^{\beta_i}$。
4.  根据构造，显然有 $p-1 \mid R$。
5.  根据费马小定理，若 $\gcd(a, p) = 1$，则 $a^{p-1} \equiv 1 \pmod p$。
6.  因此，$a^R = a^{k(p-1)} \equiv (a^{p-1})^k \equiv 1^k \equiv 1 \pmod p$。
7.  这意味着 $p$ 是 $a^R-1$ 的一个因子，所以 $p$ 也必然是 $\gcd(N, a^R-1)$ 的一个因子。通过计算这个最大公约数，就有可能找到 $p$。

Williams's p+1 算法将此思想从乘法群 $\mathbb{Z}_p^*$ 推广到了基于卢卡斯序列的代数群上。

### **类卢卡斯序列 (Lucas-like Sequences)**

定义类卢卡斯序列是 p+1 算法的数学基础。

令 $P, Q$ 为整数，方程 $x^2 - Px + Q = 0$ 的两个根为 $\alpha$ 和 $\beta$。定义序列 $U_n$ 和 $V_n$ 如下：

$$U_n(P, Q) = \frac{\alpha^n - \beta^n}{\alpha - \beta}$$

$$V_n(P, Q) = \alpha^n + \beta^n$$

该序列的判别式为 $\Delta = (\alpha - \beta)^2 = P^2 - 4Q$。

#### **序列的基本性质与恒等式**

  * **线性递推关系:**

    $$
    \begin{cases}
    U_0=0, U_1=1 \\
    V_0=2, V_1=P
    \end{cases}
    \quad \text{and} \quad
    \begin{cases}
    U_{n+1} = P U_n - Q U_{n-1} \\
    V_{n+1} = P V_n - Q V_{n-1}
    \end{cases}
    $$

  * **倍角公式:**

    $$
    \begin{cases}
    U_{2n} = U_n V_n \\
    V_{2n} = V_n^2 - 2Q^n
    \end{cases}
    $$

  * **其他重要恒等式:**

    $$
    \begin{cases}
    U_{2n-1} = U_n^2 - Q U_{n-1}^2 \\
    V_{n} = P U_n - 2Q U_{n-1} \\
    \Delta U_n = P V_n - 2Q V_{n-1} \\
    U_{m+n} = U_m U_{n+1} - Q U_{m-1} U_n
    \end{cases}
    $$

  * **复合序列性质:**

    $$
    \begin{cases}
    U_n(V_k(P, Q), Q^k) = U_{nk}(P, Q) / U_k(P, Q) \\
    V_n(V_k(P, Q), Q^k) = V_{nk}(P, Q)
    \end{cases}
    $$

  * **与 $Q=1$ 的关系:**
    如果 $\gcd(N, Q) = 1$ 且 $P' \equiv P^2 Q^{-1} - 2 \pmod N$，则有：

    $$
    U_{2m}(P, Q) \equiv Q^{m-1} P U_m(P', 1) \pmod N
    $$

#### **扩展卢卡斯定理**

如果 $p$ 是一个奇素数，$p \nmid Q$，且勒让德符号 $\left(\frac{\Delta}{p}\right) = \epsilon \in \{-1, 0, 1\}$，则有：
$$U_{(p-\epsilon)m}(P, Q) \equiv 0 \pmod p$$
$$V_{(p-\epsilon)m}(P, Q) \equiv 2 Q^{m(1-\epsilon)/2} \pmod p$$
对于 p+1 算法，我们最关心的情况是 $\epsilon = -1$。这时，$p+1$ 出现在了下标中，使得 $U_{m(p+1)} \equiv 0 \pmod p$。

### **算法第一阶段：$p+1$ 是光滑数**

**假设**: $N$ 的一个未知素因子 $p$ 满足 $p+1$ 是一个 $B_1$-光滑数。
$$p+1 = \prod_{i=1}^k q_i^{\alpha_i} \quad \text{其中所有 } q_i \le B_1$$
**步骤**:

1.  计算 $R = \prod q_i^{\beta_i}$，其中 $q_i$ 是所有小于 $B_1$ 的素数，$\beta_i$ 是满足 $q_i^{\beta_i} \le N$ 的最大整数。这样可以确保 $p+1 \mid R$。
2.  选择一个参数 $P_0$，使得勒让德符号 $\left(\frac{P_0^2-4}{p}\right) = -1$。由于 $p$ 未知，我们随机选择 $P_0$ 并希望此条件成立。
3.  根据扩展卢卡斯定理，当 $\epsilon = -1$ 时，我们有 $p \mid U_{p+1}(P_0, 1)$。因为 $p+1 \mid R$，所以 $p \mid U_R(P_0, 1)$。
4.  直接计算 $U_R$ 在数值上可能非常巨大。一个更高效的方法是利用 $V_n$ 序列。当 $Q=1$ 时，如果 $p \mid U_R(P,1)$，则 $p \mid (V_R(P,1)-2)$。因此，我们的目标转化为计算 $V_R(P_0, 1) \pmod N$。

**计算 $V_R \pmod N$:**

令 $R = r_1 r_2 \cdots r_m$ (例如 $R$ 的素因子分解)。我们定义一个序列 $P_j$：
$$P_j \equiv V_{r_j}(P_{j-1}, 1) \pmod N \quad (j=1, 2, \ldots, m)$$
根据复合序列性质，最终可以得到：
$$P_m \equiv V_{r_m}(V_{r_{m-1}}(\cdots V_{r_1}(P_0)\cdots)) \equiv V_{r_m \cdots r_1}(P_0) \equiv V_R(P_0) \pmod N$$
为了计算单步的 $V_r(P) \pmod N$，我们使用类似于二进制幂的快速算法。
令 $r = \sum_{i=0}^t b_i 2^{t-i}$ 是 $r$ 的二进制表示。令 $f_0 = 1, f_{k+1} = 2f_k + b_{k+1}$，则 $f_t=r$。
我们从 $(V_1, V_0) = (P, 2)$ 开始，迭代计算 $(V_{f_{k+1}}, V_{f_{k+1}-1})$:

  * 如果 $b_{k+1} = 0$，则 $f_{k+1} = 2f_k$。我们需要计算 $(V_{2f_k}, V_{2f_k-1})$。
  * 如果 $b_{k+1} = 1$，则 $f_{k+1} = 2f_k+1$。我们需要计算 $(V_{2f_k+1}, V_{2f_k})$。

递推关系如下 ($Q=1$):

$$
\begin{cases}
V_{2f} \equiv V_f^2 - 2 \pmod N \\
V_{2f-1} \equiv V_f V_{f-1} - P \pmod N \\
V_{2f+1} \equiv P V_{2f} - V_{2f-1} \equiv P(V_f^2 - 2) - (V_f V_{f-1} - P) \pmod N
\end{cases}
$$通过这个过程，我们可以高效地计算出 $P_m = V_R(P_0) \pmod N$。

**最后，计算 $\gcd(P_m - 2, N)$。如果结果大于 1 且小于 $N$，我们就找到了 $N$ 的一个非平凡因子。**

### **算法第二阶段：$p+1$ 包含大素数因子**

**假设**: $p+1 = s \cdot M$，其中 $M$ 是 $B_1$-光滑的，而 $s$ 是一个落在 $[B_1, B_2]$ 区间内的大素数。第一阶段计算出的 $P_m \equiv V_M(P_0) \pmod N$。

**目标**: 从 $P_m$ 出发，检测是否存在一个素数 $s \in [B_1, B_2]$ 使得 $p \mid U_s(P_m, 1)$。

**步骤**:

1.  令 $P_m$ 为第一阶段的结果。定义 $U[n] \equiv U_n(P_m, 1) \pmod N$ 和 $V[n] \equiv V_n(P_m, 1) \pmod N$。
2.  预计算一系列 $U[d_j]$ 的值。$s_j$ 是 $[B_1, B_2]$ 区间内的素数序列，$d_j$ 是它们之间的差。
3.  我们希望计算 $g = \gcd(\prod_{s_j \in [B_1, B_2]} U_{s_j}(P_m), N)$。直接计算乘积非常低效。
4.  可以采用差分和批量处理的方式。定义一系列素数 $s_1, s_2, \ldots$ 和它们之间的差 $2d_i = s_{i+1} - s_i$。
5.  定义一个辅助序列 $T[s_i] \equiv \Delta U_{s_i}(P_m) \pmod N$。
6.  使用加法公式 $U_{m+n} = U_m U_{n+1} - U_{m-1} U_n$ 可以推导出 $T[s_i]$ 的递推关系：

$$
\begin{cases}
T[s_{i+1}] \equiv T[s_i] U[2 d_i+1] - T[s_i-1] U[2 d_i] \pmod N \\
T[s_{i+1}-1] \equiv T[s_i] U[2 d_i] - T[s_i-1] U[2 d_i-1] \pmod N
\end{cases}
$$

7.  可以分组计算 $T[s_i]$ 的乘积的 GCD：
    $$
    H_t = \gcd\left(\prod_{i=0}^{c-1} T[s_{i+t}], N\right)
    $$
    其中 $t$ 以步长 $c$ 取值。如果某个 $H_t > 1$，我们就找到了一个因子。

通过这两个阶段，Williams's p+1 算法能够有效地分解出其素因子 $p$ 满足 $p+1$ 是半光滑（只有一个大素因子）的合数 $N$。

代码实现:

```python
def mlucas(v, a, n):
    """ Helper function for williams_pp1().  Multiplies along a Lucas sequence modulo n. """
    v1, v2 = v, (v**2 - 2) % n
    for bit in bin(a)[3:]: v1, v2 = ((v1**2 - 2) % n, (v1*v2 - v) % n) if bit == "0" else ((v1*v2 - v) % n, (v2**2 - 2) % n)
    return v1

for v in count(1):
    for p in primegen():
        e = ilog(isqrt(n), p)
        if e == 0: break
        for _ in xrange(e): v = mlucas(v, p, n)
        g = gcd(v-2, n)
        if 1 < g < n: return g # g|n
        if g == n: break
```
例题
```python
from random import randint
from gmpy2 import *
from Crypto.Util.number import *
 
def getprime(bits):
    while 1:
        n = 1
        while n.bit_length() < bits:
            n *= next_prime(randint(1,1000))
        if isPrime(n - 1):
            return n - 1
 
m = bytes_to_long(b'flag{************************************}')
 
p = getprime(505)
q = getPrime(512)
r = getPrime(512)
assert m < q
 
n = p * q * r
e = 0x10001
d = invert(q ** 2, p ** 2)
c = pow(m, 2, r)
cipher = pow(c, e, n)
 
print(n)
print(d)
print(cipher)
 
 
'''
7941371739956577280160664419383740967516918938781306610817149744988379280561359039016508679365806108722198157199058807892703837558280678711420411242914059658055366348123106473335186505617418956630780649894945233345985279471106888635177256011468979083320605103256178446993230320443790240285158260236926519042413378204298514714890725325831769281505530787739922007367026883959544239568886349070557272869042275528961483412544495589811933856131557221673534170105409
7515987842794170949444517202158067021118454558360145030399453487603693522695746732547224100845570119375977629070702308991221388721952258969752305904378724402002545947182529859604584400048983091861594720299791743887521228492714135449584003054386457751933095902983841246048952155097668245322664318518861440
1618155233923718966393124032999431934705026408748451436388483012584983753140040289666712916510617403356206112730613485227084128314043665913357106301736817062412927135716281544348612150328867226515184078966397180771624148797528036548243343316501503364783092550480439749404301122277056732857399413805293899249313045684662146333448668209567898831091274930053147799756622844119463942087160062353526056879436998061803187343431081504474584816590199768034450005448200
'''


```



本题的破解依赖于一个环环相扣的数学逻辑链。

### 1. Williams's p+1 算法特例

标准的 Williams's p+1 算法适用于当待分解数 $N$ 的某个素因子 $p$ 满足 $p+1$ 是一个 $B$-光滑数（即所有素因子都小于 $B$）的场景。其原理基于卢卡斯序列 (Lucas Sequence)。

对于参数为 $(P, Q)$ 的卢卡斯序列 $U_k$ 和 $V_k$，有一个关键性质：  
若 $p$ 是一个素数，且勒让德符号 $\left(\frac{P^2-4Q}{p}\right) = -1$，则我们有：  
$$
U_{p+1}(P, Q) \equiv 0 \pmod{p}
$$

当 $Q=1$ 时，序列 $V_k$ 和 $U_k$ 存在关系，如果 $p \mid U_k(P,1)$，那么可以推导出 $V_k(P,1) \equiv 2 \pmod p$。这意味着 $p$ 是 $V_k(P,1)-2$ 的一个因子。因此，通过计算 $\gcd(V_k(P,1) - 2, N)$ 就有很大概率能找出因子 $p$。

**本题的捷径：**

常规 p+1 算法会构造一个巨大的数 $M$（所有小于光滑界限 $B_1$ 的素数幂的乘积），确保 $p+1 \mid M$，然后计算 $\gcd(V_M(P) - 2, N)$。

而本题存在一个“特例”或“捷径”。我们发现，当基底 $P=5$、指数 $k=2391$ 时，$\gcd(V_{2391}(5) - 2, N)$ 能够成功分解出一个因子。这强烈地暗示了，其中一个素因子 $p$ 满足 $p+1$ 是 $2391$ 的一个倍数。  
令 $p+1 = j \cdot 2391$（其中 $j$ 是某个整数），则有：  
$$
p \mid U_{p+1}(P, 1) = U_{j \cdot 2391}(P, 1)
$$
因为 $U_k$ 是一个可除序列，即若 $a \mid b$，则 $U_a \mid U_b$。所以 $U_{2391} \mid U_{j \cdot 2391}$。  
因此，我们必然有 $p \mid U_{2391}(P, 1)$，进而可以推断出：  
$$
p \mid \gcd(V_{2391}(P, 1) - 2, N)
$$
本题的解法正是利用了这个特性，通过暴力搜索小整数 `i` 来代替构造复杂的 `M`，从而在 `i=2391` 时找到了因子。

---

### 2. 求解 $q$ - 模平方逆元与模 $n$ 次方根

在通过第一步得到因子 $p$ 之后，我们利用题目给定的特殊关系式来求解 `q`。  
给定关系：  
$$
d \cdot q^2 \equiv 1 \pmod{p^2}
$$
这是一个关于变量 $q^2$ 的线性同余方程。我们的目标是解出 $q$。

**第一步：求模逆**  
为了消去 `d`，我们在方程两边同时乘以 `d` 在模 $p^2$ 下的乘法逆元，记为 $d^{-1}$：  
$$
(d^{-1} \cdot d) \cdot q^2 \equiv d^{-1} \cdot 1 \pmod{p^2}
$$
根据模逆的定义，$d^{-1} \cdot d \equiv 1 \pmod{p^2}$，所以上式简化为：  
$$
q^2 \equiv d^{-1} \pmod{p^2}
$$
在代码中，`q_2 = gmpy2.invert(d, p**2)` 正是计算了 $d^{-1} \pmod{p^2}$ 的值。

**第二步：求解模 $p^2$ 下的平方根**  
现在我们需要求解同余方程：  
$$
q^2 \equiv q_2 \pmod{p^2}
$$
这是一个模一个合数（$p^2$）的开方问题。常规的 Tonelli-Shanks 算法仅适用于模素数的情况。对于模素数幂（如 $p^2$）的情况，需要使用更复杂的算法，通常基于**亨泽尔引理 (Hensel's Lemma)**。该引理可以将模 $p$ 下的解“提升”到模 $p^k$ 下的解。

幸运的是，`sympy` 库的 `nthroot_mod(a, n, m)` 函数内置了这种高级算法，可以直接求解此类方程，让我们能够从 $q^2$ 的值精确地还原出 `q`。

---

### 3. 多素数 RSA 解密

在获得所有因子 `p, q, r` 后，还原中间值 `c` 的过程是一个标准的多素数 RSA 解密。  
加密过程为：  
$$
\text{cipher} \equiv c^e \pmod n
$$
其中 $n = p \cdot q \cdot r$，$e$ 是公钥指数。  
要解密，我们需要私钥指数 $d_{\text{rsa}}$。根据欧拉定理，对于多素数模数，欧拉函数为：  
$$
\phi(n) = \phi(p)\phi(q)\phi(r) = (p-1)(q-1)(r-1)
$$
私钥 $d_{\text{rsa}}$ 被定义为 $e$ 对 $\phi(n)$ 的模逆：  
$$
d_{\text{rsa}} \equiv e^{-1} \pmod{\phi(n)}
$$
得到 $d_{\text{rsa}}$ 后，即可通过以下运算解密得到 `c`：  
$$
c \equiv \text{cipher}^{d_{\text{rsa}}} \pmod n
$$

---

### 4. 最终解密 - 模素数平方根

最后一步是利用关系式 $c \equiv m^2 \pmod r$ 来还原最终的明文 `m`。  
这同样是一个求解模平方根的问题：  
$$
m^2 \equiv c \pmod r
$$
与第二步不同的是，这里的模数 `r` 是一个素数。我们可以直接使用 `sympy.nthroot_mod` 或其他标准算法（如 Tonelli-Shanks）来求解。

通常，一个数在模素数下开方会得到两个解，我们记为 $m_1$ 和 $m_2$。它们之间的关系是：  
$$
m_2 = r - m_1 \quad (\text{即 } m_2 \equiv -m_1 \pmod r)
$$
因为 $(-m_1)^2 \equiv m_1^2 \pmod r$。  
题目中的断言 `assert m < q` 在这里起到了关键作用，它为我们提供了一个唯一的标准来从两个候选解中筛选出正确的明文 `m`。


题解
```python
from Crypto.Util.number import long_to_bytes
from gmpy2 import mpz, isqrt, gcd, invert, powmod
from sympy import nthroot_mod
import time

# --- 题目给定的值 ---
n_int = 7941371739956577280160664419383740967516918938781306610817149744988379280561359039016508679365806108722198157199058807892703837558280678711420411242914059658055366348123106473335186505617418956630780649894945233345985279471106888635177256011468979083320605103256178446993230320443790240285158260236926519042413378204298514714890725325831769281505530787739922007367026883959544239568886349070557272869042275528961483412544495589811933856131557221673534170105409
d_given = 7515987842794170949444517202158067021118454558360145030399453487603693522695746732547224100845570119375977629070702308991221388721952258969752305904378724402002545947182529859604584400048983091861594720299791743887521228492714135449584003054386457751933095902983841246048952155097668245322664318518861440
cipher_int = 1618155233923718966393124032999431934705026408748451436388483012584983753140040289666712916510617403356206112730613485227084128314043665913357106301736817062412927135716281544348612150328867226515184078966397180771624148797528036548243343316501503364783092550480439749404301122277056732857399413805293899249313045684662146333448668209567898831091274930053147799756622844119463942087160062353526056879436998061803187343431081504474584816590199768034450005448200
e = 0x10001
A = [5, 7, 9, 11, 13]

def mlucas_gmpy(v_p, a, n):
    """使用 gmpy2 加速的 mlucas 函数"""
    # 确保所有输入都是gmpy2类型
    v_p, a, n = mpz(v_p), mpz(a), mpz(n)
    v1, v2 = v_p, (v_p * v_p - 2) % n
    for bit in bin(a)[3:]:
        if bit == '0':
            v1, v2 = (v1 * v1 - 2) % n, (v1 * v2 - v_p) % n
        else:
            v1, v2 = (v1 * v2 - v_p) % n, (v2 * v2 - 2) % n
    return v1

def find_factor_custom_sequence(n, bases, limit):
    """
    正确实现题目要求的特殊嵌套序列，并进行高速计算
    """
    n = mpz(n)
    for v_base in bases:
        print(f"--- 正在尝试初始基底 P_0 = {v_base} ---")
        v = mpz(v_base) # 初始化序列的第一个值 P_0
        for i in range(1, limit):
            # 核心逻辑：v_{new} = V_i(v_{old})
            # 使用 mlucas_gmpy 高效计算 V_i(v)
            v = mlucas_gmpy(v, i, n)
            
            # 检查是否找到因子
            g = gcd(v - 2, n)
            if 1 < g < n:
                print(f"成功！在 i = {i} 时发现因子。")
                return int(g)
            
            # 为了能实时看到进度，可以取消下面这行注释
            # if i % 100 == 0: print(f"已尝试到 i = {i}...")
    return None

# --- 主程序 ---
start_time = time.time()

print("--- 第一步：采用“特殊嵌套序列”策略寻找因子 ---")
# limit 设置为 5000 以确保覆盖 2391
p = find_factor_custom_sequence(n_int, bases=A, limit=5000)
print(f"找到因子 p = {p}\n")

if p is None:
    print("未能找到因子，程序终止。")
else:
    print("--- 第二步：利用 d 和 p 的关系直接求解 q ---")
    p = mpz(p)
    d_given = mpz(d_given)
    q_2 = invert(d_given, p**2)
    q_list = nthroot_mod(q_2, 2, p**2, all_roots=True)
    q = q_list[0]
    print(f"通过模平方根找到 q = {q}\n")

    print("--- 第三步：直接计算 r ---")
    r = n_int // p // q
    print(f"计算得到 r = {r}\n")

    print("--- 第四步：RSA解密，还原中间值 c ---")
    p, q, r, e, cipher = mpz(p), mpz(q), mpz(r), mpz(e), mpz(cipher_int)
    phi = (p - 1) * (q - 1) * (r - 1)
    d_rsa = invert(e, phi)
    c = powmod(cipher, d_rsa, n_int)
    print(f"计算得到 c = {c}\n")

    print("--- 第五步：求解模平方根，还原消息 m ---")
    m_list = nthroot_mod(c, 2, r, all_roots=True)
    m = m_list[0]
    print(f"找到 m = {m}\n")

    flag = long_to_bytes(int(m))

    end_time = time.time()
    print("="*50)
    print(f"总计耗时 {end_time - start_time:.2f} 秒。")
    print("\n🎉🎉🎉 解密成功！🎉🎉🎉")
    print(f"🚩 Flag: {flag.decode()}")
```
![[Pasted image 20250803115944.png]]


参考
https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_module_attack/