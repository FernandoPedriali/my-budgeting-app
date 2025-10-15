"""Alert component."""

from typing import Literal, Optional

from nicegui import ui

from frontend.app.theme import light_colors

AlertType = Literal["success", "error", "warning", "info"]


def create_alert(
    message: str,
    type: AlertType = "info",
    title: str | None = None,
    dismissible: bool = True,
    icon: str | None = None,
) -> ui.element:
    """
    Cria alert (banner de notificação).

    Args:
        message: Mensagem a exibir
        type: Tipo do alert (success, error, warning, info)
        title: Título opcional
        dismissible: Se True, pode fechar o alert
        icon: Ícone customizado (opcional)

    Returns:
        ui.element com alert

    Example:
        >>> create_alert("Operação realizada com sucesso!", type="success")
        >>> create_alert("Atenção!", "Dados não salvos", type="warning")
    """
    # Configurações por tipo
    configs = {
        "success": {
            "bg": "#D1FAE5",
            "border": light_colors.success,
            "text": light_colors.success_dark,
            "icon": icon or "check_circle",
        },
        "error": {
            "bg": "#FEE2E2",
            "border": light_colors.error,
            "text": light_colors.error_dark,
            "icon": icon or "error",
        },
        "warning": {
            "bg": "#FEF3C7",
            "border": light_colors.warning,
            "text": light_colors.warning_dark,
            "icon": icon or "warning",
        },
        "info": {
            "bg": "#DBEAFE",
            "border": light_colors.info,
            "text": light_colors.info_dark,
            "icon": icon or "info",
        },
    }

    config = configs.get(type, configs["info"])

    # Container do alert
    alert = (
        ui.element("div")
        .classes("w-full rounded-lg p-4")
        .style(
            f"background-color: {config['bg']}; "
            f"border-left: 4px solid {config['border']}; "
            f"color: {config['text']}"
        )
    )

    with alert:
        with ui.row().classes("w-full items-start gap-3"):
            # Ícone
            ui.icon(config["icon"]).classes("text-2xl")

            # Conteúdo
            with ui.column().classes("flex-grow"):
                if title:
                    ui.label(title).classes("font-semibold text-base")
                ui.label(message).classes("text-sm")

            # Botão fechar
            if dismissible:
                ui.button(icon="close", on_click=lambda: alert.delete()).props(
                    "flat dense round"
                ).style(f"color: {config['text']}")

    return alert


def create_banner_alert(
    message: str,
    type: AlertType = "info",
    action_text: str | None = None,
    on_action: Optional[callable] = None,
) -> ui.element:
    """
    Cria banner alert (estilo notificação no topo).

    Args:
        message: Mensagem a exibir
        type: Tipo do alert
        action_text: Texto do botão de ação (opcional)
        on_action: Callback do botão (opcional)

    Returns:
        ui.element com banner

    Example:
        >>> create_banner_alert(
        ...     "Nova versão disponível!",
        ...     type="info",
        ...     action_text="Atualizar",
        ...     on_action=update_app
        ... )
    """
    configs = {
        "success": light_colors.success,
        "error": light_colors.error,
        "warning": light_colors.warning,
        "info": light_colors.info,
    }

    color = configs.get(type, configs["info"])

    banner = (
        ui.element("div").classes("w-full p-3").style(f"background-color: {color}; color: white")
    )

    with banner:
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(message).classes("font-medium")

            if action_text and on_action:
                ui.button(action_text, on_click=on_action).props("flat").style("color: white")

            ui.button(icon="close", on_click=lambda: banner.delete()).props(
                "flat dense round"
            ).style("color: white")

    return banner


def create_inline_alert(
    message: str,
    type: AlertType = "info",
) -> ui.row:
    """
    Cria alert inline compacto (para formulários).

    Args:
        message: Mensagem a exibir
        type: Tipo do alert

    Returns:
        ui.row com alert

    Example:
        >>> create_inline_alert("Campo obrigatório", type="error")
    """
    configs = {
        "success": (light_colors.success, "check_circle"),
        "error": (light_colors.error, "error"),
        "warning": (light_colors.warning, "warning"),
        "info": (light_colors.info, "info"),
    }

    color, icon = configs.get(type, configs["info"])

    row = ui.row().classes("items-center gap-2 p-2 rounded").style(f"color: {color}")

    with row:
        ui.icon(icon).classes("text-lg")
        ui.label(message).classes("text-sm")

    return row
