"""Account service with business logic."""

from decimal import Decimal

from sqlalchemy.orm import Session

from backend.app.models.account import Account, AccountType
from backend.app.repositories import AccountRepository
from backend.app.schemas import AccountCreate, AccountFilterParams, AccountUpdate


class AccountService:
    """Service para lógica de negócio de contas."""

    def __init__(self, db: Session) -> None:
        """
        Inicializa o service.

        Args:
            db: Sessão do banco de dados
        """
        self.db = db
        self.repository = AccountRepository(db)

    def get_by_id(self, account_id: int) -> Account | None:
        """
        Busca conta por ID.

        Args:
            account_id: ID da conta

        Returns:
            Conta encontrada ou None

        Raises:
            ValueError: Se ID inválido
        """
        if account_id <= 0:
            raise ValueError("ID da conta deve ser maior que zero")

        return self.repository.get_by_id(account_id)

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: AccountFilterParams | None = None,
    ) -> tuple[list[Account], int]:
        """
        Lista contas com filtros.

        Args:
            skip: Quantos registros pular
            limit: Limite de registros
            filters: Filtros de busca

        Returns:
            Tupla (lista de contas, total)
        """
        if filters:
            # Busca com filtros
            if filters.search:
                accounts = self.repository.search(
                    search_term=filters.search,
                    type=filters.type,
                    skip=skip,
                    limit=limit,
                    only_active=filters.only_active
                    or (filters.is_active if filters.is_active is not None else True),
                )
            elif filters.type:
                accounts = self.repository.get_by_type(
                    type=filters.type,
                    skip=skip,
                    limit=limit,
                    only_active=filters.only_active
                    or (filters.is_active if filters.is_active is not None else True),
                )
            elif filters.only_active:
                accounts = self.repository.get_active(skip=skip, limit=limit)
            else:
                accounts = self.repository.get_all(
                    skip=skip,
                    limit=limit,
                    only_active=filters.is_active if filters.is_active is not None else True,
                )
        else:
            accounts = self.repository.get_all(skip=skip, limit=limit, only_active=True)

        total = self.repository.count(only_active=filters.only_active if filters else True)

        return accounts, total

    def create(self, data: AccountCreate) -> Account:
        """
        Cria nova conta.

        Args:
            data: Dados da conta

        Returns:
            Conta criada

        Raises:
            ValueError: Se validação falhar
        """
        # Validar tipo
        self.validate_account_type(data.type)

        # Verificar nome duplicado
        if self.repository.is_name_taken(data.name):
            raise ValueError(f"Já existe uma conta com o nome '{data.name}'")

        # Criar conta com saldo inicial = saldo atual
        account_data = data.model_dump()
        account_data["current_balance"] = data.initial_balance

        return self.repository.create(account_data)

    def update(self, account_id: int, data: AccountUpdate) -> Account:
        """
        Atualiza conta existente.

        Args:
            account_id: ID da conta
            data: Novos dados

        Returns:
            Conta atualizada

        Raises:
            ValueError: Se conta não existir ou validação falhar
        """
        # Buscar conta
        account = self.repository.get_by_id(account_id)
        if not account:
            raise ValueError(f"Conta com ID {account_id} não encontrada")

        # Validar tipo se fornecido
        if data.type:
            self.validate_account_type(data.type)

        # Verificar nome duplicado se fornecido
        if data.name and self.repository.is_name_taken(data.name, exclude_id=account_id):
            raise ValueError(f"Já existe uma conta com o nome '{data.name}'")

        # Atualizar apenas campos fornecidos
        update_data = data.model_dump(exclude_unset=True)
        return self.repository.update(account, update_data)

    def delete(self, account_id: int, soft: bool = True) -> bool:
        """
        Deleta conta.

        Args:
            account_id: ID da conta
            soft: Se True, faz soft delete; se False, deleta permanentemente

        Returns:
            True se deletado com sucesso

        Raises:
            ValueError: Se conta não existir ou não puder ser deletada
        """
        # Verificar se conta existe
        account = self.repository.get_by_id(account_id)
        if not account:
            raise ValueError(f"Conta com ID {account_id} não encontrada")

        # Verificar se pode deletar
        if not self.check_account_deletable(account_id):
            raise ValueError(
                "Não é possível deletar conta com transações associadas. "
                "Delete as transações primeiro."
            )

        # Deletar
        if soft:
            result = self.repository.soft_delete(account_id)
            return result is not None
        else:
            return self.repository.delete(account_id)

    def restore(self, account_id: int) -> Account:
        """
        Restaura conta deletada logicamente.

        Args:
            account_id: ID da conta

        Returns:
            Conta restaurada

        Raises:
            ValueError: Se conta não existir
        """
        account = self.repository.restore(account_id)
        if not account:
            raise ValueError(f"Conta com ID {account_id} não encontrada")

        return account

    def calculate_balance(self, account_id: int) -> Decimal:
        """
        Calcula saldo atual da conta baseado nas transações.

        Este método recalcula o saldo baseado no saldo inicial
        e todas as transações efetivadas.

        Args:
            account_id: ID da conta

        Returns:
            Saldo calculado

        Raises:
            ValueError: Se conta não existir
        """
        from backend.app.models.transaction import TransactionStatus, TransactionType
        from backend.app.repositories import TransactionRepository

        account = self.repository.get_by_id(account_id)
        if not account:
            raise ValueError(f"Conta com ID {account_id} não encontrada")

        # Buscar todas as transações efetivadas da conta
        trans_repo = TransactionRepository(self.db)
        transactions = trans_repo.get_by_account(account_id)

        # Calcular saldo
        balance = account.initial_balance

        for trans in transactions:
            # Apenas transações efetivadas afetam o saldo
            if trans.status == TransactionStatus.COMPLETED:
                if trans.type == TransactionType.INCOME:
                    balance += trans.amount
                else:  # EXPENSE
                    balance -= trans.amount

        return balance

    def update_balance(self, account_id: int, new_balance: Decimal) -> Account:
        """
        Atualiza saldo da conta.

        Args:
            account_id: ID da conta
            new_balance: Novo saldo

        Returns:
            Conta atualizada

        Raises:
            ValueError: Se conta não existir
        """
        account = self.repository.update_balance(account_id, new_balance)
        if not account:
            raise ValueError(f"Conta com ID {account_id} não encontrada")

        return account

    def validate_account_type(self, type: AccountType) -> None:
        """
        Valida tipo de conta.

        Args:
            type: Tipo a validar

        Raises:
            ValueError: Se tipo inválido
        """
        valid_types = [
            AccountType.CHECKING,
            AccountType.SAVINGS,
            AccountType.INVESTMENT,
            AccountType.CREDIT_CARD,
            AccountType.CASH,
            AccountType.OTHER,
        ]
        if type not in valid_types:
            raise ValueError(
                f"Tipo de conta inválido. Valores válidos: {[t.value for t in valid_types]}"
            )

    def check_account_deletable(self, account_id: int) -> bool:
        """
        Verifica se conta pode ser deletada.

        Uma conta só pode ser deletada se não tiver transações.

        Args:
            account_id: ID da conta

        Returns:
            True se pode deletar, False caso contrário
        """
        return self.repository.can_delete(account_id)

    def get_total_balance(self) -> Decimal:
        """
        Calcula saldo total de todas as contas ativas.

        Returns:
            Saldo total
        """
        return self.repository.get_total_balance(only_active=True)

    def get_statistics(self) -> dict[str, any]:
        """
        Retorna estatísticas de contas.

        Returns:
            Dicionário com estatísticas
        """
        return {
            "total": self.repository.count(only_active=False),
            "active": self.repository.count(only_active=True),
            "total_balance": self.get_total_balance(),
        }
