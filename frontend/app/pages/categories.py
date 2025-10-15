"""Categories page - Manage income and expense categories."""

from typing import Optional

from nicegui import ui

from frontend.app.components.base.button import create_button, create_icon_button
from frontend.app.components.base.empty_state import create_empty_state
from frontend.app.components.base.loader import create_spinner
from frontend.app.components.base.modal import create_button
from frontend.app.components.custom.color_picker import create_color_picker
from frontend.app.components.custom.icon_picker import create_icon_picker
from frontend.app.layouts.base_layout import create_base_layout
from frontend.app.utils.api_client import api
from frontend.app.utils.notifications import notify_error, notify_success


class CategoriesPageState:
    """State management for categories page."""

    def __init__(self):
        self.categories: list[dict] = []
        self.filtered_categories: list[dict] = []
        self.loading: bool = False
        self.filter_type: Optional[str] = None
        self.search_query: str = ""
        self.selected_category: Optional[dict] = None
        self.modal_open: bool = False
        self.delete_modal_open: bool = False


state = CategoriesPageState()


@ui.page("/categories")
async def categories_page():
    """Categories page for organizing transactions."""

    def build_content():
        with ui.column().classes("gap-6 w-full"):
            # Header with actions
            create_header()

            # Filters
            create_filters()

            # Categories grid
            with ui.column().classes("w-full") as categories_container:
                state.categories_container = categories_container
                ui.timer(0.1, lambda: load_categories(), once=True)

    create_base_layout(
        title="Categorias", breadcrumb=["Dashboard", "Categorias"], content_builder=build_content
    )


def create_header():
    """Create page header with title and actions."""
    with ui.row().classes("w-full justify-between items-center"):
        ui.label("Gerencie suas categorias").classes("text-gray-600 dark:text-gray-400")

        create_button(
            label="Nova Categoria",
            icon="add",
            on_click=lambda: open_category_modal(),
            variant="primary",
        )


def create_filters():
    """Create filter section."""
    with ui.card().classes("w-full p-4"):
        with ui.row().classes("gap-4 w-full items-center"):
            # Type filter
            with ui.row().classes("gap-2 items-center"):
                ui.label("Tipo:").classes("text-sm font-medium text-gray-700 dark:text-gray-300")

                filter_buttons = (
                    ui.toggle(
                        ["Todas", "Receitas", "Despesas"],
                        value="Todas",
                        on_change=lambda e: filter_by_type(e.value),
                    )
                    .props("color=primary")
                    .classes("text-sm")
                )

            # Search
            with ui.row().classes("flex-1 gap-2 items-center"):
                ui.icon("search").classes("text-gray-400")
                search_input = (
                    ui.input(placeholder="Buscar por nome...")
                    .props("dense outlined")
                    .classes("flex-1")
                )
                search_input.on("input", lambda e: filter_by_search(e.value))


def filter_by_type(filter_value: str):
    """Filter categories by type."""
    if filter_value == "Todas":
        state.filter_type = None
    elif filter_value == "Receitas":
        state.filter_type = "income"
    elif filter_value == "Despesas":
        state.filter_type = "expense"

    apply_filters()


def filter_by_search(search_value: str):
    """Filter categories by search query."""
    state.search_query = search_value.lower()
    apply_filters()


def apply_filters():
    """Apply all filters to categories list."""
    state.filtered_categories = state.categories

    # Filter by type
    if state.filter_type:
        state.filtered_categories = [
            cat for cat in state.filtered_categories if cat["type"] == state.filter_type
        ]

    # Filter by search
    if state.search_query:
        state.filtered_categories = [
            cat for cat in state.filtered_categories if state.search_query in cat["name"].lower()
        ]

    render_categories()


async def load_categories():
    """Load categories from API."""
    state.loading = True
    render_categories()

    try:
        response = await api.get_categories(is_active=True)
        state.categories = response.get("items", [])
        state.filtered_categories = state.categories
        render_categories()
    except Exception as e:
        notify_error(f"Erro ao carregar categorias: {str(e)}")
    finally:
        state.loading = False


def render_categories():
    """Render categories grid."""
    state.categories_container.clear()

    with state.categories_container:
        if state.loading:
            create_spinner(size="lg", overlay=False)
        elif not state.filtered_categories:
            if state.search_query or state.filter_type:
                create_empty_state(
                    icon="search_off",
                    title="Nenhuma categoria encontrada",
                    description="Tente ajustar os filtros de busca",
                )
            else:
                create_empty_state(
                    icon="label_off",
                    title="Nenhuma categoria cadastrada",
                    description="Crie sua primeira categoria para começar a organizar suas finanças",
                    action_label="Criar Categoria",
                    action=lambda: open_category_modal(),
                )
        else:
            # Grid of category cards
            with ui.row().classes("gap-4 w-full flex-wrap"):
                for category in state.filtered_categories:
                    create_category_card(category)


