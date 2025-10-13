"""Transaction service with business logic."""

from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from backend.app.models.transaction import Transaction, TransactionStatus, TransactionType
from backend.app.repositories import AccountRepository, CategoryRepository, TransactionRepository
from backend.app.schemas import TransactionCreate, TransactionFilterParams, TransactionUpdate


class TransactionService:
    """Service para lógica de negócio de transações."""

    def __init__(self, db: Session) -> None:
        """
        Inicializa o service.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.repository = TransactionRepository(db)
        self.account_repository = AccountRepository(db)
        self.category_repository = CategoryRepository(db)

    def get_by_id(self, transaction_id: int) -> Transaction | None:
        """
        Busca transação por ID.

        Args:
            transaction_id: ID da transação

        Returns:
            Transação encontrada ou None

        Raises:
            ValueError: Se ID inválido
        """
        if transaction_id <= 0:
            raise ValueError("ID da transação deve ser maior que zero")

        return self.repository.get_by_id(transaction_id)

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: TransactionFilterParams | None = None,
    ) -> tuple[list[Transaction], int]:
        """
        Lista transações com filtros.

        Args:
            skip: Quantos registros pular
            limit: Limite de registros
            filters: Filtros de busca

        Returns:
            Tupla (lista de transações, total)
        """
        if filters:
            transactions = self.repository.search(
                search_term=filters.search or "",
                account_id=filters.account_id,
                category_id=filters.category_id,
                type=filters.type,
                status=filters.status,
                start_date=filters.date_from,
                end_date=filters.date_to,
                skip=skip,
                limit=limit,
            )
        else:
            transactions = self.repository.get_all(skip=skip, limit=limit)

        total = self.repository.count()

        return transactions, total

    def create_transaction(self, data: TransactionCreate) -> Transaction:
        """
        Cria nova transação e atualiza saldo da conta.

        Args:
            data: Dados da transação

        Returns:
            Transação criada

        Raises:
            ValueError: Se validação falhar
        """
        # Validar valor
        self.validate_transaction_amount(data.amount)

        # Verificar se conta existe
        account = self.account_repository.get_by_id(data.account_id)
        if not account:
            raise ValueError(f"Conta com ID {data.account_id} não encontrada")

        # Verificar se categoria existe
        category = self.category_repository.get_by_id(data.category_id)
        if not category:
            raise ValueError(f"Categoria com ID {data.category_id} não encontrada")

        # Verificar compatibilidade tipo transação x tipo categoria
        if data.type != category.type:
            raise ValueError(
                f"Tipo da transação ({data.type.value}) não compatível "
                f"com tipo da categoria ({category.type.value})"
            )

        # Criar transação
        transaction_data = data.model_dump()
        transaction = self.repository.create(transaction_data)

        # Atualizar saldo da conta se transação efetivada
        if transaction.status == TransactionStatus.COMPLETED:
            self._update_account_balance(account, transaction, is_new=True)

        return transaction

    def update_transaction(self, transaction_id: int, data: TransactionUpdate) -> Transaction:
        """
        Atualiza transação e recalcula saldo da conta.

        Args:
            transaction_id: ID da transação
            data: Novos dados

        Returns:
            Transação atualizada

        Raises:
            ValueError: Se transação não existir ou validação falhar
        """
        # Buscar transação
        transaction = self.repository.get_by_id(transaction_id)
        if not transaction:
            raise ValueError(f"Transação com ID {transaction_id} não encontrada")

        # Guardar valores antigos para recalcular saldo
        old_account_id = transaction.account_id
        old_amount = transaction.amount
        old_type = transaction.type
        old_status = transaction.status

        # Validar valor se fornecido
        if data.amount is not None:
            self.validate_transaction_amount(data.amount)

        # Verificar conta se fornecida
        if data.account_id:
            account = self.account_repository.get_by_id(data.account_id)
            if not account:
                raise ValueError(f"Conta com ID {data.account_id} não encontrada")

        # Verificar categoria se fornecida
        if data.category_id:
            category = self.category_repository.get_by_id(data.category_id)
            if not category:
                raise ValueError(f"Categoria com ID {data.category_id} não encontrada")

            # Verificar compatibilidade
            trans_type = data.type if data.type else transaction.type
            if trans_type != category.type:
                raise ValueError(
                    f"Tipo da transação ({trans_type.value}) não compatível "
                    f"com tipo da categoria ({category.type.value})"
                )

        # Atualizar transação
        update_data = data.model_dump(exclude_unset=True)
        updated_transaction = self.repository.update(transaction, update_data)

        # Recalcular saldos se necessário
        if old_status == TransactionStatus.COMPLETED:
            # Reverter impacto antigo
            old_account = self.account_repository.get_by_id(old_account_id)
            if old_account:
                self._revert_account_balance(old_account, old_amount, old_type)

        if updated_transaction.status == TransactionStatus.COMPLETED:
            # Aplicar novo impacto
            new_account = self.account_repository.get_by_id(updated_transaction.account_id)
            if new_account:
                self._update_account_balance(new_account, updated_transaction, is_new=True)

        return updated_transaction

    def delete_transaction(self, transaction_id: int) -> bool:
        """
        Deleta transação e recalcula saldo da conta.

        Args:
            transaction_id: ID da transação

        Returns:
            True se deletado com sucesso

        Raises:
            ValueError: Se transação não existir
        """
        # Buscar transação
        transaction = self.repository.get_by_id(transaction_id)
        if not transaction:
            raise ValueError(f"Transação com ID {transaction_id} não encontrada")

        # Se estava efetivada, reverter saldo
        if transaction.status == TransactionStatus.COMPLETED:
            account = self.account_repository.get_by_id(transaction.account_id)
            if account:
                self._revert_account_balance(account, transaction.amount, transaction.type)

        # Deletar transação
        return self.repository.delete(transaction_id)

    def change_transaction_status(
        self, transaction_id: int, new_status: TransactionStatus
    ) -> Transaction:
        """
        Altera status da transação e atualiza saldo.

        Pendente → Efetivada: adiciona ao saldo
        Efetivada → Pendente: remove do saldo

        Args:
            transaction_id: ID da transação
            new_status: Novo status

        Returns:
            Transação atualizada

        Raises:
            ValueError: Se transação não existir
        """
        transaction = self.repository.get_by_id(transaction_id)
        if not transaction:
            raise ValueError(f"Transação com ID {transaction_id} não encontrada")

        old_status = transaction.status

        # Se status não mudou, não faz nada
        if old_status == new_status:
            return transaction

        # Buscar conta
        account = self.account_repository.get_by_id(transaction.account_id)
        if not account:
            raise ValueError(f"Conta com ID {transaction.account_id} não encontrada")

        # Atualizar status
        updated = self.repository.change_status(transaction_id, new_status)

        # Ajustar saldo
        if old_status == TransactionStatus.PENDING and new_status == TransactionStatus.COMPLETED:
            # Pendente → Efetivada: adiciona ao saldo
            self._update_account_balance(account, updated, is_new=True)
        elif old_status == TransactionStatus.COMPLETED and new_status == TransactionStatus.PENDING:
            # Efetivada → Pendente: remove do saldo
            self._revert_account_balance(account, updated.amount, updated.type)

        return updated

    def validate_transaction_amount(self, amount: Decimal) -> None:
        """
        Valida valor da transação.

        Args:
            amount: Valor a validar

        Raises:
            ValueError: Se valor inválido
        """
        if amount == 0:
            raise ValueError("O valor da transação não pode ser zero")

    def handle_negative_transaction(self, amount: Decimal, type: TransactionType) -> bool:
        """
        Verifica se é um estorno (valor negativo).

        Args:
            amount: Valor da transação
            type: Tipo da transação

        Returns:
            True se é estorno, False caso contrário
        """
        return amount < 0

    def _update_account_balance(
        self, account: any, transaction: Transaction, is_new: bool = False
    ) -> None:
        """
        Atualiza saldo da conta baseado na transação.

        Args:
            account: Conta a atualizar
            transaction: Transação que afeta o saldo
            is_new: Se True, adiciona; se False, não faz nada
        """
        if transaction.type == TransactionType.INCOME:
            new_balance = account.current_balance + transaction.amount
        else:  # EXPENSE
            new_balance = account.current_balance - transaction.amount

        self.account_repository.update_balance(account.id, new_balance)

    def _revert_account_balance(self, account: any, amount: Decimal, type: TransactionType) -> None:
        """
        Reverte impacto de uma transação no saldo.

        Args:
            account: Conta a reverter
            amount: Valor da transação
            type: Tipo da transação
        """
        if type == TransactionType.INCOME:
            new_balance = account.current_balance - amount
        else:  # EXPENSE
            new_balance = account.current_balance + amount

        self.account_repository.update_balance(account.id, new_balance)

    def get_summary(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
        only_completed: bool = True,
    ) -> dict[str, any]:
        """
        Retorna resumo financeiro.

        Args:
            start_date: Data inicial (opcional)
            end_date: Data final (opcional)
            only_completed: Se True, considera apenas efetivadas

        Returns:
            Dicionário com resumo
        """
        total_income = self.repository.get_total_by_type(
            TransactionType.INCOME,
            TransactionStatus.COMPLETED if only_completed else None,
            start_date,
            end_date,
        )

        total_expense = self.repository.get_total_by_type(
            TransactionType.EXPENSE,
            TransactionStatus.COMPLETED if only_completed else None,
            start_date,
            end_date,
        )

        balance = self.repository.get_balance(start_date, end_date, only_completed)

        total_transactions = self.repository.count()

        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "total_transactions": total_transactions,
            "period_start": start_date,
            "period_end": end_date,
        }
