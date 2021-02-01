import config
import nonebot


async def send_all_group(group_message):
    bot = nonebot.get_bot()
    if len(config.QQ_GROUP) > 0:
        for Group in config.QQ_GROUP:
            await bot.send_group_msg(group_id=Group, group_message=group_message)
