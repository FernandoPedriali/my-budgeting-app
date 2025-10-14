"""Card component."""

from typing import Any, Callable

from nicegui import ui

from frontend.app.theme import light_colors, spacing


class Card:
    """
    Componente Card customizado.

    Wrapper para ui.card com estilos do design system.

    Example:
        ```python
        with Card(title="Meu Card"):
            ui.label("Conteúdo do card")
        ```
    """

    def __init__(
        self,
        title: str | None = None,
        subtitle: str | None = None,
        hoverable: bool = False,
        clickable: bool = False,
        on_click: Callable | None = None,
    ) -> None:
        """
        Inicializa o Card.

        Args:
            title: Título do card (opcional)
            subtitle: Subtítulo do card (opcional)
            hoverable: Se True, adiciona efeito hover
            clickable: Se True, adiciona cursor pointer
            on_click: Callback ao clicar (se clickable)
        """
        self.title = title
        self.subtitle = subtitle
        self.hoverable = hoverable
        self.clickable = clickable
        self.on_click = on_click

        # Container principal
        self.container = ui.card().classes("w-full")

        # Aplicar estilos
        self._apply_styles()

        # Adicionar header se tiver título
        if self.title:
            self._add_header()

    def _apply_styles(self) -> None:
        """Aplica estilos do design system."""
        styles = [
            f"background-color: {light_colors.bg_primary}",
            f"border: 1px solid {light_colors.border}",
            f"border-radius: {spacing.md}",
            f"padding: {spacing.lg}",
            "box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05)",
        ]

        if self.hoverable:
            styles.append("transition: box-shadow 0.2s ease")
            self.container.classes("hover:shadow-md")

        if self.clickable:
            styles.append("cursor: pointer")
            if self.on_click:
                self.container.on("click", self.on_click)

        self.container.style(" ".join(styles))

    def _add_header(self) -> None:
        """Adiciona header com título."""
        with self.container:
            with ui.row().classes("w-full items-center mb-4"):
                with ui.column().classes("flex-grow"):
                    ui.label(self.title).classes("text-lg font-semibold")
                    if self.subtitle:
                        ui.label(self.subtitle).classes("text-sm text-gray-500")

    def __enter__(self) -> "Card":
        """Context manager enter."""
        self.container.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.container.__exit__(*args)


def create_card(
    title: str | None = None,
    subtitle: str | None = None,
    hoverable: bool = False,
    clickable: bool = False,
    on_click: Callable | None = None,
) -> Card:
    """
    Função helper para criar card.

    Args:
        title: Título do card
        subtitle: Subtítulo do card
        hoverable: Adiciona hover effect
        clickable: Adiciona click effect
        on_click: Callback ao clicar

    Returns:
        Instância do Card

    Example:
        ```python
        with create_card(title="Meu Card", hoverable=True):
            ui.label("Conteúdo")
        ```
    """
    return Card(
        title=title,
        subtitle=subtitle,
        hoverable=hoverable,
        clickable=clickable,
        on_click=on_click,
    )
