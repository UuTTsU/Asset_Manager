from functools import lru_cache
from typing import Annotated
from fastapi import Depends, FastAPI
from app.core import config

app = FastAPI()

@lru_cache
def get_settings():
    return config.Settings()

@app.get("/info")
async def info(settings: Annotated[config.Settings, Depends(get_settings)]):
    return {
        "App_name": settings.app_name,

    }
