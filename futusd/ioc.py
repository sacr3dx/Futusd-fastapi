from typing import AsyncIterable
from uuid import uuid4

from dishka import Provider, Scope, provide, AnyOf, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from futusd.application import interfaces
from futusd.application.interactor import (
    GetSpendingInteractor,
    AllSpendingInteractor,
    NewSpendingInteractor,
    DeleteSpendingInteractor,
    AIAnalyzeInteractor
)
from futusd.application.interfaces import AIAnalyze
from futusd.application.interfaces import DBSession

from futusd.config import Config
from futusd.infrastructure.database.database import new_session_maker
from futusd.infrastructure.database.gateways import SpendingGateway
from futusd.infrastructure.ai.groq import GroqAdapter

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

    @provide(scope=Scope.APP)
    def get_groq_adapter(self, config: Config) -> AIAnalyze:
        return GroqAdapter(api_key=config.groq.api_key)

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

    get_spending_interactor = provide(GetSpendingInteractor, scope=Scope.REQUEST)
    all_spending_interactor = provide(AllSpendingInteractor, scope=Scope.REQUEST)
    del_spending_interactor = provide(DeleteSpendingInteractor, scope=Scope.REQUEST)
    new_spending_interactor = provide(NewSpendingInteractor, scope=Scope.REQUEST)

    ai_analyze_interactor = provide(AIAnalyzeInteractor, scope=Scope.REQUEST)
    config = from_context(provides=Config, scope=Scope.APP)