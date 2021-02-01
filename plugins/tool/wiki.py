from nonebot import on_command, CommandSession


@on_command('问', aliases=('词条', '百科',), only_to_me=True)
async def _(session: CommandSession):
    split_arg = session.current_arg_text.strip().split('答')
    if len(split_arg) == 1:
        await session.send("请使用“雪姐 问 AAA 答 BBB”来添加词条")
    else:
        tip = split_arg[0].strip()
        del split_arg[0]
        await session.send("成功添加" + tip + "\n" +
                           "内容为" + ''.join(split_arg).strip())
