from nicegui import ui
from shared.components.header import header


@ui.page("/")
def main_page():
    header()
    ui.label("Welcome to the main page!").classes("text-2xl m-4")

ui.run(title="My Budgeting App", port=8080, reload=True)
