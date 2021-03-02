from nonebot import on_command, CommandSession


@on_command('帮助', only_to_me=True)
async def _(session: CommandSession):
    await session.send(
        '使用帮助\n'
        '发送MVP使用帮助来查看MVP相关指令\n'
        '发送提醒帮助来查看提醒相关指令\n'
        '发送BOSS预约使用帮助来查看BOSS预约相关指令'
    )
