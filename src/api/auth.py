from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.shemas.users import UserResponse
from src.common.enums import UserRole
from src.db.depends import get_async_db
from src.db.models.user import User


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_async_db)],
    x_telegram_id: int = Header(..., alias="X-Telegram-ID", description="Telegram ID пользователя в заголовке"),
) -> UserResponse:
    """Получает активного пользователя по telegram id."""
    db_user = await db.scalar(select(User).where(User.telegram_id == x_telegram_id))
    if not isinstance(db_user, User):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь таким ID не найден")
    if not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь деактивирован")
    return UserResponse.model_validate(db_user)


async def get_current_auditor(current_user: Annotated[UserResponse, Depends(get_current_user)]) -> UserResponse:
    """Проверяет, что пользователь имеет роль 'Auditor'."""
    if current_user.role != UserRole.AUDITOR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для выполнения данного действия"
        )
    return current_user


async def get_current_admin(current_user: Annotated[UserResponse, Depends(get_current_user)]) -> UserResponse:
    """Проверяет, что пользователь имеет роль 'Admin'."""
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для выполнения данного действия"
        )
    return current_user


async def get_current_superadmin(current_user: Annotated[UserResponse, Depends(get_current_user)]) -> UserResponse:
    """Проверяет, что пользователь имеет роль 'Superadmin'."""
    if current_user.role != UserRole.SUPERADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав для выполнения данного действия"
        )
    return current_user
