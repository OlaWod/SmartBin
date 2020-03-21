import snowboydecoder
import signal

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted


model = './assets/小白.pmdl'  #唤醒词，叫小白吧，因为小白样本多

signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

def temp_func():
    print('aaa')
    detector.terminate() # 结束监控热词    
    snowboydecoder.play_audio_file() # ding一声

if __name__=='__main__':    # 模块测试
    
    print('Listening... Press Ctrl+C to exit')

    detector.start(detected_callback=temp_func,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)
    print('over')
    detector.terminate()
