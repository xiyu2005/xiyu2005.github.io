---
title: lab3Misc
tags:
  - CTF
  - Misc
draft: false
---

```python
# 创建一个不带预训练权重的空模型
model = M.resnet18(weights=None).eval().to(device)
# 定义模型文件在容器内的绝对路径
model_path = "/work/homework3/deploy-lightweight/resnet18-f37072fd.pth"
# 从该路径强制加载权重
model.load_state_dict(torch.load(model_path))

```

# Homework3：鲁棒性对抗样本生成

## 摘要

本次挑战的目标是绕过一个基于深度学习模型（ResNet-18）的图片验证系统。该系统要求上传的图片在像素上与原图差异极小（$L_{infty}$ 范数限制），同时要求图片在经过多次随机的图像变换后，仍能被模型以高置信度分类为指定的目标类别。本报告详细记录了从环境分析、PoW 机制破解，到对抗样本攻击算法的迭代优化，最终成功生成一个鲁棒的对抗样本并获取 Flag 的全过程。核心技术采用了**期望变换（EOT）思想，通过梯度平均**的方法生成了能够抵抗随机裁剪和翻转的对抗性扰动。

---

## 1. 题目分析

服务器端的核心逻辑由 `challenge.py` 实现，其验证流程如下：

1. **接收图片**: 接收用户以 Base64 形式上传的图片。
    
2. **扰动校验**: 计算上传图片与服务器端 `img.png` 的最大像素差值 `max_diff`。如果 `max_diff > 6`，则程序退出。这是一个非常严格的 L_infty 范数限制，要求我们的修改在视觉上几乎不可察觉。
    
3. **鲁棒性验证**: 程序会进行一个 5 轮的循环。在**每一轮**循环中，都会对用户上传的图片进行一次**新的、随机的**变换（`RandomResizedCrop` 和 `RandomHorizontalFlip`），然后送入 ResNet-18 模型进行分类。
    
4. **分类结果校验**: 每一轮都必须满足：
    
    - 预测置信度最高的类别必须是 **107** (ImageNet中的“披萨”)。
        
    - 该预测的置信度必须**大于 0.95**。
        
5. **获取 Flag**: 只有连续 5 轮测试全部通过，服务器才会返回 Flag。
    

**核心挑战**: 制作一个对抗样本，它不仅要骗过模型一次，还要在随机的数据增强（裁剪、翻转）下稳定地骗过模型 5 次。

---

## 2. 解题历程与思路演进

整个解题过程充满了挑战，我们通过逐步排查和迭代，最终定位并解决了所有问题。

1. **环境与依赖问题**: 最初，我们在本地运行脚本时遇到了各种问题，包括：
    
    - 缺少模型权重文件 (`resnet18-f37072fd.pth`)。
        
    - 容器内无法联网，导致无法自动下载权重，也无法安装 `hashcash` 等工具。
        
    - **解决方案**: 通过手动下载权重文件，并修改代码从本地加载，解决了离线环境的问题。
        
2. **PoW 挑战与网络超时**:
    
    - 最初，我们花费了大量时间调试 `EOFError` 和 `BrokenPipeError`。
        
    - 通过独立的 `pow.py` 脚本测试，我们证明了 PoW 算法本身是正确的。
        
    - 最终我们定位到问题的根源：**服务器存在 30 秒的 PoW 超时**。而我们最初的脚本流程是“先生成图片（耗时），再连接服务器”，这导致 PoW 必然超时。
        
    - **解决方案**: 重构代码执行流程为 **“先连接服务器 -> 快速完成 PoW -> 再生成图片 -> 最后发送图片”**。这又导致了服务器的“空闲超时”。最终确定了**“先离线生成图片 -> 再在线完成所有交互”** 的最优流程。
	- 其次还使用了多线程优化pow算法防止超时
