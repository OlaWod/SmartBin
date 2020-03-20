import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

INT1 = 21
INT2 = 20
INT3 = 16
INT4 = 12

GPIO.setup(INT1,GPIO.OUT)
GPIO.setup(INT2,GPIO.OUT)
GPIO.setup(INT3,GPIO.OUT)
GPIO.setup(INT4,GPIO.OUT)

GPIO.output(INT1,GPIO.HIGH)
GPIO.output(INT2,GPIO.LOW)
GPIO.output(INT3,GPIO.HIGH)
GPIO.output(INT4,GPIO.LOW)

time.sleep(5)

GPIO.cleanup()
