"""Account schemas for request/response validation."""

from decimal import Decimal

from pydantic import Field, field_validator

from backend.app.models.account import AccountType

from .base import BaseResponseSchema, BaseSchema


class AccountBase(BaseSchema):
    """Schema base para conta."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nome da conta",
        examples=["Banco Inter", "Nubank", "Carteira"],
    )
    type: AccountType = Field(..., description="Tipo da conta")
    description: str | None = Field(
        None,
        max_length=500,
        description="Descrição da conta",
    )
    color: str = Field(
        "#3B82F6",
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="Cor em hexadecimal",
        examples=["#3B82F6", "#8B5CF6"],
    )
    icon: str = Field(
        "wallet",
        min_length=1,
        max_length=50,
        description="Nome do ícone",
        examples=["wallet", "credit-card", "bank"],
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Valida e normaliza o nome."""
        v = v.strip()
        if not v:
            raise ValueError("O nome não pode estar vazio")
        return v

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str) -> str:
        """Valida e normaliza a cor."""
        return v.upper()


class AccountCreate(AccountBase):
    """Schema para criação de conta."""

    initial_balance: Decimal = Field(
        Decimal("0.00"),
        description="Saldo inicial",
        decimal_places=2,
        examples=[Decimal("1000.00"), Decimal("0.00")],
    )


class AccountUpdate(BaseSchema):
    """Schema para atualização de conta (todos campos opcionais)."""

    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Nome da conta",
    )
    type: AccountType | None = Field(None, description="Tipo da conta")
    description: str | None = Field(
        None,
        max_length=500,
        description="Descrição da conta",
    )
    color: str | None = Field(
        None,
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="Cor em hexadecimal",
    )
    icon: str | None = Field(
        None,
        min_length=1,
        max_length=50,
        description="Nome do ícone",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        """Valida e normaliza o nome."""
        return v.strip() if v else None

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str | None) -> str | None:
        """Valida e normaliza a cor."""
        return v.upper() if v else None


class AccountResponse(AccountBase, BaseResponseSchema):
    """Schema para response de conta."""

    initial_balance: Decimal = Field(..., description="Saldo inicial")
    current_balance: Decimal = Field(..., description="Saldo atual")


class AccountBalanceResponse(BaseSchema):
    """Schema para response de saldo."""

    account_id: int = Field(..., description="ID da conta", gt=0)
    account_name: str = Field(..., description="Nome da conta")
    current_balance: Decimal = Field(..., description="Saldo atual")


class AccountListResponse(BaseSchema):
    """Schema para listagem de contas."""

    accounts: list[AccountResponse] = Field(..., description="Lista de contas")
    total: int = Field(..., description="Total de contas", ge=0)
    total_balance: Decimal = Field(..., description="Saldo total de todas as contas")


class AccountFilterParams(BaseSchema):
    """Parâmetros de filtro para contas."""

    type: AccountType | None = Field(None, description="Filtrar por tipo")
    search: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Buscar por nome",
    )
    is_active: bool | None = Field(None, description="Filtrar por status ativo")
    only_active: bool = Field(False, description="Retornar apenas contas ativas")
