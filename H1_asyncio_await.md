# H1项目异步任务等待
## ntp.isTimeValid()
### 配置
+ `network_ntp.py`:获取当前时间并返回判断时间是否正确的调用，isTimeValid()。
### 调用
+ `http_check_action.py`--283(循环): https的访问需要本机处在正确的时间,需要对当前时间进行判断,在主函数中通过`self.startCheckAction()`调用
+ `pan_schedule.py`--206(循环): 先等系统有了正确的时间，再来判断日程安排,在主函数中通过`await self.startPAN()`调用
+ `pan_transmit.py`--579(循环): 先等系统有了正确的时间，再来启动NETWORK，否则 db_pan_nodes.load() 没有正确的时间可判断.,在主函数中通过`await self.startPAN()`调用
+ `blemgr/__init__.py`--105(判断): ble设备扫描,在主函数中通过`await self.startBleApp()`调用
+ `data_mgr.py`--324(循环): 数据上传前判断时间,在主函数中通过`self.startFactoryAppMgr()`调用
+ `base_rule.py`--8(判断): 获取时间戳,在主函数中通过`await self.startBleApp()`调用

## s.device_access_key
### 配置
+ `device_hub.py`--76: 获取设备访问令牌。在`self.startIotDevice()`调用
### 调用
+ `device_hub.py`--122(判断): 在`self.startIotDevice()`调用
+ `http_api_request.py`--279(判断): 新增NODE,在`await self.startPAN()`中调用
+ `rpc_notification_worker.py`--257(循环): 先确保可以拿到access key，相当于激活,在`self.startWebServer()`中调用。
+ `online_mgr.py`--139(判断): 报告周围节点前确保已经获取到access key；
--195(循环): 等待获取到access key后输出距上次报告的时间。在`await self.startBleApp()`中调用。
+ `http_upload.py`--93(循环): 等待获取到access key后查询传感器状态，在`await self.startBleApp()`中调用。
