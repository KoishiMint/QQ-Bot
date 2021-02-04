from nonebot.permission import *

from nonebot import on_command, CommandSession

import config


@on_command('开启MVP', aliases={'开启mvp'}, permission=SUPERUSER)
async def _(session: CommandSession):
    if session.event.group_id not in config.QQ_GROUP:
        config.QQ_GROUP.insert(0, str(session.event.group_id))
        await session.send('已添加本群MVP功能')
    else:
        await session.send('本群已在MVP列表中')


@on_command('关闭MVP', aliases={'关闭mvp'}, permission=SUPERUSER)
async def _(session: CommandSession):
    if session.event.group_id in config.QQ_GROUP:
        config.QQ_GROUP.remove(str(session.event.group_id))
        await session.send('已关闭本群MVP功能')
    else:
        await session.send('本群未在MVP列表中')
