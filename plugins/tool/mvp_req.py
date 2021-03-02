import re

import nonebot

from nonebot import on_command, CommandSession
from nonebot.permission import SUPERUSER

SB_MVP = 0
QQ_GROUP = []
MVP_LIST = {}


@on_command('sbmvp在哪里', aliases={'sb几', 'sb在哪', 'mvp几', 'sb几线', 'SB几', 'SBMVP在哪里'}, only_to_me=False)
async def _(session: CommandSession):
    if not session.state.get('initialized'):
        session.state['initialized'] = True
    global SB_MVP
    if SB_MVP == 0:
        await session.send('还没有SBMVP')
    else:
        await session.send('SBMVP在' + str(SB_MVP) + '线')


@on_command('sbmvp', aliases={'sb在', 'SB在', 'SBMVP', 'sb', 'SB'}, only_to_me=False)
async def _(session: CommandSession):
    if not session.state.get('initialized'):
        session.state['initialized'] = True

    channel = re.findall(pattern=r'\d+', string=session.current_arg_text)
    if len(channel) == 1:
        if 31 > int(channel[0]) > -1:
            global SB_MVP
            SB_MVP = int(channel[0])
            bot = nonebot.get_bot()
            cqm = '已修改mvp线路，目前在' + str(SB_MVP) + '线'
            for group in QQ_GROUP:
                await bot.send_group_msg(group_id=group, message=cqm)
        else:
            await session.send('输入的线路有误')
    else:
        pass


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
        for group in QQ_GROUP:
            for qq in MVP_LIST:
                if int(group) == int(MVP_LIST.get(qq)):
                    cqm += '[CQ:at,qq=' + str(qq) + '] '
            if cqm != '':
                cqm += '\n'
            cqm += 'sbmvp马上要发了，在' + str(SB_MVP) + '线'
            await bot.send_group_msg(group_id=group, message=cqm)
            cqm = ''


@on_command('求MVP', aliases={'求mvp', '有mvp吗'}, only_to_me=False)
async def _(session: CommandSession):
    if not session.state.get('initialized'):
        session.state['initialized'] = True

    if MVP_LIST.get(session.event.user_id) is not None:
        await session.send('已在通知列表内')
    else:
        MVP_LIST[session.event.user_id] = session.event.group_id
        await session.send('已添加通知列表')


@on_command('取消MVP', aliases={'取消mvp'}, only_to_me=False)
async def _(session: CommandSession):
    if not session.state.get('initialized'):
        session.state['initialized'] = True

    if MVP_LIST.get(session.event.user_id) is None:
        await session.send('未在通知列表内')
    else:
        MVP_LIST.pop(session.event.user_id)
        await session.send('已取消通知列表')


@on_command('MVP使用帮助', aliases={'mvp使用帮助', 'sbmvp使用帮助', 'SBMVP使用帮助'}, only_to_me=False)
async def _(session: CommandSession):
    await session.send('MVP预约使用帮助\n'
                       '使用以下文字来查看MVP在几线: sbmvp在哪里, sb几, sb在哪, mvp几, sb几线\n'
                       '使用以下文字来修改MVP在几线: sbmvp XX, sb在 XX, SBMVP XX, sb XX, SB XX\n'
                       '使用以下文字来申请让机器人每次在MVP要发之前提醒你: 求MVP, 求mvp, 有mvp吗\n'
                       '使用以下文字来取消MVP提醒: 取消MVP, 取消mvp\n'
                       '目前默认每小时13/14/43/44分的时候提醒')


@on_command('开启MVP', aliases={'开启mvp'}, permission=SUPERUSER)
async def _(session: CommandSession):
    if session.event.group_id not in QQ_GROUP:
        QQ_GROUP.insert(0, str(session.event.group_id))
        await session.send('已添加本群MVP功能')
    else:
        await session.send('本群已在MVP列表中')


@on_command('关闭MVP', aliases={'关闭mvp'}, permission=SUPERUSER)
async def _(session: CommandSession):
    if session.event.group_id in QQ_GROUP:
        QQ_GROUP.remove(str(session.event.group_id))
        await session.send('已关闭本群MVP功能')
    else:
        await session.send('本群未在MVP列表中')
