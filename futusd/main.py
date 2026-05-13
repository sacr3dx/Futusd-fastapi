from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from futusd.config import Config
from futusd.controllers.http import spending_router
from futusd.controllers.ai import ai_router
from futusd.ioc import AppProvider

config = Config()
container = make_async_container(AppProvider(), context={Config: config})

def get_app() -> FastAPI:
    app = FastAPI(title="Futusd")
    app.include_router(spending_router)
    app.include_router(ai_router)
    setup_dishka(container, app)
    return app
