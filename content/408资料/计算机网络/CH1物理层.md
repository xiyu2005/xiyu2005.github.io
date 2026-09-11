# ch1总体和物理层
OSI七层
**物理层**：**负责在物理介质（电缆，光纤，无线信道）传输原始比特流**，定义机械、电气、功能和规程特性。典型设备：网卡，集线器，网线，光纤，中继器；
**数据链路层**：**将物理层的比特流封装成帧**，负责在相邻节点之间的可靠传输（保证发送的帧不会丢失，如果丢失了，那么就重传），解决物理层可能出现的差错（如比特错）
功能：帧同步：定义帧开始和结束标志，确保接收方正确识别帧的边界；
差错控制：校验码（CRC，奇偶校验，海明校验）
流量控制；介质访问协议（MAC）：在共享介质（如以太网）中解决多节点信道的问题（如CSMA/CD协议）
典型设备：网卡，**二层**交换机，网桥；
**网络层**：**实现不同网络之间的数据传输（主机到主机，跨网路由），核心是路由选择和逻辑选址**。具体作用：1.逻辑寻址，为网络中设备分配唯一逻辑地址（IP地址），区分不同网络的节点。2.路由选择（OSFP和RIP），选择源网络到目的网络的最佳路径3.分组转发，将上层数据（报文）拆分为分组（Packet），并根据路由表转发到下一跳节点。拥塞控制：避免网络因数据量过大拥塞（比如路由器主动丢包），
典型设备：路由器
**传输层**：**负责端到端（源主机进程到目标主机进程）的可靠数据传输**，屏蔽底层网络的差异，为上层提供统一的通信接口。具体作用：1.分段和重组：将上层的大报文拆分为适合网络传输的小数据段，在接收端重组。2。可靠传输，如TCP三次握手，超时重传保证数据无丢失，无重复，按序到达。3.流量控制：基于接收端处理能力动态调整发送速率（TCP滑动窗口）4.分用复用（通过端口号区分不同进程）典型协议TCP，UDP
复用：多应用层进程可同时使用下面运输层服务；分用：运输层收到的信息分别交付上面应用层相应进程
TCP 协议：<span style="color:rgb(255, 0, 0)">面向连接、可靠的字节流服务</span>（有握手、重传、流量 / 拥塞控制，保证数据完整有序）
UDP 协议：无连接、不可靠的数据报服务（无建立连接流程，不纠错重传，开销小）
**会话层**：**负责建立、管理、终止两个应用程序的会话，确保通信双方同步**。1.会话建立与释放2.会话同步3.会话管理 典型应用：数据库连接会话管理，远程登陆Telnet会话控制
**表示层**：处理数据格式转换和表示，确保双方能够理解彼此数据格式。具体作用：1数据格式转换，转化为ASCII和Unicode；2.数据压缩解压（ZIP）3.数据加密解密，保障安全性（SSL/TLS）典型应用：JPEG，MP3，SSL
应用层：直接为用户程序提供网络服务，是用户和网络的接口。典型：HTTP，FTP，SMTP，DNS，Telnet

TCP/IP四层体系结构
应用层、运输层、网际层、数据链路层

## 协议
协议定义了两个或多个通信实体之间交换的报文的格式和顺序，以及报文发送/接受或其他事情的动作。要素：
1.**语法**：传输数据或者控制信息的格式或者结构
例子：MAC帧的结构：662N4，HTTP的请求格式，
2.**语义**：需要发出何种请求，作出何种相应和动作
例如：HTTP的响应状态码，200 OK，404 Not Found对应的含义
3.**时序（同步）**：动作的先后顺序
例如：TCP三次握手的时序

