"""Transaction schemas for request/response validation."""

from datetime import date
from decimal import Decimal

from pydantic import Field, field_validator

from backend.app.models.transaction import TransactionStatus, TransactionType

from .account import AccountResponse
from .base import BaseResponseSchema, BaseSchema
from .category import CategoryResponse


class TransactionBase(BaseSchema):
    """Schema base para transação."""

    description: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Descrição da transação",
        examples=["Supermercado", "Salário", "Aluguel"],
    )
    amount: Decimal = Field(
        ...,
        description="Valor da transação (pode ser negativo para estornos)",
        decimal_places=2,
        examples=[Decimal("100.50"), Decimal("-50.00")],
    )
    type: TransactionType = Field(..., description="Tipo da transação")
    transaction_date: date = Field(..., description="Data da transação")
    notes: str | None = Field(
        default=None,
        max_length=1000,
        description="Observações adicionais",
    )

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Valida e normaliza a descrição."""
        return v.strip()

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal) -> Decimal:
        """Valida que o valor não seja zero."""
        if v == 0:
            raise ValueError("O valor não pode ser zero")
        return v


class TransactionCreate(TransactionBase):
    """Schema para criação de transação."""

    status: TransactionStatus = Field(
        TransactionStatus.PENDING,
        description="Status da transação",
    )
    account_id: int = Field(..., description="ID da conta", gt=0)
    category_id: int = Field(..., description="ID da categoria", gt=0)


class TransactionUpdate(BaseSchema):
    """Schema para atualização de transação (todos campos opcionais)."""

    description: str | None = Field(
        None,
        min_length=1,
        max_length=200,
        description="Descrição da transação",
    )
    amount: Decimal | None = Field(
        None,
        description="Valor da transação",
        decimal_places=2,
    )
    type: TransactionType | None = Field(None, description="Tipo da transação")
    status: TransactionStatus | None = Field(
        TransactionStatus.PENDING, description="Status da transação"
    )
    transaction_date: date | None = Field(None, description="Data da transação")
    notes: str | None = Field(
        None,
        max_length=1000,
        description="Observações adicionais",
    )
    account_id: int | None = Field(None, description="ID da conta", gt=0)
    category_id: int | None = Field(None, description="ID da categoria", gt=0)

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None) -> str | None:
        """Valida e normaliza a descrição."""
        return v.strip() if v else None

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: Decimal | None) -> Decimal | None:
        """Valida que o valor não seja zero."""
        if v is not None and v == 0:
            raise ValueError("O valor não pode ser zero")
        return v


class TransactionStatusUpdate(BaseSchema):
    """Schema para atualização de status."""

    status: TransactionStatus = Field(..., description="Novo status")


class TransactionResponse(TransactionBase, BaseResponseSchema):
    """Schema para response de transação."""

    status: TransactionStatus = Field(..., description="Status da transação")
    account_id: int = Field(..., description="ID da conta")
    category_id: int = Field(..., description="ID da categoria")
    account: AccountResponse = Field(..., description="Dados da conta")
    category: CategoryResponse = Field(..., description="Dados da categoria")


class TransactionListResponse(BaseSchema):
    """Schema para listagem de transações."""

    transactions: list[TransactionResponse] = Field(..., description="Lista de transações")
    total: int = Field(..., description="Total de transações", ge=0)
    total_income: Decimal = Field(..., description="Total de receitas")
    total_expense: Decimal = Field(..., description="Total de despesas")
    balance: Decimal = Field(..., description="Saldo (receitas - despesas)")


class TransactionFilterParams(BaseSchema):
    """Parâmetros de filtro para transações."""

    account_id: int | None = Field(None, description="Filtrar por conta", gt=0)
    category_id: int | None = Field(None, description="Filtrar por categoria", gt=0)
    type: TransactionType | None = Field(None, description="Filtrar por tipo")
    status: TransactionStatus | None = Field(None, description="Filtrar por status")
    date_from: date | None = Field(None, description="Data inicial")
    date_to: date | None = Field(None, description="Data final")
    search: str | None = Field(
        None,
        min_length=1,
        max_length=200,
        description="Buscar na descrição",
    )
    min_amount: Decimal | None = Field(
        None,
        description="Valor mínimo",
        decimal_places=2,
    )
    max_amount: Decimal | None = Field(
        None,
        description="Valor máximo",
        decimal_places=2,
    )


class TransactionSummary(BaseSchema):
    """Schema para resumo de transações."""

    total_income: Decimal = Field(..., description="Total de receitas")
    total_expense: Decimal = Field(..., description="Total de despesas")
    balance: Decimal = Field(..., description="Saldo")
    total_transactions: int = Field(..., description="Total de transações", ge=0)
    period_start: date | None = Field(None, description="Início do período")
    period_end: date | None = Field(None, description="Fim do período")
