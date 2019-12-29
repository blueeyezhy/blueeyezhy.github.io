# 非对称加密(RSA)--Python学习总结(七)

> - **PressOne**: [张野](https://press.one/main/p/7c08521960497a61baf3f1c9760ff2a4cc66be1c)
> - [**Mixin**](https://mixin.one/) ID: 21120;  **bot**: 7000102888
> - **Github**: [@blueeyezhy](https://github.com/blueeyezhy)
> - **web**: [blueeyezhy.github.io](https://blueeyezhy.github.io/)

承接上一篇DES，继续用 `python` 实践[《卓克·密码学30讲》](https://m.igetget.com/share/course/pay/detail?id=Enb9L2q1e3OxKBmfPXrgN8P0Rwo6B7)  
为了方便说明做如下设定： 
> A = 信息的发出者；要发出的信息称为**明文**，标识为：**α**  
> B = 信息接收者；  
> C = 信息传递者； 传输过程中的信息称为**密文**，标识为：**β**  
> E = 信息的偷听者；  
>过程：A加密后，通过 C 把**密文**传递给 B ， B 解密获得信息，不让 E 知道**明文**内容。


## 第六代加密法--非对称加密算法 
第五代对称加密算法，在密钥的传递上有明显的漏洞，一旦密钥泄露所有的信息都没有秘密可言。为了解决这个问题研究者们引入了不可逆函数，密码学中把它叫做单项函数。我们通常意义上的函数（f(A)=B，通过A可以求出B）都是可逆的，即同时有反函数（f'(B)=A,通过B反过来求A）存在。  

有没有一种函数是只能通过A计算出B，而B不能计算出A呢？有，那就是"模运算"，常见的例子是时间，比如晚上22点再加3个小时是1点，再加27个小时还是1点，所以是时间就是一个模等于24的体系；同样，分钟和秒是模等于60的体系；星期是模等于7的体系。乘法也一样可以用模运算，比如在模为13的体系下，11x9等于多少？因为99除以13商数为7余数为8，99就相当于转了7圈后又走了8格，所以在模为13的体系中$11\times9=8(mod13)$。

回看这个例子，正向我们可以得到11乘以9在模13的体系下等于8；但是反过来问，在模是13的体系下，什么数乘以9等于8呢？这个问题是不能逆运算的。当模比较小的时候，可以逆运算的结果比较多；但是当模大到一程度的时候，就完全没有逆运算了，这是由数学决定。

非对称加密（RSA加密算法）就是基于这个不可逆的模运算的基础上，加上费马小数定理，质数的应用以及数论建立起来了。RSA加密法，仍是当今使用的最广泛的加密方法，就像我们的手机支付加密，网银加密，都会用到它。非对称加密算法的核心是有两套密钥：公开密钥和私有密钥（简称公钥和私钥）.
>1. 这两种完全不同密钥中，公钥用于加密，私钥用于解密。
>2. 这两个看上去无关的钥匙，在数学上是关联的。
>3. <加密-解密>的逆操作就可以完成<签名-验证>过程。

RSA加密的实现: 完整代码参看附录(因为大数乘方运算需要大算力资源的支持，所以我的代码仅仅选择100以内的质数进行原理的验证)
>1. 找两个很大的质数 $P$ 和 $Q$，越大越好，比如 $100$ 位长的。
>2. 计算这两个质数的乘积 $N=P\times Q$
>3. 计算这个两个质数最大互质数的乘积 $M=(P-1)\times(Q-1)$
>4. 寻找一个与 $M$ 互质的整数 $E$，也就是说 $M$ 和 $E$ 除了 $1$ 以外没有公约数。
>5. 找一个整数 $D$，使得 $(E\times D)\div M$ 余 $1$，即 $E\times D\ mod\ M = 1$
>6. 取 $(N,E)$ 为公钥；$(N,D)$ 为私钥；公钥公开，私钥一定要私密保管好。
>7. 将需要加密的信息进行编码数字化，比如说信息 $X=$`btc` 经编码后为 `011000100111010001100011` 等于十进制的 `6,452,323`。
>8. 对 $X$ 进行加密，$X^E\ mod \ N=Y$ 得到密码 $Y$，在没有私钥 $D$ 的情况下，神仙也无法从 $Y$ 恢复到 $X$。
>9. 用私钥 $D$ 可以轻而易举的解密 $Y^D\ mod\ N=X$，得到信息 $X$。
>10. 然后将 $X$ 解析就可以得到 $X=$`btc` 了。 

## 对称加密(DES)和非对称加密(RSA)组合实践  
根据香农的信息论：  
>密码的最高境界是敌方在截获密码后，对我方的所知没有任何增加；用信息论的专业术语讲，就是信息量没有增加。
>当密码之间分布均匀并且统计独立时，提供的信息最少。均匀分布使得敌方无从统计，而统计独立可以保证敌人即使知道了加密算法，并且看到一段密码和明文后，也无法破译另一端密码。    
>--香农

**对称加密**（DES，加密效率高，适合于对大量数据进行加密）和**非对称加密**（RSA，加密效率低需要大算力支持；私钥不暴露，保密级别高）相结合就能够逼近香侬提出的密码学的最高境界。用完全独立随机的数字作为密钥，用对称加密的方法对信息加密；然后密钥通过非对称加密的方式传输。杜绝密钥在传输中的曝光，同时可以验证传输信息的真伪。下面的代码是利用DES和RSA结合的方式传递信息的过程。
$A$ 将保密信息$a$，经过 $DES$ 加密后变成 
`Xe%-t"Xe%$ t/0Xe%w# Xe-!ru0Xeww ,Xe&%"&=.I}l}{0MD/0#!!# .Xe,uqsXe$uwtXe,sr!Xe%"w&Xe&, !/0!#"$%'0&,- !#"$0%'&,`，$DES$ 密钥通过 $RSA$ 加密后变成 `ac15457078f68c654524c74ff38c6a95`，这两段信息传递给 $B$。$B$ 通过两次解密获得信息$a$。同时实现了对一段信息进行签名和验证的过程。

```python
from cryption_des import EncryptionDES as DES
from cryption_rsa import CryptionRSA
from cryption_rsa import encrypt_verify_RSA

#B实例化RSA加密方案，获取到公钥，把公钥传递给A
B_RSA = CryptionRSA()
KEY_B = B_RSA.get_public_key()

#A实例化DES加密方式，将明文a加密生成密文b，并传递给B
a ='''姓名: 张野 （男)
Mixin ID: 21120
身份证号码: 123456 78901234 5678'''
print(a,"\n")

DES_key = "bitcoin4you"

en_DES = DES(a, DES_key, 1)
b = en_DES.encryption_des()
print("b:",b ,"\n")

#A使用B的公钥对DES密钥进行加密，将密文cipher_DES_key传递给B
cipher_DES_key = encrypt_verify_RSA(DES_key, KEY_B,flag=1)
print("cipher_DES_key:",cipher_DES_key,"\n")

#B接收到密文b和cipher_DES_key后，先将cipher_DES_key用自己的私钥解密，获取DES的密钥
DES_key_de = B_RSA.decrypt_sign_RSA(cipher_DES_key,flag=0)

#再使用该密钥，对密文b进行解密，以获取原文
de_DES = DES(b, DES_key, 0)
a_de = de_DES.encryption_des()
print(a_de, "\n")
print(a_de == a,"\n\n")

print("****************签名与验证****************","\n")
m = "bitcoin for you!"
print("massage:",m,len(m))

#A实例化一个RSA类，获取公钥，并用私钥对信息m进行签名，然后将公钥，m和签名一起发送给给B
A_RSA = CryptionRSA((79, 61))
KEY_A = A_RSA.get_public_key()

signature = A_RSA.decrypt_sign_RSA(m,flag=1)
print("signature:",signature)

#B接收到信息后，使用A的公钥验证签名信息
m_v = encrypt_verify_RSA(signature, KEY_A, flag=0)
print("massage_v:",m_v,len(m_v))
print(m_v==m)


[OUT]
姓名: 张野 （男)
Mixin ID: 21120
身份证号码: 123456 78901234 5678

b: Xe%-t"Xe%$ t/0Xe%w# Xe-!ru0Xeww ,Xe&%"&=.I}l}{0MD/0#!!# .Xe,uqsXe$uwtXe,sr!Xe%"w&Xe&, !/0!#"$%'0&,- !#"$0%'&,
cipher_DES_key: ac15457078f68c654524c74ff38c6a95

姓名: 张野 （男)
Mixin ID: 21120
身份证号码: 123456 78901234 5678
True

****************签名与验证****************
massage: bitcoin for you! 16
signature: 12421ea6c6108d6de1ea716ae134d6de1271ae1b6f6dee1a74
massage_v: bitcoin for you! 16
True
```
随着时间的推移**对称加密**和**非对称加密**都在持续发展，**对称加密**方面AES取代了DES成为美国最新的对称加密标准，加密密钥更长，算法更复杂，抗暴力破解能力更强，更加安全，加密过程也很快。**非对称加密**方面有Rabin算法，EI Gamal算法和ECC(椭圆曲线算法)等等，以更短的私钥，更强的安全属性发展着。其中ECC(椭圆曲线算法)是区块链行业的主流算法，也是当前被认为最安全的算法。

## 收获与成长  
这次实践过程中，使我更加深入掌握了**对称加密**和**非对称加密**的知识，以及签名验证过程。
代码能力方面：对场景流程的分析把握，模块，类结构设计等方面有了长足的进步；同时借助李俊老师的指导，对于装饰器的使用，在代码中的应用有了深入的理解。

## 后续尝试实践
* 第七代加密法--量子加密
* AES加密法(对称加密)
* ECC-椭圆曲线加密算法(非对称加密, 区块链核心之一)

---
> [python学习总结(六)--Encryption and decryption-DES](https://read.firesbox.com/posts/a5e467977c9a4f42947c6b5af2c5ed3e778fa3600d3f0def1284d51f60e7832b)    
> [python学习总结(五)--Encryption and decryption-1](https://read.firesbox.com/posts/88f057fa93c7f831e36014cd7b4538474c9f8ce4cb495cfd2535524c0ecbf033)    
> [python学习总结(四)--String parsing](https://read.firesbox.com/posts/7b71ead909c1b46fc5ac914e70d9d744a5bb019cf99757e28fcfc273d59c4671)   
> [python学习总结(三)--PyQt](https://read.firesbox.com/posts/d7b80845d7870c33960dc349b6b1765c4145e4afac3aac00f422b713ca8fa320)   
> [python学习总结(二)--Powershell](https://read.firesbox.com/posts/ffc76fa8634a3be98e4f7ca9e45d7b5b33a41a3f5374a8153eaa42daddd91997)  
> [python学习总结(一)](https://read.firesbox.com/posts/b4ebbc69f1e5e4ba1069f112dcfef65fd7238bce3c7a722fae78e0fb6976fe5c)  
---
**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，老虎证券王珊老师的**读财报课**，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，注册 [**Mixin**](https://mixin.one/) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mp.weixin.qq.com/s/ci_OWj9vtnsJ4OROifNfSQ) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)

---

### 附: RSA加密完整代码

```python
"""
RSA by Python
"""
from bitarray import bitarray

def data_format_self(func):
    def wrapper(self, info, flag):
        if flag == 1:
            info_list = [ord(i.encode("utf-8")) for i in info]
        else:
            info_list = [int(i,16) for i in info.split(chr(0))]  
        res = func(self, info_list, flag)
        if flag == 1:
            return chr(0).join([hex(i)[2:] for i in res])
        else:
            return "".join( [(chr(i)) for i in res])
    return wrapper  


class CryptionRSA():
    """
    class of CryptionRSA
    """
    def __init__(self, pq=(47,61), E=17, info ="", flag=""):
        #实例化的时候，保证形参(p,q)是两个质数，且乘积要大于需要要加密的数字
        #公钥加密部分E也取质数，以方便寻找互质的私钥解密部分
        try: 
            self.__public_key, self.__private_key = self.__creat_keys(pq,E)
        except:
            print("All parameters must be prime, and (p-1)*(q-1)%E !=0.")

    def __creat_keys(self, pq , E):
        """
        create public_key and private_key
        """
        #计算模
        N = pq[0]*pq[1]

        #公钥中的E与(p-1)*(q-1)互素,且(p-1)*(q-1)%E!=0,否则退出函数，重新输入参数E 
        if (pq[0]-1)*(pq[1]-1)%E == 0 or not self.is_prime(pq[0]) or not self.is_prime(pq[1]) or not self.is_prime(E):
            return False

        #计算私钥中的D，使得E*D%(p-1)*(q-1)=1
        i = 1
        while (i*(pq[0]-1)*(pq[1]-1)+1)%E != 0: i+=1

        D = (i*(pq[0]-1)*(pq[1]-1)+1)//E

        #生成公钥和私钥元组并返回
        return  (N, E), (N, D)

    def is_prime(self, n):
        """
        Return a boolean value based upon whether the argument n is a prime number.
        """
        if n < 2:
            return False
        if n == 2:
            return True
        for m in range(2, int(n**0.5)+1):
            if (n % m) == 0:
                return False
        else:
            return True

    def get_public_key(self):
        """
        get public_key
        """
        return self.__public_key 

    @data_format_self
    def decrypt_sign_RSA(self, info, flag):
        """
        info: massage which is going to be decrypted or signed.
        flag: 0 when decryption; 1 when signning a massage.
        """
        return [i ** self.__private_key[1] % self.__private_key[0] for i in info]


def data_format(func):
    def wrapper(info, K, flag):
        if flag == 1:
            info_list = [ord(i.encode("utf-8")) for i in info]
        else:
            info_list = [int(i,16) for i in info.split(chr(0))]  
        res = func(info_list, K, flag)
        if flag == 1:
            return chr(0).join([hex(i)[2:] for i in res])
        else:
            return "".join( [(chr(i)) for i in res])
    return wrapper  

@data_format
def encrypt_verify_RSA(info, K, flag):
    """
    K: public key
    info: massage which is going to be encrypted or verified.
    flag: 1 when encryption; 0 when verifiation.
    """
    return [i ** K[1] % K[0] for i in info]
```