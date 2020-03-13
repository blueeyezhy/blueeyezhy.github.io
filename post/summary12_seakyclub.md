# 从零搭建飞贴站--复盘&学习总结(十二)

## 飞贴站框架&请求响应流程  
先从整体介绍一个飞贴站的架构和请求响应流程，然后再一块一块的说明每一部分怎么实现。  

**<建站前提条件>**  
要掌握下列知识领域的基本操作： **服务器与域名基本知识，Linux系统操作，ssh服务，TLS&CA，git，nginx，docker和docker-compose，数据库**

**<飞贴站架构图>**
![seakyclub](https://static.press.one/73/8e/738ec26af0d8069a1320beb4a64ad358f9af968415cd5064c43fd17cbe119992.png)

**<请求响应流程>**
> 1. 用户通过浏览器输入域名
> 2. 浏览器通过DNS域名解析，链接到服务器外网IP
> 3. nginx监听端口80(http协议)和443(https协议)，并将所有80端口的请求全部转到443端口上(443端口是通过TLS完全认证的安全入口)
> 4. nginx根据请求的域名($host)分发到对应的服务应用或资源
> 5. 如果 $host = seaky.club, 则nginx转到首页资源目录，读取指定的静态资源(html,img,css,js等)经过nginx转发，返回给浏览器    
> 6. 如果 $host = www.seaky.club, 则nginx将请求转到**docker0**的80端口，由**docker0**的80端口映射的docker容器响应该请求，然后把响应结果通过nginx转发给浏览器
> 7. 如果 $host = pub.seaky.club, 则nginx将请求转到**br-飞贴**的8000端口，由**br-飞贴**的8000端口映射的pub容器响应该请求；pub容器根据请求中的路径和参数，通过**br-飞贴**连接到redis，PG数据库及异步队列，计算出响应结果；然后通过nginx将响应结果转发给浏览器
> 8. 如果 $host = reader.seaky.club, 则nginx将请求转到**br-飞贴**的9000端口，由**br-飞贴**的9000端口映射的reader容器响应该请求；reader容器根据请求中的路径和参数，通过**br-飞贴**连接到redis，PG数据库及异步队列，计算出响应结果；然后通过nginx将响应结果转发给浏览器         


## 详细实现过程    

### 服务器实例的采购及配置
1. 选择云主机(ECS实例)及硬件配置    
   阿里云，腾讯云，国外的云都可以。基于方便支付，成本及与云技术人员沟通方便我选择的是[阿里云](https://ecs-buy.aliyun.com/wizard?spm=5176.8709316.cart_detail_root.1.5f055f29pJNJgC&accounttraceid=7b505cab-c22e-4b9b-9f9d-39c15316dc2c&aly_as=aeEQM_-E#/prepay/cn-shenzhen)。  
   seaky.club当前的硬件配置(后期可以扩展)：2核CPU，4G内存，40G硬盘，带宽默认，最好选择支持ipv6。
2. 选择操作系统   
   这个看个人喜好，主流的是centos和ubuntu server。因为我前一段时间学习的是centos，所以我选的是centos8。
3. 选择分配公网IP，这是外网的入口，默认就好。
4. 设定安全组，追加入站规则开放80，443端口的访问，出站默认(全部允许)。
5. 创建并**保存**ssh密钥(*.pem，后面远程登陆要用)，**绑定服务器实例**(这一步很重要，不要漏掉)，修改root密码。
6. 确认订单，付钱，等待服务器的启动。
7. 确认服务器运行状态，ssh密钥是否绑定，如未绑定成功则要绑定后重启。


### 域名的采购及配置
1. 购买自己喜欢的域名，域名供应商也很多。我选的是[阿里](https://wanwang.aliyun.com/domain/)。
2. 选择DNS服务器(默认hichina)，也可以选择其他国外服务器，如fcloud
3. 添加解析记录，记录值为服务器的公网IP，[阿里教程](https://help.aliyun.com/document_detail/106669.html?spm=a2c4g.11186623.6.560.422669a0bgL99G)
   1. 一级域名：@
   2. 二级域名：www，reader，pub   
4. 服务器在中国的需要，通过工信部的ICP备案，才可以通过域名访问。页面会有提示以及申请链接，填写资料提交申请，我用个人空间的名义申请的2天获得备案号。
5. 然后就可以通过域名访问到自己的服务器了。解析到国外服务器的域名不需要ICP备案。

### 软件安装及配置
1. 本地主机需要安装远程登录工具，按照教程[使用SSH密钥对连接Linux实例](https://help.aliyun.com/document_detail/51798.html)配置ssh密钥建立链接。远程控制服务器主机的工具比较多，如 putty(上面链接有下载)，[Xshell](https://www.netsarang.com/zh/xshell/)，[SecureCRT](https://www.vandyke.com/products/securecrt/)都可以；另外也可以通过Linux系统直接远程访问服务器，命令如下：   
   `ssh -i ~/.ssh/seaky.pem root@47.103.71.170`；  
   其中 `~/.ssh/seaky.pem` = 从阿里云下载的私钥、`root@47.103.71.170` = 用户名@外网ip。  
   还有一个文件传输的工具[WinSCP](https://winscp.net/eng/download.php)，远程传输文件很好用。     


   关于私钥和公钥的相关知识大家可以自行去搜索，我自己对于加密与解密也做过一些总结：
   [加密与解密1](https://reader.seaky.club/posts/834d1552074d5ded877a22a2c2a2ab60cf5b4e5d0951154f75773915ec0c43ae)，[对称加密(DES)](https://reader.seaky.club/posts/667a66907ecc7d28572fe66bf3a8da9723b72a4714d425087a6c7df40ae4725b)，[非对称加密(RSA)](https://reader.seaky.club/posts/71bbf6bd85beb9e08da2c65e66ba0001a9d990c747afa376d065a78bcb922275)    


   核心过程是：  
   **a.** 服务器在默认路径下保存公钥；   
   **b.** 本地主机远程工具利用本地保存的私钥(阿里云下载的私钥)将通讯内容进行签名(加密)，然后通过ssh服务传输到服务器22端口；    
   **c.** 服务器的ssh服务监听22端口，接收到的信息后，利用其保存的公钥验证签名信息(解密)，校验用户和信息完整性；    
   **d.** 然后根据验证信息内容，将验证信息转发给对应的服务或操作系统指令集

2. 使用上述工具登录远程服务器，创建普通权限用户，避免远程使用root用户造成误操作
   ```powershell
   $ adduser www              # 新建用户
   $ passwd www               # 设置密码
   $ usermod -aG wheel www    # 将用户 www 加入 wheel 用户组，可执行 sudo 命令
   $ su - www                 # 切换至用户 www
   $ sudo ls -la /root        # 测试用户 www 是否能执行 sudo 命令，首次执行需要输入用户 www 的密码
   ```
3. 为新用户 `www` 配置ssh公钥
   ```powershell
   $ cd                       # 切换至当前用户的用户目录
   $ mkdir .ssh && chmod 700 .ssh && cd .ssh    # 新建.ssh目录并设置目录权限，然后进入目录
   $ sudo cat /root/.ssh/authorized_keys > ./authorized_keys # 将 root 用户的公钥复制到当前目录
   $ chmod 400 authorized_keys # 设置文件为只读权限
   $ exit   # 退出服务器
   ```
   在远程登录工具上使用 `www` 用户登录服务器，测试新用户的远程登录。
   不要禁止远程root登录，因为后续执行飞贴的docker-compose命令时需要用root用户。

4. 远程登录服务器，确认网络配置是否支持ipv6通讯功能。因为飞贴的服务是通过docker-compose创建的容器组实现的，而容器之间是通过TCP6协议进行通讯的，所以主网卡的配置需要支持ipv6，以支持TCP6协议的通讯。   
   执行 `ifconfig` 或 `nmcli` 查看当前网络配置：
   ```powershell
   $ sudo nmcli
   eth0: connected to eth0
        "Intel 82540EM"
        ethernet (e1000), 08:00:27:50:53:B3, hw, mtu 1500
        ip4 default
        inet4 172.19.159.2/24
        route4 192.168.1.0/24
        route4 0.0.0.0/0
        inet6 fe80::3bd:6895:a2d4:9fc2/64   # ipv6配置
        route6 fe80::/64                    # ipv6配置
        route6 ff00::/8                     # ipv6配置
   ```
   找到网卡(inet4参数为内网IP的网卡)，查看是否有inet6配置，如果没有则需要手动修改以下配置；
   ```powershell
   $ sudo vim /etc/default/grub     # 注释掉内核参数 IPV6.DISABLE=1 后保存退出。
   $ sudo vim /boot/grub/grub.cfg   # 注释掉内核参数 IPV6.DISABLE=1 后保存退出。
   $ reboot  # 重启ECS实例
   ```
   重新链接远程服务器实例并执行：
   ```powershell
   $ sudo vim /etc/modprobe.d/disable_ipv6.conf 
      options ipv6 disable = 0                     # 修改为 0
   $ sudo vim /etc/sysctl.conf
      net.ipv6.conf.all.disable_ipv6 = 0           # 修改为 0
      net.ipv6.conf.default.disable_ipv6 = 0       # 修改为 0
      net.ipv6.conf.lo.disable_ipv6 = 0            # 修改为 0, 保存退出
   $ sudo sysctl -p                             # 生效配置
   ```
   执行 `sudo ip addr | grep inet6` 查看ipv6是否生效
   ```powershell
   $ sudo ip addr | grep inet6
      inet6 ::1/128 scope host                     # ipv6配置生效
      inet6 fe80::42:c2ff:fee3:4eb6/64 scope link  # ipv6配置生效 
   ```
   执行 `sudo vim /etc/sysconfig/network-scripts/ifcfg-eth0` 查看网卡配置：
   ```powershell
   $ sudo vim /etc/sysconfig/network-scripts/ifcfg-eth0
      # Created by cloud-init on instance boot automatically, do not edit.
      BOOTPROTO=dhcp
      DEVICE=eth0
      ONBOOT=yes
      STARTMODE=auto
      TYPE=Ethernet
      USERCTL=no

      IPV4_FAILURE_FATAL=no      # 如果没有则添加
      IPV6INIT=yes               # 如果没有则添加
      IPV6_AUTOCONF=yes          # 如果没有则添加
      IPV6_DEFROUTE=yes          # 如果没有则添加
      IPV6_FAILURE_FATAL=no      # 如果没有则添加
      IPV6_ADDR_GEN_MODE=stable-privacy      # 如果没有则添加
   ```
   `wq` 保存退出，`nmcli c reload` 生效网络配置。

5. 查看系统防火墙配置，因为云安全组已经配置了入站规则，所以系统防火墙默认是关闭的，即使打开也不会增加多少安全度。如果想要开防火墙的话，需要进行如下操作：
   ```powershell
   $ sudo firewall-cmd --state        # 查看防火墙状态，显示 'not runing'
   $ sudo systemctl start firewalld   # 开启防火墙系统防火墙
   $ sudo systemctl enable firewalld  # 设置开机启动防火墙
   $ sudo firewall-cmd --zone=public --add-port=22/tcp --permanent  # 永久打开22端口，ssh服务端口
   $ sudo firewall-cmd --zone=public --add-port=80/tcp --permanent  # 永久打开80端口，http服务端口
   $ sudo firewall-cmd --zone=public --add-port=443/tcp --permanent  # 永久打开443端口，https服务端口
   $ sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent  # 永久打开8000端口，飞贴发布站网桥端口
   $ sudo firewall-cmd --zone=public --add-port=9000/tcp --permanent  # 永久打开9000端口，飞贴阅读站网桥端口
   $ sudo firewall-cmd --zone=public --add-port=7070/tcp --permanent  # 永久打开7070端口，飞贴同步网桥端口
   $ sudo firewall-cmd --zone=public --add-port=6379/tcp --permanent  # 永久打开6379端口，飞贴redis网桥端口
   $ sudo firewall-cmd --zone=public --add-port=5432/tcp --permanent  # 永久打开5432端口，飞贴PG数据库网桥端口
   $ sudo firewall-cmd --reload       # 加载防火墙设置
   $ sudo firewall-cmd --list-all     # 查看端口状态

   public (active)
      target: default
      icmp-block-inversion: no
      interfaces: enp0s3
      sources: 
      services: cockpit dhcpv6-client ssh
      ports: 80/tcp 443/tcp 22/tcp 8000/tcp 9000/tcp 7070/tcp 6379/tcp 5432/tcp
      protocols: 
      masquerade: no
      forward-ports: 
      source-ports: 
      icmp-blocks: 
      rich rules: 
   ```
   说明：  
   **a**.防火墙的意义和重点是设定允许访问与接入  
   **b**.启用防火墙配置前，一定要确保22/tcp端口是永久开放的，否则远程访问将被禁止  
   **c**.容器和系统公用一个网卡资源，通过命名空间隔离，如果网卡硬件设置不开放6379和5432端口的话，飞贴容器就访问不到数据库   
   **d**.因为云主机的入站规则仅开放了80和443端口，所有外部无法访问到6379和5432端口，可以保证数据库安全

6. 系统升级安装包 
   ```powershell
   $ sudo yum upgrade   # 升级yum安装包，没有用update是因为update会升级kernel内核，可能会引入不稳定因素
   $ sudo yum --version # 确认版本
   ``` 

7. 安装配置git并确认版本
   ```powershell
   $ sudo yum install git  
   $ sudo git version   
   ```

8. 安装配置 [docker](http://dockerdocs.gclearning.cn/install/linux/docker-ce/centos/)，[docker-compose](https://docs.docker.com/compose/install/)，并确认版本
   ```powershell
   $ sudo docker -v
   Docker version 19.03.6, build 369ce74a3c
   $ sudo docker-compose -v
   docker-compose version 1.25.4, build unknown
   ```

9. 安装 [flying-hub](https://github.com/Press-One/flying-pub)
   ```powershell
   $ cd     # 进入当前用户根目录
   $ sudo git clone https://github.com/Press-One/flying-pub.git   # clone flying-hub 
   $ cd flying-pub   # 进入 flying-hub 目录
   ```
   切换root用户远程登录
   ```powershell
   $ ./scripts/generate_config_prod.sh   # 初始化飞贴站，按照提示配置两个mixin app，
   $ ./scripts/start_prod.sh             # 启动飞贴站，可能需要15分钟左右
   ```
   参看 [mixinDeveloper](https://developers.mixin.one/guides)，生成应用mixin app的密钥`Secret`，下载`Session`获取`PIN`，`Session ID`，`PinToken`，`私钥`，session文件请妥善保管。   
   启动完成后，执行 `crul http://localhost:8000`，`crul http://localhost:9000` 确认返回发布站和阅读站的html首页。

1. 安装nginx    
   ```powershell
   $ sudo yum install nginx -y   # 安装nginx
   $ nginx -v                    # 确认版本
   $ sudo systemctl enable nginx # 设定开机启动
   $ sudo systemctl start nginx  # 启动nginx服务
   $ sudo systemctl status nginx # 查看nginx服务状态
   ● nginx.service - The nginx HTTP and reverse proxy server
      Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; vendor preset: disabled)
      Active: active (running) since Wed 2020-03-11 09:06:59 CST; 12h ago     # 运行正常
      Process: 952 ExecStart=/usr/sbin/nginx (code=exited, status=0/SUCCESS)
      Process: 915 ExecStartPre=/usr/sbin/nginx -t (code=exited, status=0/SUCCESS)
      Process: 910 ExecStartPre=/usr/bin/rm -f /run/nginx.pid (code=exited, status=0/SUCCESS)
      Main PID: 967 (nginx)
      Tasks: 2 (limit: 5059)
      Memory: 8.9M
      CGroup: /system.slice/nginx.service
            ├─967 nginx: master process /usr/sbin/nginx
            └─968 nginx: worker process

      Mar 11 09:06:58 seakyrun systemd[1]: Starting The nginx HTTP and reverse proxy server...
   ```
   如果开了防火墙的话，需要添加设定：
   ```powershell
   $ sudo firewall-cmd --permanent --zone=public --add-service=http 
   $ sudo firewall-cmd --permanent --zone=public --add-service=https
   $ sudo firewall-cmd --reload
   ```

2. 配置静态首页及反向代理reader和pub容器    
   nginx是轻量级高并发服务器程序，配置项目很多，可以参考[nginx通用配置](https://www.digitalocean.com/community/tools/nginx)做通用配置，然后根据自身情况修改。   
   下面是seaky.club的配置：
   ```powershell
   upstream upstream-seaky-pub {
         server localhost:8000;  # 这里使用docker0或内网ip都可以
   }
   upstream upstream-seaky-reader {
         server localhost:9000;  # 这里使用docker0或内网ip都可以
   }

   # HTTP redirect  80端口重定向到443端口
   server {
         server_name             seaky.club www.seaky.club pub.seaky.club reader.seaky.club;  # 监听域名$host
         listen                  80 default_server;               # 监听 ipv4 80端口
         listen                  [::]:80 default_server;          # 监听 ipv6 80端口
         include                 /etc/nginx/nginxconfig.io/letsencrypt.conf;  # 添加TLS认证配置路径
         location / {
                  return 301     https://$host$request_uri;      # 重定向到443端口，https服务
         }
   }

   server {
         server_name             seaky.club www.seaky.club;    # 监听静态首页$host
         listen                  443 ssl http2;                
         listen                  [::]:443 ssl http2;
         access_log              /var/log/nginx/seaky.club.access.log;
         error_log               /var/log/nginx/seaky.club.error.log error;
         include                 /etc/nginx/nginxconfig.io/ssl.conf;       # 引入ssl配置
         include                 /etc/nginx/nginxconfig.io/general.conf;   # 引入压缩等通用配置
         include                 /etc/nginx/nginxconfig.io/security.conf;  # 引入安全配置
         location / {
                  root           /home/www/seaky.club/public;       # 配置静态首页路径
                  index          seaky.html;                        # 静态首页html
         }
         location ~ /\.(?!well-known) {      # 禁止其他匹配
                  deny           all;
         }
   }

   server {
         server_name             pub.seaky.club;      # 监听发布站$host
         listen                  443 ssl http2;
         listen                  [::]:443 ssl http2;
         access_log              /var/log/nginx/pub.seaky.access.log;
         error_log               /var/log/nginx/pub.seaky.error.log error;
         include                 /etc/nginx/nginxconfig.io/ssl.conf;
         include                 /etc/nginx/nginxconfig.io/general.conf;
         include                 /etc/nginx/nginxconfig.io/security.conf;
         location ~* {
                  resolver       127.0.0.11 valid=10s;                    
                  include        /etc/nginx/nginxconfig.io/proxy.conf;    # 引入反向代理通用配置
                  proxy_pass     http://upstream-seaky-pub;               # 反向代理到发布站端口
         }
         location ~ /\.(?!well-known) {
                  deny            all;
         }
   }

   server {
         server_name             reader.seaky.club;    # 监听阅读站$host
         listen                  443 ssl http2;
         listen                  [::]:443 ssl http2;
         access_log              /var/log/nginx/reader.seaky.access.log;
         error_log               /var/log/nginx/reader.seaky.error.log error;
         include                 /etc/nginx/nginxconfig.io/ssl.conf;
         include                 /etc/nginx/nginxconfig.io/general.conf;
         include                 /etc/nginx/nginxconfig.io/security.conf;
         location ~* {
                  resolver       127.0.0.11 valid=10s;
                  include        /etc/nginx/nginxconfig.io/proxy.conf;
                  proxy_pass     http://upstream-seaky-reader;                # 反向代理到阅读站端口
         }
         location ~ /\.(?!well-known) {
                  deny            all;
         }
   }
   ```
   配置完成后，执行：
   ```powershell
   $ sudo nginx -t                  # nginx配置语法检测
   $ sudo systemctl reload nginx    # 生效新配置
   $ sudo systemctl status nginx    # 确认nginx状态
   ```

3. 其他配置内容  nginx & general & security & proxy   
   `/etc/nginx/nginx.conf;` nginx主配置    
   ```powershell
   user nginx;
   pid /run/nginx.pid;
   worker_processes auto;
   worker_rlimit_nofile 65535;

   events {
         use epoll;
         multi_accept on;
         worker_connections 65535;
   }

   http {
         charset utf-8;
         sendfile on;
         tcp_nopush on;
         tcp_nodelay on;
         log_not_found off;
         keepalive_timeout 65;
         types_hash_max_size 2048;
         client_max_body_size 100M;
         server_names_hash_bucket_size 64;

         proxy_hide_header X-Powered-By;
         proxy_hide_header Server;

         # MIME
         include  /etc/nginx/mime.types;
         default_type application/octet-stream;

         # logging
         access_log      /var/log/nginx/access.log;
         error_log       /var/log/nginx/error.log error;

         # limits
         limit_req_log_level warn;
         limit_req_zone $binary_remote_addr zone=login:10m rate=10r/m;

         # SSL
         include         /etc/nginx/nginxconfig.io/ssl.conf;

         # load configs
         include         /etc/nginx/conf.d/*.conf;
         include         /etc/nginx/sites-available/*.conf;
   }

   ```
   `/etc/nginx/nginxconfig.io/general.conf;` 压缩相关配置
   ```powershell
   # gzip 
   gzip                            on;
   gzip_vary                       on;
   gzip_proxied                    any;
   gzip_comp_level                 6;
   gzip_types                      text/plain application/javascript application/x-javascript text/javascript text/xml text/css application/xhtml+xml application/xml application/rss+xml application/atom+xml image/svg+xml;
   gzip_disable            "MSIE [1-6]\.(?!.*SV1)";
   ```
   `/etc/nginx/nginxconfig.io/security.conf;` 请求头安全相关配置
   ```powershell
   # security headers
   add_header Referrer-Policy "same-origin" always;
   add_header X-Frame-Options "SAMEORIGIN" always;
   add_header X-XSS-Protection "1; mode=block" always;
   add_header X-Content-Type-Options nosniff;
   add_header X-Download-Options noopen;
   add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
   server_tokens off;
   # . files
   location ~ /\.(?!well-known) {
         deny all;
   }
   ```
   `/etc/nginx/nginxconfig.io/proxy.conf;` 反向代理相关配置
   ```powershell
   proxy_http_version      1.1;
   proxy_cache_bypass      $http_upgrade;
   proxy_connect_timeout   30;
   proxy_send_timeout              60;
   proxy_read_timeout              60;
   proxy_buffering                 on;
   proxy_buffers                   32 32k;
   proxy_buffer_size               128k;
   proxy_busy_buffers_size 128k;
   proxy_hide_header       X-Powered-By;
   proxy_hide_header       Server;
   proxy_set_header Upgrade                $http_upgrade;
   proxy_set_header Connection             "upgrade";
   proxy_set_header Host                   $host;
   proxy_set_header X-Real-IP              $remote_addr;
   proxy_set_header X-Forwarded-For        $proxy_add_x_forwarded_for;
   proxy_set_header X-Forwarded-Proto      https;
   proxy_set_header X-NginX-Proxy          true;
   proxy_set_header X-Forwarded-Host       $host;
   proxy_set_header X-Forwarded-Port       $server_port;
   proxy_ssl_session_reuse off;
   proxy_redirect                  off;
   ```


4. https配置（选择Let's Encrypt作为认证平台，用certbot实现认证过程）    
   https安全链接是通过TLS协议和CA证书来实现的，简要实现过程如下图：过程核心是[非对称加密](https://reader.seaky.club/posts/71bbf6bd85beb9e08da2c65e66ba0001a9d990c747afa376d065a78bcb922275)。  

   ![TLS&CA](https://static.press.one/42/34/423420f2bee4bcb5441c274a0165479944b065e2933425ef621e9a3936436460.png)


   `/etc/nginx/nginxconfig.io/ssl.conf;` ssl配置TLS认证相关
   ```powershell
   #ssl
   ssl_certificate /etc/letsencrypt/live/seaky.club/fullchain.pem;      # 包含认证机构的CA证书
   ssl_certificate_key /etc/letsencrypt/live/seaky.club/privkey.pem;    # 服务器TLS私钥
   ssl_trusted_certificate /etc/letsencrypt/live/seaky.club/chain.pem;  # CA证书
   ssl_session_timeout 1d;
   ssl_session_cache shared:SSL:50m;
   ssl_session_tickets off;

   # Diffie-Hellman parameter for DHE ciphersuites
   ssl_dhparam /etc/ssl/certs/dhparam.pem;   # DHE安全增强

   ssl_protocols TLSv1.2 TLSv1.3;
   ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
   ssl_prefer_server_ciphers on;

   # OCSP Stapling     
   ssl_stapling on;
   ssl_stapling_verify on;
   resolver 1.1.1.1 1.0.0.1 8.8.8.8 8.8.4.4 208.67.222.222 208.67.220.220 valid=600s;
   resolver_timeout 600s;

   fastcgi_param   HTTPS                   on;
   fastcgi_param   HTTP_SCHEME             https;
   ```
   `/etc/nginx/nginxconfig.io/letsencrypt.conf;` 本地验证信息路径，只要是本地文件就行
   ```
   # ACME-challenge
   location ^~ /.well-known/acme-challenge/ {
         default_type    "text/plain";
         root            /usr/share/nginx/html;
   }
   location = /.well-known/acme-challenge/ {
         return 404;
   }
   ```
   根据[certbot官方文档](https://certbot.eff.org/lets-encrypt/centosrhel8-nginx)，根据向导生成域名证书，我是一套证书认证4个域名。也可以应用通配符的CA认证，可以1套证书认证多个域名。[开启DHE ciphersuites和OCSP服务](https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html)安全加固。

### 飞贴站自定义及MixinApp配置      
1. MixinApp配置     
   进入[MixinDeveloper]https://developers.mixin.one，选择与飞贴站绑定的两个app，配置url。     
   名称： seaky_reader     
   首页网址： https://reader.seaky.club     
   验证网址： https://reader.seaky.club/api/auth/mixin/callback    

   名称： seaky_pub     
   首页网址： https://pub.seaky.club     
   验证网址： https://pub.seaky.club/api/auth/mixin/callback 

2. 飞贴站自定义 （注意修改内容，避免错误）    
   远程链接进入服务器飞贴站配置目录，修改 `config.pub.js` 和 `config.reader.js` 配置
   ```powershell
   $ sudo seaky.club/flying-pub/config
   $ sudo vim config.pub.js        # title等标志性的内容修改为自己的。如“飞贴”改为“思齐”
   $ sudo vim config.reader.js     # title等标志性的内容修改为自己的。如“飞贴”改为“思齐”
   ```

### 其他   
关于学习 Linux，ssh，nginx，docker和docker-compose，可以通过在本体搭建虚拟机，安装Linux操作系统来进行练习，我用的是VirtualBox搭建的，操作系统用的是centos。   

列一下我的学习链接：
[Linux](http://www.beylze.com/linuxjiaocheng/)；
[Linux](https://www.yuhelove.com/)；
[docker](https://vuepress.mirror.docker-practice.com/image/list.html#%E9%95%9C%E5%83%8F%E4%BD%93%E7%A7%AF)；
[docker_xue.cn](https://xue.cn/user/33739411@github/reader?bookId=24&path=book_31427/txt002.ipynb&redirects=1)；
[docker](https://www.jianshu.com/p/9f76aa8740b0)；
[docker](http://c.biancheng.net/view/3189.html)

还有最重要的google搜索引擎

### 所感
一个多月的高密度学习，基本掌握了建立一个webapp的知识和初步技能。过程中遇到很多问题也解决了很多问题，同时自我感觉成长的很多。

一点心得，遇到一个弄了很久也无法解决的问题的时候，放松一下洗个碗，重新从基础知识再读一遍教程，通常就会柳暗花明。

---   
**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，老虎证券王珊老师的**读财报课**，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，注册 [**Mixin**](https://mixin.one/messenger) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mp.weixin.qq.com/s/ci_OWj9vtnsJ4OROifNfSQ) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)
