import time

import epics
import pymysql

# 定义类
pv = epics.PV('scottar:voltage:ai')

'''PV 若是不在线，则报如下错误：
Failed to start executable - "caRepeater". ϵͳ�Ҳ���ָ�����ļ���

Changes may be required in your "path" environment variable.
caStartRepeaterIfNotInstalled (): unable to start CA repeater daemon detached process
CA client library is unable to contact CA repeater after 50 tries.
Silence this message by starting a CA repeater daemon
or by calling ca_pend_event() and or ca_poll() more often.
'''


''' 供气系统 '''

GAS_PUFF_TRIG_MODE = epics.pv('GF:GAS_PUFF_ TRIG_MODE')
GAS_PUFF_ON_OFF = epics.pv('GF:GAS_PUFF_ ON_OFF')
GAS_FLOW_SET = epics.pv('GF:GAS_FLOW_SET')
GAS_FLOW_PUFF_SET = epics.pv('GF:GAS_FLOW_PUFF_SET')
DRIVER_PRESS_SET = epics.pv('GF:DRIVER_PRESS_SET')
GAS_PEV_PUFF_SET = epics.pv('GF:GAS_PEV_PUFF_SET')
PID_P_SET = epics.pv('GF:PID_P_SET')
PID_I_SET = epics.pv('GF:PID_I_SET')
PID_D_SET = epics.pv('GF:PID_D_SET')
PEV_VAL_SET = epics.pv('GF:PEV_VAL_SET')
GF_1_GF_8 =  epics.pv('GF:1-GF:8')
GF_9_GF_16 =  epics.pv('GF:9-GF:16')

gas_supply = [GAS_PUFF_TRIG_MODE,GAS_PUFF_ON_OFF,GAS_FLOW_SET,GAS_FLOW_PUFF_SET,DRIVER_PRESS_SET,GAS_PEV_PUFF_SET,PID_P_SET,PID_I_SET,PID_D_SET,PEV_VAL_SET,GF_1_GF_8,GF_9_GF_16]

'''射频系统'''

RF_FIX_POW_SET = epics.pv('RF:FIX_POW_SET')

'''PG 电源'''
PG_VOL_SET = epics.pv('PG_VOL_SET')
PG_CUR_SET = epics.pv('PG_CUR_SET')

'''引出电源'''
EXT_VOL_SET = epics.pv('EXTR:VOL_SET')
EXT_CUR_SET = epics.pv('EXTR:CUR_SET')

'''加速电源'''
ACCE_MAX_SET = epics.pv('ACCE:MAX_SET')
ACCE_MIN_SET = epics.pv('ACCE:MIN_SET')

'''腔体偏压电源'''
CHAMBER_BIAS_VOL_SET = epics.pv('CHAMBER_BIAS:VOL_SET')

'''时序控制系统'''
TIMING_STR_SET1_TIMING_STR_SET16 = epics.pv('TIMING_STR_SET1-TIMING_STR_SET16')
TIMING_END_SET1_TIMING_END_SET16 = epics.pv('TIMING_END_SET1-TIMING_END_SET16')

'''灯丝偏压'''
BIAS_VOL_SET = epics.pv('BIAS_VOL_SET')
BIAS_CUR_SET = epics.pv('BIAS_CUR_SET')

'''灯丝加热'''
HEAT_VOL_SET = epics.pv('HEAT_VOL_SET')
HEAT_CUR_SET = epics.pv('HEAT_CUR_SET')

'''连接数据库'''
conn = pymysql.connect(host='192.168.127.200', port=3306, user='root', passwd='wangsai', db='nis_hsdd', charset='utf8')
cur = conn.cursor()
# 遍历pv,获取pv中的值

# 数据库存储，如果存储为None 则表示该EPICS 并不在线
for i in range(1000):
    print('PV_Value 第',i,'次 is:',pv.value)


    sql = "insert into test_table(GAS_PUFF_TRIG_MODE.GAS_PUFF_ON_OFF) " \
          "values(%f)" \
          %(10)
    # 执行SQL, new_list是执行参数, 用于替换上面SQL中的占位符%s,%s,%s
    cur.execute(sql)
    conn.commit()
    time.sleep(1)
