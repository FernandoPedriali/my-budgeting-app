"""Base schemas for common patterns."""

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

# Type variable for generic responses
T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configurations."""

    model_config = ConfigDict(
        from_attributes=True,  # Permite criar de ORM models
        populate_by_name=True,  # Permite usar tanto nome quanto alias
        use_enum_values=True,  # Serializa enums como valores
    )


class TimestampSchema(BaseSchema):
    """Schema com timestamps."""

    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de atualização")


class SoftDeleteSchema(BaseSchema):
    """Schema com soft delete."""

    deleted_at: datetime | None = Field(None, description="Data de exclusão")
    is_active: bool = Field(True, description="Status ativo/inativo")


class BaseResponseSchema(TimestampSchema, SoftDeleteSchema):
    """Schema base para responses com ID e timestamps."""

    id: int = Field(..., description="ID do registro", gt=0)


class PaginationParams(BaseSchema):
    """Parâmetros de paginação."""

    page: int = Field(1, description="Número da página", ge=1)
    page_size: int = Field(50, description="Itens por página", ge=1, le=100)

    @property
    def skip(self) -> int:
        """Calcula quantos registros pular."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Retorna o limite de registros."""
        return self.page_size


class PaginatedResponse(BaseSchema, Generic[T]):
    """Response paginado genérico."""

    items: list[T] = Field(..., description="Lista de itens")
    total: int = Field(..., description="Total de registros", ge=0)
    page: int = Field(..., description="Página atual", ge=1)
    page_size: int = Field(..., description="Itens por página", ge=1)
    total_pages: int = Field(..., description="Total de páginas", ge=0)

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        pagination: PaginationParams,
    ) -> "PaginatedResponse[T]":
        """
        Cria response paginado.

        Args:
            items: Lista de itens
            total: Total de registros
            pagination: Parâmetros de paginação

        Returns:
            PaginatedResponse com os dados
        """
        total_pages = (total + pagination.page_size - 1) // pagination.page_size

        return cls(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages,
        )


class MessageResponse(BaseSchema):
    """Response com mensagem simples."""

    message: str = Field(..., description="Mensagem")
    success: bool = Field(True, description="Status da operação")
