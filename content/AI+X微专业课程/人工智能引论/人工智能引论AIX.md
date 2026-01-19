# 一、绪论
## 图灵机模型
机械式计算过程：
第一步：读入gcd(24,16)这一信息，触发最大公约数这一指令得到24和16的最大公约数8
第二步：触发乘法指令
第三步：触发加法指令
第四步：在纸带方格上留下97计算结果后图灵机停止工作 

![[Pasted image 20251204121333.png]]
给出12+8这一问题在图灵机上的执行步骤

# 二、知识表达与推理
1.命题逻辑
![[Pasted image 20251202195419.png]]
![[Pasted image 20251202195428.png]]

2.谓词逻辑
![[Pasted image 20251202195547.png]]

辛普森悖论
因果图是有向无环图DAG
因果图联合概率形式
对于任意的有向无环图模型，模型中d个变量的联合概率分布由每个节点与其父节点之间条件概率P(child|parents)的乘积给出：
$$
P\left(x_{1}, x_{2}, \cdots, x_{d}\right)=\prod_{j=1}^{d} P\left(x_{j} \mid x_{p a(j)}\right)
$$
$\begin{aligned} & P\left(X_1, X_2, X_3, X_4, X_5, X_6, X_i, X_j\right) \\ & =P\left(X_2\right) \times P\left(X_3\right) \times P\left(X_1 \mid X_2, X_3, X_i\right) \times P\left(X_4 \mid X_2\right) \\ & \times P\left(X_5 \mid X_3\right) \times P\left(X_6 \mid X_i\right) \times P\left(X_i \mid X_4\right) \times P\left(X_j \mid X_1, X_5, X_6\right)\end{aligned}$
![[Pasted image 20251202200851.png]]



![[Pasted image 20251202202548.png]]
![[Pasted image 20251202204535.png]]

# 第四章机器学习
一元回归算法：最小二乘法
决策树
K-means![[Pasted image 20251202210320.png]]
![[Pasted image 20251202210323.png]]


LDA线性判别分析

对于一组具有标签信息的高维数据样本，LDA利用其类别信息，将其线性投影到一个低维空间上，在低维空间中同一类别样本尽可能靠近，不同类别样本尽可能彼此远离。
![[Pasted image 20251204115428.png]]
## 主成分分析PCA
### 方差协方差和相关系数
方差 方差描述了样本数据的波动程度，数值上等于各个数据与样本均值之差的平方和之平均数，假设有 $n$ 个数据，记为 $X=\left\{x_i\right\}(i=1, \ldots, n)$ ，那么样本方差（sample variance）即为
$$
\operatorname{var}(X)=\frac{1}{n-1} \sum_{i=1}^n\left(x_i-u\right)^2
$$

其中 $u$ 是样本均值，$u=\frac{1}{n} \sum_{i=1}^n x_i$ 。 上述样本方差公式里分母为 $\mathrm{n}-1$ 的目的是为了让对方差的估计是无偏估计（unbiased estimator）。

协方差 协方差衡量了两个变量之间的相关度，假设有两个变量，观察到不同时刻两个变量的取值，记为 $(X, Y)=\left\{\left(x_i, y_i\right\}(i=1, \ldots, n)\right.$ ，那么两个变量的协方差为：
$$
\operatorname{cov}(X, Y)=\frac{1}{n-1} \sum_{i=1}^n\left(x_i-E(X)\right)\left(y_i-E(Y)\right)
$$

其中 $E(X)$ 和 $E(Y)$ 分别是 $X$ 和 $Y$ 的样本均值，分别定义如下 $E(X)= \frac{1}{n} \sum_{i=1}^n x_i, E(Y)=\frac{1}{n} \sum_{i=1}^n y_i$ 。

**主成分分析**（principal component analysis）是一种特征降维方法，在消除数据噪声、冗余等方面具有广泛应用。
降维需要尽可能将数据向方差最大的方向进行投影，使得数据所蕴含的信息丢失得尽可能少。如图4.5左图所示，向𝑦方向投影（使得二维数据映射为一维）就比向𝑥方向投影结果在降维这个意义上而言要好；图4.5右图则是黄线方向投影要好。这样的投影结果更好的保留了未降维前数据的离散程度。![[Pasted image 20251204115843.png]]
![[Pasted image 20251202210623.png]]
下面对主成分分析的描述不正确的是 
a）主成分分析是一种特征降维方法保持最大
b) 主成分分析可保证原始高维数据被投影映射后，其方差保持最大。
c）在主成分分析中，将数据向方差最大方向进行投影，可使得数据所蕴含信息没有丢失，以便在后续处理过程中各个数据 ＂彰显个性＂
d）在主成分分析中，所得低维数据中每一维度之间具有极大相关度
该题选项d

