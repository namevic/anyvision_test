import redis

from config.settings import redis_config

redis_pool = redis.ConnectionPool(**redis_config)


def get_redis():
    return redis.Redis(connection_pool=redis_pool)