#### 协议VS服务：
协议是控制两个对等实体进行通信的规则的集合。在协议控制下，两个对等实体间的通信使本层能够像上一层提供服务。要实现本层协议，还需要使用下面一层所提供的服务。
1.协议的实现保证了能够向上一层提供服务。
2.**协议是“水平”的**，即协议是控制对等实体之间通信的规则。但**服务是“垂直”的**，即服务是下层向上层通过层间接口提供的。
3.并非在一个层内的全部功能都是服务。只有能被高一层实体“看见”的功能称作服务。
比如网络层IP协议的路由选择功能，并不是为传输层提供的服务。网络层对传输层提供的服务是主机之间分组转发。上层使用下层服务必须与下层交换命令（**服务原语**）
#### SAP
SAP是服务访问点。比如**物理层的SAP是网卡物理接口**。**MAC层的2B类型字段是数据链路层的SAP**（比如0x0806表示上层为ARP协议，链路层收到后把数据交给上层ARP协议）。**网络层的SAP是IP数据头报的1B协议字段**，**传输层向上给应用层的SAP是TCP/UDP端口**

#### SDU与PDU，PCI
**层与层之间交换的数据的单位称为服务数据单元SDU**，其实就是上层交给当前层的处理块。**协议数据单元（PDU）则是对等实体之间交换的数据单位**，
<div class="wrap" style="display:flex;justify-content:center;gap:0;font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;max-width:680px;margin:0 auto;padding:16px 8px;">

  <!-- ========== 左侧：发送方 ========== -->
  <div class="col" style="display:flex;flex-direction:column;width:150px;flex-shrink:0;">

    <div style="text-align:center;font-size:11px;color:#888;margin-bottom:6px;font-weight:600;">📤 发送方</div>

    <!-- 应用层 -->
    <div class="box" style="background:#e8f0fe;border:1.5px solid #4a90d9;border-radius:6px;padding:7px 4px;text-align:center;font-weight:700;font-size:13px;color:#1a3a5c;height:34px;display:flex;align-items:center;justify-content:center;">应用层</div>
    <div class="sdu" style="text-align:center;font-size:10px;color:#999;padding:2px 0;height:18px;line-height:18px;">SDU</div>
    <div class="sap" style="text-align:center;font-size:10px;background:#fff8e1;border:1px dashed #d4a017;border-radius:4px;padding:3px 2px;height:22px;display:flex;align-items:center;justify-content:center;gap:3px;color:#7a5c00;">
      SAP <span style="color:#2e7d32;font-size:12px;font-weight:700;">↑</span> <span style="color:#2e7d32;font-weight:600;">提供服务</span>
    </div>

    <!-- 运输层 -->
    <div class="box" style="background:#e8f0fe;border:1.5px solid #4a90d9;border-radius:6px;padding:7px 4px;text-align:center;font-weight:700;font-size:13px;color:#1a3a5c;height:34px;display:flex;align-items:center;justify-content:center;">运输层</div>
    <div class="sdu" style="text-align:center;font-size:10px;color:#999;padding:2px 0;height:18px;line-height:18px;">SDU</div>
    <div class="sap" style="text-align:center;font-size:10px;background:#fff8e1;border:1px dashed #d4a017;border-radius:4px;padding:3px 2px;height:22px;display:flex;align-items:center;justify-content:center;gap:3px;color:#7a5c00;">
      SAP <span style="color:#2e7d32;font-size:12px;font-weight:700;">↑</span> <span style="color:#2e7d32;font-weight:600;">提供服务</span>
    </div>

    <!-- 网络层 -->
    <div class="box" style="background:#e8f0fe;border:1.5px solid #4a90d9;border-radius:6px;padding:7px 4px;text-align:center;font-weight:700;font-size:13px;color:#1a3a5c;height:34px;display:flex;align-items:center;justify-content:center;">网络层</div>
    <div class="sdu" style="text-align:center;font-size:10px;color:#999;padding:2px 0;height:18px;line-height:18px;">SDU</div>
    <div class="sap" style="text-align:center;font-size:10px;background:#fff8e1;border:1px dashed #d4a017;border-radius:4px;padding:3px 2px;height:22px;display:flex;align-items:center;justify-content:center;gap:3px;color:#7a5c00;">
      SAP <span style="color:#2e7d32;font-size:12px;font-weight:700;">↑</span> <span style="color:#2e7d32;font-weight:600;">提供服务</span>
    </div>

    <!-- 数据链路层 -->
    <div class="box" style="background:#e8f0fe;border:1.5px solid #4a90d9;border-radius:6px;padding:7px 4px;text-align:center;font-weight:700;font-size:13px;color:#1a3a5c;height:34px;display:flex;align-items:center;justify-content:center;">数据链路层</div>
    <div class="sdu" style="text-align:center;font-size:10px;color:#999;padding:2px 0;height:18px;line-height:18px;">SDU</div>
    <div class="sap" style="text-align:center;font-size:10px;background:#fff8e1;border:1px dashed #d4a017;border-radius:4px;padding:3px 2px;height:22px;display:flex;align-items:center;justify-content:center;gap:3px;color:#7a5c00;">
      SAP <span style="color:#2e7d32;font-size:12px;font-weight:700;">↑</span> <span style="color:#2e7d32;font-weight:600;">提供服务</span>
    </div>

    <!-- 物理层 -->
    <div class="box" style="background:#e8f0fe;border:1.5px solid #4a90d9;border-radius:6px;padding:7px 4px;text-align:center;font-weight:700;font-size:13px;color:#1a3a5c;height:34px;display:flex;align-items:center;justify-content:center;">物理层</div>
  </div>

  <!-- ========== 中间：双向箭头 + PDU标注 ========== -->
  <div class="col" style="display:flex;flex-direction:column;width:210px;flex-shrink:0;padding:0 6px;">

    <!-- 应用层箭头组 -->
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:74px;">
      <div class="note" style="font-size:11px;font-weight:600;color:#4a90d9;text-align:center;margin-bottom:4px;white-space:nowrap;">PDU：应用报文</div>
      <div style="display:flex;align-items:center;width:100%;">
        <span style="flex:1;height:2px;background:#4a90d9;"></span>
        <span style="color:#4a90d9;font-size:16px;font-weight:700;padding:0 4px;">←</span>
        <span style="flex:2;height:2px;background:#4a90d9;"></span>
        <span style="color:#4a90d9;font-size:16px;font-weight:700;padding:0 4px;">→</span>
        <span style="flex:1;height:2px;background:#4a90d9;"></span>
      </div>
    </div>

    <!-- 运输层箭头组 -->
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:74px;">
      <div class="note" style="font-size:10.5px;font-weight:600;color:#4a90d9;text-align:center;margin-bottom:4px;line-height:1.3;">PDU：TCP报文段<br/>UDP用户数据报</div>
      <div style="display:flex;align-items:center;width:100%;">
        <span style="flex:1;height:2px;background:#4a90d9;"></span>
        <span style="color:#4a90d9;font-size:16px;font-weight:700;padding:0 4px;">←</span>
        <span style="flex:2;height:2px;background:#4a90d9;"></span>
        <span style="color:#4a90d9;font-size:16px;font-weight:700;padding:0 4px;">→</span>
        <span style="flex:1;height:2px;background:#4a90d9;"></span>
      </div>
    </div>

    <!-- 网络层箭头组 -->
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:74px;">
      <div class="note" style="font-size:11px;font-weight:600;color:#4a90d9;text-align:center;margin-bottom:4px;white-space:nowrap;">PDU：数据报(或分组)</div>
      <div style="display:flex;align-items:center;width:100%;">
        <span style="flex:1;height:2px;background:#4a90d9;"></span>
        <span style="color:#4a90d9;font-size:16px;font-weight:700;padding:0 4px;">←</span>
        <span style="flex:2;height:2px;background:#4a90d9;"></span>
        <span style="color:#4a90d9;font-size:16px;font-weight:700;padding:0 4px;">→</span>
        <span style="flex:1;height:2px;background:#4a90d9;"></span>
      </div>
    </div>

    <!-- 数据链路层箭头组 -->
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:74px;">
      <div class="note" style="font-size:11px;font-weight:600;color:#4a90d9;text-align:center;margin-bottom:4px;white-space:nowrap;">PDU：帧</div>
      <div style="display:flex;align-items:center;width:100%;">
        <span style="flex:1;height:2px;background:#4a90d9;"></span>
        <span style="color:#4a90d9;font-size:16px;font-weight:700;padding:0 4px;">←</span>
        <span style="flex:2;height:2px;background:#4a90d9;"></span>
        <span style="color:#4a90d9;font-size:16px;font-weight:700;padding:0 4px;">→</span>
        <span style="flex:1;height:2px;background:#4a90d9;"></span>
      </div>
    </div>

    <!-- 物理层箭头组 -->
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:34px;">
      <div class="note" style="font-size:11px;font-weight:600;color:#4a90d9;text-align:center;margin-bottom:2px;white-space:nowrap;">PDU：比特流</div>
      <div style="display:flex;align-items:center;width:100%;">
        <span style="flex:1;height:2px;background:#4a90d9;"></span>
        <span style="color:#4a90d9;font-size:16px;font-weight:700;padding:0 4px;">←</span>
        <span style="flex:2;height:2px;background:#4a90d9;"></span>
        <span style="color:#4a90d9;font-size:16px;font-weight:700;padding:0 4px;">→</span>
        <span style="flex:1;height:2px;background:#4a90d9;"></span>
      </div>
    </div>
  </div>

  <!-- ========== 右侧：接收方 ========== -->
  <div class="col" style="display:flex;flex-direction:column;width:150px;flex-shrink:0;">

    <div style="text-align:center;font-size:11px;color:#888;margin-bottom:6px;font-weight:600;">📥 接收方</div>

    <!-- 应用层 -->
    <div class="box" style="background:#fce8e6;border:1.5px solid #d9534f;border-radius:6px;padding:7px 4px;text-align:center;font-weight:700;font-size:13px;color:#5c1a1a;height:34px;display:flex;align-items:center;justify-content:center;">应用层</div>
    <div class="sdu" style="text-align:center;font-size:10px;color:#999;padding:2px 0;height:18px;line-height:18px;">SDU</div>
    <div class="sap" style="text-align:center;font-size:10px;background:#fff8e1;border:1px dashed #d4a017;border-radius:4px;padding:3px 2px;height:22px;display:flex;align-items:center;justify-content:center;gap:3px;color:#7a5c00;">
      SAP <span style="color:#2e7d32;font-size:12px;font-weight:700;">↑</span> <span style="color:#2e7d32;font-weight:600;">提供服务</span>
    </div>

    <!-- 运输层 -->
    <div class="box" style="background:#fce8e6;border:1.5px solid #d9534f;border-radius:6px;padding:7px 4px;text-align:center;font-weight:700;font-size:13px;color:#5c1a1a;height:34px;display:flex;align-items:center;justify-content:center;">运输层</div>
    <div class="sdu" style="text-align:center;font-size:10px;color:#999;padding:2px 0;height:18px;line-height:18px;">SDU</div>
    <div class="sap" style="text-align:center;font-size:10px;background:#fff8e1;border:1px dashed #d4a017;border-radius:4px;padding:3px 2px;height:22px;display:flex;align-items:center;justify-content:center;gap:3px;color:#7a5c00;">
      SAP <span style="color:#2e7d32;font-size:12px;font-weight:700;">↑</span> <span style="color:#2e7d32;font-weight:600;">提供服务</span>
    </div>

    <!-- 网络层 -->
    <div class="box" style="background:#fce8e6;border:1.5px solid #d9534f;border-radius:6px;padding:7px 4px;text-align:center;font-weight:700;font-size:13px;color:#5c1a1a;height:34px;display:flex;align-items:center;justify-content:center;">网络层</div>
    <div class="sdu" style="text-align:center;font-size:10px;color:#999;padding:2px 0;height:18px;line-height:18px;">SDU</div>
    <div class="sap" style="text-align:center;font-size:10px;background:#fff8e1;border:1px dashed #d4a017;border-radius:4px;padding:3px 2px;height:22px;display:flex;align-items:center;justify-content:center;gap:3px;color:#7a5c00;">
      SAP <span style="color:#2e7d32;font-size:12px;font-weight:700;">↑</span> <span style="color:#2e7d32;font-weight:600;">提供服务</span>
    </div>

    <!-- 数据链路层 -->
    <div class="box" style="background:#fce8e6;border:1.5px solid #d9534f;border-radius:6px;padding:7px 4px;text-align:center;font-weight:700;font-size:13px;color:#5c1a1a;height:34px;display:flex;align-items:center;justify-content:center;">数据链路层</div>
    <div class="sdu" style="text-align:center;font-size:10px;color:#999;padding:2px 0;height:18px;line-height:18px;">SDU</div>
    <div class="sap" style="text-align:center;font-size:10px;background:#fff8e1;border:1px dashed #d4a017;border-radius:4px;padding:3px 2px;height:22px;display:flex;align-items:center;justify-content:center;gap:3px;color:#7a5c00;">
      SAP <span style="color:#2e7d32;font-size:12px;font-weight:700;">↑</span> <span style="color:#2e7d32;font-weight:600;">提供服务</span>
    </div>

    <!-- 物理层 -->
    <div class="box" style="background:#fce8e6;border:1.5px solid #d9534f;border-radius:6px;padding:7px 4px;text-align:center;font-weight:700;font-size:13px;color:#5c1a1a;height:34px;display:flex;align-items:center;justify-content:center;">物理层</div>
  </div>
