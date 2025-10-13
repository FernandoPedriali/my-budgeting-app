"""Category repository for data access."""

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from backend.app.models.category import Category, CategoryType

from .base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Repository para operações com categorias."""

    def __init__(self, db: Session) -> None:
        """Inicializa o repository."""
        super().__init__(Category, db)

    def get_by_name(self, name: str) -> Category | None:
        """
        Busca categoria por nome.

        Args:
            name: Nome da categoria

        Returns:
            Categoria encontrada ou None
        """
        return self.db.query(Category).filter(Category.name == name).first()

    def get_by_type(
        self,
        type: CategoryType,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True,
    ) -> list[Category]:
        """
        Busca categorias por tipo.

        Args:
            type: Tipo da categoria (income/expense)
            skip: Quantos registros pular
            limit: Limite de registros
            only_active: Se True, retorna apenas categorias ativas

        Returns:
            Lista de categorias
        """
        query = self.db.query(Category).filter(Category.type == type)

        if only_active:
            query = query.filter(Category.is_active == True)

        return query.offset(skip).limit(limit).all()

    def search(
        self,
        search_term: str,
        type: CategoryType | None = None,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True,
    ) -> list[Category]:
        """
        Busca categorias por nome ou descrição.

        Args:
            search_term: Termo de busca
            type: Filtrar por tipo (opcional)
            skip: Quantos registros pular
            limit: Limite de registros
            only_active: Se True, retorna apenas categorias ativas

        Returns:
            Lista de categorias encontradas
        """
        query = self.db.query(Category).filter(
            or_(
                Category.name.ilike(f"%{search_term}%"),
                Category.description.ilike(f"%{search_term}%"),
            )
        )

        if type:
            query = query.filter(Category.type == type)

        if only_active:
            query = query.filter(Category.is_active == True)

        return query.offset(skip).limit(limit).all()

    def count_by_type(self, type: CategoryType, only_active: bool = True) -> int:
        """
        Conta categorias por tipo.

        Args:
            type: Tipo da categoria
            only_active: Se True, conta apenas categorias ativas

        Returns:
            Total de categorias
        """
        query = self.db.query(func.count(Category.id)).filter(Category.type == type)

        if only_active:
            query = query.filter(Category.is_active == True)

        return query.scalar() or 0

    def is_name_taken(self, name: str, exclude_id: int | None = None) -> bool:
        """
        Verifica se o nome da categoria já está em uso.

        Args:
            name: Nome a verificar
            exclude_id: ID para excluir da verificação (útil em updates)

        Returns:
            True se o nome já existe, False caso contrário
        """
        query = self.db.query(Category.id).filter(Category.name == name)

        if exclude_id:
            query = query.filter(Category.id != exclude_id)

        return query.first() is not None

    def has_transactions(self, category_id: int) -> bool:
        """
        Verifica se a categoria tem transações associadas.

        Args:
            category_id: ID da categoria

        Returns:
            True se tem transações, False caso contrário
        """
        # Import aqui para evitar circular import
        from backend.app.models.transaction import Transaction

        return (
            self.db.query(Transaction.id).filter(Transaction.category_id == category_id).first()
            is not None
        )
