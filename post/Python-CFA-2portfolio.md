# Python实践CFA系列（二）-- 两个资产组合的收益率和风险

上一篇我们了解了一个资产的收益率和风险，并用Python实践了它们的计算方法，以及不同计算方法的使用场景。   
这一篇我们来实践一下，两个资产组合的收益率和风险，我们引入两个新概念--**相关系数，收益风险比**。 

假设我们有两个资产A、B，他们的统计收益率和风险分别是：$r_{A}$，$\sigma_{A}$ 与 $r_{B}$，$\sigma_{B}$；它们在初始投资总额中的比例分别是 $weight_{A}$ 和 $weight_{B}$；所以有 $weight_{A}+weight_{B}=1$。

**相关系数 $\rho_{AB}$** 是资产A、B收益率相关性的标准化指标。$\rho_{AB}=\frac{Cov_{AB}}{\sigma_{A}\times\sigma_{B}}$

：A与B收益率的协方差  $Cov_{AB}$ ，除以A与B各自标准差（风险）的积$\sigma_{A}\times\sigma_{B}$。 $\rho_{AB}$ 的取值范围是 $[-1~1]$ ：    

$$\rho_{AB} =
\begin{cases}
1: & \mbox{A、B  的收益率完全正相关} \\
(0~1): & \mbox{A、B  的收益率正相关程度为  } \rho_{AB} \\
0: & \mbox{A、B  的收益率完全不相关} \\
(-1~0): & \mbox{A、B  的收益率正相关程度为  } \rho_{AB} \\
-1: & \mbox{A、B  的收益率完全负相关} \\
\end{cases}$$



那么，资产A、B组合的收益率 $r$ 和风险 $\sigma$ 分别是：  
$r = r_{A}\times weight_{A} + r_{B}\times weight_{B}$   
$\sigma = \sqrt{\sigma_{A}^2 \times weight_{A}^2 + \sigma_{B}^2 \times weight_{B}^2 + 2\times\rho_{AB}\times \sigma_{A}\times weight_{A}\times \sigma_{B}\times weight_{B}}$  

对于给定的两个资产A，B的组合，其收益率 ($r$) 随着两个资产初始投资占比 ($weight$) 的变化而变化；其风险 ($\sigma$) 随着这两个资产初始投资占比 ($weight$) 与两个资产的相关系数 ($\rho$) 变化而变化。

## 下面用Python实践一下，组合收益率（$r$）、组合风险（$\sigma$）与资产占比 ($weight$) 及资产相关系数 ($\rho$) 的关系

