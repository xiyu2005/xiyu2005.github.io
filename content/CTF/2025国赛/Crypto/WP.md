## ECDSA
```python
digest_int = int.from_bytes(sha512(b"Welcome to this challenge!").digest(), "big")
# 将固定字符串的SHA512哈希转为大整数

# 行9：获取NIST521p椭圆曲线的“阶”（order）
curve_order = NIST521p.order
# 背景：椭圆曲线的阶是基点G生成的子群大小（大质数），ECDSA私钥必须满足 1 < 私钥 < 曲线阶

# 行10：哈希整数对曲线阶取模，得到合法的私钥整数
priv_int = digest_int % curve_order


# 背景：NIST521p私钥是521位（65.125字节），66字节是为了对齐，确保字节串长度符合ecdsa库要求
priv_bytes = long_to_bytes(priv_int, 66)

# 行12：从字节串生成ECDSA私钥对象
sk = SigningKey.from_string(priv_bytes, curve=NIST521p)

# 行13：从私钥导出公钥（验证密钥）对象
vk = sk.verifying_key

# 生成public.pem
f_pub = open("public.pem", "wb")
f_pub.write(vk.to_pem())
f_pub.close()
```

```python

def nonce(i):  # 行17：定义生成ECDSA签名随机数k（nonce）的函数，参数i是消息索引
    # 行18：生成nonce的种子（固定前缀+索引的SHA512哈希）
    seed = sha512(b"bias" + bytes([i])).digest()
    # 拆解：
    # - b"bias" + bytes([i])：固定前缀拼接单字节索引（i从0到59）
    # - sha512(...).digest()：生成64字节种子
    # 关键：这个nonce是“可预测的”（非真随机），是代码的“漏洞”（用于后续攻击）
    
    # 行19：种子转大整数（大端序），作为nonce k
    k = int.from_bytes(seed, "big")
    
    # 行20：返回nonce k
    return k
# 背景：ECDSA签名必须用唯一、不可预测的k，否则会泄露私钥（这段代码故意设计不安全的k）

# 行21：生成60条消息的列表（列表推导式）
msgs = [b"message-" + bytes([i]) for i in range(60)]
# 拆解：
# - range(60)：i从0到59
# - bytes([i])：将整数i转为单字节（如i=0→b'\x00'，i=1→b'\x01'）
# - 拼接后：i=0→b"message-\x00"，i=1→b"message-\x01"，共60条唯一消息

# 行22：初始化空列表，存储（消息十六进制，签名十六进制）元组
sigs = []

# 行23：遍历消息，i是索引，msg是消息字节串
for i, msg in enumerate(msgs):
    # 行24：调用nonce函数生成当前消息的k值
    k = nonce(i)
    
    # 行25：用私钥+指定k对消息签名，得到签名字节串
    sig = sk.sign(msg, k=k)
    # 背景：默认情况下ecdsa库会自动生成安全的k，这里手动指定不安全的k
    
    # 行26：消息/签名转十六进制字符串，存入sigs列表
    sigs.append((binascii.hexlify(msg).decode(), binascii.hexlify(sig).decode()))
    # 拆解：
    # - binascii.hexlify(字节串)：转十六进制字节串（如b"abc"→b'616263'）
    # - .decode()：字节串转字符串（方便文本文件存储）

f_sig = open("signatures.txt", "w")
for m, s in sigs:
    f_sig.write("%s:%s\n" % (m, s))
f_sig.close()

```



#ECDSA签名算法的核心步骤

*   $d$：**私钥**。这是一个非常大的整数，必须严格保密。
*   $G$：椭圆曲线上的一个**基点**。这是一个公开的、标准化的参数。
*   $Q$：**公钥**。它是一个点，通过计算 $Q = d \cdot G$ 得到。
*   $n$：椭圆曲线基点的**阶 (Order)**。这是一个非常大的素数，也是一个公开的参数。所有的计算都是在模 $n$ 的意义下进行的。
*   $m$：待签名的**消息**。
*   $h$：消息 $m$ 的哈希值，也是一个整数。即 $h = \text{hash}(m)$。

**2. 签名过程**

生成签名 $(r, s)$ 的过程如下：

*   第一步：生成一个一次性的秘密数字 $k$
    选择一个随机的、保密的整数 $k$，满足 $1 \le k < n$

*   **第二步：计算 $r$**
    计算椭圆曲线上的点 $P = k \cdot G$。取这个点 $P$ 的 x 坐标，并对 $n$ 取模，得到的值就是 $r$。
    $$ r = x_P \pmod{n} $$
    如果 $r=0$，则需要重新选择一个 $k$。

*   **第三步：计算 $s$**
    使用以下公式计算 $s$：
    $$ s \equiv k^{-1}(h + r \cdot d) \pmod{n} $$
    其中 $k^{-1}$ 是 $k$ 在模 $n$ 意义下的**乘法逆元**。如果 $s=0$，也需要重新选择一个 $k$。

最终的签名就是数对 $(r, s)$。

---

### **攻击原理：利用已知的 $k$ 求解私钥 $d$**

