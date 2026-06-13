from redis.asyncio import Redis
from futusd.config import RedisConfig

def new_redis_client(redis_config: RedisConfig) -> Redis:
    return Redis(
        host=redis_config.host,
        port=redis_config.port,
        decode_responses=True
    )