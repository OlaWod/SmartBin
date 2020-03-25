#coding=utf8
 
import struct, socket, sys
import hashlib
import threading, random
import time
from base64 import b64encode, b64decode
import RPi.GPIO as GPIO
import sys 
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
p=GPIO.PWM(17,600)
p_pin =35
p.start(p_pin)
####  定义Car类
class Car(object):
    def __init__(self):
 
        self.inx_pin = [19,26,5,6]
####  self.inx_pin是控制端in的pin
        self.RightAhead_pin = self.inx_pin[0]
        self.LeftAhead_pin = self.inx_pin[1]
        self.RightBack_pin = self.inx_pin[2]
        self.LeftBack_pin = self.inx_pin[3]
####  分别是右轮前进，左轮前进，右轮退后，左轮退后的pin
        self.RightP_pin=17
        self.LeftP_pin =27 
        self.setup()
       
 
####  setup函数初始化端口
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
####  初始化使能端pin，设置成高电平
        pin = None
        for pin in self.inx_pin:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin,GPIO.LOW)
####  初始化控制端pin，设置成低电平
        print ("setup ena enb pin over")
          
 
####  fornt函数，小车前进
    def front(self):
        self.setup()
        GPIO.output(self.RightAhead_pin,GPIO.HIGH)
        GPIO.output(self.LeftAhead_pin,GPIO.HIGH)
 
####  leftFront函数，小车左拐弯
    def leftFront(self):
        self.setup()
        GPIO.output(self.RightAhead_pin,GPIO.HIGH)
 
####  rightFront函数，小车右拐弯
    def rightFront(self):
        self.setup()
        GPIO.output(self.LeftAhead_pin,GPIO.HIGH)
 
####  rear函数，小车后退
    def rear(self):
        self.setup()
        GPIO.output(self.RightBack_pin,GPIO.HIGH)
        GPIO.output(self.LeftBack_pin,GPIO.HIGH)
 
####  leftRear函数，小车左退
    def leftRear(self):
        self.setup()
        GPIO.output(self.RightBack_pin,GPIO.HIGH)
 
####  rightRear函数，小车右退
    def rightRear(self):
        self.setup()
        GPIO.output(self.LeftBack_pin,GPIO.HIGH)
 
       
        
####  定义main主函数
def main(status):
    
    car = Car()
 
    if status == "front":
        car.front()
    elif status == "leftFront":
        car.leftFront()
    elif status == "rightFront":
        car.rightFront()
    elif status == "rear":
        car.rear()
    elif status == "leftRear":
        car.leftRear()
    elif status == "rightRear":
        car.rightRear()
    elif status == "stop":
        car.setup()      
        #p.stop()
    elif status == "q1":
        p.ChangeDutyCycle(35)
    elif status == "q2":
        p.ChangeDutyCycle(50)
    elif status == "q3":
        p.ChangeDutyCycle(75)
    elif status == "q4":
        p.ChangeDutyCycle(90)
    elif status == "q5":
        p.ChangeDutyCycle(100)
 
 
 
##socket
connectionlist = {}
 
def decode(data):
    if not len(data):
        return False
 
    # 用数据包的第二个字节，与127作与位运算，拿到前七位。
    length = data[1] & 127
 
    # 这七位在数据头部分成为payload，如果payload等于126，就要再扩展2个字节。
    # 如果等于127，就要再扩展8个字节。
    # 如果小于等于125，那它就占这一个字节。
    if length == 126:
        extend_payload_len = data[2:4]
        mask = data[4:8]
        decoded = data[8:]
    elif length == 127:
        extend_payload_len = data[2:10]
        mask = data[10:14]
        decoded = data[14:]
    else:
        extend_payload_len = None
        mask = data[2:6]
        decoded = data[6:]
    
    byte_list = bytearray()
 
    print(mask)
    print(decoded)
 
    # 当payload确定之后，再往后数4个字节，这4个字节成为masking key，再之后的内容就是接收到的数据部分。
    # 数据部分的每一字节都要和masking key作异或位运算，得出来的结果就是真实的数据内容。
    for i in range(len(decoded)):
        chunk = decoded[i] ^ mask[i % 4]
        byte_list.append(chunk)
    
    new_str = str(byte_list, encoding="utf-8")
    print(new_str)
    return new_str
 
