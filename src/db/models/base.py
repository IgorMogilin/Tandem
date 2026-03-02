from sqlalchemy import UUID, func, inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Базовый класс от SQLAlchemy
    """

    def as_dict(self, exclude: list | None = None) -> dict:
        exclude = exclude or []
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key not in exclude}

    def __repr__(self) -> str:
        cols = []
        for col in self.__table__.columns.keys():
            if col in self.__dict__:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class HasId:
    """
    Модель с полем ID.
    """

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        server_default=func.uuid_generate_v7(),
        sort_order=-1,
    )
