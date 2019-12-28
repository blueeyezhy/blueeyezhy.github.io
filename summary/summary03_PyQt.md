# 计算器实战(Tkinter&PyQt) -- Python学习总结(三)

> - **PressOne**: [张野](https://press.one/main/p/7c08521960497a61baf3f1c9760ff2a4cc66be1c)
> - [**Mixin**](https://mixin.one/) ID: 21120
> - **Github**: [@blueeyezhy](https://github.com/blueeyezhy)
> - **web**: [blueeyezhy.github.io](https://blueeyezhy.github.io/)


## 0.开始
刷完 [**官网 Exercises**](https://pythonbasics.org/) 的 `Tkinter` 和 `PyQt` 的模块，觉得对于窗体，控件，以及他们之间的关系掌握的有点模糊。于是决定编写一个窗口视图程序来强化一下自己对知识的掌握，我选择编写一个计算器，因为我觉得它简单，控件多，能够全面强化和检验自己所学到的知识；同时也觉得这些知识的掌握对以后学习**web**程序和移动端**APP**有帮助。借助于[李俊老师讲编程实例](https://www.bilibili.com/video/av76528595/)的思想，将 **JupyterLab** 作为实验的广场，主体在 **VS code** 里面实现，如此开始我的第一个程序之旅。

## 1.任务分解，明确需求 
1. UI设计  
   计算器原型是手机里自带的计算器(如下图)，实现其全部功能。

   ![手机计算器](https://static.press.one/4c/ec/4cec2cb2bc66311841ca0fb17a6b41f469b216efe470f2673b7bd0e61291366f.jpg)
   
   这计算器控件种类比较单一，于是我增加了 `QRadioBuRtton` 和 `QTabWidget` 控件增加练习内容；布局采用相对布局，控件随着窗口的拖拽放大延展。  
   最后UI定形为：
   
   ![计算器](https://static.press.one/ba/8a/ba8aee9138471e91e42527b28d1d29d66b6caaac1123c355d7380bd0812aabc1.jpg)

2. 数据传递  
   完成41个 `Pushbutton`, 3个 `Radiobutton` 和一个输出 `Textbrower` 数据传递与接受显示，同时增加键盘点击的联动。


3. 核心算法  
   计算表达式的值是这个小工具的核心算法，特别是在有四则运算和括号的时候，如何解析字符串并计算出结果。这个功能会涉及，正则，递归以及字符串操作等方面的知识，是个难点。

4. 生成 .exe 文件，上传 Git 及个人主页，官网上有教程，容易完成。


## 2.遇到问题点及解决方案
1. UI设计   
   Anaconda 集成了 Qt Designer 这个UI设计的窗口试图工具，在 powershell 输入：`designer` 命令可以调出 Qt Designer 进行 UI 设计。 完成 UI 设计后在 powershell 输入：`pyuic5  filename.ui  -o  filename.py`，将 `.ui` 文件转化成 `.py` 文件，进行后续的代码编写。(下图是 Designer 的界面)

   ![designer](https://static.press.one/92/54/925436045b9710510eb6d14d03c540d16ca1b741303b5feffbb5baa1b67a0f8f.jpg)
   
   为更好的理解控件，控件的布局，控件间结构关系，我没有使用 Qt Designer，而是直接通过代码的方式实现 UI 设计。下面是在实现过程中我所遇到的问题点，也是后续学习中需要注意的事项: 
   1. 类只有实例化以后才能被布局：  
        ```python
        v_4_2 = ["-", "+"]
        for i in v_4_2:
            b_tmp = QPushButton(i)  #实例化一个按钮
            b_tmp.setObjectName(i)  #设置按钮名字
            b_tmp.setShortcut(i)    #设置按钮键盘输入快捷键
            b_tmp.setSizePolicy(size_policy)  #设置延展属性
            tab_1_widget_h4_2_layout.addWidget(b_tmp) #布局按钮
        ```
    1. 自动布局分为横向布局 `QHBoxLayout()`，纵向布局 `QVBoxLayout()` 和栅格布局 `QGridLayout`，这些布局也都是类，也必须实例化以后才能对实例进行操作。还有一个重要的点是要清楚布局绑定在什么控件上，对那些控件进行布局。举例说明：
        ```python
        self.tab_2 = QWidget()  #实例化一个 QWidget() 对象，赋值给 self.tab_2
        self.tab_widget.addTab(self.tab_2, "function") #将对象 self.tab_2 绑定在self.tab_widget对象上，显示为 "function" 。

        tab_2_layout = QGridLayout(self.tab_2) #实例化一个栅格布局对象 QGridLayout()
        tab_2_layout.setSpacing(0) #设定这个栅格布局内的对象间距为0.

        f_list = ["(", ")", "x!", "xˉ¹", "x²", "x³", "xⁿ", "√x", "ⁿ√x", \
            "e", "ln", "log", "sin", "cos", "tan", "π", "Deg", "lnv"]
        n_tmp = 0
        for i in range(6):
            for j in range(3):
                b_tmp2 = QPushButton(f_list[n_tmp]) #实例化QPushButton()对象
                b_tmp2.setObjectName(f_list[n_tmp]) #设定对象名
                b_tmp2.setSizePolicy(size_policy)   #设定对象延展属性
                tab_2_layout.addWidget(b_tmp2, i, j) #将这个按钮对象添加到tab_2_layout布局对象上。
                n_tmp += 1
        ```
2. 表达式值的计算  
根据需求，点击每一按钮执行的结果都要显示在 `QTextBrowser` 控件上的，所以这个计算必须做成一个函数被频繁调用。最开始构想这个函数的时候，是想通过递归方式对包含括号的表达式内容进行解析。在寻找参考的时候发现了 Python 的内置 `eval` 函数，可以完美实现需求的功能，本着完成优先于完美的原则，就使用这个函数完成核心算法了。对于递归和字符串的解析，以后会在爬虫以及其他地方练习到。 
   
3. `RadioButton` 事件的触发  
   三个 `RadioButton` 控件是一个组合，绑定一个函数；在测试的时候，每次函数都被调用了两次。查找了好久才发现我是通过
`.toggled.connect` 绑定事件的 `self.num_system_d.toggled.connect(self.num_system_onClicked)`。 而这个事件触发方式是发生状态变化时调用函数。因为三个 `RadioButton` 时一个组合，如果点亮其中的一个，则原来已经点亮的  `RadioButton` 就会变暗，所以一个点击动作产生了两个状态变化，所有就调用了两次。解决方案时将触发方式从 `.toggled.connect` 变换成 `.clicked.connect` 方式，即 `self.num_system_d.clicked.connect(self.num_system_onClicked)` 于是完美解决。

4. 方法()与属性  
   在编程过程中，非常容易犯的错是调用方法的时候没有加括号，执行的是时候获取不到想要的数据。例如 `.objectname()` 它本身是一个类方法，如果忘记了()，就获取不到对象的名字。
   
5. 控件间信息传递  
   这个过程中一定要分辨清楚变量的作用域，全局的要用 `self.XXX`, 局部不用加 `self` ，同时也需要记住尽量少用全局变量，以减少资源的消耗。  
   另外有一点，当需要在方法中获取执行这个方法的控件时，需要使用 `self.sender` 类。  
   例如：在实例化控件的时候给控件绑定一个方法 `self.button1.clicked.connect(self.func2_clicked)` ， 在 `func2_clicked(self)` 这个方法中要调用 `self.button1` 控件的名字时，需要用到 `self.sender()` 类实例化一个 `sender` 对象指向这个控件。

    ```python
     def func2_clicked(self):
        sender = self.sender() #实例化self.sender对象, 指向这个函数的调用控件。
        name = sender.ojectName() #获取被点击的这个控件的名字赋值给name。
    ```

6. `findchildren()` 与 `findchild()`方法  
   编程过程中往往需要查找控件，然后对找到的控件进行操作。 `findchildren()` 比较好理解，通过这条语句 `btn_list = self.findChildren(QPushButton)` 就可以获得这个窗体全部 `QPushButton` 的列表。但是 `findchild()` 的用法则不同，它的语法是 `btn = self.findChild((QPushButton,), "name")` 注意其中第一个参数是需要寻找控件类开始的**元组**，第二个参数是需要寻找的控件名。

    ```python
    func = [("sin", "sinˉ¹"), ("cos", "cosˉ¹"), ("tan", "tanˉ¹"), ("ln", "eⁿ"), ("log", "10ⁿ")]
        for j in range(5):
            for i in range(2):
                if self.findChild((QPushButton,), func[j][i]): #注意第一个参数是元组。
                    btn = self.findChild((QPushButton,), func[j][i]) #注意第一个参数是元组。
                    if i == 0:
                        k = 1
                    elif i == 1:
                        k = 0
            btn.setObjectName(func[j][k])
            btn.setText(func[j][k])
    ```

7.  `pylint`  
   VS code中的 `pylint` 非常好用，他会帮助程序员检查代码的错误，发出警告。通过它会可以帮助程序员排查错误，养成很好的代码习惯，为以后的协作打下基础。当然，规则设定上也有一些非常苛刻的地方，比如：每行代码容量上线默认是80个, 用起来很不爽。这个可以通过修改个人设定进行修改。
   `settings` -> 打开 `setting.json` 文件，在两个参数 `"python.linting.pylintArgs":` 和 `"python.linting.flake8Args":` 设定中加入 `"--max-line-length=248"`
   ![vscode](https://static.press.one/28/02/28024a624bf096cded81240b687e8ff546378521c74d227c5ec66ea7b43f02fb.jpg)

## 3.所感
**完成比完美更重要**：这句话李笑来老师在讲他新书创作的过程中重点强调过的，我在这个实战编程中也深有感受。长时间没有出成果，自己的心力会受到不良的影响，以至于我放懒了一段时间，走偏了一段路；意识到以后，放宽细节先完成了再说。当看到自己的产品完成时感觉确实很爽。后续有时间会逐渐优化这个小工具的。

**解决实际问题**：是快速成长的原动力，这点大家都懂，[李俊老师在阶段总结](https://www.bilibili.com/video/av77348095/)里面也说过类似的话。我在学习编程的时候有真实感受，比如关于 `findChild()` 方法的使用，花了好多时间排查和搜索，当最后解决的时候心里还是有一份小激动的。

**魔鬼在细节里**：编程中细节会给我们带来很多麻烦，比如 `=` 与 `==`, 再比如 `\` 转义字符，再比如有没有 `()` ，再比如变量的定义后，再次被赋值时一定要注意数据类型，再比如函数传参的数据类型等等。这些都是需要在实践中逐渐养成肌肉记忆的。

**基本单元**：两个基本逻辑单元在编程中理清后，对编程乃至人生都有很大的帮助。  
> **`A.c(B)`**: 主体 **`A`** 执行动作 **`c()`** 作用在客体 **`B`** 上  
> **`C(a)=>b`**: 输入 **`a`** 通过过程 **`C()`** 输出 **`a`**

## 4.最后
能够完成一个可以执行的小程序，对我自己来说是非常大的鼓舞，再接再厉。小程序及 `.py` 文件已经上传到 `Git` 和个人主页上了，有兴趣的小伙伴儿可以自行下载，相互切磋。

---
> [python学习总结(一)](https://box.prsdev.club/posts/b4ebbc69f1e5e4ba1069f112dcfef65fd7238bce3c7a722fae78e0fb6976fe5c)  
> [python学习总结(二)--powershell](https://box.prsdev.club/posts/ffc76fa8634a3be98e4f7ca9e45d7b5b33a41a3f5374a8153eaa42daddd91997)
---
**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，注册 [**Mixin**](https://mixin.one/) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mp.weixin.qq.com/s/ci_OWj9vtnsJ4OROifNfSQ) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)