"""Script para testar repositories manualmente."""

import sys
from pathlib import Path

# Adicionar raiz do projeto ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from datetime import date, timedelta
from decimal import Decimal

from backend.app.database import SessionLocal
from backend.app.models import AccountType, CategoryType, TransactionStatus, TransactionType
from backend.app.repositories import AccountRepository, CategoryRepository, TransactionRepository


def test_category_repository() -> None:
    """Testa CategoryRepository."""
    print("\n=== TESTANDO CATEGORY REPOSITORY ===")

    db = SessionLocal()
    repo = CategoryRepository(db)

    try:
        # Criar categorias
        print("\n📝 Criando categorias...")
        cat1 = repo.create(
            {
                "name": "Salário",
                "type": CategoryType.INCOME,
                "color": "#10B981",
                "icon": "dollar-sign",
                "description": "Renda mensal",
            }
        )
        print(f"✅ Categoria criada: {cat1.name}")

        cat2 = repo.create(
            {
                "name": "Alimentação",
                "type": CategoryType.EXPENSE,
                "color": "#EF4444",
                "icon": "shopping-cart",
            }
        )
        print(f"✅ Categoria criada: {cat2.name}")

        cat3 = repo.create(
            {"name": "Transporte", "type": CategoryType.EXPENSE, "color": "#3B82F6", "icon": "car"}
        )
        print(f"✅ Categoria criada: {cat3.name}")

        # Buscar por ID
        print("\n🔍 Buscando por ID...")
        found = repo.get_by_id(cat1.id)
        print(f"✅ Encontrada: {found.name if found else 'None'}")

        # Buscar por nome
        print("\n🔍 Buscando por nome...")
        found = repo.get_by_name("Alimentação")
        print(f"✅ Encontrada: {found.name if found else 'None'}")

        # Buscar por tipo
        print("\n🔍 Buscando por tipo (EXPENSE)...")
        expenses = repo.get_by_type(CategoryType.EXPENSE)
        print(f"✅ Encontradas {len(expenses)} categorias de despesa")
        for cat in expenses:
            print(f"   - {cat.name}")

        # Buscar todas
        print("\n📋 Listando todas...")
        all_cats = repo.get_all()
        print(f"✅ Total: {len(all_cats)} categorias")

        # Contar
        print("\n🔢 Contando...")
        total = repo.count()
        print(f"✅ Total no banco: {total}")

        # Verificar nome duplicado
        print("\n✔️  Verificando nome duplicado...")
        is_taken = repo.is_name_taken("Salário")
        print(f"✅ Nome 'Salário' está em uso: {is_taken}")

        is_taken = repo.is_name_taken("Investimentos")
        print(f"✅ Nome 'Investimentos' está em uso: {is_taken}")

        # Buscar com search
        print("\n🔍 Buscando com search...")
        results = repo.search("trans")
        print(f"✅ Encontradas {len(results)} categorias com 'trans'")

        # Atualizar
        print("\n✏️  Atualizando categoria...")
        updated = repo.update(cat3, {"description": "Gastos com transporte"})
        print(f"✅ Categoria atualizada: {updated.description}")

        # Soft delete
        print("\n🗑️  Soft delete...")
        deleted = repo.soft_delete(cat3.id)
        print(f"✅ Categoria deletada logicamente: is_active={deleted.is_active}")

        # Verificar contagem apenas ativos
        total_active = repo.count(only_active=True)
        print(f"✅ Total de categorias ativas: {total_active}")

        # Restaurar
        print("\n♻️  Restaurando categoria...")
        restored = repo.restore(cat3.id)
        print(f"✅ Categoria restaurada: is_active={restored.is_active}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()


def test_account_repository() -> None:
    """Testa AccountRepository."""
    print("\n=== TESTANDO ACCOUNT REPOSITORY ===")

    db = SessionLocal()
    repo = AccountRepository(db)

    try:
        # Criar contas
        print("\n📝 Criando contas...")
        acc1 = repo.create(
            {
                "name": "Nubank",
                "type": AccountType.CHECKING,
                "initial_balance": Decimal("5000.00"),
                "current_balance": Decimal("5000.00"),
                "color": "#8B5CF6",
                "icon": "credit-card",
            }
        )
        print(f"✅ Conta criada: {acc1.name} - Saldo: R$ {acc1.current_balance}")

        acc2 = repo.create(
            {
                "name": "Inter",
                "type": AccountType.SAVINGS,
                "initial_balance": Decimal("10000.00"),
                "current_balance": Decimal("10000.00"),
                "color": "#F97316",
                "icon": "piggy-bank",
            }
        )
        print(f"✅ Conta criada: {acc2.name} - Saldo: R$ {acc2.current_balance}")

        acc3 = repo.create(
            {
                "name": "Carteira",
                "type": AccountType.CASH,
                "initial_balance": Decimal("200.00"),
                "current_balance": Decimal("200.00"),
                "color": "#10B981",
                "icon": "wallet",
            }
        )
        print(f"✅ Conta criada: {acc3.name} - Saldo: R$ {acc3.current_balance}")

        # Buscar por ID
        print("\n🔍 Buscando por ID...")
        found = repo.get_by_id(acc1.id)
        print(f"✅ Encontrada: {found.name if found else 'None'}")

        # Buscar por tipo
        print("\n🔍 Buscando por tipo (CHECKING)...")
        checkings = repo.get_by_type(AccountType.CHECKING)
        print(f"✅ Encontradas {len(checkings)} contas correntes")

        # Buscar apenas ativas
        print("\n🔍 Buscando apenas ativas...")
        active = repo.get_active()
        print(f"✅ Contas ativas: {len(active)}")

        # Saldo total
        print("\n💰 Calculando saldo total...")
        total = repo.get_total_balance()
        print(f"✅ Saldo total: R$ {total}")

        # Atualizar saldo
        print("\n💸 Atualizando saldo...")
        new_balance = Decimal("4500.00")
        updated = repo.update_balance(acc1.id, new_balance)
        print(f"✅ Novo saldo de {updated.name}: R$ {updated.current_balance}")

        # Verificar nome duplicado
        print("\n✔️  Verificando nome duplicado...")
        is_taken = repo.is_name_taken("Nubank")
        print(f"✅ Nome 'Nubank' está em uso: {is_taken}")

        # Buscar com search
        print("\n🔍 Buscando com search...")
        results = repo.search("bank")
        print(f"✅ Encontradas {len(results)} contas com 'bank'")

        # Verificar se tem transações
        print("\n🔍 Verificando transações...")
        has_trans = repo.has_transactions(acc1.id)
        print(f"✅ Conta tem transações: {has_trans}")

        # Verificar se pode deletar
        print("\n🔍 Verificando se pode deletar...")
        can_delete = repo.can_delete(acc1.id)
        print(f"✅ Pode deletar: {can_delete}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()


def test_transaction_repository() -> None:
    """Testa TransactionRepository."""
    print("\n=== TESTANDO TRANSACTION REPOSITORY ===")

    db = SessionLocal()
    repo = TransactionRepository(db)
    cat_repo = CategoryRepository(db)
    acc_repo = AccountRepository(db)

    try:
        # Buscar categoria e conta criadas anteriormente
        category = cat_repo.get_by_name("Alimentação")
        account = acc_repo.get_by_name("Nubank")

        if not category or not account:
            print("⚠️  Execute test_category_repository() e test_account_repository() primeiro!")
            return

        # Criar transações
        print("\n📝 Criando transações...")

        # Receita
        trans1 = repo.create(
            {
                "description": "Salário",
                "amount": Decimal("5000.00"),
                "type": TransactionType.INCOME,
                "status": TransactionStatus.COMPLETED,
                "transaction_date": date.today(),
                "account_id": account.id,
                "category_id": cat_repo.get_by_name("Salário").id,
            }
        )
        print(f"✅ Transação criada: {trans1.description} - R$ {trans1.amount}")

        # Despesa
        trans2 = repo.create(
            {
                "description": "Supermercado",
                "amount": Decimal("250.50"),
                "type": TransactionType.EXPENSE,
                "status": TransactionStatus.COMPLETED,
                "transaction_date": date.today() - timedelta(days=1),
                "account_id": account.id,
                "category_id": category.id,
                "notes": "Compras do mês",
            }
        )
        print(f"✅ Transação criada: {trans2.description} - R$ {trans2.amount}")

        # Despesa pendente
        trans3 = repo.create(
            {
                "description": "Restaurante",
                "amount": Decimal("80.00"),
                "type": TransactionType.EXPENSE,
                "status": TransactionStatus.PENDING,
                "transaction_date": date.today(),
                "account_id": account.id,
                "category_id": category.id,
            }
        )
        print(f"✅ Transação criada: {trans3.description} - R$ {trans3.amount} (PENDENTE)")

        # Buscar por ID (com relacionamentos)
        print("\n🔍 Buscando por ID...")
        found = repo.get_by_id(trans1.id)
        if found:
            print(f"✅ Encontrada: {found.description}")
            print(f"   Conta: {found.account.name}")
            print(f"   Categoria: {found.category.name}")

        # Buscar todas
        print("\n📋 Listando todas...")
        all_trans = repo.get_all()
        print(f"✅ Total: {len(all_trans)} transações")

        # Buscar por conta
        print("\n🔍 Buscando por conta...")
        by_account = repo.get_by_account(account.id)
        print(f"✅ {len(by_account)} transações na conta {account.name}")

        # Buscar por categoria
        print("\n🔍 Buscando por categoria...")
        by_category = repo.get_by_category(category.id)
        print(f"✅ {len(by_category)} transações na categoria {category.name}")

        # Buscar por período
        print("\n🔍 Buscando por período...")
        start = date.today() - timedelta(days=7)
        end = date.today()
        by_period = repo.get_by_period(start, end)
        print(f"✅ {len(by_period)} transações nos últimos 7 dias")

        # Buscar por status
        print("\n🔍 Buscando por status (COMPLETED)...")
        completed = repo.get_by_status(TransactionStatus.COMPLETED)
        print(f"✅ {len(completed)} transações efetivadas")

        # Buscar com múltiplos filtros
        print("\n🔍 Buscando com search...")
        results = repo.search(search_term="super", type=TransactionType.EXPENSE)
        print(f"✅ {len(results)} transações encontradas")

        # Calcular total por tipo
        print("\n💰 Calculando totais...")
        total_income = repo.get_total_by_type(TransactionType.INCOME)
        total_expense = repo.get_total_by_type(TransactionType.EXPENSE)
        print(f"✅ Total receitas: R$ {total_income}")
        print(f"✅ Total despesas: R$ {total_expense}")

        # Calcular saldo
        print("\n💰 Calculando saldo...")
        balance = repo.get_balance()
        print(f"✅ Saldo: R$ {balance}")

        # Mudar status
        print("\n🔄 Mudando status...")
        updated = repo.change_status(trans3.id, TransactionStatus.COMPLETED)
        print(f"✅ Status atualizado: {updated.status}")

        # Recalcular saldo após mudança de status
        new_balance = repo.get_balance()
        print(f"✅ Novo saldo: R$ {new_balance}")

        # Verificar se categoria tem transações
        print("\n🔍 Verificando se categoria tem transações...")
        has_trans = cat_repo.has_transactions(category.id)
        print(f"✅ Categoria tem transações: {has_trans}")

        # Verificar se conta tem transações
        has_trans = acc_repo.has_transactions(account.id)
        print(f"✅ Conta tem transações: {has_trans}")

    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()


def cleanup() -> None:
    """Limpa os dados de teste."""
    print("\n=== LIMPANDO DADOS DE TESTE ===")

    db = SessionLocal()

    try:
        from backend.app.models import Account, Category, Transaction

        # Deletar na ordem correta (relacionamentos)
        deleted_trans = db.query(Transaction).delete()
        deleted_acc = db.query(Account).delete()
        deleted_cat = db.query(Category).delete()

        db.commit()
        print(f"✅ Removidas {deleted_trans} transações")
        print(f"✅ Removidas {deleted_acc} contas")
        print(f"✅ Removidas {deleted_cat} categorias")

    except Exception as e:
        print(f"❌ Erro ao limpar: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Iniciando testes dos Repositories...")

    # Executar testes
    test_category_repository()
    test_account_repository()
    test_transaction_repository()

    # Perguntar se quer limpar
    print("\n")
    response = input("Deseja limpar os dados de teste? (s/n): ")
    if response.lower() == "s":
        cleanup()

    print("\n✨ Testes concluídos!")
