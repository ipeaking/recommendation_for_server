#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |// '.
#                 / \\|||  :  |||// \
#                / _||||| -:- |||||- \
#               |   | \\\  -  /// |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG
# @Time    : 2020-09-12 10:58
# @Author  : Hongbo Huang
# @File    : kafka_producer.py
from kafka import KafkaProducer
from kafka.errors import KafkaError
import time


def main(topic, msg):
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])     #生成者
    t = time.time()
    for i in range(10):
        future = producer.send(topic, msg)       #发送主题和信息
        try:
            record_metadata = future.get(timeout=10) #每隔10S发送一次数据   
            print(record_metadata)
        except KafkaError as e:
            print(e)

    print(time.time() - t)


if __name__ == '__main__':
    main("recommendation", b"hello")