</div>
**N+1层的PDU作为N层的SDU，交付给N层，加上N层的PCI形成了N层的PDU。**
PCI就是我们所说的首部。
多个SDU可以合成一个PDU（缓存），一个SDU也可以划分为多个PDU（分片）


传输效率：应用层数据大小/总发送数据大小。比如应用层1000B，TCP首部20B，IP首部20B，MAC帧6+6+2+4=18B，总共1058B，1000B/1058B=94.5%.


缺点：无法同步，需要时钟信号
# 物理层
基带信号
基带调制（编码）
1.不归零（NRZ）编码
不归零NRZ编码电信号用于计算机内部部件传输数据挺好的。
```custom-frames
frame: NRZ
style: height: 400px;
```
缺点：无法同步，需要时钟信号辅助同步
2.RZ编码：每个比特传输完成后归零。
```custom-frames
frame: RZ
style: height: 400px;
```

接收端可以根据信号归零特性确定以为数据结束，实现自同步，不需要额外同步信号。
但是归零需要占用一部分带宽。传输效率低。

3.反向不归零NRZI编码
```custom-frames
frame: NRZI
style: height: 400px;
```
这里采用了跳变表示1，不跳变为0。可以<span style="color:rgb(255, 0, 0)">自同步</span>

4.曼彻斯特编码
每个二进制对应信号**中间跳变，作为自同步的时钟信号，也作为数据信号**（向下跳变表示1或者相反）以太网采用。二个码元携带一个bit。
如果指定是10BASE-T ，那么是IEEE 802.3的高跳低为1.
```custom-frames
frame: Manchester
style: height: 400px;
```
曼彻斯特编码优点：1.自带同步时钟2.无直流分量，水合中低速段距离数字通信3.抗干扰能力强（10BASE-T）4.支持差分编码（用于令牌环网）
缺点：1.编码效率低2.占用带宽大（因为跳变频繁）3.时下复杂度高


