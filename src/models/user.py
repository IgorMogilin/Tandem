from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, Numeric, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from common.constants import USERNAME_LENGTH
from common.enums import UserRole
from models.base import Base, HasId


class User(Base, HasId):
    """
    Модель пользователя.
    """

    __tablename__ = "user"

    name: Mapped[str] = mapped_column(String(USERNAME_LENGTH), comment="Имя пользователя")
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, comment="Telegram ID пользователя")
    balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.00"),
        server_default="0.00",
        comment="Доля пользователя в общем фонде (сумма всех начислений)",
    )
    duty: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        default=Decimal("0.00"),
        server_default="0.00",
        comment="Долг пользователя в общий фонд",
    )
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Дата и время добавления пользователя в базу(регистрации)",
    )
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, native_enum=False),
        server_default=UserRole.ALIEN,
        comment="Роль пользователя, определяющая его возможности",
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="Флаг активности пользователя")

    __table_args__ = (
        CheckConstraint("balance >= 0", name="check_balance_non_negative"),
        CheckConstraint("duty >= 0", name="check_duty_non_negative"),
    )
