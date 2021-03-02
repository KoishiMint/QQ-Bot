from nonebot import on_command, CommandSession
import re
import json

BOSS_LIST = []


@on_command('求', only_to_me=False)
async def _(session: CommandSession):
    if not session.state.get('initialized'):
        session.state['initialized'] = True
    boss = split_boss(session.current_arg_text).split(',')
    boss.remove('')
    flag = True
    reply = False
    if len(boss) == 0:
        flag = False
    for bosses in boss:
        boss_json = json.dumps({'qq': session.event.user_id,
                                'qq_group': session.event.group_id,
                                'boss': bosses})
        for boss_req in BOSS_LIST:
            if boss_json == boss_req:
                flag = False
                break
        if flag and json != '':
            BOSS_LIST.insert(len(BOSS_LIST), boss_json)
            reply = True
            flag = True
    if reply:
        await session.send('已成功预约' + split_boss(session.current_arg_text).replace(',', ' '))


@on_command('查看需求', only_to_me=True)
async def _(session: CommandSession):
    boss_list = {
        '组航': 0,
        'c龙': 0,
        'c扎': 0,
        '三核': 0,
        '光秀': 0,
        'cra': 0,
        'mag': 0,
        '斯乌': 0,
        '大米': 0,
        '路西德': 0,
        '威尔': 0
    }
    cqm = '目前需求的BOSS数量如下：\n'
    flag = False
    for boss_req in BOSS_LIST:
        boss_json = json.loads(boss_req)
        if boss_json['qq_group'] == session.event.group_id:
            boss_list[boss_json['boss']] += 1
            flag = True
    if flag:
        for index in boss_list:
            cqm += index + ':' + str(boss_list[index]) + '人\n'
        await session.send(message=cqm)
    else:
        await session.send(message='还没有boss需求呢')


@on_command('谁要', only_to_me=True)
async def _(session: CommandSession):
    if not session.state.get('initialized'):
        session.state['initialized'] = True
    boss = split_boss(session.current_arg_text).split(',')
    boss.remove('')
    location = get_location(session.current_arg_text)
    reply_list = ''
    for bosses in boss:
        for boss_req in BOSS_LIST:
            boss_json = json.loads(boss_req)
            if boss_json['qq_group'] == session.event.group_id and boss_json['boss'] == bosses:
                reply_list += '[CQ:at,qq=' + str(boss_json['qq']) + '] '
                BOSS_LIST.remove(boss_req)
    if reply_list != '':
        await session.send(reply_list + '\n' +
                           '[CQ:at,qq=' + str(session.event.user_id) + '] 大佬开车啦\nBOSS:' + split_boss(session.current_arg_text).replace(',', ' ') +
                           '地点:' + location)
    else:
        await session.send('[CQ:at,qq=' + str(session.event.user_id) + '] 大佬开车啦\nBOSS:' + split_boss(session.current_arg_text).replace(',', ' ') +
                           '地点:' + location)


def get_location(args):
    channel = re.findall(pattern=r'\d+[\u4e00-\u9fa5a-zA-Z]+', string=args)
    if len(channel) == 1:
        return channel[0]
    else:
        return '不知道呢'


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
    if 'c龙' in args.lower():
        boss += 'c龙,'
    if 'c扎' in args.lower():
        boss += 'c扎,'
    if 'mag' in args.lower():
        boss += 'mag,'
    if '光秀' in args.lower():
        boss += '光秀,'
    return boss


@on_command('BOSS预约使用帮助', aliases='boss预约使用帮助', only_to_me=False)
async def _(session: CommandSession):
    await session.send(
        'BOSS预约使用帮助\n'
        '使用以下文字来预约boss【求 BOSS名】\n'
        '使用以下文字来发车boss【臭臭泥谁要 BOSS名 线路地点】\n'
        '请注意【求】【臭臭泥谁要】之后都有一个空格，除线路外不能输入数字\n'
        '使用以下文字来查看当前boss需求【臭臭泥 查看需求】'    
        '目前支持的BOSS有:组航、C龙、C扎、三核、cra、mag、斯乌、大米、路西德、威尔\n'
    )