5.差分曼彻斯特编码
中间都跳变，**中间的跳变仅是时钟信号。数据的表示在于每秒开始处有无跳变**。一般是不跳变为1，有跳变为0.
```custom-frames
frame: DifMan
style: height: 400px;
```


### 带通调制
振幅键控ASK
频移键控FSK
相移键控PSK
码元：一个码元可以传输多个bit。
###### 多进制振幅键控MASK
例如0V表示00，3V表示01，6V表示10，9V表示11，使得一个码元可以携带2bit。8ASK信号每个码元携带$\log_2 8 =3bit$
##### 多进制频移键控MFSK
比如4种不同频率波形那么就是4FSK，携带$log_2 4 = 2bit$
###### 多进制相移键控MPSK
4PSK也叫正交相移键控OPSK。携带2bit。但是缺点是M增大时相位差小，抗干扰能力弱。
### 正交振幅调制QAM
振幅和相位作为2个独立参量调制。比如64QAM，携带$\log_2 64 = 6bit$

M进制码元可以携带$\log_2 M$个bit。
比特率 = 波特率 * $\log_2 M$

### 数据通信系统模型
单向通信：单工通信；
双向交替通信：半双工通信
双向同时通信：全双工通信
传播速率：通常是信号比特在介质的传播速度。
传输速率：结点（主机、交换机、路由器）每秒向所连接的介质注入比特的速度，bit/s
不能笼统地认为数据发送率越高，传输总时延越小。
**时延带宽积**：
比特时间：发送1b的时间；比特距离：一个比特时间内在链路上传播的距离
$$时延带宽积 = 传播时延 \times 链路信道带宽$$
注意是<span style="color:rgb(255, 0, 0)">链路传播时延</span>
思考一下：如果是两段不同链路相连的总时延带宽积，应该是最小的带宽乘以时延之和！
### 香农定理和奈奎斯特准则
信噪比$dB = 10 \times \lg (S/N)$
香农公式：单位为bit/s
$$C=W \times log_2 (1+S/N) $$
奈奎斯特公式码元极限速率为2W，M是码元携带比特数
$$C = 2W \times \log_2 M$$
**与码间串扰相关：奈氏准则**





