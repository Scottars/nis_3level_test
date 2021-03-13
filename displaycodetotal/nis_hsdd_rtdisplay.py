#-*-coding:utf-8-*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import os,signal,sys
from pyqtgraph.Qt import QtGui,QtCore, USE_PYSIDE, USE_PYQT5,QtWidgets
import  multiprocessing
import  numpy as np
import struct
import nis_hsdd

import  pyqtgraph as pg
import pyqtgraph.exporters
from pyqtgraph.ptime import time
# 声明一个应用程序
app = QtGui.QApplication([])
from displaycodetotal import nis_hsdd_configfile


import time
import  zmq
import threading
global data_pgpowerx,data_pgpowey,data_receive_flag_02,data_receive_flag_11
data_receive_flag_02 = False
data_receive_flag_11 = False
data_pgpowerx=[]
data_pgpowery=[]

global savingprogress11value
savingprogress11value=0

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
    # try:
    _async_raise(thread.ident, SystemExit)
    # except "invalid thread id":
    #     print("Already clear the thread")


class ChildDialogWin(QDialog,nis_hsdd.Ui_Dialog):
    def __init__(self):
        super(ChildDialogWin,self).__init__()
        #
        self.setupUi(self)
        self.setWindowTitle("Real Time Display GUI")
        self.setMinimumSize(0,0)



        print('we are in init')

        self.datadensity= 100



        self.figure_init()
        self.button_init()
        self.start_total()
        # self.start_water()
    def button_init(self):
        self.pushButton_58.clicked.connect(self.SetDataDensity)
        self.pushButton_48.clicked.connect(self.StartUpdate)
        self.pushButton_43.clicked.connect(self.StopUpdate)
        self.pushButton_49.clicked.connect(self.ClearUpdate)
        self.pushButton_47.clicked.connect(self.ExportData)
        self.pushButton_46.clicked.connect(self.ExportFigure)



    def figure_init(self):
        #初始化 所有的figure

        self.p_gassupply1 = self.graphicsView_14
        self.p_gassupply2 = self.graphicsView_15


        self.p_rfpower1 = self.graphicsView_19
        self.p_rfpower2 = self.graphicsView_20


        self.p_pgpower1 = self.graphicsView_23
        self.p_pgpower2 = self.graphicsView_24

        self.p_egpower1 = self.graphicsView_25
        self.p_egpower2 = self.graphicsView_26
        self.p_egpower3 = self.graphicsView_27


        self.p_gassupply1.setDownsampling(mode='subsample')
        self.p_gassupply2.setDownsampling(mode='subsample')

        self.p_rfpower1.setDownsampling(mode='subsample')
        self.p_rfpower2.setDownsampling(mode='subsample')

        self.p_pgpower1.setDownsampling(mode='subsample')
        self.p_pgpower2.setDownsampling(mode='subsample')

        self.p_egpower1.setDownsampling(mode='subsample')
        self.p_egpower2.setDownsampling(mode='subsample')
        self.p_egpower3.setDownsampling(mode='subsample')



        self.p_gassupply1.setClipToView(True)
        self.p_gassupply2.setClipToView(True)

        self.p_rfpower1.setClipToView(True)
        self.p_rfpower2.setClipToView(True)

        self.p_pgpower1.setClipToView(True)
        self.p_pgpower2.setClipToView(True)

        self.p_egpower1.setClipToView(True)
        self.p_egpower2.setClipToView(True)
        self.p_egpower3.setClipToView(True)

        self.p_gassupply1.setLabel("left", "value", units='L/min')
        self.p_gassupply1.setLabel("bottom", "Timestamp", units='s')
        self.p_gassupply1.setTitle('CDG025D Pressure')

        self.p_gassupply2.setLabel("left", "value", units='L/min',)
        self.p_gassupply2.setLabel("bottom", "Timestamp", units='s')
        self.p_gassupply2.setTitle('Un Userd')



        self.p_rfpower1.setLabel("left", "value", units='W')
        self.p_rfpower1.setLabel("bottom", "Timestamp", units='s')
        self.p_rfpower1.setTitle('Incident power')

        self.p_rfpower2.setLabel("left", "value", units='W',)
        self.p_rfpower2.setLabel("bottom", "Timestamp", units='s')
        self.p_rfpower2.setTitle('Reflected power')


        self.p_pgpower1.setLabel("left", "value", units='V')
        self.p_pgpower1.setLabel("bottom", "Timestamp", units='s')
        self.p_pgpower1.setTitle('Accelerator Power Voltage')

        self.p_pgpower2.setLabel("left", "value", units='V')
        self.p_pgpower2.setLabel("bottom", "Timestamp", units='s')
        self.p_pgpower2.setTitle('Leading Out Power Voltage')

        self.p_egpower1.setLabel("left", "Current", units='mA')
        self.p_egpower1.setLabel("bottom", "Timestamp", units='s')
        self.p_egpower1.setTitle('GG-Board Current I1')

        self.p_egpower2.setLabel("left", "Current", units='mA')
        self.p_egpower2.setLabel("bottom", "Timestamp", units='s')
        self.p_egpower2.setTitle('HeatMeter I2')


        self.p_egpower3.setLabel("left", "Current", units='mA')
        self.p_egpower3.setLabel("bottom", "Times`tamp", units='s')
        self.p_egpower3.setTitle('PG Power Current')


        self.p_gassupply1.setBackground('w')
        self.p_gassupply2.setBackground('w')

        self.p_rfpower1.setBackground('w')
        self.p_rfpower2.setBackground('w')


        self.p_pgpower1.setBackground('w')
        self.p_pgpower2.setBackground('w')
        # self.p2.setBackground('r')

        self.p_egpower1.setBackground('w')
        self.p_egpower2.setBackground('w')
        self.p_egpower3.setBackground('w')

        # self.curve_gassupply1 = self.p_gassupply1.plot(symbol = 'o', symbolSize = 4)
        # self.curve_gassupply2 = self.p_gassupply2.plot(symbol = 'o', symbolSize = 4)
        #
        # self.curve_rfpower1 = self.p_rfpower1.plot(symbol = 'o', symbolSize = 4)
        # self.curve_rfpower2 = self.p_rfpower2.plot(symbol = 'o', symbolSize = 4)
        #
        # self.curve_pgpower1 = self.p_pgpower1.plot(symbol = 'o', symbolSize = 4)
        # self.curve_pgpower2 = self.p_pgpower2.plot(symbol = 'o', symbolSize = 4)
        #
        # self.curve_egpower1 = self.p_egpower1.plot(symbol = 'o', symbolSize = 4)
        # self.curve_egpower2 = self.p_egpower2.plot(symbol = 'o', symbolSize = 4)
        # self.curve_egpower3 = self.p_egpower3.plot(symbol = 'o', symbolSize = 4)


        self.curve_gassupply1 = self.p_gassupply1.plot(pen=(0, 0, 0))
        self.curve_gassupply2 = self.p_gassupply2.plot(pen=(0, 0, 0))

        self.curve_rfpower1 = self.p_rfpower1.plot(pen=(0, 0, 0))
        self.curve_rfpower2 = self.p_rfpower2.plot(pen=(0, 0, 0))

        self.curve_pgpower1 = self.p_pgpower1.plot(pen=(0, 0, 0))
        self.curve_pgpower2 = self.p_pgpower2.plot(pen=(0, 0, 0))

        self.curve_egpower1 = self.p_egpower1.plot(pen=(0, 0, 0))
        self.curve_egpower2 = self.p_egpower2.plot(pen=(0, 0, 0))
        self.curve_egpower3 = self.p_egpower3.plot(pen=(0, 0, 0))


        self.gassupply1_x = []
        self.gassupply1_y = []
        self.gassupply2_x = []
        self.gassupply2_y = []

        self.rfpower1_x = []
        self.rfpower1_y = []
        self.rfpower2_x = []
        self.rfpower2_y = []


        self.pgpower1_x = []
        self.pgpower1_y = []
        self.pgpower2_x = []
        self.pgpower2_y = []


        self.egpower1_x = []
        self.egpower1_y = []
        self.egpower2_x = []
        self.egpower2_y = []
        self.egpower3_x = []
        self.egpower3_y = []

        self.flag_total = True
        self.fresh_interval = 100


    def start_total(self):
        print('start gas supply')
        self.timer_total = QtCore.QTimer()
        self.timer_total.timeout.connect(self.dis_total)
        self.timer_total.start(self.fresh_interval)  # 这个是


        self.sub_gassupply_thread = threading.Thread(target=self.sub_gassupply)
        self.sub_gassupply_thread.start()


        self.sub_rfpower_thread = threading.Thread(target=self.sub_rfpower)
        self.sub_rfpower_thread.start()

        self.sub_pgpower_thread = threading.Thread(target=self.sub_pgpower)
        self.sub_pgpower_thread.start()


        self.sub_egpowerhs1_1_2_thread = threading.Thread(target=self.sub_egpowerhs1_1_2)
        self.sub_egpowerhs1_1_2_thread.start()

        self.sub_egpowerhs3_6_thread = threading.Thread(target=self.sub_egpowerhs3_6)
        self.sub_egpowerhs3_6_thread.start()

    def stop_total(self):
        print('stop gas supply ')

        self.flag_total = False
        time.sleep(1)
        stop_thread(self.sub_gassupply_thread)
        stop_thread(self.sub_rfpower_thread)
        stop_thread(self.sub_pgpower_thread)
        stop_thread(self.sub_egpowerhs1_1_2_thread)
        stop_thread(self.sub_egpowerhs3_6)

        self.timer_total.stop()

    def sub_gassupply(self):
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'\x00\x09')  # 仅仅订阅第9个通道
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.hs5_sub_addr   # 此时最好下位机就不上传第二个通道的数据
        zmqsub.setsockopt(zmq.RCVTIMEO, 500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_total = True

        first_package = 10
        last_sec = -1
        zmqsub.connect(subaddr)
        while True:
            if self.flag_total:
                try:
                    b = zmqsub.recv()
                    if first_package == 0:
                        first_package = first_package - 1

                        continue
                    else:
                        pass
                except:
                    first_package == 10
                    continue
                ####
                channel_id = struct.unpack('!H', b[0:2])[0]  # 2
                length = struct.unpack('!B', b[2:3])[0]  # 1
                fenmiaohao = struct.unpack('!B', b[3:4])[0]  # 1
                sec = struct.unpack('!I', b[4:8])[0]  # 4
                if last_sec > sec:
                    break
                else:
                    last_sec = sec
                if fenmiaohao == 100:

                    for i in range(0, length, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stampe = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stampe / 1000000, 6)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 9:
                            self.gassupply1_x.append(x)
                            self.gassupply1_y.append(data)
                        elif channel_id == 10:
                            self.gassupply2_x.append(x)
                            self.gassupply2_y.append(data)

                else:

                    for i in range(0, fenmiaohao, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stamp / 1000000, 6)
                        # print("data:",data,"x:",x)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 9:
                            self.gassupply1_x.append(x)
                            self.gassupply1_y.append(data)
                        elif channel_id == 10:
                            self.gassupply2_x.append(x)
                            self.gassupply2_y.append(data)

                    sec = sec+ 1
                    for i in range(fenmiaohao, length, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stamp / 1000000, 6)

                        # 这个地方完全可以选择二维数据
                        if channel_id == 9:
                            self.gassupply1_x.append(x)
                            self.gassupply1_y.append(data)
                        elif channel_id == 10:
                            self.gassupply2_x.append(x)
                            self.gassupply2_y.append(data)
                print('sub gas suply')

    def sub_rfpower(self):
        print('in sub rf power')
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.hs4_sub_addr
        zmqsub.setsockopt(zmq.RCVTIMEO, 500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_total = True

        first_package = 10
        last_sec = -1

        zmqsub.connect(subaddr)
        while True:
            if self.flag_total:
                try:
                    b = zmqsub.recv()
                    if first_package == 0:
                        first_package = first_package - 1

                        continue
                    else:
                        pass
                except:
                    first_package == 20
                    continue

                ####
                channel_id = struct.unpack('!H', b[0:2])[0]  # 2
                length = struct.unpack('!B', b[2:3])[0]  # 1
                fenmiaohao = struct.unpack('!B', b[3:4])[0]  # 1
                sec = struct.unpack('!I', b[4:8])[0]  # 4
                if last_sec > sec:
                    break
                else:
                    last_sec = sec
                if fenmiaohao == 100:

                    for i in range(0, length, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stampe = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stampe / 1000000, 6)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 7:
                            self.rfpower1_x.append(x)
                            self.rfpower1_y.append(data)
                        elif channel_id == 8:
                            self.rfpower2_x.append(x)
                            self.rfpower2_y.append(data)

                else:

                    for i in range(0, fenmiaohao, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stamp / 1000000, 6)
                        # print("data:",data,"x:",x)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 7:
                            self.rfpower1_x.append(x)
                            self.rfpower1_y.append(data)
                        elif channel_id == 8:
                            self.rfpower2_x.append(x)
                            self.rfpower2_y.append(data)

                    sec = sec+ 1
                    for i in range(fenmiaohao, length, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stamp / 1000000, 6)
                        # print("data:",data,"x:",x)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 7:
                            self.rfpower1_x.append(x)
                            self.rfpower1_y.append(data)
                        elif channel_id == 8:
                            self.rfpower2_x.append(x)
                            self.rfpower2_y.append(data)
                print('in rf sub addr ')

    def sub_pgpower(self):  # 选择hs2、选3，4 通道，
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.hs2_sub_addr
        zmqsub.setsockopt(zmq.RCVTIMEO, 500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_total = True

        first_package = 10
        last_sec = -1

        zmqsub.connect(subaddr)
        while True:
            if self.flag_total:
                try:
                    b = zmqsub.recv()
                    if first_package == 0:
                        first_package = first_package - 1

                        continue
                    else:
                        pass
                except:
                    first_package == 10
                    continue
                ####
                channel_id = struct.unpack('!H', b[0:2])[0]  # 2
                length = struct.unpack('!B', b[2:3])[0]  # 1
                fenmiaohao = struct.unpack('!B', b[3:4])[0]  # 1
                sec = struct.unpack('!I', b[4:8])[0]  # 4
                # print('length:',length)
                if last_sec>sec :
                    break
                else:
                    last_sec = sec


                if fenmiaohao == 100:

                    for i in range(0, length, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stampe = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stampe / 1000000, 6)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 3:
                            self.pgpower1_x.append(x)
                            self.pgpower1_y.append(data)
                        elif channel_id == 4:
                            self.pgpower2_x.append(x)
                            self.pgpower2_y.append(data)

                else:

                    for i in range(0, fenmiaohao, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stamp / 1000000, 6)
                        # print("data:",data,"x:",x)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 3:
                            self.pgpower1_x.append(x)
                            self.pgpower1_y.append(data)
                        elif channel_id == 4:
                            self.pgpower2_x.append(x)
                            self.pgpower2_y.append(data)

                    sec = sec + 1
                    for i in range(fenmiaohao, length, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stamp / 1000000, 6)
                        # print("data:",data,"x:",x)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 3:
                            self.pgpower1_x.append(x)
                            self.pgpower1_y.append(data)
                        elif channel_id == 4:
                            self.pgpower2_x.append(x)
                            self.pgpower2_y.append(data)




    def sub_egpowerhs1_1_2(self):
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'')
        # zmqsub.setsockopt(zmq.SUBSCRIBE, b'\x00\x01')
        # zmqsub.setsockopt(zmq.SUBSCRIBE, b'\x00\x02')
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.hs1_sub_addr
        zmqsub.setsockopt(zmq.RCVTIMEO, 500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_total = True

        first_package = 10
        last_sec = -1
        zmqsub.connect(subaddr)
        while True:
            if self.flag_total:
                try:
                    b = zmqsub.recv()
                    if first_package == 0:
                        first_package = first_package - 1

                        continue
                    else:
                        pass
                except:
                    first_package == 10
                    continue
                channel_id = struct.unpack('!H', b[0:2])[0]  # 2
                length = struct.unpack('!B', b[2:3])[0]  # 1
                fenmiaohao = struct.unpack('!B', b[3:4])[0]  # 1
                sec = struct.unpack('!I', b[4:8])[0]  # 4
                if last_sec > sec:
                    break
                else:
                    last_sec = sec
                if fenmiaohao == 100:

                    for i in range(0, length, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stamp / 1000000, 6)
                        # print("data:",data,"x:",x)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 1:
                            self.egpower1_x.append(x)
                            self.egpower1_y.append(data)
                        elif channel_id == 2:
                            self.egpower2_x.append(x)
                            self.egpower2_y.append(data)
                else:

                    for i in range(0, fenmiaohao, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stamp / 1000000, 6)
                        # print("data:",data,"x:",x)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 1:
                            self.egpower1_x.append(x)
                            self.egpower1_y.append(data)
                        elif channel_id == 2:
                            self.egpower2_x.append(x)
                            self.egpower2_y.append(data)
                    sec = sec + 1
                    for i in range(fenmiaohao, length, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stamp / 1000000, 6)
                        # print("data:",data,"x:",x)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 1:
                            self.egpower1_x.append(x)
                            self.egpower1_y.append(data)
                        elif channel_id == 2:
                            self.egpower2_x.append(x)
                            self.egpower2_y.append(data)



    def sub_egpowerhs3_6(self):
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.hs3_sub_addr
        zmqsub.setsockopt(zmq.RCVTIMEO, 500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_total = True

        first_package = 10
        last_sec = -1
        zmqsub.connect(subaddr)
        while True:
            if self.flag_total:
                try:
                    b = zmqsub.recv()
                    if first_package == 0:
                        first_package = first_package - 1
                        continue
                    else:
                        pass
                except:
                    first_package == 10
                    continue
                channel_id = struct.unpack('!H', b[0:2])[0]  # 2
                length = struct.unpack('!B', b[2:3])[0]  # 1
                fenmiaohao = struct.unpack('!B', b[3:4])[0]  # 1
                sec = struct.unpack('!I', b[4:8])[0]  # 4
                # print("Current sec:",sec)
                if last_sec > sec:
                    break
                else:
                    last_sec = sec
                if fenmiaohao == 100:


                    for i in range(0, length, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stamp / 1000000, 6)
                        # print("data:",data,"x:",x)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 6:
                            self.egpower3_x.append(x)
                            self.egpower3_y.append(data)

                else:


                    for i in range(0, fenmiaohao, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec + us_stamp / 1000000, 6)
                        # print("data:",data,"x:",x)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 6:
                            self.egpower3_x.append(x)
                            self.egpower3_y.append(data)

                    sec = sec + 1
                    for i in range(fenmiaohao, length, self.datadensity):
                        tmp = b[8 + i * 8:10 + (i + 1) * 8]
                        data = struct.unpack('!f', tmp[0:4])[0]
                        us_stamp = struct.unpack('!I', tmp[4:8])[0]
                        x = round(sec  + us_stamp / 1000000, 6)
                        # print("data:",data,"x:",x)
                        # 这个地方完全可以选择二维数据
                        if channel_id == 6:
                            self.egpower3_x.append(x)
                            self.egpower3_y.append(data)

                # print('sub egpower')



    def dis_total(self):
        # self.curve_gassupply1.setData(y=self.gassupply1_y)
        self.curve_gassupply1.setData(x=self.gassupply1_x, y=self.gassupply1_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        # self.curve_gassupply2.setData(y=self.gassupply2_y)
        # self.curve_gassupply2.setData(x=self.gassupply2_x,y=self.gassupply2_y)
        # app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示

        self.curve_rfpower1.setData(x=self.rfpower1_x,y= self.rfpower1_y)
        # self.curve_rfpower1.setData(y= self.rfpower1_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        self.curve_rfpower2.setData(x=self.rfpower2_x,y= self.rfpower2_y)
        # self.curve_rfpower2.setData(y= self.rfpower2_y)



        self.curve_pgpower1.setData(x=self.pgpower1_x,y= self.pgpower1_y)
        # self.curve_pgpower1.setData(y= self.pgpower1_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        self.curve_pgpower2.setData(x=self.pgpower2_x,y= self.pgpower2_y)
        # self.curve_pgpower2.setData(y= self.pgpower2_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        # print('dis pgpower')


        ## eg：-20Kv的电压的电压情况
        self.curve_egpower1.setData(x=self.egpower1_x,y= self.egpower1_y)
        # self.curve_egpower1.setData( y=self.egpower1_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        ## egpower:负极的电流大小
        self.curve_egpower2.setData(x=self.egpower2_x,y= self.egpower2_y)
        # self.curve_egpower2.setData(y=self.egpower2_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        ## GG板的电流的大小
        self.curve_egpower3.setData(x=self.egpower3_x,y= self.egpower3_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        # self.curve_egpower3.setData( y=self.egpower3_y)
        ## 后级挡板的电流的大小
        # self.curve_egpower4.setData(x=self.egpower4_x,y= self.egpower4_y)
        # # self.curve_egpower4.setData(y=self.egpower4_y)
        # print('dis egpower')



    def tabchange(self):
        #ps这个current index  是从左到右依次增加的，默认从0开始
        # 对于这个地方，我们可以实现数据接收的停止，以及对应的ui的定时刷新的停止。


        print('index:',self.tabWidget.currentIndex())
        # if self.tabWidget.currentIndex()==0
        currenttab= self.tabWidget.currentIndex()


        if self.lasttabWidget == 0:
            try:
                self.stop_gassupply()
            except:
                pass

        elif self.lasttabWidget == 1:
            try:
                self.stop_rfpower()
            except:
                pass

        elif self.lasttabWidget == 2:
            try:
                self.stop_pgpower()
            except:
                pass


        elif self.lasttabWidget == 3:
            try:
                self.stop_egpower()
            except:
                pass
        else:
            print("Not developped yet")


        if currenttab == 0:
                self.start_gassupply()

        elif currenttab == 1:
                self.start_rfpower()
        elif currenttab == 2:
                self.start_pgpower()
        elif currenttab == 3:
                self.start_egpower()
        else:
            print("Not developped yet")

        self.lasttabWidget = currenttab

    def StartUpdate(self):


        print('In startupdate')

        if self.lasttabWidget == 0:
            if self.flag_gassupply: ## 防止一个部分的线程连续启动两次
                pass
            else:
                self.start_gassupply()
        elif self.lasttabWidget == 1:
            if self.flag_rfpower: ## 防止一个部分的线程连续启动两次
                pass
            else:
                self.start_rfpower()

        elif self.lasttabWidget == 2:
            if self.flag_pgpower: ## 防止一个部分的线程连续启动两次
                pass
            else:
                self.start_pgpower()

        elif self.lasttabWidget == 3:
            if self.flag_egpowerhs1_2: ## 防止一个部分的线程连续启动两次
                pass
            else:

                self.start_egpower()
        else:
            print("Not developped yet")





    def StopUpdate(self):
        print('In stop update',self.lasttabWidget)
        if self.lasttabWidget == 0:
            try:
                self.stop_gassupply()
            except:
                pass

        elif self.lasttabWidget == 1:
            try:
                self.stop_rfpower()
            except:
                pass

        elif self.lasttabWidget == 2:
            try:
                self.stop_pgpower()
            except:
                pass


        elif self.lasttabWidget == 3:
            try:
                self.stop_egpower()
            except:
                pass
        else:
            print("Not developped yet")




    def ClearUpdate(self):

                self.gassupply1_x=[]
                self.gassupply1_y = []
                self.gassupply2_x = []
                self.gassupply2_y = []
                # self.curve_gassupply1.setData(y=self.gassupply1_y)
                # self.curve_gassupply1.setData(y=self.gassupply2_y)
                self.curve_gassupply1.setData(x = self.gassupply1_x,y=self.gassupply1_y)
                self.curve_gassupply2.setData(x=self.gassupply2_x, y=self.gassupply2_y)
                # self.p_gassupply1.close()
                # self.p_gassupply2.close()

                self.rfpower1_x = []
                self.rfpower1_y = []
                self.rfpower2_x = []
                self.rfpower2_y = []
                # self.curve_gassupply1.setData(y=self.gassupply1_y)
                # self.curve_gassupply1.setData(y=self.gassupply2_y)
                self.curve_rfpower1.setData(x=self.rfpower1_x, y=self.rfpower1_y)
                self.curve_rfpower2.setData(x=self.rfpower2_x, y=self.rfpower2_y)

                self.pgpower1_x = []
                self.pgpower1_y = []
                self.pgpower2_x = []
                self.pgpower2_y = []
                # self.curve_gassupply1.setData(y=self.gassupply1_y)
                # self.curve_gassupply1.setData(y=self.gassupply2_y)
                self.curve_pgpower1.setData(x=self.pgpower1_x, y=self.pgpower1_y)
                self.curve_pgpower2.setData(x=self.pgpower2_x, y=self.pgpower2_y)

                self.egpower1_x = []
                self.egpower1_y = []
                self.egpower2_x = []
                self.egpower2_y = []
                self.egpower3_x = []
                self.egpower3_y = []
                self.egpower4_x = []
                self.egpower4_y = []
                # self.curve_gassupply1.setData(y=self.gassupply1_y)
                # self.curve_gassupply1.setData(y=self.gassupply2_y)
                self.curve_egpower1.setData(x=self.egpower1_x, y=self.egpower1_y)
                self.curve_egpower2.setData(x=self.egpower2_x, y=self.egpower2_y)
                self.curve_egpower3.setData(x=self.egpower3_x, y=self.egpower3_y)
                self.curve_egpower4.setData(x=self.egpower4_x, y=self.egpower4_y)



    def ExportData(self):
        print('In Export data')
        # output = open('datadown.xls', 'w', encoding='gbk')
        # output.write('id\tdata\n')
        # for i in range(len(data_pgpower)):
        #     output.write(str(i))
        #     output.write('\t')
        #     output.write(str(data_pgpower[i]))
        #     output.write('\n')
        # output.close()


        pass
    def ExportFigure(self):
        print('In export figure')
        # exporter = pg.exporters.ImageExporter(self.p.sceneObj)
        # print('aaa')
        # exporter.export(fileName='figure1.png')
        #
        # exporter1 = pg.exporters.ImageExporter(self.p2.sceneObj)
        # exporter1.export('figure2.png')
        #
        # exporter2 = pg.exporters.ImageExporter(self.p2.sceneObj)
        #         # exporter2.export('figure3.png')

    def SetDataDensity(self):
        print("data densnity ")
        spinvalue = self.spinBox.value()
        print('spinvalue ',spinvalue)


        if spinvalue >= 100:
            self.datadensity = 1
        elif spinvalue <= 1:
            self.datadensity ==100
        else:
            self.datadensity =  100-spinvalue








if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # main = MainDialogImgBW()
    # main.show()
    # #app.installEventFilter(main)
    # sys.exit(app.exec_())
    import sys

    ui = ChildDialogWin()
    # ui.setupUi(win)
    ui.show()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

