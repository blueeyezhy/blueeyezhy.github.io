# Github技巧 一个本地库链接多个远程库 --Python学习总结(八)

> - **PressOne**: [张野](https://press.one/main/p/7c08521960497a61baf3f1c9760ff2a4cc66be1c)
> - [**Mixin**](https://mixin.one/) ID: 21120;  **bot**: 7000102888
> - **Github**: [@blueeyezhy](https://github.com/blueeyezhy)
> - **web**: [blueeyezhy.github.io](https://blueeyezhy.github.io/)


## 缘起  
一次和开儿童俱乐部的朋友聊天，得知俱乐部的孩子们（一群5~10岁的孩子们）在做一个PBL项目--做一个关于环保的主题绘本，人物设定和故事内容进行了一个多月，部分已经开始绘制了；孩子们想要做一个长期的连载项目，想出版宣传。为了还孩子们的这个愿望，她在寻找出版方案，但是孩子们是课余时间手绘，成书效率不高，不够精致，同时成本要求尽可能的低，与出版印刷方难以形成共识。这个项目与pressone完美切合，完全可以用pressone+自建主页及其他宣传渠道的方式来实现。于是就和她一起讨论了半天，结论是我负责pressone和自建主页方面，她推动孩子们的进度。  
建站方面刚好和我正在学习的 [python 全栈应用开发](https://xue.cn/hub/) （xue.cn 刚刚上架的一本新书）相关，于是就想用 **Django** 边学习边做，先完成静态前端，然后实现基础互动。

## 问题=需求  
刚开始着手就面临一个问题，在 Github 我有一个账号和主页，现在又加一个俱乐部的，要满足频繁切换。于是就需要有一个本地库对应多个远程库关联。这个场景在公司里很常见，将远程公司库和远程个人库关联到一台电脑的本地库上。于是一番搜索加实践，花了一整天才最终搞定；网上很多的经验文章内容不全，新手关注的关键点没有说清楚，于是整理一份我遇到的坑给大家希望你少走弯路。

## 解决过程   
因为一把公钥只能被一个Github帐号所拥有，因此必须为不同的帐号创建公钥；交互时需要本地私钥与Github帐号的公钥配对。所以，要在同一台电脑上给两个属于不同帐号的仓库提交时，必须在本地创建两对儿公私密钥，分别把两把公钥给两个帐号，提交时根据要提交的仓库所属帐号选择相应的本地私钥。当要在一个本地仓库上Push提交内容时，选择对应的私钥加密提交，Github服务器收到提交的内容时，先解析出仓库地址，然后从该仓库的所属帐号中找到能解密的公钥。

0. SSH远程登陆的安全协议（Github自动支持）  
   SSH是非对称加密（参看下面我第七篇关于RSA的学习总结）的服务，利用公私钥对儿进行信息加密传输，身份验证等。在http传输协议中，如果需要与远程账户进行交互，就要通过账户和密码的进行反复验证，进而增加了账户和密码暴露的风险。而用SSH服务，将公钥放在需要频繁交互的服务器上，通过公私钥的加密和验证过程，可以安全，快速的进行信息的交互。在远程交互领域非对称加密方式已经成为主流。 

   针对Github的使用，推荐用SSH服务；过程很简单，先在本地生成公私钥对儿（算法有多种，应用最广泛的是RSA算法），将公钥复制黏贴在Github账户上：  
   点击Github账户右边的下三角图标，选择 `settings`, 再选择 `SSH and GPG keys`，在SSH keys栏按下 `New SSH key`，起一个 `title` 方便跟踪；然后把公钥黏贴在`key` 栏里，最后点击 `Add SSH key`，然后自动返回到 `SSH and GPG keys` 界面，就会看到你添加的公钥了。首次添加钥匙是黑色的，一次访问成功之后就会变成绿色。

1. 在本地生成两个账号的密钥对儿，如果已经有了一个，再生成一个就够了。   
   在命令行（powershell或者其他prompt，不清楚的可以参看下面我的第二篇学习总结）中键入下面命令（注意其中的空格，不能少可以多）：
   ```PowerShell
   PS C:\Users\yourname> ssh-keygen -t rsa -f .ssh\id_rsa_name -C youremail@company.com
   ```
   其中：`PS C:\Users\yourname>` 是根目录，基本上所有环境设置，应用都在这里。
   `ssh-keygen` 是创建密钥的语句；`-t rsa` 选择加密算法RSA；`-f .ssh\id_rsa_name` 是在 `.ssh` 目录下创建名为 `id_rsa_name` （name可以根据实际情况自行修改）的密钥对儿；`-C youremail@company.com` 是这个密钥对儿绑定的个人邮箱（最好跟Github绑定邮箱一致或者相关，例如同一个项目组的个人公共邮箱，方便个人管理）。
   完成后你就可以在 `.ssh` 目录下看到密钥对了：
   ```PowerShell
   id_rsa               # 第一账户私钥
   id_rsa.pub           # 第一账户公钥
   id_rsa_name          # 第二账户私钥
   id_rsa_name.pub      # 第二账户公钥  
   ```
   由于有两个Github账号，要在同一台电脑上同步代码，就需要给每一个账号添加一个SSH公钥。推送时通过不同密钥对儿，与不同的账户的远程仓库交互。

2. 将新生成的密钥添加到SSH代理服务中  
   在shell中键入 `ssh-add -l` 命令，查看代理服务中的密钥信息；正常结果会显示：
    ```PowerShell
    2048 SHA256:2I1Y********************************AKNJ0KM id_rsa (RSA) 
    ```
   这是密钥 `id_rsa` 的公钥hash映射之后的信息；如果出现 `Could not open a connection to your authentication agent` ，键入 `ssh-agent bash` 命令，启动SSH代理服务。   

   在shell的根目录下，运行命令 `ssh-add .ssh/id_rsa_name`，将新的密钥`id_rsa_name` 加入服务，运行命令 `ssh-add -l` 查询结果： 
    ```PowerShell
    2048 SHA256:2I1Y********************************AKNJ0KM id_rsa (RSA)
    2048 SHA256:RGtg********************************zHt7XvM id_rsa_name (RSA)
    ```

3. 配置访问域名，目的是告诉本地库，根据远程库的域名和账号，选择密钥通道进行交互  
   我们先来看一下Github代码库界面，这是我们需要配置链接和交互的方向
   ![img](https://static.press.one/12/49/124932c7307dca79b342600432882cee6888ce6bb8f10fc56a295e9fb0639eda.jpg)  

   https链接：（点绿色 `clone...` 按钮，点 `Use HTTPS`，点完后它会变成 `Use SSH`）   
   `https://github.com/blueeyezhy/blueeyezhy.github.io.git`  
   `https://` https协议标识；   
   `github.com` Github域名可以通过DNS解析成IP+端口；  
   `/blueeyezhy` User = Github账号；  
   `/blueeyezhy.github.io.git` 代码库链接。  
   
   SSH链接：  
   `git@github.com:blueeyezhy/blueeyezhy.github.io.git`   
   `git@` Github的SSH协议标识：   
   `github.com` Github域名可以通过DNS解析成IP+端口；     
   `/blueeyezhy` User = Github账号；   
   `/blueeyezhy.github.io.git` 代码库链接。  

   理解了链接各参数的意义，我在配置SSH域名映射时就有了明确的目标。
   在 `.ssh` 目录下键入命令 `New-Item config` （Mac用touch命令）创建 `config` 文件，键入 `code config` 使用VS code 编辑内容：

    ```PowerShell
    # 代码库1
    Host blueeye                            # 自定义域名(重要)，这是后续链接远程时需要替换的域名部分
        HostName github.com                 # 代码库1的域名，个人库一般都是github.com，其他根据实际情况
        User blueeyezhy                     # 代码库1的Github账号
        IdentityFile ~/.ssh/id_rsa          # 代码库1验证账号和代码库的私钥
        PreferredAuthentications publickey  # 指定优先使用公钥加密和秘钥验证方式

    # 代码库2
    Host miaoqu                             # 自定义域名(重要)，这是后续链接远程时需要替换的域名部分
        HostName github.com                 # 代码库2的域名，个人库一般都是github.com，其他根据实际情况
        User miaoquname                     # 代码库2的Github账号
        IdentityFile ~/.ssh/id_rsa_name     # 代码库2验证账号和代码库的私钥
        PreferredAuthentications publickey  # 指定优先使用公钥加密和秘钥验证方式
    ```
4. 将两个公钥按照上面第0步流程，添加到github账户上
    ```PowerShell
    id_rsa.pub       # 代码库1，账号：blueeyezhy -> seetings -> add SSH key
    id_rsa_name.pub  # 代码库2，账号：miaoquname -> seetings -> add SSH key
    ```

5. 分别测试两个域名的链接
    ```PowerShell
    ssh -T git@blueeye   # @后面的是config里面代码库1自定义的域名
    Hi blueeyezhy! You've successfully authenticated, but GitHub does not provide shell access.
    ```
    ```PowerShell
    ssh -T git@miaoqu    # @后面的是config里面代码库2自定义的域名
    Hi miaoquertongjulebu! You've successfully authenticated, but GitHub does not provide shell access.
    ```
    链接测试成功；如果出现 `permission denied publickey` 显示拒绝访问，需要检查config内容，命令有没有输入错误，密钥有没有关联错误。

6. 取消本地Github全局用户名和邮箱的设置  
   shell中键入如下命令：
    ```PowerShell
    git config --global --unset user.name
    git config --global --unset user.email
    ```

7. Github本地库设置用户名和邮箱与远程库关联    
    1. 本地与远程都有代码库的情况下，需要重置代码库的链接（与id_rsa密钥关联）  
        进入本地代码库1的目录下，键入下面命令，配置id_rsa密钥关联的用户名和邮箱：
        ```PowerShell
        git config user.email blueeye_zhy@outlook.com   # 关联密钥id_rsa对应的邮箱
        git config user.name blueeyezhy                 # 关联密钥id_rsa对应的账号
        ```     
        shell命令: `git remote -v`，查看关联远程库 `origin/master` 的链接，结果如下：
        ```PowerShell
        origin  git@github.com:blueeyezhy/blueeyezhy.github.io.git (fetch)
        origin  git@github.com:blueeyezhy/blueeyezhy.github.io.git (push)
        ```
        shell命令: `git remote set-url origin git@blueeye:blueeyezhy/blueeyezhy.github.io.git`，用config中id_rsa密钥配置的域名 `blueeye` 替换掉 `githun.com`，然后用`git remote -v`查看结果：  
        ```PowerShell
        origin  git@blueeye:blueeyezhy/blueeyezhy.github.io.git (fetch)
        origin  git@blueeye:blueeyezhy/blueeyezhy.github.io.git (push)
        ```
        然后就可以用 `git push`；`git pull`；`git log` 自由玩耍了。
        当然也可以用 `git remote rm origin` 和 `git remote add origin git@***` 通过删除，添加的方式来重置地址，注意修改域名要与config中的密钥id_rsa对应。

    2. 本地没有代码库，远程有代码库的情况下，需要本地创建代码库（不添加内容），然后从远程库pull代码   
        shell命令 `mkdir miaoqu` 创建本地库目录；进入该目录，执行 `git init` 初始化本地库；键入下面命令，配置id_rsa_name密钥关联的用户名和邮箱；
        ```PowerShell
        git config user.email youremail@company.com     # 关联密钥id_rsa_name对应的邮箱
        git config user.name miaoquname                 # 关联密钥id_rsa_name对应的账号
        ```  
        （用 `git config --list` 命令可以查看当前库的配置信息）  
        获取远程库SSH链接：`git@github.com:miaoquname/miaoquname.github.io.git` 
        执行shell命令：`git remote add origin git@miaoqu:miaoquname/miaoquname.github.io.git`，用config中id_rsa_name密钥配置的域名 `miaoqu` 替换掉 `githun.com`，然后用`git remote -v`查看结果：
        ```PowerShell
        origin git@miaoqu:miaoquname/miaoquname.github.io.git (fetch)
        origin git@miaoqu:miaoquname/miaoquname.github.io.git (push)
        ```  
        然后，用 `git pull` 命令将远程库同步到本地；当然也可以用 `git clone` 来实现，注意修改域名。
        
    3. 本地有代码库，远程没有代码库的情况下，需要在远程创建项目代码库（不添加内容），然后从本地push到远程库   
        登录github远程，创建代码库不要添加`README.md`，获取远程库SSH链接：`git@github.com:miaoquname/miaoquname.github.io.git`   
        库根目录下，执行下面命令，配置id_rsa_name密钥关联的用户名和邮箱
        ```PowerShell
        git config user.email youremail@company.com     # 关联密钥id_rsa_name对应的邮箱
        git config user.name miaoquname                 # 关联密钥id_rsa_name对应的账号
        ```  
        然后执行：`git push -u origin master git@miaoqu:miaoquname/miaoquname.github.io.git`，用config中id_rsa_name密钥配置的域名 `miaoqu` 替换掉 `githun.com`，然后用`git remote -v`查看结果：
        ```PowerShell
        origin git@miaoqu:miaoquname/miaoquname.github.io.git (fetch)
        origin git@miaoqu:miaoquname/miaoquname.github.io.git (push)
        ```  
        然后就可以用 `git push`；`git pull`；`git log` 自由玩耍了。

## 所感

感触最大就是在总结的过程中，重新梳理了自己对非对称加密应用的理解和再次实践了git操作，在原理理解方面和实操方面有了不少的提升；  
真实项目是学习最好的驱动力，在项目进行的过程中学习效率是非常高的。

---
> [python学习总结(七)--Encryption and decryption-RSA](https://read.firesbox.com/posts/8ac4298f49b860f9ed6347f7c4a7acc85fa78a5483b79b88ba101eeba6775da1)    
> [python学习总结(六)--Encryption and decryption-DES](https://read.firesbox.com/posts/a5e467977c9a4f42947c6b5af2c5ed3e778fa3600d3f0def1284d51f60e7832b)    
> [python学习总结(五)--Encryption and decryption-1](https://read.firesbox.com/posts/88f057fa93c7f831e36014cd7b4538474c9f8ce4cb495cfd2535524c0ecbf033)    
> [python学习总结(四)--String parsing](https://read.firesbox.com/posts/7b71ead909c1b46fc5ac914e70d9d744a5bb019cf99757e28fcfc273d59c4671)   
> [python学习总结(三)--PyQt](https://read.firesbox.com/posts/d7b80845d7870c33960dc349b6b1765c4145e4afac3aac00f422b713ca8fa320)   
> [python学习总结(二)--Powershell](https://read.firesbox.com/posts/ffc76fa8634a3be98e4f7ca9e45d7b5b33a41a3f5374a8153eaa42daddd91997)  
> [python学习总结(一)](https://read.firesbox.com/posts/b4ebbc69f1e5e4ba1069f112dcfef65fd7238bce3c7a722fae78e0fb6976fe5c)  
---
**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，老虎证券王珊老师的**读财报课**，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，注册 [**Mixin**](https://mixin.one/) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mp.weixin.qq.com/s/ci_OWj9vtnsJ4OROifNfSQ) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)