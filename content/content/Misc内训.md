# 0 编码

## 0.0
一切信息在计算机内是01串存储的。
计算机通过特定规则将01串转化为了我们能看懂的内容。

常见的字符编码：
## 0.1 ASCII：
7个二进制位表示字符，一共 128 种字符，
00-1F：控制字符；7F：控制字符（DEL）20-7E：可见字符；
ASCII编码采用单字节(8 Bit)存储，实际数据存储空间是7 Bit，最高位的1 Bit是奇偶校验位。![[Pasted image 20251210200730.png]]

## 0.2 Latin-1（ISO-8859-1）：
ASCII只够美国人用，于是
欧洲人扩展了 ASCII，一共 256 个项
0x00-0x7F之间完全和ASCII一致
80-9F：控制字符；A0-FF：可见字符
特点：任何字节流都可以用其解码（因为Latin-1是一个单字节编码，每个字节都对应一个确切的字符。它没有“非法”的字节组合。所以，无论你给它一段怎样的二进制数据，它都能“强行”翻译出一个字符序列，即使结果可能毫无意义。这在处理未知二进制数据时有时会用到）



## 0.3 Unicode是什么？
世界上存在着多种编码方式，同一个二进制数字可以被解释成不同的符号。因此，要想打开一个文本文件，就必须知道它的编码方式，否则用错误的编码方式解读，就会出现乱码。

如果有一种编码，将世界上所有的符号都纳入其中。每一个符号都给予一个独一无二的编码，那么乱码问题就会消失。这就是Unicode。

Unicode当然是一个很大的集合，现在的规模可以容纳100多万个符号。每个符号的编码都不一样需要注意的是，Unicode只是一个符号集，它只规定了符号的二进制代码，却没有规定这个二进制代码应该如何存储。

利用 Unicode 字符集的一系列编码
 UTF (Unicode Transformation Format) 
UTF-8 
UTF-8就是在互联网上使用最广的一种Unicode的实现方式。
UTF-8最大的一个特点，就是它是一种变长的编码方式。它可以使用1~4个字节表示一个符号，根据不同的符号而变化字节长度。如ASCII编码的内容UTf-8中就是用一个字符存储的。
![[Pasted image 20251220130320.png]]
比如王：0x0000738B=0000 0000 0000 0000 ==0111== ==0011 10== ==00 1011==，
它对应的二进制信息插入第三区间1110xxxx 10xxxxxx 10xxxxxx，即
1110==0111== 10==001110== 10==001011==
即E78e8b。
```python
>>> print('王'.encode('utf-8'))
b'\xe7\x8e\x8b'
```
https://blog.csdn.net/whahu1989/article/details/118314154
UTF-16 / UTF-32 / UCS


中国国标字符集系列编码
GB 2312 / GBK / GB 18030-2022
### 0.4 三种核心GB系列编码方式

#### 1. GB 2312-80 (国家标准)

- **全称**：《信息交换用汉字编码字符集-基本集》，是中国最早的汉字编码国家标准。
- **编码方式**：**双字节定长编码**。
- **核心思想**：区位码是GB2312字符集编号空间的一个94*94的二维表，行表示区（高位字节），列表示位（低位字节），每区有94个位，每个区位对应一个字符。
  - **区位码**：例如，“啊”字位于16区的01位，其“区位码”就是 `1601`。
  - **国标码/交换码**：为了在计算机中传输和处理，需要将区位码转换为实际的字节。转换规则是：**将区号和位号分别加上十六进制的 `0xA0`** (即十进制的160)。
    - `第一个字节 = 区号 + 0xA0`
    - `第二个字节 = 位号 + 0xA0`
    - 所以，“啊”字的国标码就是 `(0x10 + 0xA0)` `(0x01 + 0xA0)` = `0xB0A1`。
  - **特点**：
    - 所有字节的值都在 `0xA1` 到 `0xF7` 之间，高位都为1，巧妙地避开了与标准ASCII码（0x00-0x7F）的冲突，使得中英文可以混合处理。
    - 收录了约6700个汉字和约700个符号，在当时基本满足日常使用。但对于古汉语、部分人名、方言字等则无能为力。
具体怎么存储呢？比如"侃"区位码为5709，分成0x57和0x09，两部分都加上0xA0，合起来得到0xD9A9.
```python
print('侃'.encode('gb2312'))
b'\xd9\xa9'
```
为什么要加0xA0，是因为区分ASCII码小于127，加上后才大于127.碰到连续两个大于127的就是GB2312码。
#### 2. GBK (国家标准扩展)
- **全称**：《汉字内码扩展规范》(K代表“扩展”)，它不是一个正式的国家标准，而是微软制定的一个技术规范，但因其广泛应用而成为事实标准。
- **编码方式**：**双字节定长编码**。
- **核心思想**：在完全保留GB 2312所有内容的基础上，利用其未使用的编码空间来容纳更多的字符。
  - **扩展方式**：GB 2312的两个字节都在 `0xA1` - `0xF7` 范围内。GBK打破了这个限制，极大地扩展了可用编码空间：（不再需要遵守上面的规定了）
    - **第一个字节**：范围从 `0x81` 扩展到 `0xFE`。
    - **第二个字节**：范围从 `0x40` 扩展到 `0xFE`（不包括 `0x7F`）。
  - **特点**：
    - 收录了超过21000个汉字，包含了繁体字和日、韩汉字，基本解决了GB 2312字数不足的问题。
    - 它的设计完全以兼容GB 2312为前提。

#### 3. GB 18030-2022 (现行国家强制标准)

- **全称**：《信息技术中文编码字符集》，是中国现行最新的、强制性的国家标准。
- **编码方式**：**变长编码（1、2或4字节）**。这是它与前两者最根本的区别。
- **核心思想**：目标是收录Unicode标准中的所有字符，实现与国际标准的完全对接，同时保持对GBK和GB 2312的兼容。
  - **编码结构**：
    - **单字节**：与ASCII完全一致 (`0x00` - `0x7F`)。
    - **双字节**：**完全重用GBK的编码方案**。所有在GBK中有效的双字节编码，在GB 18030中都代表同一个字符。
    - **四字节**：为映射Unicode中新增的大量字符而设计。其结构为 `[0x81-0xFE]` `[0x30-0x39]` `[0x81-0xFE]` `[0x30-0x39]`。解码器可以通过第二个字节是否在 `0x30`-`0x39` 范围内，来判断这是一个双字节字符还是四字节字符的开始。
  - **特点**：
    - 编码空间巨大，理论上可表示超过160万个字符。
    - 是GBK的超集，也是Unicode的实现方式之一（类似于UTF-8，但编码方式不同）。
