---
draft: true
---


好的，完全理解。我们需要一个独立的、专注的测试脚本，它的唯一目的就是调用和验证 `ContinuityVisionSensor` 类中的 `detect_red_line` 方法。这样做的好处是隔离了问题，调试视觉算法时无需关心状态机等其他复杂逻辑。

下面是这个专门的测试脚本。

---

### **测试脚本 `test_vision.py`**

请在你的项目根目录 `ciame_robot/` 下创建一个新文件，命名为 `test_vision.py`。

**`test_vision.py` 文件内容:**

```python
# ciame_robot/test_vision.py

import cv2
import sys
import time

# 确保可以从当前目录导入我们自己编写的模块
# 这样即使从根目录运行 `python test_vision.py` 也能找到 continuity_camera_hardware
sys.path.append('.') 

from continuity_camera_hardware import ContinuityVisionSensor

# --- 测试配置 ---
CAMERA_DEVICE_INDEX = 0  # 你的iPhone摄像头的索引号

def run_vision_test():
    """
    专门用于测试 ContinuityVisionSensor 类的函数。
    """
    print("--- 视觉传感器测试程序 ---")
    print("正在初始化摄像头...")

    try:
        # 1. 实例化视觉传感器对象
        vision_sensor = ContinuityVisionSensor(camera_index=CAMERA_DEVICE_INDEX)
    except IOError as e:
        print(f"初始化失败: {e}")
        return

    print("\n摄像头已启动。请将红色物体放入视野中进行测试。")
    print("在弹出的摄像头窗口激活时，按 'q' 键退出测试。")
    print("-" * 20)

    # 用于计算帧率 (FPS)
    frame_count = 0
    start_time = time.time()

    try:
        while True:
            # 2. 核心：调用被测试的方法
            is_red_detected = vision_sensor.detect_red_line()
            
            # 3. 在终端打印清晰的测试结果
            if is_red_detected:
                print(">>> 结果: True  (检测到红色!)")
            else:
                print(">>> 结果: False (未检测到红色)")

            # 更新并显示帧率
            frame_count += 1
            elapsed_time = time.time() - start_time
            if elapsed_time > 1:
                fps = frame_count / elapsed_time
                print(f"    (FPS: {fps:.2f})")
                frame_count = 0
                start_time = time.time()
            
            # `detect_red_line` 内部已经包含了 cv2.waitKey(1)
            # 所以这里不需要额外的延时

    except KeyboardInterrupt:
        # `detect_red_line` 内部的 'q' 键会触发这个异常
        print("\n\n测试被用户手动停止。")
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
    finally:
        # 4. 确保在测试结束后释放资源
        print("正在关闭摄像头并释放资源...")
        vision_sensor.release()
        print("测试结束。")

if __name__ == "__main__":
    run_vision_test()
```

---

### **如何使用这个测试脚本**

1.  **保存文件：** 将上面的代码保存为 `ciame_robot/test_vision.py`。
2.  **连接手机：** 确保你的iPhone通过“连续互通”连接到Mac。
3.  **运行脚本：** 打开终端，确保你位于 `ciame_robot` 目录的 **上一级** 目录，然后运行：
    ```bash
    python ciame_robot/test_vision.py
    ```
    或者，如果你的终端已经在 `ciame_robot` 目录内，可以直接运行：
    ```bash
    python test_vision.py
    ```
4.  **进行测试和调试：**
    *   程序运行后，会弹出 "iPhone Camera (Continuity)" 和 "Red Mask" 两个窗口。
    *   **终端会实时、清晰地打印出 `detect_red_line` 方法每一帧的返回值 (`True` 或 `False`)。**
    *   现在，你可以专注于视觉调试了：
        *   拿一个红色物体，在**不同光线、不同距离、不同角度**下测试。
        *   观察 `Red Mask` 窗口的效果。如果效果不理想（比如红色物体上有黑洞，或者环境中有其他东西被误识别为红色），你就应该去修改 `continuity_camera_hardware.py` 文件。
        *   **主要调试的参数是：**
            *   `lower_red1`, `upper_red1`, `lower_red2`, `upper_red2`：调整这些HSV值，扩大或缩小红色的识别范围。
            *   `red_pixel_threshold`：如果小的红色噪点总是被识别，就调高这个值；如果目标红线离得很远时识别不到，就适当调低这个值。
    *   每次修改完 `continuity_camera_hardware.py` 后，只需重新运行 `test_vision.py` 即可立即看到效果，非常高效。
5.  **结束测试：**
    *   点击任意一个OpenCV的窗口，使其成为当前激活窗口。
    *   按下键盘上的 **`q`** 键，程序会优雅地退出，并自动关闭所有窗口和摄像头。

这个测试脚本为你提供了一个完美的沙箱环境，让你可以在不干扰主程序逻辑的情况下，把视觉识别功能打磨到最佳状态。