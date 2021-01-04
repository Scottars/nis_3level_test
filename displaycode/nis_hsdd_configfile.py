'''
目标：对实时显示模块的参数的的配置
配置：zmq的连接的地址/UI刷新速度/

实现方式：
总计设定三个图像
（1） 最近1w个数据的实时显示
（2）数据累计的显示
（3）散点图显示
'''

# 基本设计说明
# req地址采用80xx  level 2 此处，同样是第二层的各个守护线程主动连接我们管理中心的线程
# req地址采用90xx level 3  此处，各个守护线程是实现主动去连接我们的管理中心的线程
# sub 地址采用50xx开始    此处，我们的实时显示模块管理中心想要获取，都是同样需要的是

# 水冷系统 01
level_2_01_udp_rcv_addr = '192.168.100.61'
level_2_01_udp_rcv_port = 5000

level_2_01_watercool_sub_addr = 'tcp://192.168.100.61:5222'
level_2_01_watercool_req_addr = 'tcp://192.168.100.61:9222'
level_3_01_watercool_req_addr = 'tcp://192.168.100.71:9333'
watercool_ui_intertal='10' #单位是ms

# 铯路系统 02
level_2_02_udp_rcv_addr = '192.168.100.62'
level_2_02_udp_rcv_port = 5000
level_2_02_cefurance_sub_addr = 'tcp://192.168.100.62:5222'
level_2_02_cefurance_req_addr = 'tcp://192.168.100.62:9222'
level_3_02_cefurance_req_addr = 'tcp://192.168.100.72:9333'
cefurance_ui_intertal='10' #单位是ms

#供气系统 03
level_2_03_udp_rcv_addr = '192.168.100.63'
level_2_03_udp_rcv_port = 5000
level_2_03_gascontrol_sub_addr = 'tcp://192.168.100.63:5222'
level_2_03_gascontrol_req_addr = 'tcp://192.168.100.63:9222'
level_3_03_gascontrol_req_addr = 'tcp://192.168.100.73:9333'
gascontrol_ui_intertal='10' #单位是ms

#磁场电源 04
level_2_04_udp_rcv_addr = '192.168.100.64'
level_2_04_udp_rcv_port = 5000
level_2_04_pgmpower_sub_addr = 'tcp://192.168.100.64:5222'
level_2_04_pgmpower_req_addr = 'tcp://192.168.100.64:9222'
level_3_04_pgmpower_req_addr = 'tcp://192.168.100.74:9333'
pgmpower_ui_intertal='10' #单位是ms

#灯丝电源 05
level_2_05_udp_rcv_addr = '192.168.100.65'
level_2_05_udp_rcv_port = 5000
level_2_05_filmentpower_sub_addr = 'tcp://192.168.100.65:5222'
level_2_05_filmentpower_req_addr = 'tcp://192.168.100.65:9222'
level_3_05_filmentpower_req_addr = 'tcp://192.168.100.75:9333'
filmentpower_ui_intertal='10' #单位是ms

#射频功率 06
level_2_06_udp_rcv_addr = '192.168.100.66'
level_2_06_udp_rcv_port = 5000
level_2_06_filmentpower_sub_addr = 'tcp://192.168.100.66:5222'
level_2_06_filmentpower_req_addr = 'tcp://192.168.100.66:9222'
level_3_06_filmentpower_req_addr = 'tcp://192.168.100.76:9333'
filmentpower_ui_intertal='10' #单位是ms


#引出电源 07
level_2_07_udp_rcv_addr = '192.168.100.67'
level_2_07_udp_rcv_port = 5000
level_2_07_leadintoutpower_sub_addr = 'tcp://192.168.100.67:5222'
level_2_07_leadintoutpower_req_addr = 'tcp://192.168.100.67:9222'
level_3_07_leadingoutpower_req_addr = 'tcp://192.168.100.77:9333'
leadingoutpower_ui_intertal='10' #单位是ms

#引出电源 08
level_2_08_udp_rcv_addr = '192.168.100.68'
level_2_08_udp_rcv_port = 5000
level_2_08_egpower_sub_addr = 'tcp://192.168.100.68:5222'
level_2_08_egpower_req_addr = 'tcp://192.168.100.68:9222'
level_3_08_egpower_req_addr = 'tcp://192.168.100.78:9333'
leadingoutpower_ui_intertal='10' #单位是ms





hs1_sub_addr = 'tcp://192.168.100.64:10000'
hs2_sub_addr = 'tcp://192.168.100.66:10001'
hs3_sub_addr = 'tcp://192.168.100.69:10002'
hs4_sub_addr = 'tcp://192.168.100.67:10003'
hs5_sub_addr = 'tcp://192.168.100.61:10004'



level2_hs1_req_addr = 'tcp://192.168.100.64:9222'
level3_hs1_req_addr = 'tcp://192.168.100.74:9333'
level2_hs2_req_addr = 'tcp://192.168.100.66:9222'
level3_hs2_req_addr = 'tcp://192.168.100.76:9333'
level2_hs3_req_addr = 'tcp://192.168.100.69:9222'
level3_hs3_req_addr = 'tcp://192.168.100.79:9333'
level2_hs4_req_addr = 'tcp://192.168.100.67:9222'
level3_hs4_req_addr = 'tcp://192.168.100.77:9333'
level2_hs5_req_addr = 'tcp://192.168.100.61:9222'
level3_hs5_req_addr = 'tcp://192.168.100.71:9333'


hs1_udp_recv_addr = '192.168.100.64'
hs1_udp_recv_port = 8080

hs2_udp_recv_addr = '192.168.100.65'
hs2_udp_recv_port = 8080

hs3_udp_recv_addr = '192.168.100.69'
hs3_udp_recv_port = 8080

hs4_udp_recv_addr = '192.168.100.67'
hs4_udp_recv_port = 8080

hs5_udp_recv_addr = '192.168.100.61'
hs5_udp_recv_port = 8080





Hs_TimeInterval = 1


level_3_para_read_req_addr  = 'tcp://192.168.100.99:10011'