## 特征人脸办法
### 奇异值分解
![[Pasted image 20251204120246.png]]
![[Pasted image 20251204120304.png]]
判断题：奇异值分解会将矩阵分解成三个子矩阵 对

1．下面对特征人脸算法描述不正确的是（ ）
a）特征人脸方法是一种应用主成分分析来实现人脸图像降维的方法
b）特征人脸方法是用一种称为＂特征人脸（eigenface）＂的特征向量按照线性组合形式来表达每一张原始人脸图像
c）每一个特征人脸的维数与原始人脸图像的维数一样大
d）特征人脸之间的相关度要尽可能大
该题选项d
## 潜在语义分析
假设单词总数为 M ，文档数为 N
矩阵 D 是一个 RxR 的对角矩阵，其对角线上值按照从大到小进行排序
$$
D=\operatorname{diag}\left(\sigma_1, \ldots, \sigma_R\right), \sigma_1 \geq \sigma_2 \geq \ldots \geq \sigma_k \geq \ldots \geq \sigma_R .
$$

矩阵 U 是一个 $\mathrm{M} \times \mathrm{R}$ 的矩阵，U中的每一个行向量被称为 LSI 单词向量
（6） V 是一个 NxR 的矩阵，$V^T$ 是一个 RxN 的矩阵， V 中的每一个行向量被称为LS文档向量（ LSI document vectors）


1．在潜在语义分析中，给定 M 个单词和 N 个文档所构成的单词－文档矩阵（term－document）矩阵，对其进行分解，将单词或文档映射到一个R维的隐性空间。下面描述不正确的是

a）单词和文档映射到隐性空间后具有相同的维度
b）通过矩阵分解可重建原始单词－文档矩阵，所得到的重建矩阵结果比原始单词－文档矩阵更好捕获了单词－单词、单词－文档、文档－文档之间的隐性关系
c）这一映射过程中需要利用文档的类别信息
d）隐性空间维度的大小由分解过程中所得对角矩阵中对角线上不为零的系数个数所决定该题选项c

# 第五章神经网络与深度学习
激活函数
sigmoid$f(x)=\frac{1}{1+e^{-x}}$,ReLu

