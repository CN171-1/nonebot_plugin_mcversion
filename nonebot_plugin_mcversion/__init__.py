# 导入必要的库
import os
import httpx
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
    async with httpx.AsyncClient() as client:
        response = await client.get("http://launchermeta.mojang.com/mc/game/version_manifest.json")
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
    async with httpx.AsyncClient() as client:
        response = await client.get("http://launchermeta.mojang.com/mc/game/version_manifest.json")
    data = response.json()
    version = data["versions"][0]
    if not os.path.exists('data/latest_version.txt'):
        with open('data/latest_version.txt', 'w') as f:
            f.write(version["id"])
    with open('data/latest_version.txt', 'r') as f:
        old_version = f.read()
    if version["id"] != old_version:
        release_time = version["releaseTime"]
        release_time = datetime.strptime(release_time, '%Y-%m-%dT%H:%M:%S%z')
        release_time = release_time.replace(hour=release_time.hour+8)
        release_time = release_time.strftime('%Y-%m-%dT%H:%M:%S+08')
        for i in mcver_group_id:
            int (i)
            await bot.send_group_msg(
                group_id=i,
                message=Message(f'发现MC更新：{version["id"]} ({version["type"]})\n时间：{release_time}')
            )
        with open('data/latest_version.txt', 'w') as f:
            f.write(version["id"])

# 获取nonebot的机器人实例
from nonebot import get_bots
# 定义定时任务，每分钟检查一次Minecraft更新
@scheduler.scheduled_job('interval', minutes=1)
async def mc_update_check():
    (bot, ) = get_bots().values()
    await check_mc_update(bot)
