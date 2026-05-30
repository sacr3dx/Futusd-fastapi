from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from futusd.application.interfaces import (
    SpendingReader,
    SpendingSaver,
    AllSpendingReader,
    SpendingDeleter
)
from futusd.domain.entities import SpendingDM
from futusd.infrastructure.models.spending_model import CashOutModel

class SpendingGateway(
    SpendingReader,
    SpendingSaver,
    AllSpendingReader,
    SpendingDeleter
):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def read_by_uuid(self, uuid: str) -> SpendingDM | None:
        query = select(CashOutModel).where(
            CashOutModel.uuid == uuid
        )
        result = await self._session.execute(query)
        row = result.scalar_one_or_none()
        if not row:
            return None
        return SpendingDM(
            uuid=row.uuid,
            base=row.base,
            category=row.category,
            date=row.date
        )


    async def del_by_uuid(self, uuid: str) -> str | None:
        query = select(CashOutModel).where(
            CashOutModel.uuid == uuid
        )
        result = await self._session.execute(query)
        obj = result.scalar_one_or_none()
        if obj:
            await self._session.delete(obj)
            await self._session.commit()


    async def read_all(self) -> list[SpendingDM]:
        result = await self._session.execute(select(CashOutModel))
        rows = result.scalars().all()
        spending= [
            SpendingDM(
                uuid=str(row.uuid),
                base=row.base,
                category=row.category,
                date=row.date
            )
            for row in rows
        ]
        if not rows:
            return []
        return spending


    async def save(self, spending: SpendingDM) -> None:
        model = CashOutModel(
            uuid=spending.uuid,
            base=spending.base,
            category=spending.category,
            date=spending.date
        )
        self._session.add(model)
        await self._session.commit()