| 激活函数名称  | 函数功能                                                                                              | 函数求导                                                                                                       |
| :------ | :------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------- |
| Sigmoid | $f(x)=\frac{1}{1+e^{-x}}$                                                                         | $f^{\prime}(x)=f(x)(1-f(x))$                                                                               |
| Tanh    | $f(x)=\frac{2}{1+e^{-2 x}}-1$                                                                     | $f^{\prime}(x)=1-f(x)^2$                                                                                   |
| Relu    | $f(x)=\left\{\begin{array}{l}0, \text { for } x<0 \\ x, \text { for } x \geq 0\end{array}\right.$ | $f^{\prime}(x)=\left\{\begin{array}{l}0, \text { for } x<0 \\ 1, \text { for } x \geq 0\end{array}\right.$ |
多分类激活函数
Softmax$f(x_i)=\frac{e^{x_i}}{\Sigma_{j=1}^k e^{x_j}}$
损失函数
（1）均方误差损失函数
$$
M S E=\frac{1}{n} \sum_{i=1}^n\left(y_i-\widehat{y}_i\right)^2
$$
（2）交又熵损失函数
$$
 \quad \mathrm{H}(p, q)=-\sum_x p(x) \log q(x)
$$
损失函数：$C E=-y * \log \left(\hat{y}^T\right)$

梯度下降
$f(\boldsymbol{x}+\Delta \boldsymbol{x})-f(\boldsymbol{x})=\|\nabla f(\boldsymbol{x})\|\|\Delta \boldsymbol{x}\| \cos \theta=-\|\Delta \boldsymbol{x}\|\|\nabla f(\boldsymbol{x})\|$
单选题：
下面对误差反向传播（error back propagation，BP）描述不正确的是 
a）BP算法是一种将输出层误差反向传播给隐藏层进行参数更新的方法
b）BP算法将误差从后向前传递，获得各层单元所产生误差，进而依据这个误差来让各层单元修正各单元参数
c）对前馈神经网络而言，BP算法可调整相邻层神经元之间的连接权重大小
d）在BP算法中，每个神经元单元可包含不可偏导的映射函数
该题选项：d

### 卷积
![[Pasted image 20251203112122.png]]
### 卷积性质
选择性感受野：卷积所得结果中，每个输出点的取值仅依赖于其在输入图像中该点及其邻域区域点的取值，而与这个区域之外的其他点取值均无关，该区域被称为感受野（receptive field）

局部感知、参数共享；
下采样约减抽象：假设被卷积图像大小为𝑤×𝑤、卷积核大小为𝐹×𝐹、上下左右四个边缘填充像素行/列数为$P=[𝐹/2]$、步长为𝑆，则被卷积结果的分辨率是$(𝑊−𝐹+2𝑃)/𝑆+1$。 

判断题

卷积是一种下采样操作。对

感受野是卷积的结果。错


## 池化
最大池化（max pooling）：从输入特征图的某个区域子块中选择值最大的像素点作为最大池化结果（见图5.12）。

平均池化（average pooling）：计算区域子块所包含所有像素点的均值，将均值作为平均池化结果。

k-max池化（k-max pooling）：对输入特征图区域子块中的像素点取前k个最大值。如图5.13所示，从包含4个取值的每一列中选取前2个最大值就得到了k-max池化结果。
![[Pasted image 20251203112626.png]]

![[Pasted image 20251203112607.png]]

### 神经网络正则化
过拟合（over fitting）：过于紧密或精确地匹配特定数据集，以致于无法良好地拟合其他数据或预测未来的观察结果的现象。

泛化能力（generalization）：拟合其他数据或预测未来的观察结果的现象的能力。
#### 正则化
Dropout：指在训练神经网络的过程中随机丢掉一部分神经元来降低神经网络的复杂度，从而防止过拟合。Dropout的实现方法很简单：在每次迭代训练中，以一定概率随机屏蔽每一层中的若干神经元，用余下神经元构成的网络继续训练。

批归一化：批归一化（batch normalization）就是通过规范化手段，把神经网络每层中任意神经元的输入值分布改变成均值为0、方差为1的标准正态分布，把偏移较大的分布强制映射为标准正态分布。经过批归一化处理，激活函数的输入值被映射到非线性函数梯度较大的区域，使得梯度变大从而克服梯度消失问题，进而加快收敛速度。


深度神经网络结构复杂、参数众多，很容易造成过拟合（over－fitting）。为了缓解神经网络在训练过程中出现的过拟合现象，需要采取一些正则化技术来提升神经网络的泛化能力（generalization）。
**$L_1$ 和 $L_2$ 正则化**：对于具有 $n$ 个训练数据 $\left\{\left(x_1, y_1\right), \ldots,\left(x_n, y_n\right)\right\}$ 的神经网络，其中 $\left(x_i, y_i\right)(1 \leq i \leq n)$ 分别为输入样本及其对应的标签。加入正则化项后，神经网络的损失函数一般可如下表示：
$$
\min \frac{1}{n} \sum_{i=1}^n \underbrace{\operatorname{Loss}\left(y_i, f\left(\boldsymbol{W}, x_i\right)\right)}_{\text {损失函数 }}+\underbrace{\lambda}_{\text {正则化权重 }} \times \underset{\text { 正则化项 }}{\Phi(\boldsymbol{W})}
$$

其中，$f\left(\boldsymbol{W}, x_i\right)$ 表示参数为 $\boldsymbol{W}$ 的神经网络对输入 $x_i$ 的预测、 $\Phi(\boldsymbol{W})$ 为正则化项（又称惩罚项）、 $\lambda$ 为正则项权重。
正则化项 $\Phi(W)$ 一般用模型参数 $W$ 的范数形式来表示。假设神经网络模型中参数数目为 $\mathbb{N}$ ，则参数的范数形式主要有：
$\boldsymbol{L}_0$ 范数：数学表示为 $\|\boldsymbol{W}\|_0=\sum_{i=1}^{\mathbb{N}} \mathbb{I}\left[w_i \neq 0\right]$ ，其中 $\mathbb{\text { 是指示函数，若括号内表达式为真，函数值为 } 1 \text { ，反之为 } 0 \text { 。所以 } L _ { 0 } \text { 范数指模型参数 } \boldsymbol { W }}$中非零元素个数。 $L_0$ 可实现模型参数的稀疏化。但是，由于 $L_0$ 范数正则化是一个NPHard问题，难以求解，因此一般不用 $L_0$ 范数。
$\boldsymbol{L}_{\mathbf{1}}$ 范数：数学表示为 $\|W\|_1=\sum_{i=1}^{\mathbb{N}}\left|w_i\right|$ 
$\boldsymbol{L}_2$ 范数：数学表示为 $\|W\|_2=\sqrt{\sum_{i=1}^{\mathbb{N}} w_i^2}$
判断题
使用dropout可以防止过拟合。对

简答题
请根据你的理解介绍什么是批归一化。
答案：通过规范化手段，把神经网络每层中任意神经元的输入值分布改变成均值为 0 、方差为 1 的标准正态分布，把偏移较大的分布强制映射为标准正态分布。
### DL in NLP&CV
#### 词向量生成
word2vec：假设词典中有 $V$ 个不同的单词，现在考虑如何生成第 $k$ 个单词的 $N$ 维词向量 。首先，将该单词表示成 $V$ 维one－hot 向量 $\boldsymbol{X}$ ，向量
$$
\begin{gathered}
\text { word2vec model }=\operatorname{maxP}(\text { 输出表达 } \mid \text { 输入表达 }) \\
=\max \log \left(\frac{e^{y_k^*}}{\sum_{j=1}^V e^{y_j}}\right)=\max \left(y_k^*-\log \sum_{j=1}^V e^{y_j}\right)
\end{gathered}
$$

其中星号（＊）表示预测值。对上式取其相反数，令其最小，则得到损失函数：
$$
\operatorname{loss}=-y_k^*+\log \sum_{j=1}^V e^{y_j}
$$

这样就可以利用梯度下降和误差后向传播来优化训练参数 $W_{V \times N}$ 和 $W_{N \times V}^{\prime}$ 了。
－通常Word2Vec的模型参数有两种训练模式。一种是Continuous Bag－of－ Words（CBoW），即根据某个单词所处的上下文单词来预测该单词。另一种是Skip－gram，即利用某个单词来分别预测该单词的上下文单词。
![[Pasted image 20251203114143.png]]图像分类与目标定位
在图像分类和目标定位过程中，单次目标检测模型不仅要检测物体位置，同时它也要判断所检测物体的类别标签。因此，图像分类和目标定位需要同时完成回归问题（位置判断）与分类问题（物体识别）两个任务，这种同时解决两个及两个以上问题的任务为多任务学习（Multi-Task Learning）。

输入一幅图像，首先利用卷积神经网络来提取视觉特征。在图5.26中，给定一幅图像，卷积神经网络经过若干次卷积与池化的操作，可提取一个特征向量来表示输入图像。这个向量作为输入特征分别传送给两个任务，即分类任务和定位任务：
a)分类任务。Softmax分类函数将全连接层所得特征向量映射为归一化概率值，用来表示每个概念在输入图像中出现的概率。在Softmax分类函数的输出概率向量中，向量中每一维代表输入图像中某个类别出现的概率。在训练中，可用交叉熵等损失函数来计算模型学习的误差；
b)目标定位。将全连接层输出向量转换为一个**四维向量**，四维向量分别代表一个包围盒的左上角横坐标和纵坐标以及该矩形框宽与高取值，并使用均方差损失函数计算模型的误差。最终，将两个任务所得误差相加，作为整个模型的误差，用于计算模型梯度，更新模型参数。这样，训练好的模型可以同时对图像分类以及对图像中视觉目标对象进行定位。
![[Pasted image 20251203114636.png]]
简答题
请简述词向量模型的结构。
答案：词向量模型由一层输入层，一层隐藏层，一层输出层构成

