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

