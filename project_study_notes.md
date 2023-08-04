# 项目学习笔记
##  项目代码的基本组成部分的三部分，以及它们的基本关系
+ 项目代码由micropython源码、ESP-IDF、python项目源码三个部分组成。
    -  micropython源码：里面包含了单片机部分的代码，主要负责将python语言编译成单片机可以解读的语言。
    - ESP-IDF：主要负责将micropython编译好的语言下载至单片机中。
    - python项目源码：里面储存了项目的主要代码。
---
## 项目代码运行流程
### 项目可以分为两种启动方式，分别为ESP32和unix仿真运行
+ ESP32启动方式：在_boot.py运行完毕之后，运行boot.py调用core.run()
+ unix仿真启动方式：通过.run/调用run_on_unix.py选择仿真的硬件后再运行core.run()。
### 项目整体代码是依托在asyncio模块上执行的，所以asyncio.run所调用的事件就为整个程序的死循环，可以通过asyncio.create_task()向事件中添加协程任务。
### 项目代码运行流程
+ core.run()
    + 1._watchdog_start()--未加载
    + 2._bootstrap()--加载磁盘文件夹
    + 3._enableCachedLog()--加载日志，将ESP32中的日志重定向至控制台，以便远程debug
    + 4._startup()--完成硬件和软件初始化
    + 5._loop_forever()--启动监视任务以及使用asyncio.run()运行看门狗程序，作为长期执行的死循环程序。
+ 在_startup()中调用variants中对应模块的init()完成对应模块的初始化
+ init()中调用各模块实现的功能
    + iomgr.init()--常用初始化、LED初始化、LCD IO初始化、蜂鸣器初始化
    + cfg.init()--加载配置信息
    + ui.init()--初始化lvgl,加载UI信息,
        + `ui/__init__.py/UIApplication`
        + 当前UI界面中存在的几个界面
        + `screens`目录，存放对每个界面的操作（激活等）
        + `pages`目录，定义每个界面上的具体内容
        + `ui/pages/home/PageDefault`中`activate`代码
        + 将首页中的每个要显示的控件启动
        + `ui/pages/home/PageDefault` 中`showRightButtons`部分代码
        + 主界面中将按钮与对应的“点击”事件绑定。
        + 根据不同的按钮，其对应的点击事件所处理的内容不一，根据点击事件选择`screenClass`对应的。
        +`ui/__init__.py`中`activate`代码
        + 当点击Settings按钮时，会”激活“settings.ScreenSettings。根据上述的代码，会再关闭原来的窗口后再激活打开对应的窗口，即会调用settings.ScreenSettings.activate()函数。
    + nwk.init()--初始化网络配置
    + ble.init()--初始化蓝牙配置
    + iot.init--初始化MQTT连接至服务器
    + devMgr.init()--初始化与BLE外设（手表）的通信
    + alert.init()--初始化警报算法
    + iot.init()--初始化登录服务器验证
+ asyncio在项目中的作用：将需要长期运行的程序（如：时间读取、数据传输、UI更改）通过asyncio.create_task()添加至长期事件中，并在所有需要运行的程序添加完毕后，通过asyncio.run()来激活长期事件，以便后续的程序运行。
---
## 创建一个项目变体
### 以template_basic项目模板为例
#### 文件结构
+ 文件结构包含三类
    + 1、模块代码:一般为模块命名的文件夹
    + 2、主函数: `__init__.py`
    + 3、配置文件:`constants.py`
#### 创建注意事项
+ 在`variants/__init__.py`中添加相关项目变体。
+ 在`code/boards`中需要添加相关项目的编译文件
+ 可在配置文件中修改项目名及项目版本号.
+ 如需添加外部模块，可以在配置文件中设置相关的硬件IO口。
#### UI模块代码运行流程
+ 1、在经过`ui.init()`跳转后，按顺序完成lvgl初始化和背光设置，之后进入到画面的初始化函数`app.init()`，并定位至`activate`函数，参数为HOME。
+ 2、在activate函数起到画面绘制关键函数为`newScr.activate(param)`，其中newScr.为同文件夹下的screens文件夹，并根据参数进入到了`home.py`中。在`home.py`/activate函数中又调用了pages/home/activate().
+ 3、在pages/home/activate()中运行了如下内容：
    + clock.start()：将时钟初始化为24小时制
    + uiWeather.start()：初始化天气
    + uiDate.start()：联网刷新时间
    + uiStatus.start()：获取蓝牙、WIFI连接状态
    + act.start()：加载语言并加载步数与卡数
    + ss.start()：加载数据
    + self.showRightButtons()：绘制按钮
    ```
    在运行过程中通过对PageDefault类的调用，提前完成了对图案的绘制，但等到start()后才会真正显示出来。
    ```
