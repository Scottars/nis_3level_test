#-*-coding:utf-8-*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import os,signal,sys
from pyqtgraph.Qt import QtGui,QtCore, USE_PYSIDE, USE_PYQT5,QtWidgets
import  multiprocessing
import  numpy as np
import struct

import  pyqtgraph as pg
import pyqtgraph.exporters
from pyqtgraph.ptime import time
# 声明一个应用程序
app = QtGui.QApplication([])


import time
import  zmq
import threading
global data_pgpowerx,data_pgpowey
data_pgpowerx=[]
data_pgpowery=[]

global savingprogress11value
savingprogress11value=0

import inspect
import ctypes
import nis_hsdd_configfile
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


import process_manager
class ChildDialogWin2(QDialog,process_manager.Ui_Dialog):
    def __init__(self):
        super(ChildDialogWin2,self).__init__()
        #
        self.setupUi(self)
        self.setWindowTitle("Process Monitor GUI")


        print('we are in init')
        self.button_function_initial()

        self.initilization()

    def button_function_initial(self):
        self.pushButton_3.clicked.connect(self.start_process_monitor)
        self.pushButton_4.clicked.connect(self.stop_process_monitor)

        self.pushButton_15.clicked.connect(self.set_exp_id)

        # self.pushButton_68.clicked.connect(self.start_udp_send)
        # self.pushButton_69.clicked.connect(self.stop_udp_send)


        ####################### Debug Mode ####################

        # self.pushButton_192.clicked.connect(self.run_level_2_11_thread)
        # self.pushButton_194.clicked.connect(self.stop_level_2_11_thread)
        #
        # self.pushButton_187.clicked.connect(self.start_level_2_11_receive)
        # self.pushButton_189.clicked.connect(self.stop_level_2_11_receive)
        #
        # self.pushButton_188.clicked.connect(self.start_level_3_11)
        # self.pushButton_191.clicked.connect(self.stop_level_3_11)


        ###################Menu Mode#########################
        #对于实现udp  数据开始接收应当由内部含事故自行运行
        #水冷
        self.pushButton_26.clicked.connect(self.menu_start_level_2_01_udp)
        self.pushButton_28.clicked.connect(self.menu_stop_level_2_01_udp)

        # 铯炉
        self.pushButton_27.clicked.connect(self.menu_start_level_2_02_udp)
        self.pushButton_30.clicked.connect(self.menu_stop_level_2_02_udp)
        #供气
        self.pushButton_40.clicked.connect(self.menu_start_level_2_03_udp)
        self.pushButton_41.clicked.connect(self.menu_stop_level_2_03_udp)
        # pg m power
        self.pushButton_44.clicked.connect(self.menu_start_level_2_04_udp)
        self.pushButton_45.clicked.connect(self.menu_stop_level_2_04_udp)
        # 灯丝电源 filement power
        self.pushButton_48.clicked.connect(self.menu_start_level_2_05_udp)
        self.pushButton_49.clicked.connect(self.menu_stop_level_2_05_udp)
        # rf power
        self.pushButton_52.clicked.connect(self.menu_start_level_2_06_udp)
        self.pushButton_53.clicked.connect(self.menu_stop_level_2_06_udp)

        #pgpower
        self.pushButton_56.clicked.connect(self.menu_start_level_2_07_udp)
        self.pushButton_57.clicked.connect(self.menu_stop_level_2_07_udp)

        # egpower
        self.pushButton_60.clicked.connect(self.menu_start_level_2_08_udp)
        self.pushButton_61.clicked.connect(self.menu_stop_level_2_08_udp)

        #
        # self.pushButton_17.clicked.connect(self.run_pararead_thread)
        # self.pushButton_19.clicked.connect(self.stop_pararead_thread)

        # self.pushButton_20.clicked.connect(self.start_epics)
        # self.pushButton_21.clicked.connect(self.stop_epics)

    def initilization(self):
        self.context = zmq.Context()

        # self.level1_udp_manage = self.context.socket(zmq.PUB)
        # self.level1_udp_manageaddr = 'tcp://192.168.100.99:7878'
        # self.level1_udp_manage.bind(self.level1_udp_manageaddr)
        #
        # #水冷
        # self.level_2_req_01 = self.context.socket(zmq.REQ)
        # self.level_2_req_01addr =  nis_hsdd_configfile.level_2_01_watercool_req_addr
        # self.level_2_req_01.setsockopt(zmq.RCVTIMEO,1000) #  设定超时时间为5s
        # self.level_2_req_01.setsockopt(zmq.SNDTIMEO,1000) #  设定超时时间为5s
        # self.level_2_req_01.connect(self.level_2_req_01addr)
        #
        #
        # self.level_3_req_01 = self.context.socket(zmq.REQ)
        # self.level_3_req_01addr = nis_hsdd_configfile.level_3_01_watercool_req_addr
        # self.level_3_req_01.connect(self.level_3_req_01addr)
        # self.level_3_req_01.setsockopt(zmq.RCVTIMEO, 100)
        # self.level_3_req_01.setsockopt(zmq.SNDTIMEO, 100)
        #
        #
        # #铯炉
        # self.level_2_req_02 = self.context.socket(zmq.REQ)
        # self.level_2_req_02addr =  nis_hsdd_configfile.level_2_02_cefurance_req_addr
        # self.level_2_req_02.setsockopt(zmq.RCVTIMEO,1000) #  设定超时时间为5s
        # self.level_2_req_02.setsockopt(zmq.SNDTIMEO,1000) #  设定超时时间为5s
        # self.level_2_req_02.connect(self.level_2_req_02addr)
        #
        #
        # self.level_3_req_02 = self.context.socket(zmq.REQ)
        # self.level_3_req_02addr = nis_hsdd_configfile.level_3_02_cefurance_req_addr
        # self.level_3_req_02.connect(self.level_3_req_02addr)
        # self.level_3_req_02.setsockopt(zmq.RCVTIMEO, 100)
        # self.level_3_req_02.setsockopt(zmq.SNDTIMEO, 100)
        #
        #
        # #供气监测
        # self.level_2_req_03 = self.context.socket(zmq.REQ)
        # self.level_2_req_03addr =  nis_hsdd_configfile.level_2_03_gascontrol_req_addr
        # self.level_2_req_03.connect(self.level_2_req_03addr)
        # self.level_2_req_03.setsockopt(zmq.RCVTIMEO,100) #  设定超时时间为5s
        # self.level_2_req_03.setsockopt(zmq.SNDTIMEO,100) #  设定超时时间为5s
        #
        # self.level_3_req_03 = self.context.socket(zmq.REQ)
        # self.level_3_req_03addr = nis_hsdd_configfile.level_3_03_gascontrol_req_addr
        # self.level_3_req_03.connect(self.level_3_req_03addr)
        # self.level_3_req_03.setsockopt(zmq.RCVTIMEO,100)
        # self.level_3_req_03.setsockopt(zmq.SNDTIMEO,100)
        #
        #
        # #pg m power 磁场电源
        # self.level_2_req_04 = self.context.socket(zmq.REQ)
        # self.level_2_req_04addr =  nis_hsdd_configfile.level_2_04_pgmpower_req_addr
        # self.level_2_req_04.connect(self.level_2_req_04addr)
        # self.level_2_req_04.setsockopt(zmq.RCVTIMEO,100) #  设定超时时间为5s
        # self.level_2_req_04.setsockopt(zmq.SNDTIMEO,100) #  设定超时时间为5s
        #
        # self.level_3_req_04 = self.context.socket(zmq.REQ)
        # self.level_3_req_04addr = nis_hsdd_configfile.level_3_04_pgmpower_req_addr
        # self.level_3_req_04.connect(self.level_3_req_04addr)
        # self.level_3_req_04.setsockopt(zmq.RCVTIMEO,100)
        # self.level_3_req_04.setsockopt(zmq.SNDTIMEO,100)
        #
        # #灯丝电源  filement power
        # self.level_2_req_05 = self.context.socket(zmq.REQ)
        # self.level_2_req_05addr =  nis_hsdd_configfile.level_2_05_filmentpower_req_addr
        # self.level_2_req_05.connect(self.level_2_req_05addr)
        # self.level_2_req_05.setsockopt(zmq.RCVTIMEO,100) #  设定超时时间为5s
        # self.level_2_req_05.setsockopt(zmq.SNDTIMEO,100) #  设定超时时间为5s
        #
        # self.level_3_req_05 = self.context.socket(zmq.REQ)
        # self.level_3_req_05addr = nis_hsdd_configfile.level_3_05_filmentpower_req_addr
        # self.level_3_req_05.connect(self.level_3_req_05addr)
        # self.level_3_req_05.setsockopt(zmq.RCVTIMEO,100)
        # self.level_3_req_05.setsockopt(zmq.SNDTIMEO,100)
        #
        #
        # #rfpower、
        # self.level_2_req_06 = self.context.socket(zmq.REQ)
        # self.level_2_req_06addr =  nis_hsdd_configfile.level_2_06_filmentpower_req_addr
        # self.level_2_req_06.connect(self.level_2_req_06addr)
        # self.level_2_req_06.setsockopt(zmq.RCVTIMEO,100) #  设定超时时间为5s
        # self.level_2_req_06.setsockopt(zmq.SNDTIMEO,100) #  设定超时时间为5s
        #
        # self.level_3_req_06 = self.context.socket(zmq.REQ)
        # self.level_3_req_06addr = nis_hsdd_configfile.level_3_06_filmentpower_req_addr
        # self.level_3_req_06.connect(self.level_3_req_06addr)
        # self.level_3_req_06.setsockopt(zmq.RCVTIMEO,100)
        # self.level_3_req_06.setsockopt(zmq.SNDTIMEO,100)
        # # pg power
        # self.level_2_req_07 = self.context.socket(zmq.REQ)
        # self.level_2_req_07addr =  nis_hsdd_configfile.level_2_07_pgpower_req_addr
        # self.level_2_req_07.connect(self.level_2_req_07addr)
        # self.level_2_req_07.setsockopt(zmq.RCVTIMEO,100) #  设定超时时间为5s
        # self.level_2_req_07.setsockopt(zmq.SNDTIMEO,100) #  设定超时时间为5s
        #
        # self.level_3_req_07 = self.context.socket(zmq.REQ)
        # self.level_3_req_07addr = nis_hsdd_configfile.level_3_07_pgpower_req_addr
        # self.level_3_req_07.connect(self.level_3_req_07addr)
        # self.level_3_req_07.setsockopt(zmq.RCVTIMEO,100)
        # self.level_3_req_07.setsockopt(zmq.SNDTIMEO,100)
        #
        #
        # # 引出电源 eg power
        # self.level_2_req_08 = self.context.socket(zmq.REQ)
        # self.level_2_req_08addr =  nis_hsdd_configfile.level_2_08_egpower_req_addr
        # self.level_2_req_08.connect(self.level_2_req_08addr)
        # self.level_2_req_08.setsockopt(zmq.RCVTIMEO,100) #  设定超时时间为5s
        # self.level_2_req_08.setsockopt(zmq.SNDTIMEO,100) #  设定超时时间为5s
        #
        # self.level_3_req_08 = self.context.socket(zmq.REQ)
        # self.level_3_req_08addr = nis_hsdd_configfile.level_3_08_egpower_req_addr
        # self.level_3_req_08.connect(self.level_3_req_08addr)
        # self.level_3_req_08.setsockopt(zmq.RCVTIMEO,100)
        # self.level_3_req_08.setsockopt(zmq.SNDTIMEO,100)
        #
        # #  热量计， 16路
        # self.level_2_req_09 = self.context.socket(zmq.REQ)
        # self.level_2_req_09addr = nis_hsdd_configfile.level_2_09_heatmeter_req_addr
        # self.level_2_req_09.connect(self.level_2_req_09addr)
        # self.level_2_req_09.setsockopt(zmq.RCVTIMEO, 100)  # 设定超时时间为5s
        # self.level_2_req_09.setsockopt(zmq.SNDTIMEO, 100)  # 设定超时时间为5s
        #
        # self.level_3_req_09 = self.context.socket(zmq.REQ)
        # self.level_3_req_09addr = nis_hsdd_configfile.level_3_09_heatmeter_req_addr
        # self.level_3_req_09.connect(self.level_3_req_09addr)
        # self.level_3_req_09.setsockopt(zmq.RCVTIMEO, 100)
        # self.level_3_req_09.setsockopt(zmq.SNDTIMEO, 100)
        #
        # # pararead
        # self.level_3_req_pararead = self.context.socket(zmq.REQ)
        # self.level_3_req_parareadaddr = nis_hsdd_configfile.level_3_para_read_req_addr
        # self.level_3_req_pararead.bind(self.level_3_req_parareadaddr)
        # self.level_3_req_pararead.setsockopt(zmq.RCVTIMEO,100)
        # self.level_3_req_pararead.setsockopt(zmq.SNDTIMEO,100)



        #hs1 level2
        self.level2_hs1_req = self.context.socket(zmq.REQ)
        self.level2_hs1_req_addr = nis_hsdd_configfile.level2_hs1_req_addr
        self.level2_hs1_req.connect(self.level2_hs1_req_addr)
        self.level2_hs1_req.setsockopt(zmq.RCVTIMEO,100)
        self.level2_hs1_req.setsockopt(zmq.SNDTIMEO,100)

        # hs2 level2
        self.level2_hs2_req = self.context.socket(zmq.REQ)
        self.level2_hs2_req_addr = nis_hsdd_configfile.level2_hs2_req_addr
        self.level2_hs2_req.connect(self.level2_hs2_req_addr)
        self.level2_hs2_req.setsockopt(zmq.RCVTIMEO, 100)
        self.level2_hs2_req.setsockopt(zmq.SNDTIMEO, 100)
        # hs3 level2
        self.level2_hs3_req = self.context.socket(zmq.REQ)
        self.level2_hs3_req_addr = nis_hsdd_configfile.level2_hs3_req_addr
        self.level2_hs3_req.connect(self.level2_hs3_req_addr)
        self.level2_hs3_req.setsockopt(zmq.RCVTIMEO, 100)
        self.level2_hs3_req.setsockopt(zmq.SNDTIMEO, 100)
        # hs4 level2
        self.level2_hs4_req = self.context.socket(zmq.REQ)
        self.level2_hs4_req_addr = nis_hsdd_configfile.level2_hs4_req_addr
        self.level2_hs4_req.connect(self.level2_hs4_req_addr)
        self.level2_hs4_req.setsockopt(zmq.RCVTIMEO, 100)
        self.level2_hs4_req.setsockopt(zmq.SNDTIMEO, 100)
        # hs5 level2
        self.level2_hs5_req = self.context.socket(zmq.REQ)
        self.level2_hs5_req_addr = nis_hsdd_configfile.level2_hs5_req_addr
        self.level2_hs5_req.connect(self.level2_hs5_req_addr)
        self.level2_hs5_req.setsockopt(zmq.RCVTIMEO, 100)
        self.level2_hs5_req.setsockopt(zmq.SNDTIMEO, 100)


        #hs1 level2
        self.level3_hs1_req = self.context.socket(zmq.REQ)
        self.level3_hs1_req_addr = nis_hsdd_configfile.level3_hs1_req_addr
        self.level3_hs1_req.connect(self.level3_hs1_req_addr)
        self.level3_hs1_req.setsockopt(zmq.RCVTIMEO,100)
        self.level3_hs1_req.setsockopt(zmq.SNDTIMEO,100)

        # hs2 level3
        self.level3_hs2_req = self.context.socket(zmq.REQ)
        self.level3_hs2_req_addr = nis_hsdd_configfile.level3_hs2_req_addr
        self.level3_hs2_req.connect(self.level3_hs2_req_addr)
        self.level3_hs2_req.setsockopt(zmq.RCVTIMEO, 100)
        self.level3_hs2_req.setsockopt(zmq.SNDTIMEO, 100)
        # hs3 level3
        self.level3_hs3_req = self.context.socket(zmq.REQ)
        self.level3_hs3_req_addr = nis_hsdd_configfile.level3_hs3_req_addr
        self.level3_hs3_req.connect(self.level3_hs3_req_addr)
        self.level3_hs3_req.setsockopt(zmq.RCVTIMEO, 100)
        self.level3_hs3_req.setsockopt(zmq.SNDTIMEO, 100)
        # hs4 level3
        self.level3_hs4_req = self.context.socket(zmq.REQ)
        self.level3_hs4_req_addr = nis_hsdd_configfile.level3_hs4_req_addr
        self.level3_hs4_req.connect(self.level3_hs4_req_addr)
        self.level3_hs4_req.setsockopt(zmq.RCVTIMEO, 100)
        self.level3_hs4_req.setsockopt(zmq.SNDTIMEO, 100)
        # hs5 level3
        self.level3_hs5_req = self.context.socket(zmq.REQ)
        self.level3_hs5_req_addr = nis_hsdd_configfile.level3_hs5_req_addr
        self.level3_hs5_req.connect(self.level3_hs5_req_addr)
        self.level3_hs5_req.setsockopt(zmq.RCVTIMEO, 100)
        self.level3_hs5_req.setsockopt(zmq.SNDTIMEO, 100)


        ## Start epics tcp server thread
        self.tcp_epics_thread = tcp_receiving_thread()
        self.tcp_epics_thread.trigger.connect(self.epics_autoprocess)

    def start_udp_send(self):
        print('in start udp send')
        self.level1_udp_manage.send(b'start')

        pass
    def stop_udp_send(self):
        print('in stop udp send')
        pass

    def process_monitor(self):
        print('start process monitor ')
        self.flag_monitor= True
        while True:
            if self.flag_monitor:
                # time.sleep(1)
                print("###########分割线################")
                ####################level 2  ##################################
                # 水冷系统
                try:
                    self.level_2_req_01.send(b'udp alive?')
                except:
                    print('level 2 01: sendtime out')
                try:
                    x = self.level_2_req_01.recv()
                    if x == b'udp yes':
                        self.pushButton_7.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_29.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_202.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_7.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_29.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_202.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_7.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_29.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_202.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 2 01: udp not online')
                app.processEvents()
                # 铯炉 模块
                try:
                    self.level_2_req_02.send(b'udp alive?')
                except:
                    print('level 2 02: sendtime out')
                try:
                    x = self.level_2_req_02.recv()
                    if x == b'udp yes':
                        self.pushButton_118.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_31.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_213.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_118.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_31.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_213.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_118.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_31.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_213.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 2 02: udp not online')
                app.processEvents()
                # 供气系统
                try:
                    self.level_2_req_03.send(b'udp alive?')
                except:
                    print('level 2 03: sendtime out')
                try:
                    x = self.level_2_req_03.recv()
                    if x == b'udp yes':
                        self.pushButton_172.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_43.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_153.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_172.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_43.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_153.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_172.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_43.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_153.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 2 03: udp not online')
                app.processEvents()
                # pg m power 磁场电源
                try:
                    self.level_2_req_04.send(b'udp alive?')
                except:
                    print('level 2 04: sendtime out')
                try:
                    x = self.level_2_req_04.recv()
                    if x == b'udp yes':
                        self.pushButton_181.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_47.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_198.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_181.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_47.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_198.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_181.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_47.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_198.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 2 04: udp not online')
                app.processEvents()
                # 5 灯丝电源
                try:
                    self.level_2_req_05.send(b'udp alive?')
                except:
                    print('level 2 05: sendtime out')
                try:
                    x = self.level_2_req_05.recv()
                    if x == b'udp yes':
                        self.pushButton_354.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_51.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_209.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_354.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_51.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_209.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_354.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_51.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_209.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 2 05: udp not online')
                app.processEvents()
                # 6 射频功率
                try:
                    self.level_2_req_06.send(b'udp alive?')
                except:
                    print('level 2 06: sendtime out')
                try:
                    x = self.level_2_req_06.recv()
                    if x == b'udp yes':
                        self.pushButton_34.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_55.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_148.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_34.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_55.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_148.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_34.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_55.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_148.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 2 06: udp not online')

                app.processEvents()
                # 引出电源 pgpwoer 07
                try:
                    self.level_2_req_07.send(b'udp alive?')
                except:
                    print('level 2 07: sendtime out')

                try:
                    x = self.level_2_req_07.recv()
                    if x == b'udp yes':
                        self.pushButton_109.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_59.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_224.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_109.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_59.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_224.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_109.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_59.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_224.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 2 07: udp not online')
                app.processEvents()
                # 引出电源 pgpwoer 08
                try:
                    self.level_2_req_08.send(b'udp alive?')
                except:
                    print('level 2 08: sendtime out')

                try:
                    x = self.level_2_req_08.recv()
                    if x == b'udp yes':
                        self.pushButton_190.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_63.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_219.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_190.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_62.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_219.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_190.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_62.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_219.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 2 08: udp not online')
                app.processEvents()
                # 热量计  heatmeter 09
                try:
                    self.level_2_req_09.send(b'udp alive?')
                except:
                    print('level 2 09: sendtime out')

                try:
                    x = self.level_2_req_09.recv()
                    if x == b'udp yes':
                        self.pushButton_158.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_67.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_163.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_158.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_67.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_163.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_158.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_67.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_163.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 2 09: udp not online')

                app.processEvents()
                #########level 3  ###############################
                #水冷系统
                try:
                    self.level_3_req_01.send(b'process alive?')
                except:
                    print('level 3 01: sendtime out')
                try:
                    x = self.level_3_req_01.recv()
                    if x == b'process yes':
                        self.pushButton_2.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_32.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_203.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_2.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_32.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_203.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_2.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_32.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_203.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

                    print('level 3 01: process not online')
                app.processEvents()
                #铯炉 系统
                try:
                    self.level_3_req_02.send(b'process alive?')
                except:
                    print('level 3 02: sendtime out')
                try:
                    x = self.level_3_req_02.recv()
                    if x == b'process yes':
                        self.pushButton_121.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_33.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_212.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_121.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_33.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_212.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_121.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_33.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_212.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

                    print('level 3 02: process not online')

                app.processEvents()
                #  供气系统 03
                try:
                    self.level_3_req_03.send(b'process alive?')
                except:
                    print('level 3 03: sendtime out')
                try:
                    x = self.level_3_req_03.recv()
                    if x == b'process yes':
                        self.pushButton_175.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_42.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_151.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_175.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_42.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_151.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_175.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_42.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_151.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 3 03: process not online')
                app.processEvents()
                # pg 磁场电源   04
                try:
                    self.level_3_req_04.send(b'process alive?')
                except:
                    print('level 3 04: sendtime out')
                try:
                    x = self.level_3_req_04.recv()
                    if x == b'process yes':
                        self.pushButton_184.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_46.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_199.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_184.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_46.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_199.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_184.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_46.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_199.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

                    print('level 3 04: process not online')
                app.processEvents()
                # 灯丝电源 05
                try:
                    self.level_3_req_05.send(b'process alive?')
                except:
                    print('level 3 05: sendtime out')
                try:
                    x = self.level_3_req_05.recv()
                    if x == b'process yes':
                        self.pushButton_357.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_50.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_207.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_357.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_50.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_207.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_357.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_50.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_207.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

                    print('level 3 05: process not online')
                app.processEvents()
                # 射频功率  06
                try:
                    self.level_3_req_06.send(b'process alive?')
                except:
                    print('level 3 06: sendtime out')
                try:
                    x = self.level_3_req_06.recv()
                    if x == b'process yes':
                        self.pushButton_37.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_54.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_147.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_37.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_54.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_147.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_37.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_54.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_147.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

                    print('level 3 06: process not online')
                app.processEvents()
                #  引出电源系统 07
                try:
                    self.level_3_req_07.send(b'process alive?')
                except:
                    print('level 3 07: sendtime out')
                try:
                    x = self.level_3_req_07.recv()
                    if x == b'process yes':
                        self.pushButton_112.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_58.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_222.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_112.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_58.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_222.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_112.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_58.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_222.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 3 07: process not online')
                app.processEvents()
                #  引出电源系统 08
                try:
                    self.level_3_req_08.send(b'process alive?')
                except:
                    print('level 3 08: sendtime out')
                try:
                    x = self.level_3_req_08.recv()
                    if x == b'process yes':
                        self.pushButton_193.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_62.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_217.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_193.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_62.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_217.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_193.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_62.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_217.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 3 08: process not online')
                app.processEvents()
                # 热量计 heatmeter   09
                try:
                    self.level_3_req_09.send(b'process alive?')
                except:
                    print('level 3 09: sendtime out')
                try:
                    x = self.level_3_req_09.recv()
                    if x == b'process yes':
                        self.pushButton_166.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_66.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                        self.pushButton_156.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                    else:
                        self.pushButton_166.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_66.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                        self.pushButton_156.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                except:
                    self.pushButton_166.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_66.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    self.pushButton_156.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                    print('level 3 09: process not online')
    def start_process_monitor(self):
        print('we have start udp update process')
        # self.process_monitor_thread = threading.Thread(target=self.process_monitor)
        # self.process_monitor_thread.start()
        self.processtimer = QtCore.QTimer()
        self.processtimer.timeout.connect(self.process_monitor)
        self.processtimer.start(1000)

    def stop_process_monitor(self):
        print('we have stoppend update udp process ')
        self.flag_monitor = False
        time.sleep(1)
        stop_thread(self.process_monitor_thread)

    def hs_process_monitor(self):
        print('start hs process monitor ')
        # self.flag_monitor = True
        # while True:
        #     if self.flag_monitor:
                # time.sleep(1)
        print("###########分割线################")
        ####################level 2  ##################################
        # level 2 hs1
        try:
            self.level2_hs1_req.send(b'udp alive?')
        except:
            print('level 2 hs1: sendtime out')
        try:
            x = self.level2_hs1_req.recv()
            if x == b'udp yes':
                self.pushButton_227.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")

            else:
                self.pushButton_227.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

        except:
            self.pushButton_227.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

            print('level 2 hs1: udp not online')
        app.processEvents()
        # level 2 hs2
        try:
            self.level2_hs2_req.send(b'udp alive?')
        except:
            print('level 2 hs2: sendtime out')
        try:
            x = self.level2_hs2_req.recv()
            if x == b'udp yes':
                self.pushButton_233.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")

            else:
                self.pushButton_233.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
        except:
            self.pushButton_233.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('level 2 hs2: udp not online')
        app.processEvents()
        # level 2 hs3
        try:
            self.level2_hs3_req.send(b'udp alive?')
        except:
            print('level 2 hs3: sendtime out')
        try:
            x = self.level2_hs3_req.recv()
            if x == b'udp yes':
                self.pushButton_244.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            else:
                self.pushButton_244.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
        except:
            self.pushButton_244.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('level 2 hs3: udp not online')
        app.processEvents()
        # level 2 hs4
        try:
            self.level2_hs4_req.send(b'udp alive?')
        except:
            print('level 2 hs4: sendtime out')
        try:
            x = self.level2_hs4_req.recv()
            if x == b'udp yes':
                self.pushButton_238.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")

            else:
                self.pushButton_238.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

        except:
            self.pushButton_238.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

            print('level 2 hs4: udp not online')
        app.processEvents()
        # level 2 hs5
        try:
            self.level2_hs5_req.send(b'udp alive?')
        except:
            print('level 2 hs5: sendtime out')
        try:
            x = self.level2_hs5_req.recv()
            if x == b'udp yes':
                self.pushButton_249.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")

            else:
                self.pushButton_249.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

        except:
            self.pushButton_249.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

            print('level 2 hs5: udp not online')
        app.processEvents()

        #########level 3  ###############################
        # hs1  level3
        try:
            self.level3_hs1_req.send(b'process alive?')
        except:
            print('level 3 hs1: sendtime out')
        try:
            x = self.level3_hs1_req.recv()
            if x == b'process yes':
                self.pushButton_228.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            else:
                self.pushButton_228.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
        except:
            self.pushButton_228.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('level 3 hs1: process not online')
        app.processEvents()
        # hs2  level3
        try:
            self.level3_hs2_req.send(b'process alive?')
        except:
            print('level 3 hs2: sendtime out')
        try:
            x = self.level3_hs2_req.recv()
            if x == b'process yes':
                self.pushButton_232.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            else:
                self.pushButton_232.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
        except:
            self.pushButton_232.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('level 3 hs2: process not online')
        app.processEvents()
        # hs3  level3
        try:
            self.level3_hs3_req.send(b'process alive?')
        except:
            print('level 3 hs3: sendtime out')
        try:
            x = self.level3_hs3_req.recv()
            if x == b'process yes':
                self.pushButton_242.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            else:
                self.pushButton_242.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
        except:
            self.pushButton_242.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('level 3 hs3: process not online')
        app.processEvents()
        # hs4  level3
        try:
            self.level3_hs4_req.send(b'process alive?')
        except:
            print('level 3 hs4: sendtime out')
        try:
            x = self.level3_hs4_req.recv()
            if x == b'process yes':
                self.pushButton_239.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            else:
                self.pushButton_239.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
        except:
            self.pushButton_239.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('level 3 hs4: process not online')
        app.processEvents()
        # hs5  level3
        try:
            self.level3_hs5_req.send(b'process alive?')
        except:
            print('level 3 hs5: sendtime out')
        try:
            x = self.level3_hs5_req.recv()
            if x == b'process yes':
                self.pushButton_247.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            else:
                self.pushButton_247.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
        except:
            self.pushButton_247.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

            print('level 3 hs5: process not online')
        app.processEvents()

    def start_hs_process_monitor(self):
        print('we have start udp update process')
        # self.process_monitor_thread = threading.Thread(target=self.process_monitor)
        # self.process_monitor_thread.start()
        self.hsprocesstimer = QtCore.QTimer()
        self.hsprocesstimer.timeout.connect(self.hs_process_monitor)
        self.hsprocesstimer.start(1000)

    def stop_hs_process_monitor(self):
        print('we have stoppend update udp process ')
        self.hsprocesstimer.stop()
        # self.flag_monitor = False
        # time.sleep(1)
        # stop_thread(self.hs_process_monitor)

    def menu_start_level_2_01_udp(self):
        try:
            self.level_2_req_01.send(b'start')
        except:
            print('start udp send timeout')
            pass

        try:
            x = self.level_2_req_01.recv()
            print('we have received ', x)

            if x == b'start received':
                print('can we set this')
                self.pushButton.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_123.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_204.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            self.pushButton.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_123.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_204.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('not online')

    def menu_stop_level_2_01_udp(self):
        try:
            self.level_2_req_01.send(b'stop')
        except:
            print('stop udp send time out')
            pass
        try:
            x = self.level_2_req_01.recv()
            if x == b'stop received':
                self.pushButton.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_123.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_204.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                print('Received Msg:', x)
        except:
            self.pushButton.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_123.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_204.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            print('not online')

    def menu_start_level_2_02_udp(self):
        try:
            self.level_2_req_02.send(b'start')
        except:
            print('start udp send timeout')
            pass

        try:
            x = self.level_2_req_02.recv()
            print('we have received ', x)

            if x == b'start received':
                print('can we set this')
                self.pushButton_114.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_124.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_214.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            self.pushButton_114.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_124.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_214.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('not online')

    def menu_stop_level_2_02_udp(self):
        try:
            self.level_2_req_02.send(b'stop')
        except:
            print('stop udp send time out')
            pass
        try:
            x = self.level_2_req_02.recv()
            if x == b'stop received':
                self.pushButton_114.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_124.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_214.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                print('Received Msg:', x)
        except:
            self.pushButton_114.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_124.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_214.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            print('not online')

    def menu_start_level_2_03_udp(self):
        try:
            self.level_2_req_03.send(b'start')
        except:
            print('start udp send timeout')
            pass

        try:
            x = self.level_2_req_03.recv()
            print('we have received ', x)

            if x == b'start received':
                print('can we set this')
                self.pushButton_168.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_125.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_152.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            self.pushButton_168.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_125.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_152.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('not online')

    def menu_stop_level_2_03_udp(self):
        try:
            self.level_2_req_03.send(b'stop')
        except:
            print('stop udp send time out')
            pass

        try:
            x = self.level_2_req_03.recv()
            if x == b'stop received':
                self.pushButton_168.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_125.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_152.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

                print('Received Msg:', x)
        except:
            self.pushButton_168.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_125.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_152.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            print('not online')

    def menu_start_level_2_04_udp(self):
        try:
            self.level_2_req_04.send(b'start')
        except:
            print('start udp send timeout')
            pass

        try:
            x = self.level_2_req_04.recv()
            print('we have received ', x)

            if x == b'start received':
                print('can we set this')
                self.pushButton_177.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_126.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_197.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            self.pushButton_177.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_126.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_197.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('not online')

    def menu_stop_level_2_04_udp(self):
        try:
            self.level_2_req_04.send(b'stop')
        except:
            print('stop udp send time out')
            pass

        try:
            x = self.level_2_req_04.recv()
            if x == b'stop received':
                self.pushButton_177.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_126.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_197.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

                print('Received Msg:', x)
        except:
            self.pushButton_177.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_126.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_197.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            print('not online')


    def menu_start_level_2_05_udp(self):
        try:
            self.level_2_req_05.send(b'start')
        except:
            print('start udp send timeout')
            pass

        try:
            x = self.level_2_req_05.recv()
            print('we have received ', x)

            if x == b'start received':
                print('can we set this')
                self.pushButton_350.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_127.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_208.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            self.pushButton_350.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_127.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_208.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('not online')

    def menu_stop_level_2_05_udp(self):
        try:
            self.level_2_req_03.send(b'stop')
        except:
            print('stop udp send time out')
            pass

        try:
            x = self.level_2_req_03.recv()
            if x == b'stop received':
                self.pushButton_350.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_127.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_208.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                print('Received Msg:', x)
        except:
            self.pushButton_350.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_127.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_208.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            print('not online')

    def menu_start_level_2_06_udp(self):
        try:
            self.level_2_req_06.send(b'start')
        except:
            print('start udp send timeout')
            pass

        try:
            x = self.level_2_req_06.recv()
            print('we have received ', x)

            if x == b'start received':
                print('can we set this')
                self.pushButton_10.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_133.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_146.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            self.pushButton_10.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_133.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_146.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('not online')

    def menu_stop_level_2_06_udp(self):
        try:
            self.level_2_req_03.send(b'stop')
        except:
            print('stop udp send time out')
            pass

        try:
            x = self.level_2_req_03.recv()
            if x == b'stop received':
                self.pushButton_10.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_133.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_146.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                print('Received Msg:', x)
        except:
            self.pushButton_10.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_133.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_146.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            print('not online')

    def menu_start_level_2_07_udp(self):
        try:
            self.level_2_req_07.send(b'start')
        except:
            print('start udp send timeout')
            pass

        try:
            x = self.level_2_req_07.recv()
            print('we have received ', x)

            if x == b'start received':
                print('can we set this')
                self.pushButton_39.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_134.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_223.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            self.pushButton_39.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_134.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_223.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('not online')

    def menu_stop_level_2_07_udp(self):
        try:
            self.level_2_req_07.send(b'stop')
        except:
            print('stop udp send time out')
            pass

        try:
            x = self.level_2_req_07.recv()
            if x == b'stop received':
                self.pushButton_39.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_134.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_223.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

                print('Received Msg:', x)
        except:
            self.pushButton_39.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_134.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_223.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            print('not online')


    def menu_start_level_2_08_udp(self):
        try:
            self.level_2_req_08.send(b'start')
        except:
            print('start udp send timeout')
            pass

        try:
            x = self.level_2_req_08.recv()
            print('we have received ', x)

            if x == b'start received':
                print('can we set this')
                self.pushButton_39.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_134.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_223.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            self.pushButton_39.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_134.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_223.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('not online')

    def menu_stop_level_2_08_udp(self):
        try:
            self.level_2_req_08.send(b'stop')
        except:
            print('stop udp send time out')
            pass

        try:
            x = self.level_2_req_08.recv()
            if x == b'stop received':
                self.pushButton_39.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_134.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_223.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

                print('Received Msg:', x)
        except:
            self.pushButton_39.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_134.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_223.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            print('not online')

    def menu_start_level_2_09_udp(self):
        try:
            self.level_2_req_09.send(b'start')
        except:
            print('start udp send timeout')
            pass

        try:
            x = self.level_2_req_09.recv()
            print('we have received ', x)

            if x == b'start received':
                print('can we set this')
                self.pushButton_159.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_136.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                self.pushButton_157.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            self.pushButton_159.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_136.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            self.pushButton_157.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
            print('not online')

    def menu_stop_level_2_09_udp(self):
        try:
            self.level_2_req_03.send(b'stop')
        except:
            print('stop udp send time out')
            pass

        try:
            x = self.level_2_req_03.recv()
            if x == b'stop received':
                self.pushButton_159.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_136.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")
                self.pushButton_157.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

                print('Received Msg:', x)
        except:
            self.pushButton_159.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_136.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.pushButton_157.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            print('not online')

    def run_level_2_11_thread(self):
        try:
            self.level_2_req_11.send(b'run udp thread')
        except:
            print('run udp thread send ')
        try:
            x = self.level_2_req_11.recv()
            print('we have received ', x)
            if x == b'run udp thread received':
                print('can we set this')
                self.pushButton_7.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            print('not online')


    def stop_level_2_11_thread(self):
        try:
            self.level_2_req_11.send(b'stop udp thread')
        except:
            print('stop udp thread timeout')
            pass


        try:
            x = self.level_2_req_11.recv()
            print('we have received ', x)
            if x == b'stop udp thread received':
                print('can we set this')
                self.pushButton_7.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            print('not online')


    def start_level_2_11_receive(self):
        try:
            self.level_2_req_11.send(b'start')
        except:
            print('start udp send timeout')
            pass

        try:
            x = self.level_2_req_11.recv()

            print('we have received ',x)

            if x == b'start received':
                print('can we set this')
                self.pushButton.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
                print('Received Msg:', x)
        except:
            print('not online')
    def stop_level_2_11_receive(self):

        try:
            self.level_2_req_11.send(b'stop')
        except:
            print('stop udp send time out')
            pass

        try:
            x = self.level_2_req_11.recv()
            if x == b'stop received':
                self.pushButton.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

                print('Received Msg:', x)
        except:
            print('not online')

    def start_level_3_11(self):
        print('we are in start level 3 11')
        try:
            self.level_3_req_11.send(b'run process thread')
        except:
            print('send run process thread tiemeout ')
            pass
        try:
            x = self.level_3_req_11.recv()
            if x == b'run process thread received':
                print('start level 3 process is sent')
            else:
                print('not received correctly')
        except:
            print('level 3  11 daemon thread is not online')
    def stop_level_3_11(self):
        print('we are in stop level 3 11')
        try:
            self.level_3_req_11.send(b'stop process thread')
            x = self.level_3_req_11.recv()
            if x == b'stop process thread received':
                print('stop level 3 process is sent')
            else:
                print('not received correctly')
        except:
            print('level 3  11 daemon thread is not online')


    def start_saving_11(self):
        print('In start saving ')
        global savingprogress11value

        self.flag11stop=False
        try:
            self.level_3_req_11.send(b'run saving thread')
        except:
            pass

        try:
            x = self.level_3_req_11.recv()
            savingprogress11value = 0
            self.progressBar.setValue(savingprogress11value)
            self.label_4.setText('Saving')
            self.pushButton_14.setStyleSheet("QPushButton{border-radius:15px;background-color:green}")
            self.timersaving11.start(1000)
            self.Saving11thread.start()
            # 使能停止按钮
            self.pushButton_11.setEnabled(True)
        except:
            print('Timeout In req receive')

    def stop_saving_11(self):
        try:
            self.level_3_req_11.send(b'stop saving thread')
            x = self.level_3_req_11.recv()
            self.label_4.setText('Stop Saving')
            self.pushButton_14.setStyleSheet("QPushButton{border-radius:15px;background-color:grey}")

        except:
            print('Timeout in stop saving')



        self.timersaving11.stop()

    def saving_progressbar_update(self):
        global savingprogress11value
        print('currenalue ', savingprogress11value)
        self.progressBar.setValue(savingprogress11value)
        if savingprogress11value==100:
            self.label_4.setText('Done')
        print("updating the progress bar")
        pass


    def set_exp_id(self):
        # 通过好几个套接字的接口然后，设定该实验id下去。
        #
        exp_id = self.spinBox.value()

        print(type(exp_id))
        ###########set exp id to level 2 ##############
        ## send id to subsys 11
        try:
            self.level_3_req_11.send(b'exp_id'+str(exp_id).encode())
        except:
            self.label_7.setText('error')
            print('exp_id send time out for 11')

        try:
            x = self.level_3_req_11.recv()
            if x == b'exp_id received':
                self.label_7.setText(str(exp_id))
        except:
            self.label_7.setText('error')

            print('exp_id recv time out for 11 ')
        ## set exp id to pv  para read

        try:
            self.level_3_req_pararead.send(b'exp_id' + str(exp_id).encode())
        except:
            self.label_12.setText('error')
            print('exp_id send time out for 11')

        try:
            x = self.level_3_req_pararead.recv()
            if x == b'exp_id received':
                self.label_12.setText(str(exp_id))
                self.label_14.setText(str(exp_id))
        except:
            self.label_12.setText('error')

            print('exp_id recv time out for pararead ')
        pass

    def run_pararead_thread(self):
        #this is a level 3 function
        try:
            self.level_3_req_pararead.send(b'run pararead thread')
        except:
            print('send run level_3_req_pararead thread tiemeout ')
            pass
        try:
            x = self.level_3_req_pararead.recv()
            if x == b'run pararead thread received':
                print('run level_3_req_pararead is sent')
            else:
                print('not received correctly')
        except:
            print('level_3_req_pararead daemon thread is not online')

    def stop_pararead_thread(self):
        #this is a level 3 function
        try:
            self.level_3_req_pararead.send(b'stop pararead thread')
        except:
            print('send run level_3_req_pararead thread tiemeout ')
            pass
        try:
            x = self.level_3_req_pararead.recv()
            if x == b'stop pararead thread received':
                print('run level_3_req_pararead is sent')
            else:
                print('not received correctly')
        except:
            print('level_3_req_pararead daemon thread is not online')


    def start_epics(self):
        print('start tcp epics thread ')
        self.tcp_epics_thread.start()
        self.tcp_epics_thread.startagain()

    def stop_epics(self):
        print('stop tcp epics thread ')

        self.tcp_epics_thread.stop()
    def epics_autoprocess(self,msg):
        print('get the action in main',msg)

