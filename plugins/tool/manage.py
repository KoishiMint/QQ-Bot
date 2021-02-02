import nonebot
import nonebot.permission

from config import *
from nonebot import on_command, CommandSession


@nonebot.on_command('开启MVP', aliases={'开启mvp'}, permission=SUPERUSERS)
async def _(session: CommandSession):
    QQ_GROUP.insert(str(session.event.group_id))
    await session.send('已添加本群MVP功能')


@nonebot.on_command('关闭MVP', aliases={'关闭mvp'}, permission=SUPERUSERS)
async def _(session: CommandSession):
    await QQ_GROUP.remove(str(session.event.group_id))
    await session.send('已关闭本群MVP功能')
