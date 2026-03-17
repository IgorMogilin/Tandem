from fastapi import FastAPI

from src.api.routers import users

app = FastAPI(
    title="Управление фондом оборотных средств",
    version="1.0",
)


@app.get("/")
async def root() -> dict:
    """
    Корневой маршрут, подтверждающий, что API работает
    """
    return {"message": "Добро пожаловать в API проекта Tandem"}


app.include_router(users.router)
