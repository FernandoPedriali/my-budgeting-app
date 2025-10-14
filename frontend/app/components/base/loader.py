"""Loader components."""

from typing import Literal

from nicegui import ui

from frontend.app.theme import light_colors

LoaderSize = Literal["sm", "md", "lg", "xl"]


def create_spinner(
    size: LoaderSize = "md",
    color: str | None = None,
) -> ui.spinner:
    """
    Cria spinner de loading.

    Args:
        size: Tamanho do spinner
        color: Cor customizada (opcional)

    Returns:
        ui.spinner instance

    Example:
        >>> create_spinner(size="lg")
    """
    sizes = {
        "sm": "1rem",
        "md": "2rem",
        "lg": "3rem",
        "xl": "4rem",
    }

    spinner = ui.spinner(
        size=sizes[size],
        color=color or light_colors.primary,
    )

    return spinner


def create_loading_overlay(
    message: str = "Carregando...",
    size: LoaderSize = "lg",
) -> ui.element:
    """
    Cria overlay de loading para tela inteira.

    Args:
        message: Mensagem a exibir
        size: Tamanho do spinner

    Returns:
        ui.element container

    Example:
        >>> overlay = create_loading_overlay("Salvando dados...")
        >>> # Para remover: overlay.delete()
    """
    overlay = (
        ui.element("div")
        .classes("fixed inset-0 flex items-center justify-center z-50")
        .style("background-color: rgba(0, 0, 0, 0.5); backdrop-filter: blur(2px)")
    )

    with overlay:
        with ui.card().classes("items-center p-6"):
            create_spinner(size=size)
            ui.label(message).classes("text-lg mt-4")

    return overlay


def create_inline_loader(
    message: str = "Carregando...",
    size: LoaderSize = "sm",
) -> ui.row:
    """
    Cria loader inline (para usar dentro de componentes).

    Args:
        message: Mensagem a exibir
        size: Tamanho do spinner

    Returns:
        ui.row com spinner e mensagem

    Example:
        >>> with ui.column():
        ...     create_inline_loader("Buscando dados...")
    """
    row = ui.row().classes("items-center gap-2")

    with row:
        create_spinner(size=size)
        ui.label(message).classes("text-sm text-gray-600")

    return row


def create_skeleton_loader(
    lines: int = 3,
    avatar: bool = False,
) -> ui.column:
    """
    Cria skeleton loader (placeholder animado).

    Args:
        lines: Número de linhas
        avatar: Se True, adiciona avatar circular

    Returns:
        ui.column com skeleton

    Example:
        >>> create_skeleton_loader(lines=4, avatar=True)
    """
    container = ui.column().classes("w-full gap-2")

    with container:
        if avatar:
            ui.element("div").classes("w-12 h-12 rounded-full bg-gray-200 animate-pulse")

        for i in range(lines):
            # Variar largura das linhas
            width = "100%" if i < lines - 1 else "60%"
            ui.element("div").style(
                f"width: {width}; height: 1rem; background-color: #E5E7EB; "
                "border-radius: 0.25rem; animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite"
            )

    return container


class LoadingContext:
    """
    Context manager para loading state.

    Example:
        ```python
        async def load_data():
            with LoadingContext("Carregando dados..."):
                await fetch_data()
        ```
    """

    def __init__(self, message: str = "Carregando..."):
        """
        Inicializa o context.

        Args:
            message: Mensagem de loading
        """
        self.message = message
        self.overlay = None

    def __enter__(self) -> "LoadingContext":
        """Mostra overlay de loading."""
        self.overlay = create_loading_overlay(self.message)
        return self

    def __exit__(self, *args) -> None:
        """Remove overlay de loading."""
        if self.overlay:
            self.overlay.delete()
