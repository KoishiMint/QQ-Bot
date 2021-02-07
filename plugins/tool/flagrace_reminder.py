"""
提醒跑旗小助手
跑旗时间默认为整点，会在整点前10,5,3,2,1分钟进行播报
如果跑旗时间有变化，请修改`FLAG_HOUR_LIST`（24小时制）
如果需要增删提醒时间，请修改`FLAG_REM_MIN_AHEAD_LIST`
"""

import nonebot
from nonebot.permission import SUPERUSER
from nonebot import on_command, CommandSession
from config import NICKNAME

NICKNAME = list(NICKNAME)[0]

FLAG_TIMEZONE = 'Asia/Shanghai'
FLAG_HOUR_LIST = "3, 5, 6, 7, 20"
FLAG_REM_MIN_AHEAD_LIST = [10, 5, 2, 1]

FLAG_GROUP_LIST = []


# Reminder hours, should be 1 before actual flag race hours
# TODO: this will be buggy if FLAG_HOUR_LIST contains 0
reminder_hour_list = ', '.join([str(int(hr) - 1) for hr in FLAG_HOUR_LIST.split(', ')])

# Send reminder before flag race starts
for min_ahead in FLAG_REM_MIN_AHEAD_LIST:
    @nonebot.scheduler.scheduled_job(
        'cron',
        hour=reminder_hour_list,
        minute=f"{60 - min_ahead}",
        timezone=FLAG_TIMEZONE,
        kwargs={'minute_ahead': min_ahead}
    )
    async def _(minute_ahead):
        if FLAG_GROUP_LIST:
            bot = nonebot.get_bot()
            cqm = f'{NICKNAME}提醒：离跑旗开始还剩{minute_ahead}分钟，请尽快移动到允许传送的地图例如主城，准备点击头顶信封。'
            for group in FLAG_GROUP_LIST:
                await bot.send_group_msg(group_id=group, message=cqm)


# Turn on/off reminder
@on_command('开启跑旗提醒', aliases={'开启跑旗'}, permission=SUPERUSER)
async def _(session: CommandSession):
    global FLAG_GROUP_LIST
    if session.event.group_id not in FLAG_GROUP_LIST:
        FLAG_GROUP_LIST.append(session.event.group_id)
        await session.send(f'{NICKNAME}已开启本群跑旗提醒功能')
    else:
        await session.send(f'{NICKNAME}发现本群跑旗提醒已是开启状态')


@on_command('关闭跑旗提醒', aliases={'关闭跑旗'}, permission=SUPERUSER)
async def _(session: CommandSession):
    global FLAG_GROUP_LIST
    if session.event.group_id in FLAG_GROUP_LIST:
        FLAG_GROUP_LIST.remove(session.event.group_id)
        await session.send(f'{NICKNAME}已关闭本群跑旗提醒功能')
    else:
        await session.send(f'{NICKNAME}发现本群跑旗提醒已是关闭状态')
