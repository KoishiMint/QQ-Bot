import nonebot
from config import *
from nonebot import on_command, CommandSession


@on_command(name='添加本群', permission=SUPERUSERS)
def _(session: CommandSession):
    QQ_GROUP.insert(session.event.group_id)


@on_command(name='删除本群', permission=SUPERUSERS)
def _(session: CommandSession):
    QQ_GROUP.remove(session.event.group_id)
