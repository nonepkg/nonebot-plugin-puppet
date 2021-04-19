# Nonebot Plugin Transfer

基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的会话转接插件

[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_transfer)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)
![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-transfer.svg)

### 安装

#### 从 PyPI 安装（推荐）

- 使用 nb-cli  

```
nb plugin install nonebot_plugin_transfer
```

- 使用 poetry

```
poetry add nonebot_plugin_transfer
```

- 使用 pip

```
pip install nonebot_plugin_transfer
```

#### 从 GitHub 安装（不推荐）

```
git clone https://github.com/Jigsaw111/nonebot_plugin_transfer.git
```

### 使用

**仅限超级用户使用**

**不建议同时链接多个会话（尤其是大群），如被风控概不负责**

- `trans link` 链接会话
- - `-u user_id, --user user_id` 可选参数，指定链接会话的 QQ 号
- - `-g group_id, --group group_id` 可选参数，指定链接会话的群号
- `trans send message` 向链接会话发送消息，用于发送已被占用的指令
- - `message` 需要发送消息，如有空格请用 `""` 包裹
- `trans unlink` 取消链接会话

### Q&A

- **这是什么？**  
  会话转接。
- **有什么用？**  
  **没有用**。这个功能一开始是 Dice! 的一部分（具体是不是这功能我不知道，我从没用过），我的移植计划将其从 NoDice 项目中剔除出来（同时剔除的还有一大堆奇奇怪怪的功能），感觉还挺好玩的就写了这么个插件。

<details>
<summary>展开更多</summary>

### Bug

- [x] 不允许多个超级用户链接到同一会话

### 原理

一开始其实只是想调用转发消息的 API 来实现，但是这样无法得知发送消息的人和会话，所以就得自己造轮子了。

0.1.0 的时候实现了简单的单对单转接 (超级用户私聊<->群，超级用户私聊<->私聊)，但是我不太满意，于是打算再进一步实现多对多的转接，然后就写会话映射的数据结构写得差点脑溢血了。目前把命令之外的消息转接部分搞定了（大概）。

私聊<->群 conv sender msg
群<->私聊
私聊<->私聊
群<->群


### Changelog

- 210416，创建项目。

</details>
