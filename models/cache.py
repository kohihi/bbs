
class Cache(object):
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value


class RedisCache(Cache):
    import redis
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def get(self, key):
        return RedisCache.redis_db.get(key)

    def set(self, key, value):
        RedisCache.redis_db.set(key, value)