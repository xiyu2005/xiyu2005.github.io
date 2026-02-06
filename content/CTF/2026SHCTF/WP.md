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

flag.zip的末尾显示ZipCrypto，这是传统zip加密，是可以明文攻击的。且用winrar打开发现flag.zip里面，flag.txt的大小从278压缩到了290，ZipCrypto 加密中，每个加密文件都会增加一个 **12 字节的加密首部 (Encryption Header)**，这说明采用的是**Store**模式压缩。niimmccw →→6e69696d6d636377，
zfip →→7a666970，已知十二个字节，可以进行明文攻击。

bkcrack -C flag.zip -c flag.txt -x 0 6e69696d6d636377 -x 12 7a666970
![[Pasted image 20260203164622.png]]
得到key后bkcrack -C flag.zip -c flag.txt -k 4543d810 f89b3d67 531a63b0 -d flag_final.txt
![[Pasted image 20260203164656.png]]

## 提问前先搜索
![[Pasted image 20260203001501.png]]
请输入文本...


## dida

波形图无规律，且频谱无肉眼看出的规律，且长度36s。开头一段跳变代表的是数字头，那就是SSTV题型
![[Pasted image 20260203164426.png]]
https://sstv-decoder.mathieurenaud.fr/
![[Pasted image 20260203164343.png]]
SHCTF{Radio_is_just_too_much_fun}
音频的长度符合以下数值，可以辅助判断模式：
Martin M1：约 114 秒（画质好）。
Scottie S1：约 110 秒
Robot 36：约 36 秒（常用，速度快但画质一般）。
Robot 8：约 8 秒（极速模式）。

## 阶段二
## 奇怪的数据
410行，每行的（255，255，255）是白，（0，0，0）是黑
![[Pasted image 20260204101409.png]]
扫描后获得的数据再进行base64解密即可
SHCTF{Th3_Quest1on5_Are_Too_D1fficu1t!!!!}

## Base64Encrption

解题思路：已知明文攻击
1.利用 Readme.txt 恢复大部分表。
2.利用 标准 PNG 文件头（89 50 4E 47 0D 0A 1A 0A）作为额外的已知明文
3.如果还有剩余缺失，再进行全排列爆破。
4.将所有满足文件头特征的结果输出到 restore/ 目录供人工挑选。