+ 4、在self.showRightButtons()中完成了对按钮的检测和函数的跳转。
    + btn_map字典中，onClicked对应的是按键按下时跳转的函数
    + 按下record跳转至ui/activate中参数为（ALARM_HISTORY）
    + 按下Mute时，运行btnMute()
    + 按下setting时，跳转至ui/activate中参数为（SETTINGS）

#### nwk模块代码运行流程
+ 1、在跳转至`nwk.init()`模块后，通过`networks.Networks()`进行WLEN和LEN的初始化配置。之后进行回调函数的设置。最后跳转至携程函数`connect()`中。
+ 2、在`connect()`中，`net.start()`会运行携程函数`self.connectOnStart()`。
+ 3、在`connectOnStart()`中，关键函数有三个，分别为`await self.connectWiFi(self.getWiFiConfig())`、`self.checkIpChanged()`和`self.checkConnectLoop()`，在这三个函数之前，程序执行的是对连接和配置状态的判断。
    + `connectWiFi(self.getWiFiConfig())`：完成对WiFi的连接，并等待连接完毕。其中`getWiFiConfig()`为获取WiFi的ID与密码，connectWiFi负责连接WIFI及设置WiFi 网络接口的参数。
    + `self.checkIpChanged()`：检查IP变化
    + `self.checkConnectLoop()`：检查掉线情况。

#### iot模块代码运行流程
+ 1、在跳转至`iot.init()`模块后，只有enableOTA和enablePing使能，分别运行`deviceOTA.start()`和`deviceHeartbeat.start()`。
+ 2、`deviceOTA.start()`：重置OTA报告。
+ 3、`deviceHeartbeat.start()`：添加两个携程程序：`self.taskSynctime()`、`self.taskCheckAction()`
    + `self.taskSynctime()`：获取当前时间
    + `self.taskCheckAction()`：向服务器发送PING请求。其中使用到了http向服务器发送请求。
        + 首先跳转至`self.ping()`，完成设备固件号、ID的设置，之后在`api.requestPing()`函数将其放入服务器地址中，之后进入到`doRequest("GET", url)`函数中向服务器请求数据。
        + 在`doRequest("GET", url)`函数中调用了`requests.get(url, headers=headers, stream=isStream, verify=verify)`向服务器请求数据，其中主要功能函数为`self.request("GET", url, **kw)`。
            + `request("GET", url, **kw)`:该函数首先完成了对服务器地址和数据的解析，之后将整合成两部分sreader, swriter，负责数据的读取和发送，其中调用到了`swriter.awrite()`完成了对数据的发送，数据的发送依照规定的数据帧来执行，数据帧为：指令/数据+host+close。之后使用`sreader.readline()`完成对数据的读取，并将数据返回至`doRequest("GET", url)`的response中。
            + 在response获得状态码，在doRequest("GET", url)中经过Response类的处理,并进入到超时处理中。
+ 4、requests库用于发送HTTP请求和处理响应。
    + 下面是一些常用的requests库的API及其解释：
        + 1.requests.get(url, params=None, **kwargs)：发送HTTP GET请求到指定的URL，并返回一个Response对象。params参数可选，用于传递查询参数。
        + 2.requests.post(url, data=None, json=None, **kwargs)：发送HTTP POST请求到指定的URL，并返回一个Response对象。data参数可选，用于传递表单数据。json参数可选，用于传递JSON数据。
        + 3.requests.put(url, data=None, **kwargs)：发送HTTP PUT请求到指定的URL，并返回一个Response对象。data参数可选，用于传递请求体数据。
        + 4.requests.delete(url, **kwargs)：发送HTTP DELETE请求到指定的URL，并返回一个Response对象。
        + 5.requests.head(url, **kwargs)：发送HTTP HEAD请求到指定的URL，并返回一个Response对象。该方法通常用于获取HTTP头信息而不获取响应体。
        + 6.requests.patch(url, data=None, **kwargs)：发送HTTP PATCH请求到指定的URL，并返回一个Response对象。data参数可选，用于传递请求体数据。
    + 以下是一些常用的Response对象的属性和方法：
        + response.status_code：响应的状态码。
        + response.text：以字符串形式返回响应内容。
        + response.json()：将响应内容解析为JSON格式。
        + response.headers：响应头的字典形式。
        + response.cookies：响应的Cookie信息。
        + response.raise_for_status()：如果响应状态码不是200，则引发一个异常。

