'''
子系统自身信息：
IP:192.168.127.11
slave：11
port:5001

子系统需要检测的信息
电源电压采样 value1:05 03 07 data crc1 crc2----registerid=07   datatype=float
电源电流采样 value1:05 03 08 data crc1 crc2----registerid=08   datatype=float

'''

import threading
import zmq
import time
import socket
import datetime
import struct
import  nis_hsdd_configfile
HWM_VAL = 100000*60*31*5

HWM_VAL = 10000000

global flag_start


import threading
import time
import inspect
import ctypes


def udp_recv_zmq_send(context, port):
    # socketzmq = context.socket(zmq.PUB)
    # socketzmq.bind("tcp://115.156.162.76:6000")
    # reveiver_url = "ipc://11_Router"
    reveiver_url = "tcp://127.0.0.1:6000"

    socketzmq = context.socket(zmq.PUB)
    socketzmq.set_hwm(HWM_VAL)

    socketzmq.bind(reveiver_url)
    # time.sleep(3)


    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('127.0.0.1',10000))
    client_socket.settimeout(1)
    packagenum = 0

    count = 0
    global flag_start
    flag_start = True
    num=0
    while True:

            if flag_start:

                try:
                    b, addr = client_socket.recvfrom(1000)
                    # if (count % 10==0):
                    count = count + 1
                    print('cnt',count)

                    socketzmq.send(b)
                except socket.timeout:
                    print('Current number of Packages',count)

                    # print('守护线程,守护进程')

    print(packagenum)
    end_time_perf = time.perf_counter()
    end_time_process = time.process_time()
    print('Receiving port is: ', port)
    print('Package num:', count)
    print('receing time cost:', end_time_perf - start_time_perf)  #

    socketzmq.close()

if __name__ == '__main__':
    print('Kaishile ')
    context = zmq.Context()  # 这个上下文是真的迷，到底什么情况下要用共同的上下文，什么时候用单独的上下文，找时间测试清楚

    udp_recv_zmq_send(context,8080)





