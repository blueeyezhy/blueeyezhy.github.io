# Python实践CFA系列（一）-- 收益率和风险

虽然我前一篇概要上说：这篇要用python直观的展示，2个资产的组合中，资产的相关性（ρ）与风险（σ）和收益（r）关系；但是我觉得有必要优先说明一下，金融学的核心-- **收益率和风险**。

**金融学**研究的核心问题就是在时间维度下，收益率和风险的关系。目标是合适的风险水平下，获得最大的收益。而度量收益率和风险的指标：是统计意义上的收益率均值 $r$（return） 和收益率的标准差 $\sigma$（风险或者波动率）。

收益率是从历史交易的数据中计算出来的，当交易日的收益率 $R_{t}=(P_{t}-P_{t-1})/P_{t-1}$ （其中$P_{t}$ 是交易日 $t$ 的收盘价）；实务中，也会用 $R_{t}'=ln(P_{t}/P_{t-1})$ 计算收益率（因为在实际情况下，价格的波动率通常很小，这时$R_{t}'\approx R_{t}$且曲线更加平滑）。而收益率均值 $r$ 和 波动率（风险）$\sigma$ 则是一段时间上 $R_{t}$ 的均值和标准差。

## 我们用Python来实践计算 $r$ 和 $\sigma$，并对比一下 $R_{t}'$ 和 $R_{t}$
```python
import numpy as np
import matplotlib.pyplot as plt 
%matplotlib inline

date = np.linspace(0, 31, 30)           # 设定X轴坐标点，0~30，共30个坐标点

price = np.random.randint(80,120,31)    # 生成随机价格，31个；价格波动20%
R = []                                  # 收益率列表，(Pt-Pt-1)/(Pt-1)
R_ln = []                               # 收益率列表ln，ln(Pt/Pt-1)

for i in list(range(1, len(price))):    # 循环生成收益率数据，共30个
    R.append((price[i]-price[i-1])/price[i-1])
    R_ln.append(np.log(price[i]/price[i-1]))

# 计算R的均值和标准差，取4位小数
r = np.mean(R).round(4)
σ = np.std(R).round(4)

# 计算R_ln的均值和标准差，取4位小数
r_ln = np.mean(R_ln).round(4)
σ_ln = np.std(R_ln).round(4)
    
# 画布基本设置
plt.figure(figsize=(12,5))            # 设定画布大小
plt.title('$r\ &\ \sigma$')           # 设定标题，LaTeX语法
plt.xlabel('$date$',fontsize = 16)    # X轴标题
plt.ylabel('$r$',fontsize = 16)       # Y轴标题
plt.ylim(-.8,.8)                      # Y轴取值区间

# 画曲线
plt.plot((date.min()-1,date.max()+1),(r,r), color='blue', lw=2)                # r均值线
plt.plot((date.min()-1,date.max()+1),(r_ln,r_ln), color='red', lw=2)           # r_ln均值线
plt.plot(date, R, label = r'$(P_{t}-P_{t-1})/P_{t-1}$', color='blue', lw=2)    # r变动曲线
plt.plot(date, R_ln, label = r'$ln(P_{t}/P_{t-1})$', color='red', lw=2)        # r_ln变动曲线
plt.text(0.5, .5, r'$r = $'+str(r) + r'$\qquad\sigma = $'+ str(σ) , fontsize=12, color="blue")
plt.text(0.5, -.6, r'$r\_ln = $'+str(r_ln) + r'$\qquad\sigma\_ln = $'+ str(σ_ln) , fontsize=12, color="red")

# 显示图例和画布
plt.legend()
plt.savefig('rr.png')
plt.show()
```
![img](https://src.seaky.club/img/rr.png)

这副图是上面代码段生成的，价格波动在20%的情况下，收益率 r 和风险 𝜎 在不同算法上的对比情况；r 和 r_ln 存在显著的背离。

我们再看一下在不同价格波动情况下，r 和 r_ln 及 𝜎 和 𝜎_ln 的对比情况。  
这次我们用 matplotlib 子画布横向对比的方式来展示。

```python
import numpy as np
import matplotlib.pyplot as plt 
%matplotlib inline

fig, ax = plt.subplots(1,3,figsize=(12, 4)) # 初始化一行三列三个画布 

date = np.linspace(0, 31, 30)       # 设定X轴坐标点，0~30，共30个坐标点
price_v = [0.05, 0.15, 0.3]          # 设定价格波动率对比区间price_volatility

for p_v in range(3):
    p = np.random.randint(100*(1 - price_v[p_v]),100*(1 + price_v[p_v]),31)   
    R = []                              
    R_ln = []                           

    for i in list(range(1, len(p))):    
        R.append((p[i]-p[i-1])/p[i-1])
        R_ln.append(np.log(p[i]/p[i-1]))

    r = np.mean(R).round(4)
    σ = np.std(R).round(4)

    r_ln = np.mean(R_ln).round(4)
    σ_ln = np.std(R_ln).round(4)

    ax[p_v].set_title('$Price\ volatility\ =\ $' + str(price_v[p_v]))        
    ax[p_v].set_xlabel('$date$',fontsize = 16)
    if p_v == 0 :
        ax[p_v].set_ylabel('$r$',fontsize = 16)
    ax[p_v].set_ylim(-.8, .8)                     

    ax[p_v].plot((date.min()-1,date.max()+1),(r,r), color='blue', lw=2)
    ax[p_v].plot((date.min()-1,date.max()+1),(r_ln,r_ln), color='red', lw=2)
    ax[p_v].plot(date, R, label = r'$(P_{t}-P_{t-1})/P_{t-1}$', color='blue', lw=2)
    ax[p_v].plot(date, R_ln, label = r'$ln(P_{t}/P_{t-1})$', color='red', lw=2)
    ax[p_v].text(0.5, -.5, r'$r = $'+str(r) + r'$\qquad\sigma = $'+ str(σ) , fontsize=10, color="blue")
    ax[p_v].text(0.5, -.7, r'$r\_ln = $'+str(r_ln) + r'$\qquad\sigma\_ln = $'+ str(σ_ln) , fontsize=10, color="red")

    ax[p_v].legend()

plt.savefig('rr2.png')
plt.show() 
```
![img](https://src.seaky.club/img/rr3.png)

从图上我们可以直观看出，随着价格波动率 price_volatility 的上升，收益率 r 的在两种算法下的差别越来越大。  
所以：在债券，股票等价格波动率较小的情况下，我们可以使用 $R_{t}=ln(P_{t}/P_{t-1})$ 来近似计算收益率；而在虚拟货币市场上，由于价格波动率很大，必须使用 $R_{t}=(P_{t}-P_{t-1})/P_{t-1}$ 来计算收益率。

**通过这篇内容，我们要了解金融学的核心是收益率和风险；并用Python实践了实务中计算收益率不同方法，以及明确了它们的使用条件。**

## 所感
说实话写这篇内容的过程，让我深刻的体会到 “以为自己会了，都记住了” 和 “自己真正会了，能够应用了” 之间的差距有多大。
整篇下来，无论对于CFA，还是对Python的理解都进了一步。




---   
**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，老虎证券王珊老师的**读财报课**，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，下载并注册 [**Mixin**](https://mixin.one/messenger) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mixin.one/messenger) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)
