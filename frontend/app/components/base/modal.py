"""Modal component."""

from typing import Any, Callable

from nicegui import ui

from frontend.app.components.base.button import create_button


class Modal:
    """
    Componente Modal customizado.

    Wrapper para ui.dialog com estilos do design system.

    Example:
        ```python
        with Modal(title="Confirmar") as modal:
            ui.label("Tem certeza?")
            with ui.row():
                create_button("Cancelar", on_click=modal.close)
                create_button("Confirmar", on_click=confirm_handler)

        modal.open()
        ```
    """

    def __init__(
        self,
        title: str | None = None,
        persistent: bool = False,
        maximized: bool = False,
    ) -> None:
        """
        Inicializa o Modal.

        Args:
            title: Título do modal
            persistent: Se True, não fecha ao clicar fora
            maximized: Se True, modal ocupa tela toda
        """
        self.title = title
        self.persistent = persistent
        self.maximized = maximized

        # Criar dialog
        self.dialog = ui.dialog()

        if persistent:
            self.dialog.props("persistent")

        if maximized:
            self.dialog.props("maximized")

        # Card dentro do dialog
        with self.dialog:
            self.card = ui.card().classes("w-full")
            self.card.style("max-width: 640px; min-width: 400px")

            with self.card:
                # Header com título
                if self.title:
                    with ui.row().classes("w-full items-center justify-between mb-4"):
                        ui.label(self.title).classes("text-xl font-semibold")
                        ui.button(icon="close", on_click=self.close).props("flat round dense")

                # Container para conteúdo
                self.content_container = ui.column().classes("w-full gap-4")

    def open(self) -> None:
        """Abre o modal."""
        self.dialog.open()

    def close(self) -> None:
        """Fecha o modal."""
        self.dialog.close()

    def __enter__(self) -> "Modal":
        """Context manager enter."""
        self.content_container.__enter__()
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit."""
        self.content_container.__exit__(*args)


def create_confirm_dialog(
    title: str,
    message: str,
    on_confirm: Callable,
    on_cancel: Callable | None = None,
    confirm_text: str = "Confirmar",
    cancel_text: str = "Cancelar",
    confirm_variant: str = "primary",
) -> Modal:
    """
    Cria modal de confirmação.

    Args:
        title: Título do modal
        message: Mensagem a exibir
        on_confirm: Callback ao confirmar
        on_cancel: Callback ao cancelar (opcional)
        confirm_text: Texto do botão confirmar
        cancel_text: Texto do botão cancelar
        confirm_variant: Variante do botão confirmar

    Returns:
        Modal instance

    Example:
        >>> modal = create_confirm_dialog(
        ...     "Deletar categoria",
        ...     "Tem certeza que deseja deletar?",
        ...     on_confirm=delete_handler
        ... )
        >>> modal.open()
    """
    modal = Modal(title=title, persistent=True)

    with modal:
        ui.label(message).classes("text-base")

        with ui.row().classes("w-full justify-end gap-2 mt-4"):
            create_button(
                cancel_text,
                on_click=lambda: (on_cancel() if on_cancel else None, modal.close()),
                variant="secondary",
            )
            create_button(
                confirm_text,
                on_click=lambda: (on_confirm(), modal.close()),
                variant=confirm_variant,
            )

    return modal


def create_form_modal(
    title: str,
    on_submit: Callable,
    on_cancel: Callable | None = None,
    submit_text: str = "Salvar",
    cancel_text: str = "Cancelar",
) -> Modal:
    """
    Cria modal para formulário.

    Args:
        title: Título do modal
        on_submit: Callback ao submeter
        on_cancel: Callback ao cancelar
        submit_text: Texto do botão submit
        cancel_text: Texto do botão cancelar

    Returns:
        Modal instance com footer de ações

    Example:
        ```python
        modal = create_form_modal("Nova Categoria", on_submit=save_category)

        with modal:
            create_input("Nome", placeholder="Digite o nome")
            create_select("Tipo", options=["Receita", "Despesa"])

        modal.open()
        ```
    """
    modal = Modal(title=title, persistent=True)

    # Adicionar footer com botões após o conteúdo
    with modal.card:
        ui.separator().classes("my-4")
        with ui.row().classes("w-full justify-end gap-2"):
            create_button(
                cancel_text,
                on_click=lambda: (on_cancel() if on_cancel else None, modal.close()),
                variant="secondary",
            )
            create_button(
                submit_text,
                on_click=lambda: (on_submit(), modal.close()),
                variant="primary",
            )

    return modal


def create_info_modal(
    title: str,
    message: str,
    close_text: str = "Fechar",
) -> Modal:
    """
    Cria modal informativo simples.

    Args:
        title: Título do modal
        message: Mensagem a exibir
        close_text: Texto do botão fechar

    Returns:
        Modal instance

    Example:
        >>> modal = create_info_modal("Informação", "Operação realizada com sucesso!")
        >>> modal.open()
    """
    modal = Modal(title=title)

    with modal:
        ui.label(message).classes("text-base")

        with ui.row().classes("w-full justify-end mt-4"):
            create_button(
                close_text,
                on_click=modal.close,
                variant="primary",
            )

    return modal
