from functools import lru_cache
from typing import Annotated
from fastapi import Depends, FastAPI
from app.core import config
from app.routers.auth import router as auth_router

app = FastAPI()


@lru_cache
def get_settings():
    return config.Settings()

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "App_name": settings.app_name,

    }

app.include_router(auth_router, prefix="/auth")

