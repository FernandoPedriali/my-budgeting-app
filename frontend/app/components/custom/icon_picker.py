"""Icon picker component."""

from typing import Callable

from nicegui import ui

# Ícones comuns organizados por categoria
COMMON_ICONS = {
    "Financeiro": [
        ("attach_money", "Dinheiro"),
        ("account_balance_wallet", "Carteira"),
        ("credit_card", "Cartão"),
        ("account_balance", "Banco"),
        ("savings", "Poupança"),
        ("paid", "Pagamento"),
        ("receipt", "Recibo"),
        ("trending_up", "Crescimento"),
        ("trending_down", "Queda"),
    ],
    "Categorias": [
        ("home", "Casa"),
        ("restaurant", "Restaurante"),
        ("local_grocery_store", "Supermercado"),
        ("local_gas_station", "Combustível"),
        ("directions_car", "Carro"),
        ("school", "Educação"),
        ("medical_services", "Saúde"),
        ("sports_esports", "Lazer"),
        ("checkroom", "Roupas"),
        ("phone_iphone", "Telefone"),
    ],
    "Ações": [
        ("add", "Adicionar"),
        ("edit", "Editar"),
        ("delete", "Deletar"),
        ("save", "Salvar"),
        ("cancel", "Cancelar"),
        ("check", "Confirmar"),
        ("close", "Fechar"),
        ("search", "Buscar"),
        ("filter_list", "Filtrar"),
        ("more_vert", "Mais"),
    ],
    "Geral": [
        ("label", "Tag"),
        ("folder", "Pasta"),
        ("star", "Estrela"),
        ("favorite", "Favorito"),
        ("shopping_cart", "Carrinho"),
        ("local_offer", "Oferta"),
        ("event", "Evento"),
        ("schedule", "Agendado"),
        ("workspace_premium", "Premium"),
    ],
}


class IconPicker:
    """
    Componente de seleção de ícone.

    Exibe grid de ícones organizados por categoria.

    Example:
        ```python
        picker = IconPicker(label="Ícone", value="wallet")
        picker.on_change(lambda icon: print(icon))
        ```
    """

    def __init__(
        self,
        label: str,
        value: str = "label",
        on_change: Callable[[str], None] | None = None,
        categories: dict[str, list[tuple[str, str]]] | None = None,
    ) -> None:
        """
        Inicializa o IconPicker.

        Args:
            label: Label do picker
            value: Ícone inicial
            on_change: Callback ao mudar ícone
            categories: Categorias customizadas (opcional)
        """
        self.label = label
        self._value = value
        self._on_change = on_change
        self.categories = categories or COMMON_ICONS

        # Container principal
        self.container = ui.column().classes("gap-2 w-full")

        with self.container:
            # Label
            ui.label(label).classes("text-sm font-medium")

            # Preview do ícone atual
            with ui.row().classes("items-center gap-3 p-2 border rounded"):
                self.preview_icon = ui.icon(value).classes("text-3xl")
                ui.label(value).classes("text-sm font-mono")
                ui.button("Escolher Ícone", on_click=self._open_dialog).props("flat dense")

        # Dialog de seleção
        self.dialog = None

    def _open_dialog(self) -> None:
        """Abre dialog de seleção de ícone."""
        self.dialog = ui.dialog()

        with self.dialog:
            with ui.card().classes("w-full").style("max-width: 600px; max-height: 500px"):
                # Header
                with ui.row().classes("w-full items-center justify-between mb-4"):
                    ui.label("Escolher Ícone").classes("text-lg font-semibold")
                    ui.button(icon="close", on_click=self.dialog.close).props("flat round dense")

                # Tabs por categoria
                with ui.tabs().classes("w-full") as tabs:
                    for category in self.categories.keys():
                        ui.tab(category)

                # Panels
                with ui.tab_panels(tabs, value=list(self.categories.keys())[0]).classes("w-full"):
                    for category, icons in self.categories.items():
                        with ui.tab_panel(category):
                            self._create_icon_grid(icons)

        self.dialog.open()

    def _create_icon_grid(self, icons: list[tuple[str, str]]) -> None:
        """
        Cria grid de ícones.

        Args:
            icons: Lista de tuplas (icon_name, label)
        """
        with ui.grid(columns=5).classes("gap-2 w-full"):
            for icon_name, icon_label in icons:
                self._create_icon_button(icon_name, icon_label)

    def _create_icon_button(self, icon_name: str, icon_label: str) -> None:
        """
        Cria botão de ícone.

        Args:
            icon_name: Nome do ícone
            icon_label: Label descritivo
        """
        with ui.column().classes(
            "items-center cursor-pointer p-2 rounded hover:bg-gray-100"
        ) as col:
            ui.icon(icon_name).classes("text-3xl text-gray-700")
            ui.label(icon_label).classes("text-xs text-center text-gray-600 mt-1")

            col.on("click", lambda icon=icon_name: self._select_icon(icon))

    def _select_icon(self, icon: str) -> None:
        """
        Seleciona um ícone.

        Args:
            icon: Nome do ícone
        """
        self._value = icon
        self.preview_icon.props(f'name="{icon}"')

        if self._on_change:
            self._on_change(icon)

        if self.dialog:
            self.dialog.close()

    @property
    def value(self) -> str:
        """Retorna ícone atual."""
        return self._value

    @value.setter
    def value(self, icon: str) -> None:
        """Define ícone."""
        self._select_icon(icon)

    def on_change(self, callback: Callable[[str], None]) -> None:
        """Registra callback para mudanças."""
        self._on_change = callback


def create_icon_picker(
    label: str,
    value: str = "label",
    on_change: Callable[[str], None] | None = None,
) -> IconPicker:
    """
    Função helper para criar IconPicker.

    Args:
        label: Label do picker
        value: Ícone inicial
        on_change: Callback ao mudar

    Returns:
        IconPicker instance

    Example:
        >>> picker = create_icon_picker("Ícone da Categoria", value="restaurant")
    """
    return IconPicker(
        label=label,
        value=value,
        on_change=on_change,
    )
