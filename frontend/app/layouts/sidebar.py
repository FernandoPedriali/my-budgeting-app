"""Sidebar component with navigation menu."""

from nicegui import ui


def create_sidebar():
    """Create the application sidebar with navigation menu and dark mode toggle.

    Returns:
        Container with sidebar content
    """
    # 1. Instanciação explícita do objeto de modo escuro para garantir o contexto de sessão.
    # O objeto 'dark_mode_element' é agora o 'owner' válido esperado pelo sistema de binding.
    dark_mode_element = ui.dark_mode()

    with ui.column().classes(
        "w-64 h-screen bg-gray-100 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800"
    ) as sidebar:
        # Header with logo/title
        with ui.row().classes("w-full p-4 items-center gap-3"):
            ui.icon("account_balance_wallet", size="2rem").classes("text-primary")
            ui.label("My Budget").classes("text-xl font-bold text-gray-800 dark:text-gray-100")

        ui.separator().classes("mb-4")

        # Navigation menu
        with ui.column().classes("flex-1 gap-1 px-2"):
            create_menu_item(
                icon="dashboard", label="Dashboard", route="/", description="Visão geral"
            )

            create_menu_item(
                icon="receipt_long",
                label="Transações",
                route="/transactions",
                description="Receitas e despesas",
            )

            create_menu_item(
                icon="account_balance",
                label="Contas",
                route="/accounts",
                description="Contas bancárias",
            )

            create_menu_item(
                icon="label", label="Categorias", route="/categories", description="Organização"
            )

        ui.separator().classes("my-4")

        # Dark mode toggle at bottom
        with ui.row().classes("w-full p-4 items-center justify-between"):
            ui.label("Modo Escuro").classes("text-sm text-gray-600 dark:text-gray-400")
            ui.switch(value=dark_mode_element.value).bind_value(dark_mode_element, "value").props(
                "color=primary"
            )

    return sidebar


def create_menu_item(icon: str, label: str, route: str, description: str = ""):
    """Create a menu item for the sidebar.

    Args:
        icon: Material icon name
        label: Menu item label
        route: Navigation route
        description: Optional description tooltip
    """
    with ui.link(target=route).classes("no-underline w-full"):
        with ui.row().classes(
            "w-full p-3 rounded-lg items-center gap-3 "
            "hover:bg-gray-200 dark:hover:bg-gray-800 "
            "transition-colors cursor-pointer"
        ):
            ui.icon(icon, size="1.5rem").classes("text-gray-600 dark:text-gray-400")

            with ui.column().classes("gap-0"):
                ui.label(label).classes("text-sm font-medium text-gray-800 dark:text-gray-100")
                if description:
                    ui.label(description).classes("text-xs text-gray-500 dark:text-gray-500")
