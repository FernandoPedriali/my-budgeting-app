from nicegui import ui


def menu() -> None:
    ui.link("Home", "/").classes(replace="text-white")
    ui.link("A", "/a").classes(replace="text-white")
    ui.link("B", "/b").classes(replace="text-white")
    ui.link("C", "/c").classes(replace="text-white")


def menu_dropdown() -> None:
    with ui.dropdown_button("Menu", icon="menu", auto_close=True, split=False).classes(
        "text-white"
    ):
        with ui.column():
            ui.link("Home", "/")
            ui.link("A", "/a")
            ui.link("B", "/b")
            ui.link("C", "/c")
