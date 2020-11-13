import pymongo
import datetime

class MongoDB(object):
    def __init__(self, db):
        mongo_client = self._connect('127.0.0.1', 27017, '', '', db)     #连接
        self.db_loginfo = mongo_client['loginfo']                        #数据库
        self.collection_test = self.db_loginfo['test_collections']       #数据集

    def _connect(self, host, port, user, pwd, db):
        mongo_info = self._splicing(host, port, user, pwd, db)    #mongoDB官方语法
        mongo_client = pymongo.MongoClient(mongo_info, connectTimeoutMS=12000, connect=False)  #不需要长时间连接
        return mongo_client

    @staticmethod
    def _splicing(host, port, user, pwd, db):
        client = 'mongodb://' + host + ":" + str(port) + "/"
        if user != '':
            client = 'mongodb://' + user + ':' + pwd + '@' + host + ":" + str(port) + "/"   #客户端
            if db != '':
                client += db   # 数据库
        return client


    def test_insert(self):
        testCollection = dict()
        testCollection['name'] = '黄鸿波'
        testCollection['job'] = 'programmer'
        testCollection['dates'] = datetime.datetime.utcnow()
        self.collection_test.insert_one(testCollection)

        for info in self.collection_test.find():
            print(info)


if __name__ == '__main__':
    mongo = MongoDB(db='test')
    mongo.test_insert()
