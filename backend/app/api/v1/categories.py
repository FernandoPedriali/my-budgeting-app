"""Categories API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.core.exceptions import BadRequestException, NotFoundException
from backend.app.models.category import CategoryType
from backend.app.schemas import (
    CategoryCreate,
    CategoryFilterParams,
    CategoryListResponse,
    CategoryResponse,
    CategoryUpdate,
    MessageResponse,
)
from backend.app.services import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=CategoryListResponse)
def list_categories(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(50, ge=1, le=100, description="Limite de registros"),
    type: CategoryType | None = Query(None, description="Filtrar por tipo"),
    search: str | None = Query(None, description="Buscar por nome"),
    is_active: bool | None = Query(None, description="Filtrar por status ativo"),
    db: Session = Depends(get_db),
) -> CategoryListResponse:
    """
    Lista todas as categorias com filtros opcionais.

    - **skip**: Paginação - quantos registros pular
    - **limit**: Paginação - limite de registros (máx: 100)
    - **type**: Filtrar por tipo (income/expense)
    - **search**: Buscar por nome ou descrição
    - **is_active**: Filtrar por status ativo/inativo
    """
    service = CategoryService(db)

    filters = CategoryFilterParams(
        type=type,
        search=search,
        is_active=is_active,
    )

    categories, total = service.get_all(skip=skip, limit=limit, filters=filters)

    return CategoryListResponse(
        categories=[CategoryResponse.model_validate(cat) for cat in categories],
        total=total,
    )


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
) -> CategoryResponse:
    """
    Busca uma categoria por ID.

    - **category_id**: ID da categoria
    """
    service = CategoryService(db)

    try:
        category = service.get_by_id(category_id)
        if not category:
            raise NotFoundException(f"Categoria com ID {category_id} não encontrada")

        return CategoryResponse.model_validate(category)

    except ValueError as e:
        raise BadRequestException(str(e))


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
) -> CategoryResponse:
    """
    Cria uma nova categoria.

    - **name**: Nome da categoria (obrigatório, único)
    - **type**: Tipo da categoria - income ou expense (obrigatório)
    - **description**: Descrição opcional
    - **color**: Cor em hexadecimal (padrão: #6B7280)
    - **icon**: Nome do ícone (padrão: tag)
    """
    service = CategoryService(db)

    try:
        category = service.create(data)
        return CategoryResponse.model_validate(category)

    except ValueError as e:
        raise BadRequestException(str(e))


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
) -> CategoryResponse:
    """
    Atualiza uma categoria existente.

    Todos os campos são opcionais. Apenas os campos fornecidos serão atualizados.

    - **category_id**: ID da categoria
    - **name**: Novo nome (opcional)
    - **type**: Novo tipo (opcional)
    - **description**: Nova descrição (opcional)
    - **color**: Nova cor (opcional)
    - **icon**: Novo ícone (opcional)
    """
    service = CategoryService(db)

    try:
        category = service.update(category_id, data)
        return CategoryResponse.model_validate(category)

    except ValueError as e:
        raise BadRequestException(str(e))


@router.delete("/{category_id}", response_model=MessageResponse)
def delete_category(
    category_id: int,
    permanent: bool = Query(False, description="Se True, deleta permanentemente"),
    db: Session = Depends(get_db),
) -> MessageResponse:
    """
    Deleta uma categoria.

    Por padrão, faz soft delete (exclusão lógica).
    Use permanent=True para deletar permanentemente.

    **Atenção**: Não é possível deletar categorias com transações associadas.

    - **category_id**: ID da categoria
    - **permanent**: Se True, deleta permanentemente (padrão: False)
    """
    service = CategoryService(db)

    try:
        success = service.delete(category_id, soft=not permanent)

        if success:
            action = "deletada permanentemente" if permanent else "desativada"
            return MessageResponse(
                message=f"Categoria {action} com sucesso",
                success=True,
            )
        else:
            raise NotFoundException(f"Categoria com ID {category_id} não encontrada")

    except ValueError as e:
        raise BadRequestException(str(e))


@router.patch("/{category_id}/restore", response_model=CategoryResponse)
def restore_category(
    category_id: int,
    db: Session = Depends(get_db),
) -> CategoryResponse:
    """
    Restaura uma categoria deletada logicamente.

    - **category_id**: ID da categoria
    """
    service = CategoryService(db)

    try:
        category = service.restore(category_id)
        return CategoryResponse.model_validate(category)

    except ValueError as e:
        raise BadRequestException(str(e))


@router.get("/by-type/{type}", response_model=CategoryListResponse)
def get_categories_by_type(
    type: CategoryType,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
) -> CategoryListResponse:
    """
    Busca categorias por tipo.

    - **type**: Tipo da categoria (income/expense)
    - **skip**: Paginação - quantos registros pular
    - **limit**: Paginação - limite de registros
    """
    service = CategoryService(db)

    filters = CategoryFilterParams(type=type)
    categories, total = service.get_all(skip=skip, limit=limit, filters=filters)

    return CategoryListResponse(
        categories=[CategoryResponse.model_validate(cat) for cat in categories],
        total=total,
    )
