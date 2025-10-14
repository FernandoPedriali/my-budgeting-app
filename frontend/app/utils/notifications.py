"""Notification utilities using NiceGUI."""

from typing import Literal

from nicegui import ui

NotificationType = Literal["positive", "negative", "warning", "info"]


def notify_success(message: str, timeout: int = 3000) -> None:
    """
    Mostra notificação de sucesso.

    Args:
        message: Mensagem a exibir
        timeout: Tempo em ms (0 = não fecha automaticamente)

    Example:
        >>> notify_success("Categoria criada com sucesso!")
    """
    ui.notify(
        message,
        type="positive",
        position="top",
        timeout=timeout,
        close_button=True,
    )


def notify_error(message: str, timeout: int = 5000) -> None:
    """
    Mostra notificação de erro.

    Args:
        message: Mensagem a exibir
        timeout: Tempo em ms

    Example:
        >>> notify_error("Erro ao salvar categoria")
    """
    ui.notify(
        message,
        type="negative",
        position="top",
        timeout=timeout,
        close_button=True,
    )


def notify_warning(message: str, timeout: int = 4000) -> None:
    """
    Mostra notificação de aviso.

    Args:
        message: Mensagem a exibir
        timeout: Tempo em ms

    Example:
        >>> notify_warning("Categoria será deletada")
    """
    ui.notify(
        message,
        type="warning",
        position="top",
        timeout=timeout,
        close_button=True,
    )


def notify_info(message: str, timeout: int = 3000) -> None:
    """
    Mostra notificação informativa.

    Args:
        message: Mensagem a exibir
        timeout: Tempo em ms

    Example:
        >>> notify_info("Carregando dados...")
    """
    ui.notify(
        message,
        type="info",
        position="top",
        timeout=timeout,
        close_button=True,
    )


def notify(
    message: str,
    type: NotificationType = "info",
    timeout: int = 3000,
    position: str = "top",
) -> None:
    """
    Mostra notificação customizada.

    Args:
        message: Mensagem a exibir
        type: Tipo da notificação
        timeout: Tempo em ms
        position: Posição (top, bottom, left, right, center)

    Example:
        >>> notify("Operação realizada", type="positive")
    """
    ui.notify(
        message,
        type=type,
        position=position,
        timeout=timeout,
        close_button=True,
    )
