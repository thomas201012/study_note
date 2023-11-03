# D1连接状态码示例，
### 连接wifi
    EVENT = 2
    EVENT = 4
    EVENT = 0
### wifi失去连接(路由器断电)
    EVENT = 21
    EVENT = 5,reason = 201

### 路由器黑名单
    EVENT = 5,reason = 37
    EVENT = 5,reason = 202
    EVENT = 5,reason = 205

### 密码错误
    EVENT = 5,reason = 6
    EVENT = 5,reason = 204
    EVENT = 5,reason = 205
    EVENT = 5,reason = 15

# 网络状态码
## 网络事件状态ID码
    SYSTEM_EVENT_WIFI_READY                = 0,           /*!< ESP32 WiFi ready *//*!< ESP32 WiFi 就绪 */
    SYSTEM_EVENT_SCAN_DONE,                = 1,           /*!< ESP32 finish scanning AP *//*!< ESP32 完成扫描 AP */
    SYSTEM_EVENT_STA_START,                = 2,           /*!< ESP32 station start *//*!< ESP32 站启动 */
    SYSTEM_EVENT_STA_STOP,                 = 3,           /*!< ESP32 station stop *//*!< ESP32 站停止 */
    SYSTEM_EVENT_STA_CONNECTED,            = 4,           /*!< ESP32 station connected to AP *//*!< ESP32 站点已连接到 AP */
    SYSTEM_EVENT_STA_DISCONNECTED,         = 5,           /*!< ESP32 station disconnected from AP *//*!< ESP32 站点与 AP 断开连接 */
    SYSTEM_EVENT_STA_AUTHMODE_CHANGE,      = 6,           /*!< the auth mode of AP connected by ESP32 station changed *//*!< ESP32 station 连接的 AP 认证模式改变 */
    SYSTEM_EVENT_STA_GOT_IP,               = 7,           /*!< ESP32 station got IP from connected AP *//*!< ESP32 站点从连接的 AP 获取 IP */
    SYSTEM_EVENT_STA_LOST_IP,              = 8,           /*!< ESP32 station lost IP and the IP is reset to 0 *//*!< ESP32 站点丢失 IP，IP 重置为 0 */
    SYSTEM_EVENT_STA_BSS_RSSI_LOW,         = 9,           /*!< ESP32 station connected BSS rssi goes below threshold *//*!< ESP32 站连接的 BSS rssi 低于阈值 */
    SYSTEM_EVENT_STA_WPS_ER_SUCCESS,       = 10,          /*!< ESP32 station wps succeeds in enrollee mode *//*!< ESP32 站 wps 在登记者模式下成功 */
    SYSTEM_EVENT_STA_WPS_ER_FAILED,        = 11,          /*!< ESP32 station wps fails in enrollee mode *//*!< ESP32 station wps 在登记者模式下失败 */
    SYSTEM_EVENT_STA_WPS_ER_TIMEOUT,       = 12,          /*!< ESP32 station wps timeout in enrollee mode *//*!< ESP32 站员模式下 wps 超时 */
    SYSTEM_EVENT_STA_WPS_ER_PIN,           = 13,          /*!< ESP32 station wps pin code in enrollee mode *//*!< ESP32 站员模式下的 WPS PIN 码 */
    SYSTEM_EVENT_STA_WPS_ER_PBC_OVERLAP,   = 14,          /*!< ESP32 station wps overlap in enrollee mode *//*!< ESP32 站 wps 在参与者模式下重叠 */
    SYSTEM_EVENT_AP_START,                 = 15,          /*!< ESP32 soft-AP start *//*!< ESP32 软 AP 启动 */
    SYSTEM_EVENT_AP_STOP,                  = 16,          /*!< ESP32 soft-AP stop *//*!< ESP32 软 AP 停止 */
    SYSTEM_EVENT_AP_STACONNECTED,          = 17,          /*!< a station connected to ESP32 soft-AP *//*!< 连接到 ESP32 软 AP 的站点 */
    SYSTEM_EVENT_AP_STADISCONNECTED,       = 18,          /*!< a station disconnected from ESP32 soft-AP *//*!< 某个站点与 ESP32 软 AP 断开连接 */
    SYSTEM_EVENT_AP_STAIPASSIGNED,         = 19,          /*!< ESP32 soft-AP assign an IP to a connected station *//*!< ESP32 soft-AP 为连接的站点分配 IP */
    SYSTEM_EVENT_AP_PROBEREQRECVED,        = 20,          /*!< Receive probe request packet in soft-AP interface *//*!< 在软 AP 接口接收探测请求数据包 */
    SYSTEM_EVENT_ACTION_TX_STATUS,         = 21,          /*!< Receive status of Action frame transmitted *//*!< 接收发送的 Action 帧的状态 */
    SYSTEM_EVENT_ROC_DONE,                 = 22,          /*!< Indicates the completion of Remain-on-Channel operation status *//*!< 表示Remain-on-Channel操作完成状态*/
    SYSTEM_EVENT_STA_BEACON_TIMEOUT,       = 23,          /*!< ESP32 station beacon timeout *//*!< ESP32 基站信标超时 */
    SYSTEM_EVENT_FTM_REPORT,               = 24,          /*!< Receive report of FTM procedure *//*!< 接收FTM过程报告*/
    SYSTEM_EVENT_GOT_IP6,                  = 25,          /*!< ESP32 station or ap or ethernet interface v6IP addr is preferred *//*!< 首选 ESP32 站或 ap 或以太网接口 v6IP 地址 */


    SYSTEM_EVENT_ETH_START,                = 26,          /*!< ESP32 ethernet start *//*!< ESP32 以太网启动 */
    SYSTEM_EVENT_ETH_STOP,                 = 27,          /*!< ESP32 ethernet stop *//*!< ESP32 以太网停止 */
    SYSTEM_EVENT_ETH_CONNECTED,            = 28,          /*!< ESP32 ethernet phy link up *//*!< ESP32 以太网 phy 连接 */
    SYSTEM_EVENT_ETH_DISCONNECTED,         = 29,          /*!< ESP32 ethernet phy link down *//*!< ESP32 以太网物理链路断开 */
    SYSTEM_EVENT_ETH_GOT_IP,               = 30,          /*!< ESP32 ethernet got IP from connected AP *//*!< ESP32 以太网从连接的 AP 获取 IP */
    SYSTEM_EVENT_ETH_LOST_IP,              = 31,          /*!< ESP32 ethernet lost IP and the IP is reset to 0 *//*!< ESP32 以太网丢失 IP 并且 IP 重置为 0 */
    SYSTEM_EVENT_MAX                       = 32,          /*!< Number of members in this enum *//*!< 此枚举中的成员数 */

