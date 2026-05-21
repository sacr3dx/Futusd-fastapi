import redis.asyncio as redis
from futusd.config import RedisConfig

def new_redis_client(redis_config: RedisConfig) -> redis.Redis:
    return redis.Redis(
        host=redis_config.host,
        port=redis_config.port,
        decode_responses=True
    )