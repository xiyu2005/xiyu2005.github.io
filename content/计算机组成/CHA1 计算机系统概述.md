---
draft: true
---

## 计算机体系概述
一、计算机系统概述 
1. 什么是计算机系统 
定义：计算机系统由**硬件**和**软件**两大部分组成
硬件特性：计算机的实体部分，看得见摸得着（如主机、鼠标、键盘、显示器），是计算机系统的物理基础，决定了系统的性能天花板
软件特性：看得见但摸不着（如操作系统、微信、微博），决定了硬件性能的发挥程度
系统评价：需要同时考察硬件功能和软件功能（举例：苹果手机硬件可能不如安卓，但结合软件生态整体体验更好）
1）软件进一步划分 
系统软件：
功能：管理整个计算机系统
典型代表：操作系统、数据库管理系统(DBMS)、标准程序库、网络软件、语言处理程序（编译/汇编程序）、服务程序（如调试程序）
应用软件：
功能：按任务需求编制的各种程序
典型代表：微信、QQ等日常应用程序
课程重点：本课程主要探讨硬件部分
2. 硬件的发展 
1）第一台电子数字计算机 
**名称：ENIAC（1946年）**
2）第一代电子管时代 
主要问题：体积大、耗电高、速度慢、可靠性低
3）第二代晶体管时代 1958-1964
技术突破：贝尔实验室发明晶体管替代电子管
改进：体积大幅缩小（从房间大小降至厕所大小），功耗降低
速度提升至每秒几十万次运算
软件发展：出现高级语言（如Fortran）和操作系统
制造问题：需手工焊接几十万个晶体管，可靠性仍不高
4）第三代中小规模集成电路时代 1964-1971
技术突破：集成电路工艺
改进：体积更小，功耗更低，可靠性显著提高
5）第四代大规模、超大规模集成电路时代 1972-现在

技术突破：微处理器出现（如CPU）
制造工艺达纳米级（例：苹果A13芯片7nm工艺，集成85亿个晶体管）
应用普及：微型计算机进入个人生活
操作系统：Windows、MacOS、Linux等普及
存储发展：半导体存储器容量按摩尔定律增长

6）微处理器的发展 
代表企业：英特尔
关键参数：
机器字长：CPU一次整数运算能处理的二进制位数
发展规律：从8位(8080)逐步发展到64位(Pentium系列)
性能影响：字长增加直接提升运算速度（如16位CPU处理16位加法只需1次运算）

7）晶体管的发明 
发明者：1947年贝尔实验室三人组（含肖克利）
创业历程：
1955年肖克利创立公司
1957年"八叛徒"创立仙童半导体公司
1959年仙童发明集成电路
1968年摩尔等人创立Intel
1969年桑德斯创立AMD
产业影响：仙童公司孕育了多家半导体巨头
8）摩尔定律 

提出者：戈登·摩尔（Intel创始人之一）
内容：
集成电路可容纳晶体管数量约每18个月翻倍
性能同步提升一倍
例：2000元CPU在18个月后同价位性能翻倍
适用范围：不仅适用于处理器，也适用于存储器发展
现状：半导体存储器容量也遵循类似发展规律
3. 软件的发展 

机器语言阶段：计算机发展初期使用二进制代码编写程序，可读性极差
汇编语言改进：将机器指令转换为人类易记的符号，本质仍与机器语言相同（后续小节会详细讲解）
早期编程困境：程序员需同时关注问题解决和机器特性，导致软件开发困难且数量有限

高级语言革命：
代表语言：FORTRAN、Pascal、C++等
核心优势：接近自然语言，程序员可专注问题本身而无需考虑机器特性
发展影响：直接推动软件世界的丰富化
网络时代语言：Java等专为网络环境设计的语言出现
操作系统演进：
早期：DOS等命令行操作系统
现代：Windows图形界面、Android/iOS等移动系统

4. 目前的发展趋势 

微型化方向：
特点：更微型化、网络化、高性能、多用途
实例：智能穿戴设备、智能手机持续小型化但功能增强
巨型化方向：
特点：更巨型化、超高速、并行处理、智能化
代表机型：
神威·太湖之光：峰值性能达每秒次浮点运算
天河二号：世界排名第四的超级计算机

5. 知识回顾与重要考点 

系统构成：计算机系统=硬件+软件
硬件代际特征：
第一代：电子管（高耗电、大体积）
第二代：晶体管（体积缩小、更省电）
第三代：中小规模集成电路（高密度集成元器件）
第四代：大规模/超大规模集成电路（工艺提升）
考察重点：
硬件代际更替（选择题高频考点）
各代核心逻辑元件特征对比
发展趋势：
微型化与巨型化两极并行发展
软件发展非课程重点，仅作了解性内容

## 计算机硬件的基本组成
### 一、计算机硬件的基本组成 

核心概念：计算机系统由硬件和软件组成，本节重点探讨硬件部分的基本结构组成。
### 早期冯诺依曼机 
1）冯·诺依曼 

历史背景：冯·诺依曼作为ENIAC计算机顾问，发现其需要手动接线控制计算的缺陷

**存储程序**概念：
定义：将指令以**二进制代码**形式预先存入主存储器，计算机**按顺序自动执行**
实现方式：通过EDVAC计算机首次实现（Electronic Discrete Variable Automatic Computer）
2）冯·诺依曼机的特点 

五大部件：
输入设备（转换为机器可识别形式）
输出设备（转换为人可理解形式）
存储器（存放数据和程序）
运算器（算术/逻辑运算）
控制器（指令解析与协调）

![[Pasted image 20250917204016.png]]
核心特征：
**二进制表示**：指令和数据均用二进制存储
**指令结构**：由操作码（操作类型）和地址码（数据位置）组成
**存储程序**：提前存储指令序列实现自动化执行
**运算器中心**：所有数据传输必须经过运算器中转

效率问题：类比加工厂案例说明运算器作为数据中转站导致的效率瓶颈

### 现代计算机的结构 
![[Pasted image 20250917204221.png]]
架构革新：
中心转移：从运算器为中心改为存储器为中心
直接存取：输入输出设备直接与存储器交换数据
集成发展：运算器与控制器集成形成CPU芯片

部件关系：
CPU组成：包含运算器（ALU）和控制器（CU）
主机定义：CPU+主存储器（注意与日常"主机"概念区别）

存储分级：
主存（内存）：直接与CPU交互
辅存（硬盘）：归类为I/O设备

1）知识回顾与重要考点 
关键对比：
冯诺依曼结构：五大部件、运算器中心、存储程序
现代结构：存储器中心、CPU集成、直接数据通路
易混淆概念：
主存vs辅存：内存（8GB）属于主机，硬盘（128GB）属于I/O设备
主机范围：仅包含CPU和主存，不含外设
技术演进：
存储程序概念的首次提出者：冯·诺依曼
现代计算机效率提升的关键：解除运算器的数据传输负担

## 各个硬件工作原理


﻿

##### 1. 知识总览

