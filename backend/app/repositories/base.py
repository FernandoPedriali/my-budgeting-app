"""Base repository with generic CRUD operations."""

from typing import Any, Generic, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.models.base import BaseModel

# Type variables
ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """
    Repository base com operações CRUD genéricas.

    Args:
        model: Classe do model SQLAlchemy

    Example:
        ```python
        repo = BaseRepository(Category, db)
        category = repo.get_by_id(1)
        ```
    """

    def __init__(self, model: Type[ModelType], db: Session) -> None:
        """
        Inicializa o repository.

        Args:
            model: Classe do model
            db: Sessão do banco de dados
        """
        self.model = model
        self.db = db

    def get_by_id(self, id: int) -> ModelType | None:
        """
        Busca um registro por ID.

        Args:
            id: ID do registro

        Returns:
            Model encontrado ou None
        """
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = False,
    ) -> list[ModelType]:
        """
        Busca todos os registros com paginação.

        Args:
            skip: Quantos registros pular
            limit: Limite de registros
            only_active: Se True, retorna apenas registros ativos

        Returns:
            Lista de models
        """
        query = self.db.query(self.model)

        if only_active:
            query = query.filter(self.model.is_active == True)

        return query.offset(skip).limit(limit).all()

    def count(self, only_active: bool = False) -> int:
        """
        Conta total de registros.

        Args:
            only_active: Se True, conta apenas registros ativos

        Returns:
            Total de registros
        """
        query = select(func.count()).select_from(self.model)

        if only_active:
            query = query.where(self.model.is_active == True)

        return self.db.execute(query).scalar() or 0

    def create(self, obj_in: dict[str, Any]) -> ModelType:
        """
        Cria um novo registro.

        Args:
            obj_in: Dicionário com dados do registro

        Returns:
            Model criado
        """
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, obj_in: dict[str, Any]) -> ModelType:
        """
        Atualiza um registro existente.

        Args:
            db_obj: Objeto do banco a ser atualizado
            obj_in: Dicionário com novos valores

        Returns:
            Model atualizado
        """
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """
        Deleta permanentemente um registro.

        Args:
            id: ID do registro

        Returns:
            True se deletado, False caso contrário
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False

        self.db.delete(db_obj)
        self.db.commit()
        return True

    def soft_delete(self, id: int) -> ModelType | None:
        """
        Deleta logicamente um registro (soft delete).

        Args:
            id: ID do registro

        Returns:
            Model deletado ou None
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None

        db_obj.soft_delete()
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def restore(self, id: int) -> ModelType | None:
        """
        Restaura um registro deletado logicamente.

        Args:
            id: ID do registro

        Returns:
            Model restaurado ou None
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None

        db_obj.restore()
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def exists(self, id: int) -> bool:
        """
        Verifica se um registro existe.

        Args:
            id: ID do registro

        Returns:
            True se existe, False caso contrário
        """
        return self.db.query(self.model.id).filter(self.model.id == id).first() is not None
