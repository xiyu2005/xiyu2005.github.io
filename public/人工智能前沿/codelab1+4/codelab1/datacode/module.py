import numpy as np
from numba import njit # 1. 導入 njit
# 为了加速卷积和池化操作，定义两个辅助函数
# im2col: 将多通道的图像区块（感受野）转换为矩阵的列，从而将卷积运算转换为矩阵乘法
@njit
def im2col(image, kernel_h, kernel_w, stride):
    N, C, H, W = image.shape
    out_h = (H - kernel_h) // stride + 1
    out_w = (W - kernel_w) // stride + 1
    
    col = np.zeros((N, C, kernel_h, kernel_w, out_h, out_w))
    
    for y in range(kernel_h):
        y_max = y + stride*out_h
        for x in range(kernel_w):
            x_max = x + stride*out_w
            col[:, :, y, x, :, :] = image[:, :, y:y_max:stride, x:x_max:stride]
            
    # ★★★ 修正點 ★★★
    # 在 transpose() 和 reshape() 之間加上 .copy()
    col = col.transpose(0, 4, 5, 1, 2, 3).copy().reshape(N*out_h*out_w, -1)
    return col

@njit
def col2im(col, input_shape, kernel_h, kernel_w, stride):
    N, C, H, W = input_shape
    out_h = (H - kernel_h) // stride + 1
    out_w = (W - kernel_w) // stride + 1
    
    # ★★★ 修正點 ★★★
    # 同样地，在 transpose() 後加上 .copy() 是一個好習慣，確保後續操作的穩定性
    col = col.reshape(N, out_h, out_w, C, kernel_h, kernel_w).transpose(0, 3, 4, 5, 1, 2).copy()
    
    img = np.zeros((N, C, H + stride - 1, W + stride - 1), dtype=col.dtype)
    for y in range(kernel_h):
        y_max = y + stride*out_h
        for x in range(kernel_w):
            x_max = x + stride*out_w
            img[:, :, y:y_max:stride, x:x_max:stride] += col[:, :, y, x, :, :]
            
    return img[:, :, 0:H, 0:W]

