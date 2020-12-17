# 实现对数据库中的波形进行校核
# 1、对接收到的数据实现数据校验和计数
#       例如是锯齿波，我们将实现计算每一个周期下，我们可以采样多少个数据点。
#
#   2 此程序用于验证系统的采样的不良率
#
#
# 数据库测试脚本

import  pymysql

if __name__ =="__main__":

    db = pymysql.connect(host='localhost', user='scottar', password='123456', db='nis_hsdd', port=3306, charset='utf8')
    cur = db.cursor()
    msgResult = ''

    sql = "SELECT v_data,v_data_time FROM v_data_monitor where register_id = 2 LIMIT 10000"
    cur.execute(sql)

############ test  测试三角波
    # 三角波的峰峰值：5v，-2.5v->2.5v  2.5v->-2.5v
    #  50KHz对应20us，每5即采样20个点，此时，准确来说，上升区间10个点， 每个点对应0.5v的大小，
    #  下降区间每个点对应0.5v 的大小，考虑一些信号源的抖动问题以及采样的浮动问题

    # find star 找到其实的查询点
    lastdata = -10
    samplepoint_num=1
    samplepoint_numList=[]
    deltaV = 0.8
    for col in (cur):
        lastdata = col[0]
        break
    num_count = 0
    error_count = 0
    for col in (cur):
        num_count += 1
        if abs(col[0] - lastdata) <= deltaV:

            lastdata = col[0]
        else:
            print('col:',col[0],'lastdata:',lastdata)
            lastdata = col[0]

            error_count += 1
        pass

    print('error count:', error_count)
    print('num count:', num_count)
    print('不良率：',error_count/num_count)
    # f = open('demo.txt', 'w')
    # k=''
    # linecount = 10
    # for i in samplepoint_numList:
    #     linecount -=1
    #     if linecount ==0:
    #         linecount = 10
    #         k+='\n'
    #     k += str(i) + ','
    # f.write(k + "\n")
    # f.close()
    # print('Total package:',numinbase)
    # print('Lost packages:',packagelost)
    # print("Package loss rate",packagelost/numinbase)


# 选择正负5v的电压的输入，此时通过直接判断0以上的数据的个数和0 以下的数据的个数，或者前后的deltau的变化。

