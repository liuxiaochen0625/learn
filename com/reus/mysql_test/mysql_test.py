#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'练习使用mysql'

import pymysql

author = 'reus'


try:
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='mysql', db='sys', port=3306)
    # 检验数据库是否连接成功
    cursor = db.cursor()
    # 执行数据库查询语句
    data = cursor.execute("select * from sys_config")
    # 获取其中一条数据
    one = cursor.fetchone()
    all = cursor.fetchall()
    print(data)
    print(one)
    print(all)
except pymysql.Error as e:
    print(e)
    print('数据库连接失败')
finally:
    if db:
        db.close()
