# QQ Bot

## 简介
QQ Bot 是一款基于NoneBot的QQ机器人，在其基础API之上提供了多种多样的插件，以方便群友问答互动、获取资料。

## 安装
首先，安装过程需要python3.7+，用户应先检查是否具有此Python版本：
```
python --version
```

其次，QQ Bot需要如下组件：
1. QQ Bot自身
2. NoneBot，提供基础解析API 
3. 底层框架，协同与QQ服务器交流

因此安装步骤分为如下三步、缺一不可。

### QQBot
下载最新源码：
```
git clone https://github.com/dusk-primrose/QQ-Bot.git
```

### NoneBot
下载NoneBot最新源码：
```
git clone https://github.com/nonebot/nonebot.git
cd nonebot
python setup.py install
```
安装完成的`.egg`位于本目录`dist`文件夹下，并已自动加入`PYTHONPATH`。

如安装过程有报错，请自行`pip install`所需组件。

如后续使用过程Python报错找不到NoneBot，请手动添加此路径。

### 底层框架
目前能与NoneBot协同的框架有以下两种，用户选择**任意一种**即可：
1. 先驱/OneBot-yaya: https://discourse.xianqubot.com/t/topic/50
2. go-cqhttp: https://github.com/Mrs4s/go-cqhttp

#### 先驱
（待补完）

#### go-cqhttp
首先，从最新release界面下载`go-cqhttp`压缩包: https://github.com/Mrs4s/go-cqhttp/releases
* Windows下32位文件为 go-cqhttp-v*-windows-386.zip
* Windows下64位文件为 go-cqhttp-v*-windows-amd64.zip
* Windows下arm用(如使用高通CPU的笔记本)文件为 go-cqhttp-v*-windows-arm.zip
* Linux下32位文件为 go-cqhttp-v*-linux-386.tar.gz
* Linux下64位文件为 go-cqhttp-v*-linux-amd64.tar.gz
* Linux下arm用(如树莓派)文件为 go-cqhttp-v*-linux-arm.tar.gz

解压缩并打开文件夹，在根目录下新建配置文件`config.hjson`，并替换`[机器人QQ]`与`[机器人密码]`:
<details><summary>config.hjson示例</summary>
<p>

```json
{
    uin: [机器人QQ]
    password: "[机器人密码]"
    encrypt_password: false
    password_encrypted: ""
    enable_db: true
    access_token: ""
    relogin: {
        enabled: true
        relogin_delay: 3
        max_relogin_times: 0
    }
    _rate_limit: {
        enabled: false
        frequency: 1
        bucket_size: 1
    }
    ignore_invalid_cqcode: false
    force_fragmented: false
    fix_url: false
    proxy_rewrite: ""
    heartbeat_interval: 0
    http_config: {
        enabled: false
        host: 127.0.0.1
        port: 8074
        timeout: 0
        post_urls: {}
    }
    ws_config: {
        enabled: false
        host: 127.0.0.1
        port: 8074
    }
    ws_reverse_servers: [
        {
            enabled: true
            reverse_url: ws://127.0.0.1:8074/ws/
            reverse_api_url: ws://127.0.0.1:8074/
            reverse_event_url: ws://127.0.0.1:8074/
            reverse_reconnect_interval: 3000
        }
    ]
    post_message_format: string
    use_sso_address: false
    debug: false
    log_level: ""
    web_ui: {
        enabled: false
        host: 127.0.0.1
        web_ui_port: 8074
        web_input: true
    }
}

```
</p>
</details>

双击`go-cqhttp.exe`，会提示抓取滑块，选**1.自行抓包**，并按如下流程操作：
https://github.com/Mrs4s/go-cqhttp/blob/master/docs/slider.md#%E6%96%B9%E6%A1%88a-%E8%87%AA%E8%A1%8C%E6%8A%93%E5%8C%85

抓包完成之后，可能需要手机扫描二维码。打开所给链接并扫描。

提示登录成功之后，框架就配置好了，可以关掉程序了。

## 使用
首先在QQ Bot根目录下运行`bot.py`:
```
python bot.py
```
此时反向WS服务器已建立，再打开框架：
1. 先驱：（待补充）
2. go-cqhttp：双击`go-cqhttp.exe`

现在机器人就设置好了，开始和机器人的第一次对话吧！

### 示例对话

1.打开QQ程序的机器人小号对话框，向机器人发送 `/echo test`。如配置成功，会收到机器人的回复`test`.

2.如机器人加入群聊，可以在群聊里向机器人发送关键词问答，详情请看源码。

# 附录
## NoneBot 简介
NoneBot 是一个基于 [OneBot 标准](https://github.com/howmanybots/onebot)（原 CQHTTP） 的 Python 异步 QQ 机器人框架，它会对 QQ 机器人收到的消息进行解析和处理，并以插件化的形式，分发给消息所对应的命令处理器和自然语言处理器，来完成具体的功能。

除了起到解析消息的作用，NoneBot 还为插件提供了大量实用的预设操作和权限控制机制，尤其对于命令处理器，它更是提供了完善且易用的会话机制和内部调用机制，以分别适应命令的连续交互和插件内部功能复用等需求。

NoneBot 在其底层与 OneBot 实现交互的部分使用 [aiocqhttp](https://github.com/nonebot/aiocqhttp) 库，后者在 [Quart](https://pgjones.gitlab.io/quart/) 的基础上封装了与 OneBot 实现的网络交互。

得益于 Python 的 [asyncio](https://docs.python.org/3/library/asyncio.html) 机制，NoneBot 处理消息的吞吐量有了很大的保障，再配合 OneBot 标准的 WebSocket 通信方式（也是最建议的通信方式），NoneBot 的性能可以达到 HTTP 通信方式的两倍以上，相较于传统同步 I/O 的 HTTP 通信，更是有质的飞跃。

需要注意的是，NoneBot 仅支持 Python 3.7+。