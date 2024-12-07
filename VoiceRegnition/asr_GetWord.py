import sys
import webrtcvad
import numpy as np
from mic_array import MicArray
import time

import struct
import json
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode

timer = time.time
                        
API_KEY = 'ZFvnPJZF3x0KZiC4qCf6fxjw'
SECRET_KEY = 'vdkX9H5kKncQ5ww14MoaIzakxIPHt6YN'


CUID = '123456PYTHON'
# 采样率
RATE = 16000  # 固定值

# 普通版
DEV_PID = 1537  # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有


CHANNELS = 4
VAD_FRAMES = 10     # ms
DOA_FRAMES = 3000    # ms  #origin:200

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

    result = json.loads(result_str)
    return result['access_token']

def main():
    
    vad = webrtcvad.Vad(3)

    speech_count = 0
    chunks = []
    doa_chunks = int(DOA_FRAMES / VAD_FRAMES)
    
    try:
        with MicArray(RATE, CHANNELS, RATE * VAD_FRAMES / 1000)  as mic:
            
            for chunk in mic.read_chunks():
                # Use single channel audio to detect voice activity
                if vad.is_speech(chunk[0::CHANNELS].tobytes(), RATE):
                    speech_count += 1
                
                # judge
                chunks.append(chunk)
                if len(chunks) == doa_chunks:
                    if speech_count > (doa_chunks / 2):
                        
                        frames = np.concatenate(chunks)
                        frames_bytes = b''.join(frames[0::CHANNELS])

                        # 根据音频数据的格式设置每个样本的字节数
                        sample_width = 2

                        # 计算音频数据的总字节数
                        num_samples = len(frames_bytes) // sample_width
                        num_channels = CHANNELS
                        sample_rate = RATE

                        # 构建类似wav文件头的字节数据
                        wav_header = struct.pack('<4sI4s', b'RIFF', 36 + num_samples * sample_width, b'WAVE')
                        wav_header += struct.pack('<4sI2s2sI4s', b'fmt ', 16, b'\x01\x00', b'\x01\x00', sample_rate, b'data')
                        wav_header += struct.pack('<I', num_samples * sample_width)

                        # 将wav文件头和音频数据字节流拼接起来，得到类似读取wav文件得到的二进制数据
                        speech_data = wav_header + frames_bytes
                        
                        token = fetch_token()
                        
                        length = len(speech_data)

                        params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID}
                        params_query = urlencode(params)

                        headers = {
                            'Content-Type': 'audio/' + 'wav' + '; rate=' + str(RATE),
                            'Content-Length': length
                        }
                        
                        #print("GetProcess")
                        url = ASR_URL + "?" + params_query
                        # print("url is", url)
                        # print("header is", headers)
                        # print post_data
                        req = Request(ASR_URL + "?" + params_query, speech_data, headers)

                        begin = timer()
                        f = urlopen(req)
                        result_str = f.read()
                        print("Request time cost %f" % (timer() - begin))

                        result_str = json.loads(str(result_str, 'utf-8'))
                        result_content = result_str["result"][0][:-1]
                        if result_content:
                            print('res:',result_content)
                        else:
                            print('res:None')
                        #print(result_str)
                        
                    speech_count = 0
                    chunks = []
                    
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

