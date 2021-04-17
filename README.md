# Nonebot Plugin Puppet

基于 [nonebot2](https://github.com/nonebot/nonebot2) 和 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 的会话转接插件

[![License](https://img.shields.io/github/license/Jigsaw111/nonebot_plugin_puppet)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a11+-red.svg)
![Pypi Version](https://img.shields.io/pypi/v/nonebot-plugin-puppet.svg)

### 安装

#### 从 PyPI 安装（推荐）

<!--
- 使用 nb-cli  

```
nb plugin install nonebot_plugin_puppet
```
-->

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

**仅限超级用户私聊使用**

- `puppet link` 链接会话
- - `-u user_id, --user user_id` 可选参数，指定链接会话的 QQ 号
- - `-g group_id, --group group_id` 可选参数，指定链接会话的群号
- `puppet send message` 向链接会话发送消息，用于发送已被占用的指令
- - `message` 需要发送消息，如有空格请用 `""` 包裹
- `puppet unlink` 取消链接会话

### Q&A

- **这是什么？**  
  会话转接，让 Nonebot 成为你的傀儡。
- **有什么用？**  
  **没有用**。

<details>
<summary>展开更多</summary>

### Bug

- [ ] 不允许多个超级用户链接到同一会话

### Changelog

- 210416，创建项目。

</details>
