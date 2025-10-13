"""API v1 router."""

from fastapi import APIRouter

from .accounts import router as accounts_router
from .categories import router as categories_router
from .transactions import router as transactions_router

# Create main API v1 router
api_router = APIRouter(prefix="/api/v1")

# Include all routers
api_router.include_router(categories_router)
api_router.include_router(accounts_router)
api_router.include_router(transactions_router)

__all__ = ["api_router"]
