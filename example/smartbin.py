import wakeuptool
from light import Light
from steer import Steer
import iflytrans
import duvoice
import aibrain
import userrec
import classify

import urllib3
import time


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)# 忽略百度api连接时的报错信息。

led1 = Light(26) # LED灯1,录音时亮
led2 = Light(19) # LED灯2,AI处理时亮

def ai_work():
    
    wakeuptool.detector.terminate() # 结束监控热词
    
    wakeuptool.snowboydecoder.play_audio_file() # ding一声
    led1.set_on()    # 开灯


    # 1.录 用户语音
    state = userrec.record()
    if state == False:   # 唤醒后太久没说话
        led.set_off()
        return
    led1.set_off()
    
        
    led2.set_on()
    # 2.用户语音 转 文字
    ai_text = "你说啥"
    user_text = iflytrans.get_usertext() # 获得语音的文字结果
    #user_text = duvoice.speech_to_text()

    
    # 3.获得 AI文字
    if user_text=='':   # 录音结果有误
        print("AI说: " + ai_text)
    else:                   # 结果无误
        result = classify.get_type(user_text)  # 从话中提取垃圾种类
        
        if result==False:   # 没有说任何垃圾
            ai_text = aibrain.ai_think(user_text)   # 思知机器人回答
        else:
            lid = Steer(result[1])    # 垃圾种类对应的盖子
            lid.open()
            ai_text = result[0]+'是'+result[1]   # 回答xx是xx垃圾
            time.sleep(5)  # 打开5秒
            lid.close()
            


    # 4.AI文字 转 语音
    duvoice.text_to_speech(ai_text)
    led2.set_off()   # 关灯

    

if __name__=='__main__':
    
    while True:
        
        print('Sleeping... ')
        
        # 实时监控
        wakeuptool.detector.start(detected_callback=ai_work,  # 自定义回调函数
                                interrupt_check=wakeuptool.interrupt_callback,
                                sleep_time=0.03)
        
        #wakeuptool.detector.terminate() # 结束监控热词
        
        print('Sleep again... ')
        
