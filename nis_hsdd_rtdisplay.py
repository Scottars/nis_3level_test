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
import nis_hsdd_configfile


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



# 水冷数据接收
class zmqrecvthread_02(QtCore.QThread):
    trigger=QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.context=zmq.Context()
        self.zmqsub=self.context.socket(zmq.SUB)
        self.zmqsub.setsockopt(zmq.SUBSCRIBE,b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        self.subaddr='tcp://192.168.127.201:5002'
        # self.subaddr='inproc://iiii'
        print('in the thread init')
        self.zmqsub.connect(self.subaddr)
        self.flag=0
        # # Initialize poll set
        # self.poller = zmq.Poller()
        # self.poller.register(self.zmqsub,zmq.POLLIN)

    def run(self):
        global  data_pgpower,data_receive_flag_02
        global pic2
        print('we are running ')
        print(self.subaddr)
        self.flag=1
        i=1
        counter=0
        while True:
            if self.flag:
                try:
                    # b = self.zmqsub.recv(zmq.DONTWAIT)
                    b = self.zmqsub.recv()
                    # print('recbeiving b',b)
                    counter+=1
                    # print('num',counter,'content:',struct.unpack('!f',b[0:4]))
                    for i in range(10):
                        tmpb = b[i * 36:(i + 1) * 36]
                        tmpby = tmpb[4:8]
                        tmpbx = tmpb[10:36]

                        try:
                            xmin = int(tmpbx[-12:-10].decode())
                            xs = float(tmpbx[-9:].decode())
                            x = xmin*60+xs
                            y = struct.unpack('!f', tmpby)[0]

                            # print('x:',x,'y:',y)
                            data_pgpowerx.append(x)
                            data_pgpowery.append(y)
                        except:
                            print('time sample error')
                except zmq.Again:
                    print('TO recv again')
                    pass
    def stop(self):
        self.flag=0
        print('we have stop the thread in stop')


# 引出电源数据接收
class zmqrecvthread_11(QtCore.QThread):
    trigger=QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.context=zmq.Context()
        self.zmqsub=self.context.socket(zmq.SUB)
        self.zmqsub.setsockopt(zmq.SUBSCRIBE,b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        self.subaddr='tcp://192.168.127.201:5011'
        # self.subaddr='inproc://iiii'
        print('in the thread init')
        self.zmqsub.connect(self.subaddr)
        self.flag=0
        # # Initialize poll set
        # self.poller = zmq.Poller()
        # self.poller.register(self.zmqsub,zmq.POLLIN)

    def run(self):
        global  data_pgpower,data_receive_flag_11
        global pic2
        print('we are running ')
        print(self.subaddr)
        self.flag=1
        i=1
        counter=0
        while True:
            if data_receive_flag_11:
                try:
                    # b = self.zmqsub.recv(zmq.DONTWAIT)
                    b = self.zmqsub.recv()
                    # print('recbeiving b',b)
                    counter+=1
                    # print('num',counter,'content:',struct.unpack('!f',b[0:4]))
                    for i in range(10):
                        tmpb = b[i * 36:(i + 1) * 36]
                        tmpby = tmpb[4:8]
                        tmpbx = tmpb[10:36]

                        try:
                            xmin = int(tmpbx[-12:-10].decode())
                            xs = float(tmpbx[-9:].decode())
                            x = xmin*60+xs
                            y = struct.unpack('!f', tmpby)[0]
                            data_pgpowerx.append(x)
                            data_pgpowery.append(y)
                        except:
                            print('time sample error')
                except zmq.Again:
                    print('TO recv again')
                    pass


class Savingrecvthread(QtCore.QThread):
    trigger1=QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.context = zmq.Context()
        self.recvsub11 = self.context.socket(zmq.SUB)
        self.recvsub11addr = 'tcp://127.0.0.1:8888'
        self.recvsub11.setsockopt(zmq.SUBSCRIBE, b'')
        self.recvsub11.bind(self.recvsub11addr)
        print('in here 111')
        self.recvsub11.setsockopt(zmq.RCVTIMEO, 2000)

        self.flag11stop = False

    def run(self):
        global savingprogress11value
        print('canwe in here')

        while True:
            if self.flag11stop:
                break
            else:
                try:
                    x = self.recvsub11.recv()
                    print('x',x)
                    step = int(float(x.decode("utf-8")))
                    savingprogress11value = step
                    if step==100:
                        print('already done')
                        break
                except:
                    print('chaoshi')

    def stop(self):
        self.flag11stop=True
        print('we have stop the thread in stop')




class ChildDialogWin(QDialog,nis_hsdd.Ui_Dialog):
    def __init__(self):
        super(ChildDialogWin,self).__init__()
        #
        self.setupUi(self)
        self.setWindowTitle("Real Time Display GUI")
        self.setMinimumSize(0,0)

        self.data3 = np.empty(100)
        self.ptr3 = 0
        self.ptrtmp = 0
        self.trix, self.triy = self.triangle_wave(0, 1, 0.01, 2, 2)

        print('we are in init')

        # self.pushButton.clicked.connect(self.start_11)
        # self.pushButton_2.clicked.connect(self.stop_11)
        # self.pushButton_3.clicked.connect(self.startRecving)
        # self.pushButton_4.clicked.connect(self.stopRecving)
        self.pushButton_5.clicked.connect(self.clearData)
        self.pushButton_6.clicked.connect(self.exportdataup)
        self.pushButton_7.clicked.connect(self.exportdatadown)
        self.pushButton_9.clicked.connect(self.exportfig)

        self.tabWidget.setCurrentIndex(0)
        self.lasttabWidget = 0
        self.tabWidget.currentChanged.connect(self.tabchange)


        self.figure_init()
        self.start_gassupply()
        # self.start_water()
    def button_init(self):
        #水冷
        self.pushButton_17.clicked.connect(self.clearData_water)


        #供气
        self.pushButton_33.clicked.connect(self.clearData_gassupply)


        #rf power

        self.pushButton_49.clicked.connect(self.clearData_rfpower)


        #引出电源
        self.pushButton_5.clicked.connect(self.clearData_pgpower)
        self.pushButton_6.clicked.connect(self.exportdataup)
        self.pushButton_7.clicked.connect(self.exportdatadown)
        self.pushButton_9.clicked.connect(self.exportfig)


    def figure_init(self):
        #初始化 所有的figure
        self.p_water1 = self.graphicsView
        self.p_water2 = self.graphicsView_2
        self.p_water3 = self.graphicsView_3
        self.p_water4 = self.graphicsView_4

        self.p_water5 = self.graphicsView_5
        self.p_water6 = self.graphicsView_6
        self.p_water7 = self.graphicsView_7
        self.p_water8 = self.graphicsView_8

        self.p_gassupply1 = self.graphicsView_14
        self.p_gassupply2 = self.graphicsView_15


        self.p_rfpower1 = self.graphicsView_19
        self.p_rfpower2 = self.graphicsView_20


        self.p_pgpower1 = self.graphicsView_23
        self.p_pgpower2 = self.graphicsView_24

        self.p_egpower1 = self.graphicsView_25
        self.p_egpower2 = self.graphicsView_26
        self.p_egpower3 = self.graphicsView_26
        self.p_egpower4 = self.graphicsView_27


        self.p_water1.setDownsampling(mode='subsample')
        self.p_water2.setDownsampling(mode='subsample')
        self.p_water3.setDownsampling(mode='subsample')
        self.p_water4.setDownsampling(mode='subsample')
        self.p_water5.setDownsampling(mode='subsample')
        self.p_water6.setDownsampling(mode='subsample')
        self.p_water7.setDownsampling(mode='subsample')
        self.p_water8.setDownsampling(mode='subsample')

        self.p_gassupply1.setDownsampling(mode='subsample')
        self.p_gassupply2.setDownsampling(mode='subsample')

        self.p_rfpower1.setDownsampling(mode='subsample')
        self.p_rfpower2.setDownsampling(mode='subsample')

        self.p_pgpower1.setDownsampling(mode='subsample')
        self.p_pgpower2.setDownsampling(mode='subsample')

        self.p_egpower1.setDownsampling(mode='subsample')
        self.p_egpower2.setDownsampling(mode='subsample')
        self.p_egpower3.setDownsampling(mode='subsample')
        self.p_egpower4.setDownsampling(mode='subsample')


        self.p_water1.setClipToView(True)
        self.p_water2.setClipToView(True)
        self.p_water3.setClipToView(True)
        self.p_water4.setClipToView(True)
        self.p_water5.setClipToView(True)
        self.p_water6.setClipToView(True)
        self.p_water7.setClipToView(True)
        self.p_water8.setClipToView(True)

        self.p_gassupply1.setClipToView(True)
        self.p_gassupply2.setClipToView(True)

        self.p_rfpower1.setClipToView(True)
        self.p_rfpower2.setClipToView(True)

        self.p_pgpower1.setClipToView(True)
        self.p_pgpower2.setClipToView(True)

        self.p_egpower1.setClipToView(True)
        self.p_egpower2.setClipToView(True)
        self.p_egpower3.setClipToView(True)
        self.p_egpower4.setClipToView(True)

        self.p_water1.setLabel("left", "value", units='L/min',color=(0,255,0))
        self.p_water1.setLabel("bottom", "Timestamp", units='s',color=(0,255,0))
        self.p_water1.setTitle('Water Temperture',color=(0,0,0))
        self.p_water2.setLabel("left", "value", units='L/min',color=(0,255,0))
        self.p_water2.setLabel("bottom", "Timestamp", units='s',color=(0,255,0))
        self.p_water2.setTitle('Water Temperture',color=(0,0,0))
        self.p_water3.setLabel("left", "value", units='L/min',color=(0,255,0))
        self.p_water3.setLabel("bottom", "Timestamp", units='s',color=(0,255,0))
        self.p_water3.setTitle('Water Temperture',color=(0,0,0))
        self.p_water4.setLabel("left", "value", units='L/min',color=(0,255,0))
        self.p_water4.setLabel("bottom", "Timestamp", units='s',color=(0,255,0))
        self.p_water4.setTitle('Water Temperture',color=(0,0,0))
        self.p_water5.setLabel("left", "value", units='L/min',color=(0,255,0))
        self.p_water5.setLabel("bottom", "Timestamp", units='s',color=(0,255,0))
        self.p_water5.setTitle('Water Temperture',color=(0,0,0))
        self.p_water6.setLabel("left", "value", units='L/min',color=(0,255,0))
        self.p_water6.setLabel("bottom", "Timestamp", units='s',color=(0,255,0))
        self.p_water6.setTitle('Water Temperture',color=(0,0,0))
        self.p_water7.setLabel("left", "value", units='L/min',color=(0,255,0))
        self.p_water7.setLabel("bottom", "Timestamp", units='s',color=(0,255,0))
        self.p_water7.setTitle('Water Temperture',color=(0,0,0))
        self.p_water8.setLabel("left", "value", units='L/min',color=(0,0,0))
        self.p_water8.setLabel("bottom", "Timestamp", units='s',color=(0,0,0))
        self.p_water8.setTitle('Water Temperture',color=(0,0,0))

        self.p_gassupply1.setLabel("left", "value", units='L/min')
        self.p_gassupply1.setLabel("bottom", "Timestamp", units='s')
        self.p_gassupply1.setTitle('CDG025D Pressure')

        self.p_gassupply2.setLabel("left", "value", units='L/min',)
        self.p_gassupply2.setLabel("bottom", "Timestamp", units='s')
        self.p_gassupply2.setTitle('627D Pressure')



        self.p_rfpower1.setLabel("left", "value", units='L/min')
        self.p_rfpower1.setLabel("bottom", "Timestamp", units='s')
        self.p_rfpower1.setTitle('射频功率')

        self.p_rfpower2.setLabel("left", "value", units='L/min',)
        self.p_rfpower2.setLabel("bottom", "Timestamp", units='s')
        self.p_rfpower2.setTitle('627D Pressure')


        self.p_pgpower1.setLabel("left", "value", units='L/min')
        self.p_pgpower1.setLabel("bottom", "Timestamp", units='s')
        self.p_pgpower1.setTitle('Water Temperture')

        self.p_pgpower2.setLabel("left", "value", units='L/min')
        self.p_pgpower2.setLabel("bottom", "Timestamp", units='s')
        self.p_pgpower2.setTitle('Water Temperture')

        self.p_egpower1.setLabel("left", "Current", units='mA')
        self.p_egpower1.setLabel("bottom", "Timestamp", units='s')
        self.p_egpower1.setTitle('I2+I3+I4 Current')

        self.p_egpower2.setLabel("left", "Current", units='mA')
        self.p_egpower2.setLabel("bottom", "Timestamp", units='s')
        self.p_egpower2.setTitle('I2 Current')


        self.p_egpower3.setLabel("left", "Current", units='mA')
        self.p_egpower3.setLabel("bottom", "Times`tamp", units='s')
        self.p_egpower3.setTitle('I3 Current')

        self.p_egpower4.setLabel("left", "Voltage", units='')
        self.p_egpower4.setLabel("bottom", "Timestamp", units='s')
        self.p_egpower4.setTitle('Water Temperture')



        self.p_water1.setBackground('w')
        self.p_water2.setBackground('w')
        self.p_water3.setBackground('w')
        self.p_water4.setBackground('w')
        self.p_water5.setBackground('w')
        self.p_water6.setBackground('w')
        self.p_water7.setBackground('w')
        self.p_water8.setBackground('w')

        self.p_gassupply1.setBackground('w')
        self.p_gassupply2.setBackground('w')
        self.p_gassupply3.setBackground('w')

        self.p_rfpower1.setBackground('w')
        self.p_rfpower2.setBackground('w')


        self.p_pgpower1.setBackground('w')
        self.p_pgpower2.setBackground('w')
        # self.p2.setBackground('r')

        self.p_egpower1.setBackground('w')
        self.p_egpower2.setBackground('w')
        self.p_egpower3.setBackground('w')
        self.p_egpower4.setBackground('w')


        self.curve_water1 = self.p_water1.plot(symbol='o',symbolSize=4)
        self.curve_water2 = self.p_water2.plot(pen=pg.mkPen(color=(0, 0, 0),width=5))
        self.curve_water3 = self.p_water3.plot(pen=pg.mkPen(color=(0, 0, 0),width=5))
        self.curve_water4 = self.p_water4.plot(pen=pg.mkPen(color=(0, 0, 0),width=5))
        self.curve_water5 = self.p_water5.plot(pen=pg.mkPen(color=(0, 0, 0),width=5))
        self.curve_water6 = self.p_water6.plot(pen=pg.mkPen(color=(0, 0, 0),width=5))
        self.curve_water7 = self.p_water7.plot(pen=pg.mkPen(color=(0, 0, 0),width=5))
        self.curve_water8 = self.p_water8.plot(pen=pg.mkPen(color=(0, 0, 0),width=5))

        self.curve_gassupply1 = self.p_gassupply1.plot(pen=(0, 0, 0))
        self.curve_gassupply2 = self.p_gassupply2.plot(pen=(0, 0, 0))

        self.curve_rfpower1 = self.p_rfpower1.plot(pen=(0, 0, 0))
        self.curve_rfpower2 = self.p_rfpower2.plot(pen=(0, 0, 0))

        self.curve_pgpower1 = self.p_pgpower1.plot(pen=(0, 0, 0))
        self.curve_pgpower2 = self.p_pgpower2.plot(pen=(0, 0, 0))

        self.curve_egpower1 = self.p_egpower1.plot(pen=(0, 0, 0))
        self.curve_egpower2 = self.p_egpower2.plot(pen=(0, 0, 0))
        self.curve_egpower3 = self.p_egpower3.plot(pen=(0, 0, 0))
        self.curve_egpower4 = self.p_egpower4.plot(pen=(0, 0, 0))

        self.water1_x = []
        self.water1_y = []
        self.water2_x = []
        self.water2_y = []
        self.water3_x = []
        self.water3_y = []
        self.water4_x = []
        self.water4_y = []
        self.water5_x = []
        self.water5_y = []
        self.water6_x = []
        self.water6_y = []
        self.water7_x = []
        self.water7_y = []
        self.water8_x = []
        self.water8_y = []

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
        self.egpower4_x = []
        self.egpower4_y = []

        self.flag_water = True
        self.flag_gassupply = True
        self.flag_rfpower = True
        self.flag_pgpower = True
        self.flag_egpower = True

        # self.data3=self.triy
        self.trix, self.triy = self.triangle_wave(0, 1, 0.01, 2, 2)
        # self.scatter = self.p3.plot(pen=(0,0,0), symbol='o')
    def start_water(self):
        print('start water')
        self.timer_water = QtCore.QTimer()
        self.timer_water.timeout.connect(self.dis_water)
        self.timer_water.start(1000) # 这个是

        self.flag_water = True
        self.sub_water_thread  = threading.Thread(target = self.sub_water)
        self.sub_water_thread.start()
    def start_gassupply(self):
        print('start gas supply')
        self.timer_gassupply = QtCore.QTimer()
        self.timer_gassupply.timeout.connect(self.dis_gassupply)
        self.timer_gassupply.start(1000)  # 这个是

        self.flag_gassupply = True
        self.sub_gassupply_thread = threading.Thread(target=self.sub_gassupply)
        self.sub_gassupply_thread.start()

    def start_rfpower(self):
        print('start rf power')
        self.timer_rfpower = QtCore.QTimer()
        self.timer_rfpower.timeout.connect(self.dis_rfpower)
        self.timer_rfpower.start(1000)  # 这个是

        self.flag_rfpower = True
        self.sub_rfpower_thread = threading.Thread(target=self.sub_rfpower)
        self.sub_rfpower_thread.start()

    def start_pgpower(self):
        print('start pgpower')

        self.timer_pgpower = QtCore.QTimer()
        self.timer_pgpower.timeout.connect(self.dis_pgpower)
        self.timer_pgpower.start(1000)

        self.flag_pgpower = True
        self.sub_pgpower_thread = threading.Thread(target=self.sub_pgpower)
        self.sub_pgpower_thread.start()

    def start_egpower(self):
        print("start egpower")
        self.timer_egpowerhs1_2 = QtCore.QTimer()
        self.timer_egpowerhs1_2.timeout.connect(self.dis_egpower)
        self.timer_egpowerhs1_2.start(1000)
        self.start_egpowerhs1_2()
        self.start_egpowerhs2_3_4()
        self.start_egpowerhs3_5()

    def start_egpowerhs1_2(self):
        self.flag_egpowerhs1_2 = True
        self.sub_egpowerhs1_2_thread = threading.Thread(target=self.sub_egpowerhs1_2)
        self.sub_egpowerhs1_2_thread.start()
    def start_egpowerhs2_3_4(self):

        self.flag_egpowerhs2_3_4 = True
        self.sub_egpowerhs2_3_4_thread = threading.Thread(target=self.sub_egpowerhs2_3_4)
        self.sub_egpowerhs2_3_4_thread.start()
    def start_egpowerhs3_5(self):
        print('start egpower')

        self.flag_egpowerhs3_5 = True
        self.sub_egpowerhs3_5_thread = threading.Thread(target=self.sub_egpowerhs3_5)
        self.sub_egpowerhs3_5_thread.start()

    def stop_water(self):
        print('stop water')

        self.flag_water = False
        time.sleep(1)
        stop_thread(self.sub_water_thread)
        self.timer_water.stop()
    def stop_gassupply(self):
        print('stop gas supply ')

        self.flag_gassupply = False
        time.sleep(1)
        stop_thread(self.sub_gassupply_thread)
        self.timer_gassupply.stop()
    def stop_rfpower(self):
        print('stop rf pwoer ')

        self.flag_rfpower = False
        time.sleep(1)
        stop_thread(self.sub_rfpower_thread)
        self.timer_rfpower.stop()
    def stop_pgpower(self):
        print('stop pgpower ')

        self.flag_pgpower = False
        time.sleep(1)
        stop_thread(self.sub_pgpower_thread)
        self.timer_pgpower.stop()
    def stop_egpower(self):
        print('stop egpower ')

        self.flag_egpowerhs1_2 = False
        self.flag_egpowerhs2_3_4 = False
        self.flag_egpowerhs3_5 = False
        time.sleep(1)
        stop_thread(self.sub_egpowerhs1_2_thread)
        stop_thread(self.sub_egpowerhs2_3_4_thread)
        stop_thread(self.sub_egpowerhs3_5_thread)
        self.timer_egpower.stop()




    def sub_water(self):
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.level_2_01_watercool_sub_addr
        zmqsub.setsockopt(zmq.RCVTIMEO,500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_water = True

        zmqsub.connect(subaddr)
        while  True:
            if self.flag_water:
                try:
                    b = zmqsub.recv()
                except:
                    continue
                ####
                print('in sub water','b',b)
                channel_id = int(b[0:1].decode())
                length = struct.unpack('!I',b[1:5])[0]
                fenmiaohao = int(b[0:1].decode())
                sec = struct.unpack('!I',b[6:10])[0]

                for i in range(length):
                    tmp = b[10+i*8:10+(i+1)*8]
                    data = struct.unpack('!f',tmp[0:4])[0]
                    us_stampe = struct.unpack('!I',tmp[4:8])[0]
                    print('aaa',data,'us',us_stampe)
                    x =round( sec + us_stampe/1000000,6)
                    # 这个地方完全可以选择二维数据
                    print('channel id ',channel_id,'length',length)
                    if channel_id == 1:
                        self.water1_x.append(x)
                        self.water1_y.append(data)
                    elif channel_id == 2:
                        self.water2_x.append(x)
                        self.water2_y.append(data)
                    elif channel_id == 3:
                        self.water3_x.append(x)
                        self.water3_y.append(data)
                    elif channel_id == 4:
                        self.water4_x.append(x)
                        self.water4_y.append(data)
                    elif channel_id == 5:
                        self.water5_x.append(x)
                        self.water5_y.append(data)
                    elif channel_id == 6:
                        self.water6_x.append(x)
                        self.water6_y.append(data)
                    elif channel_id == 7:
                        self.water7_x.append(x)
                        self.water7_y.append(data)
                    elif channel_id == 8:
                        self.water8_x.append(x)
                        self.water8_y.append(data)

                print('subwater')
                # time.sleep(1)
    def dis_water(self):
        print('data',self.water1_x)
        self.curve_water1.setData(x=self.water1_x,y=self.water1_y)
        self.curve_water2.setData(x=self.water2_x, y=self.water2_y)
        self.curve_water3.setData(x=self.water3_x, y=self.water3_y)
        self.curve_water4.setData(x=self.water4_x, y=self.water4_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        self.curve_water5.setData(x=self.water5_x, y=self.water5_y)
        self.curve_water6.setData(x=self.water6_x, y=self.water6_y)
        self.curve_water7.setData(x=self.water7_x, y=self.water7_y)
        self.curve_water8.setData(x=self.water8_x, y=self.water8_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示d
        print('dis water')
    def sub_gassupply(self):
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.hs5_sub_addr
        zmqsub.setsockopt(zmq.RCVTIMEO, 500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_gassupply = True

        zmqsub.connect(subaddr)
        while  True:
            if self.flag_gassupply:
                try:
                    b = zmqsub.recv()
                except:
                    continue
                ####
                print('in sub gas', 'b', b)
                channel_id = int(b[0:1].decode())
                length = struct.unpack('!I', b[1:5])[0]
                fenmiaohao = int(b[0:1].decode())
                sec = struct.unpack('!I', b[6:10])[0]

                for i in range(length):
                    tmp = b[10+i*8:10+(i+1)*8]
                    data = struct.unpack('!f',tmp[0:4])[0]
                    us_stampe = struct.unpack('!I',tmp[4:8])[0]
                    x = round(sec + us_stampe / 1000000, 6)
                    # 这个地方完全可以选择二维数据
                    if channel_id == 9:
                        self.gassupply1_x.append(x)
                        self.gassupply1_y.append(data)
                    elif channel_id == 10:
                        self.gassupply2_x.append(x)
                        self.gassupply2_y.append(data)
                print('sub gas suply')
    def dis_gassupply(self):

        self.curve_gassupply1.setData(x=self.gassupply1_x,y=self.gassupply1_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        self.curve_gassupply2.setData(x=self.gassupply2_x,y=self.gassupply2_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        self.curve_gassupply3.setData(x=self.gassupply3_x,y=self.gassupply3_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示

        print('dis gassupply ')
    def sub_rfpower(self):
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.hs4_sub_addr
        zmqsub.setsockopt(zmq.RCVTIMEO, 500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_rfpower = True

        zmqsub.connect(subaddr)
        while  True:
            if self.flag_rfpower:
                try:
                    b = zmqsub.recv()
                except:
                    continue
                ####
                print('in rfpower', 'b', b)
                channel_id = int(b[0:1].decode())
                length = struct.unpack('!I', b[1:5])[0]
                fenmiaohao = int(b[0:1].decode())
                sec = struct.unpack('!I', b[6:10])[0]
                print('length:',length)

                for i in range(length):
                    tmp = b[10+i*8:10+(i+1)*8]
                    data = struct.unpack('!f',tmp[0:4])[0]
                    us_stampe = struct.unpack('!I',tmp[4:8])[0]
                    x = round(sec + us_stampe / 1000000, 6)
                    # 这个地方完全可以选择二维数据
                    if channel_id == 7:
                        self.rfpower1_x.append(x)
                        self.rfpower1_y.append(data)
                    elif channel_id == 8:
                        self.rfpower2_x.append(x)
                        self.rfpower2_y.append(data)
                print('sub pgpower',len(self.pgpower1_x))
    def dis_rfpower(self):
        # self.curve_pgpower1.setData(x=self.pgpower1_x,y= self.pgpower1_y)
        self.curve_rfpower1.setData(y= self.pgpower1_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        # self.curve_pgpower2.setData(x=self.pgpower2_x,y= self.pgpower2_y)
        self.curve_rfpower2.setData(y= self.pgpower2_y)

        print('dis pgpower')
    def sub_pgpower(self):
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.level_2_07_pgpower_sub_addr
        zmqsub.setsockopt(zmq.RCVTIMEO, 500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_pgpower = True

        zmqsub.connect(subaddr)
        while  True:
            if self.flag_pgpower:
                try:
                    b = zmqsub.recv()
                except:
                    continue
                ####
                print('in pgpower', 'b', b)
                channel_id = int(b[0:1].decode())
                length = struct.unpack('!I', b[1:5])[0]
                fenmiaohao = int(b[0:1].decode())
                sec = struct.unpack('!I', b[6:10])[0]
                # print('length:',length)

                for i in range(length):
                    tmp = b[10+i*8:10+(i+1)*8]
                    data = struct.unpack('!f',tmp[0:4])[0]
                    us_stampe = struct.unpack('!I',tmp[4:8])[0]
                    x = round(sec + us_stampe / 1000000, 6)
                    # 这个地方完全可以选择二维数据
                    if channel_id == 1:
                        self.pgpower1_x.append(x)
                        self.pgpower1_y.append(data)
                    elif channel_id == 6:
                        self.pgpower2_x.append(x)
                        self.pgpower2_y.append(data)
                print('sub pgpower',len(self.pgpower1_x))
    def dis_pgpower(self):
        # self.curve_pgpower1.setData(x=self.pgpower1_x,y= self.pgpower1_y)
        self.curve_pgpower1.setData(y= self.pgpower1_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        # self.curve_pgpower2.setData(x=self.pgpower2_x,y= self.pgpower2_y)
        self.curve_pgpower2.setData(y= self.pgpower2_y)

        print('dis pgpower')

    def dis_egpower(self):
        ## eg：-20Kv的电压的电压情况
        self.curve_egpower1.setData(x=self.egpower1_x,y= self.egpower1_y)
        # self.curve_egpower1.setData( y=self.egpower1_y)
        app.processEvents()  # 这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        ## egpower:负极的电流大小
        self.curve_egpower2.setData(x=self.egpower2_x,y= self.egpower2_y)
        # self.curve_egpower2.setData(y=self.egpower2_y)
        ## GG板的电流的大小
        self.curve_egpower3.setData(x=self.egpower3_x,y= self.egpower3_y)
        ## 后级挡板的电流的大小
        self.curve_egpower4.setData(x=self.egpower4_x,y= self.egpower4_y)
        print('dis egpower')


    def sub_egpowerhs1_2(self):
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.hs1_sub_addr
        zmqsub.setsockopt(zmq.RCVTIMEO, 500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_egpowerhs1_2 = True

        zmqsub.connect(subaddr)
        while True:
            if self.flag_egpower:
                try:
                    b = zmqsub.recv()
                except:
                    continue
                channel_id = struct.unpack('!H', b[0:2])[0]  # 2
                length = struct.unpack('!B', b[2:3])[0]  # 1
                fenmiaohao = struct.unpack('!B', b[3:4])[0]  # 1
                sec = struct.unpack('!I', b[4:8])[0]  # 4

                for i in range(length):  # 此处可通过设定start，end，间隔  来选择密度
                    tmp = b[8 + i * 8:10 + (i + 1) * 8]
                    data = struct.unpack('!f', tmp[0:4])[0]
                    us_stamp = struct.unpack('!I', tmp[4:8])[0]
                    x = round(sec + us_stamp / 1000000, 6)
                    # print("data:",data,"x:",x)
                    # 这个地方完全可以选择二维数据
                    if channel_id == 2:
                        self.egpower1_x.append(x)
                        self.egpower1_y.append(data)

    def sub_egpowerhs2_3_4(self):
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.hs2_sub_addr
        zmqsub.setsockopt(zmq.RCVTIMEO, 500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_egpowerhs2_3_4 = True

        zmqsub.connect(subaddr)
        while True:
            if self.flag_egpowerhs2_3_4:
                try:
                    b = zmqsub.recv()
                except:
                    continue
                channel_id = struct.unpack('!H', b[0:2])[0]  # 2
                length = struct.unpack('!B', b[2:3])[0]  # 1
                fenmiaohao = struct.unpack('!B', b[3:4])[0]  # 1
                sec = struct.unpack('!I', b[4:8])[0]  # 4
                # print("Current sec:",sec)

                if channel_id == 3:
                    print('channel id is ', channel_id)
                for i in range(100):
                    tmp = b[8 + i * 8:10 + (i + 1) * 8]
                    data = struct.unpack('!f', tmp[0:4])[0]
                    us_stamp = struct.unpack('!I', tmp[4:8])[0]
                    x = round(sec + us_stamp / 1000000, 6)
                    # print("data:",data,"x:",x)
                    # 这个地方完全可以选择二维数据
                    if channel_id == 3:
                        self.egpower2_x.append(x)
                        self.egpower2_y.append(data)

                    elif channel_id == 4:
                        self.egpower3_x.append(x)
                        self.egpower3_y.append(data)
                print('sub egpower')

    def sub_egpowerhs3_5(self):
        context = zmq.Context()
        zmqsub = context.socket(zmq.SUB)
        zmqsub.setsockopt(zmq.SUBSCRIBE, b'')
        # self.subaddr='tcp://192.168.127.200:10011'
        subaddr = nis_hsdd_configfile.hs3_sub_addr
        zmqsub.setsockopt(zmq.RCVTIMEO, 500)
        # self.subaddr='inproc://iiii'
        # print('in the thread init')
        self.flag_egpowerhs3_5 = True

        zmqsub.connect(subaddr)
        while  True:
            if self.flag_egpowerhs3_5:
                try:
                    b = zmqsub.recv()
                except:
                    continue
                channel_id = struct.unpack('!H', b[0:2])[0]  # 2
                length = struct.unpack('!B', b[2:3])[0]  # 1
                fenmiaohao = struct.unpack('!B', b[3:4])[0]  # 1
                sec = struct.unpack('!I', b[4:8])[0]  # 4
                # print("Current sec:",sec)

                if channel_id ==5:
                    print('channel id is ',channel_id)
                for i in range(100):
                    tmp = b[8+i*8:10+(i+1)*8]
                    data = struct.unpack('!f',tmp[0:4])[0]
                    us_stamp = struct.unpack('!I',tmp[4:8])[0]
                    x = round(sec + us_stamp / 1000000, 6)
                    # print("data:",data,"x:",x)
                    # 这个地方完全可以选择二维数据
                    if channel_id == 5:
                        self.egpower4_x.append(x)
                        self.egpower4_y.append(data)


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

    def triangle_wave(self,start, zhouqi, midu, xdecimals, ydecimals):
        '''

        :param start: the fist value of the wave
        :param end:  the end value of the wave
        :param zhouqi:  the zhouqi range of the wave
        :param midu:  every zhouqi, there are how many points in this zhouqi
        :return: the x array and the y array
        '''

        xout = []
        yout = []
        x = np.around(np.arange(start, start + zhouqi, midu), decimals=xdecimals)
        # y = np.where(x<start+0.5, x-start, 0)
        y = np.around(np.where(x >= start + zhouqi / 2, start + zhouqi - x, x - start), decimals=ydecimals) - 1

        return x, y

    def update_02(self):
        # global data3, ptr3, ptrtmp
        # data3[ptr3] = np.random.normal()
        self.data3[self.ptr3] = self.triy[self.ptrtmp]
        # self.p3.clear()
        if self.ptr3>1000:
            datatmp1=self.data3[self.ptr3-1000:self.ptr3-1] # 显示最新的10000个数据

        self.ptrtmp += 1
        if self.ptrtmp == 99:
            self.ptrtmp = 0
        self.ptr3 += 1
        if self.ptr3 >= self.data3.shape[0]:
            tmp = self.data3
            self.data3 = np.empty(self.data3.shape[0] * 2)
            self.data3[:tmp.shape[0]] = tmp
        if self.ptr3>1001:
            self.curve.setData(datatmp1)
        else:
            self.curve.setData(self.data3[:self.ptr3])
        # self.p.setRange(xRange=[self.ptr3-50, self.ptr3+50])

        # self.curve.setPos(self.ptr3-1000,0)
        # print('can we in here  after 他和cureset')
        listx = []
        for i in range(self.ptr3):
            listx.append(i+10)
        self.curve2.setData(x=listx,y=self.data3[:self.ptr3])
        # self.curve2sub.setData(self.data3[:self.ptr3]+1)
        # self.scatter.setData(y=self.data3[:self.ptr3],)
    def update_11(self):
        # global data3, ptr3, ptrtmp
        # data3[ptr3] = np.random.normal()
        self.data3[self.ptr3] = self.triy[self.ptrtmp]
        # self.p3.clear()
        if self.ptr3>1000:
            datatmp1=self.data3[self.ptr3-1000:self.ptr3-1] # 显示最新的10000个数据

        self.ptrtmp += 1
        if self.ptrtmp == 99:
            self.ptrtmp = 0
        self.ptr3 += 1
        if self.ptr3 >= self.data3.shape[0]:
            tmp = self.data3
            self.data3 = np.empty(self.data3.shape[0] * 2)
            self.data3[:tmp.shape[0]] = tmp
        if self.ptr3>1001:
            self.curve.setData(datatmp1)
        else:
            self.curve.setData(self.data3[:self.ptr3])
        # self.p.setRange(xRange=[self.ptr3-50, self.ptr3+50])

        # self.curve.setPos(self.ptr3-1000,0)
        # print('can we in here  after 他和cureset')
        listx = []
        for i in range(self.ptr3):
            listx.append(i+10)
        self.curve2.setData(x=listx,y=self.data3[:self.ptr3])
        # self.curve2sub.setData(self.data3[:self.ptr3]+1)
        # self.scatter.setData(y=self.data3[:self.ptr3],)

    def update2(self):
        global  data_pgpowerx,data_pgpowery
        datatmp1x=data_pgpowerx[len(data_pgpowerx)-10000:len(data_pgpowerx)-1] # 显示最新的10000个数据
        datatmp1y = data_pgpowery[len(data_pgpowerx) - 10000:len(data_pgpowerx) - 1]
        app.processEvents()
        # print('we are in update2')
        self.curve.setData(x=datatmp1x,y=datatmp1y)
        self.curve.setPos(len(data_pgpowerx)-10000,0)
        app.processEvents() #这句话的意思是将界面的控制权短暂的交给ui界面进行显示
        # 另外一种告诉的方案，就是额外的启动两个线程， 干脆就不在当前的线程上进行数据展示，就单独额外的线程进行绘图就好了


        self.curve2.setData(data_pgpowery)
        app.processEvents() #这句话的意思是将界面的控制权短暂的交给ui界面进行显示

        # self.curve2.setData(data_pgpowery)



    def startRecving_02(self):
        global data_receive_flag_02
        data_receive_flag_02 = True
    def stopRecving_02(self):
        global data_receive_flag_02
        data_receive_flag_02 = False

    def startRecving_11(self):
        global data_receive_flag_11
        data_receive_flag_11 = True
    def stopRecving_11(self):
        global data_receive_flag_11
        data_receive_flag_11 = False

    def zmqrecvcallback(self):
        print('we have call the recvback once ')
        # self.update2()

        # print(theint)
        # Use this function to update our figure
    def clearData(self):
        global data_pgpowerx,data_pgpowery
        # data_pgpowerx=[0]
        # data_pgpowery=[0]
        print('we have cleared the data')
        # print(data_pgpower)
        # self.curve.setData(data_pgpower)
        # self.curve2.setData(data_pgpowery)
        # self.curve.setData(data_pgpowery)
        # self.p.clear()
        # self.p2.clear()


    def exportdataup(self):
        output = open('datadown.xls', 'w', encoding='gbk')
        output.write('id\tdata\n')
        for i in range(len(data_pgpower)):
            output.write(str(i))
            output.write('\t')
            output.write(str(data_pgpower[i]))
            output.write('\n')
        output.close()

    def exportdatadown(self):
        output = open('datadown.xls','w',encoding='gbk')
        output.write('id\tdata\n')
        for i in range(len(data_pgpower)):

            output.write(str(i))
            output.write('\t')
            output.write(str(data_pgpower[i]))
            output.write('\n')
        output.close()

        pass
    def exportfig(self):
        print('we are in exporr fi g')
        exporter = pg.exporters.ImageExporter(self.p.sceneObj)
        print('aaa')
        exporter.export(fileName='figure1.png')

        exporter1 = pg.exporters.ImageExporter(self.p2.sceneObj)
        exporter1.export('figure2.png')

        exporter2 = pg.exporters.ImageExporter(self.p2.sceneObj)
        exporter2.export('figure3.png')








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

