'''
子系统自身信息：
IP:192.168.127.11
slave：11
port:5001

子系统需要检测的信息
电源电压采样 value1:05 03 07 data crc1 crc2----registerid=07   datatype=int
电源电流采样 value1:05 03 08 data crc1 crc2----registerid=08   datatype=float

'''
import zmq
import struct
import threading
import pymysql
import datetime
# import crcmod
import time

import socket
import struct
import nis_hsdd_configfile

mutex = threading.Lock()
import inspect
import ctypes


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")

    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    try:
        _async_raise(thread.ident, SystemExit)
    except:
        print("Already clear the thread")

        ## 关于上面的这个线程的停止过程，我们是没有办法去停止一个阻塞过程的


global flagtosave
flagtosave = False
global exp_id
exp_id = 0
global data_list
data_list = []
global flagtoreceive
flagtoreceive = False

dateymd = time.strftime("%Y-%m-%d", time.localtime())


def process_threadfunc(context):
    receiver_subaddr =  'tcp://127.0.0.1:6000'
    receiver_sub = context.socket(zmq.SUB)
    receiver_sub.setsockopt(zmq.SUBSCRIBE, b'')  # 这个时候，这个地方订阅的内容是对应的是系统的哪个 具体的chaannel id

    receiver_sub.set_hwm(10000000)
    receiver_sub.connect(receiver_subaddr)
    # receiver_sub.setsockopt(zmq.RCVTIMEO,1000)

    counter = 0
    global flagtoreceive

    flagtoreceive = True
    while True:
        if flagtoreceive:
            try:
                b = receiver_sub.recv()
                counter += 1
                print("Counter num:", counter)

                channel_id = struct.unpack('!H', b[0:2])[0]  # 2
                length = struct.unpack('!B', b[2:3])[0]  # 1
                fenmiaofu = struct.unpack('!B', b[3:4])[0]  # 1
                sec = struct.unpack('!I', b[4:8])[0]  # 4
                # print('channel id', channel_id, 'length', length, 'fenmiaoshu ', fenmiaofu, 'sestc:', sec)

                for i in range(length):
                    tmp = b[8 + i * 8:10 + 8 * (i + 1)]
                    data = struct.unpack('!f', tmp[0:4])[0]
                    ustampe = struct.unpack('!I', tmp[4:8])[0]
                    if True:
                        second = sec % 60
                        minute = (sec // 60) % 60
                        hour = (sec // 60) // 60
                        ustampe = ustampe / 1000000
            except:
                print('Current number of Packages',counter)
#



if __name__ == '__main__':
    # zeroMQ的通信协议可以采用的ipc
    context = zmq.Context()
    import threading

    # 这个时候定义一个需要订阅子系统

    # t1=threading.Thread(target=daemon_thread,args=(context,))
    # t1.start()
    process_threadfunc(context)
    '''
    由于我们的这些进程实际上切换的还算是比较频繁的，我们是否应当考虑将其写入到一个脚本中，然后采用多线程的工作而不是多进程的工作的方式，因为如果是多进程的工作的话
    导致切换过程中消耗的资源太大，实际上就不太好了哦哦、  可能还会导致整体彗星的速度变慢

    '''

