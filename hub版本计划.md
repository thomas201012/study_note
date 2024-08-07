## HUB固件的版本计划(2023/8/8)：

1. 当前量产版本1.9.3

2. 当前测试版本(1.9.4,已运行测试一周以上)，新增功能和改动项：
bug:
    - hub提交了ble sensor空列表，导致在app上的sensor卡片为掉线状态，实际上sensor是在线的并正常更新数据，对应jira MOC-535。
    - 添加GTS Root R1证书。
    - hub在setup的时候，app没有展示出用户期望中的wifi 名称，对应jira MOC-533。

feat: 支持ST9/ST10

3. 计划在1.9.5版本上的改动有：
- 某些情况，zigbee sensor online/offline状态汇报不及时的bug。(已完成修改测试)
- 修复bug，当有一个D75LE-WI掉线时，导致其他D75-LEWI也无法刷新。(TODO)
- 对ST4，固件版本在Version等于3及以下的版本，hub做数据汇报的阈值判断，由0.5度上报改为1度上报。原因是此前的sensor测量结果变化非常频繁，所以服务器的数据会持续快速增加。（TODO）
- 同时支持influxdb数据库的两个url：[1]https://ts.mocreo.com/api/v2/write和[2]http://oo.mocreo.com:8080/api/v2/write。因为有个别用户的hub无法访问[1],单独给客户编译了hub固件，将来不好维护。（TODO）


## HUB固件的版本计划(2023/8/23)：
### 1. 当前工厂生产使用版本1.9.3, OTA客户推送的版本：1.9.4;
### 2. 当前内测版本(1.9.5)，新增功能和改动项：
- bug:
  - 某些情况，zigbee sensor online/offline状态汇报不及时的bug，对应jira HUB-124
  - 当有一个D75LE-WI掉线时，导致其他D75-LEWI也无法刷新，对应jira HUB-127
  - ST3/ST4 在探头断开后，还在更新数据，对应jira HUB-132
  - 连接以太网后，断电拔掉网线重新上电，使用Wi-Fi Setup, 完成后，Hub会断网亮红灯, 持续断网离线，对应jira HUB-136
  - hub日志错别字 Clink Botton，对应jira HUB-131
  - 不对出厂状态的BLE sensor做区分，对应jira HUB-128
  - 任务启动太快,无法拿到nodelist导致后续无法正常上报数据
        >>>
        上报zigbee sensor nodeInfo的任务启动过早，可能会导致出现online/offline状态不能更新的现象
- improve：
  - ST4数据上报阈值条件限修改，对应jira HUB-123
  - 同时支持influxdb数据库的两个url，对应jira HUB-122
  - 网络请求失败次数达到10次后进行维护性重启，对应jira HUB-120
  - 给ST3/ST4/ST5/ST6 nodeInfo 添加“probes”字段，对应jira HUB-121
- feat:
  - None
  
3. 计划在1.9.6版本上的改动有：(TODO)

### H1B/H2B 1.9.5-1的版本计划：
- 2个月内维护到达到”稳定版本“：就是没有新品就可以不更新固件，没有P2级以上的bug，能降低80%的用户投诉，升级到ss_mp的编译等。
    - [0]H1B添加一种硬件：即在当前的情况下，去掉zigbee 芯片，因为两个月后不出zigee sensor了，hub也不需要焊接这个芯片了，从而降低成本;
        >>>
            1. 如果znp通信失败，就不做zigbee相关的操作
            2. 通过IO区分硬件类型
    - [1]使用ss_mp编译hub, 也许可以解决一些wifi连接的问题
        >>>
            1.当前版本，如果反复触发hub升级，hub就会断网
            2.在新环境下编译时候不会出现这个情况
    - [1]在ss_mp编译后，更改https证书加载的方式, 在这个框架里加载证书有更加高效的方式
    - [2]*setup流程是否还有优化空间？
        >>> 是否有优化的方向？
    - [2]*对已有的ble sensor数据在hub断网后，本地存储的功能再次评估？
        >>> 
        这个功能的副作用：
        1. 这个功能增加hub的复杂度和故障风险
        2. 在sensor数量多的时候，这个功能不好承诺保存的数据量和时间
        3. 绝大多数用户不关心断网的时候hub能做什么，用户要联网
        好处：
        1. 有一个用户问过，hub恢复上线后，可以看到断网期间的温度变化吗，以知晓在这期间冰箱是否有温度超标的情况
        -------------- 
        处理办法：
            1. 

### H1/H1B/H2B 1.9.6的版本计划：
- 修改ST9的温度上报范围为-40-105

### H1/H1B/H2B 1.9.7的版本计划：
- 1.支持SS1 sensor
- 2.支持D75-LEWI 独立ble工作模式
- 3.修复在setup过程中,重试后上传错误状态的问题
- 4.Portal修改信道处新增友好提示
- 5.新增对st5 crc校验错误的限制，只打印日志，不上报状态。
- 6.调整hub_portal中关于无zigbee模块提示的字体大小。


