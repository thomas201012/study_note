## 2023/10/7
```
+ D1:commit 至最新版本，并进行测试。
+ H1B:观察1.9.5版本测试情况
+ 小米传感器:查找显示错误问题
+ 其他:转正考核
``` 
格式：xxxx项目，进度xx,计划xx时候达到xx地步
# 2023/10/9-2023/10/13

## 本周工作
+ H1B1.9.5版本更新，完成需求的更新和测试，并发布版本。
+ 小米传感器项目，解决显示乱码的问题
## 上周工作
+ H1B 1.9.5版本更新，进度：当前在根据新需求完成修改和测试，计划在国庆后完成客户端的第一批ota更新
+ D1崩溃排查，进度：还在排查原因。
+ 小米传感器项目，进度：配置编译环境和ota升级环境，计划在下周完成乱码问题的解决。

# 2023/10/16-2023/10/20

## 本周工作
+ H1B1.9.5版本更新，开始小批量的给客户推送更新。
+ 小米传感器项目，编译出第一版固件，并验证setup的方法
+ sensor_hub 项目，推进网络状态码的获取和显示
## 上周工作
+ H1B1.9.5版本更新，进度：完成更新和测试，计划在下周开始给客户进行批量OTA。
+ 小米传感器项目，进度：解决显示乱码的问题，计划在下周编译出第一版固件。
+ sensor_hub 项目，进度：整理网络状态码并思考怎样进行状态码的获取和输出，计划下周确定状态码的获取和保存流程。


# 2023/11/06-2023/11/10

- [1]重新编译HUB 1.9.7，提交到测试[]
- [1]SS_MP的编译固件V1.7.3提交到测试[x]
- [1] D1产测逻辑（通过特定的wifi名称进入，如果是工人按键操作太慢了，也不能批量操作）
- [1] D1 故障提示及实现逻辑(需求明确和方案讨论)
- [4]HUB 1.9.8(xin)

## 本周任务
+ release 1.9.7
+ 明确 1.9.8的更新内容
+ 完成ss1的软硬联调
+ D1-添加网络诊断功能
+ D1-添加厂测流程
## 上周任务
+ hub
    + 1.9.7的更改以及测试(90%)
    + 新增ble D75C蓝牙发送模板功能(done)
    + 测试hub连接多个display的可靠性，并优化刷屏流程(done)
    + 优化对ss1 sensor的支持(done)
+ SS1
    + 修改广播格式和配置指令，完成对固件的优化

### 11/06
+ 添加向ble D75C 发送wifi配置信息的功能
+ 明确d1的任务需求
+ 1.9.7--增加对st5 crc校验错误的限制，只打印日志，不上报状态

### 11/7
+ D1添加设备诊断(网络诊断)

1.检查当前是否有网络配置

    - 没有网络配置,则直接退出网络模块的检测

2.检查当前网络是否已连接

    - 若当前网络未连接,且拥有Wi-Fi配置,则尝试根据保存的配置连接网络【告知未连接的原因，或出错的原因】
    （直接拿状态码，不重连网络？）

3.开始把数据送到日志服务器【在此部分强制上报，与开机是否上传的机制没有关系】

4.检查设备时间是否有效

5.尝试Ping路由器

6.尝试ping Google等

7.尝试Http访问特定网址

8.尝试https访问sync.anypi.com (ping/action)

9.尝试https访问多个API服务

    - weather/stock/cc Api

    - 每个接口请求的最多次数为3次 (只有所有的Api接口均失败时,才认为无网络)

    - 展示失败的Api接口

10.检查MQTT/COAP连接状态

没有网络配置
网络连接成功
wifi连接失败
连接路由器失败
连接外部网站失败
http连接失败
访问api失败
MQTT/COAP状态异常

返回给ui的值：
1：步骤
2：连接错误的原因
3：错误码

Steps
ErrorReason
ErrorCode

# 尝试断开网络连接,并重新连接网络[不做]

注：
- 执行此步骤时,启动状态码记录,结束时应关闭状态码记录

- 若连接失败,则将连接过程中的Event对应的状态码保存并展示出来


D1产测流程：
1.开机判断是否有配置过WIFI信息和是否完成过产测，如果都没有，则进入产测。
2.进入产测后，扫描产测WIFI记录信号并连接
3.获取版本信息，SN、devies_key、boad类型，
    在屏幕上显示？
4.检测版本、检测固件
5.硬件检测
    - LED慢闪
    - 蜂鸣器beep
    - LCD全屏变化红、蓝、绿
    - 按键测试
        - 旋转编码 `器测试
        - 按下编码器三下
        - 按下按键三下
    - 测试完成后在LCD屏幕上显示OK
6.提交产测结果




ble display刷屏测试记录：
1.当多个display同时发送刷屏指令时，连接失败的情况出现较为频繁
2.当有多个hub，多个display时，可能会触发单次指令，多次刷新的问题
3.在获取task_Id时连接失败或者断开，程序还继续往下运行，导致了后续在发送模板这一部分停留太长时间
4.在hub重启后向display发送logo流程用时过长。(27个display的情况下，用时在10分钟-15分钟)
5.HUB存在relay_devies上报失败，但其他http正常，hub亮红灯的问题
6.当同时刷新多个display(54个)会与其他线程冲突？导致其他线程挂掉。(taskCheckAction,checkNodeAssociatedTask,sensorDataUploadTask)

优化思路(优化后两个hub同时刷新27个display用时5分钟左右，会有漏刷的情况)：
1.2.减少ble连接失败重试时间，将retry次数减少到一次
3.在获取或设置taskid和sha256时，在连接失败后不去等待taskid的获取或设置，直接退出释放ble连接权限。
4.在开机后将磁盘中的sha256存到缓存中的current_sha256，避免current_sha256开机后为空，对比后向display发送logo。
5.relay_devies上报失败后不亮红灯避免误导用户
6.减少设备数量？

现存的问题：
1.屏幕多刷-----已解决
2.屏幕漏刷-----已解决
3.开机发送logo------在开机后，HuB会拿磁盘中的sha256去和缓存中的current_sha256做比对，但current_sha256开机后为空，所以导致了开机之后必定会向idsplay发送logo。-----已解决

4.当连接多个display时可能会导致其他任务挂掉，在开机或着多个屏幕刷新时会出现

本次的修改有4个变动
1.关闭relay_devies上报失败亮红灯
2.将retry次数减少到一次
3.优化刷屏流程，减少不必要的等待
4.增加开机将sha256保存到缓存的操作，避免开机调用发送logo的指令

54个:
单个hub：用时14分钟
两个Hub：用时11分钟


----------------------------display刷屏测试记录到的问题：
1.当多个display同时发送刷屏指令时，连接失败的情况出现较为频繁
2.当有多个hub，多个display时，可能会触发单次指令，多次刷新的问题---已通过display固件修复
3.在获取task_Id时连接失败或者断开，程序还继续往下运行，导致了后续在发送模板这一部分停留太长时间
4.在hub重启后向display发送logo流程用时过长。(27个display的情况下，用时在10分钟-15分钟)
5.HUB存在relay_devies上报失败，但其他接口调用正常，hub亮红灯的问题
6.当同时刷新多个display(54个)会与其他任务冲突。导致其他任务挂掉。
----------------------------本次的修改：
1.将retry次数减少到一次（理由：为了给上层代码做更快速灵活的策略）
2.优化刷屏流程，减少不必要的等待
3.增加开机将sha256保存到缓存的操作，避免开机调用发送logo的指令（理由：减少开机不必要的负担）
----------------------------遗留的问题：
4.任务挂掉的问题（描述：hub收到50多个render 任务，就会出现其他任务没有抢到权限运行，造成task dead，hub重启一次才能继续完成所有刷屏任务，如果布置2-3个hub，那么这个概率就极低）
5.relay_devies上报失败亮红灯,但其他接口调用正常(理由：如果是断网，hub会红灯；relay_device这一个接口失败亮红灯，会让用户误判为hub掉线，但是这种情况会在设备很多的情况下出现，出现的时候意味这sensor可能会掉线，这个功能暂且保留)
6.连接失败的情况（描述：为了避免这个情况导致刷屏过长，减少了连接失败后的重试次数，直接跳到下一个刷屏任务）
----------------------------性能提高方面：
1.单个hub给55个dispaly刷屏平均用时14分钟。
2.两个hub给55个dispaly刷屏平均用时11分钟。

# 开机将磁盘中的数据保存到缓存中
def setCurrentSha256(Sha256):
    global current_sha256
    current_sha256 = Sha256

setCurrentSha256 = render_logo_template.setCurrentSha256

# 2023/11/20 - 2023-/11/25

# 上周工作
- D1
    - 完成产测流程的编写
    - 网络诊断功能的优化
- HUB
    - H1
        - 修改模板/logo的发送流程，解决logo发送失败的问题
    - H1B
        - 初步确定1.9.8的更新内容
        - 修复MQTT连接恢复后依旧亮红灯的问题
- MTV1
    - 优化产测流程
    - 产测固件的测试
    - 完成1.1.0固件的编译及发布
- 协助测试/FAE工程师排查问题
# 本周工作
- MTV1
    - 完成1.1.0固件的出货
- HUB
    - 推进1.9.8的更新
- SS1
    - 推进SS1的测试

### 2023/11/21
## HUB遗留问题

### 2023/11/27 - 2023/12/01
# 上周工作
    - H1
        - 验证hub向display发送wifi配置的功能
    - Sensor ble通讯测试
        - ble Sensor的连接和丢包率测试
    - D1
        - 网络故障状态模拟，模拟在不同网络故障状态下的code码
    - MTV1
        - 烧录出货固件
        - 产测
    - 参加V3 coap接口讨论会
    - 排查客户问题
# 本周工作
    - H1B
        - 排查测试反馈问题
            - znp模块为空的问题
            - 周末网络断开后hub没恢复的问题
    - D1
        - 交互弹窗与信息展示实现
            - 完成网络故障状态的获取和输出
        - 优化项改动实现
    - Sensor ble通讯测试
        - rola Sensor的连接和丢包率测试

#### 2023/11/29
- D1网络诊断模块优化[0]
    - 一共有7个步骤：
        1.网络配置检查
        2.Wi-Fi连接
        3.路由器连接
        4.外部网站连接
        5.HTTP请求尝试
        6.从服务器获取数据
        7.MQTT/COAP连接检测
    - 诊断结果输出
        0.网络连接正常
        1.没有网络配置
        2.连接wifi失败
        3.连接至路由器失败
        4.连接至网络失败
        5.http连接失败
        6.请求数据失败
        7.MQTT/COAP连接错误

- 发布h1b 1.9.8版本，修复ss1添加后不会立即上报数据的问题[0]
- sensor的ble 通讯测试:监听测试和临界距离的测试[1]

#### 2023/11/30
- 警报模块逻辑异常
    - 打开温度、湿度警报
    - hub收到通知，存储rule并触发温度报警
    - 当有新的数据上报后才发送event事件

### 2023/12/04 - 2023/12/08
# 上周工作
- D1
    - 网络故障状态的模拟
    - 网络检测功能的优化
        - 增加进度显示
        - 优化检测的流程及内容
        - 调整检测结果UI
- H1B
    - 发布1.9.8
        - 修复ss1 setup完成后未立即上报数据的问题
    - 其他问题修复
        - 解决ss1 hub_portal数据解析异常的问题
        - 修复在只使用以太网setup后,连不上以太网时,hub不亮红灯的问题
        - 在上传nodeId时,过滤掉空的id
        - 在同步警报规则时根据规则的结果上报events事件
- MTV
    - 进行产测和不良品的修复。
- bk3633 ble通讯测试
# 本周工作
- sensor的ble 通讯测试:监听测试和临界距离的测试
- H1B 
    - hub掉线情况模拟
    - ss_mp环境下，以太网芯片初始化失败的问题 


# 长测需要关注指标
- Hub网络情况
    - 重启之后掉线/断电之后掉线
        - wifi连接不上？
        - 调用接口失败？
    - 以太网连接不上
        - 未连接到路由器？
        - 未成功分配IP？
    - wifi信号较低时的表现
- sensor连接情况
    - zigbee
        - 重启/ota之后断连
        - 运行过程中断连
        - 断连后是否能够正常恢复
        - 探头断开或异常
    - ble
        - 信号过低
        - 探头断开或异常
- 数据汇报情况
    - hub在线但数据不上报
    - 数据误差情况
- 其他异常情况
    - 警报规则不同步
    - znp的上传情况
    - 蜂鸣器异常beep

### 2023/12/11 - 2023/12/15
# 上周工作
+ Hub
    + 2.0.0版本开发
        + logo发送功能[done]
        + wifi配置的发送[done]
        + 通过hub向display发送重置操作[done]
    + 其他问题修复
        + 修复当以太网因为芯片地址的原因初始化失败的问题
        + 修复ss_mp中开机lcd不亮红灯的问题
+ sensor hub
    + SensorHub Setup 需求确认
+ SS1
    + 在ota程序中添加记录sn码的功能
+ 排查客户侧问题
# 本周工作
+ sensor hub
    + setup流测试用例

+ 打开debug级别日志，查看是否可以区分拥有同一种错误码的异常情况
+ 验证屏幕最大容纳提示字符长度
+ 确认自定义错误码以及触发条件
+ 确认在setup中会出现的错误码
+ 验证ble和CoAP相关异常用例
+ 确认错误提示文本

### 2023/12/18 - 2023/12/22
# 上周工作
    + hub
        + 修复H1在未进行wifi配置的情况下向display发送带url格式的模板发生错误的问题
        + 修复在没有phy addr配置的情况下以太网初始化失败的问题
        + 修复delay devies调用异常的问题
        + 重新发布1.9.8
        + 排查测试及FAE反馈的问题
    + sensor hub
        + 列举setup过程中异常问题的测试用例
        + wifi连接异常情况的复现以及状态码的获取
        + 整理wifi连接异常情况，并进行归类
    + ss1
        + 烧录ss1固件
    + 协助测试lora模块的通讯
    + 完成d1RGB灯演示功能的开发
    + 蓝牙连接单元测试固件修改
# 本周工作
    + 完成sensor hub 错误处理功能setup部分的开发
    + 协助测试lora sensor的通讯功能
    + bk3633数据解析核对

### 2023/12/19
+ wifi连接异常情况文案及code码
+ BLE连接异常情况复现
+ 异常处理模块逻辑框架

### 2023/12/20
+ 确定故障系统框架
+ 初步搭建框架
+ 确定ui修改后的文案


### 2023/12/25 - 2023/1229
# 上周工作
    + hub
        + 排查客户侧问题
            hub zigbee模块无法添加
            h1 1.9.8版本setupToken异常
            ST10探头异常
            setup过程中，wifi连接错误
            hub setup异常
            hub不添加刷新任务
    + sensor hub
        + 对状态码进行  整理和文案校对
        + 测试BLE异常情况对应产生的状态
        + 调整错误显示文本和二维码大小
        + 添加故障系统框架
    + 解决BK8266蓝牙数据上报hub格式异常的问题
    + 协助测试lora sensor的数据上报
    + 测试D1天气显示异常问题
# 本周工作
    + sensor hub
        + 完成安排的任务
    + 排查客户侧问题，并对每个问题进行闭环处理
    + hub 2.0.0开发


# 23/12/27 - 24/1/5
-  GAME >>> Thomas  (3 人日)
    说明：允许客户上传游戏至D1，并通过手柄链接后进行游玩
    需求：
        + 提供游戏上传和管理界面
        + 进入Game App 选择游戏
        + 检查手柄链接情况，并提示链接手柄操作
        + 游戏模式下，不应该出现系统通知或 HTTP 请求 Lodding
        + 手柄的管理，设置页面支持手柄的连接与管理
    需要确认： 1. 是否支持除Xbox之外的其他手柄 2. 是否需要支持多手柄

-  SCREEN_MIRRORiNG >>> Thomas (1 人日)
    说明：D1 屏幕本身可以当做一个电脑扩展的屏幕
    需求：
        + 提供一个 IP 配置界面和引导界面
        + 选择 App 进入等待
- Todist >>> Thomas (1.5 人日)
    说明：展示客户在Todist添加的代办事项与详情
    需求：
        + 配置界面新增 Todist API Token 配置
        + 默认提示界面(引导页)
        + Todist 列表显示页， 详情页

- 工作时段 >>> Alan (0.5 人日)
    + 非工作时段
        + LED + LCD 关闭，时间点阵黑掉或变暗
        + 按钮按下后自动唤醒 / 1 分钟无操作自动关闭
    + 设置中配置界面

-  （1 人日）
    + 网络错误展示
    + 网络错误诊断
    + Sensor Hub 与 D1 引用用同一套代码

## 23/12/26
- Todoist
    说明：展示客户在Todist添加的代办事项与详情
    需求：
        + 配置界面新增 Todist API Token 配置
        + 默认提示界面(引导页)
        + Todist 列表显示页， 详情页
- 示例程序
$ curl -X GET \
  https://api.todoist.com/rest/v2/tasks \
  -H "Authorization: Bearer $token"
```
import requests

