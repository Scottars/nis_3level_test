'''
子系统自身信息：
IP:192.168.127.11
slave：11
port:5001

子系统需要检测的信息     上传速度100k/s
电源电压采样 value1:05 03 07 data crc1 crc2----registerid=07   datatype=float
电源电流采样 value1:05 03 08 data crc1 crc2----registerid=08   datatype=float

'''

import nis_hsdd_configfile

IP_Server='192.168.127.11'
IP_Server='115.156.162.123' #测试的时候本电脑使用的IP
IP_Server='127.0.0.1' #测试的时候本电脑使用的IP
# IP_Server='192.168.127.200' #测试

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

# 可认为是水冷系统，其会上传每10条数据，进行合并一下，然后一起上传。
# 对于这样10条数据，来说，我们应当能够保证，其采样的时间是十分准确的
# 10条通过并不是同时采样的，我们如何打上一个合适的时标呢？


if __name__=='__main__':

    localip = '192.168.100.50'
    print("we have run water  cool down in ",localip)

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


    idlist=[0x01,0x02]
    us_stampe_a = 0
    us_stampe_b = 0
    msg1 = b''
    channelid1 = idlist[0]
    channelid2 = idlist[1]
    length = 0x01
    fenmiaocnt = 0x01
    length = struct.pack('!I', 150)
    # 将当前的时间转化成对应的sec，然后进行数据的上传
    nowtime = str(datetime.datetime.now())
    curTime = nowtime[11:19]
    us_stampe = int(nowtime[20:26])
    sec = int(curTime[0:2]) * 60 * 60 + int(curTime[3:5]) * 60 + int(curTime[6:8])
    sec_encodee = struct.pack('!I', sec)  # 4个字节
    msg1 = str(channelid1).encode() + length + str(fenmiaocnt).encode() + sec_encodee
    msg2 = str(channelid2).encode() + length + str(fenmiaocnt).encode() + sec_encodee
    for item in range(150):
        # nowtime = str(datetime.datetime.now())
        data1 = ysin[datax]
        data2 = ytriangle[datax]
        data = [data1, data2]
        datax = datax + 1
        if datax == 628:
            datax = 0
        msg1 += struct.pack('!f', data[0]) + struct.pack('!I', us_stampe)
        msg2 += struct.pack('!f', data[1]) + struct.pack('!I', us_stampe)

    cnt=0
    start_time=time.perf_counter()
    Time_interal = 0.00015
    Time_last =10
    while True:
        '''
          子系统需要检测的信息   采集速度1Mhz
        电源电压采样 value1:10 03 07 04  data crc1  crc2  ----registerid=07   datatype=float
        电源电流采样 value1:10 03 08 04  data crc1  crc2  ----registerid=08   datatype=float
        '''
        # msg = sec+channels+channel_data_cnt+struct.pack('!f',data)+us_stampe

        if cnt ==100000:
            break
        high_pricision_delay(Time_interal)

        # for i in range(2):
        #     msg=b''
        #     channelid = idlist[i]
        #     length=0x01
        #     fenmiaocnt=0x01
        #     length = struct.pack('!I', 100)
        #     #将当前的时间转化成对应的sec，然后进行数据的上传
        #     nowtime = str(datetime.datetime.now())
        #     curTime = nowtime[11:19]
        #     # us_stampe = int(nowtime[20:26])
        #     sec = int(curTime[0:2])*60*60+int(curTime[3:5])*60+int(curTime[6:8])
        #     sec_encodee = struct.pack('!I', sec)  # 4个字节
        #     msg = str(channelid).encode()+length  + str(fenmiaocnt).encode() + sec_encodee
        #     for item in range(100):
        #         # nowtime = str(datetime.datetime.now())
        #         if i == 0:
        #             us_stampe =us_stampe_a
        #             us_stampe_a += 1
        #         elif i==1:
        #             us_stampe = us_stampe_b
        #             us_stampe_b += 1
        #         if us_stampe == 1000000:
        #             us_stampe = 0
        #         data1 = ysin[datax]
        #         data2 = ytriangle[datax]
        #         data = [data1, data2]
        #         datax = datax + 1
        #         if datax == 628:
        #             datax = 0
        #         msg += struct.pack('!f',data[i])+struct.pack('!I',us_stampe)

        client_socket.sendto(msg1, (nis_hsdd_configfile.level_2_07_udp_rcv_addr,nis_hsdd_configfile.level_2_07_udp_rcv_port))
        client_socket.sendto(msg2, (nis_hsdd_configfile.level_2_07_udp_rcv_addr,nis_hsdd_configfile.level_2_07_udp_rcv_port))
        cnt+=1

    end_time = time.perf_counter()



    #发送停止数据信号
    msg = b'stopstopst'
    # client_socket.send(msg)
    print('Sys:','07 pg power','2 channels')
    print('Package nums:',Time_last/Time_interal)
    print('Sending Speed:',Time_interal)
    print('Sending Port: ', Port)
    print('Sending Time Cost: ',end_time-start_time)
    client_socket.close()