面向连接

## 数据交换技术
**电报交换**
利用率最低，总时延 = 建立连接时延 + 发送时延 + 传播时延 （+释放时延）

**分组交换**（基于存储转发）
**报文交换**（基于存储转发）

存储转发技术
设分组数k，每组长度L，m段链路
$总时延 = kL/v + （m-1）（L/v）$
存储转发技术与直通交换技术（仅交换机，识别MAC地址就决定）



### 虚电路和数据报
数据报网络中路由器采用目的ip转发，虚电路中路由器使用虚电路号转发分组。
**数据报到达的顺序不能保证。**
虚电路网络中通信时，需要先建立连接（虚电路），可以**保证按序到达**。
多条虚电路逻辑上独立，但是可以使用同一段物理带宽。缺陷是一个虚电路上的一个路由器故障，整个就不能工作。
<span style="color:rgb(255, 0, 0)">以太网的逻辑结构总线型，物理结构星型</span>

## 物理层传输媒体
### 导引型传输媒体
同轴电缆，双绞线。
双绞线：<span style="color:rgb(255, 0, 0)">绞合的目的是减少电磁干扰</span>，分为无屏蔽双绞线UTP和屏蔽双绞线STP
10Base-T表示T为双绞线，Base为基带信号（以太网为曼彻斯特编码），速率为10Mb/s
光纤：-F

### 非导引醒传输媒体
电磁波为介质。波长越长一般距离越远。波长越短距离短但是穿透力好。
卫星通信具有较大的<span style="color:rgb(255, 0, 0)">传播时延</span>。

### 物理层接口特性
机械特性：接线器形状尺寸、引脚数目排列、固定和锁定装置
电气特性：电压范围、阻抗匹配情况、传播速率以及距离限制
功能特性：某一电平电压的意义、接口电缆各条信号线作用
过程特性：工作顺序和时序

## 中继器、集线器
### 中继器
中继器的作用就是信号放大。
### 集线器
集线器本质上就是多接口中继器。集线器只工作在物理层。
集线器不能分割广播域、也不能分割冲突域。

## 性能指标
转发时延
吞吐量：单位时间通过某个网络的<span style="color:rgb(255, 0, 0)">实际</span>数据量