判断题
在目标定位任务中，如何可以用（ $\mathrm{x}, \mathrm{y}, \mathrm{w}, \mathrm{h}$ ）表达一个 bounding box。对

# 第六章
### 强化学习

智能体（agent），环境（environment），状态（state），动作（action），策略（policy），奖励（reward）
![[Pasted image 20251203114833.png]]![[Pasted image 20251203114903.png]]

## 离散马尔可夫链

t+1时刻状态仅与t时刻状态相关$\operatorname{Pr}\left(X_{t+1}=x_{t+1} \mid X_0=x_0, X_1=x_1, \cdots, X_t=x_t\right)=\operatorname{Pr}\left(X_{t+1}=x_{t+1} \mid X_t=x_t\right)$
引入奖励：奖励函数 $\boldsymbol{R}: \boldsymbol{S} \times \boldsymbol{S} \mapsto \mathbb{R}$ ，其中 $\boldsymbol{R}\left(\boldsymbol{S}_t, \boldsymbol{S}_{t+1}\right)$ 描述了从第 $\boldsymbol{t}$ 步状态转移到第 $\boldsymbol{t}+\mathbf{1}$ 步状态所获得奖励
定义回报：为了比较不同奖励机制的优劣，在每个时刻定义回报（return）来反映该时刻可得到的累加奖励：
$$
G_t=R_{t+1}+\gamma R_{t+2}+\gamma^2 R_{t+3}+\cdots(6.1 .2)
$$

