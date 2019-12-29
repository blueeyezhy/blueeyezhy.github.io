# 字符串解析--Python学习总结(四)

> - **PressOne**: [张野](https://press.one/main/p/7c08521960497a61baf3f1c9760ff2a4cc66be1c)
> - [**Mixin**](https://mixin.one/) ID: 21120
> - **Github**: [@blueeyezhy](https://github.com/blueeyezhy)
> - **web**: [blueeyezhy.github.io](https://blueeyezhy.github.io/)

刷官网习题和自己编写计算器小工具的过程中，做了几次字符串的解析，在这里做个简单总结。

## 先上代码

1. [官网练习题](https://pythonbasics.org/dictionary/)
    > 1. Make a mapping from countries to country short codes
    > 2. Print each item (key and value)  
        >>**数据源**  
        >>...  
        >>AU-澳大利亚(AUSTRALIA)  
        >>AZ-阿塞拜疆(AZERBAIJAN(REPUBLIC))   
        >>B字头  
        >>BD-孟加拉(BANGLADESH)  
        >>BE-比利时(BELGIUM)  
        >>BF-布基纳法索(BURKINA FASO)  
        >>...  

    我将输出改为文件输出，增加文件读写，`json` 数据流的练习。

    ```python
    import re,json
    with open(r"./tmp/b.txt",'r',encoding="utf-8") as f:
        ls={}
        for i in f.readlines():
            t=list(i)
            # 剔除文件中的所有汉字
            for j in range(len(t)): 
                if ord(t[j])>127:
                    t[j]=""
            k="".join(t)
            # 匹配简称对应国家
            pttn=r"^.{2}-\(.{2,}"  
            if re.search(pttn,k):
                # 将匹配结果转化为字典
                n=k.split("-(")
                ls[n[0]]=n[1].strip(')\n').title()  
        # 讲字典转化成json数据
        s=json.dumps(ls,indent=4) 
        # 保存json数据 
        with open(r"./tmp/b.json",'w',encoding="utf-8") as fjson:
            fjson.write(s)
    ```

2. 计算表达式的值
    > 给定一个含有 `+,-,*,/,()` 字符串表达式，计算表达式的值。
        >>**例**  
        >>`表达式：'3*5+4*5/(2-2.0-(6-8)/9)/9-6*(5+4)'`  
        >>`输出结果：-29`

    这个是我上一篇总结中，编写的计算器的核心算法。

    ```python
    import re
    def milt(a):  # 计算乘除法
        if a[0] not in ["+","-"]:
            s=1
        elif a[0]=="+":
            s=1
            a=a[1:]
        elif a[0]=="-":
            s=-1
            a=a[1:]
        a=a.replace("*", ",*").replace("/",",/")
        l_a=a.split(",")
        for i in l_a:
            if i[0] not in ["*","/"]:
                m = float(i)
            elif i[0] == "*":
                m *= float(i[1:])
            elif i[0] == "/":
                m /= float(i[1:])
        return m*s

    def sum_str(a):  # 计算加减法
        pttn=r"[*/+-]-"   
        while re.search(pttn,a) != None:
            (n,m) = re.search(pttn,a).span()
            l_a = list(a)
            while l_a[n] not in ["+","-"] and n>0:
                n -= 1
            l_a.pop(m-1)
            if l_a[n]=="+":
                l_a[n] = "-"
            elif l_a[n]=="-":
                l_a[n] = "+"
            a="".join(l_a)
        a=a.replace("+", ",+").replace("-",",-")
        l_a=a.split(",")
        return sum(map(milt,l_a)) 

    def calculate(a):  # 匹配括号，递归计算括号内容得出结果
        dct={}
        pttn=r"\(.*?\)"
        l=re.findall(pttn,a)
        try:
            if len(l) != 0:
                for s in l:
                    for i in range(len(s)):
                        if s[-1-i] == "(":
                            tmp=str(sum_str(s[-i:-1]))
                            break
                    dct[s]=s.replace(s[-i-1:], tmp)
                for k in dct:
                    a=a.replace(k,dct[k])
                    print(a)
                return  calculat(a)
            else:
                return sum_str(a)
        except:
            print("Input error!")

    a='3*5+4*5/(2-2.0-(6-8)/9)/9-6*(5+4)'
    calculate(a)

    -29.0
    ```
## 总结与感受
1. 这类问题的解决流程  
   想要一次解决所有问题是非常非常困难的，也是不经济的，所有高效的流程是  
   > 1. 分析问题，将问题分解；
   > 2. 逐个解决拆分的问题，循序推进，最后输出结果；
   > 3. 优化，整合，减少资源消耗，最后输出代码。  
   
   如上面两个例子，第一个，先剔除汉字；然后正则匹配需要的内容；再然后对匹配结果进行清洗，生成字典；最后生成 `json` 并保存。    
   第二个，先完成计算只含有 `+,-` 符号的表达式代码；再完成计算只含有 `*/` 符号的表达式代码，作为函数被全面代码调用；再对 `()` 进行识别，调用前面两个计算表达式的函数；最后完成多重 `()` 的递归调用，输出结果。

2. 分支语句  
   分支语句的条件表达式必须满足**互斥且互补**，即各分支之间没有交集，分支之和等于总集合。否则就会出现意外的错误，这个相信大家在学习的时候都学过，而在实际的代码编写过程中往往会有遗忘，导致异常。我自己犯过这样的错误，为了以后不再犯，再写分支代码块的时候，先将表达式全部写完，然后再逐一补充代码块。养成这个习惯，为以后高效写代码打下基础。  
   另外，异常处理 `try: ... ; except: ... ; finaly: ...` 代码块也属于这一类。


3. 刻意练习，是提高代码能力和算法能力的有效手段   
   在做习题，解决问题的时候可以刻意的增加一些额外内容让自己训练，例如文件读写，数据流操作，函数调用，递归等等。在读[《自学是门手艺》](https://xue.cn/) 的时候，李老师举了一个计算单词字母和等于100的例子。为了强化练习，我在 `Git` 上 `fork` 并下载了所有英文单词的文件，自己完成了一遍寻找符合条件单词的过程。通过这个过程，我将 `Git` 操作，文件读写，逻辑运算又复习了一遍。


---
> [python学习总结(一)](https://read.firesbox.com/posts/b4ebbc69f1e5e4ba1069f112dcfef65fd7238bce3c7a722fae78e0fb6976fe5c)  
> [python学习总结(二)--powershell](https://read.firesbox.com/posts/ffc76fa8634a3be98e4f7ca9e45d7b5b33a41a3f5374a8153eaa42daddd91997)  
> [python学习总结(三)--PyQt](https://read.firesbox.com/posts/d7b80845d7870c33960dc349b6b1765c4145e4afac3aac00f422b713ca8fa320)
---
**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，注册 [**Mixin**](https://mixin.one/) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mp.weixin.qq.com/s/ci_OWj9vtnsJ4OROifNfSQ) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)