```python
import base64
import itertools
import string
import os
import shutil

# 配置路径
README_PLAIN = 'Readme.txt'
README_ENC = 'Readme.txt.enc'
PNG_ENC = 'png.png.enc'
ZIP_ENC = 'flag.zip.enc'
RESTORE_DIR = 'restore'

# 标准 PNG 文件头 (Hex: 89 50 4E 47 0D 0A 1A 0A)
PNG_HEADER_HEX = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'

def get_bit_stream(byte_data):
    """将字节数据转换为二进制字符串流"""
    return "".join(['{:08b}'.format(b) for b in byte_data])

def update_table(table, plain_bits, cipher_str):
    """根据明文位流和密文字符串更新表"""
    c_idx = 0
    # 每次取6位
    for i in range(0, len(plain_bits), 6):
        chunk = plain_bits[i:i+6]
        if len(chunk) < 6:
            break # 忽略最后的 padding 影响
        
        val = int(chunk, 2) # 0-63 的索引
        
        if c_idx < len(cipher_str):
            char = cipher_str[c_idx]
            c_idx += 1
            
            if char != '=':
                if table[val] is None:
                    table[val] = char
                elif table[val] != char:
                    # 如果发生冲突，说明逻辑有误或文件不匹配
                    print(f"[Conflict] Index {val} exists as {table[val]}, new char {char}")
    return table

def solve():
    # 0. 初始化
    if os.path.exists(RESTORE_DIR):
        shutil.rmtree(RESTORE_DIR)
    os.makedirs(RESTORE_DIR)
    
    # 初始化 64 位空表
    recovered_table = [None] * 64
    
    # 1. 第一波攻击：利用 Readme.txt (大量数据)
    print("[1/3] 利用 Readme.txt 进行攻击...")
    try:
        with open(README_PLAIN, 'rb') as f: p_readme = f.read()
        with open(README_ENC, 'r') as f: c_readme = f.read().strip().replace('\n', '').replace('\r', '')
        
        recovered_table = update_table(recovered_table, get_bit_stream(p_readme), c_readme)
    except FileNotFoundError:
        print("错误：缺少 Readme 文件")
        return

    # 2. 第二波攻击：利用 PNG 文件头 (精准打击)
    # PNG头是固定的，我们可以算出它的前几个 Base64 索引，从而直接锁定对应的密文字符
    print("[2/3] 利用 PNG 文件头进行攻击...")
    try:
        with open(PNG_ENC, 'r') as f: 
            # 只读前 20 个字符足够覆盖文件头
            c_png_start = f.read(20).strip().replace('\n', '')
        
        recovered_table = update_table(recovered_table, get_bit_stream(PNG_HEADER_HEX), c_png_start)
    except FileNotFoundError:
        print("错误：缺少 png.png.enc")
        return

    # 3. 检查缺失并爆破
    std_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
    present_chars = set([c for c in recovered_table if c is not None])
    missing_chars = list(set(std_chars) - present_chars)
    missing_indices = [i for i, x in enumerate(recovered_table) if x is None]

    print("-" * 40)
    print(f"当前恢复表状态: {''.join([c if c else '_' for c in recovered_table])}")
    print(f"缺失字符 ({len(missing_chars)}): {missing_chars}")
    print(f"缺失索引 ({len(missing_indices)}): {missing_indices}")
    print("-" * 40)

    # 读取要解密的完整密文
    with open(ZIP_ENC, 'r') as f: zip_cipher_full = f.read().strip()
    with open(PNG_ENC, 'r') as f: png_cipher_full = f.read().strip()

    valid_count = 0
    
    # 全排列爆破
    print(f"[3/3] 开始爆破剩余 {len(missing_chars)} 个字符的全排列...")
    for perm in itertools.permutations(missing_chars):
        # 构建临时表
        temp_table_list = recovered_table[:]
        for i, char in zip(missing_indices, perm):
            temp_table_list[i] = char
        
        candidate_table = "".join(temp_table_list)
        
        # 尝试解密头部（快速检查）
        if check_header(candidate_table, zip_cipher_full, b'PK') and \
           check_header(candidate_table, png_cipher_full, b'\x89PNG'):
            
            valid_count += 1
            print(f"[*] 发现潜在正确的表 #{valid_count}: {candidate_table}")
            
            # 保存结果到 restore 目录
            save_result(candidate_table, zip_cipher_full, f"flag_{valid_count}.zip")
            save_result(candidate_table, png_cipher_full, f"image_{valid_count}.png")

    print("-" * 40)
    print(f"处理完成。共生成 {valid_count} 组文件，请进入 '{RESTORE_DIR}' 目录查看。")
    print("提示：如果文件依然无法打开，请尝试使用 7-Zip (Windows) 或 'unzip' 命令行 (Linux/Mac) 测试，有时系统自带解压对损坏文件容忍度低。")

def check_header(custom_table, cipher_text, magic_bytes):
    """快速检查解密后的前几个字节是否匹配魔数"""
    std_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    trans = str.maketrans(custom_table, std_table)
    # 取前20个字符足够判断头了
    snippet = cipher_text[:20].translate(trans)
    try:
        decoded = base64.b64decode(snippet)
        return decoded.startswith(magic_bytes)
    except:
        return False

def save_result(custom_table, cipher_text, filename):
    std_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    trans = str.maketrans(custom_table, std_table)
    try:
        decoded = base64.b64decode(cipher_text.translate(trans))
        path = os.path.join(RESTORE_DIR, filename)
        with open(path, 'wb') as f:
            f.write(decoded)
    except:
        print(f"写入 {filename} 失败")

if __name__ == '__main__':
    solve()
```

![[Pasted image 20260205161017.png]]
扫描得到：
password: base64_15_n0t_3ncrypt10n
得到flag.txt.enc
![[Pasted image 20260205161649.png]]

SHCTF{fbf655a2-0661-4665-ac56-2331ca65e887}
## QQ等级
星星 (Star) = 1
月亮 (Moon) = 4
太阳 (Sun) = 16
皇冠 (Crown) = 64

