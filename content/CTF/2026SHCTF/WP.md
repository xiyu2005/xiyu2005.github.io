---
draft: true
---

# Misc

## Evan
题目信息 - Evan:so作为一位资深的CTF女师傅，却是个乙游的狂热爱好者，这是她珍藏已久的照片，找出flag
![[Pasted image 20260202140202.png]]
末尾的PK是压缩包，导出后猜密码是so，成功了。真的是猜的。甚至没用工具破解，蚌埠住了
SHCTF{Evan_1s_s0_h4nds0me!}

## Office


魔改过字母表的的base64
![[Pasted image 20260202142553.png]]

密文为lRy1m2qYkmewkTqDrneCoTCQoUiFqm7zqoeRoT7DqDCAqm7QsTqRuT3PqjWUt5e7
![[Pasted image 20260202143436.png]]

拖入cyberchef，base64 decode
SHCTF{MS_Office_is_the_best_office_software.wps}



## dida


## QRcode

LSB隐写。
![[Pasted image 20260202163146.png]]
得到FLAG_PART_1: SHCTF{55a23d24-

FLAG_PART_2: ABBB/AABBB/AAAAA/BBBBB/ABBBBA/BBBBA/B/AABBB/ABBB
这是培根密码/Morse电码。

b705-4e7b


![[Pasted image 20260202163733.png]]
part3
![[Pasted image 20260202165629.png]]

FLAG_PART_3: MkZkbDg3ZlY3ZEQxalNGenQyZUFYT3E0NmRrTXFV
![[Pasted image 20260202235918.png]]
-942e-bdd}
SHCTF{55a23d24-b705-4e7b-942e-bdd}
解决。


## 薇薇安photo
SHCTF{MV84Xzc0XzIwXzdfOTJfMTZfNV8xOF84Xzc=}
base64
SHCTF{1_8_74_20_7_92_16_5_18_8_7}
根据提示用元素周期表对应
SHCTF{H_O_W_CA_N_U_S_B_AR_O_N}
但是该喷这个出题人语文真烂啊，我以为是提醒SHCTF大写，tmd是里面内容大写，磕了半个小时以为还有藏东西



