#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import thread
import serial
import socket
import time
import threading
from threading import Thread
import os
import socket,fcntl,struct
import signal
import atexit
atexit.register(GPIO.cleanup)
GPIO.setmode(GPIO.BOARD)
ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)
data=''
SLEEP_TIME=0.1
#定义GPIO信号
INT1=11
INT2=12
INT3=13
INT4=15
INT_CHAOSHENG_TRI=3
INT_CHAOSHENG_ECHO=5
CHAOSHENG_VALUE=-1
flag_chao=[0]
#定义角度
jiaodu=0
#i=0
GPIO.setup(INT_CHAOSHENG_TRI,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(INT_CHAOSHENG_ECHO,GPIO.IN)
GPIO.setup(38,GPIO.OUT,initial=False)
p1=GPIO.PWM(38,50)
GPIO.setup(40,GPIO.OUT,initial=False)
p2=GPIO.PWM(40,50)
p1.start(0)
p2.start(0)
def print_time(threadName,delay,temp_var):
    count=0
    while count <5 and temp_var[0]==1:
        if(temp_var[0]==1):
            temp_distance1=checkdist()
            temp_distance2=checkdist()
            temp_distance3=checkdist()
            temp_distance4=checkdist()
            temp_distance5=checkdist()
            total_distance=temp_distance1+temp_distance2+temp_distance3+temp_distance4+temp_distance5
            temp_distance=(total_distance)/5.0
            #print "超声波测定距离为:%f"%temp_distance
            if (temp_distance<=0.3 ):
		go_back(0.5)
		go_left(0.5)
                go_stop(SLEEP_TIME)
                print "障碍物太近，已调整方向"

#获取ip
def get_ip(ifname):
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))[20:24])

#tcp连接
def tcplink(sock,addr):
		sock.send('欢迎使用观月堂小车系统！')
		i=0
		while True:
			data=sock.recv(1024)
			time.sleep(0.1)
			if data=='exit' or not data:
				break
			#sock.send('%s!'%data)
                        if data=='2':
                            flag_chao[0]=1
                            thread.start_new_thread(print_time,("Thread-1",0.1,flag_chao))
                            go_forward(SLEEP_TIME)
                            print "前进"
                        elif data=='5':
                            flag_chao[0]=0
                            go_back(SLEEP_TIME)
                            print "后退"
                        elif data=='4':
                            flag_chao[0]=0
                            go_left(SLEEP_TIME)
                            print "左转"
                        elif data=='6':
                            flag_chao[0]=0
                            go_right(SLEEP_TIME)
                            print "右转"
                        elif data=='1':
                            flag_chao[0]=0
                            go_stop(SLEEP_TIME)
                            print "刹车"
                        elif data=='a':
                            i=(i+10)%180
                            p1.ChangeDutyCycle(2.5+10*i/180)
                            time.sleep(0.02)
                            p1.ChangeDutyCycle(0)
                            time.sleep(0.2)
                        elif data=='b':
                            i=(i-10)%180
                            p1.ChangeDutyCycle(2.5+10*i/180)
                            time.sleep(0.02)
                            p1.ChangeDutyCycle(0)
                            time.sleep(0.2)
                        elif data=='c':
                            i=(i+10)%180
                            p2.ChangeDutyCycle(2.5+10*i/180)
                            time.sleep(0.02)
                            p2.ChangeDutyCycle(0)
                            time.sleep(0.2)
                        elif data=='d':
                            i=(i-10)%180
                            p2.ChangeDutyCycle(2.5+10*i/180)
                            time.sleep(0.02)
                            p2.ChangeDutyCycle(0)
                            time.sleep(0.2)
			else:
			    pass
		sock.close()
		print '来自 %s:%s 的连接已中断.'%addr
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#IP连接('192.168.0.101',9999)
my_ip=get_ip('wlan0')
s.bind((my_ip,9999))
s.listen(5)
def checkdist():
    GPIO.output(INT_CHAOSHENG_TRI,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(INT_CHAOSHENG_TRI,GPIO.LOW)
    while not GPIO.input(INT_CHAOSHENG_ECHO):
        pass
    t1=time.time()
    while GPIO.input(INT_CHAOSHENG_ECHO):
        pass
    t2=time.time()
    return (t2-t1)*340/2

def recv(serial):
    while True:
        data=serial.read()
        if data=='':
            continue
        else:
            break
        sleep(0.02)
        serial.flushInput()
    return data

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

init();
go_stop(1)
i=0
try:
    while True:
        i=0
	#thread.start_new_thread(print_time,("Thread-1",0.1,flag_chao))
        sock,addr=s.accept()
        t=threading.Thread(target=tcplink,args=(sock,addr))
	#print "i:%d"%i
        i=i+1
        t.start()
except KeyboardInterrupt:
    sock.close()
    s.close()
    ser.close();
    GPIO.cleanup()