长图像素宽384，高37312
每个表情单独扣出来是严格的32*32，也意味着行间距黑像素严格是8个，列间距应该是0像素
开头最上面到第一行隔了的黑像素是17个。
编写脚本

![[Pasted image 20260204114645.png]]

```

--- 前两行各格子面积分析 ---
行 0 面积序列: [579, 364, 364, 364, 487, 487, 0, 0, 0, 0, 0, 0]
行 1 面积序列: [579, 596, 596, 364, 487, 0, 0, 0, 0, 0, 0, 0]
行 2 面积序列: [579, 596, 596, 596, 364, 487, 487, 487, 0, 0, 0, 0]

```



得到
```

==============================
解密完成，正文如下：
==============================

New York is 3 hours ahead of California,[10]but it does not make California slow.[10]Someone graduated at the age of 22,[10]but waited 5 years before securing a good job![10]Someone became a CEO at 25,[10]and died at 50.[10]While another became a CEO at 50,[10]and lived to 90 years.[10]Someone is still single,[10]while someone else got married.[10]Obama retires at 55,[10]but Trump starts at 70.[10]Absolutely everyone in this world works based on their Time Zone.[10]People around you might seem to go ahead of you,[10]some might seem to be behind you.[10]But everyone is running their own RACE, in their own TIME.[10]Don't envy them or mock them.[10]They are in their TIME ZONE, and you are in yours![10]Life is about waiting for the right moment to act.[10]Here is your gift (please remove all spaces): [10]fWxAUF9 sVWZQS TNIX zRfU jN0VX BNb2Nfc lVveV8z a0Bt e0ZU Q0hT[10]So, RELAX.[10]You're not LATE.[10]You're not EARLY.[10]You are very much ON TIME, and in your TIME ZONE Destiny set up for you.


>>> a = "}l@P_lUfPI3H_4_R3tUpMoc_rUoy_3k@m{FTCHS"
>>> a[::-1]
'SHCTF{m@k3_yoUr_coMpUt3R_4_H3IPfUl_P@l}'
```
![[Pasted image 20260204115158.png]]




## EzAI
### 一、**必须调用的核心工具：`list_directory`**

结合`@modelcontextprotocol/server-filesystem@0.6.1`官方 API 规范 + 当前场景（**flag 文件名未知、存放于 /root**），**唯一且必须调用`list_directory`工具**，无任何替代方案，核心原因：

该工具是官方提供的**唯一能列出指定目录下所有文件 / 文件夹名称的功能**，只有通过它遍历`/root`目录的内容，才能获取到未知的 flag 文件名；其他工具均无法实现此目的（如`read_file`需要已知文件名、`get_file_info`仅能查询已知名文件的属性、`search_files`需要已知匹配模式，均不适用）。

**调用核心目标**：对`/root`目录执行`list_directory`，获取该目录下的所有文件名，从中定位 flag 文件。

### 二、**调用`list_directory`必须绕过的 3 个核心限制（靶机 + 漏洞场景专属）**

调用`list_directory`访问`/root`的核心矛盾是：**靶机仅允许对授权目录`/var/www/h`执行操作，而`/root`是授权目录外的敏感目录**，且服务器存在基础路径检查，因此必须同时绕过以下 3 点，才能成功执行对`/root`的目录遍历：

#### 1. 必须绕过**服务器的路径范围限制**

这是**最核心的绕过点**：该 MCP 服务器的核心安全规则（官方文档明确说明）是**仅允许对启动时指定的授权目录（/var/www/h）执行所有文件操作**，`/root`属于授权目录外的绝对禁止访问范围，若不绕过此限制，任何对`/root`的直接调用都会被直接拦截。

#### 2. 必须绕过**服务器的路径检查机制**

靶机针对`list_directory`的入参`path`做了基础校验，会拦截**纯`../`穿越路径**（如`../../../../root`）、**直接绝对路径**（如`/root`），需利用该漏洞的 **“冲突前缀路径” 特性 ** 构造合法路径（允许目录前缀 +`../`穿越，如`/var/www/h/../../../../root`），让服务器的路径校验逻辑判定路径 “在授权范围内”，从而绕过检查。