其中 $\gamma \in[0,1]$ 是折扣因子（discount factor），$R_{t+k}(t>0)$ 表示 $t+k$ 时刻获得的奖励。 $t$ 时刻所获得的回报 $G$ 反映了该时刻之后的累加奖励。当折扣因子 $\gamma$ 小于 1 时，距离当前时刻越远的奖励对该时刻反馈贡献越少。假设 $\gamma=0.99$ ，则图6．3中两个奖励序列在 0 时刻的回报值分别为
$$
\begin{gathered}
(0,0,1,1): G_0=0+0.99 \times 0+0.99^2 \times 1+0.99^3 \times 1=1.9504 \\
(1,1,0,0): G_0=1+0.99 \times 1+0.99^2 \times 0+0.99^3 \times 0=1.99
\end{gathered}
$$

根据回报值可以认为 $(1,1,0,0)$ 是一个更好的奖励序列。这一结果也与现实生活中的认知活动相符，即距离某个时刻越近，所给予的奖励会对该时刻回报产生更大影响。因此，在强化学习中，要设计的奖励机制应该对当前时刻及其附近时刻能够带来的奖励更为关注。

在马尔可夫链模型 $M P=(S, P)$ 中加入**奖励函数和折扣因子**后，可得到的模型被称为**马尔可夫奖励过程**（Markov reward process，MRP），其形式化定义为 $M R P= (S, P, R, \gamma)$ 。

马尔可夫决策过程：
如下定义马尔可夫决策过程（Markov decision process，MDP）MDP $=(S, A, P, R, \gamma)$
A为动作集合。

## 强化学习定义
如下定义马尔可夫决策过程（Markov decision process，MDP）MDP $=(S, A, P, R, \gamma)$
，学习一个最优策略$\pi^*$,对任意$s \in S$,使得$V_{\pi^*}(s)$的值最大

### 贝尔曼方程
描述了价值函数或动作-价值函数的递推关系
- 价值函数（Value Function）$V_\pi(s)=\mathbb{E}_\pi\left[R_{t+1}+\gamma R_{t+2}+\gamma^2 R_{t+3}+\cdots \mid S_t=s\right]$
- 动作－价值函数（Action－Value Function）$q_\pi(s, a)=\mathbb{E}_\pi\left[R_{t+1}+\gamma R_{t+2}+\gamma^2 R_{t+3}+\cdots \mid S_t=s, A_t=a\right]$

价值函数的贝尔曼方程 $\quad V_\pi(s)=\mathbb{E}_{a \sim \pi\left(s^{,}\right)} \mathbb{E}_{s^{\prime} \sim P(\cdot \mid s, a)}\left[R\left(s, a, s^{\prime}\right)+\gamma V_\pi\left(s^{\prime}\right)\right]$
动作－价值函数的贝尔曼方程 $\quad q_\pi(s, a)=\mathbb{E}_{s^{\prime} \sim P(\cdot \mid s, a)}\left[R\left(s, a, s^{\prime}\right)+\gamma \mathbb{E}_{a^{\prime} \sim \pi\left(s^{\prime},\right)}\left[q_\pi\left(s^{\prime}, a^{\prime}\right)\right]\right]$

### 策略优化定理
分别给出 $\pi$ 和 $\pi^{\prime}$ 两个策略，如果对于任意状态 $s \in S$ ，有 $V_\pi(s) \leq V_{\pi^{\prime}}(s)$ ，那么可以认为策略 $\pi^{\prime}$ 不比策略 $\pi$ 差，可见＂更优＂策略是一个偏序关系。可以证明，给定任意给定状态 $s \in S$ ，如果两个策略 $\pi$ 和 $\pi^{\prime}$ 满足如下条件：
$$
q_\pi\left(s, \pi^{\prime}(s)\right) \geq q_\pi(s, \pi(s))
$$

那么对于该任意给定状态 $s \in S$ ，有
$$
V_{\pi^{\prime}}(s) \geq V_\pi(s)
$$

