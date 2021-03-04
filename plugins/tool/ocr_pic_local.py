import hashlib
import json
import time
from urllib import request

import requests
from nonebot import on_command, CommandSession
from google_trans_new import google_translator
import pytesseract
from PIL import Image


@on_command('识别', only_to_me=False)
async def _(session: CommandSession):
    qq = str(session.event.user_id)
    pytesseract.pytesseract.tesseract_cmd = 'D://Program Files (x86)//OCR//tesseract.exe'
    mkdir('pic')
    # C://Program Files//Tesseract-OCR
    # D://Program Files (x86)//OCR
    for qq_image in session.current_arg_images:
        filename = 'pic//' + time.strftime("%Y%m%d-%H%M%S-", time.localtime()) + qq + '.jpg'
        request.urlretrieve(qq_image, filename)
        custom_oem_psm_config = r'--oem 3 --psm 6'
        parsed_text = pytesseract.image_to_string(Image.open(filename), lang='eng+kor', config=custom_oem_psm_config)
        # file = open(filename, "rb")
        # md = hashlib.md5()
        # md.update(file.read())
        # res = md.hexdigest()
        translator = google_translator()
        translated_text = translator.translate(parsed_text, lang_tgt='zh-CN')
        await session.send(message='识别结果：\n' + parsed_text + '\n翻译结果：\n' + translated_text)


@on_command('翻译', only_to_me=False)
async def _(session: CommandSession):
    original_text = session.current_arg_text
    translator = google_translator()
    translated_text = translator.translate(original_text, lang_tgt='zh-CN')
    await session.send('翻译结果\n' + translated_text)


def mkdir(path):
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("//")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    exist = os.path.exists(path)
    # 判断结果
    if not exist:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False
