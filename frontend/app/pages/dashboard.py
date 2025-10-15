"""Dashboard page - Overview of finances."""

from nicegui import ui

from frontend.app.layouts.base_layout import create_base_layout


@ui.page("/")
def dashboard_page():
    """Dashboard page with financial overview.

    This will be the main landing page showing:
    - Total balance across all accounts
    - Recent transactions
    - Income vs Expenses charts
    - Quick actions
    """

    def build_content():
        # Placeholder content for now
        with ui.column().classes("gap-6 w-full"):
            # Welcome section
            with ui.card().classes("p-6"):
                ui.label("Bem-vindo ao My Budget! 👋").classes(
                    "text-xl font-bold text-gray-800 dark:text-gray-100"
                )
                ui.label("Seu painel financeiro está sendo construído...").classes(
                    "text-gray-600 dark:text-gray-400"
                )

            # Quick stats (placeholder)
            with ui.row().classes("gap-4 w-full"):
                for title, value, icon, color in [
                    ("Saldo Total", "R$ 0,00", "account_balance_wallet", "primary"),
                    ("Receitas do Mês", "R$ 0,00", "trending_up", "positive"),
                    ("Despesas do Mês", "R$ 0,00", "trending_down", "negative"),
                    ("Transações", "0", "receipt_long", "info"),
                ]:
                    with ui.card().classes(f"flex-1 p-4 bg-{color}-50 dark:bg-{color}-900"):
                        ui.icon(icon, size="2rem").classes(f"text-{color}")
                        ui.label(value).classes(
                            "text-2xl font-bold text-gray-800 dark:text-gray-100 mt-2"
                        )
                        ui.label(title).classes("text-sm text-gray-600 dark:text-gray-400")

            # Coming soon notice
            with ui.card().classes("p-8 text-center"):
                ui.icon("construction", size="4rem").classes("text-gray-400 mb-4")
                ui.label("Dashboard em Construção").classes(
                    "text-xl font-bold text-gray-800 dark:text-gray-100 mb-2"
                )
                ui.label("Em breve você terá acesso a gráficos, relatórios e muito mais!").classes(
                    "text-gray-600 dark:text-gray-400"
                )

    create_base_layout(title="Dashboard", breadcrumb=["Dashboard"], content_builder=build_content)
