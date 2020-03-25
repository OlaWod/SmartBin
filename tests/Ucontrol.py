from bottle import get,post,run,request,template
import RPi.GPIO as GPIO
import time
INT1 = 21
INT2 = 20
INT3 = 16
INT4 = 12
def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(IN1,GPIO.OUT)
    GPIO.setup(IN2,GPIO.OUT)
    GPIO.setup(IN3,GPIO.OUT)
    GPIO.setup(IN4,GPIO.OUT)
# 前进
def goforward(sleep_time):
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.cleanup()
# 后退
def goback(sleep_time):
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)
    time.sleep(sleep_time)
    GPIO.cleanup()
# 左转弯
def goleft(sleep_time):
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.cleanup()
# 右转弯
def goright(sleep_time):
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.cleanup()
# 停止
def stop():
    GPIO.output(IN1,False)
    GPIO.output(IN2,False)
    GPIO.output(IN3,False)
    GPIO.output(IN4,False)
    GPIO.cleanup()

@get("/")
def index():
    return template("index")
@post("/cmd")
def cmd():
    print("按下按钮: "+request.body.read().decode())
    init()
    sleep_time = 1
    control = request.body.read().decode()
    if(control=='up'):
        goforward(sleep_time)
    elif(control=='down'):
        goback(sleep_time)
    elif(control=='left'):
        goleft(sleep_time)
    elif(control=='right'):
        goright(sleep_time)
    elif(control=='stop'):
        stop()   
    else:
        return False