![img](https://i-blog.csdnimg.cn/direct/223e9fbcd09d46e8ab1187ffb04f6348.webp)

## 0.40乱码情况
以下内容倾力感谢会长qsgg的资料支持(^v^）
https://brucejqs.github.io/MyNotebook/blog/CTF/2023-2024%E6%9A%91%E7%9F%AD%E5%AD%A6%E6%9C%9F/Lab1-Misc%20Report/


 Latin-1 编码可以解码任意字节流，但 UTF-8 不能，它的编码情况只有以下四种：

- **0**xxxxxxx
- **110**xxxxx **10**xxxxxx
- **1110**xxxx **10**xxxxxx **10**xxxxxx
- **11110**xxx **10**xxxxxx **10**xxxxxx **10**xxxxxx

所以如果一个字符开头就出现了 **10** xxxxxx 这样的字节，UTF-8 就不知道该怎么解码了。其他情况也会引起 UTF-8 解码错误。

Python 处理这种错误的默认方法是直接抛出 UnicodeDecodeError，大部分情况下是不方便的，所以一般情况的处理方式是针对错误的字节流进行替换，比如将错误的字节流替换为 U+FFFD（即 �），这也是一些古怪乱码的来源之一。


·### 用 GBK 解码 UTF-8 编码的文本
```python
>>> "CSA你好".encode("utf8").decode("utf8")
'CSA你好'
>>> "CSA你好".encode("utf8").decode("GBK")
'CSA浣犲ソ'
>>> "CSA你好".encode("utf8")
b'CSA\xe4\xbd\xa0\xe5\xa5\xbd'
```


因此对于大小写字母这些包含在 ASCII 码中的两者转换并没有区别。

在 utf-8 编码中，汉字是用 3 个字节来表示的，特殊的汉字还会用 4 个字节来表示，于是“你好”二字在 utf-8 编码下就形成了 6 个字节。

但是在 GBK 编码中，一个汉字是用 2 个字节来表示的，于是对于 utf-8 形成的 6 个字节的编码在 GBK 中就会被解码为 3 个汉字，形成乱码问题。


### 乱码情况 2：用 UTF-8 解码 GBK 编码的文本

```python
>>> "CSA你好".encode("GBK")
b'CSA\xc4\xe3\xba\xc3'
>>> "CSA你好".encode("GBK").decode("utf8")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc4 in position 3: invalid continuation byte
>>> "CSA你好".encode("GBK").decode("GBK")
'CSA你好'
```
GBK 编码将"战队"编码为 `11010101 10111101 10110110 11010011`，而对于 utf-8 编码来说，第一个字节前三位为 `110`，这意味着这个字符应当是两个字节来保存的，因此 utf-8 将前两个字节编为一个字符，但是第三个字节前两位却显示的是 10，utf-8 就不知道该怎么解码了，因此在 python 中会显示 UnicodeDecodeError；CyberChef 则将错误的字节解码为了其他奇怪的字符；而 vscode 则将其解码为奇怪的符号。
### 乱码情况 3：用 latin-1 解码 UTF-8 编码的文本
```python
>>> "CSA你好".encode("utf8").decode("latin-1")
'CSAä½\xa0å¥½'
>>> "CSA你好".encode("utf8")
b'CSA\xe4\xbd\xa0\xe5\xa5\xbd'
```
Latin-1，即 ISO-8859-1，是单字节编码，本身无法表示中文。由上面所说的，utf-8 将每个汉字编码为三个字节，因此用 Latin-1 解码 utf-8 编码的文本会出现 6 个奇怪的字符。
### 乱码情况 4：用 latin-1 解码 GBK 编码的文本

```python
>>> "CSA你好".encode("gbk")
b'CSA\xc4\xe3\xba\xc3'
>>> "CSA你好".encode("gbk").decode("latin-1")
'CSAÄãºÃ'
```
同理，GBK 将每个汉字编码为两个字节，因此用 Latin-1 解码 utf-8 编码的文本会出现 4 个奇怪的字符。

### 乱码情况 5：先用 GBK 解码 UTF-8 编码的文本，再用 UTF-8 解码前面的结果
这里我们只使用 vscode 实现（python 在该文本下 GBK 解码就报错，无法解码）
用 GBK 解码时会被错误地解释为其他字符或者无法识别的字节序列（这是为什么 python 会报错），那么解码后的十六进制就已经编成了下面的那些，最后 utf-8 转换时也就出现了乱码。
```
CSA你好
#gbk解码
CSA浣犲ソ
#utf-8还原
CSA你好

CSA你好吗在这里很开心快乐和所有的烦恼说拜拜

CSA浣犲ソ鍚楀湪杩欓噷寰堝紑蹇冨揩涔愬拰鎵€鏈夌殑鐑︽伡璇存嫓鎷�

CSA你好吗在这里很开心快乐和所有的烦恼说拜�?

```

### 先用 UTF-8 解码 GBK 编码的文本，再用 GBK 解码前面的结果


```
#原文本
CSA你好吗在这里很开心快乐和所有的烦恼说拜拜
#utf-8解码
CSA�����������ܿ��Ŀ��ֺ����еķ���˵�ݰ�
#gbk解码
CSA锟斤拷锟斤拷锟斤拷锟斤拷锟斤拷锟杰匡拷锟侥匡拷锟街猴拷锟斤拷锟叫的凤拷锟斤拷说锟捷帮拷

```
因为 utf-8 特定的编码格式，导致解码时有些字符无法被解读，而 vscode 将错误的字节流替换，才得到了现在的乱码。

#### 可恢复？

从之前的研究来看，不可恢复的情况在于解码时若遇到不存在于解码格式当中的十六进制字节流时，vscode 会进行篡改使得其符合解码格式，这样就造成了不可恢复。而且我们默认解码之后同时用这种编码方式重新编码，并保存字节流到文件。那理论上来说，以上六种乱码形式都有不可恢复的可能，因为重新编码会导致篡改的发生。

#### “锟斤拷”？

“锟斤拷”乱码的来源就在于 utf-8 特殊的编码格式，当解码时有些字符不符合编码格式时，无法匹配到正确的 utf-8 码，vscode 会将其填充为 `EF BF BD`。我们假设有三个连续的字符不符合编码格式，那么最后填充完得到的字节流是 `EF BF BD EF BF BD EF BF BD EF BF BD`，在GBK编码表中，查找对应编码，并解码为汉字，由于 `EF BF` 对应锟，`BD EF` 对应斤，`BF BD`对应拷，从而得到“锟斤拷锟斤拷”。


## 0.5 Morse电码
无线电测向同学狂喜
- - 点 ·：1 单位；划 -：3 单位
    - 点划之间间隔：1 单位；字符之间间隔：3 单位；单词之间间隔：7 单位
- 字符集：A-Z、0-9、标点符号（.:,;?='/!-_"()$&@+）
![[Pasted image 20251209104850.png]]

### 中文电码
一个汉字对应四个数字，数字用短码发送
https://dianma.bmcx.com/
![[Pasted image 20251209105147.png]]


其它一些东西
A1Z26
康托（将排列与整数进行双向映射），
三进制
NATO
培根 https://zh.wikipedia.org/wiki/%E5%9F%B9%E6%A0%B9%E5%AF%86%E7%A2%BC
棋盘	
九键\T9( https://www.dcode.fr/t9-cipher)	
盲文（三行两列 https://www.lddgo.net/common/braille）
旗语
猪圈

https://docs.qq.com/sheet/DVGNMZHRWTnNRYXdo?tab=BB08J2
https://ctf-wiki.org/crypto/classical/others/


## 0.6 base家族

### base64
首先有原始数据（文本，图片，视频等）
转化为二进制码（可能是ASCII，UTF-8的方式等等）
然后6位二进制一组然后对照字符表(`A-Z`, `a-z`, `0-9`, `+`, `/`)输出编码结果

![[Pasted image 20251211121520.png]]

![[Pasted image 20251211122211.png]]


![[Pasted image 20251211122248.png]]

```
(base) kaisenye@kaisendeMacBook-Air ~ % echo "HelloCSA" | base64
SGVsbG9DU0EK
(base) kaisenye@kaisendeMacBook-Air ~ % echo "你好" | base64
5L2g5aW9Cg==

(base) kaisenye@kaisendeMacBook-Air ~ % echo -n "HelloCSA" | base64
SGVsbG9DU0E=
(base) kaisenye@kaisendeMacBook-Air ~ % echo -n "你好" | base64
5L2g5aW9
```


### base32，58等其他
**base32的编码表是由（A-Z、2-7）32个可见字符构成，“=”符号用作后缀填充。**
**base58的编码表相比base64少了数字0，大写字母I，O，小写字母 l (这个是L），以及符号‘+’和‘/’**
base91的密文由91个字符（0-9，a-z，A-Z,!#$%&()*+,./:;<=>?@[]^_`{|}~”）组成

Base100编码/解码工具（又名：Emoji表情符号编码/解码），可将文本内容编码为Emoji表情符号；同时也可以将编码后的Emoji表情符号内容解码为文本。

### 万物皆可编码
#### JSFuck编码：
JSFuck是一种人类难以阅读的基于JavaScript的编程语言，代码中仅使用“[”“]”“（”“）”“!”和“+”六种字符。理论上，JSFuck的运行不需要依赖浏览器，它也可以在Node.JS上运行。
#### brainfuck，ook编码
发明Brainfuck是为了创建一种简单的、可以用最小的编译器来实现的、符合图灵完备思想的编程语言。这也导致Brainfuck代码对非专业人员基本不可读。该语言只有八种符号，所有操作都由这八种符号的组合来完成
https://www.bilibili.com/video/BV1kQtVzAEaS/?spm_id_from=333.337.search-card.all.click&vd_source=f87bf786d8d1f18597fcc69be52fffbe


Ook！是一种由David Morgan-Mar创建的编程语言，它与Brainfuck完全相同，只是指令被改成了其他表示形式。
```
hello word ！
+++++ +++++ [->++ +++++ +++<] >++++ .---. +++++ ++..+ ++.<+ +++++ ++[->
----- ---<] >---- ----- ----- -.<++ +++++ ++[-> +++++ ++++< ]>+++ +++.-
----- --.++ +.<++ +[->- --<]> ----- .<+++ +++++ [->-- ----- -<]>- ---.<
+++++ +++++ ++++[ ->+++ +++++ +++++ +<]>+ +++++ +++++ .<+++ ++++[ ->---
----< ]>--. <++++ +++[- >---- ---<] >---- ----- -.<

```
https://www.splitbrain.org/services/ook

### 2025ZJUCTF 喜多乐谱


## 0.7 哈希函数

MD5，SHA1:是**哈希**或者叫散列函数，不可逆。
哈希函数：
![[Pasted image 20251211164857.png]]
### **MD5特征：** 
函数初始化含有
```
0x67452301，0xEFCDAB89，0x98BADCFE，0x10325476
```
有固定长度，一般是32位,由[0-9a-f]组成。16位的md5是从 32 位 md5 值来的。是将 32 位 md5 去掉前八位，去掉后八位得到的。
md5爆破网站
https://www.cmd5.com/
[http://www.ttmd5.com/](http://www.ttmd5.com/)
[http://pmd5.com/](http://pmd5.com/)
[https://www.win.tue.nl/hashclash/fastcoll_v1.0.0.5.exe.zip](https://www.win.tue.nl/hashclash/fastcoll_v1.0.0.5.exe.zip)
### **SHA1特征：** 有固定长度，40位[0-9a-f]
```
sha1sum shattered-1.pdf
38762cf7f55934b34d179ae6a4c80cadccbb7f0a  shattered-1.pdf
```
函数的初始化含有
```
0x67452301
0xEFCDAB89
0x98BADCFE
0x10325476
0xC3D2E1F0
```
SHA1不安全了。为什么呢，我们来看下面这个例子
### 2017 SECCON SHA1 is dead

题目描述如下
1. file1 != file2
2. SHA1(file1) == SHA1(file2)
3. SHA256(file1) <> SHA256(file2)
4. 2017KiB <sizeof(file1) < 2018KiB
5. 2017KiB <sizeof(file2) < 2018KiB

我们要理解SHA1算法的5个寄存器分别处理64字节数据，当前状态 = [h0, h1, h2, h3, h4]，而算法是按文件字节流顺序更新hash的，新状态=f(当前状态，新数据块内容)，如此递推，5* 64=320，所以只需要取两个shattered.pdf文件的前320字节初始状态前缀，后面只需要padding即可，就可以满足题目要求。

生成[https://alf.nu/SHA1](https://alf.nu/SHA1)

SHA256 **64位** 的 [0-9a-f]   SHA512 **128位** 的 [0-9a-f] 字符串


HMAC (Hash-based Message Authentication Code) 常用于接口签名验证，这种算法就是在前两种加密的基础上引入了秘钥，而秘钥又只有传输双方才知道，所以基本上是破解不了的。

NTLM hash这种加密是Windows的哈希密码，是 Windows NT 早期版本的标准安全协议。与。
https://blog.csdn.net/qq_62169455/article/details/132617592






# 1.从压缩包开始

### zip
zip的内容由数据区（Local file header，File data，Data descriptor），核心目录区（Central directory） 以及核心目录结束区域组成
![[Pasted image 20251220185959.png]]

前面三个是数据区，中间的是核心目录区域，最后的是核心目录结束区


数据去和核心目录区：每个文件一条记录，有固定签名开头，数据区签名50 4B 03 04，核心目录区签名50 4B 01 02.核心目录结束区在每个压缩文件中有且仅有一个，签名味50 4B 05 06。

![[Pasted image 20251211223601.png]]
![[Pasted image 20251211224439.png]]


数据区一条文件记录包括以下内容：
解压所需最低版本，通用标记位flags，压缩算法，文件最后修改日期时间，CRC32，压缩后和压缩前大小，文件名长度与内容，文件数据。
**文件尾之后附加文件**

- **原理**：“因为解压软件读到50 4B 05 06就停止了，所以可以在**这个标记的后面，再拼接上另一个完整的文件**，比如一张图片、另一个ZIP包等等。这在正常解压时是完全看不到的。
- **工具**：
    - **binwalk**：直接运行 binwalk yourfile.zip，它会自动扫描并告诉你后面藏了什么。
    - **WinHex / 010 Editor**：直接拖到文件末尾，肉眼寻找50 4B 05 06，看看它后面是不是还有别的文件头（比如FF D8 for JPG, 89 50 4E 47 for PNG）。




### rar
| 名称         | 大小  | 描述           |
| ---------- | --- | ------------ |
| HEAD_CRC   | 2   | 全部块或块部分的 CRC |
| HEAD_TYPE  | 1   | 块类型          |
| HEAD_FLAGS | 2   | 阻止标志         |
| HEAD_SIZE  | 2   | 块大小          |
| ADD_SIZE   | 4   | 可选字段 - 添加块大小 |
Rar4及以下 压缩包的文件头为 `0x 52 61 72 21 1A 07 00`。rar5为`0x 52 61 72 21 1A 07 01 00`
以块为单位，包含签名块、压缩文件头块、文件块与结尾块。

![[Pasted image 20251211224136.png]]

我们看正常的一个rar，第一数据块crc后面的进行crc32校验，发现顺序不一样，这是因为文件是小端序存储。
![[Pasted image 20251211233152.png]]


## 1.1暴力破解
```
zip --password hello secret.zip flag.txt
```
### 1.1.1直接爆破
工具：ARCHPR
在Mac m4芯片下
随机可打印大概是长度5需要跑7分钟
随机纯字母大概长度6就跑不动了
跑纯数字到$10^{10}$跑了1分钟
例如：
我们知道有个card.zip是银行卡密码，也就是六位纯数字。
![[Pasted image 20251220164929.png]]

### 1.1.2字典破解
根据已有的字典进行匹配，可能会有提示密码是有意义的单词，或者全部是数字（比如卡号爆破这种）

工具fcrack:(Linux)
```
# Syntax
fcrackzip -u -D -p [wordlist] [ZIP file]

# Example
fcrackzip -u -D -p ~/rockyou.txt ~/file.zip
```

有时候下载来的字典，是windows格式的，也就是在windows中是
```
wingspreads\r\n
wingstem\r\n
wingtip\r\n
```
而unix格式是
```
wingspreads\n
wingstem\n
wingtip\n
```
所以字典匹配会多出\r,是无法正常匹配的。
```
# 使用 cat -A 来显示所有非打印字符
cat -A words_alpha.txt | grep "winter"
```
注意要
```
dos2unix words_alpha.txt
```
转换格式。
就可以正常使用archpr或者fcrackzip进行字典破解了
![[Pasted image 20251220165112.png]]
### 1.1.3掩码破解
密码有固定格式，例如：flag{????}、手机号158...
、生日2004????。
你知道密码的长度和部分字符类型（数字、小写字母等）。

![[Pasted image 20251209113842.png]]

## 1.2明文攻击
同一个zip压缩包里的所有文件都是使用同一个加密密钥来加密的，所以可以用已知文件来找加密密钥，利用密钥来解锁其他加密文件
要求：有一个已知文件的zip的CRC-32和要解密的压缩包内一个文件完全一样。
```
(base) kaisenye@kaisendeMacBook-Air mingwen % unzip -v 1.zip
Archive:  1.zip
 Length   Method    Size  Cmpr    Date    Time   CRC-32   Name
--------  ------  ------- ---- ---------- ----- --------  ----
      17  Defl:N       17   0% 12-02-2019 20:22 b0c530d8  flag.txt
--------          -------  ---                            -------
      17               17   0%                            1 file
(base) kaisenye@kaisendeMacBook-Air mingwen % unzip -v res.zip
Archive:  res.zip
 Length   Method    Size  Cmpr    Date    Time   CRC-32   Name
--------  ------  ------- ---- ---------- ----- --------  ----
      17  Defl:N       17   0% 12-02-2019 20:22 b0c530d8  flag.txt
      19  Defl:N       21 -11% 01-14-2020 13:14 483344c3  secret.txt
--------          -------  ---                            -------
      36               38  -6%                            2 files
```

![[Pasted image 20251220174359.png]]

flag相差12说明是对的
5-10min

![[Pasted image 20251220184501.png]]

![[Pasted image 20251220184720.png]]
## 1.3zip伪加密
分区
1.压缩源文件数据区
2.压缩源文件目录区
3.压缩源文件目录结束标志

| 状态  | 本地文件头标志         | 中央目录标志          | 说明                     |
| :-- | :-------------- | :-------------- | :--------------------- |
| 无加密 | 偶数（00 00，08 00） | 偶数（00 00，08 00） | 正常文件，无需密码。             |
| 伪加密 | 偶数（0000）        | 奇数（09 00）       | 标志位不一致，只需修复中央目录的标志位即可。 |
| 真加密 | 奇数（01 00，09 00） | 奇数（01 00，09 00） | 标志位一致且为奇数，需要进行密码破解。    |


1. **打开文件**：用 WinHex, 010 Editor 等工具打开ZIP文件。
2. **检查本地文件头**：查看其后的第7、8个字节。记录下来(00 00）。
3. **检查中央目录**：查看其后的第9、10个字节。记录下来（09 00）。
4. **对比判断**：
    **两者不一致**（一个加密标志，一个非加密标志），所以是伪加密。
DSACTF 什么密码.zip
![[什么密码.zip]]
![[Pasted image 20251210103305.png]]

我们发现两者并不一致，说明是伪加密，把下面的00 09修改成00 00，就可以解压出图片了！
![[Pasted image 20251210103504.png]]

#### rar的伪加密：
rar4存在伪加密
RAR的伪加密与ZIP的伪加密原理相同，造成伪加密的关键都是在一个指定的位标记字段上。
在RAR的第`24`个字节，也就是`010 Editor`显示的文件结构中的`ubyte PASSWORD_ENCRYPTED`字段，修改其字段为`1`即可实现RAR伪加密。

  rar5的伪加密需要修改Headflag。

![[Pasted image 20251209120857.png]]

## 1.3 CRC32碰撞
往往是一堆压缩包，每个压缩包里面的txt文件只有寥寥个长度。
然后通过每个压缩包拼接起来，得到结果。（再进行base64解密什么的）

```
root@a36171f51789:/ctf/ctf_work/work/yasuobao/crc# echo -n "CSA" > 
flag.txt
root@a36171f51789:/ctf/ctf_work/work/yasuobao/crc# zip --password "Th1s-P@ssw0rd-is-Unbr3akable-by-Brut3f0rce" crc_demo.zip flag.txt
updating: flag.txt (stored 0%)
root@a36171f51789:/ctf/ctf_work/work/yasuobao/crc# unzip -v crc_demo.zip
Archive:  crc_demo.zip
 Length   Method    Size  Cmpr    Date    Time   CRC-32   Name
--------  ------  ------- ---- ---------- ----- --------  ----
       3  Stored        3   0% 2025-12-10 11:02 1dd0951a  flag.txt
--------          -------  ---                            -------
       3                3   0%                            1 file
```

```python
# crc_cracker.py
import zlib
import string
from itertools import product

target_crc = 0x1dd0951a
file_length = 3        

charset = string.printable

for item in product(charset, repeat=file_length):
    content = "".join(item)
    content_bytes = content.encode('utf-8')
    
    # 计算当前生成内容的CRC32值
    current_crc = zlib.crc32(content_bytes)
    
    # 检查是否与目标CRC32值匹配
    if current_crc == target_crc:
        print(f"Found matching content: {content}")

```

```
(base) kaisenye@kaisendeMacBook-Air crc % python3 jiemi.py
Found matching content: CSA
```
https://blog.csdn.net/weixin_43659360/article/details/86748483


# 2. 常规取证
任何要求检查一个静态数据文件从而获取隐藏信息的都可以被认为是隐写取证题
工具介绍。
## John the ripper
最著名的、广受欢迎的多功能hash破解工具之一，它有非常快速的破解速度，也兼容极大范围的哈希类型。
```
sudo apt install john
```

#### 破解一个已知的简单哈希 (MD5, SHA1等)
```
sha1sum filename
md5sum filename

echo -n "hello" | md5sum
5d41402abc4b2a76b9719d911017c592  -

echo -n "hello" | sha1sum
aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d  -

```

```sh
# --format= 告诉john哈希类型，raw- 前缀用于标准哈希
#常见的hash其实也可以不告诉format
# --wordlist= 指定字典路径
root@fff4586fafba:/ctf/john# /ctf/john/run/john -format=raw-md5 --wordlist=/ctf/dic/rockyou.txt /ctf/work/quzhengg/test_hash.txt
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 128/128 SSE4.1 4x3])
Warning: no OpenMP support for this hash type, consider --fork=10
Note: Passwords longer than 18 [worst case UTF-8] to 55 [ASCII] rejected
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
hello            (?)     
1g 0:00:00:00 DONE (2025-12-20 11:00) 33.33g/s 6400p/s 6400c/s 6400C/s 123456..november
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed

#John破解成功后会把结果存起来，再次运行会提示“No password hashes left to crack”。必须用--show参数查看
john --show hash.txt


```
## Hashcat
hashcat也可以代替。

```
apt instll hashcat
```


```
#john
#清掉缓存演示
rm -f /ctf/john/run/john.pot

/ctf/john/run/john --wordlist=/ctf/dic/rockyou.txt --format=NT /ctf/work/hi.txt
/ctf/john/run/john --format=NT --show /ctf/work/hi.txt

#hashcat用法
root@fff4586fafba:/ctf/work# hashcat -m 1000 -a 0 hi.txt /ctf/dic/rockyou.txt
hashcat -m 1000 -a 0 hi.txt /ctf/dic/rockyou.txt --show
```
## 内存取证
常见的磁盘分区格式有以下几种

Windows: FAT12 -> FAT16 -> FAT32 -> NTFS
Linux: EXT2 -> EXT3 -> EXT4
FAT 主磁盘结构



删除文件：目录表中文件名第一字节e5。
## Volatility
```
python3 vol.py -f <内存镜像文件名> <插件名称> [插件的特定参数]
```

### 1.基本信息
分析内存镜像，自动识别出Windows的版本、内核版本、编译号、系统时间等关键信息。
```sh
python3 vol.py -f 111.vmem windows.info.Info

Variable        Value

Kernel Base     0xf80003e54000
DTB     0x187000
Symbols file:///Volumes/cipan1/volatility/volatility3/volatility3/symbols/windows/ntkrnlmp.pdb/F8E2A8B5C9B74BF4A6E4A48F18009994-2.json.xz
Is64Bit True
IsPAE   False
layer_name      0 WindowsIntel32e
memory_layer    1 FileLayer
KdDebuggerDataBlock     0xf8000403d070
NTBuildLab      7600.16385.amd64fre.win7_rtm.090
CSDVersion      0
KdVersionBlock  0xf8000403d030
Major/Minor     15.7600
MachineType     34404
KeNumberProcessors      1
SystemTime      2024-10-26 07:50:37+00:00
NtSystemRoot    C:\Windows
NtProductType   NtProductWinNt
NtMajorVersion  6
NtMinorVersion  1
PE MajorOperatingSystemVersion  6
PE MinorOperatingSystemVersion  1
PE Machine      34404
PE TimeDateStamp        Mon Jul 13 23:40:48 2009
```

### 2.进程查询
#### 2.1列出运行中的内存
```sh
(base) kaisenye@kaisendeMacBook-Air volatility % python3 ./volatility3/vol.py -f 111.vmem windows.pslist.PsList
Volatility 3 Framework 2.27.1
WARNING  volatility3.framework.layers.vmware: No metadata file found alongside VMEM file. A VMSS or VMSN file may be required to correctly process a VMEM file. These should be placed in the same directory with the same file name, e.g. 111.vmem and 111.vmss.
Progress:    0.00               Scanning layer_name using PdbSignatureScanProgress:    0.00               Scanning layer_name using PdbSignatureScanProgress:   40.33               Scanning layer_name using PdbSignatureScanProgress:  100.00               PDB scanning finished                        
PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionIdWow64    CreateTime      ExitTime        File output

4       0       System  0xfa80018d0040  68      468     N/A     False   2024-10-26 07:48:01.000000 UTC    N/A     Disabled
228     4       smss.exe        0xfa8002ccdb30  2       29      N/A     False     2024-10-26 07:48:01.000000 UTC  N/A     Disabled
292     284     csrss.exe       0xfa80033ca950  8       337     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
340     284     wininit.exe     0xfa80033d2060  3       76      0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
352     332     csrss.exe       0xfa8003341630  7       203     1       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
392     332     winlogon.exe    0xfa80033de2d0  4       115     1       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
436     340     services.exe    0xfa800340a740  9       196     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
444     340     lsass.exe       0xfa80034146f0  7       572     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
452     340     lsm.exe 0xfa800340c560  10      135     0       False   2024-10-26 07:48:02.000000 UTC    N/A     Disabled
556     436     svchost.exe     0xfa8003419b30  10      342     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
620     436     svchost.exe     0xfa8003556140  6       239     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
672     436     svchost.exe     0xfa8003582350  21      459     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
792     436     svchost.exe     0xfa80035b1b30  16      300     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
852     436     svchost.exe     0xfa8003628780  40      1025    0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
912     672     audiodg.exe     0xfa800363f3b0  4       116     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
964     436     svchost.exe     0xfa800365f060  12      261     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
356     436     svchost.exe     0xfa8003665b30  20      481     0       False     2024-10-26 07:48:03.000000 UTC  N/A     Disabled
256     436     spoolsv.exe     0xfa80037205f0  13      263     0       False     2024-10-26 07:48:03.000000 UTC  N/A     Disabled
1040    436     svchost.exe     0xfa8003738420  20      325     0       False     2024-10-26 07:48:03.000000 UTC  N/A     Disabled
1420    436     svchost.exe     0xfa800378ab30  5       96      0       False     2024-10-26 07:48:03.000000 UTC  N/A     Disabled
1556    436     svchost.exe     0xfa800389eb30  7       92      0       False     2024-10-26 07:48:03.000000 UTC  N/A     Disabled
1760    436     taskhost.exe    0xfa8003935060  10      167     1       False     2024-10-26 07:48:15.000000 UTC  N/A     Disabled
1812    792     dwm.exe 0xfa800394e9f0  4       71      1       False   2024-10-26 07:48:15.000000 UTC    N/A     Disabled
1828    1792    explorer.exe    0xfa8003958b30  19      629     1       False     2024-10-26 07:48:15.000000 UTC  N/A     Disabled
1684    436     SearchIndexer.  0xfa8003717060  13      599     0       False     2024-10-26 07:48:21.000000 UTC  N/A     Disabled
1984    1684    SearchFilterHo  0xfa800396fb30  5       96      0       False     2024-10-26 07:48:21.000000 UTC  N/A     Disabled
240     1828    cmd.exe 0xfa8003aceb30  1       21      1       False   2024-10-26 07:48:29.000000 UTC    N/A     Disabled
300     352     conhost.exe     0xfa8003aabb30  3       55      1       False     2024-10-26 07:48:29.000000 UTC  N/A     Disabled
800     1828    iexplore.exe    0xfa8003ae5060  16      434     1       True      2024-10-26 07:48:43.000000 UTC  N/A     Disabled
1120    800     iexplore.exe    0xfa80039f0a90  19      405     1       True      2024-10-26 07:48:43.000000 UTC  N/A     Disabled
740     800     iexplore.exe    0xfa8002a33060  24      641     1       True      2024-10-26 07:48:46.000000 UTC  N/A     Disabled
2300    1684    SearchProtocol  0xfa8003bcd600  7       248     1       False     2024-10-26 07:49:02.000000 UTC  N/A     Disabled
2520    436     svchost.exe     0xfa8003bd3550  11      132     0       False     2024-10-26 07:50:03.000000 UTC  N/A     Disabled
2552    436     sppsvc.exe      0xfa80036bdad0  6       150     0       False     2024-10-26 07:50:03.000000 UTC  N/A     Disabled
2588    436     svchost.exe     0xfa8001a2c060  12      309     0       False     2024-10-26 07:50:03.000000 UTC  N/A     Disabledf
```


#### 2.2树状图查看
```sh
(base) kaisenye@kaisendeMacBook-Air volatility % python3 ./volatility3/vol.py -f 111.vmem windows.pstree.PsTree
Volatility 3 Framework 2.27.1
WARNING  volatility3.framework.layers.vmware: No metadata file found alongside VMEM file. A VMSS or VMSN file may be required to correctly process a VMEM file. These should be placed in the same directory with the same file name, e.g. 111.vmem and 111.vmss.
Progress:    0.00               Scanning layer_name using PdbSignatureScanProgress:    0.00               Scanning layer_name using PdbSignatureScanProgress:   40.33               Scanning layer_name using PdbSignatureScanProgress:  100.00               PDB scanning finished                        
PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionIdWow64    CreateTime      ExitTime        Audit   Cmd     Path

4       0       System  0xfa80018d0040  68      468     N/A     False   2024-10-26 07:48:01.000000 UTC    N/A     -       -       -
* 228   4       smss.exe        0xfa8002ccdb30  2       29      N/A     False     2024-10-26 07:48:01.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\smss.exe \SystemRoot\System32\smss.exe   \SystemRoot\System32\smss.exe
292     284     csrss.exe       0xfa80033ca950  8       337     0       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\csrss.exe        %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,20480,768 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16      C:\Windows\system32\csrss.exe
340     284     wininit.exe     0xfa80033d2060  3       76      0       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\wininit.exe      wininit.exe     C:\Windows\system32\wininit.exe
* 444   340     lsass.exe       0xfa80034146f0  7       572     0       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\lsass.exe        C:\Windows\system32\lsass.exe   C:\Windows\system32\lsass.exe
* 452   340     lsm.exe 0xfa800340c560  10      135     0       False   2024-10-26 07:48:02.000000 UTC    N/A     \Device\HarddiskVolume1\Windows\System32\lsm.exe  C:\Windows\system32\lsm.exe     C:\Windows\system32\lsm.exe
* 436   340     services.exe    0xfa800340a740  9       196     0       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\services.exe     C:\Windows\system32\services.exe        C:\Windows\system32\services.exe
** 672  436     svchost.exe     0xfa8003582350  21      459     0       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\System32\svchost.exe -k LocalServiceNetworkRestricted  C:\Windows\System32\svchost.exe
*** 912 672     audiodg.exe     0xfa800363f3b0  4       116     0       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\audiodg.exe      C:\Windows\system32\AUDIODG.EXE 0x298   C:\Windows\system32\AUDIODG.EXE
** 256  436     spoolsv.exe     0xfa80037205f0  13      263     0       False     2024-10-26 07:48:03.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\spoolsv.exe      C:\Windows\System32\spoolsv.exe C:\Windows\System32\spoolsv.exe
** 1760 436     taskhost.exe    0xfa8003935060  10      167     1       False     2024-10-26 07:48:15.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\taskhost.exe     "taskhost.exe"  C:\Windows\system32\taskhost.exe
** 964  436     svchost.exe     0xfa800365f060  12      261     0       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\system32\svchost.exe -k LocalService   C:\Windows\system32\svchost.exe
** 356  436     svchost.exe     0xfa8003665b30  20      481     0       False     2024-10-26 07:48:03.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\system32\svchost.exe -k NetworkService C:\Windows\system32\svchost.exe
** 2520 436     svchost.exe     0xfa8003bd3550  11      132     0       False     2024-10-26 07:50:03.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\system32\svchost.exe -k LocalServiceAndNoImpersonation C:\Windows\system32\svchost.exe
** 2552 436     sppsvc.exe      0xfa80036bdad0  6       150     0       False     2024-10-26 07:50:03.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\sppsvc.exe       C:\Windows\system32\sppsvc.exe  C:\Windows\system32\sppsvc.exe
** 620  436     svchost.exe     0xfa8003556140  6       239     0       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\system32\svchost.exe -k RPCSS C:\Windows\system32\svchost.exe
** 556  436     svchost.exe     0xfa8003419b30  10      342     0       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\system32\svchost.exe -k DcomLaunch     C:\Windows\system32\svchost.exe
** 1420 436     svchost.exe     0xfa800378ab30  5       96      0       False     2024-10-26 07:48:03.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\system32\svchost.exe -k NetworkServiceNetworkRestricted        C:\Windows\system32\svchost.exe
** 1040 436     svchost.exe     0xfa8003738420  20      325     0       False     2024-10-26 07:48:03.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\system32\svchost.exe -k LocalServiceNoNetwork  C:\Windows\system32\svchost.exe
** 852  436     svchost.exe     0xfa8003628780  40      1025    0       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\system32\svchost.exe -k netsvcsC:\Windows\system32\svchost.exe
** 1556 436     svchost.exe     0xfa800389eb30  7       92      0       False     2024-10-26 07:48:03.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\system32\svchost.exe -k bthsvcsC:\Windows\system32\svchost.exe
** 1684 436     SearchIndexer.  0xfa8003717060  13      599     0       False     2024-10-26 07:48:21.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\SearchIndexer.exe        C:\Windows\system32\SearchIndexer.exe /Embedding  C:\Windows\system32\SearchIndexer.exe
*** 1984        1684    SearchFilterHo  0xfa800396fb30  5       96      0False    2024-10-26 07:48:21.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\SearchFilterHost.exe     "C:\Windows\system32\SearchFilterHost.exe" 0 500 504 512 65536 508        C:\Windows\system32\SearchFilterHost.exe
*** 2300        1684    SearchProtocol  0xfa8003bcd600  7       248     1False    2024-10-26 07:49:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\SearchProtocolHost.exe   "C:\Windows\system32\SearchProtocolHost.exe" Global\UsGthrFltPipeMssGthrPipe_S-1-5-21-1821445206-1600172521-4289309864-10002_ Global\UsGthrCtrlFltPipeMssGthrPipe_S-1-5-21-1821445206-1600172521-4289309864-10002 1 -2147483646 "Software\Microsoft\Windows Search" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT; MS Search 4.0 Robot)" "C:\ProgramData\Microsoft\Search\Data\Temp\usgthrsvc" "DownLevelDaemon"  "1"      C:\Windows\system32\SearchProtocolHost.exe
** 792  436     svchost.exe     0xfa80035b1b30  16      300     0       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\System32\svchost.exe -k LocalSystemNetworkRestricted   C:\Windows\System32\svchost.exe
*** 1812        792     dwm.exe 0xfa800394e9f0  4       71      1       False     2024-10-26 07:48:15.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\dwm.exe  "C:\Windows\system32\Dwm.exe"   C:\Windows\system32\Dwm.exe
** 2588 436     svchost.exe     0xfa8001a2c060  12      309     0       False     2024-10-26 07:50:03.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\svchost.exe      C:\Windows\System32\svchost.exe -k secsvcsC:\Windows\System32\svchost.exe
352     332     csrss.exe       0xfa8003341630  7       203     1       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\csrss.exe        %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,20480,768 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16      C:\Windows\system32\csrss.exe
* 300   352     conhost.exe     0xfa8003aabb30  3       55      1       False     2024-10-26 07:48:29.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\conhost.exe      \??\C:\Windows\system32\conhost.exe     C:\Windows\system32\conhost.exe
392     332     winlogon.exe    0xfa80033de2d0  4       115     1       False     2024-10-26 07:48:02.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\System32\winlogon.exe     winlogon.exe    C:\Windows\system32\winlogon.exe
1828    1792    explorer.exe    0xfa8003958b30  19      629     1       False     2024-10-26 07:48:15.000000 UTC  N/A     \Device\HarddiskVolume1\Windows\explorer.exe      C:\Windows\Explorer.EXE C:\Windows\Explorer.EXE
* 240   1828    cmd.exe 0xfa8003aceb30  1       21      1       False   2024-10-26 07:48:29.000000 UTC    N/A     \Device\HarddiskVolume1\Windows\System32\cmd.exe  "C:\Windows\system32\cmd.exe"   C:\Windows\system32\cmd.exe
* 800   1828    iexplore.exe    0xfa8003ae5060  16      434     1       True      2024-10-26 07:48:43.000000 UTC  N/A     \Device\HarddiskVolume1\Program Files (x86)\Internet Explorer\iexplore.exe        "C:\Program Files (x86)\Internet Explorer\iexplore.exe"   C:\Program Files (x86)\Internet Explorer\iexplore.exe
** 1120 800     iexplore.exe    0xfa80039f0a90  19      405     1       True      2024-10-26 07:48:43.000000 UTC  N/A     \Device\HarddiskVolume1\Program Files (x86)\Internet Explorer\iexplore.exe        "C:\Program Files (x86)\Internet Explorer\iexplore.exe" SCODEF:800 CREDAT:71937   C:\Program Files (x86)\Internet Explorer\iexplore.exe
** 740  800     iexplore.exe    0xfa8002a33060  24      641     1       True      2024-10-26 07:48:46.000000 UTC  N/A     \Device\HarddiskVolume1\Program Files (x86)\Internet Explorer\iexplore.exe        "C:\Program Files (x86)\Internet Explorer\iexplore.exe" SCODEF:800 CREDAT:71939   C:\Program Files (x86)\Internet Explorer\iexplore.exe
```


#### 2.3扫描发现隐藏进程
pslist 只能看到活动进程链表里的进程。如果一个进程通过某些Rootkit技术把自己从链表里摘掉了，pslist就看不到它。但 psscan 可以通过扫描整个内存来找到它。
```sh
(base) kaisenye@kaisendeMacBook-Air volatility % python3 ./volatility3/vol.py -f 111.vmem windows.psscan.PsScan

   
PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionIdWow64    CreateTime      ExitTime        File output

300     352     conhost.exe     0x7dcabb30      3       55      1       False     2024-10-26 07:48:29.000000 UTC  N/A     Disabled
240     1828    cmd.exe 0x7dcceb30      1       21      1       False   2024-10-26 07:48:29.000000 UTC    N/A     Disabled
800     1828    iexplore.exe    0x7dce5060      16      434     1       True      2024-10-26 07:48:43.000000 UTC  N/A     Disabled
2300    1684    SearchProtocol  0x7ddcd600      7       248     1       False     2024-10-26 07:49:02.000000 UTC  N/A     Disabled
2520    436     svchost.exe     0x7ddd3550      11      132     0       False     2024-10-26 07:50:03.000000 UTC  N/A     Disabled
1556    436     svchost.exe     0x7de9eb30      7       92      0       False     2024-10-26 07:48:03.000000 UTC  N/A     Disabled
1760    436     taskhost.exe    0x7df35060      10      167     1       False     2024-10-26 07:48:15.000000 UTC  N/A     Disabled
1812    792     dwm.exe 0x7df4e9f0      4       71      1       False   2024-10-26 07:48:15.000000 UTC    N/A     Disabled
1828    1792    explorer.exe    0x7df58b30      19      629     1       False     2024-10-26 07:48:15.000000 UTC  N/A     Disabled
1984    1684    SearchFilterHo  0x7df6fb30      5       96      0       False     2024-10-26 07:48:21.000000 UTC  N/A     Disabled
1120    800     iexplore.exe    0x7dff0a90      19      405     1       True      2024-10-26 07:48:43.000000 UTC  N/A     Disabled
852     436     svchost.exe     0x7e028780      40      1025    0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
912     672     audiodg.exe     0x7e03f3b0      4       116     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
964     436     svchost.exe     0x7e05f060      12      261     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
356     436     svchost.exe     0x7e065b30      20      481     0       False     2024-10-26 07:48:03.000000 UTC  N/A     Disabled
2552    436     sppsvc.exe      0x7e0bdad0      6       150     0       False     2024-10-26 07:50:03.000000 UTC  N/A     Disabled
1684    436     SearchIndexer.  0x7e117060      13      599     0       False     2024-10-26 07:48:21.000000 UTC  N/A     Disabled
256     436     spoolsv.exe     0x7e1205f0      13      263     0       False     2024-10-26 07:48:03.000000 UTC  N/A     Disabled
1040    436     svchost.exe     0x7e138420      20      325     0       False     2024-10-26 07:48:03.000000 UTC  N/A     Disabled
1420    436     svchost.exe     0x7e18ab30      5       96      0       False     2024-10-26 07:48:03.000000 UTC  N/A     Disabled
436     340     services.exe    0x7e20a740      9       196     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
452     340     lsm.exe 0x7e20c560      10      135     0       False   2024-10-26 07:48:02.000000 UTC    N/A     Disabled
444     340     lsass.exe       0x7e2146f0      7       572     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
556     436     svchost.exe     0x7e219b30      10      342     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
620     436     svchost.exe     0x7e356140      6       239     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
672     436     svchost.exe     0x7e382350      21      459     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
792     436     svchost.exe     0x7e3b1b30      16      300     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
352     332     csrss.exe       0x7e541630      7       203     1       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
292     284     csrss.exe       0x7e5ca950      8       337     0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
340     284     wininit.exe     0x7e5d2060      3       76      0       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
392     332     winlogon.exe    0x7e5de2d0      4       115     1       False     2024-10-26 07:48:02.000000 UTC  N/A     Disabled
228     4       smss.exe        0x7eacdb30      2       29      N/A     False     2024-10-26 07:48:01.000000 UTC  N/A     Disabled
740     800     iexplore.exe    0x7ec33060      24      641     1       True      2024-10-26 07:48:46.000000 UTC  N/A     Disabled
2588    436     svchost.exe     0x7fc2c060      12      309     0       False     2024-10-26 07:50:03.000000 UTC  N/A     Disabled
4       0       System  0x7ffc9040      68      468     N/A     False   2024-10-26 07:48:01.000000 UTC    N/A     Disabled
```
### 3.网络查询
```sh
(base) kaisenye@kaisendeMacBook-Air volatility % python3 ./volatility3/vol.py -f 111.vmem windows.netscan.NetScan
Volatility 3 Framework 2.27.1
WARNING  volatility3.framework.layers.vmware: No metadata file found alongside VMEM file. A VMSS or VMSN file may be required to correctly process a VMEM file. These should be placed in the same directory with the same file name, e.g. 111.vmem and 111.vmss.
Progress:    0.00               Scanning layer_name using PdbSignatureScanProgress:    0.00               Scanning layer_name using PdbSignatureScanProgress:   40.33               Scanning layer_name using PdbSignatureScanProgress:  100.00               PDB scanning finished                        
Offset  Proto   LocalAddr       LocalPort       ForeignAddr     ForeignPort       State   PID     Owner   Created

0x7dc083e0      UDPv6   fe80::6074:9a4a:96d8:7b6d       62994   *       02520     svchost.exe     2024-10-26 07:50:03.000000 UTC
0x7dc952b0      UDPv4   127.0.0.1       62997   *       0               2520      svchost.exe     2024-10-26 07:50:03.000000 UTC
0x7dce5cf0      TCPv4   192.168.11.137  49163   202.89.233.100  80      CLOSED    740     iexplore.exe    N/A
0x7dd3f830      UDPv4   127.0.0.1       50341   *       0               740       iexplore.exe    2024-10-26 07:48:47.000000 UTC
0x7dd6e010      TCPv4   -       0       136.135.98.3    0       CLOSED  740       iexplore.exe    N/A
0x7dd77ae0      TCPv4   192.168.11.137  49188   202.89.233.101  80      CLOSED    740     iexplore.exe    N/A
0x7dd8ccf0      TCPv4   192.168.11.137  49210   202.89.233.101  443     CLOSED    740     iexplore.exe    N/A
0x7dd96010      TCPv4   192.168.11.137  49199   23.218.94.227   80      ESTABLISHED       740     iexplore.exe    N/A
0x7ddd4010      TCPv4   -       0       136.135.98.3    0       CLOSED  740       iexplore.exe    N/A
0x7de45970      UDPv4   0.0.0.0 500     *       0               852     svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7de47d00      UDPv4   0.0.0.0 4500    *       0               852     svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7de4a640      UDPv4   0.0.0.0 4500    *       0               852     svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7de4a640      UDPv6   ::      4500    *       0               852     svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7de4ad00      UDPv4   0.0.0.0 500     *       0               852     svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7de4ad00      UDPv6   ::      500     *       0               852     svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7de4bcd0      UDPv4   0.0.0.0 0       *       0               852     svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7de4d1a0      UDPv4   0.0.0.0 0       *       0               852     svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7de4d1a0      UDPv6   ::      0       *       0               852     svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7de4f7e0      TCPv4   0.0.0.0 49155   0.0.0.0 0       LISTENING       436       services.exe    -
0x7de4f7e0      TCPv6   ::      49155   ::      0       LISTENING       436       services.exe    -
0x7de5fc30      TCPv4   0.0.0.0 49155   0.0.0.0 0       LISTENING       436       services.exe    -
0x7de638a0      TCPv4   0.0.0.0 445     0.0.0.0 0       LISTENING       4System   -
0x7de638a0      TCPv6   ::      445     ::      0       LISTENING       4System   -
0x7deca290      UDPv4   192.168.11.137  62996   *       0               2520      svchost.exe     2024-10-26 07:50:03.000000 UTC
0x7e0dfeb0      TCPv4   192.168.11.137  139     0.0.0.0 0       LISTENING4System  -
0x7e0e2a50      UDPv4   192.168.11.137  138     *       0               4System   2024-10-26 07:48:03.000000 UTC
0x7e0e3920      UDPv4   192.168.11.137  137     *       0               4System   2024-10-26 07:48:03.000000 UTC
0x7e0fa500      UDPv4   0.0.0.0 0       *       0               356     svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7e0fa500      UDPv6   ::      0       *       0               356     svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7e1128c0      TCPv4   0.0.0.0 49154   0.0.0.0 0       LISTENING       852       svchost.exe     -
0x7e113730      TCPv4   0.0.0.0 49154   0.0.0.0 0       LISTENING       852       svchost.exe     -
0x7e113730      TCPv6   ::      49154   ::      0       LISTENING       852       svchost.exe     -
0x7e12ad70      UDPv4   0.0.0.0 0       *       0               1420    svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7e12ea90      UDPv4   0.0.0.0 0       *       0               1420    svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7e12ea90      UDPv6   ::      0       *       0               1420    svchost.exe       2024-10-26 07:48:03.000000 UTC
0x7e130940      TCPv4   0.0.0.0 49156   0.0.0.0 0       LISTENING       1420      svchost.exe     -
0x7e146500      TCPv4   0.0.0.0 49156   0.0.0.0 0       LISTENING       1420      svchost.exe     -
0x7e146500      TCPv6   ::      49156   ::      0       LISTENING       1420      svchost.exe     -
0x7e32d850      UDPv4   127.0.0.1       1900    *       0               2520      svchost.exe     2024-10-26 07:50:03.000000 UTC
0x7e332940      UDPv6   ::1     1900    *       0               2520    svchost.exe       2024-10-26 07:50:03.000000 UTC
0x7e332be0      UDPv6   fe80::6074:9a4a:96d8:7b6d       1900    *       02520     svchost.exe     2024-10-26 07:50:03.000000 UTC
0x7e339ad0      UDPv4   192.168.11.137  1900    *       0               2520      svchost.exe     2024-10-26 07:50:03.000000 UTC
0x7e3457d0      UDPv6   ::1     62995   *       0               2520    svchost.exe       2024-10-26 07:50:03.000000 UTC
0x7e373010      TCPv4   0.0.0.0 135     0.0.0.0 0       LISTENING       620       svchost.exe     -
0x7e378350      TCPv4   0.0.0.0 135     0.0.0.0 0       LISTENING       620       svchost.exe     -
0x7e378350      TCPv6   ::      135     ::      0       LISTENING       620       svchost.exe     -
0x7e382900      TCPv4   0.0.0.0 49152   0.0.0.0 0       LISTENING       340       wininit.exe     -
0x7e385b70      TCPv4   0.0.0.0 49152   0.0.0.0 0       LISTENING       340       wininit.exe     -
0x7e385b70      TCPv6   ::      49152   ::      0       LISTENING       340       wininit.exe     -
0x7e38def0      TCPv4   0.0.0.0 49157   0.0.0.0 0       LISTENING       444       lsass.exe       -
0x7e7c3ec0      UDPv4   0.0.0.0 5355    *       0               356     svchost.exe       2024-10-26 07:48:06.000000 UTC
0x7e7c3ec0      UDPv6   ::      5355    *       0               356     svchost.exe       2024-10-26 07:48:06.000000 UTC
0x7e868690      TCPv4   0.0.0.0 49153   0.0.0.0 0       LISTENING       672       svchost.exe     -
0x7e868690      TCPv6   ::      49153   ::      0       LISTENING       672       svchost.exe     -
0x7e868ae0      TCPv4   0.0.0.0 49153   0.0.0.0 0       LISTENING       672       svchost.exe     -
0x7ec6f1d0      TCPv4   192.168.11.137  49164   202.89.233.101  80      CLOSED    740     iexplore.exe    N/A
0x7eca4c30      TCPv4   192.168.11.137  49161   69.192.162.125  80      ESTABLISHED       1120    iexplore.exe    N/A
0x7ed15d70      UDPv4   127.0.0.1       64077   *       0               1120      iexplore.exe    2024-10-26 07:48:43.000000 UTC
0x7f0152c0      TCPv4   0.0.0.0 49157   0.0.0.0 0       LISTENING       444       lsass.exe       -
0x7f0152c0      TCPv6   ::      49157   ::      0       LISTENING       444       lsass.exe       -
0x7f063d80      UDPv4   0.0.0.0 5355    *       0               356     svchost.exe       2024-10-26 07:48:06.000000 UTC
0x7fc2d940      TCPv6   -       0       8887:6203:80fa:ffff:8887:6203:80fa:ffff   0       CLOSED  740     iexplore.exe    N/A
0x7fe4c900      TCPv6   -       0       8887:6203:80fa:ffff:8887:6203:80fa:ffff   0       CLOSED  740     iexplore.exe    N/A
```



### 4.提取凭证
```sh
(base) kaisenye@kaisendeMacBook-Air volatility % python3 ./volatility3/vol.py -f 111.vmem windows.registry.hashdump.Hashdump
```

- **作用**：V3的 hashdump 插件功能与V2完全相同，它会通过解析内存中的注册表Hive文件（特别是SAM和SYSTEM），提取出所有本地用户的 **NTLM 哈希**。
- **后续操作**：拿到哈希后，就可以用 John the Ripper 或 Hashcat 进行离线破解了。

```sh
User    rid     lmhash  nthash

Administrator   500     aad3b435b51404eeaad3b435b51404ee        31d6cfe0d16ae931b73c59d7e0c089c0
Guest   501     aad3b435b51404eeaad3b435b51404ee        31d6cfe0d16ae931b73c59d7e0c089c0
admin   1000    aad3b435b51404eeaad3b435b51404ee        b04e9417d1983439dba83540c3f0a1e4
hxx789456       1001    aad3b435b51404eeaad3b435b51404ee        841f779368eff4c81bbc65e77191ecac
swjd    1002    aad3b435b51404eeaad3b435b51404ee        c29bf61d2a53a55e8679265f5b76c0a9
slsd    1003    aad3b435b51404eeaad3b435b51404ee        9119607211d959ef52844933d1619f73
```
### 5.查询历史
```sh
(base) kaisenye@kaisendeMacBook-Air volatility % python3 ./volatility3/vol.py -f 111.vmem windows.cmdline.CmdLine
```
查看命令和程序启动时带了哪些参数

```sh
PID     Process Args

4       System  -
228     smss.exe        \SystemRoot\System32\smss.exe
292     csrss.exe       %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,20480,768 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16
340     wininit.exe     wininit.exe
352     csrss.exe       %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,20480,768 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16
392     winlogon.exe    winlogon.exe
436     services.exe    C:\Windows\system32\services.exe
444     lsass.exe       C:\Windows\system32\lsass.exe
452     lsm.exe C:\Windows\system32\lsm.exe
556     svchost.exe     C:\Windows\system32\svchost.exe -k DcomLaunch
620     svchost.exe     C:\Windows\system32\svchost.exe -k RPCSS
672     svchost.exe     C:\Windows\System32\svchost.exe -k LocalServiceNetworkRestricted
792     svchost.exe     C:\Windows\System32\svchost.exe -k LocalSystemNetworkRestricted
852     svchost.exe     C:\Windows\system32\svchost.exe -k netsvcs
912     audiodg.exe     C:\Windows\system32\AUDIODG.EXE 0x298
964     svchost.exe     C:\Windows\system32\svchost.exe -k LocalService
356     svchost.exe     C:\Windows\system32\svchost.exe -k NetworkService
256     spoolsv.exe     C:\Windows\System32\spoolsv.exe
1040    svchost.exe     C:\Windows\system32\svchost.exe -k LocalServiceNoNetwork
1420    svchost.exe     C:\Windows\system32\svchost.exe -k NetworkServiceNetworkRestricted
1556    svchost.exe     C:\Windows\system32\svchost.exe -k bthsvcs
1760    taskhost.exe    "taskhost.exe"
1812    dwm.exe "C:\Windows\system32\Dwm.exe"
1828    explorer.exe    C:\Windows\Explorer.EXE
1684    SearchIndexer.  C:\Windows\system32\SearchIndexer.exe /Embedding
1984    SearchFilterHo  "C:\Windows\system32\SearchFilterHost.exe" 0 500 504 512 65536 508 
240     cmd.exe "C:\Windows\system32\cmd.exe" 
300     conhost.exe     \??\C:\Windows\system32\conhost.exe
800     iexplore.exe    "C:\Program Files (x86)\Internet Explorer\iexplore.exe" 
1120    iexplore.exe    "C:\Program Files (x86)\Internet Explorer\iexplore.exe" SCODEF:800 CREDAT:71937
740     iexplore.exe    "C:\Program Files (x86)\Internet Explorer\iexplore.exe" SCODEF:800 CREDAT:71939
2300    SearchProtocol  "C:\Windows\system32\SearchProtocolHost.exe" Global\UsGthrFltPipeMssGthrPipe_S-1-5-21-1821445206-1600172521-4289309864-10002_ Global\UsGthrCtrlFltPipeMssGthrPipe_S-1-5-21-1821445206-1600172521-4289309864-10002 1 -2147483646 "Software\Microsoft\Windows Search" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT; MS Search 4.0 Robot)" "C:\ProgramData\Microsoft\Search\Data\Temp\usgthrsvc" "DownLevelDaemon"  "1"
2520    svchost.exe     C:\Windows\system32\svchost.exe -k LocalServiceAndNoImpersonation
2552    sppsvc.exe      C:\Windows\system32\sppsvc.exe
2588    svchost.exe     C:\Windows\System32\svchost.exe -k secsvcs
```

翻历史
```sh
(base) kaisenye@kaisendeMacBook-Air volatility % python3 ./volatility3/vol.py -f 111.vmem windows.consoles.Consoles

    raise NotImplementedError(
NotImplementedError: This version of Windows is not supported: 6.1 15.7600!
```

有哪些用户名？

```
Administrator
Guest
admin
hxx789456
swjd
slsd
```
admin的密码？

```
#john
/ctf/john/run/john --wordlist=/ctf/dic/rockyou.txt --format=NT /ctf/work/hi.txt

#hashcat用法
root@fff4586fafba:/ctf/work# hashcat -m 1000 -a 0 hi.txt /ctf/dic/rockyou.txt

#找到b04e9417d1983439dba83540c3f0a1e4:111456    
```

输入的最后一条命令？

浏览器的搜索记录？

隐藏在用户账号中的flag？
# 3.日志分析和流量分析
```
strings file.pacp | grep 'flag{'
```

PACP流量包：
流量包是怎么来的？抓来的。
开启wireshark抓包，选择网卡wifi-en0
```
(base) kaisenye@kaisendeMacBook-Air ~ % ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=107 time=74.157 ms
64 bytes from 8.8.8.8: icmp_seq=1 ttl=107 time=76.355 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=107 time=83.243 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=107 time=77.306 ms
```
我们用协议过滤就可以看到这部分对应的数据包。
![[Pasted image 20251210143729.png]]
数据包详细信息是这一块
  （1）Frame:   物理层的数据帧概况
  （2）Ethernet II: 数据链路层以太网帧头部信息
  （3）Internet Protocol Version 4: 互联网层IP包头部信息
  （4）Transmission Control Protocol:  传输层T的数据段头部信息，此处是TCP
  （5）Hypertext Transfer Protocol:  应用层的信息，此处是HTTP协议
![[Pasted image 20251210150023.png]]

![[Pasted image 20251210145756.png]]
所以底层传输的仍然是二进制数据，我们通过wireshark就可以实现取证分析。
Wireshark基本使用分为数据包筛选、数据包搜索、数据包还原、数据提取
### 过滤器的使用
Wireshark 中有捕获过滤器（**Capture Filter**）和**显示过滤器 (Display Filter)**，我们常用的是后者，也就是这个框里。

#### 显示过滤器的核心语法

Wireshark 的显示过滤器栏有一个很棒的功能：当你输入时，输入框的背景颜色会变化：

- **绿色:** 语法正确，可以生效。
- **红色:** 语法错误，无法使用。
- **黄色:** 语法可能有效，但存在歧义或不推荐的用法。

1. 按协议过滤 (最常用)
最简单、最直接。http、tcp、udp、dns、icmp、ftp、arp
2. 按IP地址和端口过滤
IP 地址:
ip.addr == 192.168.1.1 (源或目的IP是它)
ip.src == 192.168.1.1 (源IP是它)
ip.dst == 192.168.1.1 (目的IP是它)
端口:
tcp.port == 80 (源或目的TCP端口是80)
tcp.srcport == 8080 (源TCP端口是8080)
udp.dstport == 53 (目的UDP端口是53)
3. 逻辑运算符组合
这是让过滤器变得强大的关键！
等于: == 或 eq
不等于: != 或 ne
与: && 或 and
或: || 或 or
非: ! 或 not
组合示例：
ip.src == 10.0.0.5 && tcp.dstport == 80
(查找从 10.0.0.5 发出，到 80 端口的 TCP 包)
http or dns
(显示所有的 HTTP 和 DNS 流量)
!(arp or icmp)
(隐藏所有的 ARP 和 ICMP 包，专注于看应用层流量)

这篇文章很全面 https://cloud.tencent.com/developer/article/2462400
## 协议分析
基础知识 https://www.runoob.com/np/np-tutorial.html


### http流量
明文传输
![[Pasted image 20251216154541.png]]
```
(base) kaisenye@kaisendeMacBook-Air http % strings ./http.pcapng | grep 'flag{'  
X@Yflag{This_is_a_f10g}
```

### HTTPS
https://www.runoob.com/http/http-intro.html
https = http + SSL/TLS，服务端和客户端的信息传输都会通过 TLS 进行加密，所以传输的数据都是加密后的数据
#### INSHack2019 Passthru

![[Pasted image 20251216174700.png]]

![[Pasted image 20251216192248.png]]

查看到可疑的kcahsni。
```sh
tshark -2 -r capture.pcap -o 'tls.keylog_file:sslkey.log' -Y 'http.request.uri contains "kcahsni"' -T fields -e http.request.uri.query.parameter > query.txt

```
```python
from urllib.parse import unquote
import re
with open('query.txt', 'r') as f:
    data = unquote(f.read())

rlist = re.findall(r'kcahsni=(.*?),',data)
print(bytes.fromhex(''.join(rlist))[::-1])

```
![[Pasted image 20251216194841.png]]


### DNS


### USB流量分析

https://ctf-wiki.org/misc/traffic/protocols/usb/
#### 鼠标流量
#### 键盘流量




# 4. 音频隐写
用au打开，首先会看到波形图，可以选择频谱图，多视图，都看一下，有时候直接就看到了。

## 波形
### BUUCTF来首歌吧
https://buuoj.cn/challenges#%E6%9D%A5%E9%A6%96%E6%AD%8C%E5%90%A7

![[Pasted image 20251211221529.png]]

我们发现上面像Morse电码。我们可以在左边选择只听左声道，确实是morse电码的声音。
```
..... -... -.-. ----. ..--- ..... -.... ....- ----. -.-. -... ----- .---- ---.. ---.. ..-. ..... ..--- . -.... .---- --... -.. --... ----- ----. ..--- ----. .---- ----. .---- -.-.
#丢入cyberchef
flag{5BC925649CB0188F52E617D70929191C}
```
## 频谱
### INSHack2018 not so deep
https://buuoj.cn/challenges#[INSHack2018](not)%20so%20deep

此类音频通常会有一个较明显的特征，听起来是一段杂音或者比较刺耳。

![[Pasted image 20251211194932.png]]
一开始波形图看不出东西，我们就点频谱图。
### deepsound
这道题的后半段需要deepsound工具。
deepsound是一个**音频隐写与加密工具**。它做了：
封装 ：Deepsound首先将你要隐藏的文件（载荷, Payload）封装进一个音频文件（宿主, Host）的二进制结构中。
加密 ：在封装的同时，它使用你提供的密码，通过一个密钥派生函数 (KDF)，生成一个加密密钥。然后，它使用一个对称加密算法（如AES）和这个密钥，对隐藏文件进行加密。
存储验证信息：为了能在解密时验证密码是否正确，Deepsound必须在音频文件的某个地方存储一个密码验证器 (Password Verifier)。这通常是你输入的密码经过特定哈希算法得到的结果。
![[Pasted image 20251211210733.png]]
我们要输入密码,密码我们需要通过一个./deepsound2john.py脚本提取。这个脚本作为一个哈希提取器。
```sh
root@6d6d3b24a14d:/ctf/work/yinpin/yinxie/tmp# ./deepsound2john.py final_flag.wav > hash.txt
root@6d6d3b24a14d:/ctf/work/yinpin/yinxie/tmp# cat hash.txt 
final_flag.wav:$dynamic_1529$b8f858d9deb0b805797cef03299e3bdd8990f48a
root@6d6d3b24a14d:/ctf/john/run# ./john /ctf/work/yinpin/yinxie/tmp/hash.txt
Using default input encoding: UTF-8
Loaded 1 password hash (dynamic_1529 [sha1($p null_padded_to_len_32) (DeepSound) 128/128 SSE4.1 4x1])
Warning: no OpenMP support for this hash type, consider --fork=10
Note: Passwords longer than 36 [worst case UTF-8] to 110 [ASCII] rejected
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
0g 0:00:00:00 DONE 1/3 (2025-12-11 20:48) 0g/s 1163Kp/s 1163Kc/s 1163KC/s Wavflag1900..Wflag1900
Proceeding with wordlist:./password.lst
Enabling duplicate candidate password suppressor using 256 MiB
azerty           (final_flag.wav)     
1g 0:00:00:00 DONE 2/3 (2025-12-11 20:48) 12.50g/s 353987p/s 353987c/s 353987C/s Hammer..blahblah1
Use the "--show --format=dynamic_1529" options to display all of the cracked passwords reliably
Session completed


```
![[Pasted image 20251211210718.png]]


```python
#!/usr/bin/env python3
'''
deepsound2john extracts password hashes from audio files containing encrypted
data steganographically embedded by DeepSound (http://jpinsoft.net/deepsound/).

This method is known to work with files created by DeepSound 2.0.

Input files should be in .wav format. Hashes can be recovered from audio files
even after conversion from other formats, e.g.,

    ffmpeg -i input output.wav

Usage:

    python3 deepsound2john.py carrier.wav > hashes.txt
    john hashes.txt

This software is copyright (c) 2018 Ryan Govostes <rgovostes@gmail.com>, and
it is hereby released to the general public under the following terms:
Redistribution and use in source and binary forms, with or without
modification, are permitted.
'''

import logging
import os
import sys
import textwrap


def decode_data_low(buf):
  return buf[::2]

def decode_data_normal(buf):
  out = bytearray()
  for i in range(0, len(buf), 4):
    out.append((buf[i] & 15) << 4 | (buf[i + 2] & 15))
  return out

def decode_data_high(buf):
  out = bytearray()
  for i in range(0, len(buf), 8):
    out.append((buf[i] & 3) << 6     | (buf[i + 2] & 3) << 4 \
             | (buf[i + 4] & 3) << 2 | (buf[i + 6] & 3))
  return out


def is_magic(buf):
  # This is a more efficient way of testing for the `DSCF` magic header without
  # decoding the whole buffer
  return (buf[0] & 15)  == (68 >> 4) and (buf[2]  & 15) == (68 & 15) \
     and (buf[4] & 15)  == (83 >> 4) and (buf[6]  & 15) == (83 & 15) \
     and (buf[8] & 15)  == (67 >> 4) and (buf[10] & 15) == (67 & 15) \
     and (buf[12] & 15) == (70 >> 4) and (buf[14] & 15) == (70 & 15)


def is_wave(buf):
  return buf[0:4] == b'RIFF' and buf[8:12] == b'WAVE'


def process_deepsound_file(f):
  bname = os.path.basename(f.name)
  logger = logging.getLogger(bname)

  # Check if it's a .wav file
  buf = f.read(12)
  if not is_wave(buf):
    global convert_warn
    logger.error('file not in .wav format')
    convert_warn = True
    return
  f.seek(0, os.SEEK_SET)

  # Scan for the marker...
  hdrsz = 104
  hdr = None

  while True:
    off = f.tell()
    buf = f.read(hdrsz)
    if len(buf) < hdrsz: break

    if is_magic(buf):
          hdr = decode_data_normal(buf)
          logger.info('found DeepSound header at offset %i', off)
          break

    f.seek(-hdrsz + 1, os.SEEK_CUR)

  if hdr is None:
    logger.warn('does not appear to be a DeepSound file')
    return

  # Check some header fields
  mode = hdr[4]
  encrypted = hdr[5]

  modes = {2: 'low', 4: 'normal', 8: 'high'}
  if mode in modes:
    logger.info('data is encoded in %s-quality mode', modes[mode])
  else:
    logger.error('unexpected data encoding mode %i', modes[mode])
    return

  if encrypted == 0:
    logger.warn('file is not encrypted')
    return
  elif encrypted != 1:
    logger.error('unexpected encryption flag %i', encrypted)
    return

  sha1 = hdr[6:6+20]
  print('%s:$dynamic_1529$%s' % (bname, sha1.hex()))


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('--verbose', '-v', action='store_true')
  parser.add_argument('files', nargs='+', metavar='file',
    type=argparse.FileType('rb', bufsize=4096))
  args = parser.parse_args()

  if args.verbose:
    logging.basicConfig(level=logging.INFO)
  else:
    logging.basicConfig(level=logging.WARN)

  convert_warn = False

  for f in args.files:
    process_deepsound_file(f)

  if convert_warn:
    print(textwrap.dedent('''
    ---------------------------------------------------------------
    Some files were not in .wav format. Try converting them to .wav
    and try again. You can use: ffmpeg -i input output.wav
    ---------------------------------------------------------------
    '''.rstrip()), file=sys.stderr)

```

# 5. 图片隐写

## png格式介绍
**文件头 (File Signature): 89 50 4E 47 0D 0A 1A 0A**
    - 每一个健康的PNG文件，它的开头**必须**是这8个字节。中间的50 4E 47，是**P-N-G**三个字母的ASCII码。所以用文本编辑器打开它时，能直接看到PNG这几个字母。”

**IHDR (Image HeaDeR)**。紧跟在文件头后面
- **IHDR块的结构**
    1. 00 00 00 0D (4字节): 块长度，固定为13字节。
    2. 49 48 44 52 (4字节): 块类型码，即“IHDR”。
    3. **宽 度 (4字节)**: 图片的宽度。比如00 00 03 FE 
    4. **高 度 (4字节)**: 图片的高度。比如00 00 03 FC
    5. ... (后面还有5字节的其他信息，如色深、颜色类型等)。
		CRC校验位：4字节
- https://www.ip33.com/crc.html

### PNG宽高改写
![[xiyu.png]]
![[Pasted image 20251211121150.png]]
修改高度，然后要在工具中计算CRC（49 48开始的17个字节），填回去，才能正常打开。

![[Pasted image 20251211120053.png]]



**文件尾 (IEND Chunk): 00 00 00 00 49 45 4E 44 AE 42 60 82**
    - 每一个健康的PNG文件，都以一个叫做 **IEND** (Image END) 的数据块结束。这个数据块的内容是固定的（长度为0，CRC固定），它的完整12字节十六进制就是上面这样。至此代表图片数据到此结束。
https://ctf-wiki.org/misc/picture/png/
## jpg格式介绍
**JPEG 文件的格式是分为一个一个的段来存储的**

JPEG文件里除了文件头和尾，中间还有很多不同功能的‘积木块’。好消息是，它们的结构都差不多，遵循一个简单的格式。

- **通用结构**：段标识 (Marker) + 段长度 (Length) + 段内容 (Data)
    - **段标识**：2个字节，总是以FF开头，第二个字节代表这个“积木块”的类型（比如FF C0是图像基本信息，FF C4是定义Huffman表）。
    - **段长度**：2个字节，告诉程序这个“积木块”有多长。
    - **段内容**：具体的设置信息或数据。

“这个结构对我们侦探来说非常有用！因为它意味着，即使我们不认识某个‘积木块’，我们也可以通过读取它的‘长度’，安全地跳过它，去检查下一个。这也方便我们在WinHex里快速定位和识别不同的区域。”


FF D8开始，FF D9结束

| 名称  | 字节数 | 数据  | 说明                     |
| --- | --- | --- | ---------------------- |
| 段标识 | 1   | FF  | 每个新段的开始标识              |
| 段类型 | 1   |     | 类型编码（标记码）              |
| 段长度 | 2   |     | 包括段内容和段长度本身，不包括段标识和段类型 |
| 段内容 |     |     | 不超过65533B              |

在CTFwiki里提到了十几种段，我们不需要全部记住。我们重点关注以下

1. **APP0 段 (标记码 FF E0)**
    - **是什么**：图像识别信息，里面包含了“JFIF”这个字符串。
    - **为什么重要**：它通常紧跟在文件头FF D8后面，是识别一个标准JPEG的重要特征。虽然很少直接藏flag，但如果它损坏或缺失，可能会导致图片无法识别。
2. **EXIF 信息 (通常在 APP1 段，标记码 FF E1)**
    - **是什么**：这是数码相机用来存储照片元数据的地方，比如相机型号、拍摄时间、GPS坐标等。
    - **为什么重要**：**EXIF是隐藏信息的绝佳场所！** 出题人可以把flag藏在“相机型号”、“用户注释”等字段里。
    - **侦查工具**：exiftool。


比如这段数据是 苹果 HDR 图片的 XMP 元数据（可扩展元数据平台），基于 Adobe XMP 标准（http://ns.adobe.com/xap/1.0/）和 W3C RDF 语法（http://www.w3.org/1999/02/22-rdf-syntax-ns#）编写，核心作用是记录苹果 HDR 图片的 像素格式、辅助图像类型、HDR 增益图版本 等关键技术参数，用于图片解析工具（如浏览器、图片查看器）识别和渲染 HDR 效果。
3. **COM 段 (标记码 FF FE)**
    
    - **是什么**：Comment
    - **为什么重要**：它的作用就是在图片里加入一段文字注释。拿到JPG，一定要检查有没有COM段，可能会有flag或者间接hint
    - **工具**：WinHex/010 Editor（直接搜索FF FE），或者strings命令有时也能发现。
## exiftool使用
| 命令                                         | 描述                             |
| :----------------------------------------- | :----------------------------- |
| exiftool test．jpg                          | 显示test．jpg的所有Exif信息            |
| exiftool－s－ImageSize－ExposureTime test．jpg | 显示图片尺寸                         |
| exiftool－common dir                        | 显示dir目录下所有可识别的文件的信息            |
| exiftool－I test1．jpg test2．jpg             | 显示test1．jpg和test2．jpg的所有Exif信息 |
| exiftool－all＝test．jpg                      | 删除test．jpg的所有信息                |
| exiftool－gps：all＝test．jpg                  | 删除test．jpg的GPS信息               |
| exiftool－artist＝me test．jpg                | 将＂me＂写入test．jpg的艺术家标签          |

### 2025CSACTF babySteg

```
exiftool babySteg1.jpg
Comment                         : JPEG Encoder Copyright 1998, James R. Weeks and BioElectroMech.
```
接下来怎么做，后面再说x


## 文件附加与隐写

准备一张图片和一个包含flag的压缩包 
```
echo "flag{append_is_easy}" > flag.txt 
zip secret.zip flag.txt 
cp shuhuai.jpg hidden_shuhuai.jpg 
```
将压缩包附加到图片末尾 cat secret.zip >> hidden_data.jpg
直接查看会看到FF D9后面的50 4B 03 04压缩包开头。
![[Pasted image 20251210230212.png]]
或者使用工具
```
binwalk hidden_shuhuai.jpg
```
![[Pasted image 20251210225758.png]]


一张吃饭的图片![[chifan.jpg]]
```
exiftool -Comment="flag{exif_is_metadata}" chifan.jpg
```

![[Pasted image 20251210234003.png]]
用exiftool chifan.jpg也可以找到
![[Pasted image 20251210234044.png]]
## LSB
 **LSB即最低有效位隐写**
 图片的储存方式：
如果将一幅图像放大，我们可以看到它是由一个个的小格子组成的，每个小格子就是一个色块。如果我们用不同的数字来表示不同的颜色，图像就可以表示为一个由数字组成的矩阵，这样就可以在计算机中存储。这个小格子就是像素，矩阵的行数与列数，就是分辨率。
实现原因：
因为人类的视觉冗余，对相近的像素的敏感度比较低。所以改变部分像素的值，肉眼察觉不到。
原理：
修改RGB颜色分量的最低二进制位也就是最低有效位（LSB），人类的眼睛不会注意到这前后的变化，每个像素可以携带3bit(R,G,B)的信息，因此就可以隐写字符串信息。

我们如何判断这个像素的(R,G,B)是否被修改过?
确实无法判断单个像素，但是整张图片在统计学上是显著的。比如这张AAA的图片，
![[misc_challenge2.png]]
我们采用stegsolve打开，切换到red plane 0，意思是
这张只包含所有每个像素R信息的“灰度图”，就是“Red Plane”
将图片中每一个像素的Red通道值的最低有效位（LSB，也就是第0位）全部提取出来，然后将这些 0 和 1 重新组合成一张新的、黑白的图像进行显示。
![[Pasted image 20251210123002.png]]


有时候，并不是直接用眼睛读的，我们可以用工具去读。
```
zsteg [options] filename.png [param_string]
```
什么密码的图片。
![[Pasted image 20251210113223.png]]
![[Pasted image 20251210114351.png]]


![[Pasted image 20251210113601.png]]















单图异或


双图分析



## F5隐写


这个需要java8低版本，高版本的java会报错

| 描述  | 命令                                                             |
| :-: | :------------------------------------------------------------- |
| 加密  | java Embed＜img＿file＞＜stego＿file＞－e＜payload＿file＞［－p＜password＞］ |
| 解密  | java Extract＜stego＿file＞［－p＜password＞］                         |


```
git clone https://github.com/matthewgao/F5-steganography

#要有java环境
apt-get install openjdk-8-jdk -y
```
### BUUCTF刷新过的图片
```
root@6d6d3b24a14d:/ctf/work/yinxie/tupian/jpg/F5/F5-steganography# java Extract ../Misc.jpg
Huffman decoding starts
Permutation starts
309504 indices shuffled
Extraction starts
Length of embedded file: 190 bytes
(1, 31, 5) code used
查看output.txt(默认输出在output.txt)
发现是PK开头的
```


![[Pasted image 20251212134926.png]]

我们根据之前的经验，发现开头00 00和中间的01 00不一样，是伪加密。然后就按照之前讲的处理一下就可以了。


## GIF介绍
基本概念
GIF（Graphics Interchange Format）具有以下几个特点：
​ 1. 颜色限制：GIF使用8位颜色深度，最多可以显示256种颜色。这些颜色来自一个调色板，这使得GIF适用于简单的图形和动画。
​ 2. 无损压缩：GIF使用Lempel-Ziv-Welch (LZW) 算法进行无损压缩，能够在不损失图像质量的前提下减小文件大小。
​ 3. 支持透明度：GIF支持单一颜色的透明选项，使得背景能够透过图像显示。
​ 4. 动画支持：GIF允许将多个图像帧以序列方式存储，从而创建简单的动画效果。
​ 5. 元数据：GIF文件中还包含一些控制信息，如图像尺寸、帧延迟等。
​ 一个GIF文件的结构可分为文件头（File Header）、GIF数据流（GIF Data Stream）和文件结尾（Trailer）三个部分，GIF文件结构如下表所示：
![[Pasted image 20251212170649.png]]
GIF 文件头部
1. 署名 47 49 46对应ASCII码（GIF）
2. 版本号 3字节组成（“87a”）或者（“89a”）
GIF数据流
3. 图像宽度
4. 图像高度
全局颜色表
5. 全局颜色表大小
6. 位深度
7. 保留位
8. 帧间延迟
- 最大256种颜色，每种颜色占3字节
图像数据块
1. 图像左上角坐标 (X, Y)
2. 图像宽度
3. 图像高度
4. 本地颜色表（可选）
5. 压缩图像数据 (LZW)
6. 帧延迟（用于动画）
7. 透明色（可选）
结束标记
0x3B (分号字符)


GIF分帧

GIF隐写方法
对于GIF，可以采用以下几种隐写方法：

LSB，类似png
帧间隐藏：在GIF动画中，可以利用不同帧之间的差异来隐藏信息，例如，通过改变某些帧的特定像素来存储数据。
使用透明像素：
利用GIF的透明色特性，可以在图像中添加一层透明像素，并在这些透明区域内存储数据。
重复图像：
在GIF中复制某些图像帧，稍微修改这些帧的数据，从而在视觉上不易察觉，同时隐藏信息。
改动颜色表：
对于不显著影响整体外观的情况下，可以对GIF的颜色表进行细微修改，以嵌入数据。
延迟时间：
在89a版本中，GIF添加了图形控制扩展块，它是可选的，可以放在一个图像块或文本扩展块的前面，用来控制跟在它后面的第一个图像（或文本）的渲染形式。这一部分有一个“延迟时间”字段，其单位为1/100s（也就是10ms），如果“延迟时间”字段的值为n，则表示暂停10nms后再继续处理数据流。
文件结尾是一个字节的固定值0x3b，用来指示整个文件的结束。

在CTF比赛中，GIF也是高频考点。重点介绍三种常见的GIF隐写方法：

​ 1）追加插入法隐写，就是在GIF文件后插入其他文件。这种隐写非常容易识别。在010 Editor中利用GIF模版进行解析，如果文件结尾后还有其他数据流，那么很可能在GIF后附加了其他文件，将附加数据提取出来做进一步分析即可。

​ 2）基于图像的隐写。GIF中可以包含多个图像，出题人可以在某幅图像隐写信息。我们需要分离出GIF的每幅图片，并针对每幅图片进一步分析。可以用stegsolver。Analyze，FrameBrowser
![[Pasted image 20251212151211.png]]





## 二维码
二维条码有一维条码没有的“定位点”和“容错机制”。容错机制在即使没有辨识到全部的条码、或是说条码有污损时，也可以正确地还原条码上的信息。

![[Pasted image 20251215105109.png]]

容错率也叫纠错率，就是指二维码可以被遮挡后仍能被正常扫描，而这个能被遮挡的最大面积就是容错率。

**基本概念**：最常见的QR二维码，用的是里德-所罗门码（RS）来做纠错。分有几级，纠错级别越高，整体需要携带的信息越多：L级可纠正约7%错误、M级别可纠正约15%错误、Q级别可纠正约25%错误、H级别可纠正约30%错误。RS码原理比较复杂，整体基于“任意k个确定点可表示一个阶数至少为k-1的多项式”，实际上发送超过k个点，就算中间有一些错误，也能通过数学原理反推出最初的多项式，从而获得信息。并不是所有位置都可以缺损，像最明显的那三个角上的方框，直接影响初始定位。中间零散的部分是内容编码，可以容忍缺损。

修复二维码的工具 https://merri.cx/qrazybox/

什么样的二维码可以修复？少了一点点，一点点模糊是可以的，比如⬇️
![[0269a0bc827a540fd08476997ae27d8d.jpg]]


什么样的修复不了？少了一大半（悲报：数据提错了）
![[b5ab458dba07c0ca9aa98eedda0fcee8.jpg]]

# HomeWork

## 编码
请你自己梳理和复现一下乱码情况

base64


## 哈希

查看一个文件的hash与md5码

根据以下一个简单密码的md5破解它。
f447b20a7fcbf53a5d5be013ea0b15af

## 压缩包
### 伪加密
1. 请你自己创造一个伪加密的zip文件
2. 复现2025省赛什么密码（见附件）。
3. buuctf zip伪加密 https://buuoj.cn/challenges#zip%E4%BC%AA%E5%8A%A0%E5%AF%86
## 流量分析
1. 复现DDCTF2018流量分析（见附件）
2. 2025省赛信创安全红头文件之谜（见附件）

## 图片
### 宽高改写
1. 请你自己尝试用010editor修改随便一幅png图片宽高，并且手动改好crc使得图片能正常打开。
2. BUUCTF大白 https://buuoj.cn/challenges#%E5%A4%A7%E7%99%BD
3. 2025CSACTF Hiddenworld(见附件)
### F5隐写
1. 复现上课的BUUCTF刷新过的图片（见附件）
2. 2025CSACTF babysteg的剩余部分（见附件）。
### LSB
1. BUUCTF LSB https://buuoj.cn/challenges#LSB
### gif
1. BUUCTF 鸡你太美 https://buuoj.cn/challenges#[BJDCTF2020]%E9%B8%A1%E4%BD%A0%E5%A4%AA%E7%BE%8E

### 音频

1. 帮哥哥降噪 From白延胜
