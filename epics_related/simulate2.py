#!/usr/local/bin/python3
import socket
import struct
import crcmod
#from  dataservice.datawave_produce.waveproduce import sin_wave,triangle_wave
import random

def crccreate(b,length):
    crc16_func = crcmod.mkCrcFun(0x18005, initCrc=0xFFFF, rev=True, xorOut=0x0000)
    return crc16_func(b[0:length])
def crccheckhole(b,length):
    crc16_func = crcmod.mkCrcFun(0x18005, initCrc=0xFFFF, rev=True, xorOut=0x0000)

    return hex(crc16_func(b[0:length]))==bytesToHex(b[length],b[length+1])
def crccheck(b,length):
    print('传过来的b，和lenght',b,'   ',length)
    crc16_func = crcmod.mkCrcFun(0x18005, initCrc=0xFFFF, rev=True, xorOut=0x0000)
    return crc16_func(b[0:length]) == bytesToInt(b[length], b[length + 1])

def get_send_msgflowbytes(slave,func,register,length,data):
    if length!=4:
        pass
    else:
        # print('data',data)
        a = struct.pack('!bbbbf', slave, func, register, length, data)
        # print(len(a))
        b=struct.pack('H',crccreate(a[0:8], length=8))
        a=a + b
        # print(a)
    return a


if __name__=='__main__':


    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建套接字
    tcp_server_socket.bind(('127.0.0.1',5000))#绑定本机地址和接收端口
    tcp_server_socket.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,True)
    print('Waiting connecting')
    # tcp_server_socket.listen(1)#监听（）内为最大监听值
    # client_socket,client_addr= tcp_server_socket.accept()#建立连接（accept（无参数）
    # print('Someone has connected to this sever')

    #xsin,ysin=sin_wave(0,100,1,2,2)
    #xtri,ytri=triangle_wave(0,100,1,2,2)
    #ysin=ysin-0.5
    #ytri=10*ytri
    data=0.0

    #sinindex=0;
    #triindex=0;
    while True:
        tim
        # b =client_socket.recv(10)
        # print('receiving msg:',b)
        # if b[1]==0x03:
        #     print('we are receiving setting command',b)
        #     # client_socket.send(b)
        # elif b[2]==0x01: #正弦波产生函数
        #     slave,func,register,length=struct.unpack('!bbbb',b[0:4]) #解析传过来的二进制字节流
            #sinindex +=1
        data=random.uniform(10,11)
        print(data)
            # #此处的数据包格式由epics 的protocol文件所确定
            # msg = get_send_msgflowbytes(slave, func, register, length, data)  #构建符合要求的数据包格式
            # print('sending msg:',msg)
            # print(b)
            # client_socket.send(msg)
            #if sinindex==99:
            #    sinindex=0