- ![](https://bdcm01.baidupcs.com/file/p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-1?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758114113&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-Z3LJsC8pSuwJm%2BVcz3K9PndnQiE%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-dfab66d66ed00861dd1c98c22c37c42e17e68c4d08ebd196466f08782f190e5e598f2bbd9cd8612805c1cd5195bcccd8a0af99ac2d857216305a5e1275657320&expires=8h&r=268569609&vbdid=-&fin=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-1&fn=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-1&rtype=1&dp-logid=262657864532924413&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=24f48e7bb37b52f0f0530e1807cf4ae84b730b02c0acbdaf&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 五大部件：基于冯诺依曼结构的计算机包含运算器、输入设备、主存储器、控制器、输出设备五个核心硬件部件
- 学习重点：本节主要探讨主机内部的主存储器、运算器、控制器三个部件的内部细节及协作机制

##### 2. 主存储器的基本组成

###### 1）存储体的构成与作用
- ![](https://bdcm01.baidupcs.com/file/p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-2?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758114113&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-K%2BpCiUUO2k7LdbqBkaoXgAnUteU%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-50bc39f703c0bd22925ebe7ca79d2e90f432861a79774bc0e6d495488ace82316239bdd0c3622134ea1a7c562f34f29fc25dd701208ccfad305a5e1275657320&expires=8h&r=430866884&vbdid=-&fin=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-2&fn=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-2&rtype=1&dp-logid=262657864532924413&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=c77a2290e27174be3d66e1a7460e33c3f5f52312eaafc1fe305a5e1275657320&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 核心组件：由存储体、MAR（存储地址寄存器）、MDR（存储数据寄存器）三部分组成
- 存储体功能：由存储元件构成，用于存放二进制数据（0/1），类比菜鸟驿站的货架存放包裹
- 寄存器说明：MAR存放地址信息（如"11号货架第一层第42个包裹"），MDR暂存读写数据（如"柜台上待取的包裹"）

###### 2）存储单元与地址管理

- ![](https://bdcm01.baidupcs.com/file/p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-3?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758114113&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-p4EZT2ZOhj5fYdlVMd%2BPGgwEsVQ%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-9206fe5d8f09fe6559b45dc836c507c816a4ddd8e779988a4d0d0d34d9285f55ccdb3c6a097966d4fb83a91e5a2493827670067943e0c456305a5e1275657320&expires=8h&r=597928207&vbdid=-&fin=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-3&fn=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-3&rtype=1&dp-logid=262657864532924413&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=5eee304bbb22b9c2b94d4c3788c069c565d1c5b081ac0b2fc48031c257b32a4e&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 存储单元划分：存储体被划分为若干存储单元，每个单元存放一个存储字（word）
- 地址编码：每个存储单元有唯一地址（从0开始编号），地址信息存放于MAR
- 存储字长：每个存储单元存放的二进制位数（常见为8/16/32/64比特的整数倍）

###### 3）存储元件原理

﻿

06:56

﻿

- 物理实现：使用电容原理制造存储元件，单个电容存储1比特（利用电荷存储特性）
- 单元构成：多个存储元件组合形成存储单元，具体电路设计不需深究

###### 4）寄存器位数关系

﻿
﻿

- MAR位数：决定存储单元数量（n位MAR可寻址$2^n$个单元）
- MDR位数：等于存储字长（如16位MDR对应16比特/字的存储单元）
- 示例说明：4位MAR对应16个存储单元（$2^4$），16位MDR表示每个单元存放16bit数据

###### 5）计量单位辨析

- 字(word)：存储单元容量单位，长度可变（16/32/64比特等）
- 字节(Byte)：固定8比特，用大写B表示（如1MB=8Mb）
- 比特(bit)：最小单位，用小写b表示（宽带100Mb/s=12.5MB/s下载速度）
- 易混淆点：注意广告中"100M宽带"实际指100Mbps（兆比特每秒），需除以8换算为字节单位

##### 3. 运算器的基本组成

- ![](https://bdcm01.baidupcs.com/file/p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-4?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758114113&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-SzgG5mlaws6H7ouyDSiLjzV866M%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-87b444c7d85695f45652f9759a2fcf22bf102734918b110825b3130d50500e6aaab952a416594d9e85060f1f903409e5ac1ee53766b420de305a5e1275657320&expires=8h&r=498766388&vbdid=-&fin=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-4&fn=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-4&rtype=1&dp-logid=262657864532924413&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=7717645f262844ca5d56a4409b209f554b730b02c0acbdaf&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 核心部件：ALU（算术逻辑单元），通过内部复杂电路实现算术运算和逻辑运算，是运算器中制造成本最高的部件
- 寄存器组：
    - ACC（累加器）：存放操作数或运算结果，在加减乘除运算中分别存储被加数/和、被减数/差、乘积高位、被除数/余数
    - MQ（乘商寄存器）：专用于乘除运算，存放乘数/乘积低位或商
    - X（通用寄存器）：可存放任意操作数，运算器可能包含多个此类寄存器
- 运算类型：
    - 算术运算：加减乘除
    - 逻辑运算：与或非等
- 硬件特点：寄存器构造简单，ALU构造复杂

##### 4. 控制器的基本组成

﻿

﻿

- ![](https://bdcm01.baidupcs.com/file/p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-5?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758114113&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-lTMQDvf3lt6mrAwAUWTWeCJfcNE%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-7ebc0ca9555c1e7e4cf9705786b35fedec1ba5ab247db559f69a3ddf3da8f976a40242469ce5bb3e71ae4f02039d41f75f55e271269a28c5305a5e1275657320&expires=8h&r=462851509&vbdid=-&fin=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-5&fn=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-5&rtype=1&dp-logid=262657864532924413&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=a5f92b9aebde11e5b44eeb1a4e4f7f1e118eebb7d9152704&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 核心部件：
    - CU（控制单元）：分析指令并发出控制信号，是控制器的核心部件
    - IR（指令寄存器）：存放当前正在执行的指令
    - PC（程序计数器）：存放下一条指令地址，具有自动加1功能
- 指令执行流程：
    - 取指令阶段：根据PC地址从内存取出指令
    - 分析阶段：指令存入IR，CU分析指令内容
    - 执行阶段：CU控制各部件完成指令操作
- 阶段划分：
    - 取指阶段（包含前两个阶段）
    - 执行阶段（最后一个阶段）
- 注意点：PC（Program Counter）与个人电脑的PC概念不同

##### 5. 计算机的工作过程

﻿

15:54

﻿

###### 1）例题：C语言程序编译执行过程

﻿

- 高级语言与机器指令差异：高级语言中看似简单的复合运算（如y=a×b+c﻿）会被CPU分解为多个基本操作步骤（先乘法后加法）
- 编译过程：通过编译链接将高级语言转换为机器语言，生成多条机器指令（如示例中1行C代码转换为5条机器指令）
- 存储结构：
    - 指令存储在0-4号存储单元
    - 变量a、b、c、y分别存储在5-8号存储单元
    - 每个存储单元为16位（2字节）
    - ![](https://bdcm01.baidupcs.com/file/p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-6?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758114113&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-E0c5GtWDl%2FJqJTq%2B0u18nc6HnWs%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-01b21e05eba91672c3c281289608fd94bc7fa908ee943ca0a6c88482d6798218437f50c866c4d2e1ac81d22fcdfa8bdf07c99ea4c9ef114d305a5e1275657320&expires=8h&r=508824621&vbdid=-&fin=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-6&fn=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-6&rtype=1&dp-logid=262657864532924413&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=3612dd02eb4608ab429372593084af8c118eebb7d9152704&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 指令格式：
    - 操作码（前6位）：指明操作类型（如000001表示取数）
    - 地址码（后10位）：指明操作数地址
- 数据存储：
    - 变量a=2（二进制0000000000000010）
    - 变量b=3（二进制0000000000000011）
    - 变量c=1（二进制0000000000000001）
    - 变量y初始为0

###### 2）指令执行过程详解

- ![](https://bdcm01.baidupcs.com/file/p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-7?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758114114&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-XCU4xGKX3PaU%2BHcaUb1o99Q66sI%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-ec9be9b9d336b792698534009ed3777b01f3a416065c753e2bd3344603ad078723ab5385b9cbc9375a2d7a5eb07b8cb82cac5db8180d28f7305a5e1275657320&expires=8h&r=790703571&vbdid=-&fin=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-7&fn=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-7&rtype=1&dp-logid=262657864532924413&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=3612dd02eb4608ab372d39155f1155bc118eebb7d9152704&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 取数指令执行流程：
    - ﻿(PC)→MAR(PC)→MAR(PC)→MAR﻿
        
        ：将程序计数器内容送地址寄存器（MAR=0）
    - ﻿M(MAR)→MDRM(MAR)→MDRM(MAR)→MDR﻿
        
        ：从主存读取指令到数据寄存器（MDR=000001 0000000101）
    - ﻿(MDR)→IR(MDR)→IR(MDR)→IR﻿
        
        ：指令送指令寄存器
    - ﻿(PC)+1→PC(PC)+1→PC(PC)+1→PC﻿
        
        ：程序计数器自动加1（PC=1）
    - ﻿OP(IR)→CUOP(IR)→CUOP(IR)→CU﻿
        
        ：操作码送控制单元分析（识别为取数指令）
    - ﻿Ad(IR)→MARAd(IR)→MARAd(IR)→MAR﻿
        
        ：地址码送地址寄存器（MAR=5）
    - ﻿M(MAR)→MDRM(MAR)→MDRM(MAR)→MDR﻿
        
        ：读取变量a的值（MDR=2）
    - ﻿(MDR)→ACC(MDR)→ACC(MDR)→ACC﻿
        
        ：数据送累加寄存器（ACC=2）
- 乘法指令执行流程：
    - 取指令阶段与取数指令相同（PC=1→MAR=1）
    - 控制单元识别为乘法指令（操作码000100）
    - 将被乘数a从ACC传送到通用寄存器X
    - 将乘数b从主存读取到MQ寄存器（b=3）
    - ALU执行乘法运算（2×3=6），结果存回ACC
- 加法指令执行流程：
    - 取指令阶段相同（PC=2→MAR=2）
    - 控制单元识别为加法指令（操作码000011）
    - 将加数c从主存读取到通用寄存器X（c=1）
    - ALU执行加法运算（6+1=7），结果存回ACC
- 存数指令执行流程：
    - 取指令阶段相同（PC=3→MAR=3）
    - 控制单元识别为存数指令（操作码000010）
    - 将ACC的值（7）通过MDR存入主存8号单元（y=7）
- 停机指令执行：
    - 控制单元识别操作码000110为停机指令
    - 通过中断机制通知操作系统终止进程

###### 3）指令执行周期总结

- ![](https://bdcm01.baidupcs.com/file/p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-8?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758114114&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-ya%2BKGcWJRc64h7rChWWwgjsapkw%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-6d25545cab3c1cb2c1b7995363c61ffec50018fd5b87d84bd219d7ecdcb0b4a7731d222e7996c80fe82ef64dcf85885c1be9239b4aad4097305a5e1275657320&expires=8h&r=632478585&vbdid=-&fin=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-8&fn=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-8&rtype=1&dp-logid=262657864532924413&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=12146e4ffd7df3c9bc45b0a93630176549adfc417011a289305a5e1275657320&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 三阶段模型：
    - 取指阶段：完成指令读取（步骤1-4）
    - 分析阶段：操作码译码（步骤5）
    - 执行阶段：执行具体操作（步骤6-9）
- 关键特点：
    - 前两个阶段对所有指令相同
    - 执行阶段因指令类型而异
    - PC在取指后自动加1
    - CPU通过执行阶段区分指令和数据
- 寄存器作用：
    - MAR：存储要访问的内存地址
    - MDR：暂存从内存读取或要写入的数据
    - IR：存储当前执行的指令
    - ACC：存储算术运算结果
    - MQ：辅助存储乘法结果（低位部分）

##### 6. 知识回顾与重要考点

###### 1）存储体相关概念

- 存储元: 存储二进制信息的最小单位，对应一个二进制位
- 存储单元: 由若干存储元组成，是CPU访问存储器的基本单位
- 存储字: 存储单元中存放的二进制代码组合
- 存储字长: 存储单元中二进制代码的位数
- 地址: 用于标识存储单元的位置编号

###### 2）计算机主要部件功能

- ![](https://bdcm01.baidupcs.com/file/p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-9?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758114114&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-JuL5cj%2FgjLg4Rarvugcx1gjurk4%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-c6e027c1039fc97c1ab3d67f2666a4bf898dcabffdae0ad6fd26b7b7ffb75e9cdd1b439076e14f0bec7df03ad232b9af66803eabc2fd8dab305a5e1275657320&expires=8h&r=711242929&vbdid=-&fin=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-9&fn=p-335ca414e830d4cf3fe4cef8c2ca2987-40-2025042100-9&rtype=1&dp-logid=262657864532924413&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=12146e4ffd7df3c926c82c2210ab4224ca2f99807f3f1ae5&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- MAR(地址寄存器): 用于指明要读/写哪个存储单元，其位数反映存储单元数量
- MDR(数据寄存器): 暂存要读/写的数据，位数等于存储字长
- ACC(累加计数器): 存放操作数和运算结果
- MQ(乘商寄存器): 专门用于乘除法运算
- 通用寄存器: 存放操作数
- ALU(算术逻辑单元): 用电路实现各种算术运算和逻辑运算，是运算器核心部件
- PC(程序计数器): 存放下一条指令的地址
- IR(指令寄存器): 存放当前执行的指令
- CU(控制单元): 分析指令并给出控制信号，是控制器核心部件
- 注意点:
    - 字和字节的区别需要特别注意
    - 大B(Byte)和小b(bit)的区别是重要考点
    - 现代计算机中MAR和MDR通常集成在CPU内部

###### 3）计算机工作过程

- 初始阶段: 指令和数据存入主存，PC指向第一条指令地址
- 执行过程:
    - 从主存取指令放入IR
    - PC自动加1指向下一条指令
    - CU分析指令操作码
    - CU指挥各部件执行指令

##### 7. 回顾冯诺依曼机的特点

﻿

36:07

﻿

- 五大部件组成: 计算机由运算器、控制器、存储器、输入设备和输出设备组成
- 指令数据同等存储: 指令和数据以同等地位存入存储器，可按地址寻访
- 二进制表示: 指令和数据都用二进制表示
- 指令结构: 指令由操作码和地址码组成(可能有单地址、双地址等不同格式)
- 存储程序: 程序运行前指令和数据都预先存入主存
- 运算器中心: 原始设计以运算器为中心，现代计算机多以存储器为中心
- 理解要点:
    - 指令和数据在存储器中无差别存储，只是存放位置不同
    - 按地址寻访意味着无论读取指令还是数据都需要给出内存地址
    - 存储程序概念强调程序执行前必须完整存入主存

#### 二、小结

| 知识点    | 核心内容                                  | 考试重点/易混淆点                           | 难度系数  |
| ------ | ------------------------------------- | ----------------------------------- | ----- |
| 冯诺依曼结构 | 现代计算机五大硬件部件设计基础                       | 五大部件的具体组成与协作关系                      | ⭐⭐    |
| 主存储器组成 | 存储体+MAR(地址寄存器)+MDR(数据寄存器)             | MAR位数决定存储单元数量，MDR位数=存储字长            | ⭐⭐⭐   |
| 存储单元概念 | 按地址存储二进制数据，包含存储字(word)                | 字长可变(8/16/32/64比特) vs 固定字节(8比特)     | ⭐⭐    |
| 寄存器功能  | MAR存地址/MDR存数据/ACC存运算数/IR存指令/PC存下条指令地址 | PC自动加1机制，IR与MDR的数据流向区别              | ⭐⭐⭐⭐  |
| 运算器结构  | ALU(核心)+ACC(累加器)+MQ(乘商寄存器)+X(通用寄存器)   | 乘法运算时ACC→X，MQ存乘数的数据流转               | ⭐⭐⭐⭐  |
| 控制器原理  | CU(指令分析)+IR(当前指令)+PC(程序计数器)           | 取指-分析-执行三阶段，CU产生的控制信号类型             | ⭐⭐⭐⭐  |
| 指令执行流程 | 以"y=a×b+c"为例演示取数/乘法/加法/存数/停机指令        | 操作码译码过程，不同指令的数据路径差异                 | ⭐⭐⭐⭐⭐ |
| 数据单位辨析 | 字(word)：与硬件相关 vs 字节(Byte)：固定8比特       | 大B(Byte)/小b(bit)：宽带100Mb/s=12.5MB/s | ⭐⭐    |
| 存储程序原理 | 指令与数据同等地位存储，按地址寻访                     | 指令=操作码+地址码(可能多地址)                   | ⭐⭐⭐   |
| 硬件成本对比 | ALU/CU制造成本最高，寄存器成本较低                  | 现代计算机将MAR/MDR集成到CPU                 | ⭐⭐    |

#### 一、计算机软件

##### 1. 软件分类
###### 1）应用软件

- ![](https://bdcm01.baidupcs.com/file/p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-1?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758115649&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-SvIR9j71zVrG5LCPn6ByRIAKXJo%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-1a84e138907c5c62d206bf29194949c37874aabe818360dc5505e2333ddddc587db2943562c3fbb08e40312cfdfd18df932ae085e5681ee7305a5e1275657320&expires=8h&r=668520889&vbdid=-&fin=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-1&fn=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-1&rtype=1&dp-logid=263070129300507750&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=24f48e7bb37b52f09d8727ac1dae56f0f302d47d758eedf1&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 定义: 为解决特定应用领域问题而编制的程序
- 特点:
    - 直接面向终端用户提供服务
    - 每种软件针对特定需求开发
- 典型示例:
    - 大众软件：抖音（短视频）、QQ（社交）、美图秀秀（图片处理）
    - 专业软件：Photoshop（图像设计）、AutoCAD（工程制图）
###### 2）系统软件
- ![](https://bdcm01.baidupcs.com/file/p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-2?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758115649&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-HoK6cENsCu9VmCyRxlrHndggc24%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-a585e76903a4f0026ce1c444dc71b30c18dff0803f40dd78979b318ee3a8c714dedecc19e1567418b685e1743ecf1821b482e9e23ea51a2b305a5e1275657320&expires=8h&r=736764205&vbdid=-&fin=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-2&fn=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-2&rtype=1&dp-logid=263070129300507750&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=66239664855e8068230408e99c62dfffd08206a3057820e6305a5e1275657320&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 核心功能:
    - 管理底层硬件资源
    - 为上层应用软件提供基础服务
- 主要类型:
    - 操作系统（如Android/iOS）：支撑所有应用运行
    - 数据库管理系统（DBMS）：提供数据存储服务
    - 网络软件（如网卡驱动）：实现网络通信
    - 语言处理程序：完成代码翻译
    - 服务程序（如调试工具）：辅助开发
    - 标准程序库（如printf）：提供通用功能
- 类比: 相当于软件世界的"基础设施"

##### 2. 三种级别的语言


- ![](https://bdcm01.baidupcs.com/file/p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-3?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758115649&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-MxxKkCnt4Vhwr9clxHFYUtMA8bE%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-9603bb96b0b9f0ede076eee9dff9645685f6fe22582348ea0955655a5128acfd983f15385f41f9cecc39eaa6875f60c7d13e04597d222698305a5e1275657320&expires=8h&r=296621972&vbdid=-&fin=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-3&fn=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-3&rtype=1&dp-logid=263070129300507750&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=24f48e7bb37b52f0f0530e1807cf4ae8f302d47d758eedf1&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 高级语言:
    - 人类友好型：C/C++、Java、Python等
    - 特点：使用自然语言结构和数学表达式（如y=a∗b+c﻿）
- 汇编语言:
    - 低级语言：使用助记符（如LOAD、MUL）
    - 特点：比机器语言更易理解
- 机器语言:
    - 最底层：二进制代码（如00000100000001010101）
    - 特点：计算机硬件直接识别

###### 1）编译型语言
- 处理流程:
    - 编译器：将高级语言整体翻译为汇编语言或机器语言
    - 汇编器：将汇编语言转换为机器语言
- 执行特点:
    - 一次性翻译生成可执行文件（如.exe）
    - 类比：纸质文档的批量翻译
- 优势:
    - 执行效率高（重复代码只需翻译一次）
###### 2）解释型语言
- 处理流程:
    - 解释程序：逐行翻译并立即执行
- 执行特点:
    - 翻译与执行交替进行
    - 类比：同声传译
- 劣势:
    - 效率较低（重复代码需多次翻译）
- 典型语言:
    - Java、Shell脚本等

##### 3. 软件和硬件的逻辑功能等价性﻿

- ![](https://bdcm01.baidupcs.com/file/p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-4?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758115649&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-4AZGYr1mL%2FhzJQ%2Bsxxd32%2F0rIbU%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-22f267a52c80831b352f6c9629f0137d7712a3b5439b2c43beb07f4ccc291dd3f089c6a3405a11dde079abf689d985993365ae174500e892305a5e1275657320&expires=8h&r=954216634&vbdid=-&fin=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-4&fn=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-4&rtype=1&dp-logid=263070129300507750&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=6a9088c7620f7a1736564e37f877fcb0f302d47d758eedf1&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 核心概念:
    - 同一功能既可用硬件实现也可用软件实现
- 实现对比:
    - 硬件实现（如乘法电路）：
        - 性能高但成本高
        - 示例：直接使用MUL指令计算
            ﻿985×6985
    - 软件实现（如加法循环）：
        - 性能低但成本低
        - 示例：用6次ADD指令实现
            
            ﻿985+985+...985+985+...985+985+...﻿
            

###### 1）指令集体系结构

- ![](https://bdcm01.baidupcs.com/file/p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-5?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758115649&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-jFtM33bUjTUxlIWlxtbLtaFxFgw%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-d49971ad201c17e120d4774b901d9207906b7d860d812c730753bdf712dafeb8f0dc5ab5a565a291e1d64111b6143d233c60291db5950b5b305a5e1275657320&expires=8h&r=113654937&vbdid=-&fin=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-5&fn=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-5&rtype=1&dp-logid=263070129300507750&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=c77a2290e27174be3d66e1a7460e33c3d08206a3057820e6305a5e1275657320&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 定义（Instruction Set Architecture）:
    - 规定软件与硬件的交互界面
- 设计内容:
    - 支持的指令类型（如ADD/MUL）
    - 每条指令的功能定义
    - 指令的使用规范
- 设计考量:
    - 性能与成本的平衡
    - 明确划分软硬件边界

##### 4. 知识回顾与重要考点
- ![](https://bdcm01.baidupcs.com/file/p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-6?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758115649&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-xVVWIQ8%2F5KhTNkOxcRSdUIPnp74%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-a4858cf34ff9d5ce7273a4547399c6a457202f1b6db7f6cc91ae74c71007d2a04597d0a1e1b1e715b21ff8c2a512b76ac8ceada8a2844a94305a5e1275657320&expires=8h&r=257896017&vbdid=-&fin=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-6&fn=p-f606034f55d08e6dfa2329c4b870e7d1-40-2025042100-6&rtype=1&dp-logid=263070129300507750&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=5eee304bbb22b9c2b6e12d2bd14114dd9c36f93ed53dc6fda6c2ad6eeb587c84&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 系统要点:
    - 管理硬件资源并提供基础服务
- 应用要点:
    - 直接面向用户的专用程序
- 语言要点:
    - 高级→汇编→机器语言的层级关系
    - 编译器/汇编器/解释器的区别
- 等价性要点:
    - 硬件实现（高性能高成本）
    - 软件实现（低成本低性能）
- ISA要点:
    - 定义计算机支持的指令集
    - 规定软硬件交互规范

#### 二、知识小结

| 知识点          | 核心内容                                                    | 考试重点/易混淆点                | 难度系数 |
| ------------ | ------------------------------------------------------- | ------------------------ | ---- |
| 计算机软件分类      | 分为系统软件（管理硬件资源，如操作系统、数据库管理系统）和应用软件（直接服务用户，如抖音、Photoshop） | 区分系统软件与应用软件的功能差异         | ⭐⭐   |
| 高级语言与低级语言    | 高级语言（C/C++、Java）、汇编语言（助记符）、机器语言（二进制）                    | 理解三种语言的转换过程（编译→汇编→机器语言）  | ⭐⭐⭐  |
| 翻译程序类型       | 编译器（一次性翻译）、解释器（逐句翻译）、汇编器（汇编→机器语言）                       | 编译型与解释型语言效率对比（编译型效率更高）   | ⭐⭐⭐⭐ |
| 软硬件逻辑等价性     | 同一功能可通过硬件（专用电路）或软件（指令组合）实现，硬件性能高但成本高                    | 指令集体系结构（ISA）的作用（定义软硬件界限） | ⭐⭐⭐  |
| 指令集体系结构（ISA） | 规定计算机支持的指令及其作用、用法，平衡性能与成本                               | 设计计算机系统时需明确ISA的指令范围      | ⭐⭐⭐⭐ |


#### 一、计算机系统的多级层次结构
##### 1. 传统机器
- ![](https://bdcm01.baidupcs.com/file/p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-1?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116192&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-ysJEbUZfOwLVVf9NZacDoSkCh6o%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-d4db4c97a99ef45aeea7dacadb1ce8fae509c4d683c43903fe47bcf23532fbf1bfceff95edf91bd2fc4921b4b309eec0c92700c7177b8a46305a5e1275657320&expires=8h&r=714981996&vbdid=-&fin=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-1&fn=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-1&rtype=1&dp-logid=263215929992335336&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=66239664855e8068230408e99c62dfff9df97e73009b5b54305a5e1275657320&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 执行原理：传统机器M1只能识别二进制机器指令，每条指令需要分解为多个微指令执行。例如取数指令"0000010000000101"需要分解为9个微操作步骤：
    - ﻿(PC)→MAR(PC)→MAR(PC)→MAR﻿
        
        （将程序计数器值送入内存地址寄存器）
    - ﻿M(MAR)→MDRM(MAR)→MDRM(MAR)→MDR﻿
        
        （从内存读取数据到内存数据寄存器）
    - ﻿(MDR)→IR(MDR)→IR(MDR)→IR﻿
        
        （将指令送入指令寄存器）
    - 操作码分析
    - 地址码传送等步骤
- 存储结构示例：
- ![](https://bdcm01.baidupcs.com/file/p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-2?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116192&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-o8FGIDHuYSCoMFOD%2BJLjCY%2BAOu4%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-a8c7632a21375835d6bc156b92597e955d8eaa1dfd41941c5848fd5a424c2ad31c4fdbabe5528d03edaf5958a6e52378cce0aaeb71c17332305a5e1275657320&expires=8h&r=382289033&vbdid=-&fin=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-2&fn=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-2&rtype=1&dp-logid=263215929992335336&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=24f48e7bb37b52f0f0530e1807cf4ae8687cf7818c51c640&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 微指令系统：微程序机器M0是传统机器M1的下层基础，由硬件直接执行微指令（如微指令1、3、7等），用于解释和执行上层机器指令。

##### 2. 虚拟机器
- ![](https://bdcm01.baidupcs.com/file/p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-3?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116192&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-Bh8w7zhXTsEDo9InWnGZprwF3hQ%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-a20d3a72efddd3b03a4ae7babeafe8bbbd3fcb9877725171be3e9d44a7aeccb7a76cd83d564c6b484d9c8bcdfe0ce76c9e614d3dc18db1ac305a5e1275657320&expires=8h&r=754071708&vbdid=-&fin=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-3&fn=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-3&rtype=1&dp-logid=263215929992335336&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=6a9088c7620f7a1736564e37f877fcb0687cf7818c51c640&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 汇编语言机器M2：
    - 使用符号化指令（如LOAD 5）替代二进制指令
    - 每条汇编指令与机器指令一一对应，例如：
        - "LOAD 5" ↔ "0000010000000101"
        - "MUL 6" ↔ "0001000000000110"
    - 需要通过汇编程序翻译为机器语言
- 高级语言机器M4：
    - 如C/JAVA等高级语言编写的程序（示例：y=a∗b+c﻿）
    - 需要经过编译程序→汇编程序→机器语言的多级翻译
    - 程序员视角的"虚拟机器"实际不存在
- 操作系统机器M3：
    - 提供系统调用（广义指令）服务
    - 位于汇编语言机器与传统机器之间
    - 属于软件层与硬件层的分界

##### 3. 计算机系统的层次结构
- ![](https://bdcm01.baidupcs.com/file/p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-4?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116192&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-23buHMNFW20Ty2%2FXECi%2BQSqG4yw%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-d42965b17a9e97572d5e8da09243fda701fab56b8b76ea00fab682c17172d34fbaa316ae312193d90f4f41a3a875b3773c04fde09b652050305a5e1275657320&expires=8h&r=236530313&vbdid=-&fin=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-4&fn=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-4&rtype=1&dp-logid=263215929992335336&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=0cce998314b34a673f5b22d5a4a7dcee054a23aea6920806&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 层级关系：
    - 微程序机器M0（微指令系统）
    - 传统机器M1（机器语言）
    - 操作系统机器M3（系统调用）
    - 汇编语言机器M2
    - 高级语言机器M4
- 核心特点：
    - 下层是上层的基础，上层是下层的扩展
    - 硬件层（M0-M1）与软件层（M2-M4）通过操作系统分隔
    - 虚拟机器（M2-M4）的实际执行都需要翻译为下层指令
- 设计视角：该层次结构从编程人员（关注语言抽象）和硬件设计人员（关注指令执行）的视角划分，与操作系统课程的划分方式不同但都正确。

#### 二、知识回顾与重要考点
- ![](https://bdcm01.baidupcs.com/file/p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-5?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116192&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-cEGz75FIpIzHAbCPwi9NCNwr42I%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-9aa3b0e552bdbd9d70950db88345427db32de3cbf519ea1ecbde6e6550e602048e47f8b17c38a9cd98bfe505722ed7c8fdff65fcefc10bf2305a5e1275657320&expires=8h&r=273693587&vbdid=-&fin=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-5&fn=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-5&rtype=1&dp-logid=263215929992335336&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=c77a2290e27174be3d66e1a7460e33c39df97e73009b5b54305a5e1275657320&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 层次划分:
    - M4: 高级语言机器（执行高级语言）
    - M3: 汇编语言机器（执行汇编语言）
    - M2: 操作系统机器（向上提供广义指令）
    - M1: 传统机器（执行机器语言指令）
    - M0: 微程序机器（执行微指令）
- 执行本质：虽然高层机器能识别更高级的代码，但所有代码最终都需要翻译成机器语言执行
- 课程重点：计算机组成原理主要研究M1传统机器和M0微程序机器这两层的实现原理

#### 三、计算机体系结构与计算机组成原理的区别

- ![](https://bdcm01.baidupcs.com/file/p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-6?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116193&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-mrAGAuLQE9%2B5df4ywE0WAqECljI%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-f742e771c84f9296c0764d29a83d2e9dc0faeb52898c7ee822af6f3c4bce1c55c42d7db72a1e71fa7c7587fde5e9554b458b1e9e81009c61305a5e1275657320&expires=8h&r=498995436&vbdid=-&fin=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-6&fn=p-856290192b60b0e9da6d4cf7cb63912e-40-2025042100-6&rtype=1&dp-logid=263215929992335336&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=e83ff6a1394898305c92c18ca9f96aba687cf7818c51c640&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 体系结构定义：机器语言程序员可见的计算机系统属性，包括：
    - 指令系统设计（如有无乘法指令）
    - 数据类型支持
    - 寻址技术实现
    - I/O工作机制
- 组成原理定义：实现体系结构定义的接口，具体包括：
    - 硬件实现方案（如乘法指令的电路设计）
    - 对程序员透明（不可见）的实现细节
- 专业术语"透明"：在计算机专业中指"不可见"（与日常用语相反），类似《海贼王》中透明果实能力者的隐身特性
- 核心区别：
    - 体系结构解决"做什么"（接口设计）
    - 组成原理解决"怎么做"（硬件实现）

#### 四、知识小结


| 知识点                | 核心内容                                                            | 考试重点/易混淆点                                                   | 难度系数 |
| ------------------ | --------------------------------------------------------------- | ----------------------------------------------------------- | ---- |
| 计算机系统的多级层次结构       | 计算机系统分为五层：微程序机器、传统机器（实际机器）、操作系统机器、汇编语言机器、高级语言机器。每一层都是对下层的抽象和扩展。 | 传统机器与虚拟机器的区别：传统机器只能识别二进制指令，而虚拟机器（如汇编语言机器、高级语言机器）是通过翻译实现的假象。 | ⭐⭐⭐  |
| 机器语言与微指令           | 机器语言由二进制指令构成，CPU执行时需分解为微指令（微操作）。例如，一条取数指令可能被拆分为9个微指令执行。         | 微程序机器的作用：用微指令解释并执行传统机器的每一条机器指令。                             | ⭐⭐   |
| 汇编语言与机器语言的对应关系     | 汇编语言是符号化的机器语言，每条汇编指令对应一条机器指令。例如，取数操作LOAD 5对应二进制指令的操作码和地址码。      | 汇编语言的本质：仍是低级语言，需通过汇编程序翻译为机器语言。                              | ⭐⭐   |
| 高级语言的执行过程          | 高级语言代码需先编译为汇编语言，再汇编为机器语言。程序员视角的“虚拟机器”实际依赖多层翻译。                  | 高级语言与底层执行的关系：程序员无需关心底层实现，但最终仍需转换为机器语言。                      | ⭐⭐   |
| 操作系统机器的角色          | 位于汇编语言机器下层，提供系统调用（广义指令）服务。程序（包括汇编程序）需通过操作系统访问硬件资源。              | 操作系统与硬件的交互：属于软件层，但直接管理硬件资源。                                 | ⭐⭐⭐  |
| 计算机组成原理 vs 计算机体系结构 | 体系结构：定义指令系统等软硬件接口（如是否提供乘法指令）；组成原理：研究如何用硬件实现指令（如乘法指令的电路设计）。      | 透明性概念：计算机专业中“透明”指不可见（如硬件实现细节对程序员透明）。                        | ⭐⭐⭐⭐ |
#### 一、从C语言源程序到可执行文件

﻿

00:06

﻿

- ![](https://bdcm01.baidupcs.com/file/p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-1?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116444&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-FY7MluFPh5szQe0VNJ8On0qIZNQ%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-bbc2fc4050a697935030350eb945573bcefed2a9a86bcc59f7dad82665213b0220d53b2c492c7e74a47b5330df6b65715b1a193fba972b21305a5e1275657320&expires=8h&r=845110775&vbdid=-&fin=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-1&fn=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-1&rtype=1&dp-logid=263283662563838188&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=718800a01e5121ca67a4b8c3cb26e049f28ec273a6c7270c&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 源程序格式: C语言源程序以.c后缀结尾，如hello.c
- 转换目标: 将源程序转换为可执行文件（.exe文件）

##### 1. 预处理器

﻿

00:27

﻿

- ![](https://bdcm01.baidupcs.com/file/p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-2?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116444&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-dcFxn%2BEPwFR2mJZdYW0Lk%2BJBh8I%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-e544ef7d0ea48814d07ecd0f027149a50716b8540c4490551fcc03d98476ab080fafe2f5ec0db32a5e3957bed42f63083aa97add10145d15305a5e1275657320&expires=8h&r=256659355&vbdid=-&fin=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-2&fn=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-2&rtype=1&dp-logid=263283662563838188&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=7717645f262844ca5d56a4409b209f55f28ec273a6c7270c&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 处理对象: 对C语言中以#开头的命令进行处理
- 主要功能:
    - 宏定义常量的替换（如将﻿PI替换为﻿3.14159）
    - 提高代码可读性，但编译器需要还原为原始值
- 输出文件: 生成预处理后的源程序（.i文件）
##### 2. 编译器

- ![](https://xacm01.baidupcs.com/file/p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-3?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116445&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-U3iCOlVwT1lFOaLSxgBw2wSQIO4%3D&to=131&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CXian%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-7ad2c01272fd2314ed520726997291705f3375f4e845e04faf5f3b53034d11f6b6209bac9b64b09ee9f472c0f8cad7647a8dc66d0e67413a305a5e1275657320&expires=8h&r=863708040&vbdid=-&fin=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-3&fn=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-3&rtype=1&dp-logid=263283662563838188&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=718800a01e5121ca44342240fa99746f5cf4a7321e8c610b305a5e1275657320&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 转换过程: 将预处理后的源程序翻译为汇编语言程序
- 输出文件: 生成汇编语言程序（.s文件）

##### 3. 汇编器
- 转换过程: 将汇编语言程序翻译为机器语言程序
- 输出格式: 由0/1二进制组成
- 输出文件: 生成目标模块（.o文件）

##### 4. 链接器
- ![](https://bdcm01.baidupcs.com/file/p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-4?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116445&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-2Qvhrhr824y0%2BTcnHeQxXvLUnv0%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-9bdd5d02555ac73fdb6b69edcbb39aba64f989a0c935fa7f9afbff2ba7b42dd782109aa3abb8c9226b9efd9bb740e976f3713ec275f34e9b305a5e1275657320&expires=8h&r=539272875&vbdid=-&fin=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-4&fn=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-4&rtype=1&dp-logid=263283662563838188&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=718800a01e5121caae339351eea0af8ed8f7d94ecdec83a5&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 主要功能:
    - 将多个目标模块链接成统一的可执行文件
    - 处理标准库函数调用（如printf）
- 输出文件: 生成最终可执行文件（.exe文件）

#### 二、计算机系统的工作原理

- ![](https://bdcm01.baidupcs.com/file/p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-5?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116445&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-592caNx8nUgkvHMAmQxPlz9VnEk%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-ed32f95d10ce8c9024b82c844e5c535d149dae3bf7d4c5e0b0ad0f4537ec97869c3aedb8f6fd709b546ce9d825454b66d19a7202445f0964305a5e1275657320&expires=8h&r=680046374&vbdid=-&fin=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-5&fn=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-5&rtype=1&dp-logid=263283662563838188&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=3612dd02eb4608ab372d39155f1155bc0bad7d3b0738f6e5&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 文件存储位置: 可执行文件最初存储在外存（硬盘）中
- 程序运行过程:
    - 可执行文件从外存调入主存
    - CPU执行程序指令
- 输入输出设备:
    - 输入设备：鼠标、键盘等
    - 输出设备：显示器等

#### 三、存储程序工作方式

- ![](https://bdcm01.baidupcs.com/file/p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-6?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116445&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-FnpIgokNe8eHopcr73rzmA6d17E%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-0cda8f7775151a895ba5680b423e50e6cdbb42d078115248038fda59f66ac5ae10a6a78383e5b308ae6dfcf44db2c50c95744ea71f5f264c305a5e1275657320&expires=8h&r=706675411&vbdid=-&fin=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-6&fn=p-bb44e7c033d48f3f866516d2f2fe1f81-40-2025042100-6&rtype=1&dp-logid=263283662563838188&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=2a0349c66f068e0f700a8c64e62d80040bad7d3b0738f6e5&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 存储特点:
    - 指令和数据无差别存储在主存中
    - 每条指令/数据对应唯一主存地址
- 程序计数器(PC):
    - CPU内部寄存器，指向下一条待执行指令
    - 执行指令后自动加1
- 指令执行过程:
    - 从内存/寄存器获取操作数据
    - 进行运算操作（加减乘除等）
    - 将结果写回指定位置

#### 四、知识小结

|   |   |   |   |
|---|---|---|---|
|知识点|核心内容|考试重点/易混淆点|难度系数|
|C程序编译流程|源程序(.c) → 预处理器处理宏定义 → 编译器生成汇编代码 → 汇编器生成机器码(.o) → 链接器整合库函数生成可执行文件(.exe)|预处理与编译阶段区别；目标模块(.o)与可执行文件关系|⭐⭐⭐|
|程序运行机制|可执行文件从硬盘加载到主存 → CPU通过PC寄存器按序执行指令 → 指令操作数据（内存/寄存器） → 结果输出|存储程序原理；PC寄存器自动递增特性|⭐⭐⭐⭐|
|硬件交互逻辑|程序运行时通过输入设备（键盘/鼠标）交互 → 处理结果通过输出设备（显示器）呈现|主存与外存（硬盘）的数据流动关系|⭐⭐|
|关键工具作用|预处理器：替换宏常量；编译器：转译汇编代码；汇编器：生成机器码；链接器：合并目标模块|四者功能边界及协作顺序|⭐⭐⭐⭐|
#### 一、存储器的性能指标
##### 1. 存储器的容量
- ![](https://bdcm01.baidupcs.com/file/p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-1?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116612&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-UobThvmhZ1Bwyo5g3uTW3lSpXxM%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-08406cb322fc6046552b8abf1f88943088f825a896e81b178dd7580436b7768c505492347c40f0593302ac285d87fabf273f77f31902388a305a5e1275657320&expires=8h&r=741708147&vbdid=-&fin=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-1&fn=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-1&rtype=1&dp-logid=263328538734198682&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=b3434a369726e9249598d5fd593929892a3011e712882a0d80d4af97bfb69cf0&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 容量计算原理：存储器总容量=存储单元数量×每个单元存储位数。通过MAR（地址寄存器）位数﻿n可计算存储单元数量为$2^n$个，MDR（数据寄存器）位数决定每个单元存储的比特数。
- 实际容量说明：MAR位数反映的是最大支持容量，实际安装容量可能小于最大值。如32位MAR理论上支持4GB，但实际可能只安装1GB。
- 二进制表示原理：n位二进制数可表示$2^n$
    
    种不同状态，因此32位地址总线最多寻址$2^32$
    
    个存储单元。需熟记($2^1,2^{10}$)
    对应数值（2,4,8,16,32,64,128,256,512,1024）。
- 容量单位换算：
    - 存储容量单位：1KB=1024B，1MB=1024KB，1GB=1024MB，1TB=﻿1024GB
    - 注意区分大小写：大B表示字节(8bit)，小b表示比特(1bit)

#### 二、CPU的性能指标
##### 1. CPU主频
- ![](https://bdcm01.baidupcs.com/file/p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-2?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116612&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-m8d0VulLhtLQYPBccfk9faSritY%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-683939dab88c2d20c777fe3d0739ca1a9531b47cd1fbd425ac4bd6aeca09796a83903267730634451575fe0482b9400c8049b8fafe69f273305a5e1275657320&expires=8h&r=547743853&vbdid=-&fin=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-2&fn=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-2&rtype=1&dp-logid=263328538734198682&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=66239664855e8068c32f23017ea016b02a3011e712882a0d60f1fd2882e1895f&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 定义：CPU内数字脉冲信号的振荡频率，单位赫兹(Hz)。如3.6GHz表示每秒产生36亿个时钟脉冲。
- 作用机制：时钟脉冲像"广播体操口令"协调CPU各部件的操作节奏，每个脉冲触发一个基本操作步骤。

##### 2. CPU时钟周期
- ![](https://xacm01.baidupcs.com/file/p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-3?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116612&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-hxnkwfETtt5Y395jS9QXlEn0II8%3D&to=131&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CXian%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-dd946ac2cb63df9b9226dd21593daab2742acc203a252d9e59c6e4cc95f8971983b0bb463ce640d61d1ca599786ff3434b24414137e8500d305a5e1275657320&expires=8h&r=280770520&vbdid=-&fin=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-3&fn=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-3&rtype=1&dp-logid=263328538734198682&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=66239664855e8068b85158c4a6b08351d71f910815ef4b42305a5e1275657320&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 计算公式：时钟周期=1/主频，单位通常为纳秒。如1GHz主频对应1ns时钟周期。
- 性能影响：主频越高通常性能越好，但并非唯一决定因素。不同架构CPU在相同主频下性能可能差异显著。

##### 3. 执行一条指令所需的时钟周期数

- ![](https://bdcm01.baidupcs.com/file/p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-4?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116612&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-9iYiMds1vUfMtuQbKrS8jCCL02o%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-bc086ee4f8c47dc9fd5062e889efdca8f0761e6959268d4f688f9933f7a5c4fb9b41b3b5526bfbda5393cf8eba17c572bb00fda1bf304d43305a5e1275657320&expires=8h&r=796430960&vbdid=-&fin=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-4&fn=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-4&rtype=1&dp-logid=263328538734198682&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=66239664855e8068ffbe007f2b50d09d2a3011e712882a0d60f1fd2882e1895f&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- CPI概念：Clock cycle Per Instruction，反映指令执行效率。不同指令CPI不同（如取数指令需9周期，乘法指令需11周期）。
- 动态特性：相同指令的CPI可能因系统状态变化（如内存繁忙时取数操作周期数增加）。
- CPU时间计算：程序总执行时间=(指令条数×平均CPI)/主频。例如100条指令、CPI=3、主频1kHz的程序需0.3秒。

##### 4. 每秒执行多少条指令

- ![](https://bdcm01.baidupcs.com/file/p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-5?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116612&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-bunxJc1OaCWiO6josVoPhtxdqkY%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-3891c405d5d0583064957ebb5dc3372fe598da53a437a3c5f2fca279b51a8e62af899a068d5880c3d901913aa17b43eee44e947663efe665305a5e1275657320&expires=8h&r=621396740&vbdid=-&fin=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-5&fn=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-5&rtype=1&dp-logid=263328538734198682&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=66239664855e8068fca2b103d063e44cd71f910815ef4b42305a5e1275657320&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- IPS计算：IPS=主频/平均CPI，表示CPU的指令吞吐量。
- 单位规范：
    - 速率单位：1kIPS=1000IPS，1MIPS=$10^6$IPS
    - 示例：2MIPS表示每秒执行200万条指令

##### 5. 每秒执行多少次浮点运算
- FLOPS意义：专用于科学计算领域，衡量浮点运算能力。1TFLOPS=$10^{12}$FLOPS（每秒万亿次浮点运算）。
- 应用场景：超级计算机常用TFLOPS作为性能指标，如3TFLOPS表示每秒3万亿次浮点运算。

##### 6. 例题：CPU性能计算
- ![](https://bdcm01.baidupcs.com/file/p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-6?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116612&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-obxyb0m1Gyla6iGQZ%2FcVc5JkVI8%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-23f48ac00073a9df00d00fa03491ca075570361b3d31958b9abb1b75125052bff70a4732e6668ed911b67ed616663f1158abed5298f2018a305a5e1275657320&expires=8h&r=773586874&vbdid=-&fin=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-6&fn=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-6&rtype=1&dp-logid=263328538734198682&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=66239664855e8068230408e99c62dfffd71f910815ef4b42305a5e1275657320&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 题目解析
    - 已知条件：主频1000Hz，指令数100条，平均CPI=3
    - 计算过程：总时钟周期=100×3=300个，执行时间=300×(1/1000)=0.3秒
    - 关键点：理解CPI的统计平均特性，掌握时间=周期数/频率的转换关系

#### 三、系统整体的性能指标

##### 1. 数据通路带宽
- ![](https://bdcm01.baidupcs.com/file/p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-7?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116612&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-cN5nLCAR%2FPIvW5PsklyMpIyBJ68%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-268f1749627c010c1999f76a35b621ab05c09eca63766848e0ffa0721076c327cfee99fa38860e147b077adbb35cf4b6f7285cae14547ce8305a5e1275657320&expires=8h&r=895520247&vbdid=-&fin=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-7&fn=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-7&rtype=1&dp-logid=263328538734198682&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=6a9088c7620f7a1736564e37f877fcb02efd475fc46c06fc&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 定义：数据总线一次所能并行传送信息的位数，各硬件部件通过数据总线传输数据
- 影响：直接影响硬件部件间数据传输效率。例如：8位带宽的计算机读取16位数据需要2次传输，比单次传输更慢
- 应用场景：CPU与内存、内存与I/O设备间的信息传输都通过数据总线进行

##### 2. 吞吐量

- 定义：系统在单位时间内处理请求的数量，请求可以是单条指令或完整程序运行
- 关键因素：主要取决于主存的存取周期，包括：信息输入内存速度、CPU取指令速度、数据存取速度、结果输出速度
- 实例：
    - 淘宝服务器每秒钟处理的HTTP请求数
    - 食堂师傅单位时间内完成的打饭请求数

##### 3. 响应时间
- ![](https://bdcm01.baidupcs.com/file/p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-8?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116612&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-KKblYe5qhKHpJn2yxIuJHyJcmco%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-920139c66985715e38112b0d09cc8cd43a567aa92fd01557f917b2580259db04b6b9c6813619588586ade0f91ffdfeec0b5bbf78a7430415305a5e1275657320&expires=8h&r=363298788&vbdid=-&fin=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-8&fn=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-8&rtype=1&dp-logid=263328538734198682&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=0cce998314b34a673f5b22d5a4a7dcee2859b7547fbeed18&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 定义：从用户发送请求到系统返回结果所需的等待时间
- 实例：
    - 电脑右键点击到菜单弹出的时间间隔
    - 发送信息到收到回复的时间间隔
- 特点：与吞吐量类似，是适用范围很广的性能指标

#### 四、系统整体的性能指标动态测试

- ![](https://bdcm01.baidupcs.com/file/p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-9?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116612&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-sO4z5ILrpCABRlQTMNaClwSV28w%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-1ea444b64d6e4b560b2e9b1fe97fa3b09895f4c15d3454ddfc41682a72fccc515aaaaa3c111e7d8c4cc5b2327f0f67d365484b146e4724fc305a5e1275657320&expires=8h&r=831540490&vbdid=-&fin=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-9&fn=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-9&rtype=1&dp-logid=263328538734198682&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=c77a2290e27174be3d66e1a7460e33c3d71f910815ef4b42305a5e1275657320&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 基准程序：
    - 本质：设计好的包含各种指令频率的程序代码
    - 作用：通过运行耗时给出计算机综合评分（如鲁大师跑分）
    - 局限性：测试结果受程序指令设计影响，不能完全代表实际性能
- 应用实例：
    - 电脑性能测试（如显卡测试）
    - 手机跑分软件

#### 五、问题思考

- ![](https://bdcm01.baidupcs.com/file/p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-10?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116614&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-h7%2FVDYxWWZYuxLqL6DgVobhKqTg%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-fb2ed17ed06d6a64bf74569785602f7a747a70056968b91c61f2312db47dbdc98f48efbdfdb735f9097fa9aa7bd532057b48962a9a77bb3a305a5e1275657320&expires=8h&r=848091876&vbdid=-&fin=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-10&fn=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-10&rtype=1&dp-logid=263328538734198682&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=e83ff6a1394898305c92c18ca9f96aba2efd475fc46c06fc&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 主频与性能关系：
    - 主频高的CPU不一定更快（需考虑CPI因素）
    - 示例：2GHz CPU（CPI=10）实际比1GHz CPU（CPI=1）慢
- 指令系统影响：
    - 相同CPI下，支持更多指令类型的CPU可能表现更好
    - 示例：支持乘法指令的CPU比仅支持加法的CPU效率更高
- 基准程序局限性：
    - 测试结果与程序指令频度相关
    - 专用测试程序（如图形测试）不能反映其他应用场景性能

#### 六、知识回顾与重要考点
- ![](https://bdcm01.baidupcs.com/file/p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-11?bkt=en-3de6f374fcad9f514a94920d227b7f50&fid=282335-250528-&time=1758116614&sign=FDTAXUVGEQlBHSKfWqij-GBWOGYTBgG0KqHy7wNbwoLTVMyJyK6xE-Jf54DBzSj1GpSIr0KPNI4uIv1xI%3D&to=93&size=10&sta_dx=10&sta_cs=0&sta_ft=&sta_ct=7&sta_mt=7&fm2=MH%2CBaoding%2CAnywhere%2C%2C%E6%B5%99%E6%B1%9F%2Ccmnet&ctime=0&mtime=0&dt3=0&resv0=-1&resv1=0&resv2=rlim&resv3=5&resv4=10&vuk=0&iv=2&vl=0&htype=&randtype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-0bba3331275a8bfdf44130cfd6ed50095d9d6ca9e3ef8d0da2c744b60c9f67e94d0824a0d44ebace66aff3740095d202c0bf0fdd7fcd094f305a5e1275657320&expires=8h&r=974933751&vbdid=-&fin=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-11&fn=p-e5bd5047821cd340d815f2238a244ac5-40-2025042100-11&rtype=1&dp-logid=263328538734198682&dp-callid=0.1&hps=1&tsl=0&csl=0&fsl=-1&csign=dmayhhcqdS1jXSxjkf6DN1P7N8o%3D&so=0&ut=1&uter=1&serv=-1&uc=2198793033&ti=a5f92b9aebde11e5b44eeb1a4e4f7f1eaf3be29b3595ceca&hflag=30&from_type=&adg=n&reqlabel=250528_n_a41f86df5e35cbb101454d30a2b62fa9_0_a48b1707a0b6dfa129125efb8fb05ef2&chkv=5&bid=250528&by=themis)
- 关键公式：
    - CPU执行时间 = （指令条数×CPI）/主频
    - IPS（每秒指令数）= 主频/平均CPI
    - FLOPS（每秒浮点运算次数）
- 单位换算：
    - 存储容量：
        $K=2^{10},M=2^{20}﻿,G=2^{30}﻿,T=2^{40}$
    - 频率速率：
        ﻿$K=10^3,M=10^6,G=10^9,T=10^{12}$

- 扩展单位：
    - ﻿$P=10^{15},E=10^{18},Z=10^{21}$
    - 示例：神威太湖之光（93亿亿FLOPS=93P FLOPS）

#### 七、知识小结

| 知识点        | 核心内容                                                                      | 考试重点/易混淆点                                                           | 难度系数 |
| ---------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------- | ---- |
| 存储器容量计算    | 通过MAR（地址寄存器位数）和MDR（数据寄存器位数）计算总容量：总容量 = 2^MAR位数 × MDR位数，单位转换（比特→字节需÷8）     | MAR位数反映最大容量，实际容量可能小于理论值；二进制位数与地址数量的关系（n位→2^n个地址）                    | ⭐⭐   |
| 二进制数量级记忆   | 需掌握2^1到2^10的常用值（如2^5=32，2^8=256），扩展知识：游戏“2048”对应2^11                      | 区分存储容量单位（K=2^10，M=2^20）与速率单位（K=10^3，M=10^6）                         | ⭐⭐   |
| CPU主频与时钟周期 | 主频（Hz）= 时钟周期倒数；主频越高，性能通常越强，但受CPI（每条指令周期数）影响                               | 主频≠绝对性能，需结合CPI和指令集差异；例题：主频1000Hz，CPI=3，100条指令耗时=100×3×(1/1000)=0.3秒 | ⭐⭐⭐  |
| IPS与FLOPS  | IPS（指令/秒）= 主频/CPI；FLOPS（浮点运算/秒），单位前缀差异（1MIPS=10^6指令/秒，1MFLOPS=10^6浮点运算/秒） | 速率单位用10^n进制（如3T FLOPS=3×10^12），与存储单位区分                              | ⭐⭐⭐  |
| 系统性能指标     | 数据通路带宽（并行传输位数）、吞吐量（请求/秒）、响应时间（请求→响应耗时）                                    | 吞吐量与响应时间的关系；基准程序（跑分软件）的局限性（指令频次影响评分）                                | ⭐⭐   |
| 超算数量单位扩展   | 新增单位：P（10^15）、E（10^18）、Z（10^21）；案例：神威太湖之光=93P FLOPS                       | 单位递增规律（每级×10^3），与存储单位K/M/G/T的二进制基数区别                                | ⭐⭐   |
