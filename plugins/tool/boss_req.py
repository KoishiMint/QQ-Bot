from nonebot import on_command, CommandSession
import re
import json

import config


@on_command('求', only_to_me=False)
async def _(session: CommandSession):
    boss = split_boss(session.current_arg_text).split(',')
    boss.remove('')
    flag = True
    if len(boss) == 0:
        flag = False
    for bosses in boss:
        boss_json = json.dumps({'qq': session.event.user_id,
                                'qq_group': session.event.group_id,
                                'boss': bosses})
        for boss_req in config.BOSS_LIST:
            if boss_json == boss_req:
                flag = False
                break
    if flag:
        config.BOSS_LIST.insert(len(config.BOSS_LIST), boss_json)
        await session.send('已成功预约' + split_boss(session.current_arg_text).replace(',', ' '))


@on_command('~', only_to_me=True)
async def _(session: CommandSession):
    boss = split_boss(session.current_arg_text).split(',')
    boss.remove('')
    location = get_location(session.current_arg_text)
    reply_list = ''
    for bosses in boss:
        print('bosses=' + bosses)
        for boss_req in config.BOSS_LIST:
            boss_json = json.loads(boss_req)
            print(boss_json)
            if boss_json['qq_group'] == session.event.group_id and boss_json['boss'] == bosses:
                reply_list += '[CQ:at,qq=' + str(boss_json['qq']) + '] '
                config.BOSS_LIST.remove(boss_req)
    await session.send(reply_list + '\n' +
                       '[CQ:at,qq=' + str(session.event.user_id) + '] 大佬开车啦\n' +
                       'BOSS:' + split_boss(session.current_arg_text).replace(',', ' ') +
                       '地点:' + location)


def get_location(args):
    channel = re.findall(pattern=r'\d+[\u4e00-\u9fa5a-zA-Z]+', string=args)
    if len(channel) == 1:
        return channel[0]
    else:
        return None


def split_boss(args):
    boss = ''
    if '三核' in args:
        boss += '三核,'
    if 'cra' in args.lower():
        boss += 'cra,'
    if '斯乌' in args or '四米' in args:
        boss += '斯乌,'
    if '大米' in args or '黛米安' in args or 'damein' in args.lower() or '四米' in args:
        boss += '大米,'
    if '路西德' in args or 'lcd' in args.lower() or 'lucid' in args.lower():
        boss += '路西德,'
    if '威尔' in args or 'will' in args.lower():
        boss += '威尔,'
    if '组航' in args:
        boss += '组航,'
    return boss