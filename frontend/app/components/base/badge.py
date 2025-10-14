"""Badge component."""

from typing import Literal

from nicegui import ui

from frontend.app.theme import light_colors

BadgeVariant = Literal["success", "error", "warning", "info", "primary", "secondary"]


def create_badge(
    text: str,
    variant: BadgeVariant = "primary",
    icon: str | None = None,
    outline: bool = False,
) -> ui.badge:
    """
    Cria badge customizado.

    Args:
        text: Texto do badge
        variant: Variante de cor
        icon: Ícone opcional
        outline: Se True, apenas borda colorida

    Returns:
        ui.badge instance

    Example:
        >>> create_badge("Novo", variant="success")
        >>> create_badge("Pendente", variant="warning", icon="schedule")
    """
    badge = ui.badge(text)

    # Cores por variante
    colors = {
        "success": (light_colors.success, "#D1FAE5", light_colors.success_dark),
        "error": (light_colors.error, "#FEE2E2", light_colors.error_dark),
        "warning": (light_colors.warning, "#FEF3C7", light_colors.warning_dark),
        "info": (light_colors.info, "#DBEAFE", light_colors.info_dark),
        "primary": (light_colors.primary, "#DBEAFE", light_colors.primary_dark),
        "secondary": (light_colors.secondary, "#EDE9FE", light_colors.secondary_dark),
    }

    color, bg_color, text_color = colors.get(variant, colors["primary"])

    if outline:
        badge.style(
            f"background-color: transparent; " f"border: 1px solid {color}; " f"color: {text_color}"
        )
    else:
        badge.style(f"background-color: {bg_color}; " f"color: {text_color}")

    badge.style(
        "padding: 0.125rem 0.5rem; "
        "font-size: 0.75rem; "
        "font-weight: 500; "
        "border-radius: 9999px"
    )

    if icon:
        badge.props(f'icon="{icon}"')

    return badge


def create_status_badge(
    status: Literal["pending", "completed", "active", "inactive"],
) -> ui.badge:
    """
    Cria badge de status pré-configurado.

    Args:
        status: Status a exibir

    Returns:
        ui.badge instance

    Example:
        >>> create_status_badge("completed")
    """
    status_config = {
        "pending": ("Pendente", "warning", "schedule"),
        "completed": ("Efetivada", "success", "check_circle"),
        "active": ("Ativo", "success", "check_circle"),
        "inactive": ("Inativo", "error", "cancel"),
    }

    text, variant, icon = status_config.get(status, ("", "primary", None))

    return create_badge(text, variant=variant, icon=icon)


def create_type_badge(
    type: Literal["income", "expense"],
    show_icon: bool = True,
) -> ui.badge:
    """
    Cria badge de tipo (receita/despesa).

    Args:
        type: Tipo (income ou expense)
        show_icon: Se True, mostra ícone

    Returns:
        ui.badge instance

    Example:
        >>> create_type_badge("income")
    """
    if type == "income":
        text = "Receita"
        variant = "success"
        icon = "arrow_upward" if show_icon else None
    else:
        text = "Despesa"
        variant = "error"
        icon = "arrow_downward" if show_icon else None

    return create_badge(text, variant=variant, icon=icon)


def create_count_badge(
    count: int,
    variant: BadgeVariant = "primary",
) -> ui.badge:
    """
    Cria badge de contagem.

    Args:
        count: Número a exibir
        variant: Variante de cor

    Returns:
        ui.badge instance

    Example:
        >>> create_count_badge(5, variant="error")
    """
    badge = create_badge(str(count), variant=variant)
    badge.style("min-width: 1.25rem; text-align: center")

    return badge
