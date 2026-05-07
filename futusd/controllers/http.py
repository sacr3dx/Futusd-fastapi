from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter, Path, HTTPException
from typing import Annotated
from uuid import UUID

from starlette.status import HTTP_404_NOT_FOUND

from futusd.application.interactor import (
    NewSpendingInteractor,
    GetSpendingInteractor,
    AllSpendingInteractor,
    DeleteSpendingInteractor
)
from futusd.application.dto import SpendingDTO
from futusd.domain.entities import SpendingDM
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

@spending_router.get('/all_spending')
async def get_all_spending(
        interactor: FromDishka[AllSpendingInteractor]
) -> list[SpendingDM]:
    all_spending = await interactor()

    if not all_spending:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Spending not found"
        )

    return all_spending

@spending_router.delete("/{spending_id:uuid}")
async def delete_spending(
        spending_id: Annotated[UUID, Path(description="Spending_ID", title="Spending_ID")],
        interactor: FromDishka[DeleteSpendingInteractor]
) -> str:

    del_spending = await interactor(uuid = str(spending_id))
    if not del_spending:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Spending not found"
        )
    return f'{spending_id} has been deleted'

@spending_router.post("/spending_add")
async def add_spending(
        data: SpendingSchema,
        interactor: FromDishka[NewSpendingInteractor]
) -> str:

    dto = SpendingDTO(
        base=data.base,
        category=data.category
    )
    uuid = await interactor(dto)
    return uuid
