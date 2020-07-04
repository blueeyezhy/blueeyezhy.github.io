# 实践总结14--进程，线程与协程

在编写自动交易策略的时候，一个并发的问题困扰我很长时间：管理多账号资产时，当交易信号出现之后，多个交易所账号必须同时执行；因为这个执行操作包含多次网路请求，延时较长，如果不并发执行的话，排在后面的交易账号就可能错过时机，乃至于不能成交。最终通过协程（I/O复用）的方式实现并发执行。（JavaScript promise的方式）

借着这个机会重新复习了一遍进程，线程与协程的内容，整理一下思路做个总结。学习资源除了网络搜索相关文章之外，还粗浅的学习了神书《深入理解计算机系统》的第12章《并发编程》。



## 并发

为什么要并发呢？上边交易策略的例子是为了让多账号在信号出现时，同时执行以获得同样的预期收益。其本质是连续几个操作的操作时间不同，导致资源使用上的不平衡，严重浪费；通过并发来实现各个资源在时效上和实效上的充分利用。

下面这个表格是计算机操作的时间量级对比表，为了直观感受差距，我引入的相当于的比较时间：

| 操作                      | 延时（时长）                | 类比时间（相当于）                      |
| ------------------------- | --------------------------- | --------------------------------------- |
| 1个 CPU 运行周期          | 0.5 ns （1ns = $10^{-9}$s） | 1 秒   （如果CPU运行周期相当于1秒的话） |
| 内存访问速度              | 0.2 μs （1μs = $10^{-6}$s） | 6 分钟                                  |
| I/O 设备（硬盘等）        | 1 ms （1ms = $10^{-3}$s）   | 1 个月                                  |
| 网络请求（TCP数据包转发） | 1 s                         | 100 年                                  |

如上表格，CPU执行一个内存请求指令只需要几秒钟，需要等待10分钟才能拿到内存的回复；执行一个I/O请求，需要一个月才能拿到回复；如果执行一个网路请求，需要等待近100年才能拿到结果，估计这时候CPU都要长毛了。

这种情况下，为了有效的利用资源，并满足时效，1个CPU内核要配置很多内存单元，要配置更多的I/O设备，执行网络请求的时候需要在等待结果的过程中执行其他很多操作。而这些资源的合理分配和使用就是通过进程，线程和协程来实现的。



**进程**：一个手机APP就是一个进程，是一个资源单位，包含程序运行所需的资源（地址空间，内存，数据栈等）；由至少一个线程组成。

**线程**：负责执行具体代码，类似于车间流水线；一个进程内的线程们共享进程资源，相互之间通过让步使用进程资源。

**协程**：单线程内部通过**交换控制权**的方式将阻塞的I/O资源，网路资源有效复用以提升时效和效率的方式。可以基于事件驱动编写高效的多任务程序。如：生产者和消费者模式。



举一个容易理解的例子：  

一家四口人（爸爸，妈妈，姐姐，妹妹）的生活可以看作一个**进程**；四口人中的每个人相当于一个**线程**；生活中洗衣（①:将衣服放入洗衣机-5s -> ②:洗衣机自动洗衣-1h-> ③:拿出洗好的衣服晾晒-1m）和 焖饭（①:淘米放入饭锅-10s -> ②:饭锅焖饭 -1h -> ③:饭好了拔电-1s）相当于需要执行的操作；其中等待洗衣机洗衣，饭锅焖饭是耗时操作。

1. 爸爸先洗衣服执行①②③后，再去焖饭执行①②③。---- 单线程顺序执行（**同步**），总耗时 = **2h1m16s**，花费 = **1个人**；
2. 爸爸去洗衣服执行①②③；同时妈妈去焖饭。---- 多线程并发（**异步多线程**），总耗时 = **1h1m5s**，花费 = **2个人**；
3. 爸爸去洗衣服执行①②③；让隔壁小明爸爸过来焖饭。---- 多进程并发（**异步多进程**），总耗时 =  **1h1m5s**，花费 = **2个家庭**；
4. 爸爸去执行洗衣①开动洗衣机，再执行焖饭①开动饭锅，然后等衣服洗好了执行洗衣③晾衣服，然后再去执行焖饭③拔电。 ---- 协程并发（**异步单线程**），总耗时 = **1h1m6s**，花费 = **1个人**；

由上面的例子可以看出：多进程耗费资源最高；多线程总耗时最短；协程介于两者之间。在现实当中根据不同的场景，应用不同的并发方式来实现高时效和高效率。计算密集型场景（如：计算天气云图，风暴模拟，高频解码等）一般用多核CPU+适量进程+适量线程大算力来实现；I/O密集型（如互联网应用）一般用多线程和协程的方式来提高服务器的使用效率。



## 代码实践

