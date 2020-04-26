# 虚拟机安装Linux操作系统 
李笑来老师在直播中提到，虚拟机安装Ubuntu操作系统学习的事情，这对大多数初学者来说或许是一个门槛。碰巧我刚刚更新了一下自己虚拟机，把详细步骤记录下来，分享给你，希望对你有一点帮助。

## 环境与背景  
我宿主机操作系统是win10，虚拟机用的是VirtualBox，虚拟机中安装Ubuntu server，安装后配置ssh服务，然后用SecureCRT和WinSCP远程操作虚拟机中的Ubuntu系统。

[VirtualBox：](https://www.virtualbox.org/wiki/Downloads) 是一款好用免费的虚拟机，提供虚拟操作系统运行所需要的环境，能满足你绝大多数的需求；类似的虚拟机还有功能更强大的付费软件 [VMware](https://www.vmware.com/cn.html)。   
**注意：安装VirtualBox后，记得把 [Extension Pack](https://www.virtualbox.org/wiki/Downloads) 也一起装上。**  

[Ubuntu：](https://ubuntu.com/) 著名的Linux操作系统发行版，主流版本分为 [Ubuntu Desktop](https://ubuntu.com/download/desktop) 和 [Ubuntu Server](https://ubuntu.com/download/server)。Desktop 版和 Windows 一样是面向终端用户的窗口视图操作系统，硬件配置(CPU 2GHz, 内存 4G等)要求较高；Server 版是面向服务器应用的命令行操作系统，不需要终端渲染，所以硬件要求相对不高。   
我的宿主机没有足够资源分配给虚拟机，同时我安装 Ubuntu 的目的是服务器的操作和命令行操作系统的学习，所以选择 server 版。当然也可以选择 CentOS (Linux的另一个主流发行版) 来学习Linux服务器操作。 

[SSH服务：](https://www.ssh.com/) 是远程安全链接服务，通过[非对称加密](https://reader.seaky.club/posts/71bbf6bd85beb9e08da2c65e66ba0001a9d990c747afa376d065a78bcb922275)技术对通讯内容进行加密，来保证本地与远程服务器进行安全的通讯和控制操作。ssh服务软件生成加密用的公私钥对儿，公钥保存在远程服务器登录用户默认的.ssh目录中；公私钥对儿需要保存在本地，需要注意安全和保密。

[SecureCRT：](https://www.vandyke.com/products/securecrt/) 是远程登录软件，类似的还有 [putty](http://www.putty.be/latest.html)，[Xshell](https://www.netsarang.com/zh/xshell/) 这些都可以。作用是管理密钥，对通讯内容进行加密和解密。

[WinSCP：](https://winscp.net/eng/download.php)是通过密钥进行加密的远程安全文件传输工具。

## 虚拟机安装及配置：
### 1. 打开 VirtualBox 创建虚拟机

![img](https://src.seaky.club/img/101.png) 
   
输入名称，选择类型和版本，一直下一步，默认配置足够用了。

![img](https://src.seaky.club/img/102.png)  
![img](https://src.seaky.club/img/103.png)  
![img](https://src.seaky.club/img/104.png) 
![img](https://src.seaky.club/img/105.png) 
![img](https://src.seaky.club/img/106.png) 
![img](https://src.seaky.club/img/107.png) 
![img](https://src.seaky.club/img/108.png)

### 2. 设置虚拟机（点击[设置]的齿轮）

![img](https://src.seaky.club/img/201.png)

网络配置选择网桥，后面给虚拟机分配一个静态IP和宿主机在同一个网段。
这样，宿主机可以通过IP+端口与虚拟机进通信，和局域网类似；同时虚拟机也可以通过路由直接访问到外部网络。

![img](https://src.seaky.club/img/202.png)

将 Ubunt iso 镜像加载到虚拟光驱。

![img](https://src.seaky.club/img/203.png)

### 3. 启动安装 Ubuntu server 系统（绿色启动箭头）

![img](https://src.seaky.club/img/301.png)
![img](https://src.seaky.club/img/302.png)

网络设置，配置静态IP，链接上网。
![img](https://src.seaky.club/img/303.png)

选择编辑 IPv4，
![img](https://src.seaky.club/img/304.png)

选择手动配置，
![img](https://src.seaky.club/img/305.png)

配置IPv4，网段选择宿主机所在网段；IP随意选择一个；网关选择宿主机的网关；配置域名解析服务器。
![img](https://src.seaky.club/img/306.png)

查看宿主机网络配置，widows -> [运行] -> [powershell] -> [ipconfig]
![img](https://src.seaky.club/img/306-.png)

网络配置完成后，下面的按钮从[continue without network]变成绿色的[Done]，点击，
![img](https://src.seaky.club/img/307.png)

代理服务器配置，不用填。
![img](https://src.seaky.club/img/308.png)

镜像地址可以默认，国内的可以修改为阿里云的：
http://mirrors.aliyun.com/ubuntu
![img](https://src.seaky.club/img/309.png)

硬盘格式选择：不加密的LVM卷积，默认的也行。
![img](https://src.seaky.club/img/310.png)

确认一下硬盘格式，点击[Done]。
![img](https://src.seaky.club/img/311.png)

格式化提醒，点击[Continue]。
![img](https://src.seaky.club/img/312.png)

设置服务器名称和登录用户名及密码，
![img](https://src.seaky.club/img/313.png)

选择安装 OpenSSH 服务，
![img](https://src.seaky.club/img/314.png)

预装程序可以根据自己需求选择。这里不选后面也可以通过apt命令自行安装。
![img](https://src.seaky.club/img/315.png)

安装完选择重启。
![img](https://src.seaky.club/img/316.png)

进入系统登录界面。
![img](https://src.seaky.club/img/317.png)

### 4. user1 用户远程连接 Ubuntu server (用户名+密码)

启动远程链接工具，创建新连接，输入IP，用户名；第一次选择密码登录。  
![img](https://src.seaky.club/img/401.png)
![img](https://src.seaky.club/img/402.png)

进入系统后，修改 root 密码；切换 root 用户；查看 root 用户.ssh目录下的公钥配置是否是空文件。
```powershell
$ sudo passwd root        # 修改root密码
$ su root                 # 切换root用户
$ cd && cd .ssh/ && ls -l # 进入root根目录，.ssh默认目录，查看公钥
```
![img](https://src.seaky.club/img/403.png)

进入ssh服务密钥目录，复制公钥到根目录的.ssh目录里，
```powershell
$ cd /etc/ssh/            # 进入密钥保存目录
$ cp ssh_host_rsa_key.pub /root/.ssh/     # 复制公钥到root默认.ssh目录
$ cd && cd .ssh/          # 进入root默认.ssh目录
$ mv ssh_host_rsa_key.pub authorized_keys   # 覆盖验证公钥
$ chmod 400 authorized_keys     # 修改公钥权限为root只读
$ exit                    # 退出root用户
```
![img](https://src.seaky.club/img/404.png)

进入 user1 回到根目录，创建验证目录，复制公钥到验证目录
```powershell
$ mkdir .ssh && chomd 700 .ssh && cd .ssh  # 创建，修改权限，进入验证目录 .ssh
$ sudo cat /root/.ssh/authorized_keys > ./authorized_keys  # 复制公钥到本目录下
$ chmod 400 authorized_keys     # 修改权限为只读
```
![img](https://src.seaky.club/img/405.png)

修改私钥权限允许WinSCP下载（下载完后需将权限改回），测试网络链接
```powershell
$ cd /etc/ssh/          # 进入ssh服务密钥目录
$ sudo chmod 644 ssh_host_rsa_key   # 修改私钥权限为其他用户可读

$ ping www.baidu.com    # 测试一下网络链接
```
![img](https://src.seaky.club/img/406.png)

### 5. WinSCP 下载公私钥对儿到本地
启动WincSCP，创捷新连接，输入IP，用户名和密码，

![img](https://src.seaky.club/img/501.png)
![img](https://src.seaky.club/img/502.png)
![img](https://src.seaky.club/img/503.png)

下载密钥对儿到本地（直接拖）。
![img](https://src.seaky.club/img/504.png)

### 6. root 用RSA密钥，远程链接 Ubuntu server

新建远程连接，配置IP，用户名，和密钥对儿，选择公钥即可。
![img](https://src.seaky.club/img/601.png)
![img](https://src.seaky.club/img/602.png)
![img](https://src.seaky.club/img/603.png)

进入系统。
![img](https://src.seaky.club/img/604.png)

其他用户同样操作。
这样就可以通过远程登录软件学习和本地调试服务器应用了。

---   

**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，老虎证券王珊老师的**读财报课**，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，下载并注册 [**Mixin**](https://mixin.one/messenger) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mixin.one/messenger) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)
