# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.2.0 - 2021-09-28 

### Removed

- 删除数据文件莫名其妙的前缀

### Fixed

- 修复 flag 记录残留的 bug
- 修复 aprv/rej 操作无效的 bug
- 修复 aprv 需要参数 message 的 bug

## 0.2.0-alpha.6 - 2021-05-25 

### Added 

- 新增退群功能

### Fixed

- 修复 list 重复展示的 bug
- 修复 aprv/rej 操作无效的 bug

## 0.2.0-alpha.5 - 2021-05-25

### Added

- 实现转接请求事件

### Fixed

- 修复 ln/rm 操作无效的 bug
- 修复 list 重复展示的 bug
- 修复 --undirect 参数无效的 bug

## 0.2.0-alpha.4 - 2021-04-29 

### Added

- 支持 -h, --help 参数
- 发生错误时返回相关信息

### Changed

- 部分命令提供缩写
- list 命令能够显示单双向
- 分离 handle 与 parser

## 0.2.0-alpha.3 - 2021-04-29 

### Added

- 实现单向的会话转接

### Fixed

- 修复未设置群名片时昵称为空的问题

## 0.2.0-alpha.2 - 2021-04-29 

### Fixed

- 修复指定会话不在会话列表时会产生错误的问题
- 修复群发消息时由于风控/禁言而被打断的问题

## 0.2.0-alpha.1 - 2021-04-21 

### Added

- 实现多对多的会话转接

### Changed

- 重构数据结构以便下次更新

## 0.1.0 - 2021-04-16 

### Added

- 实现单对单的会话转接
