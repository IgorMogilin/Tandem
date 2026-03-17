from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from src.common.enums import UserRole


class UserResponse(BaseModel):
    """
    Схема для ответа с данными пользователя.
    """

    name: str = Field(description="Имя пользователя")
    telegram_id: int = Field(description="Telegram ID пользователя")
    balance: Decimal = Field(description="Сумма всех вложений пользователя")
    duty: Decimal = Field(description="Сумма всех задолженностей пользователя")
    role: str = Field(description="Роль пользователя в системе")
    registered_at: datetime = Field(description="Дата регистрации пользователя")
    is_active: bool = Field(description="Флаг активности пользователя")

    @field_serializer("balance", "duty")
    def serialize_decimal(self, value: Decimal) -> str:
        return f"{value:.2f}"

    @field_serializer("registered_at")
    def serialize_datetime(self, value: datetime) -> str:
        return value.strftime("%d.%m.%Y %H:%M:%S")

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """
    Схема для обновления пользователя
    """

    role: UserRole = Field(..., description="Роль пользователя в системе")