class Conv2d:
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int, 
                 stride: int = 1, padding: int = 0, dtype = None):
        """
        初始化卷积层
        :param in_channels: 输入特征图的通道数
        :param out_channels: 输出特征图的通道数 (即卷积核的数量)
        :param kernel_size: 卷积核的尺寸
        :param stride: 步长
        :param padding: 填充
        """
        self.C_in = in_channels
        self.C_out = out_channels
        self.K = kernel_size
        self.S = stride
        self.P = padding
        
        # 使用He初始化/Kaiming初始化，有助于防止梯度消失/爆炸
        # 权重形状: (输出通道数, 输入通道数, 核高, 核宽)
        self.weight = np.random.randn(self.C_out, self.C_in, self.K, self.K) * np.sqrt(2. / (self.C_in * self.K * self.K))
        # 偏置形状: (输出通道数, 1)
        self.bias = np.zeros((self.C_out, 1))
        
        # 初始化梯度
        self.w_grad = None
        self.b_grad = None
        # 缓存前向传播的输入，用于反向传播计算
        self.x = None
        self.col = None
        self.col_w = None
        
    def forward(self, x):
        """
        执行前向传播
        x - 输入数据，形状 (N, C, H, W)
        返回 - 卷积结果，形状 (N, O, H', W')
        """
        self.x = x
        N, C, H, W = x.shape
        # 计算输出特征图的尺寸
        out_h = (H + 2*self.P - self.K) // self.S + 1
        out_w = (W + 2*self.P - self.K) // self.S + 1

        # 对输入进行填充(padding)
        # np.pad的格式是((dim0_pad_before, dim0_pad_after), (dim1_pad_before, ...))
        x_padded = np.pad(x, ((0,0), (0,0), (self.P, self.P), (self.P, self.P)), 'constant')

        # 使用im2col将输入和卷积核展开为矩阵
        self.col = im2col(x_padded, self.K, self.K, self.S)
        self.col_w = self.weight.reshape(self.C_out, -1).T # (C_in*K*K, C_out)
        
        # 核心计算：将卷积操作转换为矩阵乘法
        out = np.dot(self.col, self.col_w) + self.bias.T # (N*H'*W', C_out)
        
        # 将输出结果重塑为标准的图像格式 (N, H', W', C_out) -> (N, C_out, H', W')
        out = out.reshape(N, out_h, out_w, -1).transpose(0, 3, 1, 2)
        
        return out

    def backward(self, dy, lr):
        """
        执行反向传播和参数更新
        :param dy: 来自下一层的梯度，形状 (N, C_out, H', W')
        :param lr: 学习率
        :return: 传给上一层的梯度 dx，形状 (N, C_in, H, W)
        """
        N, C_out, H_out, W_out = dy.shape
        
        # 1. 计算偏置的梯度 self.b_grad
        self.b_grad = np.sum(dy, axis=(0, 2, 3)).reshape(self.C_out, 1)

        # 2. 计算权重的梯度 self.w_grad
        # dy 形状转换 (N, C_out, H', W') -> (N, H', W', C_out) -> (N*H'*W', C_out)
        dy_reshaped = dy.transpose(0, 2, 3, 1).reshape(-1, self.C_out)
        # self.col.T @ dy_reshaped = (C_in*K*K, N*H'*W') @ (N*H'*W', C_out) -> (C_in*K*K, C_out)
        self.w_grad = np.dot(self.col.T, dy_reshaped)
        # 转换回原始权重形状 (C_out, C_in, K, K)
        self.w_grad = self.w_grad.transpose(1, 0).reshape(self.C_out, self.C_in, self.K, self.K)

        # 3. 计算传给上一层的梯度 dx
        # dy_reshaped @ self.col_w.T = (N*H'*W', C_out) @ (C_out, C_in*K*K) -> (N*H'*W', C_in*K*K)
        d_col = np.dot(dy_reshaped, self.col_w.T)
        # 使用 col2im 将梯度还原为输入图像的形状
        # 注意：这里的input_shape需要考虑padding
        H_padded, W_padded = self.x.shape[2] + 2*self.P, self.x.shape[3] + 2*self.P
        dx_padded = col2im(d_col, (N, self.C_in, H_padded, W_padded), self.K, self.K, self.S)
        # 去掉padding部分
        dx = dx_padded[:, :, self.P:self.x.shape[2]+self.P, self.P:self.x.shape[3]+self.P]

        # 4. 更新权重和偏置
        self.weight -= lr * self.w_grad
        self.bias -= lr * self.b_grad
        
        return dx


# ------------------------------ 激活函数 ------------------------------

class ReLU:
    def __init__(self):
        self.mask = None # 用于记录输入中 > 0 的位置

    def forward(self, x):
        self.mask = (x > 0)
        return x * self.mask # np.maximum(0, x)
      
    def backward(self, dy):
        # 梯度只通过那些在前向传播中大于0的元素
        return dy * self.mask

class Tanh:
    def __init__(self):
        self.y = None # 缓存前向传播的输出

    def forward(self, x):
        self.y = np.tanh(x)
        return self.y
       
    def backward(self, dy):
        # tanh的导数是 1 - tanh^2(x)
        return dy * (1 - self.y**2)
        
class Sigmoid:
    def __init__(self):
        self.y = None # 缓存前向传播的输出

    def forward(self, x):
        self.y = 1 / (1 + np.exp(-x))
        return self.y
       
    def backward(self, dy):
        # sigmoid的导数是 y * (1 - y)
        return dy * self.y * (1 - self.y)

# ------------------------------ 池化层 ------------------------------

class MaxPool2d:
    def __init__(self, kernel_size: int, stride = None, padding = 0):
        self.K = kernel_size
        self.S = stride if stride is not None else kernel_size
        self.P = padding # 注意：numpy实现的池化通常不支持padding，这里为保持API一致性
        self.x = None
        self.arg_max = None # 记录最大值的位置

    def forward(self, x):
        self.x = x
        N, C, H, W = x.shape
        out_h = (H - self.K) // self.S + 1
        out_w = (W - self.K) // self.S + 1

        # 使用im2col技巧
        col = im2col(x, self.K, self.K, self.S)
        col = col.reshape(-1, self.K * self.K)

        # 找到每行（每个窗口）的最大值及其索引
        self.arg_max = np.argmax(col, axis=1)
        out = np.max(col, axis=1)
        
        # 重塑输出
        out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)
        return out

    def backward(self, dy):
        # 将dy的形状从(N, C, H', W') -> (N*H'*W', C) -> (N*H'*W'*C)
        dy_flat = dy.transpose(0, 2, 3, 1).flatten()
        
        # 准备一个用于放置梯度的矩阵，形状和im2col的输出一致
        d_col = np.zeros((len(self.arg_max), self.K * self.K))
        # 将梯度dy放置到前向传播时最大值所在的位置
        d_col[np.arange(len(self.arg_max)), self.arg_max] = dy_flat
        
        # 使用col2im将梯度还原回输入图像的形状
        dx = col2im(d_col, self.x.shape, self.K, self.K, self.S)
        return dx
     