此题中，`nonce` 函数的实现是有缺陷的，它生成的 $k$ 是完全可以预测的。这意味着，作为攻击者，我们**知道了 $k$ 的值**。

现在，我们来分析一下第三步的签名公式，看看我们拥有什么，想要求什么。

$$ s \equiv k^{-1}(h + r \cdot d) \pmod{n} $$


*   **已知量**:
    *   $s,r$: 从 `signatures.txt` 文件中读到。

    *   $k$: 通过运行题目中给出的 `nonce(i)` 函数自己计算出来。
    *   $h$: 我们可以拿到消息原文 `m`，然后用同样的哈希函数（SHA-512）计算出哈希值 $h$。
    *   $n$: 这是椭圆曲线的公开参数，我们知道。

*   **未知量**:
    *   $d$: **私钥**

现在，我们有了一个只包含一个未知数 $d$ 的线性同余方程。我们的任务就是通过代数变换来解出 $d$。

$$ s \equiv k^{-1}(h + r \cdot d) \pmod{n} $$
$$ s \cdot k \equiv k \cdot k^{-1}(h + r \cdot d) \pmod{n} $$
$$ s \cdot k \equiv h + r \cdot d \pmod{n} $$
$$ s \cdot k - h \equiv r \cdot d \pmod{n} $$
$$ r^{-1}(s \cdot k - h) \equiv r^{-1} \cdot r \cdot d \pmod{n} $$
$$ d \equiv r^{-1}(s \cdot k - h) \pmod{n} $$

```python
from ecdsa import SigningKey, NIST521p
from ecdsa.util import sigdecode_string
from hashlib import sha512, sha1
import binascii
import hashlib

n = NIST521p.order

# 抄过来
def nonce(i):
    seed = sha512(b"bias" + bytes([i])).digest()
    return int.from_bytes(seed, "big")

# 读取第一个签名
with open("signatures.txt", "r") as f:
    msg_hex, sig_hex = f.readline().strip().split(":")
    msg = binascii.unhexlify(msg_hex)
    sig_bytes = binascii.unhexlify(sig_hex)

# 解析签名
r, s = sigdecode_string(sig_bytes, n)

# 计算nonce和消息哈希
k = nonce(0)
h = int.from_bytes(sha1(msg).digest(), "big") % n

# 根据推导的公式恢复私钥
r_inverse = pow(r, -1, n)
d = (s * k - h) * r_inverse % n

flag = f"flag{{{hashlib.md5(str(d).encode()).hexdigest()}}}"
print(flag)
```

flag{581bdf717b780c3cd8282e5a4d50f3a0}





EzFlag
```c++
__int64 __fastcall f(unsigned __int64 a1)  // a1是输入（即v11，无符号正整数）
{
__int64 v2; // 临时变量，仅存每次循环的v4旧值
unsigned __int64 i; // 循环计数器，从0开始
__int64 v4; // 迭代变量1，初始值1，每次循环更新
__int64 v5; // 迭代变量2，初始值0，每次循环更新（最终作为取字符的索引）
v5 = 0;     // 初始化v5为0
v4 = 1;     // 初始化v4为1
for ( i = 0; i < a1; ++i )  // 循环次数 = 输入a1的值（执行a1次循环）
{
v2 = v4;                    // 步骤1：把当前v4的值存到临时变量v2（保存旧值）
v4 = ((_BYTE)v5 + (_BYTE)v4) & 0xF;  // 步骤2：计算新的v4（核心运算）
v5 = v2;                    // 步骤3：把v4的旧值（v2）赋值给v5，更新v5
}
// 循环结束后，用最终的v5作为索引，从字符串K中取第v5个字符返回
return *(unsigned __int8 *)std::string::operator[](&K, v5);
}
```


寻找字符串K = "012ab9c3478d56ef"
![[Pasted image 20260131180845.png]]

```python

def solve():
    K = "012ab9c3478d56ef"
    seq = [0,1,1,2,3,5,8,13,5,2,7,9,0,9,9,2,11,13,8,5,13,2,15,1]
    flag = ""
    v11 = 1
    for i in range(32):
        index = v11 % 24
        seq_val = seq[index]
        char_val = K[seq_val]
        flag += char_val
        if i in [7, 12, 17, 22]:
                flag += "-"

        # v11 *= 8LL; v11 += i + 64;
        v11 = v11 * 8 + i + 64
    print("Flag:{" + flag + "}")

def f(a):
    v5=0;v4=1
    for i in range(0,a):
        v2 = v4
        v4_next = (v5+v4) % 16
        v5 = v2
        v4 = v4_next
    return v5

# #输出f(a)前50项
# for i in range(100):
#     print(f(i), end=',')

solve()
```
Flag:{10632674-1d219-09f29-147a2-760632674}


或者找到std::this_thread::sleep_for...
![[Pasted image 20260131185812.png]]

![[Pasted image 20260131192349.png]]
![[Pasted image 20260131192310.png]]

55换成C3
可以做到进入函数后就直接rtn掉它。
但是这个sleep并不是主要耗时，计算大数耗时间才是主要的问题（所以并没有成功也