headers = {
    "Authorization": "Bearer 009c6c6e9d0b5bc61730aa5674fb6220c8025337"  # 替换为您的有效令牌
}

url = "https://api.todoist.com/rest/v2/tasks"

response = requests.get(url, headers=headers)
data = response.json()

# 处理响应数据
if response.status_code == 200:
    print(data)
else:
    print("请求失败:", response.status_code)
    print("错误信息:", data["error"])

```
```
import requests

headers = {
    "Authorization": "Bearer 009c6c6e9d0b5bc61730aa5674fb6220c8025337"  # 替换为您的有效令牌
}

url = "https://api.todoist.com/rest/v2/tasks/7534992183/close"

response = requests.post(url, headers=headers)

if response.status_code == 204:
    print("任务已成功关闭")
else:
    print("关闭任务时出现错误")

```
- 返回数据
```
[{'id': '7534992183', 'assigner_id': None, 'assignee_id': None, 'project_id': '2325578894', 'section_id': None, 'parent_id': None, 'order': 1, 'content': '任务1', 'description': '123', 'is_completed': False, 'labels': [], 'priority': 4, 'comment_count': 0, 'creator_id': '47504791', 'created_at': '2023-12-27T01:33:40.006337Z', 'due': {'date': '2023-12-27', 'string': '12月27日16:00', 'lang': 'zh', 'is_recurring': False, 'datetime': '2023-12-27T16:00:00'}, 'url': 'https://todoist.com/showTask?id=7534992183', 'duration': None}, 
{'id': '7534993097', 'assigner_id': None, 'assignee_id': None, 'project_id': '2325578894', 'section_id': None, 'parent_id': None, 'order': 2, 'content': '任务2', 'description': '123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789123456789', 'is_completed': False, 'labels': [], 'priority': 3, 'comment_count': 0, 'creator_id': '47504791', 'created_at': '2023-12-27T01:34:38.238429Z', 'due': {'date': '2023-12-27', 'timezone': 'Asia/Shanghai', 'string': '12月27日21:00', 'lang': 'zh', 'is_recurring': False, 'datetime': '2023-12-27T13:00:00Z'}, 'url': 'https://todoist.com/showTask?id=7534993097', 'duration': None}]
```
- 响应示例
```
{
    "creator_id": "2671355",
    "created_at": "2019-12-11T22:36:50.000000Z",
    "assignee_id": null,
    "assigner_id": null,
    "comment_count": 0,
    "is_completed": false,
    "content": "Buy Milk",
    "description": "",
    "due": {
        "date": "2016-09-01",
        "is_recurring": false,
        "datetime": "2016-09-01T12:00:00.000000Z",
        "string": "tomorrow at 12",
        "timezone": "Europe/Moscow"
    },
    "duration": null,
    "id": "2995104339", //任务ID
    "labels": [],
    "order": 1,
    "priority": 4,
    "project_id": "2203306141",
    "section_id": null,
    "parent_id": null,
    "url": "https://todoist.com/showTask?id=2995104339"
}
```

# 23/12/28
+ Todoist
    + 过滤非当日任务
    + 子页面跳转回父页面
    + 过期任务的提示
    + 任务的完成

# 23/12/29
+ Screen Mirroring
    + 在没有配置时进入引导界面
    + 在配置完成后，进入app有个等待画面

+ web界面需要的提供的数据
+ Todoist
    + api Token
+ Screen Mirroring
    + 目标计算机IP
    + 端口号port
    + 设置密码

+ setup完成提示重启界面优化

# 24/01/02 - 24/01/06
# 上周工作
    + D1
        - Todoist APP开发 >>> done
            + TodoistAPI文档阅读
            + 接口调用的验证及实现
            + UI的绘制
            + todoistAPI接口信息的获取和解析
            + 详情页面的跳转
        - Screen Mirroring 功能完善
            + 等待界面和异常界面的UI绘制
            + 逻辑完善
    + sensor_hub
        - 调整故障通知界面UI
        - 重新整理故障文本
    + hub
        + 排查ss_mp无法正常获取远程日志
        + 单元测试连接、调用失败问题
# 本周工作
    + D1
        + GAME 完善
        + Network Wizard 完善和移植

# 24/01/02
# Game App
# 实现逻辑
- 1.进入APP后判断当前是否存在游戏文件，若不存在则引导用户至app setting中添加
- 2.存在游戏则进入等待手柄连接UI界面
- 3.完成手柄连接后，进入游戏列表
- 4.在游戏列表中选择游戏进入
- 5.游戏中.....
- 6.退出后进入游戏列表
- 7.退出app
# 游戏列表
- 游戏的上传和删除均通过web
- 在web中显示当前游戏和剩余磁盘空间大小

+ web界面需要的提供的数据
+ Todoist
    + api Token
+ Screen Mirroring
    + 目标计算机IP
    + 端口号port
    + 设置密码
+ Game
    + 游戏上传
    + 游戏删除
    + 游戏大小上传限制

# 24/01/04
+ 三个软件支持web portal配置
+ 移植网络诊断模块


# 24/02/05
+ html联调
+ 调整网络诊断模块UI
+ 提供现有的二维码信息
+ 故障测试用例评审
+ 12月份自评

+ BUG
    + 展示错误信息后取消，下一次展示时会有错误码重复显示

+ 现有的二维码信息
    + computer_monitor
        + 内容：提示用户下载程序的网址
    + game_emulator
        + 内容：手柄连接模式错误
        + 文本标题：Controller not in AUTO mode.
        + 文本提示信息：Press the Start button on the controller for 5 seconds to turn it off. Then press B + Start for 1 second to switch to AUTO mode.
    + now_playing
        + 内容：蓝牙连接错误
        + 文本标题：Connection failed.
        + 文本提示信息：This is not a valid iOS device. Please check and try again.
    + screen_mirroring
        + 内容：远程屏幕连接失败
        + 文本标题：Connection failed!
        + 文本提示信息：Please check the configuration and try again!
    + tips_support
        + 内容：了解更多信息，帮助用户跳转至FAQ网站
    + todoist
        + 内容：任务界面跳转，直接跳转至todoist网站的任务界面
    + notification/setup/diagnostics
        + 内容：
        + 文本标题：
        + 文本提示信息：
    
+ 需要的图标







16
f0c8 -- 正方形
f133 -- 日历
f057 -- 错误
f058 -- 正确
f110 -- 进行中
f111 -- 圆圈等待

32
f005 -- 星星
f294 -- 蓝牙图标
f11b -- 游戏手柄
f055 -- 圆圈加号

f294 -> 62164
f0c8 -> 61640
f005 -> 61445
f11b -> 61723
f133 -> 61747
f057 -> 61527
f058 -> 61528
f110 -> 61712
f111 -> 61713
f055 -> 61525


# 24/01/08 - 24/01/13
# 上周工作
- D1
    - games app
        - 手柄连接引导和游戏列表UI界面的绘制
        - 游戏上传逻辑实现
        - 游戏删除逻辑实现
        - 修复反复进入APP卡死问题
    - 网络诊断模块
        - 重新调整诊断流程
        - 绘制网络诊断功能的流程UI
    - SCREEN_MIRRORiNG
        - 修复画面显示异常问题
- hub
    - 修复在ss_mp环境下，无法上传远程的问题
# 本周工作
- D1
    - 网络诊断模块
        - 测试用例的补充及测试
    - 产测流程的调整
    - 在设置增加一个对退出弹窗的确认按钮
    - 其他问题的修复


# 24/01/08
    - web界面的支持
    - 网络诊断模块测试用例的补充：
        1.在连接上路由器后断网
        2.DNS解析错误
    - 网络诊断模块文案的确认

HUB 版本迭代次数
H1/H1B(1.8.0-1.9.8共16次)(缺1.8.2、1.8.4、1.9.2)


H1B重大升级内容：
1.9.8:支持SS1传感器
1.9.5：新增探头状态上报
     ：新增对无zigbee芯片hub的支持
     ：开机100s后开启http失败10次后重启
1.9.1：支持ST9、ST10传感器

H1重大升级内容：
1.9.8：支持7.5inch ble版本

1.9.4 修复BUG：3 新增优化/功能：1
1.9.5 修复BUG：14 新增优化/功能：6
1.9.6 修复BUG：0 新增优化：4
1.9.7/1.9.8 修复BUG：3 新增优化：6

# 24/01/13
- 增加加载超时弹窗 >>>done
- 在game app中暂时关闭ping接口 >>> 待自侧
- 网络诊断UI优化
- 重置设备文案优化 >>> done
- 产测增加对屏幕安装的检测步骤
- web界面的更改
- 第一次开机不对网络超时进行判断


# 24/01/16
- ui调整内容
    - 文本调整
        - computer monitor
            - 提示连接界面 >> done
            - 主界面微调 >> done
            - 连接等待界面调整 >> done
        - game
            - 图标更替 >> done
        - now playing 
            - 等待蓝牙连接文本微调 >> done
        - todoist
            - 图标替换 >> done
            - 列表界面调整 >> done
            - 详细界面调整 >> done
        - Stock
            - 查看当超过10后会不会有影响 >> 有影响，待确认修改字体
        - tips
            - ui微调 >> done
        - 通知
            - 详细下拉 >> done(在系统级通知中下滑会卡顿)
        - 网络诊断
            - ui调整
        
    - 二维码调整
        - notification info、wornning级别不显示二维码，error级别显示二维码
            - 根据是否需要显示二维码来决定
        - 二维码下框修改为more >> done
        
+ 现有的二维码信息
    + computer_monitor
        + 内容：提示用户下载程序的网址
    + game_emulator
        + 内容：手柄连接模式错误
        + 文本标题：Controller not in AUTO mode.
        + 文本提示信息：Press the Start button on the controller for 5 seconds to turn it off. Then press B + Start for 1 second to switch to AUTO mode.
    + now_playing
        + 内容：蓝牙连接错误
        + 文本标题：Connection failed.
        + 文本提示信息：This is not a valid iOS device. Please check and try again.
    + screen_mirroring
        + 内容：远程屏幕连接失败
        + 文本标题：Connection failed!
        + 文本提示信息：Please check the configuration and try again!
    + tips_support
        + 内容：了解更多信息，帮助用户跳转至FAQ网站
    + todoist
        + 内容：任务界面跳转，直接跳转至todoist网站的任务界面
    + 配置引导
        + 内容： 需要配置的app，在未进行配置的情况引导客户。
    + 接口超时(weather、stock、cryptocurrency、todoist)
        + 内容： 接口调用超时
        + 文本标题：Resource retrieval timed out.
        + 文本提示信息：Please ensure a stable network connection and retry.
    + notification/setup/diagnostics
        + 错误码引导界面，参照自定义错误码内容


2024/01/19
+ URL替换
+ web界面文案优化
+ app图标替换
+ setup失败提示

2024/01/22
+ todoist
    + 返回提示修改为honse
    + 超过6个时下滚到底部再翻页
    + 选项前使用圆形样式

+ setup
    + connet按键样式调整
+ url替换
    + 配置页:https://dock.myvobot.com/guide/apps/

2024/01/23
+ 故障系统故障恢复清除弹窗逻辑修改
+ 文本校对后的修改
+ setup web界面的更改
+ 故障码文案的校对与修改

## 内部归因
- 通常情况为
    1.
- 在以下场景出现
    1.
- 错误代码说明：
- 其他潜在原因：暂无

## UI
- 标题：Error
- 错误信息：Wi-Fi connection problem.
- 具体提示
- 错误码：
- 错误提示语：
- 排查引导
    + 1. 
## FAQ
- 2001 Unable to find Wi-Fi.
- 
- 请按照以下步骤进行检查：
    1.
若通过上述步骤操作后，问题仍然存在，请通过邮箱(info@vobot.com)或点此()联系我们获取进一步的帮助。


## 小电视ota流程
在App中选择OTA选项，此时将重启并运行factory分区中的固件，将自动连接Wi-Fi，下载新的固件并更新到App分区；
需要单独将一个OTA固件烧录至factory分区中，这个OTA程序是独立于主程序单独运行的。
不清楚的是，怎么确定将固件更新至哪个分区，是由 esp_https_ota 这个函数自动选择还是

2023/1/24
+ 状态码新增一个配置，在有这个配置时，用户可以自定义跳转至指定页面 >> 延后
+ 2007状态码改用ntp获取失败触发，并且更细分内容 >> 延后

+ 文本优化
    + 番茄钟
        Pomodoro Timer >>> Pomodoro
        Dedicated Time >>> FOCUS
        xxxx (休息时间) >>> BREAK
    + 屏幕扩展
        标题下文本替换
        The Screen Mirroring App allows you to use the screen of your Mini Dock device as an extended display for your computer through a VNC connection. If you are using this feature for the first time, please refer to this user guide for instructions.
        VNC Server IP
        Note: Please ensure that your computer and Mini Dock device are connected to the same network, i.e., within the same LAN.
        e.g., 192.168.0.100
        VNC Server Port
        e.g., 5900
        VNC Server Password
        Enter password
        url替换
        <div class="form-text">
            Please ensure that the computer running the VNC server is on the same local network.Download the screen mirroring software:
            <a href=" http://vobot.oss-us-west-1.aliyuncs.com/firmware/mini_dock/download/mac/computer_monitor.zip" target="_blank" class="hint"> Windows</a> |
            <a href=" http://vobot.oss-us-west-1.aliyuncs.com/firmware/mini_dock/download/mac/computer_monitor.zip" target="_blank" class="hint"> macOS</a> |
            <a href=" http://vobot.oss-us-west-1.aliyuncs.com/firmware/mini_dock/download/mac/computer_monitor.zip" target="_blank" class="hint"> Android</a>
        </div>
    + setup 
        wifi名
        Network Name
            Enter the SSID
    + 电脑监控
        提示页文本替换
            If this is your first time using, please access the link below on your computer for instructions.(https://xxx)
    + todoist
        web 占位符
        Enter your Todoist API Token
    

+ 产测流程更改>>
3. 开始产测
现象：前面板的led灯开始闪烁，lcd显示红框，rgb显示白灯>>>>LED改为常亮；rgb显示白灯；LCD上显示，检查内容
如果OK，按编码器确认按键，如果NG，按esc按键，再测试下一项

4. 测试Beep； 
蜂鸣器开始beep，LCD上显示，检查内容；如果OK，按编码器确认按键，如果NG，按esc按键，再测试下一项

4. lcd检测
提示旋转编码器切换LCD颜色，检查LCD装配位置与LCD显示；
正向旋转3次旋钮->lcd屏幕颜色变化(红、绿、蓝)>反显旋转3次
如果OK，按编码器确认按键，如果NG，按esc按键，再测试下一项

5. 测试结果展示与上传：
LCD上显示本次测试结果，按编码器确认按键上传测试结果，如果重测，按esc按键，重新测试；

上传产测结果前将SN、DEVKEY、测试结果(led、蜂鸣器、LCD)一起显示出来

现有的：5. rgb灯检测/6. 发送产测结果  不需要了/7. 产测结束

13台出货SN码
806599A3E9D0
806599A3E3D8
806599A3E6B8
806599A5018C
806599A3E924
806599A3E740
806599A3E8F0
806599A3E90C
806599A4F968
806599A3E780
806599A3E74C
806599A3EA4C
806599A3E920
806599A3E9F4

./go build
esptool.py -p /dev/ttyACM0 -b 2000000 --before default_reset --after hard_reset --chip esp32s3 --no-stub         write_flash --flash_mode dio --flash_size detect --flash_freq 80m         0xE0000 build-DOCK_HUB/micropython.bin
./go monitor

port="/dev/ttyACM0"; ./go build; esptool.py -p "$port" -b 2000000 --before default_reset --after hard_reset --chip esp32s3 --no-stub write_flash --flash_mode dio --flash_size detect --flash_freq 80m 0xE0000 build-DOCK_HUB/micropython.bin; ./go monitor

idf.py -DMICROPY_BOARD=$BOARD -DMICROPY_BOARD_DIR=$BOARD_DIR -B$BUILD_DIR build

2024/01/27
+ 出入站端口
    + 出站
        + UDP协议 端口: 123 目的域: pool.ntp.org、0.asia.pool.ntp.org、europe.pool.ntp.org、time.google.com、0.north-america.pool.ntp.org  功能: ntp时间同步
        + TCP协议 端口: 443 目的域: sync.sync-sign.com 功能: Device Health Report
        + TCP协议 端口: 443 目的域: update.sync-sign.com 功能: OTA Update Server
        + TCP协议 端口: 443 目的域: apiproxy.myvobot.com 功能: 获取资源信息
        + TCP协议 端口: 443 目的域: api.todoist.com 功能: 同步todoist任务信息
        + TCP协议 端口: 80 目的域: pub.sync-sign.com 功能: Time Server (as failsafe to NTP)

54C7DA38C1A40A882B065F1E5D420E

+ 产测流程调整
+ 

# 本周任务
    + D1
        + 故障系统FAQ内容整理以及引导内容文案调整
        + ota固件应用层逻辑实现，以及对企业级wifi和开放式wifi的调整
        + 文本优化，app ui调整
        + 产测流程变更
        + web界面的更改
        + 修复编码器旋转无效的问题
        + 修复和调整一些bug
        + 出货设备的产测和出货测试
    + hub
        + 排查h2连接不上OZ_Office的问题
        + 协助FAE/测试工程师排查问题
# 下周任务
    + D1继续进行bug的修复和优化项的调整
    + SS1电量问题的长期跟踪排查

2024/01/29
+ 当前HOME页app的排列顺序
+ Calendar
+ Weather
+ Stock
+ Cryptocurrency
+ Pomodoro
+ Settings
+ PC H/W Monitoring
+ Screen Mirroring
+ Game Emulator
+ Now Playing
+ Todoist

+ 开箱默认聚焦在最后一个app

2024/1/31
+ 长测部署
    + H1
    + 2.0.0 版本一个
    + H1B
    + 1.9.8/2.0.0 正常版本各一个    
    + 1.9.8/2.0.0 关闭维护性重启各一个
    + 1.9.8/2.0.0 路由器定时关闭各一个
正则表达式是一种强大的工具，用于在文本中搜索、匹配和替换特定模式的字符串。下面是一个简单的正则表达式教程，介绍了正则表达式的基本用法和常用的元字符和模式：

字面匹配：正则表达式可以直接匹配字面字符。例如，正则表达式 abc 可以匹配字符串中连续的 "abc"。

字符类：使用方括号 [] 来定义一个字符类，表示匹配其中任意一个字符。例如，[aeiou] 可以匹配任何一个元音字母。

范围：在字符类中可以使用连字符 - 来表示一个范围。例如，[a-z] 可以匹配任何一个小写字母。

元字符：正则表达式中有一些特殊字符被称为元字符，具有特殊的含义。例如，. 表示匹配任意一个字符，\d 表示匹配一个数字字符，\s 表示匹配一个空白字符。

量词：使用量词来指定匹配的次数。例如，* 表示匹配前面的模式零次或多次，+ 表示匹配一次或多次，? 表示匹配零次或一次，{n} 表示匹配恰好 n 次，{n,} 表示匹配至少 n 次。

边界匹配：使用边界匹配符号来指定匹配的位置。例如，^ 表示匹配字符串的开始位置，$ 表示匹配字符串的结束位置，\b 表示匹配单词边界。

分组和捕获：使用圆括号 () 来创建一个分组，并可以通过捕获组来提取匹配的内容。

转义字符：使用反斜杠 \ 来转义特殊字符，使其失去特殊含义。例如，\. 可以匹配一个点号。


2024/2/04
+ 发布0.2.2 
1. Settings > My Devices 改为 My Device >> done
2. Settings > My Device 里面，增加一个Reboot吧（程序有bug，为了我重启还得拔两条线） >> done
3. 天气的location信息在web上修改后，因为没有过期，它不会及时去取 >> done
4. DOCK系列产品的服务器网址修改 >> done
```
    DOCK系列产品的服务器网址修改为：

    - 固件下载：https://dock-file.myvobot.com  
        - 测试链接：https://dock-file.myvobot.com/firmware/mini_dock/download/mac/computer_monitor.zip
    - ping action: https://dock-sync.myvobot.com 
        - 测试链接：https://dock-sync.myvobot.com/ping?id=01234567890A
    - 检查新固件：https://dock-update.myvobot.com  
        - 测试链接：https://dock-update.myvobot.com/checkUpgrades?deviceId=806599A3EA40&types=system&versions=0.2.0
    - 取ntp时间: http://dock-pub.myvobot.com/time    

    下面这个不用改：

    - 访问API的缓存代理: https://apiproxy.myvobot.com 