### 以dock_hub为例
#### iomgr模块代码运行流程
+ 该代码实现了对I2C、LED、LCD、BUTTONS的初始化
    + 使用`I2C(0, scl=Pin(pinSCL), sda=Pin(pinSDA), freq=400000)`完成I2C初始化
    + `led_digits.init()`：`tm1652.init(),ch455.init()`分别完成tm1652、ch455模块的初始化。`_show_current_time()`显示当前时间
    + `lcd_tp.init()`：LEDio初始化
    + `buttonInit`:其中包含两个模块：setup、menu，利用`Buttons/pollBtns()`中的循环完成对按键的扫描。

#### diagnose_network模块运行流程
+ 通过`diagNwk.init(on_diag_nwk_cb)`函数注册回调函数on_diag_nwk_cb，并跳转至C代码：mod_diagnose.c/diagnose_nwk_init()中
## 在硬件上烧录文件
### 修改文件：
+ 在`code/boards`中需要添加相关项目的编译文件：
    + 在`export.variant.sh`中修改相对应项目的名称
    + 在`manifest.py`中调用项目所需模块

### 以h1为例
#### http发送流程
+ 在完成ble广播的扫描后进入回调函数analysisDeepAll中完成本次扫描的数据采集并跳转至sensorble.dataScanning(msg)中。
+ dataScanning函数主要完成的是每一个设备的故障扫描和数据解析，之后依次判断是否含有历史数据、实时数据、状态数据，并依次进入对应的函数完成数据的上传。
+ 在实时数据的上传中，调用了uploadDataTask函数，该函数完成了实时数据的获取、对网络状态的判断并完成数据的上报，当包含有历史数据或者实时数据上传失败时，会调用uploadHistoryData函数循环上报数据直至数据成功上报。
+ 在数据的上报中，起到主要作用的函数是doUploadData(httpDataUpload,bodyInfo,retry_time=HTTP_RETRY_TIMES)，该函数规定了每次上报的次数并回调httpDataUpload函数。httpDataUpload函数中主要完成对服务器地址和数据的整理并传入do_request函数中。
+ do_request函数判断了本次和服务器通信的目的，并调用对应的函数完成数据上报。
+ 每条数据的格式如："temperature,nodeId=00124B002345D263 tm=9999 1627465818000\n"
+ 使用http主要是向InfluxDB中上传数据，方便后续的调用
+ InfluxDB是一个开源的时间序列数据库，专门用于处理大规模的时间序列数据。它被设计用于高性能、高可用性和可扩展性，适用于存储和查询时间相关的数据，如监控数据、传感器数据、日志数据等。

### 以GREEDBIRD_mini_hub为例
#### setup运行流程
+ buttonInit()中运行bts.Buttons(c.HAL_DEFINES.get("PINS").get('SYSTEM').get('SETUP'), btn_holded_callback = setupHoldedClb, btn_pressed_callback = setupPressClb)当按键按下后回调至setupHoldedClb中运行net.doSetup()
+ net.doSetup() 
    + blinkMgr.setBlinkMode("SETUP_WIFI")：设置LED灯
    + 依次等待await self.setup.start()和await self.setup.wait()运行完成
    + 
+ setup.start()：断开已连接的网络
+ setup.wait()：
    + await self.startBlufi()：使用nimble协议，开始运行blufi：blufi.start(0)。
        + blufi.start(0)：开启蓝牙广播，注册蓝牙接收回调：on_rx，运行_handleSingleFrame(blePeripheral, v)
        + _handleSingleFrame(blePeripheral, v)，分包接收数据，并将数据存储至rcvSession结构体中，并跳转至_blufiJsonProv中转入rcvSession结构体，
        + _blufiJsonProv(p, data)：通过json.loads(data)解析json文件，之后运行onJsonReceivedCb跳转至prov.onJsonReceived中。
        + onJsonReceived(data)：在检查数据对象类型后跳转至_parseProvisioningData(data)中。_parseProvisioningData(data)完成了对json数据的分析并根据其内容配置相关数据后返回，继续执行pktSend向APP发送"\x00"。
    + 进入循环开始配置wifi或espNow或保存配置并退出，在退出10s后关闭Blufi和退出setup模式。

    + json数据文件格式:
        ```
        {'account': {'token': ''},
        'server': {'source': 'SYNCSIGN_CLOUD'}, 
        'activate': {'mqtt': False, 'http': False}, 
        'network': {'SyncFi': {'primaryChannel': 9, 'secondaryChannel': 13}, 
        'tryEspNow': False, 'prefer': 'SyncFi'}}
        ```