1. **顺序（同步）**

   ```python
   from datetime import datetime
   import time
   
   def run_time_decorator(f):            	# 定义一个装饰器，用于标记函数运行的启始和结束时间，并计算输出运行的时间
       def wrapper(*args, **kwargs):
           start_time = datetime.now()
           print(f'function {f.__name__} start at {start_time}')
           f(*args, **kwargs)
           end_time = datetime.now()
           print(f'function {f.__name__} end at {end_time} , spend {end_time - start_time}s')
       return wrapper
   
   @run_time_decorator
   def sleep3s():					      	# 定义一个函数，睡3秒
       time.sleep(3)
       
   @run_time_decorator
   def sleep5s():							# 定义一个函数，睡5秒
       time.sleep(5)
       
   @run_time_decorator
   def sleep_sync():						# 定义一个顺序函数，调用sleep3s和sleep5s两个函数
       sleep3s()
       sleep5s()
       
   if __name__ == "__main__":              # 运行顺序函数
       sleep_sync()
       
   '''    
   OUTPUT:
   function sleep_sync start at 2020-07-03 19:43:37.147489							# 函数sleep_sync开始
   function sleep3s start at 2020-07-03 19:43:37.147489							# sleep3s开始
   function sleep3s end at 2020-07-03 19:43:40.159003 , spend 0:00:03.011514s		# sleep3s结束，用时3s
   function sleep5s start at 2020-07-03 19:43:40.159003							# sleep5s开始
   function sleep5s end at 2020-07-03 19:43:45.160281 , spend 0:00:05.001278s		# sleep5s结束，用时5s
   function sleep_sync end at 2020-07-03 19:43:45.161017 , spend 0:00:08.013528s	# 函数sleep_sync结束，用时8s
   '''
   ```
   
   如上执行结果，`sleep_sync` 开始，然后顺序执行 sleep3s和sleep5s，最后主程序结束。总耗时 = 两个函数耗时之和 8 秒钟。



2. **多线程并发**

   装饰器与sleep3s，sleep5s与上述相同，引入`threading` 模块的 `Thread`.

   ```python
   # 装饰器与sleep3s，sleep5s函数同上 
   
   from threading import Thread
   
   @run_time_decorator
   def asyncsleeps():
       t1 = Thread(target = sleep3s)		# 创建线程t1,执行sleep3s
       t2 = Thread(target = sleep5s)		# 创建线程t2,执行sleep5s
       t1.start()							# 启动线程t1
       t2.start()							# 启动线程t2
       t1.join()							# 函数等待p1完成再结束
       t2.join()							# 函数等待p2完成再结束
       
   if __name__ == "__main__":
       asyncsleeps()
       
   '''
   OUTPUT:
   function asyncsleeps start at 2020-07-03 19:47:42.242101						# 函数sleep_async开始
   function sleep3s start at 2020-07-03 19:47:42.243065							# sleep3s开始
   function sleep5s start at 2020-07-03 19:47:42.244064            				# sleep5s开始
   function sleep3s end at 2020-07-03 19:47:45.250563 , spend 0:00:03.007498s 		# sleep3s结束，耗时3s
   function sleep5s end at 2020-07-03 19:47:47.253953 , spend 0:00:05.009889s		# sleep5s结束，耗时5s
   function asyncsleeps end at 2020-07-03 19:47:47.254674 , spend 0:00:05.012573s  # 函数sleep_async结束，耗时5.01s
   '''
   ```
   
   如上使用多线程并发后，`sleep3s` 和 `sleep5s` 同时进行，整个操作总耗时5.01秒。



3. **多进程并发** 

   ```python
   # 多进程时，装饰器不能简单移植，所以在函数内部计算时间
   
   from datetime import datetime
   from multiprocessing import Process
   import time
   
   def sleep3s():
       start_time = datetime.now()
       print(f'function sleep3s start at {start_time}')
       time.sleep(3)
       end_time = datetime.now()
       print(f'function sleep3s end at {end_time} , spend {end_time - start_time}s')
    
   def sleep5s():
       start_time = datetime.now()
       print(f'function sleep5s start at {start_time}')
       time.sleep(5)
       end_time = datetime.now()
       print(f'function sleep5s end at {end_time} , spend {end_time - start_time}s')
       
   if __name__ == "__main__":
       start_time = datetime.now()
       print(f'function main start at {start_time}')
       p1 = Process(target=sleep3s)           	# 创建进程p1, 执行sleep3s
       p2 = Process(target=sleep5s) 			# 创建进程p2, 执行sleep5s
       p1.start()								# 启动进程p1
       p2.start()								# 启动进程p2
       p1.join()								# 主进程等待p1完成再结束
       p2.join()								# 主进程等待p2完成再结束
       end_time = datetime.now()
       print(f'function main end at {end_time} , spend {end_time - start_time}s')
       
   '''
   OUTPUT:    
   function main start at 2020-07-03 19:27:42.217542							# 主函数开始
   function sleep3s start at 2020-07-03 19:27:42.364083						# sleep3s开始
   function sleep5s start at 2020-07-03 19:27:42.374849						# sleep5s开始
   function sleep3s end at 2020-07-03 19:27:45.364383 , spend 0:00:03.000300s	# sleep3s结束，耗时3s
   function sleep5s end at 2020-07-03 19:27:47.380219 , spend 0:00:05.005370s 	# sleep5s结束，耗时5s
   function main end at 2020-07-03 19:27:47.418109 , spend 0:00:05.200567s		# 主函数结束，总耗时5.2s
   '''      
```
   
   如上使用多进程并发后，`sleep3s` 和 `sleep5s` 同时进行，整个操作总耗时5.2秒。



