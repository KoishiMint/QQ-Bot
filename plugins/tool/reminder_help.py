from nonebot.permission import GROUP_OWNER, GROUP_ADMIN, SUPERUSER
from nonebot import on_command, CommandSession
from config import NICKNAME

NICKNAME = list(NICKNAME)[0]


@on_command('提醒帮助', aliases={'提醒使用帮助'}, permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER)
async def _(session: CommandSession):
    msg = (f"{NICKNAME}提醒小助手使用命令：\n"
           f"Ursus:\n"
           f"\t开启564提醒：{NICKNAME} 开启564\n"
           f"\t关闭564提醒：{NICKNAME} 关闭564\n"
           f"跑旗:\n"
           f"\t开启跑旗提醒：{NICKNAME} 开启跑旗\n"
           f"\t关闭跑旗提醒：{NICKNAME} 关闭跑旗\n"
           f"日常周常:\n"
           f"\t开启日常周常提醒：{NICKNAME} 开启日常周常\n"
           f"\t关闭日常周常提醒：{NICKNAME} 关闭日常周常\n"
           )
    await session.send(msg)