### 运行指令
+ 运行环境配置：
    + 在`mp`目录下。 
    + `git submodule init`
    + `git submodule update lib/berkeley-db-1.xx lib/micropython-lib lib/mbedtls`
+ 编译指令：
    + 在`code`目录下。
    + `source boards/GATEWAY_LCD_BLE/esp32/export.sh`
    + `cd mp/ports/esp32`
    + `./go build`
+ 下载指令：
    + `./go flash monitor`
### 注意事项
+ 在硬件接入时，需要对硬件接口提升权限：
    + `sudo chmod 777 /dev/ttyUSB*`星号为对应的接口
+ 在有多设备接入时，使用`export ESPPORT=/dev/ttyUSB*`设置下载接口
+ `ls /dev/ttyUSB*`查询插入的接口
+ 在编译失败时，有可能是IDF版本号与项目版本号不对应，可以进入`ss_lcd_display/code/mp`中使用以下指令：
    + `git branch`:查询IDF当前分支
    + `git checkout XXX`:切换分支，XXX为分支名
    + `git si`:初始化主仓库中的子模块
    + `git ss`:同步子模块的远程仓库和本地仓库之间的状态
    + `git su`:更新主仓库中的子模块
+ 在完成IDF版本号的切换后需要对硬件缓存进行清除：`./go fullclean`。
+ esp-idf-5.2-dev编译报错`tarfile.CompressionError: lzma module is not available`解决方法：
    + 原因是ubuntu环境下lzma模块未安装，安装方法为:
        + sudo apt-get install liblzma-dev
        + sudo apt-get install lzma
        + cd 至对应python版本的目录：如/usr/local/python3.8.x
        + sudo ./configure --enable-optimizations --with-ssl
        + sudo make
        + sudo make altinstall
    + 最后在进行esp-idf-5.2-dev编译./install.sh
+ 编译报错：`error: 'service' may be used uninitialized [-Werror=maybe-uninitialized]`原因是service未定义，需要在service调用语句后加上 = {0}。

---
## 从ESP32升级为ESP32-S3版本需要修改的内容
### boards
#### boards/MOCREO-HUB/esp32为参数主要修改位置。
#### export.sh(相通)
+设置自动化编译
#### manifest.py（相通）
+ 设置所需要调用的软件
#### mp_variant.cmake（重要）
+ 设置要包含在构建中的用户 C 模块。
+ 
#### mpconfigboard.cmake(重要)
+ 调用各模块的参数设置SDK
#### mpconfigboard.h（无关）
+ 配置调用的硬件及参数
+ 调用的芯片也在其中进行修改
#### partitions.csv（无关）
+ 配置地址空间大小

## 项目正式版本固件发布流程
### 正式版本固件从发布方式分为云端固件和烧录固件两个版本，从使用方式分为出厂固件和测试固件。
### 发布步骤--以gateway_lcd_ble固件为例
+ 在完成项目固件的测试编译及下载确定无误后，进入到code/mp/ports/esp32/release中，执行`./auto_make.sh`指令完成固件的打包。
+ 打包生成的文件位于upload中，并以项目或版本号的名字命名。打包生成的文件为压缩包通过`tar xzf filename.tar.gz`指令完成解压。
+ 解压后的文件一般有8个，两个为一组，分别是云端出厂固件和测试固件、烧录出厂固件和测试固件。每个固件包含了固件本体.bin和数据校对文件。
+ 一般完成固件的打包后需要进行烧录测试，使用`esptool.py --port /dev/ttyUSB0 --b 921600 write_flash 0x2000 filename.bin`完成固件的烧录。
+ 之后需要将云端固件在服务器中发布。可以通过`python -m http.server 8000`指令分享当前文件夹下的文件，可以通过IP+端口访问。