## 资源平权
明文攻击[[Misc内训#1.2明文攻击]]

用winrar把这个压缩包拖进去可以直接提取出里面的资源使用说明.txt，保存出来重命名为txt
![[Pasted image 20260202200245.png]]
![[Pasted image 20260202195931.png]]
![[1acaeb30b01ee87b0afc5ba057d0291b.png]]


## Open_my_puff
![[Pasted image 20260202225415.png]]
隐藏文本
keyA:12345678
keyB:qwertyui
keyC:asdfghjk
2.png末尾提示OpenPuffv4.01，下载来用
![[Pasted image 20260202225559.png]]

显示flag.txt与flag.zip
flag.txt
niimmccw????zfip



## 提问前先搜索
![[Pasted image 20260203001501.png]]
请输入文本...

# Reverse
## a cup of tea

ida打开

```c
__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  _DWORD v4[4]; // [rsp+0h] [rbp-30h] BYREF //数组v4
  char dest[24]; // [rsp+10h] [rbp-20h] BYREF //flag内容
  unsigned __int64 v6; // [rsp+28h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  sub_1209(a1, a2, a3);
  v4[0] = 0;
  v4[1] = 0;
  v4[2] = 0;
  v4[3] = 0;
  sub_12D3(v4); //应该是输入函数，输入数组v4
  strcpy(dest, src);
  if ( !(unsigned int)sub_1439(v4) ) //判断函数sub_1439,进去看看
  {
    puts("password error");
    exit(1);
  }
  puts("password correct");
  printf("here is your flag: SHCTF{%s}\n", dest);
  return 0;
}
```

看几个关键函数和数据
```c
_BOOL8 __fastcall sub_1439(_DWORD *a1)
{
  sub_134E(a1, aWelcomeToShctf_0);
  if ( *a1 != -1699360031 || a1[1] != -1120419751 )
    return 0;
  sub_134E(a1 + 2, aWelcomeToShctf_0);
  return a1[2] == -1515845715 && a1[3] == -1804683212;
}
```
查看aWelcomeToShctf_0内容
.data:0000000000004010 aWelcomeToShctf_0 db 'welcome_to_SHCTF',0
查看134E函数的逻辑
```c
__int64 __fastcall sub_134E(unsigned int *a1, _DWORD *a2)
{
  __int64 result; // rax
  unsigned int v3; // [rsp+1Ch] [rbp-24h]
  unsigned int v4; // [rsp+20h] [rbp-20h]
  int v5; // [rsp+24h] [rbp-1Ch]
  unsigned int i; // [rsp+28h] [rbp-18h]

  v3 = *a1;
  v4 = a1[1];
  v5 = 0;
  for ( i = 0; i <= 0x1F; ++i )
  {
    v5 -= 1640531527;
    v3 += (v4 + v5) ^ (16 * v4 + *a2) ^ ((v4 >> 5) + a2[1]);
    v4 += (v3 + v5) ^ (16 * v3 + a2[2]) ^ ((v3 >> 5) + a2[3]);
  }
  *a1 = v3;
  result = v4;
  a1[1] = v4;
  return result;
}
```

```c
int sub_1209()
{
  puts("Welcome to SHCTF 2025!");
  puts("this is a signin challenge");
  return puts("plz input the correct password");
}


char *__fastcall sub_12D3(__int64 a1)
{
  __isoc99_scanf("%16s", src);
  if ( strlen(src) != 16 )
  {
    puts("password length error");
    exit(1);
  }
  sub_1241(a1, src);
  return src;
}


```


所以
```
	v5 -= 1640531527;
    v3 += (v4 + v5) ^ (16 * v4 + *a2) ^ ((v4 >> 5) + a2[1]);
    v4 += (v3 + v5) ^ (16 * v3 + a2[2]) ^ ((v3 >> 5) + a2[3]);
```
把逻辑反过来

v1 -= (v0 + sum) ^ (v0 * 16 + k2) ^ ((v0 >> 5) + k3)
v0 -= (v1 + sum) ^ (v1 * 16 + k0) ^ ((v1 >> 5) + k1)
sum = sum + 1640531527

解密脚本
```python
import struct
from ctypes import c_uint32

# 1. 准备密文
# 从 main 函数中提取的比较数值
# v4[0], v4[1], v4[2], v4[3]
cipher_values = [
    -1699360031, 
    -1120419751, 
    -1515845715, 
    -1804683212
]
# 转为无符号整数
cipher = [c & 0xffffffff for c in cipher_values]

# 2. 准备密钥
# 字符串 "welcome_to_SHCTF" 转为 4 个 32位整数 (Little Endian)
key_str = b'welcome_to_SHCTF'
key = struct.unpack('<4I', key_str)

# 3. TEA 解密函数
def decrypt_tea(v, k):
    v0 = c_uint32(v[0])
    v1 = c_uint32(v[1])
    
    delta = 1640531527
    
    # 也就是加密时 sum 的最终状态
    # 因为加密代码是 v5 -= delta，循环 32 次
    # 所以初始 sum = 0 - (delta * 32)
    sum_val = c_uint32(0 - (delta * 32))
    
    # 密钥拆分
    k0, k1, k2, k3 = k[0], k[1], k[2], k[3]
    
    # 逆向 32 轮
    for _ in range(32):
        # 对应原代码：v4 += (v3 + v5) ^ (16 * v3 + a2[2]) ^ ((v3 >> 5) + a2[3]);
        # 解密：v1 -= ... (注意这里 v1 对应 v4, v0 对应 v3)
        # 必须先解密 v1 (因为加密时 v1 是后加密的)
        part1 = (v0.value + sum_val.value)
        part2 = (v0.value * 16 + k2)
        part3 = ((v0.value >> 5) + k3)
        v1.value -= (part1 ^ part2 ^ part3)
        
        # 对应原代码：v3 += (v4 + v5) ^ (16 * v4 + *a2) ^ ((v4 >> 5) + a2[1]);
        # 解密：v0 -= ...
        part1 = (v1.value + sum_val.value)
        part2 = (v1.value * 16 + k0)
        part3 = ((v1.value >> 5) + k1)
        v0.value -= (part1 ^ part2 ^ part3)
        
        # 对应原代码：v5 -= 1640531527;
        # 解密：sum += delta (恢复 sum 到上一轮的状态)
        sum_val.value += delta
        
    return v0.value, v1.value

# 4. 执行解密
# 前半部分
dec1 = decrypt_tea(cipher[0:2], key)
# 后半部分
dec2 = decrypt_tea(cipher[2:4], key)

# 5. 组合并打印
flag_data = struct.pack('<4I', dec1[0], dec1[1], dec2[0], dec2[1])
print("Flag content:", flag_data)

try:
    print(f"Flag: SHCTF{{{flag_data.decode()}}}")
except:
    print("解码失败，请检查脚本")
```


# Crypto

分析e指数很大，考虑低解密指数d攻击
### 1. 题目分析

*   **参数大小**：
    *   $n$ 是两个 512 位素数的乘积，约为 1024 位。
    *   $e$ 是一个 1019 位的素数。
    *   在 RSA 中，满足 $ed \equiv 1 \pmod{\phi(n)}$。
*   **攻击原理**：
    当解密指数 $d$ 满足 $d < \frac{1}{3}n^{1/4}$ 时，可以使用 **Wiener's Attack**（维纳攻击）通过 $e/n$ 的连分数展开快速找回 $d$。
    即使 $d$ 稍微大一点（例如 $d < n^{0.292}$），也可以使用基于格规约（LLL 算法）的 **Boneh-Durfee Attack**。
    在本题中，$e$ 达到了 1019 位，而 $n$ 为 1024 位。通常情况下，如果 $e$ 特别大，根据 $ed = k\phi(n) + 1$，为了使等式成立，$d$ 往往会比较小。

### 2. 推导过程

1.  **RSA 基本公式**：
    $ed - k\phi(n) = 1$
    因为 $\phi(n) \approx n$，所以：
    $\frac{e}{n} \approx \frac{k}{d}$
2.  **连分数原理**：
    通过对 $\frac{e}{n}$ 进行连分数展开，得到的渐进分数（Convergents）中，有一个分数 $\frac{k}{d}$ 极大概率就是我们需要的。
3.  **验证条件**：
    对于每一个可能的渐进分数 $\frac{k}{d}$：
    *   计算可能的 $\phi(n) = \frac{ed-1}{k}$。
    *   由于 $n = pq$ 且 $\phi(n) = (p-1)(q-1) = n - (p+q) + 1$。
    *   设 $s = p+q = n - \phi(n) + 1$。
    *   根据一元二次方程根与系数的关系，$p$ 和 $q$ 是方程 $x^2 - sx + n = 0$ 的两个根。
    *   如果判别式 $\Delta = s^2 - 4n$ 是一个完全平方数，说明找到了正确的 $d$。


```python
import gmpy2
from Crypto.Util.number import long_to_bytes

n = 107464134871680646151655304067173578951022679613817744422854142736895193478923970402314237869266898585661396817719803005109183572552933963881756199330890085692291647461683934019264121186823772581796061998307778635680038707808422026396560620912393186072263186503236380890048319797143644270579169484448179083299
e = 3924586561728843234261049280560557566669922961436496251423249382498887294225142535297862819865029081145630384268177735578769958711287734205364353929040337350836000661255957087233897675207507752217828489549059197109918195953230752720210793300168746820366115929509596904295875481061789801178045962611893883689
c = 4557192604704814579224198928010541193712311907197292139423304635523945088581321950910727673367241811197226152299201713883344661436550024661781925551129803469824570154317098612833694631836257698682075695287756551674264966935203485636255394639674521955953445322493019052791894426980946209383266707043869522774

# 连分数展开函数
def continued_fraction(n, d):
    res = []
    while d:
        res.append(n // d)
        n, d = d, n % d
    return res

# 渐进分数生成函数
def convergents(cf):
    nm = [0, 1]
    dn = [1, 0]
    for x in cf:
        nm.append(x * nm[-1] + nm[-2])
        dn.append(x * dn[-1] + dn[-2])
        yield nm[-1], dn[-1]

def wiener_attack(e, n):
    cf = continued_fraction(e, n)
    for k, d in convergents(cf):
        if k == 0: continue
        # 根据公式 ed - k*phi = 1 推导 phi
        if (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            # x^2 - (n-phi+1)x + n = 0
            s = n - phi + 1
            delta = s*s - 4*n
            if delta > 0:
                sqrt_delta = gmpy2.isqrt(delta)
                if sqrt_delta * sqrt_delta == delta:
                    # 判别式为完全平方数，说明找到了正确的 d
                    return d
    return None

# 执行攻击
d = wiener_attack(e, n)

if d:
    print(f"找到解密指数 d: {d}")
    m = pow(c, d, n)
    print(f"Flag: {long_to_bytes(m).decode()}")
else:
    print("Wiener Attack 失败，尝试 Boneh-Durfee 攻击或其他方法。")
```

### 4. 结论
由于本题中 $e$ 的值极其庞大（接近 $n$），根据 RSA 的数学特性，这通常暗示 $d$ 处于 Wiener 攻击的有效范围内。运行上述脚本即可通过连分数展开找到解密密钥 $d$，进而解密密文获得 Flag。
# OSINT
## 1
![[Pasted image 20260202155147.png]]