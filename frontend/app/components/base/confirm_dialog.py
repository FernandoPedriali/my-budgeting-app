"""Advanced confirm dialog component."""

from typing import Callable, Literal

from nicegui import ui

from frontend.app.components.base.button import create_button

DialogType = Literal["info", "warning", "error", "success"]


class ConfirmDialog:
    """
    Dialog de confirmação avançado com ícones e variantes.

    Example:
        ```python
        dialog = ConfirmDialog(
            title="Deletar Categoria",
            message="Esta ação não pode ser desfeita. Tem certeza?",
            type="error",
            on_confirm=delete_handler
        )
        dialog.open()
        ```
    """

    def __init__(
        self,
        title: str,
        message: str,
        type: DialogType = "warning",
        on_confirm: Callable | None = None,
        on_cancel: Callable | None = None,
        confirm_text: str = "Confirmar",
        cancel_text: str = "Cancelar",
        show_checkbox: bool = False,
        checkbox_label: str = "Não perguntar novamente",
    ) -> None:
        """
        Inicializa o ConfirmDialog.

        Args:
            title: Título do dialog
            message: Mensagem a exibir
            type: Tipo do dialog (info, warning, error, success)
            on_confirm: Callback ao confirmar
            on_cancel: Callback ao cancelar
            confirm_text: Texto do botão confirmar
            cancel_text: Texto do botão cancelar
            show_checkbox: Se True, mostra checkbox de confirmação
            checkbox_label: Label do checkbox
        """
        self.title = title
        self.message = message
        self.type = type
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.confirm_text = confirm_text
        self.cancel_text = cancel_text
        self.show_checkbox = show_checkbox
        self.checkbox_label = checkbox_label
        self.checkbox_value = False

        # Configurações por tipo
        self.configs = {
            "info": {
                "icon": "info",
                "icon_color": "#3B82F6",
                "confirm_variant": "primary",
            },
            "warning": {
                "icon": "warning",
                "icon_color": "#F59E0B",
                "confirm_variant": "warning",
            },
            "error": {
                "icon": "error",
                "icon_color": "#EF4444",
                "confirm_variant": "error",
            },
            "success": {
                "icon": "check_circle",
                "icon_color": "#10B981",
                "confirm_variant": "success",
            },
        }

        self.dialog = None

    def open(self) -> None:
        """Abre o dialog."""
        config = self.configs.get(self.type, self.configs["warning"])

        self.dialog = ui.dialog().props("persistent")

        with self.dialog:
            with ui.card().classes("w-full").style("max-width: 480px"):
                # Header com ícone e título
                with ui.row().classes("w-full items-center gap-4 mb-4"):
                    ui.icon(config["icon"]).classes("text-5xl").style(
                        f"color: {config['icon_color']}"
                    )
                    ui.label(self.title).classes("text-xl font-semibold")

                # Mensagem
                ui.label(self.message).classes("text-base text-gray-700 mb-4")

                # Checkbox opcional
                if self.show_checkbox:
                    self.checkbox = ui.checkbox(self.checkbox_label).classes("mb-4")
                    self.checkbox.on(
                        "update:model-value", lambda e: setattr(self, "checkbox_value", e.args)
                    )

                # Separator
                ui.separator().classes("my-4")

                # Botões
                with ui.row().classes("w-full justify-end gap-2"):
                    create_button(
                        self.cancel_text,
                        on_click=self._handle_cancel,
                        variant="secondary",
                    )
                    create_button(
                        self.confirm_text,
                        on_click=self._handle_confirm,
                        variant=config["confirm_variant"],
                    )

        self.dialog.open()

    def close(self) -> None:
        """Fecha o dialog."""
        if self.dialog:
            self.dialog.close()

    def _handle_confirm(self) -> None:
        """Handler para confirmação."""
        if self.on_confirm:
            if self.show_checkbox:
                self.on_confirm(self.checkbox_value)
            else:
                self.on_confirm()
        self.close()

    def _handle_cancel(self) -> None:
        """Handler para cancelamento."""
        if self.on_cancel:
            self.on_cancel()
        self.close()


def show_confirm_dialog(
    title: str,
    message: str,
    type: DialogType = "warning",
    on_confirm: Callable | None = None,
    on_cancel: Callable | None = None,
    confirm_text: str = "Confirmar",
    cancel_text: str = "Cancelar",
) -> ConfirmDialog:
    """
    Mostra dialog de confirmação.

    Args:
        title: Título
        message: Mensagem
        type: Tipo do dialog
        on_confirm: Callback confirmar
        on_cancel: Callback cancelar
        confirm_text: Texto botão confirmar
        cancel_text: Texto botão cancelar

    Returns:
        ConfirmDialog instance

    Example:
        >>> show_confirm_dialog(
        ...     "Deletar Item",
        ...     "Tem certeza que deseja deletar este item?",
        ...     type="error",
        ...     on_confirm=delete_item
        ... )
    """
    dialog = ConfirmDialog(
        title=title,
        message=message,
        type=type,
        on_confirm=on_confirm,
        on_cancel=on_cancel,
        confirm_text=confirm_text,
        cancel_text=cancel_text,
    )
    dialog.open()
    return dialog


def show_delete_confirm(
    item_name: str,
    on_confirm: Callable,
) -> ConfirmDialog:
    """
    Atalho para dialog de confirmação de exclusão.

    Args:
        item_name: Nome do item a deletar
        on_confirm: Callback ao confirmar

    Returns:
        ConfirmDialog instance

    Example:
        >>> show_delete_confirm("Categoria Alimentação", on_confirm=delete_category)
    """
    return show_confirm_dialog(
        title="Confirmar Exclusão",
        message=f"Tem certeza que deseja deletar '{item_name}'? Esta ação não pode ser desfeita.",
        type="error",
        on_confirm=on_confirm,
        confirm_text="Deletar",
        cancel_text="Cancelar",
    )