```python
# --- PoW 求解器 (多进程加速版) ---
def pow_worker(args):
    start_counter, chunk_size, bits, resource, date, rand, target = args
    ver = "1"; ext = ""
    for counter in range(start_counter, start_counter + chunk_size):
        b64_counter = base64.b64encode(str(counter).encode()).decode().strip("=")
        token = f"{ver}:{bits}:{date}:{resource}:{ext}:{rand}:{b64_counter}"
        h = hashlib.sha1(token.encode()).digest()
        if int.from_bytes(h, 'big') < target:
            return token.encode()
    return None

def solve_hashcash_fast(bits, resource):
    log.info(f"正在为资源 '{resource}' 进行多进程并行计算 ({bits}位 PoW)...")
    date = datetime.now(timezone.utc).strftime('%y%m%d')
    rand = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    target = 2**(160 - bits)
    num_processes = mp.cpu_count()
    log.info(f"启动 {num_processes} 个工作进程...")
    chunk_size = 1000000
    pool = mp.Pool(processes=num_processes)
    start_counter = 0
    while True:
        args_list = [(start_counter + i * chunk_size, chunk_size, bits, resource, date, rand, target) for i in range(num_processes)]
        for result in pool.imap_unordered(pow_worker, args_list):
            if result:
                log.success(f"成功找到 Token: {result.decode()}")
                pool.terminate()
                return result
        start_counter += num_processes * chunk_size
```
1. **对抗攻击算法的迭代**:
    
    - **初步攻击失败**: 最初的 PGD 攻击生成的图片 `Loss` 值很高，无法骗过模型，导致服务器返回的 `max_diff` 为 0，分类结果错误。
        
    - **`max_diff` 边界问题**: 当攻击生效后，我们遇到了 `max_diff` 恰好为 7 的情况。这是由于浮点数到整数的取整误差导致的。通过将扰动上限从 `6.0` 调整为 `5.8`，我们成功地为取整误差留出了安全边际。![[Pasted image 20250731215820.png]]
        
    - **鲁棒性不足**: 解决了 `max_diff` 问题后，我们成功通过了 `round=0`，但失败在了 `round=1`。这证明了我们的攻击虽然有效，但不够鲁棒，无法抵抗所有的随机变换。
        

---

## 3. 核心代码详解：`generate_adversarial_image`

为了解决最终的鲁棒性问题，我们采用了基于**梯度平均的期望变换（EOT）**策略。这是最终成功的核心代码，其设计思路如下：
### 关键理论与数学公式

本次攻击的核心是投影梯度下降 (Projected Gradient Descent, PGD) 攻击，并结合了期望变换 (Expectation Over Transformation, EOT) 的思想来确保其鲁棒性。

**目标函数 (Loss Function)**

我们的目标是生成一张图片 $X_{adv}$，使得模型 $f$ 对它的预测结果为目标类别 $y_{target}$ 的置信度最高。这等价于最大化该类别的 Logit 值 $Z_{y_{target}}$。在优化中，我们通过最小化其负值来实现：

$$\text{minimize} \quad L(X_{adv}, y_{target}) = -Z_{y_{target}}(X_{adv})$$

**投影梯度下降 (PGD)**

PGD 是一种迭代攻击方法。在第 $t+1$ 步，它在上一步的对抗样本 $X_{adv}^{(t)}$ 基础上，朝着能使损失函数减小的方向（梯度的反方向）前进一小步，然后通过一个投影函数 $\Pi$ 将结果拉回到允许的扰动范围内。

$$X_{adv}^{(t+1)} = \Pi_{X, \epsilon} \left( X_{adv}^{(t)} - \alpha \cdot \text{sign}(\nabla_{X} L(X_{adv}^{(t)}, y_{target})) \right)$$

- $X_{adv}^{(t)}$ 是第 $t$ 次迭代的对抗样本。
- $\alpha$ 是步长（Learning Rate）。
- $\nabla_{X}L$ 是损失函数对输入图片的梯度。
- $\Pi_{X,\epsilon}$ 是投影操作，它确保 $X_{adv}^{(t+1)}$ 与原始图片 $X$ 之间的最大像素差值（L_infty 范数）不超过 $\epsilon$。在代码中，这通过 `clamp` 操作实现。

**期望变换 (EOT)**

