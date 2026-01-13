import numpy as np
from module import Conv2d, Sigmoid, MaxPool2d, AvgPool2d, Linear, ReLU, Tanh, CrossEntropyLoss
import struct
import glob
from tqdm import tqdm
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

# --- 以下的 load_mnist 和 LeNet5 類保持不變 ---

def load_mnist(path, kind='train'):
    """
    从指定路径加载MNIST数据集。
    :param path: 数据集所在的文件夹路径。
    :param kind: 'train' 表示加载训练集, 't10k' 表示加载测试集。
    :return: 返回包含图像和标签的元组。
    """
    image_path_pattern = os.path.join(path, f'{kind}*3-ubyte')
    label_path_pattern = os.path.join(path, f'{kind}*1-ubyte')
    try:
        image_path = glob.glob(image_path_pattern)[0]
        label_path = glob.glob(label_path_pattern)[0]
    except IndexError:
        print(f"错误：在路径 '{path}' 中找不到数据文件。请检查文件是否存在且路径正确。")
        exit()

    with open(label_path, "rb") as lbpath:
        magic, n = struct.unpack('>II', lbpath.read(8))
        labels = np.fromfile(lbpath, dtype=np.uint8)

    with open(image_path, "rb") as impath:
        magic, num, rows, cols = struct.unpack('>IIII', impath.read(16))
        images = np.fromfile(impath, dtype=np.uint8).reshape(len(labels), 28*28)
    return images, labels
    
class LeNet5:
    def __init__(self):
        self.conv1 = Conv2d(in_channels=1, out_channels=6, kernel_size=5, stride=1, padding=2)
        self.relu1 = ReLU()
        self.pool1 = AvgPool2d(kernel_size=2)
        self.conv2 = Conv2d(in_channels=6, out_channels=16, kernel_size=5)
        self.relu2 = ReLU()
        self.pool2 = AvgPool2d(kernel_size=2)
        self.fc1 = Linear(in_features=16*5*5, out_features=120)
        self.relu3 = ReLU()
        self.fc2 = Linear(in_features=120, out_features=84)
        self.relu4 = ReLU()
        self.fc3 = Linear(in_features=84, out_features=10)

    def forward(self, x):
        x = self.conv1.forward(x)
        x = self.relu1.forward(x)
        x = self.pool1.forward(x)
        x = self.conv2.forward(x)
        x = self.relu2.forward(x)
        x = self.pool2.forward(x)
        x = self.fc1.forward(x)
        x = self.relu3.forward(x)
        x = self.fc2.forward(x)
        x = self.relu4.forward(x)
        x = self.fc3.forward(x)
        return x

    def backward(self, dy, lr):
        dy = self.fc3.backward(dy, lr)
        dy = self.relu4.backward(dy)
        dy = self.fc2.backward(dy, lr)
        dy = self.relu3.backward(dy)
        dy = self.fc1.backward(dy, lr)
        dy = self.pool2.backward(dy)
        dy = self.relu2.backward(dy)
        dy = self.conv2.backward(dy, lr)
        dy = self.pool1.backward(dy)
        dy = self.relu1.backward(dy)
        dy = self.conv1.backward(dy, lr)

# --- 主程序部分 major changes here ---

