from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from futusd.domain.entities import SpendingDM


class SpendingSaver(Protocol):
    @abstractmethod
    async def save(self, spending: SpendingDM) -> None:
        ...


class SpendingDeleter(Protocol):
    @abstractmethod
    async def del_by_uuid(self, uuid: str) -> str | None:
        ...


class SpendingReader(Protocol):
    @abstractmethod
    async def read_by_uuid(self, uuid: str) -> SpendingDM | None:
        ...


class AllSpendingReader(Protocol):
    @abstractmethod
    async def read_all(self) -> list[SpendingDM]:
        ...

class GenerateUUID(Protocol):
    def __call__(self) -> UUID:
        ...

class DBSession(Protocol):
    async def commit(self) -> None:
        ...

class AIAnalyze(Protocol):
    @abstractmethod
    async def analyze_saver(self, spending: list[SpendingDM]) -> str:
        ...

class RegisterUser(Protocol):
    @abstractmethod
    async def register(self, session_id: str, user_uuid: str) -> str:
        ...

class InLoginUser(Protocol):
    @abstractmethod
    async def get_user_uuid(self, session_id: str) -> str | None:
        ...

class DeleteUser(Protocol):
    @abstractmethod
    async def delete(self, session_id: str) -> str | None:
        ...