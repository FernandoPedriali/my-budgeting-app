"""Base layout with sidebar and content area."""

from typing import Callable, Optional

from nicegui import ui

from .sidebar import create_sidebar


def create_base_layout(
    title: str, breadcrumb: Optional[list[str]] = None, content_builder: Optional[Callable] = None
):
    """Create the base layout with sidebar, header, breadcrumb and content area.

    Args:
        title: Page title to display in header
        breadcrumb: List of breadcrumb items (e.g., ["Dashboard", "Transações"])
        content_builder: Optional function that builds the page content

    Returns:
        The content container where page content should be added
    """
    with ui.row().classes("w-full h-screen m-0 p-0 gap-0"):
        # Sidebar
        create_sidebar()

        # Main content area
        with ui.column().classes("flex-1 h-screen overflow-auto bg-gray-50 dark:bg-gray-950"):
            # Header
            with ui.row().classes(
                "w-full p-6 bg-white dark:bg-gray-900 "
                "border-b border-gray-200 dark:border-gray-800 "
                "items-center justify-between"
            ):
                with ui.column().classes("gap-2"):
                    # Breadcrumb
                    if breadcrumb:
                        create_breadcrumb(breadcrumb)

                    # Page title
                    ui.label(title).classes("text-2xl font-bold text-gray-800 dark:text-gray-100")

            # Content area
            with ui.column().classes("flex-1 p-6 gap-4 w-full") as content:
                if content_builder:
                    content_builder()

    return content


def create_breadcrumb(items: list[str]):
    """Create a breadcrumb navigation.

    Args:
        items: List of breadcrumb items (e.g., ["Dashboard", "Transações"])
    """
    with ui.row().classes("items-center gap-2 text-sm"):
        for i, item in enumerate(items):
            # Show separator except for first item
            if i > 0:
                ui.icon("chevron_right", size="1rem").classes("text-gray-400")

            # Last item is the current page (not a link)
            if i == len(items) - 1:
                ui.label(item).classes("text-gray-800 dark:text-gray-100 font-medium")
            else:
                ui.label(item).classes("text-gray-500 dark:text-gray-400")