即策略 $\pi^{\prime}$ 不比策略 $\pi$ 差。这个结论称为策略优化定理。


与马尔可夫奖励过程相比，马尔可夫决策过程引入了哪一个新的元素（ ）？
A．反馈
B．动作
C．终止状态
D．概率转移矩阵
（B）


### 策略评估
#### 动态规划
#### 蒙特卡洛采样
#### 时序差分


在策略评估动态规划法的基础上，每次迭代只对一个状态进行**策略评估**和**策略优化**，就可以得到算法6.5，这个算法被称为价值迭代（value iteration）算法
![[Pasted image 20251203140036.png]]
Q学习算法
Q学习中直接记录和更新动作-价值函数q_π而不是价值函数V_π，这是因为策略优化要求已知动作-价值函数q_π，如果算法仍然记录价值函数V_π，在不知道状态转移概率的情况下将无法求出q_π。于是，Q学习中，只有动作-价值函数（即q函数）参与计算。![[Pasted image 20251203140028.png]]

在强化学习中，通过哪两个步骤的迭代，来学习得到最佳策略（D ）
A．价值函数计算与动作 - 价值函数计算
B．动态规划与Q－Learning
C．贪心策略优化与Q－learning
D．策略优化与策略评估


# 第七章 博弈论

合作博弈，非合作博弈；静态博弈，动态博弈；完全信息博弈，不完全信息博弈
## 纳什均衡
博弈的稳定局势即为纳什均衡
Nash定理：若参与者有限，每位参与者的策略集有限，收益函数为实值函数，则博弈必存在混合策略意义下的纳什均衡。

策梅洛定理（Zermelo's theorem）：对于任意一个有限步的双人完全信息零和动态博弈，一定存在先手必胜策略或后手必胜策略或双方保平策略

图 1．标志着现代博弈理论的初步形成的事件是（A ）
A 1944年冯•诺伊曼与奥斯卡•摩根斯特恩合著《博弈论与经济行为》的出版
B纳什均衡思想的提出
C囚徒困境思想的提出
D冯•诺伊曼计算机的实现
图 2．下面对博弈研究分类不正确的是 (D)
A 合作博弈与非合作博弈
B 静态博弈与动态博弈
C 完全信息博弈与不完全信息博弈
D 囚徒困境与纳什均衡

## 虚拟遗憾最小化算法

定义：对于一个有 $N$ 个玩家参加的博弈，玩家 $i$ 在博弈中采取的策略记为 $\sigma_i$ 。对于所有玩家来说，他们的所有策略构成了一个策略组合，记作 $\sigma=\left\{\sigma_1, \sigma_2, \ldots, \sigma_N\right\}$ 。策略组中，除玩家 $i$ 外，其他玩家的策略组合记作 $\sigma_{-i}= \left\{\sigma_1, \sigma_2, \ldots, \sigma_{i-1}, \sigma_{i+1}, \ldots, \sigma_N\right\}_{\circ}$

**最优反应策略**：给定策略组合 $\sigma$ ，玩家 $i$ 在终结局势下的收益记作 $u_i(\sigma)$ 。在给定其他玩家的策略组合 $\sigma_{-i}$ 的情况下，对玩家 $i$ 而言的最优反应策略 $\sigma_i^*$ 满足如下条件：$u_i\left(\sigma_i^*, \sigma_{-i}\right) \geq \max _{\sigma_i^{\prime} \in \Sigma_i} u_i\left(\sigma_i^{\prime}, \sigma_{-i}\right)$ 。这里 $\Sigma_i$ 是玩家 $i$ 可以选择的所有策略，如上条件表示当玩家 $i$ 采用最优反应策略时，玩家 $i$ 能够获得最大收益。

在策略组合 $\sigma^*$ 中，如果每个玩家的策略相对于其他玩家的策略而言都是最佳反应策略，那么策略组合 $\sigma^*$ 就是一个纳什均衡（Nash equilibrium）策略。在有限对手、有限策略情况下，纳什均衡一定存在。

即策略组 $\sigma^*=\left\{\sigma_1^*, \sigma_2^*, \ldots, \sigma_N^*\right\}$ 对任意玩家 $i=1, . ., N$ ，满足如下条件：
$$
u_i\left(\sigma^*\right) \geq \max _{\sigma_i^{\prime} \in \Sigma_i} \mu_i\left(\sigma_1^*, \sigma_2^*, \ldots, \sigma_i^{\prime}, \ldots, \sigma_N^*\right)
$$



