from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Path, HTTPException
from typing import Annotated
from uuid import UUID

from starlette.status import HTTP_404_NOT_FOUND

from futusd.application.interactor import NewSpendingInteractor, GetSpendingInteractor
from futusd.application.dto import CashOutDTO
from futusd.controllers.schemas import SpendingSchema

spending_router = APIRouter(prefix="/spending", route_class=DishkaRoute)

@spending_router.get("/{spending_id:uuid}")
async def get_spending(
        spending_id: Annotated[UUID, Path(description="Spending_ID", title="Spending_ID")],
        interactor: FromDishka[GetSpendingInteractor]
)->SpendingSchema:
    spending_dm = await interactor(uuid=str(spending_id))

    if not spending_dm:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Spending not found"
        )

    return SpendingSchema(
        base=spending_dm.base,
        category=spending_dm.category,
        date=spending_dm.date
    )


@spending_router.post("/spending_add")
async def add_spending(
        data: SpendingSchema,
        interactor: FromDishka[NewSpendingInteractor]
) -> str:

    dto = CashOutDTO(
        base=data.base,
        category=data.category
    )
    uuid = await interactor(dto)
    return uuid