class AvgPool2d:
    def __init__(self, kernel_size: int, stride = None, padding = 0):
        self.K = kernel_size
        self.S = stride if stride is not None else kernel_size
        self.P = padding
        self.x_shape = None

    def forward(self, x):
        """
        x - shape (N, C, H, W)
        return the result of AvgPool2d with shape (N, C, H', W')
        """
        self.x_shape = x.shape
        N, C, H, W = x.shape
        out_h = (H - self.K) // self.S + 1
        out_w = (W - self.K) // self.S + 1
        
        # 使用im2col将输入数据展开
        col = im2col(x, self.K, self.K, self.S) # shape: (N*H'*W', C*K*K)
        
        # --- 修正部分 ---
        # 将展开的数据重塑，把通道(C)和窗口内的元素(K*K)分开
        col_reshaped = col.reshape(N * out_h * out_w, C, self.K * self.K)
        
        # 沿窗口元素维度(axis=2)计算平均值，保留通道维度
        out = np.mean(col_reshaped, axis=2) # shape: (N*H'*W', C)
        # --- 修正结束 ---

        # 将输出重塑为 (N, H', W', C)，再转换为 (N, C, H', W')
        out = out.reshape(N, out_h, out_w, C).transpose(0, 3, 1, 2)
        return out

    def backward(self, dy):
        """
        dy - shape (N, C, H', W')
        return the result of gradient dx with shape (N, C, H, W)
        """
        N, C, H_out, W_out = dy.shape
        
        # --- 修正部分 ---
        # 将传入的梯度dy重塑为 (N*H'*W', C)
        dy_reshaped = dy.transpose(0, 2, 3, 1).reshape(-1, C)

        # 准备一个用于放置梯度的矩阵，形状为 (N*H'*W', C, 1)
        d_col = dy_reshaped[:, :, np.newaxis]
        
        # 将梯度复制K*K次并除以窗口大小，以分发梯度
        d_col = np.repeat(d_col, self.K * self.K, axis=2) # shape: (N*H'*W', C, K*K)
        d_col /= (self.K * self.K)

        # 重塑回col2im期望的二维形状
        d_col = d_col.reshape(-1, C * self.K * self.K) # shape: (N*H'*W', C*K*K)
        # --- 修正结束 ---

        # 使用col2im将梯度还原回输入图像的形状
        dx = col2im(d_col, self.x_shape, self.K, self.K, self.S)
        return dx
# ------------------------------ 全连接层和损失函数 ------------------------------

class Linear:
    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        self.in_features = in_features
        self.out_features = out_features
        
        # He/Kaiming 初始化
        self.weight = np.random.randn(in_features, out_features) * np.sqrt(2. / in_features)
        self.bias = np.zeros((1, out_features)) if bias else None

        self.w_grad = None
        self.b_grad = None
        self.x = None
        self.x_shape = None

    def forward(self, x):
        # 缓存输入和其原始形状
        self.x = x
        self.x_shape = x.shape
        
        # 如果输入是多维的（如来自卷积层），则将其展平
        if x.ndim > 2:
            batch_size = x.shape[0]
            self.x = x.reshape(batch_size, -1)
            # 断言确保展平后的特征数量与期望的in_features匹配
            assert self.x.shape[1] == self.in_features, \
                f"Input feature size mismatch. Expected {self.in_features}, got {self.x.shape[1]}"

        # 核心计算
        out = np.dot(self.x, self.weight)
        if self.bias is not None:
            out += self.bias
        return out

    def backward(self, dy, lr):
        # 1. 计算梯度
        self.w_grad = np.dot(self.x.T, dy)
        if self.bias is not None:
            self.b_grad = np.sum(dy, axis=0, keepdims=True)
        
        # 2. 更新权重
        self.weight -= lr * self.w_grad
        if self.bias is not None:
            self.bias -= lr * self.b_grad

        # 3. 计算传给上一层的梯度dx
        dx = np.dot(dy, self.weight.T)
        
        # 将dx的形状还原为输入的原始形状
        return dx.reshape(self.x_shape)

