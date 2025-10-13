"""Account repository for data access."""

from decimal import Decimal

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from backend.app.models.account import Account, AccountType

from .base import BaseRepository


class AccountRepository(BaseRepository[Account]):
    """Repository para operações com contas."""

    def __init__(self, db: Session) -> None:
        """Inicializa o repository."""
        super().__init__(Account, db)

    def get_by_name(self, name: str) -> Account | None:
        """
        Busca conta por nome.

        Args:
            name: Nome da conta

        Returns:
            Conta encontrada ou None
        """
        return self.db.query(Account).filter(Account.name == name).first()

    def get_by_type(
        self,
        type: AccountType,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True,
    ) -> list[Account]:
        """
        Busca contas por tipo.

        Args:
            type: Tipo da conta
            skip: Quantos registros pular
            limit: Limite de registros
            only_active: Se True, retorna apenas contas ativas

        Returns:
            Lista de contas
        """
        query = self.db.query(Account).filter(Account.type == type)

        if only_active:
            query = query.filter(Account.is_active == True)

        return query.offset(skip).limit(limit).all()

    def get_active(self, skip: int = 0, limit: int = 100) -> list[Account]:
        """
        Busca apenas contas ativas.

        Args:
            skip: Quantos registros pular
            limit: Limite de registros

        Returns:
            Lista de contas ativas
        """
        return self.get_all(skip=skip, limit=limit, only_active=True)

    def search(
        self,
        search_term: str,
        type: AccountType | None = None,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True,
    ) -> list[Account]:
        """
        Busca contas por nome ou descrição.

        Args:
            search_term: Termo de busca
            type: Filtrar por tipo (opcional)
            skip: Quantos registros pular
            limit: Limite de registros
            only_active: Se True, retorna apenas contas ativas

        Returns:
            Lista de contas encontradas
        """
        query = self.db.query(Account).filter(
            or_(
                Account.name.ilike(f"%{search_term}%"),
                Account.description.ilike(f"%{search_term}%"),
            )
        )

        if type:
            query = query.filter(Account.type == type)

        if only_active:
            query = query.filter(Account.is_active == True)

        return query.offset(skip).limit(limit).all()

    def update_balance(self, account_id: int, new_balance: Decimal) -> Account | None:
        """
        Atualiza o saldo de uma conta.

        Args:
            account_id: ID da conta
            new_balance: Novo saldo

        Returns:
            Conta atualizada ou None
        """
        account = self.get_by_id(account_id)
        if not account:
            return None

        account.current_balance = new_balance
        self.db.commit()
        self.db.refresh(account)
        return account

    def get_total_balance(self, only_active: bool = True) -> Decimal:
        """
        Calcula saldo total de todas as contas.

        Args:
            only_active: Se True, conta apenas contas ativas

        Returns:
            Saldo total
        """
        query = self.db.query(func.sum(Account.current_balance))

        if only_active:
            query = query.filter(Account.is_active == True)

        result = query.scalar()
        return result if result is not None else Decimal("0.00")

    def is_name_taken(self, name: str, exclude_id: int | None = None) -> bool:
        """
        Verifica se o nome da conta já está em uso.

        Args:
            name: Nome a verificar
            exclude_id: ID para excluir da verificação (útil em updates)

        Returns:
            True se o nome já existe, False caso contrário
        """
        query = self.db.query(Account.id).filter(Account.name == name)

        if exclude_id:
            query = query.filter(Account.id != exclude_id)

        return query.first() is not None

    def has_transactions(self, account_id: int) -> bool:
        """
        Verifica se a conta tem transações associadas.

        Args:
            account_id: ID da conta

        Returns:
            True se tem transações, False caso contrário
        """
        # Import aqui para evitar circular import
        from backend.app.models.transaction import Transaction

        return (
            self.db.query(Transaction.id).filter(Transaction.account_id == account_id).first()
            is not None
        )

    def can_delete(self, account_id: int) -> bool:
        """
        Verifica se uma conta pode ser deletada.

        Uma conta só pode ser deletada se não tiver transações.

        Args:
            account_id: ID da conta

        Returns:
            True se pode deletar, False caso contrário
        """
        return not self.has_transactions(account_id)
