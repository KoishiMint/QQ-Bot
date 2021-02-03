import nonebot

import config
from nonebot import on_command, CommandSession


SB_MVP = 0


@on_command('sbmvp在哪里', aliases={'sb几', 'sb哪', 'mvp几', 'sb几线'}, only_to_me=False)
async def _(session: CommandSession):
    global SB_MVP
    if SB_MVP == 0:
        await session.send('还没有SBMVP')
    else:
        await session.send('SBMVP在' + str(SB_MVP) + '线')


@on_command('sbmvp', aliases={'sb在', 'SBMVP', 'sb', 'SB'}, only_to_me=False)
async def _(session: CommandSession):
    if 31 > int(session.current_arg_text) > -1:
        global SB_MVP
        SB_MVP = int(session.current_arg_text)
        await session.send('已修改SBMVP在' + str(SB_MVP) + '线')


@nonebot.scheduler.scheduled_job(
    'cron',
    # year=None,
    # month=None,
    # day=None,
    # week=None,
    # day_of_week="mon,tue,wed,thu,fri",
    # hour=7,
    minute="13,14,43,44"
    # second="0, 15, 30, 45"
    # start_date=None,
    # end_date=None,
    # timezone=None,
)
async def _():
    if SB_MVP != 0:
        bot = nonebot.get_bot()
        cqm = ''
        for group in config.QQ_GROUP:
            for qq in config.MVP_LIST:
                if int(group) == int(config.MVP_LIST.get(qq)):
                    cqm += '[CQ:at,qq=' + str(qq) + '] '
            if cqm != '':
                cqm += '\n'
            cqm += 'sbmvp马上要发了，在' + str(SB_MVP) + '线'
            await bot.send_group_msg(group_id=group, message=cqm)
            cqm = ''


@on_command('求MVP', aliases={'求mvp', '有mvp吗'}, only_to_me=False)
async def _(session: CommandSession):
    if config.MVP_LIST.get(session.event.user_id) is not None:
        await session.send('已在通知列表内')
    else:
        config.MVP_LIST[session.event.user_id] = session.event.group_id
        await session.send('已添加通知列表')


@on_command('取消MVP', aliases={'取消mvp'}, only_to_me=False)
async def _(session: CommandSession):
    if config.MVP_LIST.get(session.event.user_id) is None:
        await session.send('未在通知列表内')
    else:
        config.MVP_LIST.pop(session.event.user_id)
        await session.send('已取消通知列表')