class CrossEntropyLoss:
    def __init__(self):
        self.probs = None  # 缓存softmax的输出概率
        self.label = None  # 缓存真实标签

    def forward(self, x, label):
        """
        计算交叉熵损失
        :param x: 模型的原始输出（logits），形状 (N, num_classes)
        :param label: 真实标签，形状 (N,)
        """
        self.label = label
        N = x.shape[0]
        
        # 1. Softmax: 将logits转换为概率
        # 为了数值稳定性，先减去每行的最大值（log-sum-exp trick）
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        self.probs = exp_x / np.sum(exp_x, axis=1, keepdims=True)
        
        # 2. 计算交叉熵损失
        # 从概率矩阵中只取出真实标签对应的概率
        log_probs = -np.log(self.probs[np.arange(N), label] + 1e-9) # 加一个极小值防止log(0)
        
        loss = np.sum(log_probs) / N
        return loss

    def backward(self):
        """
        计算损失函数对模型输出x的梯度
        """
        N = self.probs.shape[0]
        
        # 交叉熵损失对softmax输入的梯度有一个非常简洁的形式: probs - y_true
        # 首先，我们需要将真实标签转换为one-hot编码
        y_true = np.zeros_like(self.probs)
        y_true[np.arange(N), self.label] = 1
        
        # 计算梯度，并除以批大小N以匹配损失的平均值
        dx = (self.probs - y_true) / N
        
        return dx
    

class ResidualBlock:
    def __init__(self, in_channels, out_channels, stride=1):
        """
        初始化殘差塊。
        :param in_channels: 輸入通道數
        :param out_channels: 輸出通道數
        :param stride: 第一个卷积层的步长，用于控制尺寸缩小
        """
        self.stride = stride
        
        # 主要路徑 (Main Path)
        self.conv1 = Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1)
        self.relu1 = ReLU()
        self.conv2 = Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1)
        
        # 捷徑/短路 (Shortcut Path)
        # 如果維度不匹配 (步長不為1导致尺寸变化，或通道数改变)，
        # 我們需要一個1x1的卷積層來使它們的維度一致，以便相加。
        if stride != 1 or in_channels != out_channels:
            self.shortcut = Conv2d(in_channels, out_channels, kernel_size=1, stride=stride)
        else:
            self.shortcut = None # 维度相同时，捷徑是恆等映射，無需額外層
            
        self.relu2 = ReLU()

    def forward(self, x):
        """定義前向傳播"""
        identity = x # 保存原始輸入，用於捷徑連接

        # 1. 訊號通過主要路徑
        out = self.conv1.forward(x)
        out = self.relu1.forward(out)
        out = self.conv2.forward(out)
        
        # 2. 訊號通過捷徑
        if self.shortcut is not None:
            identity = self.shortcut.forward(x)
            
        # 3. 將主路徑的輸出與捷徑的輸出相加 (殘差連接的核心)
        out += identity
        out = self.relu2.forward(out) # 最後通過激活函數
        return out

    def backward(self, dy, lr):
        """定義反向傳播"""
        # 梯度首先通過最後的激活函數
        dy = self.relu2.backward(dy)
        
        # 梯度在此處被複製，一份流向主路徑，一份流向捷徑
        d_main = dy
        d_shortcut = dy
        
        # 梯度沿主路徑反向傳播
        dx_main = self.conv2.backward(d_main, lr)
        dx_main = self.relu1.backward(dx_main)
        dx_main = self.conv1.backward(dx_main, lr)
        
        # 梯度沿捷徑反向傳播
        dx_shortcut = d_shortcut # 默認梯度
        if self.shortcut is not None:
            dx_shortcut = self.shortcut.backward(d_shortcut, lr)

        # 最終的梯度是兩條路徑梯度之和
        return dx_main + dx_shortcut