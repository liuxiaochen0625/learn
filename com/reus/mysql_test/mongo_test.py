#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'练习使用mongodb'

from pymongo import MongoClient

user = 'reus'

# 连接数据库(连接之前需要先打开mongodb数据库)
# client = MongoClient()  # 最简单的连接
# client = MongoClient('loaclhost', 270171)  # 指定端口和数据库地址进行连接
client = MongoClient('mongodb://192.168.21.180:27017')  # 使用url地址进行连接

db = client['test']

print(db.collection_names())

collection = db['example3']

print(collection.find_one())

for item in collection.find():
    print(item)

# 关闭连接
client.close()
