# 导入必要的库
import os
import requests
from datetime import datetime
from nonebot import on_command, get_driver, require, Config
from nonebot.adapters.onebot.v11 import Bot
from nonebot.adapters.onebot.v11.message import Message

env_config = Config(**get_driver().config.dict())
mcver_group_id = list(env_config.mcver_group_id)

# 定义命令“mcver”
mcver = on_command('mcver', aliases={'mcversion', 'MC版本'}, priority=50)

# 处理命令“mcver”
@mcver.handle()
async def mcver_handle():
    # 获取Minecraft版本信息
    url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
    response = requests.get(url)
    data = response.json()
    latest_release = data['latest']['release']
    latest_snapshot = data['latest']['snapshot']
    # 发送消息
    await mcver.finish(message = Message(f'最新正式版：{latest_release}\n最新快照版：{latest_snapshot}'))

# 获取nonebot的调度器
scheduler = require('nonebot_plugin_apscheduler').scheduler

# 定义异步函数，用于检查Minecraft更新
async def check_mc_update(bot: Bot):
    # 获取Minecraft版本信息
    url = 'https://launchermeta.mojang.com/mc/game/version_manifest.json'
    response = requests.get(url)
    data = response.json()
    latest_release = data['latest']['release']
    latest_snapshot = data['latest']['snapshot']
    if not os.path.exists('data/latest_release.txt'):# 检查data目录下是否有latest_release.txt文件
    # 若没有，则创建一个latest_release.txt文件
        with open('data/latest_release.txt', 'w') as f:
            f.write(latest_release)
    if not os.path.exists('data/latest_snapshot.txt'):# 检查data目录下是否有latest_snapshot.txt文件
    # 若没有，则创建一个latest_snapshot.txt文件
        with open('data/latest_snapshot.txt', 'w') as f:
            f.write(latest_snapshot)
    # 读取旧版本信息
    with open('data/latest_release.txt', 'r') as f:
        old_release = f.read()
    with open('data/latest_snapshot.txt', 'r') as f:
        old_snapshot = f.read()
    # 检查是否有新版本
    if latest_release != old_release:
        # 更新版本信息
        with open('data/latest_release.txt', 'w') as f:
            f.write(latest_release)
        # 获取版本发布时间
        release_time = ''
        for version in data['versions']:
            if version['id'] == latest_release:
                release_time = version['releaseTime']
                break
        release_time = datetime.strptime(release_time, '%Y-%m-%dT%H:%M:%S%z')
        release_time = release_time.replace(hour=release_time.hour+8)
        release_time = release_time.strftime('%Y-%m-%dT%H:%M:%S+08')
        # 发送群消息
        for i in mcver_group_id:
            int (i)
            await bot.send_group_msg(
                group_id=i,
                message=Message(f'发现MC更新：{latest_release} (Release)\n时间：{release_time}')
            )
    if latest_snapshot != old_snapshot:
        # 更新版本信息
        with open('data/latest_snapshot.txt', 'w') as f:
            f.write(latest_snapshot)
        # 获取版本发布时间
        snapshot_time = ''
        for version in data['versions']:
            if version['id'] == latest_snapshot:
                snapshot_time = version['releaseTime']
                break
        snapshot_time = datetime.strptime(snapshot_time, '%Y-%m-%dT%H:%M:%S%z')
        snapshot_time = snapshot_time.replace(hour=snapshot_time.hour+8)
        snapshot_time = snapshot_time.strftime('%Y-%m-%dT%H:%M:%S+08')
        # 发送群消息
        for i in mcver_group_id:
            int (i)
            await bot.send_group_msg(
                group_id=i,
                message=Message(f'发现MC更新：{latest_snapshot} (Snapshot)\n时间：{snapshot_time}')
            )
# 获取nonebot的机器人实例
from nonebot import get_bots
# 定义定时任务，每分钟检查一次Minecraft更新
@scheduler.scheduled_job('interval', minutes=1)
async def mc_update_check():
    (bot, ) = get_bots().values()
    await check_mc_update(bot)
