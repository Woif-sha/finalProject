# coding=utf-8

import json
import time
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode

timer = time.time

API_KEY = 'ZFvnPJZF3x0KZiC4qCf6fxjw'
SECRET_KEY = 'vdkX9H5kKncQ5ww14MoaIzakxIPHt6YN'

# 需要识别的文件
AUDIO_FILE = '1-1.wav'  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
# 文件格式
FORMAT = AUDIO_FILE[-3:]  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式

CUID = '123456PYTHON'
# 采样率
RATE = 16000  # 固定值

# 普通版
DEV_PID = 1537  # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有


# 极速版
class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    f = urlopen(req)
    result_str = f.read().decode()

    # print("str:",result_str)
    result = json.loads(result_str)
    # print("res:",result)
    if 'access_token' in result.keys() and 'scope' in result.keys():
        # print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']


"""  TOKEN end """

if __name__ == '__main__':
    token = fetch_token()
    speech_data = []
    with open(AUDIO_FILE, 'rb') as speech_file:
        speech_data = speech_file.read()
    # print(speech_data)
    length = len(speech_data)

    params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID}
    params_query = urlencode(params)

    headers = {
        'Content-Type': 'audio/' + FORMAT + '; rate=' + str(RATE),
        'Content-Length': length
    }

    url = ASR_URL + "?" + params_query
    # print("url is", url)
    # print("header is", headers)
    # print post_data
    req = Request(ASR_URL + "?" + params_query, speech_data, headers)

    begin = timer()
    f = urlopen(req)
    result_str = f.read()
    print("Request time cost %f" % (timer() - begin))

    result_str = str(result_str, 'utf-8')
    print(result_str)
    # with open("result.txt", "w") as of:
    #     of.write(result_str)