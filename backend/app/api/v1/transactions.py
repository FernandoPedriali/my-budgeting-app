"""Transactions API endpoints."""

from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db
from backend.app.core.exceptions import BadRequestException, NotFoundException
from backend.app.models.transaction import TransactionStatus, TransactionType
from backend.app.schemas import (
    MessageResponse,
    TransactionCreate,
    TransactionFilterParams,
    TransactionListResponse,
    TransactionResponse,
    TransactionStatusUpdate,
    TransactionSummary,
    TransactionUpdate,
)
from backend.app.services import TransactionService

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=TransactionListResponse)
def list_transactions(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(50, ge=1, le=100, description="Limite de registros"),
    account_id: int | None = Query(None, description="Filtrar por conta"),
    category_id: int | None = Query(None, description="Filtrar por categoria"),
    type: TransactionType | None = Query(None, description="Filtrar por tipo"),
    status: TransactionStatus | None = Query(None, description="Filtrar por status"),
    date_from: date | None = Query(None, description="Data inicial"),
    date_to: date | None = Query(None, description="Data final"),
    search: str | None = Query(None, description="Buscar na descrição"),
    min_amount: Decimal | None = Query(None, description="Valor mínimo"),
    max_amount: Decimal | None = Query(None, description="Valor máximo"),
    db: Session = Depends(get_db),
) -> TransactionListResponse:
    """
    Lista todas as transações com filtros opcionais.

    - **skip**: Paginação - quantos registros pular
    - **limit**: Paginação - limite de registros (máx: 100)
    - **account_id**: Filtrar por conta específica
    - **category_id**: Filtrar por categoria específica
    - **type**: Filtrar por tipo (income/expense)
    - **status**: Filtrar por status (pending/completed)
    - **date_from**: Data inicial do período
    - **date_to**: Data final do período
    - **search**: Buscar na descrição ou observações
    - **min_amount**: Valor mínimo
    - **max_amount**: Valor máximo
    """
    service = TransactionService(db)

    filters = TransactionFilterParams(
        account_id=account_id,
        category_id=category_id,
        type=type,
        status=status,
        date_from=date_from,
        date_to=date_to,
        search=search,
        min_amount=min_amount,
        max_amount=max_amount,
    )

    transactions, total = service.get_all(skip=skip, limit=limit, filters=filters)

    # Calcular totais
    summary = service.get_summary(start_date=date_from, end_date=date_to)

    return TransactionListResponse(
        transactions=[TransactionResponse.model_validate(trans) for trans in transactions],
        total=total,
        total_income=summary["total_income"],
        total_expense=summary["total_expense"],
        balance=summary["balance"],
    )


@router.get("/summary", response_model=TransactionSummary)
def get_transactions_summary(
    start_date: date | None = Query(None, description="Data inicial"),
    end_date: date | None = Query(None, description="Data final"),
    only_completed: bool = Query(True, description="Apenas efetivadas"),
    db: Session = Depends(get_db),
) -> TransactionSummary:
    """
    Retorna resumo financeiro das transações.

    - **start_date**: Data inicial do período (opcional)
    - **end_date**: Data final do período (opcional)
    - **only_completed**: Se True, considera apenas transações efetivadas
    """
    service = TransactionService(db)
    summary = service.get_summary(start_date, end_date, only_completed)

    return TransactionSummary(**summary)


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
) -> TransactionResponse:
    """
    Busca uma transação por ID.

    - **transaction_id**: ID da transação
    """
    service = TransactionService(db)

    try:
        transaction = service.get_by_id(transaction_id)
        if not transaction:
            raise NotFoundException(f"Transação com ID {transaction_id} não encontrada")

        return TransactionResponse.model_validate(transaction)

    except ValueError as e:
        raise BadRequestException(str(e))


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    data: TransactionCreate,
    db: Session = Depends(get_db),
) -> TransactionResponse:
    """
    Cria uma nova transação.

    **Importante**: Se a transação for criada com status "completed" (efetivada),
    o saldo da conta será atualizado automaticamente.

    - **description**: Descrição da transação (obrigatório)
    - **amount**: Valor da transação (obrigatório, não pode ser zero)
    - **type**: Tipo da transação - income ou expense (obrigatório)
    - **status**: Status - pending ou completed (padrão: pending)
    - **transaction_date**: Data da transação (obrigatório)
    - **account_id**: ID da conta (obrigatório)
    - **category_id**: ID da categoria (obrigatório)
    - **notes**: Observações adicionais (opcional)
    """
    service = TransactionService(db)

    try:
        transaction = service.create_transaction(data)
        return TransactionResponse.model_validate(transaction)

    except ValueError as e:
        raise BadRequestException(str(e))


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    db: Session = Depends(get_db),
) -> TransactionResponse:
    """
    Atualiza uma transação existente.

    Todos os campos são opcionais. Apenas os campos fornecidos serão atualizados.

    **Importante**: Se o valor, tipo, status ou conta forem alterados,
    o saldo será recalculado automaticamente.

    - **transaction_id**: ID da transação
    - **description**: Nova descrição (opcional)
    - **amount**: Novo valor (opcional)
    - **type**: Novo tipo (opcional)
    - **status**: Novo status (opcional)
    - **transaction_date**: Nova data (opcional)
    - **account_id**: Nova conta (opcional)
    - **category_id**: Nova categoria (opcional)
    - **notes**: Novas observações (opcional)
    """
    service = TransactionService(db)

    try:
        transaction = service.update_transaction(transaction_id, data)
        return TransactionResponse.model_validate(transaction)

    except ValueError as e:
        raise BadRequestException(str(e))


@router.delete("/{transaction_id}", response_model=MessageResponse)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
) -> MessageResponse:
    """
    Deleta uma transação permanentemente.

    **Importante**: Se a transação estava efetivada, o saldo da conta
    será ajustado automaticamente.

    - **transaction_id**: ID da transação
    """
    service = TransactionService(db)

    try:
        success = service.delete_transaction(transaction_id)

        if success:
            return MessageResponse(
                message="Transação deletada com sucesso",
                success=True,
            )
        else:
            raise NotFoundException(f"Transação com ID {transaction_id} não encontrada")

    except ValueError as e:
        raise BadRequestException(str(e))


@router.patch("/{transaction_id}/status", response_model=TransactionResponse)
def change_transaction_status(
    transaction_id: int,
    data: TransactionStatusUpdate,
    db: Session = Depends(get_db),
) -> TransactionResponse:
    """
    Altera o status de uma transação.

    **Importante**: A mudança de status afeta o saldo da conta:
    - **Pendente → Efetivada**: Adiciona ao saldo
    - **Efetivada → Pendente**: Remove do saldo

    - **transaction_id**: ID da transação
    - **status**: Novo status (pending ou completed)
    """
    service = TransactionService(db)

    try:
        transaction = service.change_transaction_status(transaction_id, data.status)
        return TransactionResponse.model_validate(transaction)

    except ValueError as e:
        raise BadRequestException(str(e))
