"""Data table component."""

from typing import Any, Callable

from nicegui import ui


class DataTable:
    """
    Componente de tabela de dados com paginação e ordenação.

    Wrapper para ui.table com funcionalidades extras.

    Example:
        ```python
        columns = [
            {'name': 'name', 'label': 'Nome', 'field': 'name', 'align': 'left'},
            {'name': 'value', 'label': 'Valor', 'field': 'value', 'align': 'right'},
        ]

        rows = [
            {'name': 'Item 1', 'value': 100},
            {'name': 'Item 2', 'value': 200},
        ]

        table = DataTable(columns=columns, rows=rows)
        ```
    """

    def __init__(
        self,
        columns: list[dict[str, Any]],
        rows: list[dict[str, Any]],
        row_key: str = "id",
        pagination: int | None = 10,
        selection: str | None = None,
        on_row_click: Callable[[dict], None] | None = None,
    ) -> None:
        """
        Inicializa o DataTable.

        Args:
            columns: Definição das colunas
            rows: Dados das linhas
            row_key: Campo usado como chave única
            pagination: Linhas por página (None = sem paginação)
            selection: Tipo de seleção ('single', 'multiple', None)
            on_row_click: Callback ao clicar em linha
        """
        self.columns = columns
        self.rows = rows
        self.row_key = row_key
        self.pagination_size = pagination
        self.selection = selection
        self.on_row_click = on_row_click

        # Criar tabela
        self.table = ui.table(
            columns=columns,
            rows=rows,
            row_key=row_key,
        )

        self.table.classes("w-full")

        # Configurar paginação
        if pagination:
            self.table.props(
                f'rows-per-page-options="[{pagination}, {pagination*2}, {pagination*5}]"'
            )
            self.table.props(f':pagination="{{rowsPerPage: {pagination}}}"')

        # Configurar seleção
        if selection:
            self.table.props(f'selection="{selection}"')

        # Configurar evento de clique
        if on_row_click:
            self.table.on("row-click", lambda e: on_row_click(e.args[1]))

        # Adicionar estilos
        self._apply_styles()

    def _apply_styles(self) -> None:
        """Aplica estilos customizados."""
        self.table.props("flat bordered")
        self.table.classes("rounded-lg")

    def update_rows(self, new_rows: list[dict[str, Any]]) -> None:
        """
        Atualiza os dados da tabela.

        Args:
            new_rows: Novos dados
        """
        self.rows = new_rows
        self.table.update()

    def add_row(self, row: dict[str, Any]) -> None:
        """
        Adiciona uma linha.

        Args:
            row: Dados da linha
        """
        self.rows.append(row)
        self.table.update()

    def remove_row(self, row_key_value: Any) -> None:
        """
        Remove uma linha pelo valor da chave.

        Args:
            row_key_value: Valor da chave da linha
        """
        self.rows = [row for row in self.rows if row.get(self.row_key) != row_key_value]
        self.table.update()

    def get_selected_rows(self) -> list[dict[str, Any]]:
        """
        Retorna linhas selecionadas.

        Returns:
            Lista de linhas selecionadas
        """
        if not self.selection:
            return []

        # Acessar seleção via props do Quasar
        return self.table.props.get("selected", [])


def create_data_table(
    columns: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    row_key: str = "id",
    pagination: int | None = 10,
    selection: str | None = None,
    on_row_click: Callable[[dict], None] | None = None,
) -> DataTable:
    """
    Função helper para criar DataTable.

    Args:
        columns: Definição das colunas
        rows: Dados das linhas
        row_key: Campo chave única
        pagination: Linhas por página
        selection: Tipo de seleção
        on_row_click: Callback ao clicar

    Returns:
        DataTable instance

    Example:
        ```python
        columns = [
            {'name': 'id', 'label': 'ID', 'field': 'id'},
            {'name': 'name', 'label': 'Nome', 'field': 'name', 'sortable': True},
            {'name': 'amount', 'label': 'Valor', 'field': 'amount', 'sortable': True},
        ]

        rows = [
            {'id': 1, 'name': 'Transação 1', 'amount': 100},
            {'id': 2, 'name': 'Transação 2', 'amount': 200},
        ]

        table = create_data_table(
            columns=columns,
            rows=rows,
            on_row_click=lambda row: print(row)
        )
        ```
    """
    return DataTable(
        columns=columns,
        rows=rows,
        row_key=row_key,
        pagination=pagination,
        selection=selection,
        on_row_click=on_row_click,
    )


def create_simple_table(
    headers: list[str],
    rows: list[list[Any]],
) -> ui.table:
    """
    Cria tabela simples sem funcionalidades extras.

    Args:
        headers: Lista de cabeçalhos
        rows: Lista de listas com dados

    Returns:
        ui.table instance

    Example:
        >>> table = create_simple_table(
        ...     headers=['Nome', 'Valor', 'Data'],
        ...     rows=[
        ...         ['Item 1', 'R$ 100', '13/10/2025'],
        ...         ['Item 2', 'R$ 200', '14/10/2025'],
        ...     ]
        ... )
    """
    # Converter para formato do Quasar
    columns = [
        {
            "name": f"col{i}",
            "label": header,
            "field": f"col{i}",
            "align": "left",
        }
        for i, header in enumerate(headers)
    ]

    table_rows = [{f"col{i}": cell for i, cell in enumerate(row)} for row in rows]

    table = ui.table(columns=columns, rows=table_rows)
    table.classes("w-full")
    table.props("flat bordered")

    return table
