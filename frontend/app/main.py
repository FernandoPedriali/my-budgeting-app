"""Main entry point for the NiceGUI frontend application."""

from nicegui import app, ui

from frontend.app.config import settings

# Import all pages to register routes
from frontend.app.pages import (
    accounts_page,
    categories_page,
    dashboard_page,
    not_found_page,
    transactions_page,
)


def setup_ui():
    # Configure dark mode
    ui.dark_mode().enable()

    # Add custom CSS for better styling
    ui.add_head_html(
        """
        <style>
            * {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }

            body {
                margin: 0;
                padding: 0;
            }

            /* Remove default link underline */
            a {
                text-decoration: none !important;
            }

            /* Smooth transitions */
            * {
                transition: background-color 0.2s ease, color 0.2s ease;
            }
        </style>
    """
    )


app.on_startup(setup_ui)


def main():
    """Initialize and run the NiceGUI application."""
    # Run the application
    ui.run(
        host=settings.FRONTEND_HOST,
        port=settings.FRONTEND_PORT,
        title="My Budget - Controle Financeiro",
        favicon="💰",
        reload=True,
        show=False,
        dark=True,
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
