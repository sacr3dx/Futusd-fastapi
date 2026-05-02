from typing import AsyncIterable
from uuid import uuid4

from dishka import Provider, Scope, provide, AnyOf, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from futusd.application import interfaces
from futusd.application.interactor import (
    GetSpendingInteractor,
    NewSpendingInteractor
)
from futusd.application.interfaces import DBSession

from futusd.config import Config
from futusd.infrastructure.database import new_session_maker
from futusd.infrastructure.gateways import SpendingGateway


class AppProvider(Provider):

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.GenerateUUID:
        return uuid4

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AnyOf[
        AsyncSession,
        DBSession
    ]]:
        async with session_maker() as session:
            yield session

    spending_gateways = provide(
        SpendingGateway,
        scope = Scope.REQUEST,
        provides=AnyOf[
            interfaces.SpendingReader,
            interfaces.SpendingSaver]
    )

    get_spending_interactor = provide(GetSpendingInteractor, scope=Scope.REQUEST)
    new_spending_interactor = provide(NewSpendingInteractor, scope=Scope.REQUEST)
    config = from_context(provides=Config, scope=Scope.APP)