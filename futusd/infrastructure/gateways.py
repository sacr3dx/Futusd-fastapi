from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from futusd.application.interfaces import SpendingReader, SpendingSaver
from futusd.domain.entities import CashOutDM
from futusd.infrastructure.models import CashOutModel

class SpendingGateway(SpendingReader, SpendingSaver):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def read_by_uuid(self, uuid: str) -> CashOutDM | None:
        query = select(CashOutModel).where(
            CashOutModel.uuid == uuid
        )
        result = await self._session.execute(query)
        row = result.scalar_one_or_none()
        if not row:
            return None
        return CashOutDM(
            uuid=row.uuid,
            base=row.base,
            category=row.category,
            date=row.date
        )

    async def save(self, spending: CashOutDM) -> None:
        model = CashOutModel(
            uuid=spending.uuid,
            base=spending.base,
            category=spending.category,
            date=spending.date
        )
        self._session.add(model)
        await self._session.commit()
