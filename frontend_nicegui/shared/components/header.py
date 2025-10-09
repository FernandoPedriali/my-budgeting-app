from nicegui import ui


def header():
    with ui.header().classes(
        "bg-gray-800 text-white p-4 flex items-center justify-between"
    ):
        ui.label("My Application").classes("text-lg font-bold")
        with ui.row().classes("gap-4"):
            ui.button("Home").on("click", lambda: ui.notify("Home clicked"))
            ui.button("About").on("click", lambda: ui.notify("About clicked"))
            ui.button("Contact").on("click", lambda: ui.notify("Contact clicked"))
