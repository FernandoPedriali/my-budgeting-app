"""Transaction model for financial transactions."""

from datetime import date
from decimal import Decimal
from enum import Enum

from sqlalchemy import CheckConstraint, Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class TransactionType(str, Enum):
    """Tipo de transação."""

    INCOME = "income"  # Receita
    EXPENSE = "expense"  # Despesa


class TransactionStatus(str, Enum):
    """Status da transação."""

    PENDING = "pending"  # Pendente (não afeta saldo)
    COMPLETED = "completed"  # Efetivada (afeta saldo)


class Transaction(BaseModel):
    """
    Model para transações financeiras (versão simples - Sprint 1).

    Representa movimentações financeiras (receitas e despesas).
    Versão simples sem recorrência e sem parcelas.

    Attributes:
        description: Descrição da transação
        amount: Valor da transação
        type: Tipo (receita ou despesa)
        status: Status (pendente ou efetivada)
        transaction_date: Data da transação
        notes: Observações adicionais
        account_id: ID da conta
        category_id: ID da categoria
        account: Relacionamento com conta
        category: Relacionamento com categoria
    """

    __tablename__ = "transactions"

    description: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Descrição da transação",
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=2),
        nullable=False,
        comment="Valor da transação (pode ser negativo para estornos)",
    )

    type: Mapped[TransactionType] = mapped_column(
        nullable=False,
        comment="Tipo da transação (receita/despesa)",
    )

    status: Mapped[TransactionStatus] = mapped_column(
        nullable=False,
        default=TransactionStatus.PENDING,
        comment="Status da transação",
    )

    transaction_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        comment="Data da transação",
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Observações adicionais",
    )

    # Foreign Keys
    account_id: Mapped[int] = mapped_column(
        ForeignKey("accounts.id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID da conta",
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID da categoria",
    )

    # Relationships
    account: Mapped["Account"] = relationship(
        back_populates="transactions",
        lazy="joined",
    )

    category: Mapped["Category"] = relationship(
        back_populates="transactions",
        lazy="joined",
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "amount != 0",
            name="check_amount_not_zero",
        ),
    )

    def __repr__(self) -> str:
        """Representação string da transação."""
        return (
            f"<Transaction(id={self.id}, description='{self.description}', "
            f"amount={self.amount}, type='{self.type}')>"
        )
