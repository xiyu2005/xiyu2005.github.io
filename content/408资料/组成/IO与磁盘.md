### 磁盘容量
$$磁盘容量 = 字节数每扇区 \times 平均扇区数 \times 磁道数 \times 表面数 \times 盘片数$$
字节数一般为512B每扇区。磁盘容量$1TB=10^3 GB.$

### 访问时间

寻道时间$T_{avg\_seek}$,传动臂将读/写头顶味道目标扇区的**磁道**上
平均旋转时间$T_{avg\_rotation}=\frac{1}{2}\frac{1}{RPM}*60$秒（转半圈）
传送时间$T_{avg\_transfer}$:传送数据的时间


$$
T_{access} = T_{avg\_seek}+T_{avg\_rotation}+T_{avg\_transfer}
$$

>[!问题]
>假设磁盘存储器共6盘片，最外面两侧盘面不能记录，每面204磁道，每条磁道12个扇区，每个扇区512B，磁盘机转速7200rpm，平均寻道时间8ms。
1求存储容量2计算平均存储时间3设计磁盘地址格式

解答:
1.$(12-2)*204*12*512B = 12533760B$
2.$T_{avg\_seek}=8ms,+T_{avg\_rotation}=\frac{60}{2*7200}=4.167ms,T_{avg\_transfer}=\frac{60}{12*7200} = 0.694ms,$$T_{access} = T_{avg\_seek}+T_{avg\_rotation}+T_{avg\_transfer} = 12.86ms.$

3.$2^8>204,2^4>(6*2-2),2^4>12$,
柱面号（8位）、磁头号（4位）、扇区号（4位）
