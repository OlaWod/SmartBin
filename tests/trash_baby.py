import time
import os
import urllib.request
import json
from aip import AipSpeech
import speech_recognition as sr
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)# 忽略百度api连接时的报错信息。

# Baidu Speech API
APP_ID = '18705667'
API_KEY = 'cYBHtUrTgiKMD4LjR3dxFgSl'
SECRET_KEY = 'Mql8tU4LBQiqgLyRct6lhygDwmeLkz86'
    
client = AipSpeech(APP_ID,API_KEY,SECRET_KEY)

#Turing API
TURING_KEY = "06eccece6059f8ce0a1ad004a8dd2485"
API_URL = "https://api.ownthink.com/bot"




# 录音
def rec(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)

    with open("recording.wav", "wb") as f:
        f.write(audio.get_wav_data())


# 百度语音转文字
def listen():
    with open('recording.wav', 'rb') as f:
        audio_data = f.read()

    result = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1537,
    })

    print(result)
    text_input = "讲个笑话吧"
    if result["err_no"]==0: #成功返回
        text_input = result["result"][0]
        print("我说: " + text_input)
        Robot_think(text_input)
    else:   #失败返回
        results_text="你说啥"
        print("AI说: " + results_text)
        du_say(results_text)
        os.system('robot.mp3')


# 图灵处理
def Robot_think(text_input):
    req = {
        "spoken": text_input,
        "appid": TURING_KEY,
        "userid": "dad"
    }
    # print(req)
    # 将字典格式的req编码为utf8
    req = json.dumps(req).encode('utf8')
    # print(req)

    http_post = urllib.request.Request(API_URL, data=req, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(http_post)
    response_str = response.read().decode('utf8')
    # print(response_str)
    response_dic = json.loads(response_str)
    # print(response_dic)

    #intent_code = response_dic['intent']['code']
    results_text = response_dic['data']['info']['text']
    print("AI说: " + results_text)
    du_say(results_text)
    os.system('robot.mp3')

    
# 文字转语音
def du_say(results_text):
    # per 3是汉子 4是妹子，spd 是语速，vol 是音量
    # 发音人选择, 0为女声，1为男声，
    # 3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
    result = client.synthesis(results_text, 'zh', 1, {
        'vol': 5, 'per': 4, 'spd': 4
    })
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        #print(result)
        f=open('robot.mp3', 'r')
        f.close()
        with open('robot.mp3', 'wb') as f:
            #print(2333333333333)
            f.write(result)


if __name__ == '__main__':
    while True:
        rec()
        listen()