## 网络事件信息

    system_event_sta_connected_t               connected;          /*!< ESP32 station connected to AP *//*!< ESP32 站连接到 AP */
    system_event_sta_disconnected_t            disconnected;       /*!< ESP32 station disconnected to AP *//*!< ESP32 站点与 AP 断开连接 */
    system_event_sta_scan_done_t               scan_done;          /*!< ESP32 station scan (APs) done *//*!< ESP32 站扫描（AP）完成 */
    system_event_sta_authmode_change_t         auth_change;        /*!< the auth mode of AP ESP32 station connected to changed *//*!< 所连接的 AP ESP32 站点的认证模式已更改 */
    system_event_sta_got_ip_t                  got_ip;             /*!< ESP32 station got IP, first time got IP or when IP is changed *//*!< ESP32 站点获取 IP、第一次获取 IP 或 IP 更改时*/
    system_event_sta_wps_er_pin_t              sta_er_pin;         /*!< ESP32 station WPS enrollee mode PIN code received *//*!< ESP32 站 WPS 注册者模式 PIN 码收到 */
    system_event_sta_wps_fail_reason_t         sta_er_fail_reason; /*!< ESP32 station WPS enrollee mode failed reason code received *//*!< 收到 ESP32 站 WPS 登记者模式失败原因代码 */
    system_event_sta_wps_er_success_t          sta_er_success;     /*!< ESP32 station WPS enrollee success *//*!< ESP32站WPS注册成功*/
    system_event_ap_staconnected_t             sta_connected;      /*!< a station connected to ESP32 soft-AP *//*!< 连接到 ESP32 soft-AP 的站点 */
    system_event_ap_stadisconnected_t          sta_disconnected;   /*!< a station disconnected to ESP32 soft-AP *//*!< 某个站点与 ESP32 soft-AP 断开连接 */
    system_event_ap_probe_req_rx_t             ap_probereqrecved;  /*!< ESP32 soft-AP receive probe request packet *//*!< ESP32 soft-AP 接收探测请求数据包 */
    system_event_ftm_report_t                  ftm_report;         /*!< Report of FTM procedure *//*!< FTM程序报告*/
    system_event_ap_staipassigned_t            ap_staipassigned;   /**< ESP32 soft-AP assign an IP to the station*//**< ESP32 soft-AP 为站点分配 IP*/
    system_event_got_ip6_t                     got_ip6;            /*!< ESP32 station　or ap or ethernet ipv6 addr state change to preferred *//*!< ESP32 station或 ap 或 ethernet ipv6 addr 状态更改为首选 */
