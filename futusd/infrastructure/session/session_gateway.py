import redis.asyncio as redis

from futusd.application.interfaces import (
    RegisterUser,
    InLoginUser,
)

class SessionGateway(
    RegisterUser,
    InLoginUser
):
    def __init__(self, redis_client: redis.Redis) -> None:
        self._redis=redis_client

    async def register(self, session_id: str, user_uuid: str) -> str:
        session_id= session_id
        await self._redis.setex(
            name=f"session:{session_id}",
            time=3600,
            value=user_uuid
        )
        return session_id

    async def get_user_uuid(self, session_id: str) -> str | None:
        return await self._redis.get(f"session:{session_id}")

    async def delete(self, session_id: str) -> None:
        await self._redis.delete(f"session:{session_id}")
