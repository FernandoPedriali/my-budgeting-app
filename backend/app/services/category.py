"""Category service with business logic."""

from sqlalchemy.orm import Session

from backend.app.models.category import Category, CategoryType
from backend.app.repositories import CategoryRepository
from backend.app.schemas import CategoryCreate, CategoryFilterParams, CategoryUpdate


class CategoryService:
    """Service para lógica de negócio de categorias."""

    def __init__(self, db: Session) -> None:
        """
        Inicializa o service.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.repository = CategoryRepository(db)

    def get_by_id(self, category_id: int) -> Category | None:
        """
        Busca categoria por ID.

        Args:
            category_id: ID da categoria

        Returns:
            Categoria encontrada ou None

        Raises:
            ValueError: Se ID inválido
        """
        if category_id <= 0:
            raise ValueError("ID da categoria deve ser maior que zero")

        return self.repository.get_by_id(category_id)

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: CategoryFilterParams | None = None,
    ) -> tuple[list[Category], int]:
        """
        Lista categorias com filtros.

        Args:
            skip: Quantos registros pular
            limit: Limite de registros
            filters: Filtros de busca

        Returns:
            Tupla (lista de categorias, total)
        """
        if filters:
            # Busca com filtros
            if filters.search:
                categories = self.repository.search(
                    search_term=filters.search,
                    type=filters.type,
                    skip=skip,
                    limit=limit,
                    only_active=filters.is_active if filters.is_active is not None else True,
                )
            elif filters.type:
                categories = self.repository.get_by_type(
                    type=filters.type,
                    skip=skip,
                    limit=limit,
                    only_active=filters.is_active if filters.is_active is not None else True,
                )
            else:
                categories = self.repository.get_all(
                    skip=skip,
                    limit=limit,
                    only_active=filters.is_active if filters.is_active is not None else True,
                )
        else:
            categories = self.repository.get_all(skip=skip, limit=limit, only_active=True)

        total = self.repository.count(
            only_active=filters.is_active if filters and filters.is_active is not None else True
        )

        return categories, total

    def create(self, data: CategoryCreate) -> Category:
        """
        Cria nova categoria.

        Args:
            data: Dados da categoria

        Returns:
            Categoria criada

        Raises:
            ValueError: Se validação falhar
        """
        # Validar tipo
        self.validate_category_type(data.type)

        # Verificar nome duplicado
        if self.repository.is_name_taken(data.name):
            raise ValueError(f"Já existe uma categoria com o nome '{data.name}'")

        # Criar categoria
        category_data = data.model_dump()
        return self.repository.create(category_data)

    def update(self, category_id: int, data: CategoryUpdate) -> Category:
        """
        Atualiza categoria existente.

        Args:
            category_id: ID da categoria
            data: Novos dados

        Returns:
            Categoria atualizada

        Raises:
            ValueError: Se categoria não existir ou validação falhar
        """
        # Buscar categoria
        category = self.repository.get_by_id(category_id)
        if not category:
            raise ValueError(f"Categoria com ID {category_id} não encontrada")

        # Validar tipo se fornecido
        if data.type:
            self.validate_category_type(data.type)

        # Verificar nome duplicado se fornecido
        if data.name and self.repository.is_name_taken(data.name, exclude_id=category_id):
            raise ValueError(f"Já existe uma categoria com o nome '{data.name}'")

        # Atualizar apenas campos fornecidos
        update_data = data.model_dump(exclude_unset=True)
        return self.repository.update(category, update_data)

    def delete(self, category_id: int, soft: bool = True) -> bool:
        """
        Deleta categoria.

        Args:
            category_id: ID da categoria
            soft: Se True, faz soft delete; se False, deleta permanentemente

        Returns:
            True se deletado com sucesso

        Raises:
            ValueError: Se categoria não existir ou estiver em uso
        """
        # Verificar se categoria existe
        category = self.repository.get_by_id(category_id)
        if not category:
            raise ValueError(f"Categoria com ID {category_id} não encontrada")

        # Verificar se está em uso
        if not self.check_category_deletable(category_id):
            raise ValueError(
                "Não é possível deletar categoria com transações associadas. "
                "Delete as transações primeiro."
            )

        # Deletar
        if soft:
            result = self.repository.soft_delete(category_id)
            return result is not None
        else:
            return self.repository.delete(category_id)

    def restore(self, category_id: int) -> Category:
        """
        Restaura categoria deletada logicamente.

        Args:
            category_id: ID da categoria

        Returns:
            Categoria restaurada

        Raises:
            ValueError: Se categoria não existir
        """
        category = self.repository.restore(category_id)
        if not category:
            raise ValueError(f"Categoria com ID {category_id} não encontrada")

        return category

    def validate_category_type(self, type: CategoryType) -> None:
        """
        Valida tipo de categoria.

        Args:
            type: Tipo a validar

        Raises:
            ValueError: Se tipo inválido
        """
        valid_types = [CategoryType.INCOME, CategoryType.EXPENSE]
        if type not in valid_types:
            raise ValueError(
                f"Tipo de categoria inválido. Valores válidos: {[t.value for t in valid_types]}"
            )

    def check_category_in_use(self, category_id: int) -> bool:
        """
        Verifica se categoria está em uso (tem transações).

        Args:
            category_id: ID da categoria

        Returns:
            True se está em uso, False caso contrário
        """
        return self.repository.has_transactions(category_id)

    def check_category_deletable(self, category_id: int) -> bool:
        """
        Verifica se categoria pode ser deletada.

        Uma categoria só pode ser deletada se não tiver transações.

        Args:
            category_id: ID da categoria

        Returns:
            True se pode deletar, False caso contrário
        """
        return not self.check_category_in_use(category_id)

    def get_statistics(self) -> dict[str, int]:
        """
        Retorna estatísticas de categorias.

        Returns:
            Dicionário com estatísticas
        """
        return {
            "total": self.repository.count(only_active=False),
            "active": self.repository.count(only_active=True),
            "income": self.repository.count_by_type(CategoryType.INCOME),
            "expense": self.repository.count_by_type(CategoryType.EXPENSE),
        }
