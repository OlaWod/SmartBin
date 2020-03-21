import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SLEEP_TIME = 1
#定义GPIO信号
INT1 = 21
INT2 = 20
INT3 = 16
INT4 = 12

#初始化
def init():
    GPIO.setup(INT1,GPIO.OUT)
    GPIO.setup(INT2,GPIO.OUT)
    GPIO.setup(INT3,GPIO.OUT)
    GPIO.setup(INT4,GPIO.OUT)

#前进
def go_forward(sleep_time):
    GPIO.output(INT1,GPIO.HIGH)
    GPIO.output(INT2,GPIO.LOW)
    GPIO.output(INT3,GPIO.HIGH)
    GPIO.output(INT4,GPIO.LOW)
    time.sleep(sleep_time)

#后退
def go_back(sleep_time):
    GPIO.output(INT2,GPIO.HIGH)
    GPIO.output(INT1,GPIO.LOW)
    GPIO.output(INT4,GPIO.HIGH)
    GPIO.output(INT3,GPIO.LOW)
    time.sleep(sleep_time)
  
#左转  
def go_left(sleep_time):
    GPIO.output(INT1,GPIO.HIGH)
    GPIO.output(INT2,GPIO.LOW)
    GPIO.output(INT3,GPIO.LOW)
    GPIO.output(INT4,GPIO.HIGH)
    time.sleep(sleep_time)

#右转
def go_right(sleep_time):
    GPIO.output(INT1,GPIO.LOW)
    GPIO.output(INT2,GPIO.HIGH)
    GPIO.output(INT3,GPIO.HIGH)
    GPIO.output(INT4,GPIO.LOW)
    time.sleep(sleep_time)

#刹车
def go_stop(sleep_time):
    GPIO.output(INT1,False)
    GPIO.output(INT2,False)
    GPIO.output(INT3,False)
    GPIO.output(INT4,False)


if __name__=='__main__':
    init()
    go_stop(1)

    go_forward(SLEEP_TIME)
    go_back(SLEEP_TIME)
    go_left(SLEEP_TIME)
    go_right(SLEEP_TIME)
    go_stop(SLEEP_TIME)

    GPIO.cleanup()
