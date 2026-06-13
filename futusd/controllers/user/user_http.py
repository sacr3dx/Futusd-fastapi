from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter

from futusd.controllers.schemas import UserCreateSchema
from futusd.application.dto import UserDTO
from futusd.application.interactor import UserRegisterInteractor

session_router = APIRouter(prefix="/auth", route_class=DishkaRoute, tags=["User_session"])

@session_router.post("/registration")
async def register_user(
        data: UserCreateSchema,
        interactor: FromDishka[UserRegisterInteractor]
) -> str:

    dto = UserDTO(
        username=data.username,
        password=data.password
    )
    uuid = await interactor(dto)
    return uuid