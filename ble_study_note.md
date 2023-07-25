# BLE学习笔记
## BLE通信的基本概念
+ 1.设备角色：在BLE通信中，有两种设备角色：中心设备（Central）和外围设备（Peripheral）。中心设备负责发起连接请求和接收数据，而外围设备则提供数据和服务。

+ 2.广播（Advertising）：外围设备可以通过广播的方式发送广播包，以宣告自己的存在和提供的服务。广播包包含设备的标识、服务UUID等信息，中心设备可以通过监听广播包来发现周围的外围设备。

+ 3.连接（Connection）：中心设备可以与外围设备建立连接，建立连接后可以进行双向通信。连接是由中心设备发起的，需要外围设备同意连接请求。

+ 4.服务（Service）：外围设备提供的功能和数据被组织成一个或多个服务。每个服务都有一个唯一的UUID来标识，可以包含一个或多个特征。

+ 5.特征（Characteristic）：特征是服务中的一个单元，用于描述某种数据或操作。特征包含一个唯一的UUID和相应的值。特征可以是只读、可写或可通知的，可以用于读取传感器数据、发送控制命令等。

+ 6.描述符（Descriptor）：描述符提供有关特征的附加信息，例如特征的单位、范围等。描述符可以用于扩展特征的属性。

+ 7.GATT（Generic Attribute Profile）：GATT是BLE中定义的通用属性协议，用于描述设备之间的服务、特征和描述符。GATT规定了设备之间的数据交换方式和规范。

+ 8.UUID（Universally Unique Identifier）：UUID是一个128位的唯一标识符，用于标识BLE设备、服务、特征和描述符。UUID可以是标准预定义的，也可以是自定义的。
---
## BLE通信项目运行流程--以G3为例
### 建立连接
#### ble.init()
+ 完成对保存的BLE外设清单进行扫描，使用bleMgr.init()选定初始连接的设备。
+ saveTask()：向字典中存储扫描到的外设清单
+ bleMgr.start()：正式程序运行
#### saveTask()
+ 创建一个线程并循环运行
+ 通过cfg.set("FOUND", ds)存储外设清单
#### bleMgr.start()
+ 使用了回调函数onScan()，在onScanDone()扫描函数结束后调用处理。
+ BLESimpleCentral()：初始化外设查找及连接模块。
+ loopScan()：定时循环执行central.scan()函数完成外设查找，并在每次查找完成后执行回调函数onScanDone()
    + central.scan(): 查找周围环境的外设
    + onScanDone()：处理扫描到的外设，判断是否进入产测，并在最后调用onScan()
    + onScan()将所有扫描到的设备存入字典ds中。
+ jt.start()：运行loopUpload()
+ loopUpload()：循环报告周围外设执行doReportNode()
+ doReportNode()：将数据存入info中方便后续的调用，并执行report_ble_nodes_for_relay()
+ report_ble_nodes_for_relay()：汇报周围BLE外设信息至服务器中。

### BLE广播数据格式
+ prefix---数据格式前缀
+ name---BLE外设名称
+ addrType---地址数据
+ rssi---接收强度

### 数据通信
#### devMgr.init()--执行loop()
#### loop()：间隔轮询时间循环处理通讯任务并执行commTasks()
#### commTasks()：通讯任务，包括一次连接，多个任务，并最终断开。
+ 任务连接：`vw.connect()`
    + 获取设备id，判断设备是否在线，通过prepare()函数订阅消息，当收到通知时，回调onRx。
+ 设置时间：`setDateTime()`
    + 通过setDateTime()函数每天同步一次时间
    + setDateTime()：经过数据整理后通过_read()函数向设备发送数据。
+ 读取卡路里和布数：`readStepCalCurrent()`
    + 注册回调函数processResult(data)后进入readCurrentValue()进行数据读取。
+ 读取BT：`readBt(date = day)`
+ 读取PrBpOx：`readPrBpOx(date = day)`
+ 读取Steps：`readSteps(date = day)`
+ 读取操作基本操作为：注册回调函数processResult(data)后进入readHistory()进行数据读取。
+ 任务关闭：`disconnect()`
+ readCurrentValue()：根据输入的读取操作设置发送命令，通过_read()向设备读取数据，并设在回调函数onRx。
+ readHistory()：根据输入的日期和读取操作设置发送命令，通过_read()向设备读取数据，并设在回调函数onRx。
#### _read()
+ 向设备发送指令bleMgr.write(msg, onRx)
    + 通过bleCentral.write(msg, response=True)函数发送指令
+ 等待数据接收完毕bleMgr.waitRxDone()


