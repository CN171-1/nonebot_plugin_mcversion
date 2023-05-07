# README
<!--
<div align="center">
  <img src="your_project_logo.png" alt="Logo" width="200">
</div>
-->
## 描述

该项目是一个使用 Python 编写的简单程序，用于获取 Minecraft 最新版本信息并定时检查更新，并在指定的群组内发送消息通知。

## 功能特点

- 获取最新的 Minecraft 版本信息
- 定时检查 Minecraft 是否有新版本
- 在指定群组内发送更新通知消息

## 安装

（待补充）

## 使用

1. 使用 `mcver` , `mcversion` ,`MC版本` 来获取当前最新MC版本
2. 程序会每分钟自动检查 Minecraft 是否有新版本，若有则会在指定的群组内发送消息。

## 配置

在配置文件中可以进行以下设置：

- `mcver_group_id`：指定检查 Minecraft 更新后发送消息的群组 ID。

```python
mcver_group_id = [123456, 789012]
```

## 鸣谢

- [nonebot_plugin_apscheduler](https://github.com/nonebot/nonebot-plugin-apscheduler) - NoneBot 的定时任务插件

## 反馈

- 问题跟踪：[GitHub Issues](https://github.com/your_username/your_project/issues)
