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
# @Time    : 2020-09-12 11:11
# @Author  : Hongbo Huang
# @File    : kafka_consumer.py
from kafka import KafkaConsumer
from kafka.structs import TopicPartition
import time


class Consumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            group_id="test",          # 用户所在的组
            auto_offset_reset="earliest",   # 用户的位置
            enable_auto_commit=False,  # enable.auto.commit 设置为 true，既可能重复消费，也可能丢失数据
            bootstrap_servers=["localhost:9092"]  # Kafka群集信息列表，用于连接kafka集群，如果集群中机器数很多，只需要指定部分的机器主机的信息即可
        )

    def consumer_data(self, topic, partition):
        my_partition = TopicPartition(topic=topic, partition=partition)   #指定消费者的消费分区,topic下,partition的消息
        self.consumer.assign([my_partition])

        print(f"consumer start position:{self.consumer.position(my_partition)}")

        try:
            while True:
                poll_num = self.consumer.poll(timeout_ms=1000, max_records=5)  #Kafka轮询一次就相当于拉取（poll）一定时间段broker中可消费的数据，在这个指定时间段里拉取，时间到了就立刻返回数据
                if poll_num == {}:
                    print("empty")
                    exit(1)   #exit(1)表示异dao常退出，在退出前可以给du出一些zhi提示信息，或在调试程序中察dao看出错原回因
                for key, record in poll_num.items():
                    for message in record:
                        # 数据处理
                        print(
                            #以 f 开头，包含的{}表达式在程序运行时会被表达式的值代替
                            f"{message.topic}:{message.partition}:{message.offset}: key={message.key} value={message.value}")

                try:
                    self.consumer.commit_async()  #成功消费后,手动返回,进行下一次迭代
                    time.sleep(0.05)

                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

        finally:
            try:
                self.consumer.commit()    #最后将消费者提交
            finally:
                self.consumer.close()     #消费结束

def main():
    topic = "recommendation"
    partition = 0
    my_consumer = Consumer()
    my_consumer.consumer_data(topic, partition)


if __name__ == '__main__':
    main()