#### 3. 必须绕过**虚假的权限 / 访问控制限制**

此前操作中遇到的 “没有权限” 并非真的缺少文件系统权限，而是**服务器层面的访问控制拦截**（因路径格式不合法，被判定为非法访问），需通过合规的路径构造（贴合漏洞特性），让服务器认为对`/root`的`list_directory`调用是 “合规操作”，从而放行，绕过该访问控制限制。

### 核心总结

1. 唯一必调工具：`list_directory`（仅能通过它获取 /root 下未知的 flag 文件名）；
2. 必绕核心限制：① 授权目录的路径范围限制 ② 服务器的路径校验机制 ③ 服务器层面的访问控制 / 虚假权限限制；
3. 绕过大法：利用 CVE-2025-53110 目录遍历漏洞，构造 **「允许目录前缀 +/var/www/h」+「../ 路径穿越」** 的冲突前缀路径，对 /root 执行`list_directory`。
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



## Safe Image Encryption


已知部分明文攻击的图像题。


1.  **加密逻辑**：
    程序读取一个 PNG 图像，获取其原始像素数据（RGBA，每个像素 4 字节）。然后读取一个长度为 **1003** 的密钥文件（Key），对每个像素的四个通道进行异或（XOR）变换，最后保存为 `encrypted.png`。
2.  **关键参数**：
    *   密钥长度：`1003` 字节。
    *   像素定位：每个像素索引为 `v10 = 4 * (x + y * width)`。
    *   Key 索引：基于 `v10 % 1003` 循环。
3.  **核心公式推导**：
    令 $k = (4(x + y \cdot width)) \pmod{1003}$，$key$ 为密钥数组。
    根据反汇编代码，加密过程如下：
    *   **红色通道 (R)**：$C_R = P_R \oplus (x^2 + key[k] + (key[k] \oplus 0xAA)) \pmod{256}$
    *   **绿色通道 (G)**：$C_G = P_G \oplus (key[(k+2)\%1003] \oplus (x \cdot y) \oplus (3 \cdot key[(k+1)\%1003])) \pmod{256}$
    *   **蓝色通道 (B)**：$C_B = P_B \oplus (y^2 + key[(k+1)\%1003] + (2 \cdot key[(k+2)\%1003] \oplus 0x66)) \pmod{256}$
    *   **透明通道 (A)**：$C_A = P_A \oplus ((key[(k+3)\%1003] \oplus 0x55) - 16) \pmod{256}$


**突破口：Alpha（透明）通道。**
在大多数 PNG 图像中，如果不包含透明背景，Alpha 通道的值通常全是 `255`（不透明）。
如果我们假设原图的 $P_A = 255$，那么：
$$C_A \oplus 255 = (key[(k+3)\%1003] \oplus 0x55) - 16$$
由此可反推 $key$ 的每一个字节：
$$key[(k+3)\%1003] = ((C_A \oplus 255) + 16) \oplus 0x55$$

由于图像很大（如 $1000 \times 600$），像素数量远多于 $1003$，通过遍历像素，我们可以轻松填满并验证这 $1003$ 个字节的 $key$。

使用 `Pillow` 库来处理图像。

