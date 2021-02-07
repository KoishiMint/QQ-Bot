"""
提醒周常日常小助手
周常提醒包括：
    1.每周日之前的周常任务
    2.每周四之前的boss
日常提醒包括：
    1.每日任务
目前周常日常刷新时间均为UTC：0AM。机器人提醒时间为刷新前N小时的整点。
如果刷新时间有变化，请修改`DW_REFRESH_HOUR`（24小时制）
如果周常刷新时间有变化，请修改`W_BOSS_REMIND_DAY`与`W_QUEST_REMIND_DAY`
如果需要改变开始提醒时间（小时），请修改`DW_REM_HR_AHEAD_LIST`，请注意，该助手只能提前一天之内提醒。
如果需要改变提醒时间间隔（分钟），请修改`DW_REM_MIN_INTRVL`
"""
import datetime
import pytz

import nonebot
from nonebot.permission import SUPERUSER
from nonebot import on_command, CommandSession
from config import NICKNAME

NICKNAME = list(NICKNAME)[0]

# 提前播报小时列表。注意：必须 < 24
DW_REM_HR_AHEAD_LIST = [23, 22, 21, 20, 12, 8, 3, 1]

# 播报分钟间隔
DW_REM_MIN_INTRVL = 1

# 刷新时刻以及时区
DW_TIMEZONE = 'UTC'  # 使用UTC比较方便周常日期转换
DW_REFRESH_HOUR = 0

# 刷新周常日期，以0-6对应周一到周日，0即周一，2即周三
W_BOSS_REFRESH_DAY = 3  # 周四
W_QUEST_REFRESH_DAY = 0  # 周一


DW_GROUP_LIST = []


class DWReminder(object):
    """
    Class to remind daily/weekly routines.
    Also will report a refresh message
    """
    def __init__(self, remind_msg, refresh_msg, refresh_day_of_week=None):
        self.__remind_hour = self.__get_remind_hour()
        self.__remind_minute = f"*/{DW_REM_MIN_INTRVL}"
        self.__remind_msg = remind_msg
        self.__remind_day_of_week = self.__get_remind_day_of_week(refresh_day_of_week)

        self.__refresh_hour = DW_REFRESH_HOUR
        self.__refresh_minute = 0
        self.__refresh_day_of_week = refresh_day_of_week
        self.__refresh_msg = refresh_msg

        self.remind()
        self.refresh()

    @classmethod
    def __get_remind_day_of_week(cls, refresh_day_of_week):
        """
        返回提醒日，是刷新日前一天
        :param refresh_day_of_week:
        :return:
        """
        if not refresh_day_of_week:
            return None

        remind_day_of_week = refresh_day_of_week - 1
        if remind_day_of_week < 0:
            return remind_day_of_week + 7
        return remind_day_of_week

    @classmethod
    def __get_remind_hour(cls):
        """
        Return remind hour list, given `DW_REM_HR_AHEAD_LIST`
        :return:
        """
        remind_hour_list = [DW_REFRESH_HOUR - hr for hr in DW_REM_HR_AHEAD_LIST]
        remind_hour_list = [hr + 24 if hr < 0 else hr for hr in remind_hour_list]
        return ", ".join(str(hr) for hr in remind_hour_list)

    # 两个方便报剩余时间的帮助函数
    @classmethod
    def __get_cur_time(cls):
        """
        Get current time with given time zone
        :return:
        datetime
        """
        dw_timezone = pytz.timezone(DW_TIMEZONE)
        cur_dt = datetime.datetime.now(dw_timezone)
        return cur_dt

    @classmethod
    def __report_remaining_time_in_minute(cls):
        """
        Format current time's remaining minutes in hour/min comparing to given `DW_REFRESH_HOUR`.
        :return:
        str
        """
        cur_dt = cls.__get_cur_time()
        # Always next day
        refresh_dt = (cur_dt + datetime.timedelta(days=1)).replace(hour=DW_REFRESH_HOUR, minute=0)
        dt_diff = refresh_dt - cur_dt
        min_diff = int(dt_diff.seconds / 60)
        assert min_diff >= 0, f"Current dt{cur_dt} is not ahead of refresh dt{refresh_dt}"
        if min_diff >= 60:  # More than an hour
            hour_diff = int(min_diff // 60)
            remain_min_diff = min_diff - hour_diff * 60
            msg = f"{hour_diff}小时"
            if remain_min_diff > 0:
                msg += f"{remain_min_diff}分钟"
            return msg
        return f"{min_diff}分钟"

    def remind(self):
        """
        Create scheduled reminders job
        :return:
        """
        # Send reminder at given interval before daily refreshes
        @nonebot.scheduler.scheduled_job(
            'cron',
            hour=self.__remind_hour,
            minute=self.__remind_minute,
            day_of_week=self.__remind_day_of_week,
            timezone=DW_TIMEZONE
        )
        async def _():
            if DW_GROUP_LIST:
                bot = nonebot.get_bot()
                remain_time = self.__report_remaining_time_in_minute()
                cqm = f'{NICKNAME}提醒：离刷新还剩{remain_time}，{self.__remind_msg}。'
                for group in DW_GROUP_LIST:
                    await bot.send_group_msg(group_id=group, message=cqm)

    def refresh(self):
        """
        Create scheduled refresh job
        :return:
        """
        # Send reminder for refreshes
        @nonebot.scheduler.scheduled_job(
            'cron',
            hour=self.__refresh_hour,
            minute=self.__refresh_minute,
            day_of_week=self.__refresh_day_of_week,
            timezone=DW_TIMEZONE
        )
        async def _():
            if DW_GROUP_LIST:
                bot = nonebot.get_bot()
                cqm = f'{NICKNAME}提醒：{self.__refresh_msg}。'
                for group in DW_GROUP_LIST:
                    await bot.send_group_msg(group_id=group, message=cqm)


# Turn on/off reminder
@on_command('开启日常周常提醒', aliases={'开启日常周常'}, permission=SUPERUSER)
async def _(session: CommandSession):
    global DW_GROUP_LIST
    if session.event.group_id not in DW_GROUP_LIST:
        DW_GROUP_LIST.append(session.event.group_id)
        await session.send(f'{NICKNAME}已开启本群日常周常提醒功能')
    else:
        await session.send(f'{NICKNAME}发现本群日常周常提醒已是开启状态')


@on_command('关闭日常周常提醒', aliases={'关闭日常周常'}, permission=SUPERUSER)
async def _(session: CommandSession):
    global DW_GROUP_LIST
    if session.event.group_id in DW_GROUP_LIST:
        DW_GROUP_LIST.remove(session.event.group_id)
        await session.send(f'{NICKNAME}已关闭本群日常周常提醒功能')
    else:
        await session.send(f'{NICKNAME}发现本群日常周常提醒已是关闭状态')

daily_reminder = DWReminder(remind_msg="请大家尽快完成日常任务", refresh_msg="日常已经刷新，可以开始新的一天啦")
weekly_boss_reminder = DWReminder(remind_msg="请大家尽快完成周Boss", refresh_msg="周Boss已经刷新，可以上车带车啦",
                                  refresh_day_of_week=W_BOSS_REFRESH_DAY)
weekly_quest_reminder = DWReminder(remind_msg="请大家尽快完成周常任务", refresh_msg="周常已经刷新，可以开始新的一周啦",
                                   refresh_day_of_week=W_QUEST_REFRESH_DAY)
