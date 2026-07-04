from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Response, Request, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from futusd.controllers.schemas import UserCreateSchema, UserLoginSchema
from futusd.application.dto import UserDTO, LoginDTO
from futusd.application.interactor import (
    UserRegisterInteractor,
    UserLoginInteractor,
    UserLogoutInteractor
)

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

@session_router.post("/login")
async def login_user(
        data: UserLoginSchema,
        response: Response,
        interactor: FromDishka[UserLoginInteractor]
) -> dict:

    dto = LoginDTO(
        username=data.username,
        password=data.password
    )

    session_id = await interactor(dto)

    if not  session_id:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Wrong password or username"
        )

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=3600
    )
    return {"message": "Success"}

@session_router.post("/logout")
async def logout_user(
        request: Request,
        response: Response,
        interactor: FromDishka[UserLogoutInteractor]
) -> dict:

    if not request.cookies.get("session_id"):
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="The user is not logged in"
        )

    session_id = request.cookies.get("session_id")
    await interactor(session_id)
    response.delete_cookie("session_id")

    return {"message": "Logged out success"}


