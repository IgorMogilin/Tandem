from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth import get_current_superadmin
from src.api.shemas.users import UserResponse, UserUpdate
from src.common.constants import USER_NOT_FOUND, USER_NOT_SELF_CHANGES
from src.db.depends import get_async_db
from src.db.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register",
    response_model=UserResponse,
    summary="Регистрация и получение пользователя из БД",
    description="Доступно всем пользователям. Используется при запуске бота",
)
async def create_user(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_async_db)],
    telegram_id: int = Body(..., description="Telegram ID пользователя"),
    name: str = Body(..., description="Имя пользователя"),
) -> UserResponse:
    """
    Регистрация нового пользователя в базе данных с присвоением роли Alien
    """
    result = await db.execute(select(User).where(User.telegram_id == telegram_id))
    db_user = result.scalar_one_or_none()
    if db_user:
        response.status_code = status.HTTP_200_OK
        return UserResponse.model_validate(db_user)
    db_user = User(telegram_id=telegram_id, name=name)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    response.status_code = status.HTTP_201_CREATED
    return UserResponse.model_validate(db_user)


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Получить всех зарегистрированных пользователей",
    description="Доступно только суперадминам",
)
async def get_all_user(
    db: Annotated[AsyncSession, Depends(get_async_db)],
    _: Annotated[UserResponse, Depends(get_current_superadmin)],
) -> list[UserResponse]:
    """
    Получение всех зарегистрированных пользователей. В том числе и неактивных
    """
    result = await db.scalars(select(User))
    users = result.all()
    return [UserResponse.model_validate(user) for user in users]


@router.get(
    "/{telegram_id}",
    response_model=UserResponse,
    summary="Получить пользователя по Telegram ID",
    description="Доступно только суперадминам",
)
async def get_user_by_telegram_id(
    db: Annotated[AsyncSession, Depends(get_async_db)],
    _: Annotated[UserResponse, Depends(get_current_superadmin)],
    telegram_id: int = Path(..., description="Telegram ID искомого пользователя"),
) -> UserResponse:
    """
    Получение конкретного пользователя по ID
    """
    db_user = await db.scalar(select(User).where(User.telegram_id == telegram_id))
    if not db_user:
        raise USER_NOT_FOUND
    return UserResponse.model_validate(db_user)


@router.patch("/{telegram_id}", summary="Обновление роли пользователя", description="Доступно только суперадминам")
async def update_user(
    new_role: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_async_db)],
    superadmin: Annotated[UserResponse, Depends(get_current_superadmin)],
    telegram_id: int = Path(..., description="Telegram ID искомого пользователя"),
) -> UserResponse:
    """
    Изменение роли пользователя по Telegram ID
    """
    if superadmin.telegram_id == telegram_id:
        raise USER_NOT_SELF_CHANGES
    db_user = await db.scalar(select(User).where(User.telegram_id == telegram_id))
    if not db_user:
        raise USER_NOT_FOUND
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Перед изменениями сначала активируйте пользователя"
        )
    if db_user.role == new_role.role.value:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользовать уже имеет указанную роль")
    db_user.role = new_role.role.value
    await db.commit()
    await db.refresh(db_user)
    return UserResponse.model_validate(db_user)


@router.delete(
    "/{telegram_id}", summary="Деактивация пользователя по Telegram ID", description="Доступно только суперадминам"
)
async def delete_user(
    db: Annotated[AsyncSession, Depends(get_async_db)],
    superadmin: Annotated[UserResponse, Depends(get_current_superadmin)],
    telegram_id: int = Path(..., description="Telegram ID искомого пользователя"),
) -> dict:
    """
    Деактивация пользователя по Telegram ID
    """
    if superadmin.telegram_id == telegram_id:
        raise USER_NOT_SELF_CHANGES
    db_user = await db.scalar(select(User).where(User.telegram_id == telegram_id))
    if not db_user:
        raise USER_NOT_FOUND
    if not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь уже деактивирован")
    db_user.is_active = False
    await db.commit()
    return {"message": "Пользователь усппешно деактивирован"}
