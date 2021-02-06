import nonebot
from nonebot.permission import SUPERUSER
from nonebot import on_command, CommandSession


URSUS_TIMEZONE = 'Asia/Shanghai'
URSUS_HOUR_LIST = "2, 3, 9, 10"
URSUS_LAST_HOUR_LIST = "3, 10"

URSUS_GROUP_LIST = []


# Send reminder every 30 min
@nonebot.scheduler.scheduled_job(
    'cron',
    hour=URSUS_HOUR_LIST,
    minute="0, 30",
    timezone=URSUS_TIMEZONE
)
async def _():
    if URSUS_GROUP_LIST:
        bot = nonebot.get_bot()
        for group in URSUS_GROUP_LIST:
            cqm = '现在是双倍Ursus时间，请尽快完成。'
            await bot.send_group_msg(group_id=group, message=cqm)


# Send final reminder
@nonebot.scheduler.scheduled_job(
    'cron',
    hour=URSUS_LAST_HOUR_LIST,
    minute="50",
    timezone=URSUS_TIMEZONE
)
async def _():
    if URSUS_GROUP_LIST:
        bot = nonebot.get_bot()
        for group in URSUS_GROUP_LIST:
            cqm = '离双倍Ursus结束还剩10分钟，请尽快完成。'
            await bot.send_group_msg(group_id=group, message=cqm)


@on_command('开启564', aliases={'开启ursus'}, permission=SUPERUSER)
async def _(session: CommandSession):
    global URSUS_GROUP_LIST
    if session.event.group_id not in URSUS_GROUP_LIST:
        URSUS_GROUP_LIST.append(session.event.group_id)
        await session.send('已开启本群Ursus播报功能')
    else:
        await session.send('本群Ursus播报已是开启状态')


@on_command('关闭564', aliases={'关闭ursus'}, permission=SUPERUSER)
async def _(session: CommandSession):
    global URSUS_GROUP_LIST
    if session.event.group_id in URSUS_GROUP_LIST:
        URSUS_GROUP_LIST.remove(session.event.group_id)
        await session.send('已关闭本群Ursus播报功能')
    else:
        await session.send('本群Ursus播报已是关闭状态')