class uitimerthread(QtCore.QThread):
    trigger = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        # # Initialize poll set
        # self.poller = zmq.Poller()
        # self.poller.register(self.zmqsub,zmq.POLLIN)
        print('in 0')

        # self.app1=QtGui.QGuiApplication([])
        self.p=pg.plot()

        # self.p.setWindowTitle('pyqtgraph example: PlotSpeedTest')
        self.curve = self.p.plot()
        print('in 1')
        self.data = np.random.normal(size=(50, 5000))
        self.ptr = 0
        self.fps = None
        print('in 2')
        self.flagupdate=True
    def run(self):
        print('in run')
        while True:
            # time.sleep(0.01)
            if self.flagupdate:
                time.sleep(0.01)
                self.update()
    def update(self):
        # print('in 4 ')
        # global curve, data, ptr, p, lastTime, fps
        # self.curve.setData(self.data[self.ptr % 10])
        # self.ptr += 1
        global data_pgpower
        # print('datapower',data_pgpower)
        self.curve.setData(data_pgpower)

    def startsub(self):
        print('in ')
        self.flagupdate=True

        # self.run()

    def  stop(self):
        print('stop update')
        self.flagupdate=False


class tcp_receiving_thread(QtCore.QThread):
    '''
    说明：
    此线程的作用模拟底层被控设别而用于接收epics 的对不同进程的控制指令。
    更具体而言：
    1、具有收到管理中心启停的功能
    2、工作在tcp服务器模式下，能够接收到来自ioc发过来的不同进程启停的功能
    3、

    '''
    trigger=QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.flagtcpforepics = True


    def run(self):

        # 通过触发不同的函数的去调用主线程中的函数，这个时候就是属于来自epics 的自动控制
        while True:
            if self.flagtcpforepics:
                print('in tcp receive part')

                self.filestr = "hhaha "
                self.trigger.emit(self.filestr)


            else:
                pass

            time.sleep(1)


    def stop(self):
        self.flagtcpforepics= False
        print('we have stop the thread in stop')
    def startagain(self):
        self.flagtcpforepics = True




if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # main = MainDialogImgBW()
    # main.show()
    # #app.installEventFilter(main)
    # sys.exit(app.exec_())
    import sys

    ui = ChildDialogWin2()
    # ui.setupUi(win)
    ui.show()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

