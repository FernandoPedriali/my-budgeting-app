"""Accounts API endpoints."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.core.exceptions import BadRequestException, NotFoundException
from backend.app.models.account import AccountType
from backend.app.schemas import (
    AccountBalanceResponse,
    AccountCreate,
    AccountFilterParams,
    AccountListResponse,
    AccountResponse,
    AccountUpdate,
    MessageResponse,
)
from backend.app.services import AccountService

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=AccountListResponse)
def list_accounts(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(50, ge=1, le=100, description="Limite de registros"),
    type: AccountType | None = Query(None, description="Filtrar por tipo"),
    search: str | None = Query(None, description="Buscar por nome"),
    is_active: bool | None = Query(None, description="Filtrar por status ativo"),
    only_active: bool = Query(False, description="Retornar apenas contas ativas"),
    db: Session = Depends(get_db),
) -> AccountListResponse:
    """
    Lista todas as contas com filtros opcionais.

    - **skip**: Paginação - quantos registros pular
    - **limit**: Paginação - limite de registros (máx: 100)
    - **type**: Filtrar por tipo de conta
    - **search**: Buscar por nome ou descrição
    - **is_active**: Filtrar por status ativo/inativo
    - **only_active**: Se True, retorna apenas contas ativas
    """
    service = AccountService(db)

    filters = AccountFilterParams(
        type=type,
        search=search,
        is_active=is_active,
        only_active=only_active,
    )

    accounts, total = service.get_all(skip=skip, limit=limit, filters=filters)
    total_balance = service.get_total_balance()

    return AccountListResponse(
        accounts=[AccountResponse.model_validate(acc) for acc in accounts],
        total=total,
        total_balance=total_balance,
    )


@router.get("/active", response_model=AccountListResponse)
def list_active_accounts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
) -> AccountListResponse:
    """
    Lista apenas contas ativas.

    Atalho para listar contas com only_active=True.

    - **skip**: Paginação - quantos registros pular
    - **limit**: Paginação - limite de registros
    """
    service = AccountService(db)

    filters = AccountFilterParams(only_active=True)
    accounts, total = service.get_all(skip=skip, limit=limit, filters=filters)
    total_balance = service.get_total_balance()

    return AccountListResponse(
        accounts=[AccountResponse.model_validate(acc) for acc in accounts],
        total=total,
        total_balance=total_balance,
    )


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    db: Session = Depends(get_db),
) -> AccountResponse:
    """
    Busca uma conta por ID.

    - **account_id**: ID da conta
    """
    service = AccountService(db)

    try:
        account = service.get_by_id(account_id)
        if not account:
            raise NotFoundException(f"Conta com ID {account_id} não encontrada")

        return AccountResponse.model_validate(account)

    except ValueError as e:
        raise BadRequestException(str(e))


@router.get("/{account_id}/balance", response_model=AccountBalanceResponse)
def get_account_balance(
    account_id: int,
    db: Session = Depends(get_db),
) -> AccountBalanceResponse:
    """
    Obtém o saldo atual de uma conta.

    - **account_id**: ID da conta
    """
    service = AccountService(db)

    try:
        account = service.get_by_id(account_id)
        if not account:
            raise NotFoundException(f"Conta com ID {account_id} não encontrada")

        return AccountBalanceResponse(
            account_id=account.id,
            account_name=account.name,
            current_balance=account.current_balance,
        )

    except ValueError as e:
        raise BadRequestException(str(e))


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    data: AccountCreate,
    db: Session = Depends(get_db),
) -> AccountResponse:
    """
    Cria uma nova conta.

    - **name**: Nome da conta (obrigatório, único)
    - **type**: Tipo da conta (obrigatório)
    - **initial_balance**: Saldo inicial (padrão: 0.00)
    - **description**: Descrição opcional
    - **color**: Cor em hexadecimal (padrão: #3B82F6)
    - **icon**: Nome do ícone (padrão: wallet)
    """
    service = AccountService(db)

    try:
        account = service.create(data)
        return AccountResponse.model_validate(account)

    except ValueError as e:
        raise BadRequestException(str(e))


@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int,
    data: AccountUpdate,
    db: Session = Depends(get_db),
) -> AccountResponse:
    """
    Atualiza uma conta existente.

    Todos os campos são opcionais. Apenas os campos fornecidos serão atualizados.

    **Atenção**: Não é possível atualizar o saldo diretamente por este endpoint.
    O saldo é atualizado automaticamente pelas transações.

    - **account_id**: ID da conta
    - **name**: Novo nome (opcional)
    - **type**: Novo tipo (opcional)
    - **description**: Nova descrição (opcional)
    - **color**: Nova cor (opcional)
    - **icon**: Novo ícone (opcional)
    """
    service = AccountService(db)

    try:
        account = service.update(account_id, data)
        return AccountResponse.model_validate(account)

    except ValueError as e:
        raise BadRequestException(str(e))


@router.delete("/{account_id}", response_model=MessageResponse)
def delete_account(
    account_id: int,
    permanent: bool = Query(False, description="Se True, deleta permanentemente"),
    db: Session = Depends(get_db),
) -> MessageResponse:
    """
    Deleta uma conta.

    Por padrão, faz soft delete (exclusão lógica).
    Use permanent=True para deletar permanentemente.

    **Atenção**: Não é possível deletar contas com transações associadas.

    - **account_id**: ID da conta
    - **permanent**: Se True, deleta permanentemente (padrão: False)
    """
    service = AccountService(db)

    try:
        success = service.delete(account_id, soft=not permanent)

        if success:
            action = "deletada permanentemente" if permanent else "desativada"
            return MessageResponse(
                message=f"Conta {action} com sucesso",
                success=True,
            )
        else:
            raise NotFoundException(f"Conta com ID {account_id} não encontrada")

    except ValueError as e:
        raise BadRequestException(str(e))


@router.patch("/{account_id}/restore", response_model=AccountResponse)
def restore_account(
    account_id: int,
    db: Session = Depends(get_db),
) -> AccountResponse:
    """
    Restaura uma conta deletada logicamente.

    - **account_id**: ID da conta
    """
    service = AccountService(db)

    try:
        account = service.restore(account_id)
        return AccountResponse.model_validate(account)

    except ValueError as e:
        raise BadRequestException(str(e))
