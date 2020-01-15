# Django框架--学习总结(十一)

Dajango 是 python 的 web 应用框架之一，应用非常广泛。作为这阶段我的学习目标，读完了三本关于 Django 的书，边读边实践复制完成了一个基于 Dajongo 的论坛项目，做个总结整理一下实践中的问题和心得。 

三本书中，xue.cn 上有两本，还有一本是 [《A Complete Beginner's Guide to Django》](https://simpleisbetterthancomplex.com/series/beginners-guide/1.11/)。总体评价，xue.cn 上的这两本成书质量一般，对于想要进阶的初学者来说并不是最好的选择，而上面这部英文书（虽然是全英文，但是很简单，英文有一点基础的人都可以阅读和实践下去的）从项目思路，代码质量，测试控制等方面循序渐进的演示了一个真实项目的推进过程，我也是跟着这本书完成了自己的第一个成型 web 应用。这本书真的很好，极力推荐。   

由于这本书是2017年完成的，之后 Django 升级为2.0版本，所以书中的部分代码需要修改过后才能执行。而这个查找，修改过程对于我的成长也有很大帮助。这些问题以外，书中的代码全部亲测可以执行。

## 问题与解决

1. 由于 Django 升级，代码库进行修整，部分包找不到    
    书中代码：  
    ```python
    from django.core.urlresolvers import reverse
    from django.urls import resolve
    ```
    当前版本的实践代码：  
    ```python
    from django.urls import resolve, reverse
    ```
    这两个函数是单元测试程序中最重要的两个函数，框架升级后全部都保存在 `urls` 包中。其中 `reverse` 函数是接收 `utl` 的 `name` 以及其他参数来反向解析出 `url` 的函数，用于测试链接跳转页面是否是我们期望的页面。而 `resolve` 函数是测试 `veiw` 指定的 `url` 是否和设计预想的页面一致。详细对比大家一看代码就会明白的。

2. 框架升级后，视图中匹配 `url` 的函数由 `conf.urls` 包中的 `url` 函数，变为 `urls` 包中的 `path` 和 `re_path` 函数。引入代码从：    
    ```python
    from django.conf.urls import url
    ```
    变为：
    ```python
    from django.urls import path, re_path
    ```
    其中 `path` 是根据Django自己定义的 `url` 匹配语法进行匹配的，而 `re_path` 函数是按照正则语法进行 `url` 匹配。（我用这个函数进行匹配）

3. 数据库模型中外键一对多关建立模型是的时候，增加了 `on_delete` 参数来指定级联删除的方式，`on_delete=models.CASCADE` 表示当删除主表的数据时候从表中的数据也随着一起删除。如果不指定这个参数的话，数据库迁移会报错。
    ```python
    updated_by = models.ForeignKey(User, null=True, related_name="+")
    ```
    修改为：
    ```python
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="+")
    ```

4. 关于字符串引用问题   
    我写的代码是这样的：
    ```python
    board_topics_url = reverse("board_topics", kwargs={"pk": self.board.pk})
    self.assertContains(self.response, "href='{0}'".format(board_topics_url))
    ```
    执行后报错 `AssertionError: False is not true : Couldn't find 'href='/'' in response`，是因为Django获取字符串用的单引号内嵌套双引号 `'str/"{}"str'`，而我习惯上用双引号套单引号传递字符串参数 `"href='{0}'"` ，结果程序执行的时候就变成了`'href='/''` 两个str夹一个斜杠，比配不到，所以报错。用Django进行编程的时候，对字符串的引用一定要用单引套数双引 `'href="{0}"'` ，这点需要注意。正确代码：
    ```python
    board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
    self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))
    ``` 

5. Python 2升级到python 3，字符串解码直接生成str类型。而2版本需要通过bytestrang作为中转。所有书中的代码会报错：
    ```python
    uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
    ```
    正确代码：（去掉decode函数）
    ```python
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    ```


## 所感

完整的跟着做了一个应用，在实践中学习感受模型，视图+模板，路由控制各自功能，三者之间的关系，以及如何交互协作。对于web应用框架有了一个整体的理解。

实践中感触最深的莫过于测试驱动的编程了。模块的开发与单元测试编程同时推进，工作量虽然大了一点；但是对于代码的质量绝对是有信心，同时也能预见到代码的维护也会非常简单。    
单元测试内容（做个列表我复习一下，也给你留个整体印象）：    
> 对于每一个视图+模板都要进行下面几个单元测试
> * 响应状态确认（response.status_code ？= 200）
> * 未找到请求时是否返回404（response.status_code ？= 404）
> * 回调url是否正确（response ？= redirection）
> * 实行执行返回的页面是否正确（类形式，函数形式2中，都可以）
> * 响应数据中是否包含指定链接
> * 验证响应中是否包含，加密中间件的csrf（response ？包含 csrf）
> * 响应中的 form是否与设定form类型一致
> * 响应中的输入与输出参数的类型和数量是否正确
> * 接收到非法输入或者零输入后是否返回错误信息
> * 请求数据中的数据与模型定义是否一致，非法输入是否返回错误信息
> * 用户登录验证，新用户返回注册，老用户验证权限和token
> * 用户注册非法输入响应，合法输入响应
> * 邮件验证的id和回调链接是否正确
> * 重置密码回调链接
> * 密码重置功能是否有效，成功后的回调，失败后的回调是否正确



最后一步是web应用的部署上线，一直以来听说的是部署很神秘，繁琐，是耗费精力和时间的步骤。经历过了，才知道它跟我们安装软件本质是一样。就是在空的服务器上安装配置软件所需要的资源和链接，不同的是服务器只有最基础的操作系统。绝大多数情况都是Linux系统，没有显示器，还需要程操作。所以必须要学习Linux系统的操作，虚拟环境的搭建，安装依赖工具包，配置环境变量，数据库远程安装与配置，静态文件配置，wed服务配置，负载均衡配置等。需要的对web应用结构，运行过程，相关资源非常熟悉。为了能够使部署工作顺利进行，在实现代码的过程中就要一个项目创建一个虚拟环境，仅仅安装必要的工具包，定期跟踪依赖文件，搞清楚每个依赖文件的作用，以及用在自己应用的什么地方；这样最后部署上线额时候就不会由太多的麻烦了。


---
> [python学习总结(十)--Protocals](https://read.firesbox.com/posts/7e409fc4518288870abe6b8c2fc850fe9c70e5ad3f82f53565760fa0652df861)  
> [python学习总结(九)--PressOne Protocal](https://read.firesbox.com/posts/22129abc8b6989cd088b793ffe1096fa15a5eb3a3e17b9f97a19f4c6b67f3d1e)     
> [python学习总结(八)--Github 1 to 2](https://read.firesbox.com/posts/4c2e85b07c27665426ceaadc9a5b8905b34c11c3fa759e6a7067a7a48f4935e1)    
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
