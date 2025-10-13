"""Base model with common fields for all models."""

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class TimestampMixin:
    """Mixin para adicionar timestamps automáticos."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Data de criação do registro",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Data da última atualização",
    )


class SoftDeleteMixin:
    """Mixin para soft delete (exclusão lógica)."""

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
        comment="Data de exclusão (soft delete)",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Indica se o registro está ativo",
    )

    def soft_delete(self) -> None:
        """Marca o registro como deletado."""
        self.deleted_at = datetime.utcnow()
        self.is_active = False

    def restore(self) -> None:
        """Restaura um registro deletado."""
        self.deleted_at = None
        self.is_active = True


class BaseModel(Base, TimestampMixin, SoftDeleteMixin):
    """
    Model base com ID, timestamps e soft delete.

    Todos os models devem herdar desta classe.

    Attributes:
        id: Chave primária
        created_at: Data de criação
        updated_at: Data de atualização
        deleted_at: Data de exclusão (soft delete)
        is_active: Status ativo/inativo
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Chave primária",
    )

    def __repr__(self) -> str:
        """Representação string do objeto."""
        return f"<{self.__class__.__name__}(id={self.id})>"
