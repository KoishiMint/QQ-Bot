import nonebot
from config import *
from nonebot import on_command, CommandSession

from plugins.tool.bottool import send_all_group

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
    minute="10,13,14,40,43,44"
    # second="10,13,14,40,43,44"
    # start_date=None,
    # end_date=None,
    # timezone=None,
)
async def _():
    bot = nonebot.get_bot()
    if SB_MVP != 0:
        cqm = ''
        for qq in MVP_LIST:
            cqm += '[CQ:at,qq=' + str(qq) + ']'
        if cqm != '':
            cqm += '\n'
        message = cqm + 'sbmvp马上要发了，在' + str(SB_MVP) + '线'
        send_all_group(message)


@on_command('求MVP', aliases={'求mvp', '有mvp吗'}, only_to_me=False)
async def _(session: CommandSession):
    flag = False
    for VALUE in MVP_LIST:
        if VALUE == session.event.user_id:
            await session.send('已在通知列表内')
            flag = True
            break
    if not flag:
        MVP_LIST.insert(len(MVP_LIST), session.event.user_id)
    await session.send('已添加通知列表')


@on_command('取消MVP', aliases={'取消mvp'}, only_to_me=False)
async def _(session: CommandSession):
    MVP_LIST.remove(session.event.user_id)
    await session.send('已取消mvp')

