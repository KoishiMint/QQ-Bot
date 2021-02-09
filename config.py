from datetime import timedelta
from typing import Collection, Union, Iterable, Pattern, Optional, Dict, Any
from nonebot.typing import Expression_T

# bot自带的配置内容
NICKNAME = {'臭臭泥'}
COMMAND_START = {''}

API_ROOT: str = ''
ACCESS_TOKEN: str = ''
SECRET: str = ''
HOST: str = '0.0.0.0'
PORT: int = 8074
DEBUG: bool = False

SUPERUSERS: Collection[int] = {1820534362, 675052968}

COMMAND_SEP: Iterable[Union[str, Pattern]] = {'/', '.'}

SESSION_EXPIRE_TIMEOUT: Optional[timedelta] = timedelta(minutes=5)
SESSION_RUN_TIMEOUT: Optional[timedelta] = None
SESSION_RUNNING_EXPRESSION: Expression_T = '您有命令正在执行，请稍后再试'

SHORT_MESSAGE_MAX_LENGTH: int = 50

DEFAULT_VALIDATION_FAILURE_EXPRESSION: Expression_T = '您的输入不符合要求，请重新输入'
MAX_VALIDATION_FAILURES: int = 3
TOO_MANY_VALIDATION_FAILURES_EXPRESSION: Expression_T = \
    '您输入错误太多次啦，如需重试，请重新触发本功能'

SESSION_CANCEL_EXPRESSION: Expression_T = '好的'

APSCHEDULER_CONFIG: Dict[str, Any] = {'apscheduler.timezone': 'Asia/Shanghai'}

__all__ = [
    'API_ROOT',
    'ACCESS_TOKEN',
    'SECRET',
    'HOST',
    'PORT',
    'DEBUG',
    'SUPERUSERS',
    'NICKNAME',
    'COMMAND_START',
    'COMMAND_SEP',
    'SESSION_EXPIRE_TIMEOUT',
    'SESSION_RUN_TIMEOUT',
    'SESSION_RUNNING_EXPRESSION',
    'SHORT_MESSAGE_MAX_LENGTH',
    'DEFAULT_VALIDATION_FAILURE_EXPRESSION',
    'MAX_VALIDATION_FAILURES',
    'TOO_MANY_VALIDATION_FAILURES_EXPRESSION',
    'SESSION_CANCEL_EXPRESSION',
    'APSCHEDULER_CONFIG',
    'QQ_GROUP',
    'MVP_LIST',
    'BOSS_LIST'
]
