"""Button components."""

from typing import Callable, Literal

from nicegui import ui

from frontend.app.theme import light_colors

ButtonVariant = Literal["primary", "secondary", "success", "warning", "error", "ghost"]
ButtonSize = Literal["sm", "md", "lg"]


def create_button(
    text: str,
    on_click: Callable | None = None,
    variant: ButtonVariant = "primary",
    size: ButtonSize = "md",
    icon: str | None = None,
    icon_right: bool = False,
    full_width: bool = False,
    disabled: bool = False,
) -> ui.button:
    """
    Cria botão customizado com design system.

    Args:
        text: Texto do botão
        on_click: Callback ao clicar
        variant: Estilo do botão (primary, secondary, success, error, ghost)
        size: Tamanho (sm, md, lg)
        icon: Nome do ícone (Quasar icons)
        icon_right: Se True, ícone à direita
        full_width: Se True, ocupa 100% da largura
        disabled: Se True, botão desabilitado

    Returns:
        ui.button instance

    Examples:
        >>> create_button("Salvar", on_click=save_handler, variant="success")
        >>> create_button("Deletar", variant="error", icon="delete")
    """
    # Configurar cores por variante
    colors = {
        "primary": light_colors.primary,
        "secondary": light_colors.secondary,
        "success": light_colors.success,
        "warning": light_colors.warning,
        "error": light_colors.error,
        "ghost": "transparent",
    }

    # Configurar tamanhos
    sizes = {
        "sm": "height: 2rem; font-size: 0.75rem; padding: 0 1rem",
        "md": "height: 2.5rem; font-size: 0.875rem; padding: 0 1.5rem",
        "lg": "height: 3rem; font-size: 1rem; padding: 0 2rem",
    }

    # Criar botão
    button = ui.button(
        text,
        on_click=on_click,
        icon=icon if not icon_right else None,
        icon_right=icon if icon_right else None,
    )

    # Aplicar estilos
    bg_color = colors.get(variant, colors["primary"])

    if variant == "ghost":
        button.props("flat")
        button.style(f"color: {light_colors.text_primary}")
    else:
        button.style(f"background-color: {bg_color}; color: white")

    button.style(sizes[size])
    button.style("border-radius: 0.375rem; font-weight: 600; transition: all 0.2s ease")

    if full_width:
        button.classes("w-full")

    if disabled:
        button.props("disable")

    # Adicionar classes do Quasar
    button.classes("no-wrap")

    return button


def create_icon_button(
    icon: str,
    on_click: Callable | None = None,
    variant: ButtonVariant = "ghost",
    size: ButtonSize = "md",
    tooltip: str | None = None,
    disabled: bool = False,
) -> ui.button:
    """
    Cria botão apenas com ícone.

    Args:
        icon: Nome do ícone
        on_click: Callback ao clicar
        variant: Estilo do botão
        size: Tamanho
        tooltip: Texto do tooltip
        disabled: Se True, botão desabilitado

    Returns:
        ui.button instance

    Example:
        >>> create_icon_button("edit", on_click=edit_handler, tooltip="Editar")
    """
    button = ui.button(icon=icon, on_click=on_click)
    button.props("flat round")

    # Tamanhos para ícone
    icon_sizes = {
        "sm": "1.5rem",
        "md": "2rem",
        "lg": "2.5rem",
    }

    button.style(f"width: {icon_sizes[size]}; height: {icon_sizes[size]}")

    # Cores
    if variant != "ghost":
        colors = {
            "primary": light_colors.primary,
            "secondary": light_colors.secondary,
            "success": light_colors.success,
            "warning": light_colors.warning,
            "error": light_colors.error,
        }
        button.style(f"color: {colors.get(variant, light_colors.primary)}")

    if disabled:
        button.props("disable")

    if tooltip:
        button.tooltip(tooltip)

    return button


def create_button_group(*buttons: ui.button) -> ui.row:
    """
    Agrupa botões lado a lado.

    Args:
        *buttons: Botões a agrupar

    Returns:
        ui.row com botões

    Example:
        >>> btn1 = create_button("Cancelar", variant="secondary")
        >>> btn2 = create_button("Salvar", variant="primary")
        >>> create_button_group(btn1, btn2)
    """
    row = ui.row().classes("gap-2")
    with row:
        for button in buttons:
            pass  # Botões já foram criados
    return row