```python
from PIL import Image

# 1. 加载加密图像
enc_img = Image.open('encrypt.png').convert('RGBA')
width, height = enc_img.size
pixels = enc_img.load()

key_len = 1003
key = [0] * key_len
found_key = [False] * key_len

# 2. 假设 Alpha 通道原值为 255，恢复 Key
for y in range(height):
    for x in range(width):
        v10 = 4 * (x + y * width)
        k = v10 % key_len
        idx_in_key = (k + 3) % key_len
        
        if not found_key[idx_in_key]:
            _, _, _, ca = pixels[x, y]
            # 根据公式: ca = 255 ^ ((key[idx] ^ 0x55) - 16)
            # 反推: key[idx] = ((ca ^ 255) + 16) ^ 0x55
            k_val = ((ca ^ 255) + 16) & 0xFF
            key[idx_in_key] = k_val ^ 0x55
            found_key[idx_in_key] = True

# 3. 使用恢复的 Key 解密整张图
dec_img = Image.new('RGBA', (width, height))
dec_pixels = dec_img.load()

for y in range(height):
    for x in range(width):
        v10 = 4 * (x + y * width)
        k = v10 % key_len
        cr, cg, cb, ca = pixels[x, y]
        
        # 提取相关 key 字节
        k0 = key[k]
        k1 = key[(k + 1) % key_len]
        k2 = key[(k + 2) % key_len]
        k3 = key[(k + 3) % key_len]
        
        # 计算加密时使用的变元 (注意 8位 截断)
        v15_low = (x*x + k0 + (k0 ^ 0xAA)) & 0xFF
        v16 = (k2 ^ (x*y) ^ (3 * k1)) & 0xFF
        v17 = (y*y + k1 + ((2 * k2) ^ 0x66)) & 0xFF
        v18 = ((k3 ^ 0x55) - 16) & 0xFF
        
        # XOR 还原
        pr = cr ^ v15_low
        pg = cg ^ v16
        pb = cb ^ v17
        pa = ca ^ v18 # 理论上应该是 255
        
        dec_pixels[x, y] = (pr, pg, pb, pa)

dec_img.save('flag.png')
print("解密完成，请查看 flag.png")
```

### 总结
这道题的难点在于从繁杂的汇编代码中提取出四个通道对应的数学公式。一旦发现 Key 是循环使用的，且 Key 长度远小于像素总数，利用已知明文（通常是 Alpha=255 或背景色）即可秒杀。如果 Alpha 通道不对，可以尝试假设原图左上角第一个像素是白色（255, 255, 255）来获取 Key。
SHCTF{@lPh4_b1T_L3Ak_th3_kEy_bUt_Ci4ll0!!}
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


## TE
已知p,q,n=pq,m为flag明文，
$$
 
