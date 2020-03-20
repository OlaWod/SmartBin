import json
import os
from aip import AipSpeech



# 百度语音 API
APP_ID = '18705667'
API_KEY = 'cYBHtUrTgiKMD4LjR3dxFgSl'
SECRET_KEY = 'Mql8tU4LBQiqgLyRct6lhygDwmeLkz86'
    
client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)



# 语音转文字
def speech_to_text():
    
    with open('usersay.wav', 'rb') as f:
        audio_data = f.read()

    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1537,
    })
    print(result)
    
    if result["err_no"]==0: #成功返回
        user_text = result["result"][0]
        print("我说: " + user_text)
        return user_text
    else:                   #失败返回
        return False



# 文字转语音
def text_to_speech(ai_text):
    
    # spd：语速0-9，vol：音量0-15，per：发音人选择 0女 1男 3男 4女
    result = client.synthesis(ai_text, 'zh', 1, {
        'vol': 5, 'per': 4, 'spd': 4
    })
    
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('aisay.mp3', 'wb') as f:
            f.write(result)
        os.system('mpg123 '+'aisay.mp3')



if __name__=='__main__':    # 模块测试
    
    print(speech_to_text())
    text_to_speech('我是测试专用文字')
    