```
5. 在固件名字里面尽量只使用小写和横杠，例如，application-dock-hub-0.2.0-prd.bin  application-dock-hub-0.2.1-prd.bin
6. 在OSS上，有 oss://vobot/firmware/dock_hub/ 也有：oss://vobot/firmware/mini_dock/ 建议统一到mini_dock文件夹里面
7. Screen Mirroring 出错时，除了说连接失败，还应该显示：VNC Server: 192.168.66.123:5901 >> done
8. 开机10分钟之后再检查更新 >> done
9. 这个页面需要适当的CSS优化，指setup Wi-Fi 的web界面 >> done(调大字体，后续在进行进一步的更改)
10. 在D1的Network & Internet页面，假如当前连接不到热点，SSID位置应该给出“拟连接的热点的名称”，RSSI一列，可以用“Access Point Not Found”文本来代替信号图标；至于IP地址等信息，不应该是0.0.0.0，应该写"N/A"，代表不可用 >> done
11. Setup Wi-Fi这个名字，在英文中不太正规，改为：Wi-Fi Configuration >> done

html加载周期

+ 长测设备
ttyUSB0 - > D1BC38F22C98  > 2.0.0 定时断网
ttyUSB1 - > D8BC38F22FF0  > 2.0.0 正常
ttyUSB2 - > 2.0.0 h1
ttyUSB3 - > D8BC38F22F48  > 2.0.0 关闭重启
ttyUSB4 - > D8BC38F23020  > 1.9.8 定时断网 
ttyUSB5 - > D8BC38F22C9C  > 1.9.8 关闭重启 

2024/2/18
+ 通知标题样式长度过长修改为滚动
+ now playing 退出时增加退出等待界面

# input
def get_settings_json():
    # When entering the application configuration, the device calls this function and generates application-specific HTML content based on the returned dictionary.
    return {
        "category": "Other", # App type[Lifestyle/Finance/Experimental/Other]
        "form": [{
            "type": "input", # Regular input field
            "default": "30", # Default value for configuration option
            "caption": "Countdown Timer Duration", # Title corresponding to the configuration option
            "name": "remainder", # Keyword for saving the configuration option
            "attributes": {"maxLength": 6, "placeholder":"e.g., 300"}, # Attributes of the input field
        }]
    }

# select
def get_settings_json():
    # When entering the application configuration, the device calls this function and generates application-specific HTML content based on the returned dictionary.
    return {
        "category": "Other", # App type[Lifestyle/Finance/Experimental/Other]
        "form": [{
            "type": "select", # 输入类型
            "default": "optionname", # 默认值(填入option中的选项名称)
            "caption": "Countdown Timer Duration", # 标题名称
            "name": "remainder", # 保存时的键值
            "option":[("optionname", "value"), ("optionname1", "value1")]# 选项名称及对应的值
        }]
    }

# checkbox
def get_settings_json():
    # When entering the application configuration, the device calls this function and generates application-specific HTML content based on the returned dictionary.
    return {
        "category": "Other", # App type[Lifestyle/Finance/Experimental/Other]
        "form": [{
            "type": "checkbox", # 输入类型
            "default": "optionname", # 默认值(填入option中的选项名称)
            "caption": "Countdown Timer Duration", # 标题名称
            "name": "remainder", # 保存时的键值
            "option":[("optionname", "value"), ("optionname1", "value1")]# 选项名称及对应的值
        }]
    }

# radio
def get_settings_json():
    # When entering the application configuration, the device calls this function and generates application-specific HTML content based on the returned dictionary.
    return {
        "category": "Other", # App type[Lifestyle/Finance/Experimental/Other]
        "form": [{
            "type": "radio", # 输入类型
            "default": "optionname", # 默认值(填入option中的选项名称)
            "caption": "Countdown Timer Duration", # 标题名称
            "name": "remainder", # 保存时的键值
            "option":[("optionname", "value"), ("optionname1", "value1")]# 选项名称及对应的值
        }]
    }

,{
            "type": "select", # 输入类型
            "default": "value", # 默认值(填入option中的值)
            "caption": "Countdown Timer Duration", # 标题名称
            "name": "remainder1", # 保存时的键值
            "option":[("optionname", "value"), ("optionname1", "value1")],# 选项名称及对应的值
            "tip": _("Please ensure that the computer running the VNC server is on the same local network. Download the screen mirroring software: "),
            "hint": {
                "url": "https://dock.myvobot.com/guide/apps/screen-mirroing/",
                "label": "Windows | macOS | Android",
            }
        },{
            "type": "checkbox", # 输入类型
            "default": ["value"], # 默认值(填入option中的值)
            "caption": "Countdown Timer Duration", # 标题名称
            "name": "remainder2", # 保存时的键值
            "option":[("optionname", "value"), ("optionname1", "value1")],# 选项名称及对应的值
            "tip": _("Please ensure that the computer running the VNC server is on the same local network. Download the screen mirroring software: "),
            "hint": {
                "url": "https://dock.myvobot.com/guide/apps/screen-mirroing/",
                "label": "Windows | macOS | Android",
            }
        },{
            "type": "radio", # 输入类型
            "default": "value", # 默认值(填入option中的值)
            "caption": "Countdown Timer Duration", # 标题名称
            "name": "remainder3", # 保存时的键值
            "option":[("optionname", "value"), ("optionname1", "value1")],# 选项名称及对应的值
            "tip": _("Please ensure that the computer running the VNC server is on the same local network. Download the screen mirroring software: "),
            "hint": {
                "url": "https://dock.myvobot.com/guide/apps/screen-mirroing/",
                "label": "Windows | macOS | Android",
            }
        }

step 1: 设备连接 Wi-Fi（Connect the Device to Wi-Fi AP）
##### STATUS_WIFI_CONNECTED >>>> Wi-Fi Connected

    -   WiFi 已连接 （但是其他的状态也可能代表 WiFi 已连接，比如 STATUS_BIND_AND_MQTT_START，STATUS_INTERNET_CONNECTED）

#####   STATUS_WIFI_START_CONNECT: >>> Connecting to Wi-Fi SSID: XXXXX

    -   设备在尝试连接 WiFi

#####   STATUS_WIFI_CONNECT_FAILURE >>> Failed to connect your Wi-Fi AP. The password may be incorrect, please double check and try again. Meanwhile, please make sure the Wi-Fi auth mode is WPA/WPA2.
    -   (1) Incorrect password?
    -   (2) AP 的加密协议是否为 WPA/WPA2?

step 2: 设备登陆 IoT 服务器（Register the device to the cloud server）
#####   STATUS_INTERNET_CONNECTED >>>> Device login the cloud server OK

    -   设备从服务器登陆成功，获得了 access token
    -   Hub 调用Post /certificate 接口创建MQTT证书
    -   （但是其他的状态也可能代表 Internet 已连接，比如 STATUS_BIND_AND_MQTT_START）

#####   STATUS_INTERNET_FAILURE >>> (Wi-Fi connected. However it) Failed to connect to the Internet or our server, please try again. Or check the outbound firewall/blacklist settings on your router.

    -   (1) Failed to connect the Internet;
    -   (2) 连接不上我们的服务器,原因可能是网络环境内的防火墙设置或者路由器的一些设置导致的

#####   STATUS_LOGIN_FAILURE >>> Internet connected however there is a glitch in our cloud service. Please contact us with your device's serial number.

-   STATUS_ACCESS_KEY_EXPIRED >>> Identity information expired, please try again.
    -   Device 登录服务器需要的 accesskey 过期,这种情况一般不会出现,即使出现也不是客户的问题

step 3: 绑定账号并激活 MQTT 服务（Bind the Device to Current Account）
v1.5.2: 第三步成功后就会断开蓝牙
#####   STATUS_BIND_AND_MQTT_SUCCESS: Device Linked to Your Account

    -   Hub 调用 POST /user 绑定设备到账号，且 MQTT 激活成功（即表示Hub 信息 certificate_oregon已存在，则继续下一步 ）

#####   STATUS_BIND_FAILURE 
    >>> Failed to link the device with your account. Please contact us for help.

#####   STATUS_INTERNET_FAILURE >>> 提示和上面一样

    -   绑定过程中，出现了互联网连接错误

#####   STATUS_BIND_DISABLE >>> (The Wi-Fi connected successfully. However) This device is in developer mode and cannot be linked to your account.

    -   hub 当前处于开发者模式,需要到 hub portal 中关闭相关的设置

#####   STATUS_BIND_TIMEOUT (**App 什么情况下报这个错误？每一秒检查设备返回的状态码，如果到达40次还没有绑定成功，且没有返回其他的失败原因，则返回绑定超时，设备未响应**) 
    >>> Connecting the device timed out. Please check whether the device is in pairing mode or whether the Internet is good.

#####   STATUS_ACTIVATE_FAILURE >>> Unable to activate this device on our cloud server. Please contact us with your device's serial number.

    -   激活失败,应该和 MQTT 认证有关

#####   STATUS_DISK_CORRUPTION >>> There is a glitch on this device. Please restore it to factory default then try again, or contact us for help.

step 4: 等待同步设备信息（Waiting to sync device infomation）
#####   REQUEST_DEVICE_INFO_FAIL (**App 什么情况下报这个错误？绑定完成后，将设备添加到设备列表里面，获取设备信息，这一步通常不会失败，如果失败了一般是网络原因**) 
    >>> Failed to load device info. Please check your Internet conditions and try again.
    
#####   STATUS_WAIT_SYNC_INFO_FAILURE

    - Hub MQTT未连接，请检查端口8883与8888是否开放
    
    - 版本信息同步失败，请检查网络，重启Hub

# 2月23日
- 调整app通知弹窗的按键
    - 增加滚动效果
    - 只允许输入string类型， 默认为none,为string类型是响应按键，文字为输入内容

# 2月26日-3月1日
# 上周
- D1
    - 修复已知问题
    - 完善开发者文文档以及开放API模块的调整
    - 发布0.2.3版本
- HUB
    - 排查客户侧问题
# 本周
- D1
    - 产测新增功能
- H5
    - 根据开发计划完成开发任务

# 2月4日-2月8日
# 本周
- D1
    - 修复已知问题
    - 增加开发者模式开关 >> 已完成
    - 发布0.2.3版本 >> 已完成
- H5
    - 将D1中的部分模块移植至H5中 >> 完成通知模块、故障系统、setting的移植
# 下周
- D1
    - 修复已知问题
    - 发布0.2.4版本
- H5
    - H5一阶段任务

# 3月7日
- D1
    - SETUP关闭错误弹窗，将弹窗作为setup流程的一部分
    - setup支持刷新web界面刷新
    - 番茄钟问题
    - 夏令时时区同步问题
# 3月8日
- D1
    - 不自动跳转问题

# 3月4日-3月8日
# 本周
- D1
    - 修复已知问题
    - 发布0.2.4/0.2.5版本 >> 已完成
- H5
    - 将D1中的模块移植至H5中 >> 完成产测的移植，OTA模块延后
    - 确认H5中的UI结构目录及元素
- SS1修复OTA固件开机无法自动运行的问题
# 上周
- H5
    - UI界面的设计
    - Sensor APP的开发
    - 其他协助任务

# 3月11日
- H5 
    - UI界面的设计
        - Sensor列表
        - Sensor详情页
            - 历史温度数据折线图
            - 历史湿度数据折线图
            - 数据详情页
        - Sensor故障提示

# 3月13日
- 字库生成
    - 图标
        - Wi-Fi 28 f1eb
        - 蓝牙  28  f294
        - 探头  28  22  f1e6 e560 e55d
        - 电量  28  22  f240 f241 f242 f243 f244
        - °    28  22
        - 打勾  22  f00c
        - 放大镜 28 f002

    - 数字(Noto Sans)
        - 96
        - 85
        - 62
        - 48
        - 44
        - 36

    - 字体(Roboto)
        - 22
        - 28
        - 44
        - 48
61441,61448,61451,61452,61453,61457,61459,61461,61465,61468,61473,61478,61479,61480,61488,61502,61512,61515,61516,61517,61521,61522,61523,61524,61528,61543,61544,61550,61552,61553,61556,61559,61560,61561,61563,61587,61589,61636,61637,61639,61671,61674,61683,61724,61732,61770,61787,61914,61931,62016,62017,62018,62019,62020,62087,62099,62212,62296,62297,62298,62189,62810,63426,62437,63231,62100,61610,61611,61675,61463,63337,61640,61747,61527,61712,61713,61926,58720,58717,61442

# 3月18日-3月22日
# 本周
- D1
    - 将datatime更改为clocktime
- H5
    - 绘制H5 UI原型图并通过评审
    - 根据原型图编译出对应的字库
    - 在代码中完成sensor APP的UI绘制
    - sensor APP的开发 >>> 70%
# 上周
- H5
    - sensor APP的开发[1]
    - Identify Device SN APP的开发[1]
    - H5 探头的验证[1]
- D1
    - 修复已知问题
    - 完成jira上的优化项
    - 发布v0.2.6版本


# 3月16日
- H5
    - 历史数据时间调整 >>> done
    - 掉线时间调整 >>> done
# 3月18日
- H5
    - sensor APP
        - 详细数据页数据实时更新 >>> done
        - 数据更新时间显示调整 >>> done
        - 新增故障引导界面 >>> done
        - 新增设备和删除设备逻辑 >>> done
        - 支持显示sensor名称
        - 支持戳一下变色 >>> done
        - 支持警报变色
    - Identify Device SN APP
    - OTA支持
        - 
    - LED点阵: 轮播 Sensor 数据

# 3月19日
- H5
    - sensor APP
        - 详细数据页数据实时更新 >>> done
        - 数据更新时间显示调整 >>> done
        - 新增故障引导界面 >>> done
        - 新增设备和删除设备逻辑 >>> done
        - 支持显示sensor名称 >>> done
        - 支持戳一下变色 >>> done
        - 支持警报变色
    - Identify Device SN APP
    - OTA支持
        - 支持OTA分区
        - 支持通过coap获取版本信息
        - 支持在OTA分区中通过https同步进度
        - 升级步骤
            - 1.检查网络
            - 2.
    - LED点阵: 轮播 Sensor 数据
        - 显示规则
            - 温度
                -最大支持99.9度
                -低温支持-999度，小数点后一位只支持至-9.9度
            - 湿度
                -支持0-100%
                靠右显示

# 3月22日
- H5
    - sensor APP
        - 支持警报变色
    - Identify Device SN APP
    - OTA支持
        - 支持在OTA分区中通过https同步进度
        - 支持通过远程指令完成升级，并分为强制升级和自动升级
        - 开机检测升级
    - LED点阵: 轮播 Sensor 数据
        - 显示规则
            - 温度
                -最大支持99.9度
                -低温支持-999度，小数点后一位只支持至-9.9度
            - 湿度
                -支持0-100%
                靠右显示

# 本周
- H5
    - sensor APP的开发 >>> 基本完成
    - OTA流程实现 >>> 70%
    - LED点阵：轮播 Sensor 数据 >>> done
    - UI 界面原型图确认与实现 >>> 待确认后调整
    - 修复已知问题
# 下周
- H5
    - [1]OTA流程实现
    - [1]Identify Device SN APP的开发
    - [2]产测流程调整
    - [3]H5 探头的验证

- [1] H5-Lite Sensor App 卡片警报状态展示 >>> Thomas
- [1] H5-Lite OTA 支持 >>> Thomas 周一结束
- [1] UI 界面原型图确认与实现 >>> Thomas
    - Sensor 错误引导页面
    - Identify Device 界面确认
- [2] 网络诊断接口与 UI 调整 >>> Thomas
- [2] 产测修改与支持
- [3] Identify Device SN APP的开发 >>> Thomas >>> 延后
- [3] H5-Lite 探头验证与功能实现 >>> Thomas >>> 延后

# 3月27日
- H5
    - UI 界面原型图确认与实现
    - 网络诊断接口与 UI 调整
    - 产测修改与支持
    - sensor app探头断开提示失效的修复

# 3月29日
- H5
    - 支持h5自身探头 >>> done
    - sensor App获取数据更新方式
    - 替换开机画面 >>> done
    - 亮度调整
    - 产测增加对探头的检测
    - 修改app 图标 >>> done
    - 修复jira问题


# 本周
- [1] H5-Lite Sensor App 卡片警报状态展示 >>> Done
- [1] H5-Lite OTA 支持 >>> Done
- [1] UI 界面原型图确认与实现 >>> Done
- [2] 网络诊断接口与 UI 调整 >>> Done
- H5自身探头验证及逻辑实现 >>> Done
- 修复已知问题
# 下周
- 修复已知问题
- Identify Device SN APP的开发


# 4月1日
- 亮度统一性调整
- 产测增加对探头的检测
- 支持警报提示
- 故障通知调整
- 修复jira问题

# 4月7日
- 网络没问题用 正确色(绿色) >>> done
- Led Assigned to 交互逻辑调整 >>> done
    a. LED Data View
        i. Time
        ii. Sensor Data
            1. Sensor Lite(非温湿度Sensor 时置灰)
                a. Temperature / Humidity(只有一个时直接跳转至LED Data View 所在页面层级)
- Sensor 卡片展示一条数据时， Name 用 28 加粗 >>> done
- Sensor Display Layout >>> Sensor View >>> done
    a. Single / Double / Quad
- Enable Prober Plugin Hub >>> Hub Internal Probe >>> done
- 24-Hour Time 放到 Locale 中 >>> done
- 故障引导调整
    - 针对问题给出详细的操作流程
- home页图标替换以及新增WIFI和蓝牙图标
- 数据历史界面优化
    - 调整切换速度
    - 时间格式调整
- 睡眠模式调整 >>> done
- 设置校准值后未及时同步

# 本周工作
    - UI 界面细节调整 >>> 进行中
    - 网络诊断接口重新调整 >>> Done
    - 部分功能优化
    - 0.1.1/0.1.2版本发布
    - 已知问题修复
# 下周工作
    - D1 
        - 已知问题修复
        - 0.2.6版本发布
    - H5
        - 功能优化
        - 已知问题修复

4月9日
- H5
    - 故障引导调整
        - 针对问题给出详细的操作流程
    - home页图标替换以及新增WIFI和蓝牙图标
    - 数据历史界面优化
        - 调整切换速度
        - 时间格式调整
    - 设置校准值后未及时同步
    - 设备名称变更后未及时同步
    - led 和 lcd数据同步
    - 警报提示形式调整
    - sensor list名称修改，将sensor name与符号分开绘制
- D1
    - Sleep mode 默认值未同步导致的设置失效问题 >>> Done
    - 番茄钟配置单位变更 >>> Done
    - setup 提示框文案调整 >>> Done
    - setup 步骤提示优化 >>> Done
    - 开启开发者模式时，关闭看门狗重启 >>> Done
    - setup 手机界面优化 >>> Done
    - 产测删除IIC寻值 >>> Done
    - 移除时区配置 >>> Done
    - http连接10次失败先提示再重启 >>> Done

4月10日
- H5
    - 故障引导调整
        - 针对问题给出详细的操作流程
    - home页图标替换以及新增WIFI和蓝牙图标
    - 数据历史界面优化
        - 调整切换速度
        - 时间格式调整 > done
    - 设置校准值后未及时同步 > done
    - 设备名称变更后未及时同步 > done
    - led 和 lcd数据同步 > done
    - 警报提示形式调整 > done
    - sensor list名称修改，将sensor name与符号分开绘制 > done
    - 网络诊断模块新增错误码210、211、212

- 设备同步
    - asset：node信息
    - property： 特有属性
    - attribute：通用属性 

4月11日
-H5
    - ui调整
    - 

# 本周工作
    - D1 
        - 已知问题修复
        - 0.2.6版本发布
    - H5
        - 功能优化
        - 已知问题修复
        - 一轮试用反馈问题修复
        - 0.1.3 发布 
# 下周工作
    - D1
        - 反馈问题修复
    - H5
        - 已知问题修复
        - 版本发布
    
# 4月18日
- H5 
    - 自身探头
        - 85度异常
        - 温度范围-55——125

- H5涉及到的URL
    - 错误码对应URL
    - 添加 sensor
    - Tips & Support
    - setup过程
        - 配置接收错误
        - 无线网络不可用
        - 账号绑定失败
        - 无法与服务器建立连接
        - 与 AP 连接失败(在没有错误码的情况)

STATUS_WIFI_START_CONNECT    = const(1) # 开始连接WiFi
STATUS_WIFI_CONNECTED        = const(2) # WiFi连接成功
STATUS_WIFI_CONNECT_FAILURE  = const(3) # WiFi连接失败
STATUS_WIFI_CONNECT_NO_IP    = const(3) # TODO: 区别于STATUS_WIFI_CONNECT_FAILURE，它表示WiFi连接上了，但是没有获得IP地址
STATUS_INTERNET_CONNECTED    = const(4) # 请求AccessKey成功
STATUS_INTERNET_FAILURE      = const(5) # 网络连接失败
STATUS_BIND_AND_RPC_START    = const(6) # 开始请求绑定
STATUS_BIND_AND_RPC_SUCCESS  = const(7) # 绑定成功，退出配网
STATUS_BIND_FAILURE          = const(8) # 绑定失败，返回值不是200
STATUS_IDLE                  = const(9) # Setup流程开始
STATUS_BIND_DISABLED         = const(10) # 退出配网
STATUS_LOGIN_FAILURE         = const(11) # 获取AccessKey失败，返回值不是200
STATUS_ACCESS_KEY_EXPIRED    = const(12) # AccessKey已过期
STATUS_ACTIVATE_FAILURE      = const(13) # 绑定的返回值不是200，或者返回值是200但没有有效信息/服务器返回了证书，但是取值无效（暂时不可能出现）
STATUS_DISK_CORRUPTION       = const(14) # 磁盘损坏，无法写入证书
STATUS_BIND_TIMEOUT          = const(20) # 只在App上自己用
STATUS_SETUP_COMPLETE        = const(21) # 只在App上自己用
STATUS_PROVISIONING_DATA_OK  = const(30) # 接收到Provisioning App提供的JSON, OK
STATUS_PROVISIONING_DATA_NG  = const(31) # 接收到Provisioning App提供的JSON,但是出错了
STATUS_ESPNOW_CONNECTED       = const(40) 
STATUS_ESPNOW_CONNECT_FAILURE = const(41)
STATUS_ESPNOW_DISABLED        = const(42)
STATUS_CONFIG_SAVED           = const(50)
STATUS_WIFI_DISABLED          = const(60) # 无线网络不可用！
STATUS_ETHERNET_DISABLED      = const(61) # 以太网不可用！


# 本周工作
    - D1 
        - 已知问题修复 >>> 进行中
    - H5
        - 功能优化
        - 已知问题修复
        - 二/三轮试用反馈问题修复
        - 0.1.4/0.1.5/0.1.6 版本发布 
# 下周工作
    - D1
        - [1] 反馈问题修复
        - [1] 重发0.2.6版本
    - H5
        - [1] 已知问题修复
        - [1] 产测功能完善
        - [1] 烧录版本发布
        - [2] 错误模块功能重新调整
        - [3] Identify Device SN APP的开发

# 4月22日
- 配置接收错误：STATUS_PROVISIONING_DATA_NG
    - 标题：The configuration information retrieval failed.
    - 内容：Device Name:
- Wi-Fi未初始化：STATUS_WIFI_DISABLED
    - 标题：Connection Failed with AP
    - 内容：wifi not available!
- STATUS_WIFI_START_CONNECT
    - 标题：
    - 内容：Connection Failed with AP
- STATUS_WIFI_CONNECTED
    - 标题：
    - 内容：Failed to establish connection with the server.
- STATUS_BIND_AND_RPC_START
    - 标题：
    - 内容：Account binding failed.

- setup过程中通过Blufi传递的错误码及对应的值:
    - [150] ---- [2000]
        - 未知的错误
    - [151] ---- [2001]
        - 1. 添加的 Wi-Fi 不存在
        - 2. 连接了禁用SSID的网络
    - [152] ---- [2002]
        - Wi-Fi 密码错误，连接失败
    - [153] ---- [2003]
        - 企业级模式下，用户名或密码错误
    - [154] ---- [2004]
        - Wi-Fi连接数量已达路由器连接上限
    - [155] ---- [2005]
        - 连接企业级Wi-Fi，认证服务器认证超时
    - [156] ---- [2006]
        - AP断开连接
    - [157] ---- [2007]
        - 1. Wi-Fi已经连接上，但网络断开
        - 2. DNS解析错误
        - 3. MAC地址冲突
    - [158] ---- [2008]
        - Wi-Fi名称错误
    - [159] ---- [2009]
        - 企业级模式下，用户名或密码为空
    - [160] ---- [2010]
        - 无法获取到IP地址
    - [161] ---- [2011]
        - 1. 防火墙端口限制
        - 2. 网络拥堵
    - [162] ---- [2012]
        - 认证方式不匹配导致的连接网络失败
    - [163] ---- [2013]
        - 信号值过低导致的断开(前提为在配置WiFi时设置了信号限制)

# 4月22日
- sensor异常状态引导流程提示 >> 剩余文本替换
- 查找APP
- 重构sensor app代码 >> done
- 产测新增对HUB自身探头的检测 >> done
- 增加戳一下变黄，并且聚焦到该sensor >> done


- 修改项:
    - 历史详情页切换卡顿 >>> 尽力优化
    - 等待卡片加载更改为 loading to sensor data... >> done
    - 显示两个卡片时，ST6的温度字体加大 >> done
    - 详情页修改为: Last Seen >> done

# 4月28日
- 查找APP
    - 显示周边扫描到的并且在HUB中存在描述文件的设备，对信号值也存在限制
    - 列表刷新规则，每5S更新一次列表
    - 显示的排序根据扫描到的信号值大小来排
    - 在戳一下设备后，设备列表中的该设备高亮显示，并聚焦至该设备，聚焦时间3s

- v0.1.7改动内容
    - 优化项/新增项
        - 新增sensor异常状态的引导流程
        - 修改ST6的测温范围
        - sensor app新增戳一下聚焦的功能
        - settings中的sensor list新增型号显示
        - 新增对H5自身探头CRC错误的判断
        - 在时区变更后，强制PING一次，同步时区
        - 优化历史界面的切换速度
    - 修复项
        - 修复关闭"Hub 自身探头"功能后，LED异常显示的问题
        - 修复在详情页戳一下报错的问题
        - 修复sensor app 在历史数据界面改变数据校准值时未更新的问题
        - 修复在setup模式中,错误弹窗显示异常内容的问题
        - 修复在设置12小时制后，睡眠模式显示错误时间的问题
        - 修复App 修改自动更新后，设备需退出重进My Devices才能更新的问题
    - 文案及UI调整详见jira

SN: MC806599A50024 KEY: hgms9p
SN: MC806599A4FE8C KEY: wn8dms
SN: MC806599A500CC KEY: d5w4gk

# 5月6日
- RGB api
    #### 初始化设备RGB灯[peripherals.rgb_init()]
    - **描述：** 在APP中启用并初始化设备的RGB灯。
    - **注意事项：** 该设置仅在自定义app中生效
    #### 停止启用设备RGB灯[peripherals.rgb_deinit()]
    - **描述：** 停止启用RGB灯，RGB灯恢复至系统配置。
    #### RGB灯数量[peripherals.rgb_count]
    - **描述：** 获取当前设备RGB灯的数量。
    #### 设置所有RGB灯的颜色[peripherals.set_all_rgb_color(rgb_color)]
    - **描述：** 配置所有RGB灯的颜色，使其统一显示一个颜色。
    - **参数：**
            + rgb_color:
                设置的rgb颜色,每个颜色的取值范围为(0-255),其中0表示完全透明，255表示完全不透明。
                格式:(R,G,B)
                例如:
                    红色:(255,0,0)
                    绿色:(0,255,0)
                    蓝色:(0,0,255)

    #### 设置每个RGB灯的颜色[peripherals.set_rgb_color(color_buffer)]
    - **描述：** 配置所有RGB灯的颜色，使其统一显示一个颜色。
    - **参数：**
            + color_buffer:
                设置的RGB颜色列表，每个列表中的颜色会根据索引映射到对应灯的位置
                格式:[(R,G,B),(R,G,B)...]
    - **返回值：** False（错误的列表内容）或 True（成功设置）。
    - **注意事项：** 列表的长度应对应设备RGB灯的数量，如果列表长度超过或者少于RGB灯的数量，将会返回False

- led api
    
    #### 初始化设备LED时钟阵列[peripherals.led_init()]
    - **描述：** 在APP中启用并初始化设备的LED时钟阵列。
    - **注意事项：** 该设置仅在自定义app中生效

    #### 停止启用设备LED时钟阵列[peripherals.led_deinit()]
    - **描述：** 停止启用LED时钟阵列，LED时钟阵列恢复至系统配置。

    #### 设置LED时钟阵列的亮度[peripherals.set_led_brightness(brightness)]
    - **描述：** 对所有的LED灯进行亮度的设置。
    - **参数：**
            + brightness:
                设置亮度的百分比
    #### 设置LED时钟阵列[peripherals.set_led(ordinal, data)]
    - **描述：** 选择需要显示的灯组进行设置。
    - **参数：**
            + ordinal:
                选择需要设置的LED时钟阵列上对应的灯组
            + data:
                每个灯组对应的显示内容
                每个灯组包含7个LED灯，一个灯组的点亮由一个字节(8bit)控制
                0 为点亮,1 为熄灭
                8bit中: 低7位控制数字的7个段
                例如:
                    0:0xA0,
                    1:0xF9,
                    2:0xC4,
                    3:0xD0,
                    4:0x99,
                    5:0x92,
                    6:0x82,
                    7:0xF8,
                    8:0x80, 
                    9:0x90
    #### 设置LED时钟阵列中的符号[peripherals.set_led_symbol(show)]
    - **描述：** 对LED时钟阵列中的冒号是否显示进行配置。
    - **参数：**
            + show:
                是否使能符号的显示
                True(显示) 或False(不显示)
    
- 展示APP
    - 展示的APP
        - 番茄钟
        - 日历
        - 天气
        - 股票
        - 虚拟货币
        - todoist
        - 电脑监控
        - Now Playing
        - Game Emulator
    - 方案
        - 通过图片展示 
        - 通过简单绘制各个app的界面进行展示
        - 绘制+图片的形式进行展示
            - 番茄钟 >>> 图片 > DONE
            - 日历 >>> 图片 > DONE
            - 天气 >>> 图片 > DONE
            - 股票 >>> 图片 > DONE
            - 虚拟货币 >>> 图片 > DONE
            - todoist >>> 图片 > DONE
            - 电脑监控 >>> 图片 > DONE
            - Now Playing >>> 图片 > DONE
            - Game Emulator >>> 图片



# 上周工作
    - D1 
        - 已知问题修复
        - 0.2.7版本发布
    - H5
        - 功能优化
        - 已知问题修复
        - Identify Device SN APP的开发
        - sensor错误引导的调整
        - 0.1.7版本发布
# 本周工作
    - D1
        - [1] 展示APP的开发
        - [1] RGB、LED时钟外设的API开放
        - [1] 已知问题修复
        - [1] 发布1.0.0版本
    - H5
        - [1] 已知问题修复
        - [1] 发布1.0.0版本
# 5月9日
- 查找APP
    - 进入APP：
        - 进入app等待扫描10S后，显示扫描到的列表
    - 在APP中：
        - sensor列表只显示信号值在-70以上的设备
        - 列表根据信号值大小排序
        - 列表每30s更新一次，显示最新扫描到的信号
    - 戳一下sensor后的表现:
        - 戳一下后，app弹出提示框
        - 提示内容包含:
            1. Name
            2. SN
            3. 设备是否绑定(与当前帐号下设备列表进行比对)
            4. 型号
            5. 信号值
            6. 电量

    - 显示周边扫描到的并且在HUB中存在描述文件的设备，对信号值也存在限制
    - 列表刷新规则，每5S更新一次列表
    - 显示的排序根据扫描到的信号值大小来排
    - 在戳一下设备后，设备列表中的该设备高亮显示，并聚焦至该设备，聚焦时间3s

3 205疑似新的密码错误组合码
1 3 205疑似新的错误码组合

# 5月10日
- 0.1.8版本更新内容
    - 优化项/新增项
        - sensor app历史数据界面时间始终为24小时制(jira-V3-526)
        - 优化历史数据界面切换速度
        - 新增seq用来记录ping的次数(jira-V3-528)
        - ping 失败后每 5min 执行一次ping(jira-V3-586)
        - 在H5自身探头连续读取到三次8500才认为探头异常
    - 修复项
        - 修复sw2异常显示离线的问题(jira-V3-525)
        - 修复断电后H5自身探头拔出上电后异常显示的问题(jira-V3-531)
        - 修改未扫描到的情况进入sensor详情页的内容(jira-V3-534)
    - UI及文案调整详见jira


# 上周工作
    - D1
        - 展示APP的开发
        - 已知问题修复
    - H5
        - 已知问题修复
        - 排查已知问题
        - 调整获取数据的方式，确保数据实时更新
        - 产测调整
        - 新增日历和天气app
        - 发布0.1.8版本
# 本周工作
    - D1
        - [1] 已知问题修复
        - [1] 发布1.0.0版本
        - [1] setup问题排查及修复
        - [2] 自带app调整
        - [2] 睡眠模式增加关闭和变暗选项
        - [3] RGB、LED时钟外设的API开放
    - H5
        - [1] 已知问题修复
        - [1] 发布1.0.0版本

# 5月14
    options = gcfg.get("OPTIONS", {})
    options["enable_prober"] = True
    options["enable_led_view"] = True
    options["sensor_assigned"] = "Temperature"
    options["display_sensor"] = utils.getDeviceSn()
    options["useCelsius"] = True
    gcfg.set("OPTIONS", options)

vobot:
    固件下载：https://dock-file.myvobot.com  
    ping action: https://dock-sync.myvobot.com 
    检查新固件：https://dock-update.myvobot.com  
    获取ntp时间: http://dock-pub.myvobot.com/time  
    访问API的缓存代理: https://apiproxy.myvobot.com  

mocreo-v3:
    Coap服务: coaps://coap.mocreo.com:5684
    上传ota进度链接: https://api.mocreo.com:443/v1/devices/upgrade
    其中访问API的缓存代理和检查新固件走的都是Coap服务地址
    mocreo的还漏了固件下载和获取ntp时间这两个接口

mocreo-v2:

# 5月10日
- 1.0.0版本更新内容
    - 优化项/新增项
        - 新增天气\日历app(jira-V3-613)
        - 修改setup中广播的数据格式,支持广播设备类型(jira-V3-672)
        - 调整数据获取方式,确保数据实时更新(jira-V3-612)
        - 调整Settings中Sensor Card位置(jira-V3-610)
        - Version 展示中版本可以点击检查更新(jira-V3-611)
        - 测量数据上报修改为发现设备符合上报规则就立即上报,而不是等待60s扫描结束后统一上报
        - 调整接口网址为mocreo.com
    - 修复项
        - 在调用上传接口前先判断网络连接是否正常
        - 修复sensor app华氏度显示异常的问题
        - 修复开机进入菜单页聚焦错误的问题
        - 修复进入sensor诊断时错误展示上一个Sensor名字的问题(jira-V3-618)
        - 修复开启延迟警报后异常警报的问题,在同步规则时更新数据时间戳,上报规则时更新上报时间戳(jira-V3-624)
        - 修复修改h5自身探头校准值不同步的问题(jira-V3-625)
        - 修复开机rule处于警报状态时,event为空导致的重复通知功能失效的问题
        - 修复在修改校准值后，sensor app显示距上次上报温度差值异常的问题(jira-V3-673)
    - UI及文案调整详见jira

Hub 离线 ：https://doc.mocreo.com/#/hub-offline?id=ho
Sensor 离线：https://doc.mocreo.com/#/sensor-offline?id=so
错误码：https://doc.mocreo.com/#/error-code?id=_2x00
如何部署Sensor：https://doc.mocreo.com/#/sensor-set-up?id=hsis
如何配置Sensor（添加Sensor）：https://doc.mocreo.com/#/sensor-set-up?id=hscs
H5探头断开引导：https://doc.mocreo.com/#/h5-probe?id=h5pm
常见Hub Setup失败错误：
    配置接收错误：https://doc.mocreo.com/#/setup-failed?id=cre
    无线网络不可用：https://doc.mocreo.com/#/setup-failed?id=wnu
    账号绑定失败：https://doc.mocreo.com/#/setup-failed?id=abf
    无法与服务器建立连接：https://doc.mocreo.com/#/setup-failed?id=utecws
    与 AP 连接失败(在没有错误码的情况)：https://doc.mocreo.com/#/setup-failed?id=ftcta


#5月16日
- 1.0.1版本更新内容
    - 优化项/新增项
        - factory固件使用宏定义进行项目的区分
        - 调整url链接地址
    - 修复项
        - 修复戳一下高亮异常的问题(jira-V3-678)
        - 修复探头断开/sensor离线异常展示的问题(jira-V3-679)
        - 修复setup完成后上传探头状态为0的问题(jira-V3-686)
        - 修复ota完成后不同步版本号的问题，开机强制调用同步一次Attribute(jira-V3-676)
        - 修复开箱设备开机后默认配置不生效的问题
    - UI及文案调整详见jira

# 5月17日
- 代码审查结果
    - 逗号后要注意加上空格
    - 开机时的加载页面把等待1s和等待网络连接结合
    - ui_home中，绘制界面的align变量名需要进行调整，使其可读性增强
    - 自定义蓝牙数据中要补上注释
    - ui_home中，data的


当前总使用 3363040
3323392
当前使用内存：3.17 MB
剩余内存:2.96 MB
#### 内置
1. 番茄钟（工作学习）(python 11 kB)
2. 天气（桌搭）(python 18.78 kB)
3. 日历（桌搭，有koc反馈长时间使用该app）(python 2.79 kB)
4. 电脑硬件监控（游戏，电脑爱好者）(python 9.12 kB)
5. todoist（日程安排）(python 9.03 kB)
#### 商城下载
1. 股票（特定用户）(python 7.67 kB)
2. 加密货币（特定用户）(python 4.42 kB)
3. 游戏模拟器（蓝牙模块难剥离？）(python 13.09 kB)
4. nowplaying（蓝牙模块难剥离？）(python 46.04 kB)
5. 屏幕扩展（配置复杂）(python 6.57 kB)
6. 电子相册\* (python 88.2 kB)

屏幕扩展（配置复杂）   3294944  27.78
游戏模拟器（蓝牙模块难剥离？） 3223696 97.35

H5-Lite v1.0.1 生产版本发布
版本号: [v1.0.1]
发布日期: [2024年5月17日]

新特性
新增天气、日历 app
新特性2: 简要描述新特性2的功能和用途。
新特性3: 简要描述新特性3的功能和用途。
改进
改进1: 描述对现有功能的改进和优化。
改进2: 描述对现有功能的改进和优化。
改进3: 描述对现有功能的改进和优化。
修复
修复1: 描述修复的错误或漏洞。
修复2: 描述修复的错误或漏洞。
修复3: 描述修复的错误或漏洞。
已知问题
问题1: 描述该版本中仍然存在的问题和限制。
问题2: 描述该版本中仍然存在的问题和限制。
问题3: 描述该版本中仍然存在的问题和限制。
升级注意事项
注意事项1: 提供升级到该版本时需要注意的事项或特别步骤。
注意事项2: 提供升级到该版本时需要注意的事项或特别步骤。
注意事项3: 提供升级到该版本时需要注意的事项或特别步骤。
兼容性信息
兼容性1: 说明与其他软件、硬件或系统的兼容性情况。
兼容性2: 说明与其他软件、硬件或系统的兼容性情况。
兼容性3: 说明与其他软件、硬件或系统的兼容性情况。


# 本周工作
    - D1
        - 已知问题修复
        - 压缩文件解压验证 > 进行中
        - setup问题排查及修复 > 进行中
    - H5
        - 已知问题/反馈问题修复
        - 测量数据上报规则更改
        - 修改setup中广播的数据格式,支持广播设备类型
        - 完善天气/日历app
        - 发布1.0.0/1.0.1版本
# 下周工作
    - D1
        - [1] 已知问题修复
        - [1] 发布1.0.0版本
        - [1] App 从应用市场下载验证
        - [1] setup问题排查及修复
        - [2] 自带app调整
        - [2] 睡眠模式增加关闭和变暗选项
        - [3] RGB、LED时钟外设的API开放
    - H5
        - [1] 已知问题修复
        - [1] 发布1.0.2版本 >> 待定


# 5月22日
chang'jian'bu'zhoH5-Lite  探头断开 / 异常状态 表现 以及解决方案
- 如果您的探头在插入设备后仍未被检测到。请尝试一下的解决方法。
    - 确认您的探头插入位置正确，探头接口位于设备背部，并带有"PR0BE"的标识
    - 您可以尝试用湿纸巾擦拭探头接口后再用干纸巾擦拭（消除静电），并再次插入设备，观察其是否恢复。
    如果您在尝试以上操作后，仍然无法使H5外置测温探头状态恢复正常，请联系我们。

常见Hub Setup失败错误：
    配置接收错误：https://doc.mocreo.com/#/setup-failed?id=cre
    无线网络不可用：https://doc.mocreo.com/#/setup-failed?id=wnu
    账号绑定失败：https://doc.mocreo.com/#/setup-failed?id=abf
    无法与服务器建立连接：https://doc.mocreo.com/#/setup-failed?id=utecws
    与 AP 连接失败(在没有错误码的情况)：https://doc.mocreo.com/#/setup-failed?id=ftcta
H5-Lite Setup 失败常见步骤（App提示步骤）对应的H5-Lite LED 显示屏 显示的步骤，以及对应步骤失败的解决方案
### Step 1: Connect the device

### Step 2: Synchronize the device information

### Step 3: Retrieve the AP (Access Point) list

### Step 4: Synchronize the device settings

### Step 5: Connect to the network

### Step 6: Bind the account

# 配置接收错误: 会发生在整个setup流程中
- 请检查蓝牙是否被异常关闭。
- 请重新尝试setup
- 如果上述操作仍未能够正常连接，请联系我们。

# 无线网络不可用: 发生在步骤5,连接网络中
- 确认设备电源已正常连接
- 如果上述操作仍未能够正常连接，请联系我们。

# 账号绑定失败: 发生在步骤6
- Wi-Fi 已连接，但无法连接到互联网或我们的服务器
    - 防火墙对端口号的限制，检查路由器是否有阻止123、80、443、5684端口的防火墙策略。获取路由器IP地址>>进入路由器浏览器设置页面>>在高级设置中检查端口限制。
- 该设备尚未被记录，请联系我们

# 无法与服务器建立连接: 发生在步骤6
- Wi-Fi 已连接，但无法连接到互联网或我们的服务器
    - 防火墙对端口号的限制，检查路由器是否有阻止123、80、443、5684端口的防火墙策略。获取路由器IP地址>>进入路由器浏览器设置页面>>在高级设置中检查端口限制。
- 该设备尚未被记录，请联系我们

# 与 AP 连接失败(在没有错误码的情况): 发生在步骤5,连接网络中
- Wi-Fi 密码错误
    - 修改密码，验证密码正确性，重新配对Hub。
- 网络状态受到影响且不稳定。
    - 保证网络状态良好，不影响网络状态，如（附近的冰箱、微波炉、无绳电话等）。
- 路由器已设置了固定连接设备数量，无法添加新设备。
    - 更改允许连接的设备数量，增加连接数量，然后重新配对集线器。


### 步骤 1：连接设备

### 步骤 2：同步设备信息

### 步骤 3：检索 AP（接入点）列表

### 步骤 4：同步设备设置

### 步骤 5：连接网络

### 步骤 6：绑定账号


# 上周工作
    - D1
        - 已知问题修复
        - 睡眠模式增加关闭和变暗选项
        - setup问题排查及修复
        - 自带app调整
    - H5
        - 已知问题/反馈问题修复
        - MS1 型号支持
        - 发布1.0.2版本
# 本周工作
    - D1
        - [1] 已知问题修复
        - [1] 发布1.0.0版本
        - [2] App 从应用市场下载验证
    - H5
        - [1] 已知问题修复
        - [2] 发布1.0.3版本

- v1.0.0 版本更新内容
    - 优化项/新增项
        - Loading...界面修改为小尺寸的图标
        - 在setup Error页新增”重试”按钮,在按下重试之前关闭设备自身热点(D1-372)
        - 睡眠模式增加显示模式的选择，在番茄钟和游戏app中正在使用时不会触发睡眠(D1-378)
        - setup web界面新增刷新按钮(D1-385)
        - 新增LED/LCD对外开放的Api(D1-375/D1-376)
        - 将todoist和screen mirroring两个app移除
        - 将experimental的默认值修改为False
    - 修复项
        - 修复在网络请求异常时退避的bug
        - 修复在断网的情况下启动切换默认app失效的问题(D1-379)
        - 进入或退出setup时,停止等待Wi-Fi连接的过程,避免有多个等待Wi-Fi连接的过程导致setup异常(D1-384)
        - 在setup中连接上网络后不做扫描的操作(D1-384)
        - 修复在连接某些Wi-Fi时，能够正常连接但还是会产生的错误码导致的误报的问题(D1-384)
    - UI及文案调整详见jira

    2dddee30

# 上周工作
    - D1
        - 已知问题修复
        - 发布1.0.0版本
        - 新增应用市场下载app功能 >>> 进行中
        - 编译一版特殊固件用于展会
    - H5
        - 已知问题修复
    - H1
        - 调整测试模板
        - 重新编译和发布1.9.9版本
    - H1B
        - 排查用户MQTT连接失败的问题
        - 编译一版特殊固件用于尝试修复用户MQTT连接失败的问题
# 本周工作
    - D1
        - [1] 已知问题修复
        - [1] 发布1.0.1版本(待定) 
        - [2] 新增应用市场下载app功能 
    - H5
        - [1] 已知问题修复
        - [2] 发布1.0.3版本

def signal_ui(parent, signal):
    if parent.get_child_cnt() > 1:
        parent.get_child(1).del_async()
    step_list = lv.obj(parent)
    step_list.set_size(33, 40)
    step_list.align(lv.ALIGN.RIGHT_MID, 0, -10)
    step_list.set_style_radius(0, 0)
    step_list.set_style_pad_all(0, 0)
    step_list.set_style_border_width(0, 0)
    step_list.set_style_bg_color(lv.color_hex3(0x000), 0)
    step_list.set_style_bg_opa(lv.OPA._0, 0)

    style_line = lv.style_t()
    style_line.init()
    style_line.set_line_width(4)
    for index in range(5):
        if index < signal:
            line_points = [{"x": index * 6 + 6, "y": 20 - 5 * index}, {"x": index * 6 + 6, "y": 25}]
        else:
            line_points = [{"x": index * 6 + 6, "y": 23}, {"x": index * 6 + 6, "y": 25}]
        line = lv.line(step_list)
        line.set_points(line_points, len(line_points))  # Set the points
        line.add_style(style_line, 0)
        line.set_style_line_color(lv.color_hex3(0xFFF), lv.PART.MAIN)



# 当前分组详情
- H1B
    - VSN1-PRD-V3  >>> H1B-V3的正式生产分组
    - VSN1-PRD-CHANGE-UPDATA >>> H1B-V3的更改上传数据URL的分组
    - SSMP_REBOOT_VSN1-PRD-V3-TEMP >>> 新的IDF环境下连不上网络自动重启的分组(目的是减轻hub掉线的问题)
    - VSN1-PRD >>> H1B的正式生产分组
    - VSN1-PRD-TEMP >>> 使用VSN1-PRD 的原始下载链接，解决部分固件升级失败的问题 》》》已删除
    - VSN1-PRD-V3-TEMP >>> 在1.9.6的基础上ST10的广播原始数据
        - B0A732204568
        - E05A1BCC450C
        - 64B708C7B1E8
        - B0B21CB09348
    - VSN1-DEV-V3 >>> H1B-v3的测试分组
    - VSN1-DEV >>> H1B的测试分组
    - VSN1-FACTORY-V3 >>> 产测固件请求分组(虚拟) >>> 更新至1.9.8
    - VSN1-PRD-V1-TEMP - 1个设备
        - D4D4DAFAAB68
    - VSN1-PRD-V3-oo8080 - 8个设备 
        - 083A8D901604
        - 90380C6291F0
        - 94E6868F0484
        - 244CAB010624
        - 90380C6105AC
        - 94E6868F051C
        - 441793E7364C
        - 90380C61FDE4
        - 90380C629558
- H1
    - SS-PRD-V3-CHANGE-TEST >>> 修改测试模板的分组
    - SS-PRD-V3-SOPS-0409 >>> 关闭ntp服务的分组
        - E465B8D83510
    - SSMP_SS-PRD-V3-TEMP >>> 新的IDF环境下连不上网络自动重启的分组(目的是减轻hub掉线的问题)
    - SS-PRD-V3 >>> H1-V3的生产分组
    - SS-DEV-V3 >>> H1-V3的测试分组
    - SS-PRD-V1.9.7 >>> 给display BK V1版本的用户使用
        - B48A0A943200
        - B0B21C38F068
        - 34987A822E78
        - E05A1B43F700
    - SS-PRD >>> H1的生产分组
    - SS-DEV >>> H1的测试分组
    - SS-PRD-V1-TEMP - 11个设备
        BCDDC2D39DA0
        F008D166B094
        BCDDC2D39520
        7C9EBD298234
        240AC4CBBAF8
        246F2853C2C0
        240AC4CB787C
        A8032A58AC88
        A8032A58ABCC
        FCF5C43AEFDC
        B0B21C38FAE8

- D1
    - DOCK_HUB_DEV >>> 内部人员使用分组
    - DOCK_HUB_TEMP >>> 展会使用分组
    - DOCK_HUB_DEV_TEMP >>> 开发和测试使用分组
    - DOCK_HUB_PRD >>> 正式生产分组
    - DOCK_HUB_DEV_OTA_TEST >>> OTA测试分组
- H5
    - H5-Lite-PRD >>> 正式分组
    - H5-Lite-DEV-TEMP >>> 开发和测试使用分组
    - H5-Lite-DEV >>> 内部人员使用分组
- NS1
    - NS1-DEV >>> 测试分组
    - NS1-PRD >>> 生产分组

- v1.0.1 版本更新内容
    - 优化项/新增项
        - 在app settings中锁屏的开关做分级处理(D1-399)
        - 公开库代码调整(重点)
        - 将交互方式分为光标模式和内容模式，光标模式聚焦于单个选项，内容模式聚焦于整个界面(重点)
        - crypto、stock逐个查询改为批量查询
        - 亮度配置项调整
    - 修复项
        - 修复在打开或关闭实验性应用开关后,settings中的数据不实时更新的问题(D1-400)
        - 修复在打开或关闭实验性应用开关后,app列表有时会聚焦异常的问题(D1-395)
    - UI及文案调整详见jira

# 上周工作
    - D1
        - 已知问题修复
        - 发布1.0.1版本
        - 新增应用市场下载app功能 >>> 进行中
    - H5
        - 已知问题修复
    - 对当前项目所用到的分组进行分类和调整，删除一些不需要的分组
# 本周工作
    - D1
        - [1] 已知问题修复
        - [1] 发布1.0.2版本
        - [2] 新增应用市场下载app功能 
    - H5
        - [1] 已知问题修复
        - [2] 发布1.0.3版本

- v1.0.2 版本更新内容
    - 优化项/新增项
        - 字体调整
        - screen_mirroring 移回内置app(D1-401)
        - 支持另一款Gamepad: ShanWan 'Q36 for Android'
        - 调整Setup模式中url path的处理逻辑
    - 修复项
        - 修复MAC/IOS设备连接热点后没有弹窗的问题(D1-403)
        - 修复退出setup后, 交互方式异常的问题(D1-402)
    - UI及文案调整详见jira

- H5 v1.0.3 版本更新内容
    - 优化项/新增项
        - 支持MS1
        - 上报/trigger事件前,请求体更新为当前的实时数据(V3-701)
        - 新增在setup过程中获取不到IP的触发条件
        - 增加对开机连接某些Wi-Fi异常产生错误码的过滤(V3-205)
        - 在扫描到数据后立即进行规则判断,在触发了规则之后强制上报一次测量数据(V3-702)(V3-705)
        - 在app中删除hub后，如果在sensor app中，hub直接提示帐号未绑定(V3-685)
        - 在时区变更后，调用接口强制PING一次，同步时区(V3-752)
        - 在部分app中将交互方式切换为光标模式,在通知中将交互方式切换为内容模式
        - sensor app 中sensor根据资产中的顺序来进行排序
        - 上报温度范围调整(V3-754)
    - 修复项
        - 修复LED展示湿度异常的问题(V3-758)(V3-764)
        - 修复sensor app中的异常报错问题(V3-684)
        - 修复sensor app卡片数据不显示的问题(V3-757)
        - 历史数据界面显示湿度时不显示不在范围内的数据(V3-756)
        - 修复发送Coap请求时,概率导致后续请求一直失败[-2]的问题(V3-753)
    - UI及文案调整详见jira


### 二、 指示灯显示样式
|            led modes             |     mode      |    layer     |                  remarks                   |
| :------------------------------: | :-----------: | :----------: | :----------------------------------------: |
|             未知状态             |    UNKNOWN    |   DEFAULT    |           蓝色闪烁，间隔时间500            |
|            开机启动中            |     BOOT      |   DEFAULT    |         紫色快速闪烁，间隔时间200          |
|             正常工作             |    NORMAL     |   DEFAULT    |          紫色较慢呼吸，间隔时间80          |
|             网络断开             |   NET_FAIL    | APPLICATION  |          红色快速呼吸，间隔时间10          |
- 网络断开后亮红灯
|        无法登录api服务器         |   ERROR_API   | APPLICATION  |          红色慢速呼吸，间隔时间80          |
- 设备访问密钥无效/数据上传接口调用失败/relay_device上报失败/
|        无法登录MQTT服务器        |   ERROR_RPC   | APPLICATION  |         红色慢速闪烁，间隔时间800          |
|      日历解析出现了无效数据      | INVAILD_DATA  | APPLICATION  | 红色快速呼吸（持续时间3000ms），间隔时间10 |
|     传感器被触发，数据上传中     |   TRIGGERED   | NOTIFICATION | 紫色快速闪烁（持续时间500ms），闪烁间隔200 |
|              升级中              |    UPDATE     | NOTIFICATION |           蓝红交替，间隔时间200            |
|           进入pair模式           |  PERMIT_JOIN  | NOTIFICATION |           蓝紫渐变，间隔时间200            |
|           进入配网模式           |  SETUP_WIFI   | NOTIFICATION |          蓝色快速呼吸，间隔时间10          |
|             配网成功             | SETUP_SUCCESS | NOTIFICATION |          蓝色闪烁3秒，间隔时间800          |
|             配网失败             |  SETUP_FAIL   | NOTIFICATION |        红色慢速闪烁3秒，间隔时间800        |
- OTA失败
|             开始重置             |   RECOVERY    | NOTIFICATION |        红色快速闪烁3秒，间隔时间200        |
|            不可用状态            |     FATAL     | NOTIFICATION |                  红色常亮                  |
|           进入入网模式           |  CONNECTING   | NOTIFICATION |          紫色快速呼吸，间隔时间10          |
| 网络连接成功 或 eink画面更新模式 |   CONNECTED   | NOTIFICATION |          蓝色慢速呼吸，间隔时间80          |

# 上周工作
    - D1
        - [1] 已知问题修复
        - [1] 发布1.0.2版本
        - [2] 新增应用市场下载app功能 >>> 基本完成
    - H5
        - [1] 已知问题修复
        - [2] 发布1.0.3版本
# 本周工作
    - D1
        - [2] 已知问题修复
    - H5
        - [2] 已知问题修复
    -HUB
        - [1] 已知问题修复和功能新增
            - Setup 过程中，在某一步停留时间超过5min，将自动退出setup模式
            - 在SETUP过程中，完成WIFI连接后以及调用一次PING
            - 在汇报测量数据时，加上接口调用失败时自动切域名重试的机制
            - MQTT端口新增备用URL
            - 在上传WIFI列表时也将加密方式一起上传
            - 修复数据打包存储的情况，数据长度会被修改的问题
        - [1] 发布2.0.0版本

html代码里面不要直接绑定IP地址，post到相对路径就行了，这方面需要学习一下html的原理。

通过 mpy-cross __init__.py  这个命令，可以得到：__init__.mpy 
把这些mpy文件，打zip包上传到App库，下载后解压缩到/apps/xxx 文件夹里面，是可以直接运行的，这个我验证过了
./mpy-cross ../

# 上周工作
    - D1
        - 产测模式新增老化测试功能
        - 将BOOTLOADER_RESET配置的PIN口修改为39(编码器按键)
        - 发布V1.0.3/1.0.4版本固件
    - HUB
        - 已知问题修复和功能新增
            - 修复V1版本芯片在最新环境下无法正常编译的问题
            - Setup 过程中，在某一步停留时间超过5min，将自动退出setup模式
            - 在SETUP过程中，完成WIFI连接后以及调用一次PING
            - 在汇报测量数据时，加上接口调用失败时自动切域名重试的机制
            - MQTT端口新增备用URL
            - 在上传WIFI列表时也将加密方式一起上传
            - 新增对MS1/MS2的支持
            - 对relay_device上报周边设备数量进行限制
    - 排查ESP32芯片连接不上OZ这个WiFi的问题
# 本周工作
    - D1
        - [2] 已知问题修复
    - H5
        - [2] 已知问题修复
        - [1] 新增对ST9、ST10的支持
        - [2] 发布v1.0.4版本
    - HUB
        - [1] H1B
            - 对遗留反馈问题进行复现及修复
            - 发布2.0.0版本
        - [2] H1
            - 修复已知问题
            - 新增DISPLAY重置指令
            - 新增DISPLAY wifi配置信息的发送
            - 优化DISPLAY SETUP HUB端逻辑
            - 发布2.0.0版本
    - 熟悉并编译共享打印机项目

- H5-Lite 上传masureID时的逻辑，在SW2触发警报的同时也会上报一次数据，需要理清除其中的逻辑

- H1B v2.0.0 版本更新内容
    - 优化项/新增项
        - 更新编译环境至esp-idf v4.4.7
        - 在上传nodeId时,过滤掉空的id(V3-835)
        - 在znp初始化重试成功后将panid同步至服务器(V3-834)
        - 在MQTT连接失败后,自动切换mqtt_aws的地址重新进行连接(V3-844)
        - 在开机15min后仍连接不上网络则进行重启操作(V3-846)
        - 在数据上报失败时，不会触发维护性重启机制，避免短时间内频繁上报数据失败导致频繁重启(V3-840)
        - 在setup中未进行操作5min后会自动退出setup模式(V3-845)
        - 调整数据上报和relay_device接口指示灯显示逻辑(V3-894)
        - 在setup中连接上wifi后立即调一次ping,用于获取relog指令(V3-847)
        - 新增对MS1/MS2的支持(V3-865)
        - 限制delay_device上报的设备数量为信号最好的100个(V3-896)
        - 在数据校验时,不再对数据的范围做限制,超出范围的数据也会上传(V3-839)
        - 在上传BLE数据失败后,尝试切换目标地址重新上传(V3-842)
        - 在同步警报规则时根据规则的结果上报events事件(V3-836)
    - 修复项
        - 修改ss1设备信息,确保hub_portal中的内容显示正确(V3-838)
        - 修复在只使用以太网setup后,连不上以太网时,hub不亮红灯的问题(V3-837)
        - 修复在SETUP成功后，有时会异常亮红灯的问题(V3-833)
        - 修复hub由于芯片地址错误导致以太网初始化失败的问题
    - portal页文案调整详见jira


# 上周工作
    - HUB
        - H1B
            - 排查events接口重复上报相同警报的问题
            - 修复已知问题
            - 发布v2.0.0版本
        - H1
            - portal界面文案和UI调整
            - 修复给display刷新logo时异常的问题
            - Template Setup支持BLE Only 模式
    - H5
        - 新增对ST9/ST10的支持
        - 修复已知问题
        - 发布v1.0.4版本
# 本周工作
    - D1
        - [1] Hot Desking 平台整合前期验证
        - [2] 轮播模式实现
        - [2] app菜单显示选择功能实现
        - [2] settings 密码功能实现
        - [2] 已知问题修复
    - H5
        - [3] 已知问题修复
    - HUB
        - [1] H1B
            - 重新发布2.0.0版本
        - [1] H1
            - 修复已知问题
            - 发布2.0.0版本

# hot_desking需求分析
- 具体的实现方式如下，
  1. 在 Mini Dock 内置一个 Hot Desking 配置页面
  1. 允许用户选择支持的预订系统（如 Nexudus 或 Robin）
  2. 输入令牌或登录凭证，调用 API 进行身份验证
  3. 通过 API 获取到会议室和办公桌列表并展示，并允许用户进行选择
  4. 在 Mini Dock 运行 Hot Desking App 时，自动从集成的预订系统中获取当前的事件状态。

- Nexudus系统功能实现具体流程
    1. 用户在portal中填入refresh_token或账户密码获取access_token(每15天重新获取一次access_token)
    2. 获取当前帐号下的所有Desk(Hot Desk包含Hot Desk和Dedicated Desk)显示在portal中
    3. 用户选择对应的desk
    4. 进入app时
        - 获取Nexudus系统中设置的时区(使用的是本地的时区还是系统的时区?)
        - 获取当前desk中对应的合同ID和合同开始时间
        - 获取当前desk中对应资源的预定ID和预定开始时间(预定的时间和合同的时间并不会冲突)
    5. 获取与当前时间相邻的两个合同或预定的内容
    6. 显示当前时间desk所处的状态
        - desk包含的状态
            - 空闲
            - 已被预定
            - 正在使用中
            - 即将到期
            - 已过期
            - 暂时不可用
        - UI中显示的内容
            - 办公室名称
            - 办公桌名称
            - 可用/不可用时间
            - 使用人名称
    7. 当一个合同或预定结束后，继续获取下一个合同或预定的内容
    8. 在显示期间，每15mins获取一次当前desk中对应的合同或预定ID。

- 问题
    1. 在客户想要使用hot desk时，会选择哪种方式进行确认，是以合同的方式还是预定的方式？
        - 两个都会可能使用到，合同的方式适用于以天为单位的长期预定，预定的方式适用于短期以分钟为单位的预定。

# Mini Dock Hot Desk App 功能概述
- Mini Dock Hot Desk App 旨在将 Nexudus Desk 的预订事件与当前 Desk 的状态展示在 Mini Dock 上。支持的状态包括：
  + 空闲 / 已被预定 / 正在使用 / 即将到期 / 暂时不可用

# 实现方式
1. 用户在 Mini Dock App 设置中输入 Nexudus 管理员账号和密码。
2. Mini Dock 调用 API 获取所有的 floorPlans 和 Desk 信息。用户选择一个 Desk 并与设备进行绑定，完成设置。
3. 进入 Hot Desk App 时，设备通过 GET /api/spaces/bookings 获取该 Desk 下的当前预订事件列表，并最终处理和展示在屏幕上。


# 需要向 Nexudus 确认的内容
1. 目前我们仅获取了 Desk 的预订信息进行展示。但我们发现有些 Desk 具备合同。这些 Desk 的合同信息是否需要展示在 Mini Dock 的屏幕上？
2. 我们注意到 Desk Type 中包含 Dedicated desk 和 Hot-desk 等选项。Mini Dock 是否需要支持所有类型的 Desk？


# 上周工作
    - HUB
        - 排查和修复已知问题
        - 修复在event事件过多时，接口timeout导致重复上报的问题
    - D1
        - hot desking app 实现方案的确认
        - hot desking app的开发
        
# 本周工作
    - D1
        - [1] Hot Desking 平台整合前期验证
            - [1] 剩余逻辑的补充
        - [1] v1.0.5版本发布
            - APP管理界面的实现
            - 移回todoist app
            - 其他已知问题的修复
        - [3] 轮播模式实现
        - [3] app菜单显示选择功能实现
        - [3] settings 密码功能实现
    - HUB
        - [2] H1B
            - 修复2.0.0版本测试反馈问题
            - 排查和修复event事件异常不上报问题
            - 发布2.0.1版本
        - [2] H1
            - 排查和修复ble连接异常导致的设备重启问题
            - 发布2.0.0版本

syncsign.nexudus
thomas@oazon.com
aA12345678@

nexudus
scott@sync-sign.com
s-3N4tG_p

# v1.0.5版本更新内容
    - 优化项/新增项
        - 将todoist移回内置app(D1-414)
        - 将温度控制配置整合至单位中,使用英制和公制进行区分(D1-416)
        - 调整部分app获取数据的间隔时间(D1-418)
        - 新增app 管理界面(D1-392)
    - 修复项
        - 修复在睡眠模式中触发弹窗后，无法唤醒的问题
        - 调整ui初始化步骤,避免在开机加载页面时不能够正常连接Wi-Fi
        - 修复只有一个app时菜单页失效的问题
        - 调整setup接收wifi配置后的处理流程,取消对%的特殊处理(D1-417)
        - 修复Now Playing 手机蓝牙连接后页面未跳转，退出后卡在退出页的问题(D1-408)
    - UI文案调整详见jira


# 上周工作
    - D1
        - Hot Desking 平台整合前期验证及DEMO开发
        - v1.0.5版本发布
            - APP管理界面的实现
            - 移回todoist app
            - 其他已知问题的修复
    - 排查博德越共享打印机项目连接不上网络的问题
        
# 本周工作
    - D1
        - [2] 重发v1.0.5
        - [3] 轮播模式实现
        - [3] app菜单显示选择功能实现
        - [3] settings 密码功能实现
    - HUB
        - [1] H1B
            - 修复2.0.0版本测试反馈问题
            - 排查和修复event事件异常不上报问题
            - 发布2.0.1版本
        - [2] H1
            - 排查和修复ble连接异常导致的设备重启问题
            - 发布2.0.0版本

# D1 v1.0.5-2版本更新内容
    - 优化项/新增项
        - stocks新增对股票货币的识别(D1-419)
    - 修复项
        - 修复只有一个app时,菜单界面显示异常的问题(D1-421)
        - 修复在web protal 页面配置含有特殊符号的天气地址时页面没有任何错误弹框提示的问题(D1-429)
        - 修复股票在查询到的收盘价为0的情况导致卡死的问题(D1-428)
        - 修复app Managment 功能输入超过长度的app id 页面没有提示的问题(D1-427)
        - 修复在设备退出application settings页后，在浏览器上输入app id，点击下载和安装页面无相应的问题(D1-426)
        - 修复剩余闪存提示出现负数的问题(D1-431)

# factory固件 v1.1.0版本更新内容
    - 优化项/新增项
        - 重构代码结构
        - 新增GTS Root R4证书
        - 下载固件或上报下载进度时，增加timeout机制
        - 新增版本号

# D1 v1.0.5-3版本更新内容
    - 修复项
        - 修复my_device中Storage会出现超过100%的情况(D1-431)
        - 修复在连接SSID中包含有引号的WIFI时web界面报错的问题

# factory固件 v1.1.1版本更新内容
    - 优化项/新增项
        - 重构代码结构
        - 新增多个常用SSL证书，用BUNDLE方式而不是直接指定证书
        - 配置调整缩减固件尺寸
    - 修复项
        -将要显示在屏幕上字符中的非ASCII字符替换成*


# 上周工作
    - D1
        - v1.0.5版本的重新发布
            - factory固件问题排查及修复
            - stock app支持多货币显示
            - 其他反馈问题的修复
    - HUB
        - [1] H1B
            - 证书新增
            - 排查和修复在触发events/dismiss事件后，Hub未及时上报的问题
            - 数据上报接口逻辑优化
            - 修复2.0.0版本测试反馈问题
    - H5
        - 编译一版特殊固件用作于led灯的比对测试
# 本周工作
    - D1
        - [1] 应用市场app开发
        - [3] 轮播模式实现
        - [3] app菜单显示选择功能实现
        - [3] settings 密码功能实现
    - HUB
        - [1] H1B
            - 发布2.0.0版本 >>> 待服务端确认后发布
        - [2] H1
            - 排查和修复ble连接异常导致的设备重启问题
            - 发布2.0.0版本


@韦常源(Thomas-韦常源)   许多新闻机构都提供 RSS (Really Simple Syndication) feeds，方便用户订阅和获取最新的新闻更新。

我们可以使用一些现有的库来解析这些 RSS feeds 并展示内容。以下是一些主要新闻机构及其 RSS feed 链接：

- BBC: http://feeds.bbci.co.uk/news/rss.xml
- CNN(美国有线电视新闻网): http://rss.cnn.com/rss/cnn_topstories.rss
- Fox News(福克斯新闻): http://moxie.foxnews.com/google-publisher/latest.xml
- The Wall Street Journal(华尔街日报): http://www.wsj.com/xml/rss/3_7085.xml

- [1] 货币汇率
- [1] Kickstarter 众筹金额
    - 输入创建者、项目、项目名
    - 输出无单位金额、支持者
- [1] Indiegogo 众筹金额
    - 输入ID
- [1] Discord 社区成员数量
    - 输入ID和KEY
    - 输出数量
- [1] YouTube 粉丝计数器
    - API密钥+ID


- [1] 距离圣诞节还有几天
- [1] 键盘自动按下
    - 按下空格
- [1] 倒计时

- [1] TeslaMate App
- [2] Top 10 news headlines from BBC News
- [2] Instagram 粉丝计数器
- [2] YouTube 视频观看次数计数器
- [2] X 粉丝计数器
- [2] 显示二维码
- [2] 相册功能（定时循环在屏幕上显示客户自定义的图片/照片合集）


- H1B v2.0.0-2 版本更新内容
    - 优化项/新增项
        - 新增GTS Root R4证书
        - 修复在初始化pan网络失败后等待时间过长的问题(V3-1006)
        - 限制 events 事件上报的警报数量(V3-991)
        - 优化了请求接口切换的逻辑(V3-1007)
        - 在发生event和dismiss事件后立即上报(V3-1002)(V3-1003)(V3-1018)
        - 在触发sta事件时,将相同id的事件进行合并,符合/nodes的接口上传规范(V3-1066)
    - 修复项
        - 过滤掉重复的event事件(V3-1001)
        - 修复在delay_alarm状态下不可以dismiss的问题

- H1 v2.0.0 版本更新内容
    - 优化项/新增项
        - 新增GTS Root R4证书
        - 在刷新存在url图片的模板时，先将WIFI配置信息发送至display(V3-915)
        - Hub Portal Template Setup 模块支持 D75C-LEWI BLE Only 模式(V3-902)
        - hub向display发送wifi信息/hub portal可以支持用户手工给display更新wifi信息(V3-943)
        - hub portal可以支持用户手工给display发送重置命令(V3-944)
    - 修复项
        - 修复Hub JOSN 没有 PANid 问题(V3-914)
        - 修复给单个 Hub 发送 logo 指令后，不会触发生效的问题(V3-927)
    - 文案调整详见jira
