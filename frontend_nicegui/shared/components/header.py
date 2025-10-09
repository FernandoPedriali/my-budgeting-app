from nicegui import ui


def header():
    with ui.header().classes(
        "bg-black text-white p-4 flex items-center justify-between"
    ):
        with ui.button(on_click=lambda: ui.notify("Check flat button clicked")
                       ).props('flat').classes('text-black'):
            ui.image("frontend_nicegui/shared/assets/svg/Flat_tick_icon.svg").classes('w-6 h-6')
        ui.space()
        ui.button("About").on("click", lambda: ui.notify("About clicked"))
        ui.space()
        ui.button("Contact").on("click", lambda: ui.notify("Contact clicked"))
