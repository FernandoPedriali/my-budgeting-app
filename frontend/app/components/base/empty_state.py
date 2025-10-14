"""Empty state component."""

from typing import Callable

from nicegui import ui

from frontend.app.components.base.button import create_button


def create_empty_state(
    title: str,
    description: str | None = None,
    icon: str = "inbox",
    action_text: str | None = None,
    on_action: Callable | None = None,
) -> ui.column:
    """
    Cria empty state (quando não há dados).

    Args:
        title: Título principal
        description: Descrição opcional
        icon: Ícone a exibir
        action_text: Texto do botão de ação (opcional)
        on_action: Callback do botão (opcional)

    Returns:
        ui.column com empty state

    Example:
        >>> create_empty_state(
        ...     "Nenhuma categoria encontrada",
        ...     "Crie sua primeira categoria para começar",
        ...     icon="label",
        ...     action_text="Nova Categoria",
        ...     on_action=create_category
        ... )
    """
    container = ui.column().classes("w-full items-center justify-center py-16 px-4")

    with container:
        # Ícone grande
        ui.icon(icon).classes("text-6xl text-gray-300 mb-4")

        # Título
        ui.label(title).classes("text-xl font-semibold text-gray-700 text-center")

        # Descrição
        if description:
            ui.label(description).classes("text-sm text-gray-500 text-center mt-2 max-w-md")

        # Botão de ação
        if action_text and on_action:
            ui.element("div").classes("mt-6")
            create_button(
                action_text,
                on_click=on_action,
                variant="primary",
                icon="add",
            )

    return container
