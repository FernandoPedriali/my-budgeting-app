"""Application pages."""

from .accounts import accounts_page
from .categories import categories_page
from .dashboard import dashboard_page
from .not_found import not_found_page
from .transactions import transactions_page

__all__ = [
    "dashboard_page",
    "transactions_page",
    "accounts_page",
    "categories_page",
    "not_found_page",
]
