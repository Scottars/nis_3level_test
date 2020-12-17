'''
子系统自身信息：
IP:192.168.127.11
slave：11
port:5001

子系统需要检测的信息     上传速度100k/s
电源电压采样 value1:05 03 07 data crc1 crc2----registerid=07   datatype=float
电源电流采样 value1:05 03 08 data crc1 crc2----registerid=08   datatype=float

'''








import datetime


Port = 5011
#当前未采用
url = ('115.156.163.107', 5001)


#upload speed
Time_interal=0.00000   #1000k/s

import socket
import  time
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 建立连接:
# s.bind(('115.156.163.107', 6001))
import socket

# import crcmod
import time
import nis_hsdd_configfile
import socket
import  struct
def high_pricision_delay(delay_time):
    '''
    it is seconds
    :param delay_time:
    :return:
    '''
    _ = time.perf_counter_ns()+delay_time*1000000000
    while time.perf_counter_ns() < _ :
        pass

def crccreate(b,length):
    crc16_func = crcmod.mkCrcFun(0x18005, initCrc=0xFFFF, rev=True, xorOut=0x0000)
    return crc16_func(b[0:length])

# 将要发送的数据转换成的ieee 754标准
def get_send_msgflowbytes(slave,func,register,length,data):
    if length == 2:
        a = struct.pack('!bbbbh', slave, func, register, length, data)  #h 代表的是short
        # print(len(a))
        b=struct.pack('H',crccreate(a[0:6], length=6))
        a=a + b + b'xx'
    elif length==4:
        # print('data',data)
        a = struct.pack('!bbbbf', slave, func, register, length, data)
        # print(len(a))
        b=struct.pack('H',crccreate(a[0:8], length=8))
        a=a + b
            # print(a)
    return a





def level1_udp_send():
    global flag_start

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #不需要建立连接：
    # s.sendto(b'helloworld', ('192.168.100.60', 5000))

    # s  channels numdata channel1+data+us channel2+data+us ....


    msg=b''
    import random
    import datetime

    from waveproduce import sin_wave,triangle_wave

    xsin, ysin = sin_wave(start=0, zhouqi=6.28, midu=0.01, xdecimals=2, ydecimals=2)
    xtriangle, ytriangle = sin_wave(start=0, zhouqi=6.28, midu=0.01, xdecimals=2, ydecimals=2)
    datax = 0

    wholemsg_list1 = []
    wholemsg_list2 = []

    data1=0
    data2=0
    start_time = time.perf_counter()
    Time_interal = 0.015
    Time_last = 10

    for i in range(100):


        msg1 = b''
        msg2 = b''
        channelid1 = struct.pack('!H', 1)
        channelid2 = struct.pack('!H', 2)
        fenmiaocnt =struct.pack('!B', 100)
        length = struct.pack('!B', 100)
        # 将当前的时间转化成对应的sec，然后进行数据的上传
        nowtime = str(datetime.datetime.now())
        curTime = nowtime[11:19]
        us_stampe = int(nowtime[20:26])
        sec = int(curTime[0:2]) * 60 * 60 + int(curTime[3:5]) * 60 + int(curTime[6:8])
        sec_encodee = struct.pack('!I', sec)  # 4个字节
        msg1 = channelid1 + length + fenmiaocnt + sec_encodee
        msg2 = channelid2 + length + fenmiaocnt + sec_encodee
        for item in range(100):
            # nowtime = str(datetime.datetime.now())
            data1 = ysin[item]
            data2 = ytriangle[item]
            msg1 += struct.pack('!f', data1) + struct.pack('!I', us_stampe)
            msg2 += struct.pack('!f', data2) + struct.pack('!I', us_stampe)

        print(len(msg1),'  ',len(msg2))



        print('about to send the data')
        '''
          子系统需要检测的信息   采集速度1Mhz
        电源电压采样 value1:10 03 07 04  data crc1  crc2  ----registerid=07   datatype=float
        电源电流采样 value1:10 03 08 04  data crc1  crc2  ----registerid=08   datatype=float
        '''
        # msg = sec+channels+channel_data_cnt+struct.pack('!f',data)+us_stampe
        high_pricision_delay(Time_interal)

        client_socket.sendto(msg1, (nis_hsdd_configfile.hs1_udp_recv_addr,nis_hsdd_configfile.hs1_udp_recv_port))
        client_socket.sendto(msg2, (nis_hsdd_configfile.hs1_udp_recv_addr,nis_hsdd_configfile.hs1_udp_recv_port))
    end_time = time.perf_counter()



    #发送停止数据信号
    msg = b'stopstopst'
    # client_socket.send(msg)
    print('Sys','08 eg power',' 2 channels')
    print('Package nums: ',Time_last/Time_interal)
    print('Sending Speed: ',Time_interal)
    print('Sending Port: ', Port)
    print('Sending Time Cost: ',end_time-start_time)
    client_socket.close()





# 可认为是水冷系统，其会上传每10条数据，进行合并一下，然后一起上传。
# 对于这样10条数据，来说，我们应当能够保证，其采样的时间是十分准确的
# 10条通过并不是同时采样的，我们如何打上一个合适的时标呢？
def zmq_monitor_thread():
    global flag_start
    context = zmq.Context()
    monitored_zmq = context.socket(zmq.SUB)
    monitored_zmq.setsockopt(zmq.SUBSCRIBE,b'')
    monitored_zmqaddr ='tcp://192.168.100.99:7878'
    # monitored_zmq.setsockopt(zmq.IDENTITY,b'udp_11')

    monitored_zmq.connect(monitored_zmqaddr)
    # monitored_zmq.setsockopt(zmq.RCVTIMEO,2000)
    jiange=0
    while True:

        try:
            x = monitored_zmq.recv()
            if x==b'start':
                flag_start = True
                print(b'start received')
                time.sleep(1)
                udpthread = threading.Thread(target=level1_udp_send)
                udpthread.start()
        except:
            print('time out in zmq')

if __name__=='__main__':
    import zmq
    import threading

    global flag_start
    # flag_start = False
    # t1= threading.Thread(target=zmq_monitor_thread)
    # t1.start()

    level1_udp_send()

