"""Script para testar models e schemas manualmente."""

import sys
from pathlib import Path

# Adicionar raiz do projeto ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from datetime import date
from decimal import Decimal

from backend.app.database import SessionLocal
from backend.app.models import (
    Account,
    AccountType,
    Category,
    CategoryType,
    Transaction,
    TransactionStatus,
    TransactionType,
)
from backend.app.schemas import (
    AccountCreate,
    AccountResponse,
    CategoryCreate,
    CategoryResponse,
    TransactionCreate,
    TransactionResponse,
)


def test_categories() -> None:
    """Testa criação e consulta de categorias."""
    print("\n=== TESTANDO CATEGORIES ===")

    db = SessionLocal()

    try:
        # Criar categoria
        cat = Category(
            name="Alimentação",
            type=CategoryType.EXPENSE,
            color="#EF4444",
            icon="shopping-cart",
            description="Gastos com alimentação",
        )
        db.add(cat)
        db.commit()
        db.refresh(cat)
        print(f"✅ Categoria criada: {cat}")

        # Buscar categoria
        found = db.query(Category).filter(Category.name == "Alimentação").first()
        print(f"✅ Categoria encontrada: {found}")

        # Testar schema
        response = CategoryResponse.model_validate(found)
        print(f"✅ Schema Response: {response.model_dump_json(indent=2)}")

        # Testar validação
        create_data = CategoryCreate(
            name="Transporte", type=CategoryType.EXPENSE, color="#3B82F6", icon="car"
        )
        print(f"✅ Schema Create validado: {create_data}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()


def test_accounts() -> None:
    """Testa criação e consulta de contas."""
    print("\n=== TESTANDO ACCOUNTS ===")

    db = SessionLocal()

    try:
        # Criar conta
        acc = Account(
            name="Nubank",
            type=AccountType.CHECKING,
            initial_balance=Decimal("1000.00"),
            current_balance=Decimal("1000.00"),
            color="#8B5CF6",
            icon="credit-card",
        )
        db.add(acc)
        db.commit()
        db.refresh(acc)
        print(f"✅ Conta criada: {acc}")

        # Buscar conta
        found = db.query(Account).filter(Account.name == "Nubank").first()
        print(f"✅ Conta encontrada: {found}")
        print(f"   Saldo: R$ {found.current_balance}")

        # Testar schema
        response = AccountResponse.model_validate(found)
        print(f"✅ Schema Response: {response.model_dump_json(indent=2)}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()


def test_transactions() -> None:
    """Testa criação e consulta de transações."""
    print("\n=== TESTANDO TRANSACTIONS ===")

    db = SessionLocal()

    try:
        # Buscar categoria e conta criadas anteriormente
        category = db.query(Category).first()
        account = db.query(Account).first()

        if not category or not account:
            print("⚠️  Execute test_categories() e test_accounts() primeiro!")
            return

        # Criar transação
        trans = Transaction(
            description="Supermercado",
            amount=Decimal("150.50"),
            type=TransactionType.EXPENSE,
            status=TransactionStatus.COMPLETED,
            transaction_date=date.today(),
            account_id=account.id,
            category_id=category.id,
            notes="Compras do mês",
        )
        db.add(trans)
        db.commit()
        db.refresh(trans)
        print(f"✅ Transação criada: {trans}")

        # Buscar transação com relacionamentos
        found = db.query(Transaction).filter(Transaction.id == trans.id).first()
        print(f"✅ Transação encontrada: {found}")
        print(f"   Conta: {found.account.name}")
        print(f"   Categoria: {found.category.name}")

        # Testar schema
        response = TransactionResponse.model_validate(found)
        print(f"✅ Schema Response: {response.model_dump_json(indent=2)}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()


def test_validations() -> None:
    """Testa validações dos schemas."""
    print("\n=== TESTANDO VALIDAÇÕES ===")

    # Testar validação de cor inválida
    try:
        CategoryCreate(name="Teste", type=CategoryType.INCOME, color="invalid")  # Cor inválida
        print("❌ Deveria ter falhado!")
    except Exception as e:
        print(f"✅ Validação de cor funcionou: {e}")

    # Testar validação de valor zero
    try:
        TransactionCreate(
            description="Teste",
            amount=Decimal("0.00"),  # Valor zero
            type=TransactionType.EXPENSE,
            transaction_date=date.today(),
            account_id=1,
            category_id=1,
        )
        print("❌ Deveria ter falhado!")
    except Exception as e:
        print(f"✅ Validação de valor zero funcionou: {e}")

    # Testar validação de nome vazio
    try:
        AccountCreate(name="   ", type=AccountType.CASH)  # Nome vazio
        print("❌ Deveria ter falhado!")
    except Exception as e:
        print(f"✅ Validação de nome vazio funcionou: {e}")


def cleanup() -> None:
    """Limpa os dados de teste."""
    print("\n=== LIMPANDO DADOS DE TESTE ===")

    db = SessionLocal()

    try:
        # Deletar todas as transações
        db.query(Transaction).delete()
        # Deletar todas as contas
        db.query(Account).delete()
        # Deletar todas as categorias
        db.query(Category).delete()

        db.commit()
        print("✅ Dados de teste removidos!")

    except Exception as e:
        print(f"❌ Erro ao limpar: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Iniciando testes dos Models e Schemas...")

    # Executar testes
    test_categories()
    test_accounts()
    test_transactions()
    test_validations()

    # Perguntar se quer limpar
    print("\n")
    response = input("Deseja limpar os dados de teste? (s/n): ")
    if response.lower() == "s":
        cleanup()

    print("\n✨ Testes concluídos!")
