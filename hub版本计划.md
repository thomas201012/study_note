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

### H1B/H2B 1.9.6的版本计划：
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