### H1/H1B/H2B 1.9.8的版本计划(临时替换1.9.7)：
- 修复ss1在setup之后不立即上报数据的问题


### H1/H1B/H2B 2.0.0的版本计划：
- 在ss_mp环境下编译
    - 在连接以太网失败后，自动切换addr
- 连接Wi-Fi AP 后 开始调用ping接口，接收relog指令 便于查看后续Setup流程 日志或自动实现relog
- H1B
    - 1.setup后亮红灯的问题（MQTT连接失败可能也会导致一直亮红灯）
        - mqtt在重连成功后没有及时将app层的状态进行清除。
    - 2.https添加根证书(Roger)
    - 3.znp初始化失败重试成功后，将panid上传服务器
    - 4.在上传panid时，对空的panid进行过滤，修改为默认值
    - 5.在同步警报规则后，立即进行将警报规则判断结果通过events接口上报服务器
    - 6.在用户setup之后，开机连不上网亮红灯。----之前客户在使用以太网时，连不上网是不会亮红灯的。
    - 8.ss1 hub portal中解析错误的问题
    - 9.支持ST7、ST8设备(延后)
    - 10.在测量值超出测量范围后，应该上报上下限，而不是不报。
    - 11.对于数据上报失败的情况，不应该触发维护性重启
    - 12.数据打包存储的情况，数据长度会被修改
    - 13.在汇报测量数据时，加上接口调用失败时自动切域名重试的机制。
    - 14.Zigbee Sensor >>> Zigbee Nodes
    - 15.MQTT端口新增备用URL:d00182382sdytmlnz4l3s-ats.iot.us-west-2.amazonaws.com
    - 16.Setup 过程中，在某一步停留时间超过5min，将自动退出setup模式
    - 17.HUB指示灯调整
    - 18.HUB重启后连接不上WIFI 15min后强制重启
    - 19.在SETUP过程中，完成WIFI连接后以及调用一次PING
    - 20.在上传WIFI列表时也将加密方式一起上传
- H1
    - 1.关于logo发送（Hub v1.9.8支持）(需要重新进行编码，功能未实现)
        - 在hub portal可以支持用户手工给display更新logo；
        - 支持通过hub远程命令给指定的display发送；
    - 2.关于wifi信息的发送（Hub v1.9.8支持）
        - hub向display发送wifi信息(已完成)
        - hub portal可以支持用户手工给display更新wifi信息；(已完成)
        - 支持通过hub远程命令给指定的display发送wifi信息；
    - 3.关于display的重置操作（Hub v1.9.8支持）
        - 支持长按trigger 20s后将display进行重置；(7.5inch)
        - hub portal可以支持用户手工给display发送重置命令；
        - 支持通过hub远程命令给指定的display发送重置命令；
    - 4.取消Hacking in Progress的模板显示


### SS1针对于原版开源固件修改的地方
- 在uuid:1F1F中增加0xAX段指令
    - 0xA1: 进入setup模式
    - 0xA2: 修改校准值
    - 0xA3: 修改温度单位
    - 0xA4: 修改measureId改变条件 1+4个字节
            |    0x0000   |   0x00   |   0x00   |
             温度/单位0.1度  湿度/单位1% 时间/单位1min
- 修改广播间隔为1.5s
- 关闭内部保存测量数据功能
- 增加数据判断 》》当measureId改变时上报最新数据。
    》》measureId改变条件
    1.温差大于1度
    2.湿度变化大于6%
    3.距离上次measureId改变超过10分钟
    4.进入setup模式


- 开源固件中可能会用到的接口
    - 0x56 恢复默认设置
    - 0x72 断开连接后重启
    - 0x20 获取/设置舒适度参数




1.让用户使用以太网
2.ss_mp版本是否能够解决？
3.开机连接wifi失败100次后是否触发重启hub的机制。

### Hub_v1.9.4

083A8D0AE840
083A8D0AFAF4
083A8D0AFF24
083A8D0B1A34
083A8D0B31A0
083A8D0B3838
083A8D0B3A10
083A8D0B43B4
083A8D0B4918
083A8D0B4D48

### Hub_v1.8.9

 083A8D0D1C40
 083A8D0D2888
 083A8D9019D0
 083A8D901CA8
0C8B9541B608
0C8B9541C270
0C8B9541C940
0C8B9541CE70
0C8B9541D05C
0C8B9541D0DC

### Hub_v1.9.3

B0B21C38FAE8
B0A7321C5884
90380C61F304
B0A7321B0B74
1097BD3A9A74
FCF5C43A5F1C
E0E2E6B2AFFC
E0E2E6B50ADC
64B708C38918
083A8D0DE864