遗憾最小化算法是一种根据以往博弈过程中所得遗憾程度来选择未来行为的方法。

玩家 $i$ 在过去 $T$ 轮中采取策略 $\sigma_i$ 的累加遗憾值定义如下：
$$
\operatorname{Regret}_i^T\left(\sigma_i\right)=\sum_{t=1}^T\left(u_i\left(\sigma_i, \sigma_{-i}^t\right)-u_i\left(\sigma^t\right)\right)
$$

其中 $\sigma^t$ 和 $\sigma_{-i}^t$ 分别表示第 $t$ 轮中所有玩家的策略组合和除了玩家 $i$ 以外的策略组合。简单地说，累加遗憾值代表着在过去 $T$ 轮中，玩家 $i$ 在每一轮中选择策略 $\sigma_i$ 所得收益与采取其他策略所得收益之差的累加。
有效遗憾值$\operatorname{Regret}_i^{T,+}\left(\sigma_i\right)=\max \left(\operatorname{Regret}_i^T\left(\sigma_i\right), 0\right)$

利用有效遗憾值的遗憾匹配可得到玩家 $i$ 在 $T$ 轮后第 $T+1$ 轮选择策略 $\sigma_i$ 的概率 $P\left(\sigma_i^{T+1}\right)$ 为：
$$
P\left(\sigma_i^{T+1}\right)=\left\{\begin{array}{cc}
\frac{\operatorname{Regret}_i^{T,+}\left(\sigma_i\right)}{\sum_{\sigma_i^{\prime} \in \Sigma_i} \operatorname{Regret}_i^{T,+}\left(\sigma_i^{\prime}\right)} & \text { if } \sum_{\sigma_i^{\prime} \in \Sigma_i} \operatorname{Regret}_i^{T,+}\left(\sigma_i^{\prime}\right)>0 \\
\frac{1}{\left|\Sigma_i\right|} & \text { otherwise }
\end{array}\right.
$$
$\left|\Sigma_i\right|$ 表示玩家 $i$ 所有策略的总数。显然，如果在过往 $T$ 轮中策略 $\sigma_i$ 所带来的遗憾值大、其他策略 $\sigma_i^{\prime}$ 所带来的遗憾值小，则在第 $T+1$ 轮选择策略 $\sigma_i$ 的概率值 $P\left(\sigma_i^{T+1}\right)$ 就大。也就是说，带来越大遗憾值的策略具有更高的价值，因此其在后续被选择的概率就应该越大。如果没有一个能够提升前 $T$ 轮收益的策略，则在后续轮次中随机选择一种策略。依照一定的概率选择行动是为了防止对手发现自己所采取的策略（如采取遗憾值最大的策略）。

石头剪刀布的例子：
![[Pasted image 20251203142828.png]]


虚拟遗憾最小化算法
在虚拟最小化算法的求解过程中，同样需要反复模拟多轮博弈来拟合最佳反应策略，算法步骤如下：
1）初始化遗憾值和累加策略表为 $\mathbf{0}$
2）采用随机选择的方法来决定策略
3）利用当前策略与对手进行博弈
4）计算每个玩家采取每次行为后的遗憾值
5）根据博弈结果计算每个行动的累加遗憾值大小来更新策略
6）重复3）到5）步若干次，不断的优化策略
7）根据重复博弈最终的策略，完成最终的动作选择

习题：在遗憾最小化算法中，玩家 i 按照如下方法来计算其在每一轮产生的悔恨值 
A、其他玩家策略不变，只改变玩家i的策略后，所产生的收益之差。
B、所有玩家策略均改变，所产生的收益之差。
C、至少改变 1 个以上玩家的策略，所产生的收益之差。
D、每个玩家策略不变，只改变收益函数，所产生的收益之差。
答案A


## 博弈规则设计
### 双边匹配问题
在生活中，人们常常会碰到与资源匹配相关的决策问题（如求职就业、报考录取等），这些需要双向选择的情况被称为是双边匹配问题。在双边匹配问题中，需要双方互相满足对方的需求才会达成匹配。

稳定婚姻问题（stable marriage problem）：典型的双匹配问题

该问题指在给定成员偏好顺序的情况下，为两组成员寻找稳定的匹配。假设有 $\boldsymbol{n}$ 个单身男性构成的集合 $\boldsymbol{M}= \left\{m_1, m_2, \ldots, m_n\right\}$ ，以及 $n$ 个单身女性构成的集合 $F=\left\{f_1, f_2, \ldots, f_n\right\}$ 。对于任意一名单身男性 $m_i$ ，都有自己爱慕的单身女性的顺序 $s_{m_i}:=f_{m_{i, 1}}>f_{m_{i, 2}}>\cdots>f_{m_{i, n}}$ ，这里 $f_{m_{i, j}}$ 表示第 $i$ 名男性所喜欢单身女性中排在第 $j$ 位的单身女性，同理对于任意一名单身女性 $f_i$ 也有其爱慕的单身男性顺序 $f_{f_i}:=m_{f_{i, 1}}>m_{f_{i, 2}}>\cdots>m_{f_{i, n}}, m_{f_{i, j}}$ 表示第 $i$ 名女性所喜欢单身男性中排在第 $j$ 位的单身男性。算法的最终目标是为这 $2 n$ 个男士和女士匹配得到 $n$ 对伴侣，每一对伴侣可以表示为 $\left(m_i, f_j\right)$ 。
假设有4名单身男性{1,2,3,4}和4名单身女性{A,B,C,D}，他（她）们的、爱慕序列如表7.10所示
![[Pasted image 20251203145943.png]]
1962年，美国数学家大卫·盖尔和博弈论学家沙普利提出了针对双边稳定匹配问题的解决算法（也被称为Gale- Shapely算法或G-S算法）应用于稳定婚姻问题的求解，算法过程如下：
1单身男性向最喜欢的女性表白
2所有收到表白的女性从向其表白男性中选择最喜欢的男性，暂时匹配
3未匹配的男性继续向没有拒绝过他的女性表白。收到表白的女性如果没有完成匹配，则从这一批表白者中选择最喜欢男性。即使收到表白的女性已经完成匹配，但是如果她认为有她更喜欢的男性，则可以拒绝之前的匹配者，重新匹配
4如此循环迭代，直到所有人都成功匹配为止
![[Pasted image 20251203152008.png]]

### 单边匹配问题
例如室友的匹配或者是座位的分配。这些问题中分配的对象都是不可分的标的物，他们只能属于一个所有者，且可以属于任何一个所有者。
![[Pasted image 20251203152049.png]]
对于这种单边匹配问题，1974年，沙普利和斯卡夫提出了针对单边匹配问题的稳定匹配算法“最大交易圈算法（Top-trading cycle，TTC）”，算法过程如下：

1)首先记录每个标的物的初始占有者，或者对物品进行随机分配。

