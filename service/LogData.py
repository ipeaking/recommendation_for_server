from dao import mongo_db
from datetime import datetime
from dao import redis_db


class LogData(object):
    def __init__(self):
        self._mongo = mongo_db.MongoDB(db='test')
        self._redis = redis_db.Redis()

    def insert_log(self, user_id, content_id, title, tables):
        collections = self._mongo.db_loginfo[tables]
        info = {}
        info['user_id'] = user_id
        info['content_id'] = content_id
        info['title'] = title
        info['date'] = datetime.utcnow()
        collections.insert_one(info)
        return True


    def get_logs(self, user_id, tables):
        collections = self._mongo.db_loginfo[tables]
        data = collections.find(
            {"user_id": user_id}
        )
        results = []
        for x in data:
            results.append(x)

        return results

    def modify_article_detail(self, key, ops):
        try:
            info = self._redis.redis.get(key)
            info = eval(info)
            print(info)
            # info[ops] += 1
            # self._redis.redis.set(key, str(info))
            return True
        except Exception as e:
            return False


if __name__ == '__main__':
    log_data = LogData()
    print(log_data.modify_article_detail("news_detail:5f5246f8e15b93a6c8d926af", "likes"))
    # print(log_data.modify_article_detail("news_detail:5f52468fe15b93a6c8d9202d", "read"))
