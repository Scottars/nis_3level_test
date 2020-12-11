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

    sql = "SELECT v_data,v_data_time FROM v_data_monitor where register_id = 1 LIMIT 100000"
    cur.execute(sql)
    numinbase = 0
    lastdata=0

############ test  测试锯齿波
    # find star 找到其实的查询点
    start_index = 0
    lastdata = -10
    flag_start = False
    flag_firstseveralpoint = True
    decrese_error = 80

    samplepoint_num=1
    samplepoint_numList=[]
    jishu = 0
    for  col in (cur):
        jishu+=1
        #
        #
        # # print(col)
        if not flag_start:
            print('col[0]',col[0], 'last data :' ,lastdata)
            if col[0]>lastdata:
                start_index += 1
                lastdata=col[0]
                continue
            else:
                flag_start=True
                print(start_index)
                lastdata = -10

        else:
            # print(samplepoint_num)
            # print('col[0]', col[0], 'last data :', lastdata)
            if flag_firstseveralpoint:
                samplepoint_num += 1
                decrese_error -= 1
                if decrese_error == 0:
                    flag_firstseveralpoint = False
                    lastdata = -10
            else:

                if col[0]>lastdata or col[0] > 1.6:
                    samplepoint_num += 1
                    lastdata=col[0]
                else:

                    print('test sample legnth:',samplepoint_num)
                    samplepoint_numList.append(samplepoint_num)
                    samplepoint_num=1
                    decrese_error = 80
                    flag_firstseveralpoint = True

    f = open('demo.txt', 'w')
    k=''
    linecount = 10
    for i in samplepoint_numList:
        linecount -=1
        if linecount ==0:
            linecount = 10
            k+='\n'
        k += str(i) + ','
    f.write(k + "\n")
    f.close()
    # print('Total package:',numinbase)
    # print('Lost packages:',packagelost)
    # print("Package loss rate",packagelost/numinbase)


# 选择正负5v的电压的输入，此时通过直接判断0以上的数据的个数和0 以下的数据的个数，或者前后的deltau的变化。

