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

    async def flush(self) -> None:
        ...