#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 导入mysql模块
import pymysql

try:
    # 打开数据库链接  这些信息需要换成你自己的
    # host:数据库地址,
    # port:数据库端口
    # user:数据库连接的用户名,
    # passwd:数据库连接的密码,
    # db: 数据库名
    # charset:数据库的编码格式
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='canal', charset='utf8')
    with conn:
        cur = conn.cursor()
        # 文件路径, 自己修改
        file_path = 'data/PV1.log'
        # 打开文件 r: 表示以只读的方式 , encoding='utf-8' : 指定读取文件的格式为utf-8编码
        file = open(file_path, 'r', encoding='utf-8')
        # 遍历文件的每一行
        for line in file:
            # strip() 去除字符串前后的空字符包括空格符,回车符,制表符tab, split(" ")表示用" "空格符分隔字符串
            # 一行文本的内容是 ginkgo:aiExample.VAL 2018-11-29 21:15:55.72276 4
            # 所以分隔以后是一个长度为4的数组, 分别是pv名,年月日,时分秒,pv值
            line_list = line.strip().split(" ")
            print(line_list)
            # 重新组合数组, 把年月日和时分秒合在一起, 构成一个元组, 关于为什么要使用元组, 规范! 优先使用元组而不是数组
            new_list = (line_list[0], line_list[1] + " " + line_list[2], line_list[3])
            print(new_list)
            # 定义SQL, 因为主键ID是自增的, 所以不需要插入主键,只需要插入其他三个值
            # pv_data 表名  `pv_name`,`created_at`,`value`是表的三个字段名, %s,%s,%s 是三个占位符
            sql = "insert into `pv_data`(`pv_name`,`created_at`,`value`) values(%s,%s,%s)"
            # 执行SQL, new_list是执行参数, 用于替换上面SQL中的占位符%s,%s,%s
            cur.execute(sql, new_list)
# 捕获异常
except Exception as e:
    # 打印异常信息
    print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
