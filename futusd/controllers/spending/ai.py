from dishka.integrations.fastapi import FromDishka, DishkaRoute
from fastapi import APIRouter

from futusd.application.interactor import AIAnalyzeInteractor
from futusd.controllers.schemas import AIAnalyzeResponse

ai_router = APIRouter(prefix="/ai_functional", route_class=DishkaRoute, tags=["AI_function"])

@ai_router.get("/analyze_all")
async def analyze_all(
        interactor: FromDishka[AIAnalyzeInteractor]
) -> AIAnalyzeResponse:
    result = await interactor()
    return AIAnalyzeResponse(message=result)