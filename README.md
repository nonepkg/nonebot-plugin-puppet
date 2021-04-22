# Nonebot Plugin Puppet

基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的会话转接插件

[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_puppet)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)
![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-puppet.svg)

### 安装

#### 从 PyPI 安装（推荐）

- 使用 nb-cli  

```
nb plugin install nonebot_plugin_puppet
```

- 使用 poetry

```
poetry add nonebot_plugin_puppet
```

- 使用 pip

```
pip install nonebot_plugin_puppet
```

#### 从 GitHub 安装（不推荐）

```
git clone https://github.com/Jigsaw111/nonebot_plugin_puppet.git
```

### 使用

**仅限超级用户使用**

**不建议同时链接多个会话（尤其是大群），如被风控概不负责**

- `puppet link` 链接会话
- - `-ua user_id ..., --user-a user_id ...` 可选参数，指定源会话的 QQ 号
- - `-ga group_id ..., --group-b group_id ...` 可选参数，指定源会话的群号
- - 不设置的话默认为当前会话的 QQ 号/群号
- - `-u user_id ..., --user-b user_id ...` 可选参数，指定链接会话的 QQ 号
- - `-g group_id ..., --group-b group_id ...` 可选参数，指定链接会话的群号
- - 至少需要设置一个
- `puppet unlink` 取消链接会话
- - `-ua user_id ..., --user-a user_id ...` 可选参数，指定源会话的 QQ 号
- - `-ga group_id ..., --group-b group_id ...` 可选参数，指定源会话的群号
- - 不设置的话默认为当前会话的 QQ 号/群号
- - `-u user_id ..., --user-b user_id ...` 可选参数，指定链接会话的 QQ 号
- - `-g group_id ..., --group-b group_id ...` 可选参数，指定链接会话的群号
- - 不设置的话，默认为当前会话链接的所有会话
- `puppet list` 查看链接会话列表
- - `-u user_id, --user user_id` 互斥参数，指定会话的 QQ 号
- - `-g group_id, --group group_id` 互斥参数，指定会话的群号
- - 不设置的话默认为当前会话的 QQ 号/群号
- `puppet send message` 向指定会话发送消息，支持 CQ 码
- - - `message` 需要发送的消息，支持 CQ 码，如含空格请用 `""` 包裹
- - `-u user_id ..., --user user_id ...` 可选参数，指定接收会话的 QQ 号
- - `-g group_id ..., --group group_id ...` 可选参数，指定接收会话的群号
- - 不设置的话默认为当前会话链接的所有会话
- - `--a, --all` 可选参数，指定所有群聊

### Q&A

- **这是什么？**  
  会话转接。
- **有什么用？**  
  **没有用**。这个功能一开始是 Dice! 的一部分（具体是不是这功能我不知道，我从没用过），我的移植计划将其从 NoDice 项目中剔除出来（同时剔除的还有一大堆奇奇怪怪的功能），感觉还挺好玩的就写了这么个插件。

<details>
<summary>展开更多</summary>

### Bug

- [x] 不允许多个超级用户链接到同一会话
- [x] 如果指定的会话不在会话列表里会产生错误

### To Do

- [ ] 允许单向转接
- [ ] 转接请求和通知

### Changelog

- 210421 0.2.0-alpha.1
- - 实现多对多的会话转接
- - 重构数据结构以便下次更新
- 210416 0.1.0
- - 实现单(超级用户)对单(好友,群)的会话转接

</details>