def create_category_card(category: dict):
    """Create a category card."""
    type_config = {
        "income": {"label": "Receita", "color": "positive"},
        "expense": {"label": "Despesa", "color": "negative"},
    }

    config = type_config.get(category["type"], {"label": "Outro", "color": "grey"})

    with ui.card().classes("p-4 cursor-pointer hover:shadow-lg transition-shadow w-64"):
        with ui.row().classes("w-full justify-between items-start"):
            # Icon and color
            with ui.row().classes("gap-3 items-center flex-1"):
                with (
                    ui.element("div")
                    .classes(f"p-3 rounded-lg")
                    .style(f"background-color: {category['color']}20")
                ):
                    ui.icon(category["icon"], size="1.5rem").style(f"color: {category['color']}")

                with ui.column().classes("gap-1 flex-1"):
                    ui.label(category["name"]).classes(
                        "text-base font-medium text-gray-800 dark:text-gray-100"
                    )
                    ui.label(config["label"]).classes(f"text-xs text-{config['color']}")

            # Actions menu
            with ui.button(icon="more_vert").props("flat dense round size=sm"):
                with ui.menu():
                    ui.menu_item(
                        "Editar", lambda c=category: open_category_modal(c), auto_close=True
                    ).props("icon=edit")
                    ui.menu_item(
                        "Excluir", lambda c=category: open_delete_modal(c), auto_close=True
                    ).props("icon=delete")

        # Description
        if category.get("description"):
            ui.label(category["description"]).classes(
                "text-sm text-gray-600 dark:text-gray-400 mt-2 line-clamp-2"
            )


def open_category_modal(category: Optional[dict] = None):
    """Open modal for creating/editing category."""
    state.selected_category = category
    is_edit = category is not None

    # Form state
    form_data = {
        "name": category["name"] if is_edit else "",
        "type": category["type"] if is_edit else "expense",
        "description": category.get("description", "") if is_edit else "",
        "color": category["color"] if is_edit else "#EF4444",
        "icon": category["icon"] if is_edit else "label",
    }

    with ui.dialog() as dialog, ui.card().classes("w-full max-w-md"):
        dialog.open()

        # Header
        with ui.row().classes("w-full justify-between items-center mb-4"):
            ui.label("Editar Categoria" if is_edit else "Nova Categoria").classes(
                "text-xl font-bold"
            )
            create_icon_button(icon="close", on_click=dialog.close)

        # Form
        with ui.column().classes("gap-4 w-full"):
            # Name
            name_input = (
                ui.input(label="Nome *", value=form_data["name"])
                .props("outlined")
                .classes("w-full")
            )
            name_input.on("input", lambda e: form_data.update({"name": e.value}))

            # Type
            type_select = (
                ui.select(
                    label="Tipo *",
                    options={"income": "Receita", "expense": "Despesa"},
                    value=form_data["type"],
                )
                .props("outlined")
                .classes("w-full")
            )
            type_select.on("update:model-value", lambda e: form_data.update({"type": e.value}))

            # Description
            desc_input = (
                ui.textarea(label="Descrição", value=form_data["description"])
                .props("outlined")
                .classes("w-full")
            )
            desc_input.on("input", lambda e: form_data.update({"description": e.value}))

            # Color picker
            with ui.column().classes("gap-2 w-full"):
                ui.label("Cor").classes("text-sm font-medium")
                color_value = create_color_picker(
                    value=form_data["color"],
                    on_change=lambda color: form_data.update({"color": color}),
                )

            # Icon picker
            with ui.column().classes("gap-2 w-full"):
                ui.label("Ícone").classes("text-sm font-medium")
                icon_value = create_icon_picker(
                    value=form_data["icon"], on_change=lambda icon: form_data.update({"icon": icon})
                )

        # Actions
        with ui.row().classes("w-full justify-end gap-2 mt-4"):
            create_button(label="Cancelar", on_click=dialog.close, variant="ghost")
            create_button(
                label="Salvar" if is_edit else "Criar",
                on_click=lambda: save_category(form_data, is_edit, dialog),
                variant="primary",
            )


async def save_category(form_data: dict, is_edit: bool, dialog):
    """Save category (create or update)."""
    # Validation
    if not form_data["name"]:
        notify_error("O nome é obrigatório")
        return

    try:
        if is_edit:
            await api.update_category(state.selected_category["id"], form_data)
            notify_success("Categoria atualizada com sucesso!")
        else:
            await api.create_category(form_data)
            notify_success("Categoria criada com sucesso!")

        dialog.close()
        await load_categories()
    except Exception as e:
        error_msg = str(e)
        if "already exists" in error_msg.lower():
            notify_error("Já existe uma categoria com este nome")
        else:
            notify_error(f"Erro ao salvar categoria: {error_msg}")


def open_delete_modal(category: dict):
    """Open confirmation modal for deleting category."""
    state.selected_category = category

    with ui.dialog() as dialog, ui.card().classes("w-full max-w-md"):
        dialog.open()

        # Header
        with ui.row().classes("w-full items-center gap-3 mb-4"):
            ui.icon("warning", size="2rem").classes("text-negative")
            ui.label("Confirmar Exclusão").classes("text-xl font-bold")

        # Content
        with ui.column().classes("gap-2"):
            ui.label(f"Deseja realmente excluir a categoria '{category['name']}'?").classes(
                "text-gray-700 dark:text-gray-300"
            )
            ui.label(
                "Esta ação não poderá ser desfeita se a categoria estiver sendo usada em transações."
            ).classes("text-sm text-gray-600 dark:text-gray-400")

        # Actions
        with ui.row().classes("w-full justify-end gap-2 mt-4"):
            create_button(label="Cancelar", on_click=dialog.close, variant="ghost")
            create_button(
                label="Excluir", on_click=lambda: delete_category(dialog), variant="error"
            )


async def delete_category(dialog):
    """Delete the selected category."""
    try:
        await api.delete_category(state.selected_category["id"])
        notify_success("Categoria excluída com sucesso!")
        dialog.close()
        await load_categories()
    except Exception as e:
        error_msg = str(e)
        if "in use" in error_msg.lower() or "foreign key" in error_msg.lower():
            notify_error(
                "Não é possível excluir esta categoria pois ela está sendo usada em transações"
            )
        else:
            notify_error(f"Erro ao excluir categoria: {error_msg}")
            notify_error(f"Erro ao excluir categoria: {error_msg}")
