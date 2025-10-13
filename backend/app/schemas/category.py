"""Category schemas for request/response validation."""

from pydantic import Field, field_validator

from backend.app.models.category import CategoryType

from .base import BaseResponseSchema, BaseSchema


class CategoryBase(BaseSchema):
    """Schema base para categoria."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nome da categoria",
        examples=["Salário", "Alimentação"],
    )
    type: CategoryType = Field(..., description="Tipo da categoria")
    description: str | None = Field(
        default=None,
        max_length=500,
        description="Descrição da categoria",
    )
    color: str = Field(
        default="#6B7280",
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="Cor em hexadecimal",
        examples=["#3B82F6", "#EF4444"],
    )
    icon: str = Field(
        default="tag",
        min_length=1,
        max_length=50,
        description="Nome do ícone",
        examples=["wallet", "shopping-cart", "home"],
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


class CategoryCreate(CategoryBase):
    """Schema para criação de categoria."""

    pass


class CategoryUpdate(BaseSchema):
    """Schema para atualização de categoria (todos campos opcionais)."""

    name: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Nome da categoria",
    )
    type: CategoryType | None = Field(None, description="Tipo da categoria")
    description: str | None = Field(
        None,
        max_length=500,
        description="Descrição da categoria",
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


class CategoryResponse(CategoryBase, BaseResponseSchema):
    """Schema para response de categoria."""

    pass


class CategoryListResponse(BaseSchema):
    """Schema para listagem de categorias."""

    categories: list[CategoryResponse] = Field(..., description="Lista de categorias")
    total: int = Field(..., description="Total de categorias", ge=0)


class CategoryFilterParams(BaseSchema):
    """Parâmetros de filtro para categorias."""

    type: CategoryType | None = Field(None, description="Filtrar por tipo")
    search: str | None = Field(
        None,
        min_length=1,
        max_length=100,
        description="Buscar por nome",
    )
    is_active: bool | None = Field(None, description="Filtrar por status ativo")
