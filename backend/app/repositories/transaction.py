"""Transaction repository for data access."""

from datetime import date
from decimal import Decimal

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session, joinedload

from backend.app.models.transaction import Transaction, TransactionStatus, TransactionType

from .base import BaseRepository


class TransactionRepository(BaseRepository[Transaction]):
    """Repository para operações com transações."""

    def __init__(self, db: Session) -> None:
        """Inicializa o repository."""
        super().__init__(Transaction, db)

    def get_by_id(self, id: int) -> Transaction | None:
        """
        Busca transação por ID com relacionamentos carregados.

        Args:
            id: ID da transação

        Returns:
            Transação encontrada ou None
        """
        return (
            self.db.query(Transaction)
            .options(joinedload(Transaction.account), joinedload(Transaction.category))
            .filter(Transaction.id == id)
            .first()
        )

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = False,
    ) -> list[Transaction]:
        """
        Busca todas as transações com relacionamentos.

        Args:
            skip: Quantos registros pular
            limit: Limite de registros
            only_active: Se True, retorna apenas transações ativas

        Returns:
            Lista de transações
        """
        query = (
            self.db.query(Transaction)
            .options(joinedload(Transaction.account), joinedload(Transaction.category))
            .order_by(Transaction.transaction_date.desc(), Transaction.created_at.desc())
        )

        if only_active:
            query = query.filter(Transaction.is_active == True)

        return query.offset(skip).limit(limit).all()

    def get_by_account(
        self,
        account_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Transaction]:
        """
        Busca transações por conta.

        Args:
            account_id: ID da conta
            skip: Quantos registros pular
            limit: Limite de registros

        Returns:
            Lista de transações
        """
        return (
            self.db.query(Transaction)
            .options(joinedload(Transaction.account), joinedload(Transaction.category))
            .filter(Transaction.account_id == account_id)
            .order_by(Transaction.transaction_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_category(
        self,
        category_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Transaction]:
        """
        Busca transações por categoria.

        Args:
            category_id: ID da categoria
            skip: Quantos registros pular
            limit: Limite de registros

        Returns:
            Lista de transações
        """
        return (
            self.db.query(Transaction)
            .options(joinedload(Transaction.account), joinedload(Transaction.category))
            .filter(Transaction.category_id == category_id)
            .order_by(Transaction.transaction_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_period(
        self,
        start_date: date,
        end_date: date,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Transaction]:
        """
        Busca transações por período.

        Args:
            start_date: Data inicial
            end_date: Data final
            skip: Quantos registros pular
            limit: Limite de registros

        Returns:
            Lista de transações
        """
        return (
            self.db.query(Transaction)
            .options(joinedload(Transaction.account), joinedload(Transaction.category))
            .filter(
                and_(
                    Transaction.transaction_date >= start_date,
                    Transaction.transaction_date <= end_date,
                )
            )
            .order_by(Transaction.transaction_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_status(
        self,
        status: TransactionStatus,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Transaction]:
        """
        Busca transações por status.

        Args:
            status: Status da transação
            skip: Quantos registros pular
            limit: Limite de registros

        Returns:
            Lista de transações
        """
        return (
            self.db.query(Transaction)
            .options(joinedload(Transaction.account), joinedload(Transaction.category))
            .filter(Transaction.status == status)
            .order_by(Transaction.transaction_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search(
        self,
        search_term: str,
        account_id: int | None = None,
        category_id: int | None = None,
        type: TransactionType | None = None,
        status: TransactionStatus | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Transaction]:
        """
        Busca transações com múltiplos filtros.

        Args:
            search_term: Buscar na descrição ou observações
            account_id: Filtrar por conta
            category_id: Filtrar por categoria
            type: Filtrar por tipo
            status: Filtrar por status
            start_date: Data inicial
            end_date: Data final
            skip: Quantos registros pular
            limit: Limite de registros

        Returns:
            Lista de transações encontradas
        """
        query = self.db.query(Transaction).options(
            joinedload(Transaction.account), joinedload(Transaction.category)
        )

        # Busca textual
        if search_term:
            query = query.filter(
                or_(
                    Transaction.description.ilike(f"%{search_term}%"),
                    Transaction.notes.ilike(f"%{search_term}%"),
                )
            )

        # Filtros específicos
        if account_id:
            query = query.filter(Transaction.account_id == account_id)

        if category_id:
            query = query.filter(Transaction.category_id == category_id)

        if type:
            query = query.filter(Transaction.type == type)

        if status:
            query = query.filter(Transaction.status == status)

        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)

        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)

        return query.order_by(Transaction.transaction_date.desc()).offset(skip).limit(limit).all()

    def get_total_by_type(
        self,
        type: TransactionType,
        status: TransactionStatus | None = TransactionStatus.COMPLETED,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> Decimal:
        """
        Calcula total por tipo de transação.

        Args:
            type: Tipo da transação
            status: Filtrar por status (default: apenas efetivadas)
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)

        Returns:
            Total calculado
        """
        query = self.db.query(func.sum(Transaction.amount)).filter(Transaction.type == type)

        if status:
            query = query.filter(Transaction.status == status)

        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)

        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)

        result = query.scalar()
        return result if result is not None else Decimal("0.00")

    def get_balance(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
        only_completed: bool = True,
    ) -> Decimal:
        """
        Calcula saldo (receitas - despesas).

        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            only_completed: Se True, considera apenas transações efetivadas

        Returns:
            Saldo calculado
        """
        income = self.get_total_by_type(
            TransactionType.INCOME,
            TransactionStatus.COMPLETED if only_completed else None,
            start_date,
            end_date,
        )

        expense = self.get_total_by_type(
            TransactionType.EXPENSE,
            TransactionStatus.COMPLETED if only_completed else None,
            start_date,
            end_date,
        )

        return income - expense

    def change_status(
        self, transaction_id: int, new_status: TransactionStatus
    ) -> Transaction | None:
        """
        Altera o status de uma transação.

        Args:
            transaction_id: ID da transação
            new_status: Novo status

        Returns:
            Transação atualizada ou None
        """
        transaction = self.get_by_id(transaction_id)
        if not transaction:
            return None

        transaction.status = new_status
        self.db.commit()
        self.db.refresh(transaction)
        return transaction
