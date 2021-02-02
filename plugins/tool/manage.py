import nonebot
from nonebot.permission import *

from nonebot import on_command, CommandSession

import config


@on_command('开启MVP', aliases={'开启mvp'}, permission=SUPERUSER)
async def _(session: CommandSession):
    config.QQ_GROUP.insert(0, str(session.event.group_id))
    await session.send('已添加本群MVP功能')


@on_command('关闭MVP', aliases={'关闭mvp'}, permission=SUPERUSER)
async def _(session: CommandSession):
    config.QQ_GROUP.remove(str(session.event.group_id))
    await session.send('已关闭本群MVP功能')
