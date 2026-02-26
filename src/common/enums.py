from enum import auto

from strenum import UppercaseStrEnum


class OperationType(UppercaseStrEnum):
    """
    Тип операции со счетом.
    INCOMING - входящие транзакции. Все, что увеличивает баланс оборотных средств.
    OUTGOING  - исходящие транзакции, любые виды списаний.
    REJECTED - особый тип транзакций, в него входят любые операции которые были отменены.
    """

    INCOMING = auto()
    OUTGOING = auto()
    REJECTED = auto()


class UserRole(UppercaseStrEnum):
    """
    Роль пользователя.
    SUPERADMIN - тоже что и админ, но может раздавать права и удалять пользователей.
    ADMIN - может видеть баланс и операции, а также делать транзакции.
    AUDITOR - не может ничего вносить или списывать. Доступен только просмотр баланса.
    ALIEN - не может ничего, видит только сообщение с предложением связаться с админом.
    """

    SUPERADMIN = auto()
    ADMIN = auto()
    AUDITOR = auto()
    ALIEN = auto()