为了让攻击能抵抗随机变换 $t \in \mathcal{T}$（如随机裁剪、翻转），我们优化的目标不是针对单个变换后的损失，而是所有可能变换下的期望损失。在实践中，我们通过在每一步迭代中采样 $N$ 个随机变换，并计算其梯度的平均值来近似这个期望：

$$\nabla_{X_{adv}} \approx \frac{1}{N} \sum_{i=1}^{N} \nabla_{X_{adv}} L(t_i(X_{adv}), y_{target})$$

在我们的代码中，这个思想通过在每次迭代中对 `adv_tensor_full_size` 进行多次独立的随机变换，并累加其梯度来实现。


```python
import torchvision.transforms.functional as F

def generate_adversarial_image(original_image_path):
    # --- 1. 定义超参数 ---
    TARGET_CLASS_ID = 107
    MAX_PIXEL_DIFF = 5.8  # 留出安全边际以满足 max_diff <= 6
    PERTURBATION_LIMIT = MAX_PIXEL_DIFF / 255.0 # 将扰动范围归一化
    ITERATIONS = 300      # 攻击迭代总轮数
    LEARNING_RATE = 5e-4  # 更新步长
    
    # --- 2. 初始化 ---
    log.info("开始在本地生成鲁棒对抗样本...")
    device = torch.device("cpu")
    model = M.resnet18(weights=M.ResNet18_Weights.IMAGENET1K_V1).eval().to(device)
    
    image_pil = Image.open(original_image_path).convert("RGB")
    image_tensor_orig = T.ToTensor()(image_pil).to(device)

    # 关键：我们优化的不是图片本身，而是这个与原图尺寸相同的“扰动量”delta
    delta = torch.zeros_like(image_tensor_orig, requires_grad=True)
    optimizer = torch.optim.Adam([delta], lr=LEARNING_RATE)
    norm_transform = T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    
    # --- 3. PGD 迭代优化 ---
    for i in range(ITERATIONS):
        optimizer.zero_grad()

        # 4. 【核心】手动实现可微分的随机变换
        # 我们不能用 T.Compose，因为它会破坏计算图
        
        # 4.1. 将当前扰动添加到原始图片上，得到一个“临时”的对抗图片
        adv_tensor_full_size = (image_tensor_orig + delta).clamp(0, 1)

        # 4.2. 手动获取该轮随机裁剪和翻转的参数
        crop_params = T.RandomResizedCrop.get_params(adv_tensor_full_size, scale=(0.08, 1.0), ratio=(3.0/4.0, 4.0/3.0))
        is_flipped = torch.rand(1) < 0.5
        
        # 4.3. 使用 functional API 应用变换，这能保持计算图的连续性
        adv_tensor_cropped = F.resized_crop(adv_tensor_full_size, *crop_params, size=[224, 224])
        if is_flipped:
            adv_tensor_cropped = F.hflip(adv_tensor_cropped)

        # 4.4. 归一化，准备输入模型
        adv_input_normalized = norm_transform(adv_tensor_cropped)

        # 5. 计算损失函数
        output = model(adv_input_normalized.unsqueeze(0))
        # 我们的目标是让类别107的输出值最大化，等价于最小化它的负值
        loss = -output[0][TARGET_CLASS_ID]
        
        # 6. 反向传播，计算梯度并更新 delta
        loss.backward()
        optimizer.step()
        
        # 7. 扰动投影：确保 delta 的每个像素值的变动都不超过限制
        delta.data.clamp_(-PERTURBATION_LIMIT, PERTURBATION_LIMIT)

        if (i + 1) % 50 == 0:
            log.info(f"生成进度 [{i+1}/{ITERATIONS}], Loss: {loss.item():.4f}")

    # --- 8. 生成并返回最终图片 ---
    log.info("扰动计算完毕，正在生成最终图片...")
    # 将最终优化好的扰动 delta 加到原始图片上
    final_adv_tensor = (image_tensor_orig + delta.detach()).clamp(0, 1)
    final_adv_image_pil = T.ToPILImage()(final_adv_tensor.cpu())
    log.success("对抗样本生成完毕!")
    return final_adv_image_pil
```

![[Pasted image 20250731204012.png]]




![[Pasted image 20250731215511.png]]![[Pasted image 20250731221545.png]]