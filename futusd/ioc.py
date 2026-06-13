from typing import AsyncIterable
from uuid import uuid4
from redis.asyncio import Redis

from passlib.context import CryptContext

from dishka import Provider, Scope, provide, AnyOf, from_context
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from futusd.application import interfaces
from futusd.application.interactor import (
    GetSpendingInteractor,
    AllSpendingInteractor,
    NewSpendingInteractor,
    DeleteSpendingInteractor,
    UserRegisterInteractor,
    AIAnalyzeInteractor
)
from futusd.application.interfaces import AIAnalyze
from futusd.application.interfaces import DBSession

from futusd.config import Config
from futusd.infrastructure.database.database import new_session_maker
from futusd.infrastructure.database.gateways import SpendingGateway, UserGateway
from futusd.infrastructure.ai.groq_client import GroqAdapter
from futusd.infrastructure.session.redis_client import new_redis_client


class AppProvider(Provider):

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.GenerateUUID:
        return uuid4

    @provide(scope=Scope.APP)
    def hashing_generate(self) -> CryptContext:
        return CryptContext(schemes=[bcrypt])

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    def get_redis(self, config: Config) -> Redis:
        return new_redis_client(config.redis)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[
        AsyncSession,
        DBSession
    ]]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_groq_adapter(self, config: Config) -> AIAnalyze:
        return GroqAdapter(config.groq)

    spending_gateways = provide(
        SpendingGateway,
        scope = Scope.REQUEST,
        provides=AnyOf[
            interfaces.SpendingReader,
            interfaces.AllSpendingReader,
            interfaces.SpendingSaver,
            interfaces.SpendingDeleter
        ]
    )

    user_gateway = provide(
        UserGateway,
        scope=Scope.REQUEST,
        provides=interfaces.RegisterUser
    )

    get_spending_interactor = provide(GetSpendingInteractor, scope=Scope.REQUEST)
    all_spending_interactor = provide(AllSpendingInteractor, scope=Scope.REQUEST)
    del_spending_interactor = provide(DeleteSpendingInteractor, scope=Scope.REQUEST)
    new_spending_interactor = provide(NewSpendingInteractor, scope=Scope.REQUEST)

    user_register_interactor = provide(UserRegisterInteractor, scope=Scope.REQUEST)

    ai_analyze_interactor = provide(AIAnalyzeInteractor, scope=Scope.REQUEST)
    config = from_context(provides=Config, scope=Scope.APP)