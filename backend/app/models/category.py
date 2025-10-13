"""Category model for organizing transactions."""

from enum import Enum

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class CategoryType(str, Enum):
    """Tipo de categoria."""

    INCOME = "income"  # Receita
    EXPENSE = "expense"  # Despesa


class Category(BaseModel):
    """
    Model para categorias de transações.

    Categorias são usadas para organizar receitas e despesas.
    Exemplos: Salário, Alimentação, Transporte, etc.

    Attributes:
        name: Nome da categoria
        type: Tipo (receita ou despesa)
        description: Descrição opcional
        color: Cor para visualização (hex)
        icon: Ícone para visualização
        transactions: Relacionamento com transações
    """

    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment="Nome da categoria",
    )

    type: Mapped[CategoryType] = mapped_column(
        nullable=False,
        comment="Tipo da categoria (receita/despesa)",
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Descrição da categoria",
    )

    color: Mapped[str] = mapped_column(
        String(7),
        nullable=False,
        default="#6B7280",
        comment="Cor em hexadecimal (#RRGGBB)",
    )

    icon: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="tag",
        comment="Nome do ícone",
    )

    # Relationships
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="category",
        lazy="select",
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "color ~ '^#[0-9A-Fa-f]{6}$'",
            name="check_color_hex_format",
        ),
    )

    def __repr__(self) -> str:
        """Representação string da categoria."""
        return f"<Category(id={self.id}, name='{self.name}', type='{self.type}')>"
