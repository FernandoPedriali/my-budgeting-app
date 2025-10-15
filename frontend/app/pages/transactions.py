"""Transactions page - Manage income and expenses."""

from nicegui import ui

from frontend.app.layouts.base_layout import create_base_layout


@ui.page("/transactions")
def transactions_page():
    """Transactions page for managing income and expenses.

    Features (to be implemented in Phase L):
    - List all transactions
    - Filter by period, account, category, type, status
    - Search by description
    - Create/edit/delete transactions
    - Change status (pending/completed)
    - Show period summary
    """

    def build_content():
        with ui.column().classes("gap-6 w-full"):
            # Placeholder notice
            with ui.card().classes("p-8 text-center"):
                ui.icon("receipt_long", size="4rem").classes("text-primary mb-4")
                ui.label("Página de Transações").classes(
                    "text-xl font-bold text-gray-800 dark:text-gray-100 mb-2"
                )
                ui.label("Esta página será implementada na Fase L da Sprint 1").classes(
                    "text-gray-600 dark:text-gray-400 mb-4"
                )

                with ui.column().classes("gap-2 items-start text-left mt-4"):
                    ui.label("Funcionalidades planejadas:").classes(
                        "font-medium text-gray-700 dark:text-gray-300"
                    )
                    for feature in [
                        "📋 Listagem de transações em tabela",
                        "🔍 Filtros avançados (período, conta, categoria, tipo, status)",
                        "🔎 Busca por descrição",
                        "➕ Criar novas transações",
                        "✏️ Editar e excluir transações",
                        "✅ Alterar status (pendente ↔ efetivada)",
                        "💰 Resumo financeiro do período",
                    ]:
                        with ui.row().classes("gap-2 items-center"):
                            ui.label(feature).classes("text-sm text-gray-600 dark:text-gray-400")

    create_base_layout(
        title="Transações", breadcrumb=["Dashboard", "Transações"], content_builder=build_content
    )
