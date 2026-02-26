from datetime import datetime
from decimal import Decimal

from common.constants import AMOUNT_ACCURANCY, BANK_COMMENT_LENGTH
from common.enums import OperationType
from sqlalchemy import UUID, CheckConstraint, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, HasId


class FundOperation(Base, HasId):
    """
    Модель фонда оборотных средств.
    """

    __tablename__ = "fund_operations"

    operation_type: Mapped[OperationType] = mapped_column(
        SQLEnum(OperationType, native_enum=False), comment="Тип операции со средствами фонда"
    )
    payday: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="Дата выполнения транзакции или ее попытки"
    )
    payer_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="RESTRICT"),
        comment="Ссылка на ID пользователя, сделавшего транзакцию",
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(*AMOUNT_ACCURANCY), default=Decimal("0.00"), server_default="0.00", comment="Сумма транзакции"
    )
    operation_text: Mapped[str | None] = mapped_column(String(BANK_COMMENT_LENGTH), comment="Комментарий к транзакции")

    __table_args__ = CheckConstraint("amount >= 0", name="check_amount_non_negative")
