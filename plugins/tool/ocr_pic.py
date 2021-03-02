import hashlib
import time
import json
from urllib import request

import requests
from nonebot import on_command, CommandSession


def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


def get_md5(url: str, qq: str):
    time_str = time.strftime("%Y%m%d-%H%M%S-", time.localtime())
    filename = 'pic/' + time_str + qq + '.jpg'
    request.urlretrieve(url, filename)
    file = open(filename, "rb")
    md = hashlib.md5()
    md.update(file.read())
    res = md.hexdigest()
    return res


@on_command('识图', only_to_me=True)
async def _(session: CommandSession):
    for qq_image in session.current_arg_images:
        ocr_text = ocr_space_url(url=qq_image)
        parsed_text = json.loads(ocr_text)['ParsedResults'][0]['ParsedText']
        # image_md5 = get_md5(qq_image, qq=str(session.event.user_id))
        await session.send(message='识别结果：\n' + parsed_text)
