"""404 Not Found page."""

from nicegui import ui


@ui.page("/404")
def not_found_page():
    """404 error page for non-existent routes."""

    with ui.column().classes(
        "w-full h-screen items-center justify-center bg-gray-50 dark:bg-gray-950 gap-6 p-6"
    ):
        # Error icon and code
        with ui.column().classes("items-center gap-4"):
            ui.icon("error_outline", size="6rem").classes("text-gray-400")
            ui.label("404").classes("text-6xl font-bold text-gray-800 dark:text-gray-100")
            ui.label("Página não encontrada").classes("text-xl text-gray-600 dark:text-gray-400")

        # Description
        ui.label("A página que você está procurando não existe ou foi movida.").classes(
            "text-center text-gray-500 dark:text-gray-500 max-w-md"
        )

        # Action buttons
        with ui.row().classes("gap-4 mt-4"):
            with ui.link(target="/"):
                ui.button("Voltar ao Dashboard", icon="home").props("color=primary")

            ui.button("Voltar", icon="arrow_back", on_click=lambda: ui.navigate.back()).props(
                "flat color=primary"
            )
