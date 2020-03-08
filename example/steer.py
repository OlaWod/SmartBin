import RPi.GPIO as GPIO
import time

class Steer(object):
    def __init__(self, port):
        self.port = port
        self.fpWM = 50  # 50 Hz
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.port, GPIO.OUT)
        self.gear = GPIO.PWM(self.port,self.fpWM)
        self.gear.start(0)

    def set_degree(self,degree):
        duty = float(degree)/18 + 2.5
        self.gear.ChangeDutyCycle(duty)
        time.sleep(0.5)

    def open(self):
        self.set_degree(90)

    def close(self):
        self.set_degree(0)



if __name__=="__main__":    # 模块测试
    lid=Steer(21)
    time.sleep(2)
    lid.open()
    time.sleep(5)
    lid.close()
