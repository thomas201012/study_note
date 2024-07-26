# 自定义code码（0-65534）0xffff
|  XX  |   X   | XX |  
|异常类型|特定模块|错误码|  
例如：
- 2101---代表了Wi-Fi功能在setup模块中产生了01的异常
- 2001---代表了Wi-Fi功能产生了01的异常
## 特定模块
```
特定模块决定了异常的发生位置以及异常信息提示的方式
```
- [0]全局功能
- [1]setup模块
- [2]故障检测模块
## 异常类型
- X由发生异常的位置决定
### 系统异常[00]（0X00-0X99）
### BLE[01]（1X00-1X99）
### Wi-Fi[02]（2X00-2X99）
#### (2X00)
```
- 错误内容
    - 未知的内容
- 触发条件
    - 除开已知的错误外，其他网络情况的错误都使用该错误码
- 提示内容
    - "Network issue detected"
- 引导内容
    "1.Please check your network settings"
    "2.Restart the devices and the router."
```
#### (2X01)
```
- 错误内容
    1. 添加不存在的Wi-Fi
    2. 连接了禁用SSID的网络
- 触发条件
    - 错误码触发：(5 201)
- 提示内容
    "Unable to find Wi-Fi",
- 引导内容
    "1.Re-enter the Wi-Fi name."
    "2.Weak Wi-Fi signal strength."
    "3.Check if Wi-Fi has been disabled."
```
#### (2X02)
```
- 错误内容
    - 密码错误
- 触发条件
    - 错误码触发：
        1. （5  15）（5  205）
        2. （5  202）（5  205）
- 提示内容
    "The password is incorrect."
- 引导内容
    "1.Re-enter the correct password."
    "2.Verify that the Wi-Fi name is correct."
    "3.Restart the devices and the router."
```
#### (2X03)
```
- 错误内容
    - 企业级模式下，用户名或密码错误
- 触发条件
    - 错误码触发：（5 1）（5 205）
- 提示内容
    "Invalid username or password.",
- 引导内容
    "1.Enter correct credentials."
    "2.Verify enterprise network settings."
    "3.Restart the devices and the router."
```
#### (2X04)
```
- 错误内容
    - Wi-Fi连接数量已达上限
- 触发条件
    - 错误码触发：(5 5) (5 205)
- 提示内容
    "Wi-Fi connections limit reached."
- 引导内容
    "1.Attempt reconnection."
    "2.Remove excess devices from Wi-Fi."
    "3.Verify router configuration."

```
#### (2X05)
```
- 错误内容
    - 认证服务器认证超时
- 触发条件
    - 错误码触发：(5 204) (5 205)
- 提示内容
    "Authentication server timeout."
- 引导内容
    "1.Check network connectivity."
    "2.Verify authentication credentials."
    "3.Verify authentication server status."
```
#### (2X06)
```
- 错误内容
    - AP断开连接
    - 信号较差
- 触发条件
    - 错误码触发：
        1.(21) (5 200) (5 201)
        2.(21) (5 3) (5 205) (5 201)
- 提示内容
    "Access point (AP) disconnected."
- 引导内容
    "1.Check router status."
    "2.Verify Wi-Fi signal strength."
    "3.Ensure network connectivity."
    "4.Review router settings."
    "5.Restart devices."
```
#### (2X07)
```
- 错误内容
    - 
- 触发条件
    - 错误码触发：

- 提示内容
    - [2X07]"错误提示","错误引导",
```

#### (2X08)
```
- 错误内容
    - Wi-Fi名称错误
- 触发条件
    - 日志错误触发：NETW:"OSError：Wifi SSID Incalid"
- 提示内容
    "Invalid Wi-Fi name."
- 引导内容
    "1.Verify if the Wi-Fi name is correct."
```
#### (2X09)
```
- 错误内容
    - 企业级模式下，用户名或密码错误
- 触发条件
    - 日志错误触发："RuntimeError: Wifi UnKnown Error 0x0102"
- 提示内容
    "Invalid username or password."
- 引导内容
    "1.Enter correct credentials."
    "2.Verify enterprise network settings."
    "3.Restart the devices and the router."
```
#### (2X10)
```
- 错误内容
    - 无法获取到IP地址
- 触发条件
    - 程序逻辑触发：wifi连接超时
- 提示内容
    "Unable to obtain IP address."
- 引导内容
    "1.Check network connection."
    "2.Verify DHCP settings."
    "3.Verify IP address configuration."
    "4.Review router settings."
    "5.Restart devices."
```
#### (2X11)
```
- 错误内容
    - DNS地址无效
- 触发条件
    - 日志错误触发："OSError: -202"
- 提示内容
    " Invalid DNS address."
- 引导内容
    "1.Check network connection."
    "2.Restart the router and devices."
```
#### (2X12)
```
- 错误内容
    - 防火墙端口限制
- 触发条件
    - 日志错误触发："ValueError: Timeout"
- 提示内容
    " Firewall blocking access."
- 引导内容
    "1.Verify firewall settings."
    "2.Check network configuration."
    "3.Temporarily disable the firewall."
```
#### (2X13)
```
- 错误内容
    - MAC地址冲突
- 触发条件
    - 日志错误触发：
        1."OSError: -202"
        2."ValueError: open connection OSError"
- 提示内容
    " MAC address conflict detected."
- 引导内容
    "1.Check network devices."
    "2.Disconnect conflicting device."
    "3.Change the MAC address."
```
#### (2X14)
```
- 错误内容
    - 网络拥堵
- 触发条件
    - 日志错误触发：
        1."ValueError: Timeout"
        2."OSError: -202"
- 提示内容
    " Network congestion detected."
- 引导内容
    "1.Check network connectivity."
    "2.Check network device load."
    "3.Restart network devices."
```
### Eth[03]（3X00-3X99）

### CoAP[04]（4X00-4X99）

### HTTP[05] (5X00-5X99)

### DIAG[06] (6X00-6X99)

#### (6200)
```
- 错误内容
    - 通用错误码
- 触发条件
    - 当发生了未知的错误时触发
- 提示内容
    " Network congestion detected."
- 引导内容
    "1.Check network connectivity."
    "2.Check network device load."
    "3.Restart network devices."
```

#### (6201)
```
- 错误内容
    - 未查询到Wi-Fi配置
- 触发条件
    - 1.未查找到Wi-Fi配置
    - 2.Wi-Fi配置读取异常
- 提示内容
    " Network congestion detected."
- 引导内容
    "1.Check network connectivity."
    "2.Check network device load."
    "3.Restart network devices."
```

#### (6202)
```
- 错误内容
    - 内网连接失败
- 触发条件
    - ping路由器失败
- 提示内容
    " Network congestion detected."
- 引导内容
    "1.Check network connectivity."
    "2.Check network device load."
    "3.Restart network devices."
```

#### (6203)
```
- 错误内容
    - 外网连接失败
- 触发条件
    - ping外部网站失败
- 提示内容
    " Network congestion detected."
- 引导内容
    "1.Check network connectivity."
    "2.Check network device load."
    "3.Restart network devices."
```

#### (6204)
```
- 错误内容
    - 云服务连接失败
- 触发条件
    - https连接ping服务器失败
- 提示内容
    " Network congestion detected."
- 引导内容
    "1.Check network connectivity."
    "2.Check network device load."
    "3.Restart network devices."
```

#### (6205)
```
- 错误内容
    - 资源获取失败
- 触发条件
    - https连接天气服务器获取资源失败
- 提示内容
    " Network congestion detected."
- 引导内容
    "1.Check network connectivity."
    "2.Check network device load."
    "3.Restart network devices."
```