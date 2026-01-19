### 操作步骤

我们将分两步走：先启动“网络主机” (`atrust-vpn`)，再启动“环境客户端” (`pwn-env`) 并把它“挂”上去。

#### ➡️ 步骤一：启动 `atrust-vpn` 容器（网络主机）

这个容器的唯一使命就是**提供网络连接和挂载数据**。我们使用你之前用过的命令，确保它有一个固定的名字 (`atrust-vpn`)，并且挂载了你的工作目录。

1. **进入你存放脚本的目录**：
    
    Bash
    
    ```
    # 确保你在这个目录下
    cd ~/Desktop/lab1crypto/challenge2.4
    ```
    
2. **启动 `atrust-vpn` 容器**（如果它已经在运行，可以先 `docker stop atrust-vpn && docker rm atrust-vpn` 来确保一个干净的启动）：
    
    Bash
    
    ```
    docker run -d --restart unless-stopped --name atrust-vpn -v "$(pwd)":/work --device /dev/net/tun --cap-add NET_ADMIN -e PASSWORD=1234 -e URLWIN=1 -p 127.0.0.1:5901:5901 hagb/docker-atrust
    ```
    
    - **注意**：我把其他端口映射（`-p`）都去掉了，因为我们不再需要它们了，只保留 VNC 的 `5901` 端口。
        
    - `-v "$(pwd)":/work` 这个参数至关重要，它把你的脚本目录共享给了容器。
        
3. **连接 VNC 并登录 VPN**： 像以前一样，用 VNC 客户端连接 `127.0.0.1:5901`，然后在容器的桌面上**把 aTrust VPN 登录好**。这是关键一步，必须确保网络已经连通。
    

#### ➡️ 步骤二：启动 `pwn-env` 容器并“寄生”网络

现在，`atrust-vpn` 容器已经进入了内网。我们来启动你的 `pwn-env` 容器，并把它连接上去。

1. **运行 `pwn-env` 容器**： 在 Mac 终端里运行以下命令：
    
    Bash
    
    ```
    docker run -it --rm --network=container:atrust-vpn -v $(pwd):/work pwn-env:latest /bin/bash
    ``` 
    
    **命令解释（这是最关键的部分）：**
    
    - `docker run -it --rm ... pwn-env:latest /bin/bash`：这是启动你的 `pwn-env` 容器的标准方式，`--rm` 表示容器退出后自动删除，方便我们调试。
        
    - `--network=container:atrust-vpn`：**这就是魔法发生的地方！** 它告诉 Docker，这个新容器不要建立自己的网络，而是去**使用名为 `atrust-vpn` 的容器的网络**。
        
    - `--volumes-from atrust-vpn`：这是一个锦上添花的参数。它会自动把 `atrust-vpn` 容器上挂载的所有数据卷（也就是我们之前设置的 `/work` 目录）也**同样挂载到 `pwn-env` 容器里**。
        

#### ➡️ 步骤三：在 `pwn-env` 容器内运行脚本


http_proxy="" https_proxy="" pip3 install sympy -i https
://pypi.tuna.tsinghua.edu.cn/simple