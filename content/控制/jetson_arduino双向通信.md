---
draft: false
---
先配置软件sudo /opt/nvidia/jetson-io/jetson-io.py
![[Pasted image 20250921154955.png]]
选第一个40pin header
![[Pasted image 20250921155043.png]]
把最后的uarta-cts/rts选上，确认重启。
代码
jetson端
```python
import serial
import time

try:
    # 使用我们已知的端口和波特率初始化串口
    # timeout参数很重要，它决定了 readline() 函数最多等待多少秒
    ser = serial.Serial('/dev/ttyCH341USB0', 9600, timeout=1)
    print("Serial port /dev/ttyCH341USB0 opened successfully.")
    time.sleep(2) # 等待Arduino重启和初始化
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

try:
    while True:
        # --- 发送部分 ---
        command = 's'
        print(f"Sending command to Arduino: '{command}'")
        # 将指令字符编码为字节并发送
        ser.write(command.encode('utf-8'))

        # --- 接收部分 ---
        # 等待Arduino的回应
        # ser.in_waiting 会返回接收缓冲区中的字节数
        if ser.in_waiting > 0:
            # 读取一行数据，解码成字符串，并去掉末尾的换行符
            response = ser.readline().decode('utf-8').rstrip()
            print(f"Received response from Arduino: '{response}'")
        else:
            print("No response from Arduino (timeout).")

        # 每隔3秒循环一次
        print("---------------------------------")
        time.sleep(3)

except KeyboardInterrupt:
    print("\nExiting program.")
finally:
    # 确保程序退出时关闭串口
    ser.close()
    print("Serial port closed.")


```
arduino端
```c
/*
  Arduino 双向通信代码
  功能：
  1. 监听来自Jetson的串口指令。
  2. 当接收到字符 's' 时，执行一个动作（例如打印信息）。
  3. 执行动作后，向Jetson回送一条确认消息。
*/

// 定义板载LED引脚，方便我们进行可视化调试
const int ledPin = LED_BUILTIN; 

void setup() {
  // 初始化串口通信，波特率必须与 Jetson 的 Python 脚本一致 (9600)
  Serial.begin(9600);
  
  // 将LED引脚设置为输出模式
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // 初始状态关闭LED

  // 打印一条准备就绪的消息
  Serial.println("Arduino is ready for commands...");
}

void loop() {
  // 检查串口缓冲区中是否有可读的数据
  if (Serial.available() > 0) {
    // 读取接收到的单个字符
    char command = Serial.read();

    // 判断接收到的指令是否为 's'
    if (command == 's') {
      // 1. 在串口监视器中打印一条消息，用于我们自己调试
      Serial.println("Command 's' received.");

      // 2. 让LED闪烁一下，提供一个直观的反馈
      digitalWrite(ledPin, HIGH);
      delay(100);
      digitalWrite(ledPin, LOW);

      // 3. 向Jetson回送一条确认消息。
      //    Python脚本使用的是readline()，所以我们必须用println()来发送，
      //    以确保消息以换行符结尾。
      Serial.println("OK: Command processed.");
    }
  }
}


```

result
![[Pasted image 20250920192903.png]]