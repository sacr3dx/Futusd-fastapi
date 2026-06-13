# from redis.asyncio import Redis
#
# from futusd.application.interfaces import RegisterUser, InLoginUser, LogoutUser
#
# class SessionGateway(
#     RegisterUser,
#     InLoginUser,
#     LogoutUser
# ):
#     def __init__(self, redis_client: Redis) -> None:
#         self._redis = redis_client
#
#     async def register(self, user) -> None:
#         model = UsersModel(
#             uuid=user.uuid,
#             username=user.username,
#             hashed_password=user.hashed_password
#         )
#         self._redis.add(model)
#
#     async def login(self, session_id: str) -> str | None:
#         # session_id= session_id
#         # await self._redis.setex(
#         #     name=f"session:{session_id}",
#         #     time=3600,
#         #     value=user_uuid
#         # )
#         # return session_id
#         return await self._redis.get(f"session:{session_id}")
#
#     async def logout(self, session_id: str) -> str | None:
#         return await self._redis.delete(f"session:{session_id}")

