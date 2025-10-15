"""Accounts page - Manage bank accounts and wallets."""

from nicegui import ui

from frontend.app.layouts.base_layout import create_base_layout


@ui.page("/accounts")
def accounts_page():
    """Accounts page for managing bank accounts, credit cards, cash, etc.

    Features (to be implemented in Phase K):
    - List all accounts in cards
    - Show current balance for each account
    - Filter by account type
    - Search by name
    - Create/edit/delete accounts
    - Activate/deactivate accounts
    - Show total balance summary
    """

    def build_content():
        with ui.column().classes("gap-6 w-full"):
            # Placeholder notice
            with ui.card().classes("p-8 text-center"):
                ui.icon("account_balance", size="4rem").classes("text-primary mb-4")
                ui.label("Página de Contas").classes(
                    "text-xl font-bold text-gray-800 dark:text-gray-100 mb-2"
                )
                ui.label("Esta página será implementada na Fase K da Sprint 1").classes(
                    "text-gray-600 dark:text-gray-400 mb-4"
                )

                with ui.column().classes("gap-2 items-start text-left mt-4"):
                    ui.label("Funcionalidades planejadas:").classes(
                        "font-medium text-gray-700 dark:text-gray-300"
                    )
                    for feature in [
                        "💳 Listagem de contas em cards",
                        "💰 Exibição do saldo atual de cada conta",
                        "🔍 Filtros por tipo de conta",
                        "🔎 Busca por nome",
                        "➕ Criar novas contas",
                        "✏️ Editar e excluir contas",
                        "🔄 Ativar/desativar contas",
                        "📊 Resumo do saldo total",
                    ]:
                        with ui.row().classes("gap-2 items-center"):
                            ui.label(feature).classes("text-sm text-gray-600 dark:text-gray-400")

    create_base_layout(
        title="Contas", breadcrumb=["Dashboard", "Contas"], content_builder=build_content
    )
