# Python实践CFA系列（概要）

CFA是“特许金融分析师”（Chartered Financial Analyst）的简称，它是证券投资与管理界的一种职业资格称号。其知识体系涵盖资产类别，投资工具等10项基础知识。

CFA分析师最终干的事儿，用一句话来概括是：**提供科学、有效的资产组合配置方案；在满足投资人风险偏好的前提下，取得预期的回报，实现最适合的回报风险比。**

在引入数量分析之后，CFA从玄学变成了以数据为基础，数量分析为工具的科学体系；随着大量数据采集，使用计算机编程的方式进行数据清洗，分析，建模和预测成为主流。其中Python以其高效的处理能力，快速上手的特点，成为CFA最主要的编程分析工具之一。

后面的一部分学习总结，我尝试着用Python实践CFA里面的部分知识，深入体会CFA知识的同时，提升Python的技能水平。

## CFA知识体系
CFA知识体系包含10门基础知识，分为道德准则，资产类别，投资工具三大类。详细结构如下：

![img](https://src.seaky.club/img/CFA.png)  

> 1. **Ethics**（道德准则）：CFA的行为规范，作为一个CFA在面对法律，面对市场，面对客户，面对雇主，面对冲突，面对记录数据以及面对CFA协会时，必须要选择的立场和行为。
> 2. **Fixed Income**（固定收益）：资产类别的一种，债券等具有还本付息特性的资产。未来现金流固定（或者说可知），其当前价值受利率变动，发行者信用等级影响显著；久期匹配是其风险管理的主要手段之一。
> 3. **Equity**（权益）：资产类别的一种，股票等以股息和未来价格为价值锚点的一类资产。其价值主要体现在股票发行者的经营情况及未来的发展；估值方式主要有直接法（未来现金流折现法）和间接法（PE，PB，PE/G等与可比股票的对照分析方法）。
> 4. **Alternative**（另类资产）：资产类别的一种，股票和债券以外的其他标的资产，主要有不动产，不动产证券，PE投资（一级市场股权投资），大宗商品，艺术品等等。每种都有其独有的估值方法。
> 5. **Derivatives**（衍生品）：资产类别的一种，本质是合约的交易，其目的是风险管控。主要有远期，期货合约，互换，期权等。合约标的资产也有很多种，如大宗商品，股指，债券指数，利率，汇率等，甚至于天气等也可以作为合约的标的。
> 6. **Porfolio management**（组合管理）：特殊的资产类别，是将多种上述4类资产，按照一定的比例，考虑到周期，投资者风险偏好等，组合在一起形成的资产类别。着重体现在符合投资人的风险收益诉求，最合适的收益风险比例。
> 7. **Quantitative Methods**（数量方法）：统计，数学的分析方法，用于分析，建模和预测。分析的目标主要是交易量，价格，收益率，方差（风险）及他们与时间的关系。还包括回归分析，量化交易，机器学习，和金融科技等方面。是基本面分析和技术分析的有效工具。
> 8. **Financial Reporting Analysis**（财务报表分析）：微观基本面分析工具之一。分析跟踪公司的财报，剔除异常，粉饰等的影响；在同一个基本面下，纵向分析公司不同时期的发展和对未来的预期；横向比较不同公司的差异，为投资决策提供依据。
> 9. **Economics**（经济学）：宏观/微观基本面分析工具；主要讲述量价关系，市场形态，行业分析，生产均衡，GDP，生产函数，经济增长，地域发展，汇率变动，经济危机等。为决策提供宏观指导依据。
> 10. **Corporate Finance**（公司金融）：微观基本面分析工具。站在公司角度，理解公司的资本结构；研究公司的资本来源（融资过程）；运营管理（经营过程）；资金出项（投资过程，和分配过程）。以及公司治理上的优缺点分析。

## Python的实践内容概要
我计划从这几个方面，用Python进行实践：
1. 基本金融学理论，如马科维兹的有效前沿理论；组合风险收益分析；
2. 最优组合分析，风险分析
3. 金融交易数据的量价分析，时间序列的收益率与风险分析与预测
4. 在线组合的比例动态调整等

## 预告
下一篇：用python直观的展示，2个资产的组合中，资产的相关性（ρ）与风险（σ）和收益（r）关系；会使用到 pandas，numpy，matplotlib三个模块。 


---   
**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，老虎证券王珊老师的**读财报课**，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，下载并注册 [**Mixin**](https://mixin.one/messenger) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mixin.one/messenger) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)
