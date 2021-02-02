import config
import nonebot


async def send_all_group(group_message):
    if len(config.QQ_GROUP) > 0:
        bot = nonebot.get_bot()
        for Group in config.QQ_GROUP:
            await bot.send_group_msg(group_id=Group, message=group_message)
