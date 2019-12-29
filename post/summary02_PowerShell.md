# 学习中遇到的PowerShell -- python学习总结(二)

> - **张野** ，**PMP**，**CFA**在读
> - **Github**: [@blueeyezhy](https://github.com/blueeyezhy)
> - **web**: [blueeyezhy.github.io](https://blueeyezhy.github.io/)
> - **PRESSone**: [张野](https://press.one/main/p/7c08521960497a61baf3f1c9760ff2a4cc66be1c)
> - [**Mixin**](https://mixin.one/) ID: 21120

## 0.源起   
这篇总结源起于和李俊老师在 `Git` 上的对话，于初学的我对 PowerShell 现在的理解是够用了。再深入的东西我也不知道，也不是当前时点的重点。

![yulilaoshideduihua](https://static.press.one/20/34/2034b10d4f784b98a025ef0a8ec43cc9b53fc11d03c7f219c38f6ff74c0dd661.png)


## 1.CMD 与 Windows PowerShell
**CMD**：左下角Windows图标右键 -> 点'运行' -> 输入'cmd'回车。  
**Windows PowerShell**：左下角Windows图标右键 -> 点'运行' -> 输入'powershell'回车。(蓝色背景的窗口感觉很舒服)  

CMD 是直接跟 os(操作系统) 对话的命令入口，可以执行 os 内部命令，以及在环境变量(下面会说明在哪里找)中path参数配置的路径下面的可执行程序和脚本文件。

PowerShell 是全兼容CMD所有功能，同时支持一些我们常用的shell命令，如 `ls` ，`dwg`，`clear` 等。这些命令在学习编程的过程中经常会使用到，所有用 PowerShell 方便很多。(fig1所示)

![img](https://static.press.one/46/ac/46ac9626f50983e93452d82b57d4220633cd7451535bdf7b8bb42a500c1017e7.png)

## 2.Anaconda prompt 与 Anaconda PowerShell prompt
Anaconda prompt 与 Anaconda PowerShell prompt 是安装 Anaconda 这个 Python 开发执行环境时自动安装的。保存在Anaconda的安装目录中，里面集成了 Jupyter, Python, canda, VS code(如果选择安装的话) 等执行程序及脚本文件。 其中 Anaconda prompt 相当于 CMD 可以和 os 对话，但是不支持部分shell命令；Anaconda PowerShell prompt 相当于 Windows PowerShell ，兼容 Anaconda prompt 并支持 shell 命令。

所有通过这两各终端，都可以运行 Jupyter Lab，启动 Python 交互，执行 canda 命令，启动 VS code。 但是，在安装 Anaconda 的时候，这几个可执行文件或脚本文件的路径，没有被配置到 os 环境变量的 path 中，所以使用 CMD 及 Windows PowerShell 时，无法执行 `canda install ***` ，` code ***` ，`jupyter lab`等命令。  (fig2所示)

对于，喜欢蓝屏的我来说，为了能在 Windows PowerShell 中执行这些程序和命令，我需要将这几个程序和脚本文件的路径配置到环境变量的path中。具体步骤如下图，按着红色的圈圈点 (程序的路径可以自己搜索，也可以参考图中我的路径，基本不会有问题的)。 找不到 “我的电脑” 的自己去搜索。对于，独立安装 VS code的也增加一下path路径，这样就可以直接在 PowerShell 启动 VS code了。

![img](https://static.press.one/fb/3c/fb3cc8da633c4fcf4db5c77b56adb163aea39905d95639699ad84b5a44945698.png)

**npm** 是个包管理工具，这执行 Jupyter lab 的时候，这个工具一直管理着包的载入和执行，所以不能关，否则 Jupyter lab 就执行不了了。

## 3.虚拟运行环境设定  
在创建虚拟运行环境 `conda create --name $ENVIRONMENT_NAME python` 的时候会报错，提示权限问题。这个时候以管理员身份运行 Windows PowerShell 执行上述命令就可以创建虚拟环境了。

## 4.最后    
学习很重要，练习很重要，之后的总结输出也很重要。如果不是为了这篇总结输出，我也不会对 cmd，powershell 与 os 与环境变量，与 path 有这番了解。


---
> [python学习总结(一)](https://press.one/files/4c7f8014a7c4d8a3bdeb04207171c096b59d27765458429129bd07a060dee68a)
---
**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，注册 [**Mixin**](https://mixin.one/) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mp.weixin.qq.com/s/ci_OWj9vtnsJ4OROifNfSQ) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)