def encode(data):  
    data=str.encode(data)
    head = b'\x81'
 
    if len(data) < 126:
        head += struct.pack('B', len(data))
    elif len(data) <= 0xFFFF:
        head += struct.pack('!BH', 126, len(data))
    else:
        head += struct.pack('!BQ', 127, len(data))
    return head+data
                
def sendMessage(message):
    global connectionlist
    for connection in connectionlist.values():
        connection.send(encode(message))
 
def deleteconnection(item):
    global connectionlist
    del connectionlist['connection'+item]
 
class WebSocket(threading.Thread):
 
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
 
    def __init__(self,conn,index,name,remote, path="/"):
        threading.Thread.__init__(self)
        self.conn = conn
        self.index = index
        self.name = name
        self.remote = remote
        self.path = path
        self.buffer = ""     
    def run(self):
        print('Socket%s Start!' % self.index)
        headers = {}
        self.handshaken = False
 
        while True:
          try: 
            if self.handshaken == False:
                print ('Socket%s Start Handshaken with %s!' % (self.index,self.remote))
                self.buffer += bytes.decode(self.conn.recv(1024))
 
                if self.buffer.find('\r\n\r\n') != -1:
                    header, data = self.buffer.split('\r\n\r\n', 1)
                    for line in header.split("\r\n")[1:]:
                        key, value = line.split(": ", 1)
                        headers[key] = value
 
                    headers["Location"] = ("ws://%s%s" %(headers["Host"], self.path))
                    key = headers['Sec-WebSocket-Key']
                    token = b64encode(hashlib.sha1(str.encode(str(key + self.GUID))).digest())
 
                    handshake="HTTP/1.1 101 Switching Protocols\r\n"\
                        "Upgrade: websocket\r\n"\
                        "Connection: Upgrade\r\n"\
                        "Sec-WebSocket-Accept: "+bytes.decode(token)+"\r\n"\
                        "WebSocket-Origin: "+str(headers["Origin"])+"\r\n"\
                        "WebSocket-Location: "+str(headers["Location"])+"\r\n\r\n"
                    
                    self.conn.send(str.encode(str(handshake)))
                    self.handshaken = True  
                    print('Socket%s Handshaken with %s success!' %(self.index, self.remote))
                    sendMessage('Welcome, ' + self.name + ' !')
 
            else:
                msg = decode(self.conn.recv(1024))
                main(msg)
                if msg == 'quit':
                    print ('Socket%s Logout!' % (self.index))
                    nowTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
                    sendMessage('%s %s say: %s' % (nowTime, self.remote, self.name+' Logout'))                  
                    deleteconnection(str(self.index))
                    self.conn.close()
                    break
                else:
                    #print('Socket%s Got msg:%s from %s!' % (self.index, msg, self.remote))
                    nowTime = time.strftime('%H:%M:%S',time.localtime(time.time()))
                    sendMessage('%s %s say: %s' % (nowTime, self.remote, msg))       
                
            self.buffer = ""
          except Exception as e:
            self.conn.close()
 
class WebSocketServer(object):
    def __init__(self):
        self.socket = None
    def begin(self):
        print( 'WebSocketServer Start!')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("192.168.0.104", 8081))
        self.socket.listen(50)
 
        global connectionlist
 
        i = 0
        while True:
            connection, address = self.socket.accept()
 
            username=address[0]     
            newSocket = WebSocket(connection,i,username,address)
            newSocket.start()
            connectionlist['connection'+str(i)]=connection
            i = i + 1
 
if __name__ == "__main__":
    server = WebSocketServer()
    server.begin()

    
