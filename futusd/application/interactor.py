from datetime import date

from futusd.application import interfaces
from futusd.application.dto import CashOutDTO
from futusd.domain import entities


class GetSpendingInteractor:
    def __init__(self, get_spending: interfaces.SpendingReader) -> None:
        self._get_spending=get_spending

    async def __call__(self, uuid: str) ->  entities.CashOutDM | None:
        return await self._get_spending.read_by_uuid(uuid)


class NewSpendingInteractor:
    def __init__(
            self,
            db_session: interfaces.DBSession,
            get_spending: interfaces.SpendingReader,
            generate_uuid: interfaces.GenerateUUID
    ) -> None:
        self._db_session=db_session
        self._get_spending=get_spending
        self._generate_uuid=generate_uuid

    async def __call__(self, dt: CashOutDTO) -> str:
        uuid = str(self._generate_uuid())
        date_add = date.today()
        spending = entities.CashOutDM(
            uuid=uuid,
            base=dt.base,
            category=dt.category,
            date=date_add
        )

        await self._get_spending.save(spending)
        await self._db_session.commit()
        return uuid

