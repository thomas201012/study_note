在安装好ota程序后，需要进行ota开机启动的配置
1. 配置延时启动定时器
    - 创建一个新的定时器单元文件。使用以下命令创建一个名为 delayed-start.timer 的定时器单元文件：
        sudo nano /etc/systemd/system/delayed-start.timer
        在编辑器中，将以下内容粘贴到文件中：

        [Unit]
        Description=Delayed Start Timer

        [Timer]
        OnBootSec=2min  # 设置延时启动的时间，这里是2分钟
        Unit=nodemon.service

        [Install]
        WantedBy=multi-user.target
        在上面的示例中，我们设置了一个延时为30秒的定时器，并指定了要启动的服务单元为 delayed-start.service。
2. 配置nodemon.server服务
    创建一个新的服务单元文件。使用以下命令创建一个名为 delayed-start.service 的服务单元文件：
    sudo nano /etc/systemd/system/delayed-start.service
    在编辑器中，将以下内容粘贴到文件中：

    [Unit]
    Description=Nodemon Service
    After=network.target

    [Service]
    ExecStart=/home/ubuntu/.nvm/versions/node/v16.13.2/bin/nodemon /home/ubuntu/factory_mijia_ble_ota/js/index.js
    WorkingDirectory=/home/ubuntu/factory_mijia_ble_ota/js/
    User=ubuntu
    Restart=always

    [Install]
    WantedBy=multi-user.target
    在上面的示例中，我们使用 ExecStart 指令来定义要在延时启动时执行的命令。这里的命令是启动 nodemon.service。

    保存并关闭文件。

    运行以下命令重新加载 systemd 并启用定时器：

    sudo systemctl daemon-reload
    sudo systemctl enable delayed-start.timer
    这将重新加载 systemd 的配置，并将定时器设置为在系统启动时自动启用。