## wifi断开原因状态码（disconnected->reason）
    WIFI_REASON_UNSPECIFIED                        = 1,"未指定的原因，或原因未知"
    WIFI_REASON_AUTH_EXPIRE                        = 2,"身份验证过期"
    WIFI_REASON_AUTH_LEAVE                         = 3,"身份验证离开"
    WIFI_REASON_ASSOC_EXPIRE                       = 4,"关联过期"
    WIFI_REASON_ASSOC_TOOMANY                      = 5,"关联太多"
    WIFI_REASON_NOT_AUTHED                         = 6,"未经身份验证"
    WIFI_REASON_NOT_ASSOCED                        = 7,"未关联"
    WIFI_REASON_ASSOC_LEAVE                        = 8,"关联离开"
    WIFI_REASON_ASSOC_NOT_AUTHED                   = 9,"关联但未经身份验证"
    WIFI_REASON_DISASSOC_PWRCAP_BAD                = 10,"断开关联，电源能力不佳"
    WIFI_REASON_DISASSOC_SUPCHAN_BAD               = 11,"断开关联，支持的信道不佳"
    WIFI_REASON_BSS_TRANSITION_DISASSOC            = 12,"BSS 过渡断开关联"
    WIFI_REASON_IE_INVALID                         = 13,"无效的信息元素"
    WIFI_REASON_MIC_FAILURE                        = 14,"MIC（消息完整性校验）失败"
    WIFI_REASON_4WAY_HANDSHAKE_TIMEOUT             = 15,"4次握手超时"
    WIFI_REASON_GROUP_KEY_UPDATE_TIMEOUT           = 16,"组密钥更新超时"
    WIFI_REASON_IE_IN_4WAY_DIFFERS                 = 17,"4次握手中的信息元素不匹配"
    WIFI_REASON_GROUP_CIPHER_INVALID               = 18,"组密码无效"
    WIFI_REASON_PAIRWISE_CIPHER_INVALID            = 19,"一对一密码无效"
    WIFI_REASON_AKMP_INVALID                       = 20,"AKMP（认证和密钥管理协议）无效"
    WIFI_REASON_UNSUPP_RSN_IE_VERSION              = 21,"不支持的 RSN（Robust Security Network）信息元素版本"
    WIFI_REASON_INVALID_RSN_IE_CAP                 = 22,"无效的 RSN 信息元素能力"
    WIFI_REASON_802_1X_AUTH_FAILED                 = 23,"802.1X 身份验证失败"
    WIFI_REASON_CIPHER_SUITE_REJECTED              = 24,"密码套件被拒绝"
    WIFI_REASON_TDLS_PEER_UNREACHABLE              = 25,"TDLS（Tunneled Direct Link Setup）对等端无法访问"
    WIFI_REASON_TDLS_UNSPECIFIED                   = 26,"未指定的 TDLS 原因"
    WIFI_REASON_SSP_REQUESTED_DISASSOC             = 27,"SSP（Secure Simple Pairing）请求断开关联"
    WIFI_REASON_NO_SSP_ROAMING_AGREEMENT           = 28,"没有 SSP 漫游协议"
    WIFI_REASON_BAD_CIPHER_OR_AKM                  = 29,"不良的密码或 AKM（认证和密钥管理）"
    WIFI_REASON_NOT_AUTHORIZED_THIS_LOCATION       = 30,"未经授权的位置"
    WIFI_REASON_SERVICE_CHANGE_PERCLUDES_TS        = 31,"服务更改阻止了 TS（Traffic Specification）"
    WIFI_REASON_UNSPECIFIED_QOS                    = 32,"未指定的 QoS（Quality of Service）"
    WIFI_REASON_NOT_ENOUGH_BANDWIDTH               = 33,"带宽不足"
    WIFI_REASON_MISSING_ACKS                       = 34,"缺少 ACK（确认）"
    WIFI_REASON_EXCEEDED_TXOP                      = 35,"超过 TXOP（传输机会）"
    WIFI_REASON_STA_LEAVING                        = 36,"STA（Station）离开"
    WIFI_REASON_END_BA                             = 37,"结束 BA（Block Acknowledgment）"
    WIFI_REASON_UNKNOWN_BA                         = 38,"未知的 BA"
    WIFI_REASON_TIMEOUT                            = 39,"超时"
    WIFI_REASON_PEER_INITIATED                     = 46,"对等端发起"
    WIFI_REASON_AP_INITIATED                       = 47,"AP（Access Point）发起"
    WIFI_REASON_INVALID_FT_ACTION_FRAME_COUNT      = 48,"无效的 FT（Fast Transition）操作帧计数"
    WIFI_REASON_INVALID_PMKID                      = 49,"无效的 PMKID（Pairwise Master Key Identifier）"
    WIFI_REASON_INVALID_MDE                        = 50,"无效的 MDE（Mobility Domain Element）"
    WIFI_REASON_INVALID_FTE                        = 51,"无效的 FTE（Fast Transition Element）"
    WIFI_REASON_TRANSMISSION_LINK_ESTABLISH_FAILED = 67,"传输链路建立失败"
    WIFI_REASON_ALTERATIVE_CHANNEL_OCCUPIED        = 68,"替代信道被占用"

    WIFI_REASON_BEACON_TIMEOUT                     = 200,"信标超时"
    WIFI_REASON_NO_AP_FOUND                        = 201,"未找到 AP"
    WIFI_REASON_AUTH_FAIL                          = 202,"身份验证失败"
    WIFI_REASON_ASSOC_FAIL                         = 203,"关联失败"
    WIFI_REASON_HANDSHAKE_TIMEOUT                  = 204,"握手超时"
    WIFI_REASON_CONNECTION_FAIL                    = 205,"连接失败"
    WIFI_REASON_AP_TSF_RESET                       = 206,"AP 的 TSF（Time Synchronization Function）重置"
    WIFI_REASON_ROAMING                            = 207,"漫游"
    WIFI_REASON_ASSOC_COMEBACK_TIME_TOO_LONG       = 208,"关联回来时间过长"
    WIFI_REASON_SA_QUERY_TIMEOUT                   = 209," SA（Security Association）查询超时"

## 认证模式状态码(auth_change->old_mode)(auth_change->new_mode)
    WIFI_AUTH_OPEN = 0,         /**< authenticate mode : open */
    WIFI_AUTH_WEP,              /**< authenticate mode : WEP */
    WIFI_AUTH_WPA_PSK,          /**< authenticate mode : WPA_PSK */
    WIFI_AUTH_WPA2_PSK,         /**< authenticate mode : WPA2_PSK */
    WIFI_AUTH_WPA_WPA2_PSK,     /**< authenticate mode : WPA_WPA2_PSK */
    WIFI_AUTH_WPA2_ENTERPRISE,  /**< authenticate mode : WPA2_ENTERPRISE */
    WIFI_AUTH_WPA3_PSK,         /**< authenticate mode : WPA3_PSK */
    WIFI_AUTH_WPA2_WPA3_PSK,    /**< authenticate mode : WPA2_WPA3_PSK */
    WIFI_AUTH_WAPI_PSK,         /**< authenticate mode : WAPI_PSK */
    WIFI_AUTH_MAX