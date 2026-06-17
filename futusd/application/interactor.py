from datetime import date

from passlib.context import CryptContext

from futusd.application import interfaces
from futusd.application.dto import SpendingDTO, UserDTO, LoginDTO
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
            generate_uuid: interfaces.GenerateUUID,
            pwd_context: CryptContext
    ) -> None:
        self._db_session = db_session
        self._user_saver=user_saver
        self._generate_uuid=generate_uuid
        self._pwd_context=pwd_context

    async def __call__(self, dt: UserDTO) -> str:
        uuid = str(self._generate_uuid())
        hash_password = self._pwd_context.hash(dt.password)
        user = entities.UserDM(
            uuid = uuid,
            username = dt.username,
            hashed_password=hash_password
        )
        await self._user_saver.register(user)
        await self._db_session.commit()
        return uuid


class UserLoginInteractor:
    def __init__(
            self,
            user_reader: interfaces.ReadUser,
            login_user: interfaces.InLoginUser,
            generate_uuid: interfaces.GenerateUUID,
            pwd_context: CryptContext
    ) -> None:
        self._user_reader = user_reader
        self._login_user = login_user
        self._generate_uuid = generate_uuid
        self._pwd_context = pwd_context

    async def __call__(self, dt: LoginDTO):
        user = await self._user_reader.get_by_username(dt.username)
        if not user:
            raise ValueError("User is not found")

        checked_password = self._pwd_context.verify(dt.password, user.hashed_password)

        if not checked_password:
            raise ValueError("Wrong password")

        session_id = str(self._generate_uuid())
        return await self._login_user.login(session_id, user.uuid)