import redis

host = 'localhost'
#host = '192.168.0.246:49154'

class RedisManager:

    def __init__(self):
        self.r = r = redis.Redis(host=host, port=6379, charset="utf-8", decode_responses=True)

    @staticmethod
    def set_remaining_counter(x):
        r = redis.Redis(host=host, port=6379, charset="utf-8", decode_responses=True)
        r.set("remaining", x.strip())


    @staticmethod
    def get_remaining_counter():
        r = redis.StrictRedis(host=host, port=6379)
        return int(r.get("remaining"))