\left\{\begin{matrix}
c_1 \equiv m^{e1} \mod n
 \\
c_2 \equiv m^{e2} \mod n
\end{matrix}\right.
$$
这是共模攻击



根据Bezourt定理 ，对于任何两个整数 $e_1, e_2$，一定存在整数 $a, b$ 满足：
$$a \cdot e_1 + b \cdot e_2 = \gcd(e_1, e_2)$$

本题目中，$e_1$ 和 $e_2$ 互质的，即 $\gcd(e_1, e_2) = 1$。
$$a \cdot e_1 + b \cdot e_2 = 1$$

我们要寻找 $m$。我们可以对密文进行如下幂运算：
$$c_1^a \cdot c_2^b \equiv (m^{e_1})^a \cdot (m^{e_2})^b \pmod n$$
$$c_1^a \cdot c_2^b \equiv m^{a \cdot e_1 + b \cdot e_2} \pmod n$$
$$c_1^a \cdot c_2^b \equiv m^1 \pmod n$$

因此，只要满足条件的 $a$ 和 $b$，就能计算出 $m$。

在求解 $a \cdot e_1 + b \cdot e_2 = 1$ 时，系数 $a$ 或 $b$ 中必然有一个是**负数**。假设 $a < 0$，我们需要在模 $n$ 下计算：
$$c_1^a \equiv (c_1^{-1})^{-a} \pmod n$$
其中 $c_1^{-1}$ 是 $c_1$ 在模 $n$ 下的逆元。
求a，b用扩展欧几里得算法。




```python
from Crypto.Util.number import long_to_bytes
from gmpy2 import gcd, invert


e1 = 740153575
e2 = 2865243571
n = 136622832042809215646904518487100682818433235485047740604612449039291802103378650845690420527029208661555957840623544220907967041438993189882681277161437473818861280518627112617436473837014181944318974950710633690704711613682306786783611123590732850783007770603201513394002330426718261667816328404673167404897
c1 = 56187319559060690757544481076112948328826527679002578544683022765347668056620384831778729489197135280950314627119815558644487151419126272267146826463912815062442590228193753706779325992179790583792001196548329204758137104234662611732735693150331594645734142941475121453410494160975503459516324097097434727685
c2 = 45042409947237296641429229414329516753664139389113206575966507524195434716702812078844474626406932213486611190698953613898299571473488550533642524208077653917354039305279692307471529748408234617430389423630015569730564585740596832844917494965974840512412454337766930330443409183293514761911902752336129193323


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

def common_modulus_attack(c1, c2, e1, e2, n):
    g, a, b = extended_gcd(e1, e2)
    if g != 1:
        raise ValueError("e1 and e2 are not coprime")

    if a < 0:
        a = -a
        c1 = invert(c1, n)
    if b < 0:
        b = -b
        c2 = invert(c2, n)

    m1 = pow(c1, a, n)
    m2 = pow(c2, b, n)
    m = (m1 * m2) % n
    return m

m = common_modulus_attack(c1, c2, e1, e2, n)
flag = long_to_bytes(m)
print(flag)
```


## Stream
密文：bcin!guy zeui wh! wwps ce yryz ysex:wpurt{wc@xdii_u2frmt_cwkg_ktani0}
encode_key:ABBAAABBABBAABABAABBABAAAAABBAAABAAABBAAAABAABAAAAAABAA

wpurt:SHCTF
4 8 18  -2 14=EISYO

ABBAA ABBAB BAABA BAABB ABAAA AABBA AABAA ABBAA AABAA BAAAA AABAA可能是培根密码。
MNSTIGEMEQE

notvigenere


## LCG
```python
def gen():
    while True:
        # 生成模数m：63位、>2^62、奇数的随机整数
        m = randbits(63) | (1 << 62) | 1
        if m > 2**62:  # 保证m超过2^62，固定m的位数范围
            break
    # 生成乘数a：62位、最低两位为1（a%4=3）的随机整数
    a = randbits(62) | 3
    # 生成增量c：62位、奇数的随机整数
    c = randbits(62) | 1
    # 生成初始种子s0：62位、最低位/第2位为1（s0=5 mod 8）的随机整数
    s0 = randbits(62) | 5
    return m, a, c, s0
```

```python
def LCG(m, a, c, s0, nblocks):
    x = s0  # 初始化当前值为初始种子s0
    out = []  # 存储生成的伪随机数序列
    for _ in range(nblocks):
        x = (a * x + c) % m  # LCG核心递推公式（线性计算+模运算）
        out.append(x)
    return out
```

```python
def encrypt(m, a, c, s0, plaintext: bytes) -> bytes:
    # 步骤1：8字节分组补零，保证明文总长度为8的整数倍
    padlen = (-len(plaintext)) % 8  # 计算需要填充的0字节数（如长度10→补6个0）
    pt = plaintext + b'\x00' * padlen  # 明文拼接填充的空字节（\x00是0的十六进制表示）
    
    # 步骤2：8字节分组，字节串转大端序整数（密码学常用大端序，高位在前）
    blocks = [int.from_bytes(pt[i:i+8], 'big') for i in range(0, len(pt), 8)]
    # 步骤3：生成与明文分组数相同的LCG密钥流
    ks = LCG(m, a, c, s0, len(blocks))
    # 步骤4：逐组异或加密（异或是对称加密核心，可逆：b ^ k ^ k = b）
    cblocks = [b ^ k for b, k in zip(blocks, ks)]
    # 步骤5：密文整数转回8字节大端序字节串，拼接为最终密文
    return b''.join(cb.to_bytes(8, 'big') for cb in cblocks)
```

```python
def main():
    m, a, c, s0 = gen()  # 生成LCG随机参数
    cipher  = encrypt(m, a, c, s0,  P_known + FLAG)  # 加密「已知明文+FLAG」拼接内容
    
    # 拆分密文：与明文拼接顺序一一对应，无填充干扰
    C_known = cipher[:len(P_known)]  # 前len(P_known)字节：P_known对应的密文
    C_flag  = cipher[len(P_known):len(P_known) + len(FLAG)]  # 后续字节：FLAG对应的密文

    # 输出结果：已知明文、已知密文十六进制、FLAG密文十六进制
    print("P_known =",P_known)
    print("C_known =", C_known.hex())
    print("C_flag  =", C_flag.hex())
```

encrypt主要逻辑$C_i = P_i \oplus x_i$，所以$C_i \oplus P_i = P_i \oplus x_i \oplus P_i = x_i$
LCG：$x_1 = s_0,x_n = (ax_{n-1}+c) \% m,out = [x_1,x_2,...,x_{nblocks}]$

所以考虑$y_n = x_{n+1} - x_n \equiv (ax_n + c)-a(x_{n-1}+c) \equiv ay_{n-1}(\mod m)$
所以由模m等比数列性质$y_{n+2}y_n - y_{n+1}^2\equiv 0(\mod m)$
所以
$$
m = \gcd (|y_3y_1-y_2^2|,|y_4y_2-y_3^2|,...)
$$
得到m后,$a = (x_3-x_2)(x_2-x_1)^{-1} \mod m,c = (x_2-ax_1) \mod m$
已知m,a,,c,x6,由$x_n = (ax_{n-1}+c) mod m$即可生成后续。
最终$P_{flag,j} =C_{flag,j} \oplus x_{6+j}$

```python
from gmpy2 import gcd, invert

# 1. 基础数据
P_known = b'Insecure_linear_congruential_random_number!!!!!!'
C_known_hex = "44e18dfa1acd14aa790fc3bac4ca54c137bcd47bdfc2209a53b83715ecad3e29249845720588cac007bfb94f8476d91a"
C_flag_hex = "1995374a5b64c6696578c1d5bdc6fa3d1e974b813436eab4348db801fb7a6703658eaa4fefa2c6fd6792beb969df8ca70ad87a4f4aea6ca0040d65a3c1e3a5bf2655cafc1e5603a171edc9aa077c0ca264677c351907f35756c14dd7ece428cb424a3804b544ccb53e99935f9bc2d8483dd7587379c99b3542c222008a"

C_known = bytes.fromhex(C_known_hex)
C_flag = bytes.fromhex(C_flag_hex)

# 2. 还原前 6 个 LCG 状态 (x1 到 x6)
x = []
for i in range(0, len(P_known), 8):
    p_block = int.from_bytes(P_known[i:i+8], 'big')
    c_block = int.from_bytes(C_known[i:i+8], 'big')
    x.append(p_block ^ c_block)

# 3. 计算模数 m
y = [x[i+1] - x[i] for i in range(len(x)-1)]
t = [abs(y[i+2]*y[i] - y[i+1]**2) for i in range(len(y)-2)]

g = t[0]
for val in t[1:]:
    g = gcd(g, val)

# 这里的 m 必须是奇数且在 2^62 到 2^63 之间
m = g
for p in [2, 3, 5, 7, 11, 13, 17, 19]: # 消除可能存在的小因子
    while m % p == 0 and m // p > 2**61:
        m //= p

# 4. 计算 a 和 c
# a = (x3 - x2) * inv(x2 - x1) % m
a = ((x[2] - x[1]) * invert(x[1] - x[0], m)) % m
c = (x[1] - a * x[0]) % m

# 5. 解密 Flag (处理字节对齐)
curr_x = x[-1] # 这是 x6
flag_plaintext = b""

# C_flag 可能不是 8 的倍数，需要按块处理
for i in range(0, len(C_flag), 8):
    curr_x = (a * curr_x + c) % m # 生成 x7, x8...
    
    # 关键点：将当前的密钥流转换回 8 字节
    keystream_bytes = int(curr_x).to_bytes(8, 'big')
    
    # 获取当前密文块（可能是 1-8 字节）
    cipher_chunk = C_flag[i:i+8]
    
    # 逐字节异或
    for j in range(len(cipher_chunk)):
        flag_plaintext += bytes([cipher_chunk[j] ^ keystream_bytes[j]])

print("Decrypted Flag:")
print(flag_plaintext)


Decrypted Flag:
b'SHCTF{LLLLLLLLLLLLLLLCCCCCGGGGGGGGG_TGY%JgWOmAM6V5n55w3m*jcPJZjHO8E1VvzrGjT84tXS332D&o4GZe8%KKzEyAngmwwx9bp5dv_O4dPpOvMy1^hM}'
```

# OSINT
## 1
![[Pasted image 20260202155147.png]]