学习Linux的使用
https://github.com/team-s2/ctf_summer_courses/blob/2022/homework/trivial/01_linux_hw.pdf
https://slides.tonycrane.cc/PracticalSkillsTutorial/2023-spring-cs/lec1/#/

# 编码相关
（晚上会讲，大概列一下）
ASCII码，Latin-1
Unicode，UTF-8
GB 2312 / GBK / GB 18030-2022
base家族编码尤其是base64

# 下载工具：

## Hex编辑工具
010editor或者winhex

推荐010editor，它可以自动的给出一些数据块的区分(之前用winhex才发现吃的是什么苦hhh)
![[Pasted image 20251219230417.png]]
## 查看文件信息

exiftool
binwalk

## 压缩包工具：
7z，winrar(解压缩查看信息，一个也许够了？)
ARCHPR(windows暴力，明文，掩码，字典破解几乎都有，很建议下)

fcrackzip:linux命令行的字典破解工具（应该archpr也可以替代它）
```
apt install fcrackzip
fcrackzip -u -D -p [wordlist] [ZIP file]
```


## 图片隐写工具：
1.zsteg（很建议下）(如果虚拟机内clone有网络问题也可以本地git clone后再移进去)
https://blog.csdn.net/Aluxian_/article/details/142085162
```
git clone https://github.com/zed-0xff/zsteg
cd zsteg/
gem install zsteg
```
2.stegsolve下载（很建议下）
这个需要有java环境。因为我是mac没在windows下这个，大家可以参考文章下载（）
https://blog.csdn.net/wzk4869/article/details/132635923

3.F5隐写工具
要下载java8，高版本的比如java11会报错。
```
git clone https://github.com/matthewgao/F5-steganography
docker build -t f5_tool .
#要有java环境
apt-get install openjdk-8-jdk -y
```


### 二维码


## 取证分析
### 哈希相关工具
你可能要下载 john ripper（linux）或者hashcat（linux），破解hash相关
你可能还需要下载SecList https://github.com/danielmiessler/SecLists 超全开源字典集合（有2个多G好像）
## 流量分析

## pacp文件
自行下载**wireshark**（因为我是mac版的，所以不放附件了大家自己去官网下x）
https://www.wireshark.org/

pacp文件是网络中流动的数据包，包括包内数据以及相关协议等
## 协议分析
可以了解一些基础知识 https://www.runoob.com/np/np-tutorial.html
### http/https
https://www.runoob.com/http/http-intro.html
### WIFI
（不一定讲到）
了解一下无线网络的小知识 https://blog.csdn.net/wit_732/article/details/103772676
工具：aircrack-ng套件



DNS，Domain Name System
```

```

### DDCTF2018流量分析
我们查看是rsa
![[Pasted image 20251212201047.png]]
TCP stream follow
![[Pasted image 20251212202140.png]]

