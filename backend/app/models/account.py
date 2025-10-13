"""Account model for managing financial accounts."""

from decimal import Decimal
from enum import Enum

from sqlalchemy import CheckConstraint, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class AccountType(str, Enum):
    """Tipo de conta."""

    CHECKING = "checking"  # Conta corrente
    SAVINGS = "savings"  # Poupança
    INVESTMENT = "investment"  # Investimento
    CREDIT_CARD = "credit_card"  # Cartão de crédito
    CASH = "cash"  # Dinheiro
    OTHER = "other"  # Outro


class Account(BaseModel):
    """
    Model para contas financeiras.

    Representa contas bancárias, carteiras, investimentos, etc.

    Attributes:
        name: Nome da conta
        type: Tipo da conta
        description: Descrição opcional
        initial_balance: Saldo inicial
        current_balance: Saldo atual (calculado)
        color: Cor para visualização
        icon: Ícone para visualização
        transactions: Relacionamento com transações
    """

    __tablename__ = "accounts"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        comment="Nome da conta",
    )

    type: Mapped[AccountType] = mapped_column(
        nullable=False,
        comment="Tipo da conta",
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="Descrição da conta",
    )

    initial_balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        default=Decimal("0.00"),
        comment="Saldo inicial da conta",
    )

    current_balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        default=Decimal("0.00"),
        comment="Saldo atual da conta",
    )

    color: Mapped[str] = mapped_column(
        String(7),
        nullable=False,
        default="#3B82F6",
        comment="Cor em hexadecimal (#RRGGBB)",
    )

    icon: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="wallet",
        comment="Nome do ícone",
    )

    # Relationships
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="account",
        lazy="select",
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "color ~ '^#[0-9A-Fa-f]{6}$'",
            name="check_account_color_hex_format",
        ),
    )

    def __repr__(self) -> str:
        """Representação string da conta."""
        return f"<Account(id={self.id}, name='{self.name}', balance={self.current_balance})>"