2)每个交易者连接一条指向他最喜欢的标的物的边，并从每一个标的物连接到其占有者或是具有高优先权的交易者。

3)此时形成一张有向图，且必存在环，这种环被称为“交易圈”，对于交易圈中的交易者，将每人指向结点所代表的标的物赋予交易者，同时交易者放弃原先占有的标的物，占有者和匹配成功的标的物离开匹配市场。

4)接着从剩余的交易者和标的物之间重复进行交易圈匹配，直到无法形成交易圈，算法停止。
![[Pasted image 20251203152444.png]]
假设某寝室有A、B、C、D四位同学和1、2、3、4四个床位，当前给A、B、C、D四位同学随机分配4、3、2、1四个床位
在图7.5可以看出，A和D之间构成一个交易圈，可达成交易，所以A得到床位1，D得到床位4，之后将 A和D以及1和4从匹配图中移除。
从图7.6可以看出，B和C都希望得到床位2，无法再构成交易圈，但是由于C是床位的本身拥有者，所以C仍然得到床位2，B只能选择床位3 。


# 第八章 人工智能历史
符号主义（逻辑推理）、连接主义（神经网络）、行为主义（强化学习）
生成式人工智能



# 第九章 人工智能架构与系统

最基础的部分是人工智能芯片

运行系统可分为四个层次：芯片指令集标准、AI编译框架、关键算法与模型以及AI垂直领域开放创新平台。

![[Pasted image 20251203153325.png]]

人工智能芯片

图形处理器（GPU）
张量处理器（TPU）
可扩展处理器（XPU）
类脑芯片（Neuromorphic Chip）
特定领域芯片（Domain-Specific Chip）


人工智能系统
分布式神经网络训练算法与系统
是一种将神经网络训练任务分布在多台计算设备上并协同工作的方法。它通过将数据和计算任务划分为多个部分，分配给不同的计算节点并利用并行计算能力，加快神经网络的训练速度和性能。目前主流的并行算法主要包括数据并行、张量并行和流水线并行。