```python
%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
plt.rcParams['font.sans-serif'] = ['SimHei'] # 显示中文字符

def portfolio2(rA, rB, sA, sB, weightA, rho):
    '''计算收益率和风险
    
    :param rA: 资产A的收益率
    :type rA: float
    :param rB: 资产B的收益率s
    :type rB: float
    :param sA: 资产A的风险
    :type sA: float
    :param sB: 资产A的风险
    :type sB: float
    :param weightA: 初始投资中资产A的占比
    :type weightA: float
    :param rho: 资产A，B收益率的相关系数
    :type rho: float

    :returns rp : 组合收益率
    :rtype: float
    :returns sp : 组合风险
    :rtype: float    
    '''  
    weightB = 1 - weightA
    rp = rA*weightA + rB*weightB
    sp = ((sA**2)*(weightA**2) + (sB**2)*(weightB**2) + 2*rho*sA*weightA*sB*weightB)**0.5
    return rp, sp
    
rA = 0.03   # 设定资产A收益率B
rB = 0.08   # 设定资产B收益率A
sA = 0.1    # 设定资产A风险
sB = 0.14   # 设定资产B风险
weightAs = np.arange(101)/100  # 资产A比重，从0~1取100个点进行绘图对比
rhos = np.arange(-10,11,2)/10  # A与B回报率相关系数，从-1~1取11个进行对比

result = pd.DataFrame(columns = ['rho','weightA','rp','sp'])  # 实例化一个pandas DF对象，设定列名
# 向 result 循环添加组合数据
for rho in rhos:
    for weightA in weightAs:
        rp, sp = portfolio2(rA, rB, sA, sB, weightA, rho)   # 计算当前rho和weight下的rp和sp
        row = pd.DataFrame([rho, weightA, rp, sp]).T        # 将当前的[rho, weightA, rp, sp]实例化为 pandas DF对象，转成一行
        row.columns = ['rho','weightA','rp','sp']           # 修改row属性名与result对象一致
        result = result.append(row)                         # 将row添加到result中

plt.figure(figsize=(12,5))

for i in rhos:                 # 循环绘制不同相关系数的图形
    datas = result.loc[result.rho == i]
    plt.scatter(datas.sp, datas.rp, marker = 'o', label = 'rho = '+ str(i))

# 增加说明辅助线
plt.plot((0, 0.15), (0.06, 0.06), color='red', lw=2, alpha = 0.5)  
    
plt.legend(loc='lower right')
plt.xlim(0, 0.16)
plt.xlabel('组合风险 σ',fontsize = 16)
plt.ylim(0, 0.09)
plt.ylabel('组合收益率 r',fontsize = 16)
# plt.savefig("2p.png")
plt.show()
```
![img](https://src.seaky.club/img/pf2.png)

如上图，组合收益率目标确定的情况下（如上图 r = 0.06 辅助线）：相关系数 $\rho$ 越小，组合的风险 $\sigma$ 越小；也就是说我们通关选择相关系数小的资产进行组合配置，来对冲掉风险。

## 收益风险比

收益风险比是收益率 $r$ 与风险 $\sigma$ 比值 $= r/\sigma$；其含义是单位风险所对应的收益率。对于不同的资产或者组合 $r/\sigma$ 越大，说明风险分散的越好，被投标的的质量越高。他也是著名的夏普比例的前身。

让我们在上图中增加三条风险回报比的曲线对比一下。

```python
plt.figure(figsize=(12,5))

for i in rhos:                 # 循环绘制不同相关系数的图形
    datas = result.loc[result.rho == i]
    plt.scatter(datas.sp, datas.rp, marker = 'o', label = 'rho = '+ str(i))

# 增加说明辅助线
plt.plot((0, sA), (0, rA),  color='orangered', lw=2, )  # 资产A
plt.plot((0, sB), (0, rB),  color='gold', lw=2)         # 资产A
rp, sp = portfolio2(rA, rB, sA, sB, 0.5, -0.6)
# print(rp, sp)
plt.plot((0, sp), (0, rp),  color='limegreen', lw=2)    # 组合，A资产投资占比50%，相关系数 -0.6
    
plt.legend(loc='lower right')
plt.xlim(0, 0.16)
plt.xlabel('组合风险 σ',fontsize = 16)
plt.ylim(0, 0.09)
plt.ylabel('组合收益率 r',fontsize = 16)
# plt.savefig("2p1.png")
plt.show()
```
![img](https://src.seaky.club/img/pf21.png)

如上图三条直线：   
红色直线的斜率表示资产 A 的收益风险比 $= 0.3\ (= 0.03/0.1)$；  
黄色直线的斜率表示资产 B 的收益风险比 $= 0.57\ (= 0.08/0.14)$；   
绿色直线的斜率表示资产A，B按照0.5:0.5的初始比例，相关系数是-0.6时的收益风险比 $= 0.97\ (= 0.055/0.057)$。
**显然组合要远远优于单个资产。**

**这篇内容，我们用python实践了2个资产组合的收益率和风险，在不同初始投资比例和相关系数下的对比；验证了选择相关小的两个资产进行组合投资，会大幅降低我们的投资风险，提高收益风险比。**

## 所感
编程过程中尽管编程逻辑简单易懂、见码知意很重要，但是注释也非常重要。如上我在函数 portfolio2 中添加的注释，描述了输入参数，返回值的内容和类型，这样就可以很清楚帮助调用者了解它的功能，调用者只需执行 `help(portfolio2)` 就可以获取到注释信息。如下：
```python
help(portfolio2)

[OUT]:
Help on function portfolio2 in module __main__:

portfolio2(rA, rB, sA, sB, weightA, rho)
    计算收益率和风险
    
    :param rA: 资产A的收益率
    :type rA: float
    :param rB: 资产B的收益率s
    :type rB: float
    :param sA: 资产A的风险
    :type sA: float
    :param sB: 资产A的风险
    :type sB: float
    :param weightA: 初始投资中资产A的占比
    :type weightA: float
    :param rho: 资产A，B收益率的相关系数
    :type rho: float
    
    :returns rp : 组合收益率
    :rtype: float
    :returns sp : 组合风险
    :rtype: float
```

---
**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，老虎证券王珊老师的**读财报课**，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，下载并注册 [**Mixin**](https://mixin.one/messenger) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mixin.one/messenger) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)