if __name__ == '__main__':
    
    # --- 1. 数据加载 ---
    data_root = "MNIST-Dataset"
    train_path = os.path.join(data_root, "Train")
    print(f"正在从 '{train_path}' 加载训练数据...")
    train_images, train_labels = load_mnist(train_path, kind="train")
    test_path = os.path.join(data_root, "Test")
    print(f"正在从 '{test_path}' 加载测试数据...")
    test_images, test_labels = load_mnist(test_path, kind="t10k")
    print("数据加载完成。")

    # --- 2. 数据预处理 ---
    train_images_normalized = train_images.astype(np.float32) / 255.0
    test_images_normalized = test_images.astype(np.float32) / 255.0
    
    # --- 3. 初始化模型、损失函数和超参数 ---
    model = LeNet5()
    loss_fn = CrossEntropyLoss()
    epochs = 10
    batch_size = 64
    learning_rate = 0.001 # 根据上次讨论，使用一个较优的學習率

    # --- 4. 开始训练循环 ---
    print("\n🚀 开始训练...")
    # 用于存储每个epoch的历史记录，以供后续可视化
    history = {'loss': [], 'accuracy': []}

    for epoch in range(epochs):
        process_bar = tqdm(range(0, len(train_images_normalized), batch_size), desc=f"Epoch {epoch+1}/{epochs}")
        epoch_loss, correct_predictions, total_samples = 0.0, 0, 0
        
        permutation = np.random.permutation(len(train_images_normalized))
        train_images_shuffled = train_images_normalized[permutation]
        train_labels_shuffled = train_labels[permutation]

        for i in process_bar:
            batch_images = train_images_shuffled[i: i+batch_size]
            batch_labels = train_labels_shuffled[i: i+batch_size]
            batch_images = batch_images.reshape(-1, 1, 28, 28)

            predictions = model.forward(batch_images)
            loss = loss_fn.forward(predictions, batch_labels)
            epoch_loss += loss
            dy = loss_fn.backward() 
            model.backward(dy, learning_rate)

            predicted_labels_batch = np.argmax(predictions, axis=1)
            correct_predictions += np.sum(predicted_labels_batch == batch_labels)
            total_samples += len(batch_labels)
            process_bar.set_postfix(loss=f"{loss:.4f}", acc=f"{correct_predictions / total_samples:.4f}")

        avg_loss = epoch_loss / (len(train_images_normalized) / batch_size)
        epoch_accuracy = correct_predictions / total_samples
        history['loss'].append(avg_loss)
        history['accuracy'].append(epoch_accuracy)
        print(f"Epoch {epoch+1} 完成: 平均损失 = {avg_loss:.4f}, 训练准确率 = {epoch_accuracy:.4f}\n")

    # --- 5. 训练过程可视化 ---
    print("📈 正在生成训练过程可视化图表...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # 绘制损失曲线
    ax1.plot(range(1, epochs + 1), history['loss'])
    ax1.set_title('Training Loss vs. Epochs')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.grid(True)
    
    # 绘制准确率曲线
    ax2.plot(range(1, epochs + 1), history['accuracy'])
    ax2.set_title('Training Accuracy vs. Epochs')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Accuracy')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

    # --- 6. 在测试集上评估模型 ---
    print("\n🔬 开始在测试集上进行最终评估...")
    test_images_reshaped = test_images_normalized.reshape(-1, 1, 28, 28)
    test_predictions = model.forward(test_images_reshaped)
    predicted_labels = np.argmax(test_predictions, axis=1)
    accuracy = np.sum(predicted_labels == test_labels) / len(test_labels)
    print(f"✅ 测试完成! 最终测试准确率: {accuracy:.4f}")
    
    # --- 7. 详细模型评估分析 ---
    
    # 7.1 分类报告
    print("\n📊 分类报告:")
    # target_names 是为了在报告中显示类别名称
    target_names = [f'Digit {i}' for i in range(10)]
    print(classification_report(test_labels, predicted_labels, target_names=target_names))

    # 7.2 混淆矩阵
    print(" मैट्रिक्स (Confusion Matrix):")
    cm = confusion_matrix(test_labels, predicted_labels)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=range(10), yticklabels=range(10))
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()

    # 7.3 错误样本可视化
    misclassified_indices = np.where(predicted_labels != test_labels)[0]
    # 随机选择最多9个错误样本进行展示
    num_samples_to_show = min(len(misclassified_indices), 9)
    if num_samples_to_show > 0:
        print(f"\n🤔 随机展示 {num_samples_to_show} 个预测错误的样本:")
        random_indices = np.random.choice(misclassified_indices, num_samples_to_show, replace=False)
        
        plt.figure(figsize=(10, 10))
        for i, idx in enumerate(random_indices):
            plt.subplot(3, 3, i + 1)
            # 注意：这里我们使用未经归一化的原始图像 `test_images` 来显示，视觉效果更好
            plt.imshow(test_images[idx].reshape(28, 28), cmap='gray', interpolation='none')
            plt.title(f"True: {test_labels[idx]}, Pred: {predicted_labels[idx]}")
            plt.axis('off')
        plt.tight_layout()
        plt.show()
    else:
        print("\n🎉 恭喜！在测试集上没有发现错误样本！")