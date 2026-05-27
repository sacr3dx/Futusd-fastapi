from datetime import date

from futusd.application import interfaces
from futusd.application.dto import SpendingDTO
from futusd.domain import entities


class GetSpendingInteractor:
    def __init__(self, get_spending: interfaces.SpendingReader) -> None:
        self._get_spending=get_spending

    async def __call__(self, uuid: str) -> entities.SpendingDM | None:
        return await self._get_spending.read_by_uuid(uuid)


class AllSpendingInteractor:
    def __init__(self, get_all_spending: interfaces.AllSpendingReader) -> None:
        self._get_all_spending=get_all_spending

    async def __call__(self) -> list[entities.SpendingDM]:
        return await self._get_all_spending.read_all()



class NewSpendingInteractor:
    def __init__(
            self,
            db_session: interfaces.DBSession,
            get_spending: interfaces.SpendingSaver,
            generate_uuid: interfaces.GenerateUUID
    ) -> None:
        self._db_session=db_session
        self._get_spending=get_spending
        self._generate_uuid=generate_uuid

    async def __call__(self, dt: SpendingDTO) -> str:
        uuid = str(self._generate_uuid())
        date_add = date.today()
        spending = entities.SpendingDM(
            uuid=uuid,
            base=dt.base,
            category=dt.category,
            date=date_add
        )

        await self._get_spending.save(spending)
        await self._db_session.commit()
        return uuid


class DeleteSpendingInteractor:
    def __init__(
            self,
            db_session: interfaces.DBSession,
            del_spending: interfaces.SpendingDeleter
    ) -> None:
        self._db_session=db_session
        self._del_spending=del_spending

    async def __call__(self, uuid: str) -> str | None:
        await self._del_spending.del_by_uuid(uuid)
        await self._db_session.commit()
        return f'{uuid} has been deleted'


class AIAnalyzeInteractor:
    def __init__(
            self,
            get_saver: interfaces.AIAnalyze,
            get_all_spending: interfaces.AllSpendingReader
    ) -> None:
        self._get_saver=get_saver
        self._get_all_spending=get_all_spending

    async def __call__(self) -> str:
        spending = await self._get_all_spending.read_all()
        return await self._get_saver.analyze_saver(spending)


class UserRegisterInteractor:
    def __init__(
            self,
            db_session: interfaces.DBSession,
            user_saver: interfaces.RegisterUser,
            generate_uuid: interfaces.GenerateUUID
    ) -> None:
        self._db_session = db_session
        self._user_saver=user_saver
        self._generate_uuid=generate_uuid

    async def __call__(self, dt: entities.UserDM) -> str:
        uuid = str(self._generate_uuid())


        user = entities.UserDM(
            uuid = uuid,
            username = dt.username,
            hashed_password=dt.hashed_password
        )
        await self._user_saver.register(user)
        await self._db_session.commit()
        return uuid
