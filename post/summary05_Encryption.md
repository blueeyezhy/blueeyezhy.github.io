# 加密与解密1--Python学习总结(五)

> - **PressOne**: [张野](https://press.one/main/p/7c08521960497a61baf3f1c9760ff2a4cc66be1c)
> - [**Mixin**](https://mixin.one/) ID: 21120
> - **Github**: [@blueeyezhy](https://github.com/blueeyezhy)
> - **web**: [blueeyezhy.github.io](https://blueeyezhy.github.io/)

前段时间学习了[《卓克·密码学30讲》](https://m.igetget.com/share/course/pay/detail?id=Enb9L2q1e3OxKBmfPXrgN8P0Rwo6B7)，加上现在学习`python`，就想着用编程的方式实践这些加密过程。

## 密码学的发展脉络(源自卓克老师)
为了方便说明做如下设定： 
> A = 信息的发出者；要发出的信息称为**原文**  
> B = 信息接收者；  
> C = 信息传递者； 传输过程中的信息称为**密文**   
> E = 信息的偷听者；  
>过程：A 加密后，通过 C 把**密文**传递给 B ， B 解密获得信息，不让 E 知道**原文**内容。

### 古典密码学--以字母为单位的加密算法
1. 第一代加密法--隐藏法  
   A 把信息藏在 C 身上；C 把信息带给 B；B获取到信息。
   隐藏的方式有很多种(涂层，人类 C 的头皮，不可见药水等等)；其破解方法就是 E 靠体力的搜查捕获 C 以获得信息。对 E 来讲破解方法全靠经验积累和体力排查，对 A，B 来说传输效率低。

2. 第二代加密法--移位法和替代法  
   A 把信息内容的每一个字符用移位或者特殊字符替代，然后通过 C 传递给 B。
   这样，E (包括 C ) 在不知道移位和替换规则的情况下，即使获得了**密文**，也不知道**原文**的内容。这类加密方法还有一些变种，如倒序，奇偶位变化，首尾相连等不同的方法。  
   下面是模拟这种加密算法的代码：将信息 `Long Bitcoin, Short The World!` 加密成**密文**；及将**密文**解密为**原文**。

   ```python
    class encode_decode():
    def __init__(self, origin_info="", cipher_info=""):
        # 密码本(原文:密文对照表，是由字母移位，以及部分特殊字符替换形成的)
        self.origin_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self.cipher_str = "NOPQRSTUV+XYZABCD=F~HIJKLMnopqrstuvwxyzabcd>fghijklm"
        self.origin_info = origin_info
        self.cipher_info = cipher_info 

    def encode(self, origin_info):
        # 加密函数
        tmp = []
        for i in range(len(origin_info)):
            for j in range(len(self.origin_str)):
                if origin_info[i] == self.origin_str[j]:
                    tmp.append(self.cipher_str[j])
                    break
            else:
                tmp.append(origin_info[i])      
        self.cipher_info = "".join(tmp)
        return self.cipher_info
        
    def decode(self, cipher_info):
        # 解密函数
        tmp = []
        for i in range(len(cipher_info)):
            for j in range(len(self.cipher_str)):
                if cipher_info[i] == self.cipher_str[j]:
                    tmp.append(self.origin_str[j])
                    break
            else:
                tmp.append(cipher_info[i])
        self.origin_info = "".join(tmp)
        return self.origin_info

    coding = encode_decode()
    origin_info = "Long Bitcoin, Short The World!"

    # 原文加密
    cipher = coding.encode(origin_info)
    print(f"cipher: {cipher}")
    
    # 密文解密
    origin_info = coding.decode(cipher)
    print(f"origin: {origin_info}")

    [OUT]
    # 密文输出
    cipher: Ybat Ovgpbva, Fub>g ~ur Jb>yq!
    # 解密输出原文
    origin: Long Bitcoin, Short The World!

   ```
   第二代加密法一直统治着加密世界，直到16世纪数学的概率方法出现，这个加密法才宣告被破解 。
   其破解原理很简单，就是英文中字母出现的频率是不一样的。比如，字母 e 是出现频率最高的约占12.7%；其次是字母 t，9.1%；然后是 a, o, i, n等，最少的是z，只占 0.1%。(除了英文之外,其他语种统计也有[字母频率](https://wiki.tw.wjbk.site/zh-hans/%E5%AD%97%E6%AF%8D%E9%A2%91%E7%8E%87))。再加上其他规则，首字母频率，连续相同字母出现的频率，从而大幅度降低字母排列组合的可能。然后通过于几篇密文进行对照筛选，就可以获得密码本，进而就可以破译密文的内容。后来虽然出现了同音替代等增强版的变种加密法，只需要通过增加语言习惯，频率规则，**密文**最终都被会被破译。

3. 第三代加密法--维吉尼亚加密法  
   随着频率分析法的出现，替代法加密不好使了；为了对抗频率分析法，第三代维吉尼亚加密法出现了。其原理：在维吉尼亚加密法中，对于一个字母进行多套符号的替代，这样这个字母的频率特性就会消失，频率分析法就失效了。
   这个方法需要两个要素，一个是密码本(26x26字母对应矩阵)；另一个是替代规则，也就是"钥匙"，必须绝对保密。从这时候开始以后的加密算法就再也离不开"钥匙"了。 
   维吉尼亚加密法的代码实现如下：
   ```python
    class encode_decode():
        def __init__(self, origin_info="", cipher_info="", key=""):
            # 钥匙，循行定义使用那一套密码
            self.key = key
            self.origin_info = origin_info
            self.cipher_info = cipher_info
            # 密码本(原文:密文对照表，26*26)
            self.cipher_matrix = (("a", "abcdefghijklmnopqrstuvwxyz"),
                                ("b", "bcdefghijklmnopqrstuvwxyza"),
                                ("c", "cdefghijklmnopqrstuvwxyzab"),
                                ("d", "defghijklmnopqrstuvwxyzabc"),
                                ("e", "efghijklmnopqrstuvwxyzabcd"),
                                ("f", "fghijklmnopqrstuvwxyzabcde"),
                                ("g", "ghijklmnopqrstuvwxyzabcdef"),
                                ("h", "hijklmnopqrstuvwxyzabcdefg"),
                                ("i", "ijklmnopqrstuvwxyzabcdefgh"),
                                ("j", "jklmnopqrstuvwxyzabcdefghi"),
                                ("k", "klmnopqrstuvwxyzabcdefghij"),
                                ("l", "lmnopqrstuvwxyzabcdefghijk"),
                                ("m", "mnopqrstuvwxyzabcdefghijkl"),
                                ("n", "nopqrstuvwxyzabcdefghijklm"),
                                ("o", "opqrstuvwxyzabcdefghijklmn"),
                                ("p", "pqrstuvwxyzabcdefghijklmno"),
                                ("q", "qrstuvwxyzabcdefghijklmnop"),
                                ("r", "rstuvwxyzabcdefghijklmnopq"),
                                ("s", "stuvwxyzabcdefghijklmnopqr"),
                                ("t", "tuvwxyzabcdefghijklmnopqrs"),
                                ("u", "uvwxyzabcdefghijklmnopqrst"),
                                ("v", "vwxyzabcdefghijklmnopqrstu"),
                                ("w", "wxyzabcdefghijklmnopqrstuv"),
                                ("x", "xyzabcdefghijklmnopqrstuvw"),
                                ("y", "yzabcdefghijklmnopqrstuvwx"),
                                ("z", "zabcdefghijklmnopqrstuvwxy"))

        def encode(self, origin_info, key):
            # 加密函数
            num_key =list(map(lambda x: ord(x)-ord("a"), list(key)))
            tmp = []
            for i in range(len(origin_info)):
                for j in range(len(self.cipher_matrix)):
                    if origin_info[i] == self.cipher_matrix[j][0]:
                        tmp.append(self.cipher_matrix[j][1][i%len(num_key)])
                        break
                else:
                    tmp.append(origin_info[i]) 
            self.cipher_info = "".join(tmp)
            return self.cipher_info
            
        def decode(self, cipher_info, key):
            # 解密函数
            num_key =list(map(lambda x: ord(x)-ord("a"), list(key)))
            tmp = []
            for i in range(len(cipher_info)):
                for j in range(len(self.cipher_matrix)):
                    if cipher_info[i] == self.cipher_matrix[j][1][i%len(num_key)]:
                        tmp.append(self.cipher_matrix[j][0])
                        break
                else:
                    tmp.append(cipher_info[i])
            self.origin_info = "".join(tmp)
            return self.origin_info

            
    coding = encode_decode()
    key = "bitcoin"
    origin_info = "long bitcoin, short the world!"
    
    # 原文加密
    cipher = coding.encode(origin_info, key)
    print(f"cipher: {cipher}")

    # 密文解密
    origin_info = coding.decode(cipher, key)
    print(f"origin: {origin_info}")

    [OUT]
    # 密文输出
    cipher: lppj gotdqlr, siqux zhf zswrd!
    # 解密输出原文
    origin: long bitcoin, short the world!

   ```
   由于密码本是 26x26 (26套移位法密码本)的矩阵，而钥匙又有大数量级的可能性，所有同样原文对应上亿种密文，同样的密文也一样对应着上亿种原文。这才是维吉尼亚加密法难以破解的关键。但是这也不意味着这种加密方法没有办法破解，破解方法比较烧脑，大致分为：
   > 1. 从密文中找出完全相同的字母串。 
   > 2. 计算各个完全相同字母串的间隔，根据间隔数公约数的方法确定钥匙的位数。
   > 3. 根据钥匙的位数将，将全文按照钥匙的位数分成钥匙位数个组。比如钥匙是4位，那么把第1,5,9...字母分成第一组; 第2,6,10...字母分成第二组; 第3,7,11...字母分成第三组; 第4,8,12...字母分成第四组。
   > 4. 将上面的各组，分别应用频率分析法，确定出各组的移位，继而确定了钥匙。

   但是这个过程需要大量密文支撑，同时钥匙的长度增加，使得密文中没有完全相同的字母串重复出现，那么这套加密方法就非常可靠了。
   
   这样的钥匙也需要好传播和记忆，所以一般会是一首诗或者一篇其他的文章，以方便大家约定规则。可是一旦有了规律，就会有可能被通过对照猜测的方法推断出密钥的。所以最后的维吉尼亚加密法中的钥匙发展成为一个长的随机字母串，这样的加密法就非常可靠了，几乎没有办法破解。

   但是受限于当时的条件，在人工加密的过程中工作量巨大，且非常容易出错，安全性虽然高，但是效率非常低，所有这套加密法没有被广泛应用。  
   这个年代的密码世界里有一个传奇故事--[**比尔密码**](https://wiki.tw.wjbk.site/zh-hans/%E6%AF%94%E5%B0%94%E5%AF%86%E7%A0%81)，挺有意思有兴趣可以找来看看。  

4. 第四代加密法--恩尼格玛机加密   
   随着蒸汽机，电报，无线电，等机械电子技术的发展，以及战争因素的影响，第四代加密法诞生了。其原理本质上仍然是第三代的维吉尼亚加密法。其原文输入，加密过程，密文输出是通过，由齿轮，键盘和电路制造成的26x26x26...的密码本，和通过操纵杆，齿轮的初始值进行随机设定的钥匙，及钥匙的钥匙实现的。钥匙每天随机产生，都不定时更换，兼顾可操作性的同时大大提高了安全性。这样加密和解密过程的而工作量大幅消减，准确率大幅提升使得，其在二战种大方异彩。python代码实现和上面维吉尼亚一样，只不过扩大了密码本的维数和钥匙的位数。

   恩尼格玛机的破译是大神图灵在科学家和军队的支持下破译的。因为恩尼格玛机是机械电子设备，所以搞清设备的机械电子结构成为破译的关键，另外还有一些你要的条件：
   > 1. 搞清军用恩尼格玛机机械电子结构
   > 2. 大量密文供统计分析
   > 3. 捕获德国潜艇获得真实恩尼格玛机和一本钥匙薄
   > 4. 德军士兵在使用恩尼格玛机时，经常不按规范操作
   > 5. 盟军采用诱骗战术让德军故意发送特定词语   
   
   从这些条件可以看出恩尼格玛机破译是建立在，数学，人性，间谍通力协作下完成的。详细过程可以参看[《卓克·密码学30讲》](https://m.igetget.com/share/course/pay/detail?id=Enb9L2q1e3OxKBmfPXrgN8P0Rwo6B7)

### 由于中文字符都是表意字符，不存在移位，所以中文的古典加密发展的很慢。


### 这篇总结先到这里，下一篇将进入到现代密码学
* 现代密码学--以二进制数字为单位的加密算法， 
* 第五代加密法--魔王加密法 (Lucifer) 
* 第六代加密法--RSA加密系统，互联网的底层，同期还有Rabin算法，EI Gamal算法(椭圆曲线算法，区块链技术的核心之一)
* 第七代加密法--量子加密 终极加密


---
> [python学习总结(四)--String parsing](https://read.firesbox.com/posts/7b71ead909c1b46fc5ac914e70d9d744a5bb019cf99757e28fcfc273d59c4671)   
> [python学习总结(三)--PyQt](https://read.firesbox.com/posts/d7b80845d7870c33960dc349b6b1765c4145e4afac3aac00f422b713ca8fa320)   
> [python学习总结(二)--powershell](https://read.firesbox.com/posts/ffc76fa8634a3be98e4f7ca9e45d7b5b33a41a3f5374a8153eaa42daddd91997)  
> [python学习总结(一)](https://read.firesbox.com/posts/b4ebbc69f1e5e4ba1069f112dcfef65fd7238bce3c7a722fae78e0fb6976fe5c)  
---
**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，注册 [**Mixin**](https://mixin.one/) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mp.weixin.qq.com/s/ci_OWj9vtnsJ4OROifNfSQ) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)