4. **协程并发**

   ```python
   from datetime import datetime
   import time
import asyncio
   
   async def sleep3s():					      	# 定义一个异步函数，异步睡3秒
       start_time = datetime.now()
       print(f'function sleep3s start at {start_time}')
       await asyncio.sleep(3)						# 异步程序或有__await__属性的对象
   #    time.sleep(3)								# 如果这里的函数是非异步函数的话，最总僵尸同步的结果
       end_time = datetime.now()
       print(f'function sleep3s end at {end_time} , spend {end_time - start_time}s')
   
   async def sleep5s():							# 定义一个异步函数，异步睡5秒
       start_time = datetime.now()
       print(f'function sleep5s start at {start_time}')
       await asyncio.sleep(5)						# 异步程序或有__await__属性的对象
   #    time.sleep(3)    							# 如果这里的函数是非异步函数的话，最总僵尸同步的结果
       end_time = datetime.now()
       print(f'function sleep5s end at {end_time} , spend {end_time - start_time}s')
   
   if __name__ == "__main__":
       start_time = datetime.now()
       print(f'function sleep_xiecheng start at {start_time}')
   
       loop = asyncio.get_event_loop()
       tasks = [sleep3s(), sleep5s()]
       loop.run_until_complete(asyncio.wait(tasks))
       loop.close() 
          
       end_time = datetime.now()
       print(f'function sleep_xiecheng end at {end_time} , spend {end_time - start_time}s')
       
   '''
   OUTPUT:
   function sleep_xiecheng start at 2020-07-03 22:11:44.859353                		# 主函数开始
   function sleep5s start at 2020-07-03 22:11:44.872562							# sleep5s开始
   function sleep3s start at 2020-07-03 22:11:44.879544							# sleep3s开始
   function sleep3s end at 2020-07-03 22:11:47.883118 , spend 0:00:03.003574s		# sleep3s结束，耗时3s
   function sleep5s end at 2020-07-03 22:11:49.898418 , spend 0:00:05.025856s		# sleep5s结束，耗时5s
   function sleep_xiecheng end at 2020-07-03 22:11:49.900886 , spend 0:00:05.041533s  # 主函数结束，总耗时5.04s
   '''
   ```
   
   如上使用协程后，`sleep3s` 和 `sleep5s` 同时进行，整个操作总耗时5.4秒。这里需要注意 `sleep3s` 和 `sleep5s` 必须是异步程序或有 `__await__` 属性的对象，这样在执行的过程中才会挂起，让出I/O控制权；如果这个函数是非异步函数或者是没有 `__await__` 属性的对象的话，函数将不会挂起阻塞I/O，直到执行完，其结果和顺序一样。



## 所感

1. 温故知新：知识只有通过多次实践，多次的复习，多次的总结参能转化为技能，长到自己身上。
2. 解决问题之后，千万要记得复习与总结，这是深化知识点的掌握和提升技能的有效手段。
3. 想把一个理论解释清楚，一定要用他人可以听得懂的场景，例子去说明。



---

**定投践行社区**里面有李俊老师的**Python编程课**，刘晓艳老师的**英文课**(正在讲的是《**beyond feelings**》)，廖智小姐姐的幸福力(**汶川地震30小时深埋地下的感悟**)，老虎证券王珊老师的**读财报课**，还有李笑来老师的**写作课**和**定投课**，**定投时间**超值体验如果你也想加入，注册 [**Mixin**](https://mixin.one/messenger) 加我(ID: **21120**)好友，送你邀请码。

**注:** 践行社区是建立在 [**Mixin Massager**](https://mp.weixin.qq.com/s/ci_OWj9vtnsJ4OROifNfSQ) 上的社群，所以你必须学会使用 Mixin  Massager ；同时践行社区是封闭课程社区没有邀请码不能加入。)