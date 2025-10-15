"""API client for backend communication."""

from typing import Any, Optional

import httpx

from frontend.app.config import settings


class APIClient:
    """HTTP client for backend API requests."""

    def __init__(self):
        self.base_url = f"http://{settings.BACKEND_HOST}:{settings.BACKEND_PORT}/api/v1"
        self.timeout = 10.0

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict[str, Any]:
        """Make an HTTP request to the backend API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint (e.g., "/categories")
            params: Query parameters
            json: JSON body

        Returns:
            Response data as dictionary

        Raises:
            httpx.HTTPError: If request fails
        """
        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=json,
            )
            response.raise_for_status()
            return response.json()

    # Categories endpoints
    async def get_categories(
        self,
        type: Optional[str] = None,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> dict[str, Any]:
        """Get all categories with optional filters."""
        params = {}
        if type:
            params["type"] = type
        if search:
            params["search"] = search
        if is_active is not None:
            params["is_active"] = is_active

        return await self._request("GET", "/categories", params=params)

    async def get_category(self, category_id: int) -> dict[str, Any]:
        """Get a category by ID."""
        return await self._request("GET", f"/categories/{category_id}")

    async def create_category(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new category."""
        return await self._request("POST", "/categories", json=data)

    async def update_category(self, category_id: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update a category."""
        return await self._request("PUT", f"/categories/{category_id}", json=data)

    async def delete_category(self, category_id: int, permanent: bool = False) -> dict[str, Any]:
        """Delete a category (soft or hard delete)."""
        params = {"permanent": permanent}
        return await self._request("DELETE", f"/categories/{category_id}", params=params)

    async def restore_category(self, category_id: int) -> dict[str, Any]:
        """Restore a soft-deleted category."""
        return await self._request("PATCH", f"/categories/{category_id}/restore")

    # Accounts endpoints
    async def get_accounts(self, is_active: Optional[bool] = None) -> dict[str, Any]:
        """Get all accounts."""
        params = {}
        if is_active is not None:
            params["is_active"] = is_active
        return await self._request("GET", "/accounts", params=params)

    async def get_account(self, account_id: int) -> dict[str, Any]:
        """Get an account by ID."""
        return await self._request("GET", f"/accounts/{account_id}")

    async def create_account(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new account."""
        return await self._request("POST", "/accounts", json=data)

    async def update_account(self, account_id: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update an account."""
        return await self._request("PUT", f"/accounts/{account_id}", json=data)

    async def delete_account(self, account_id: int, permanent: bool = False) -> dict[str, Any]:
        """Delete an account."""
        params = {"permanent": permanent}
        return await self._request("DELETE", f"/accounts/{account_id}", params=params)

    # Transactions endpoints
    async def get_transactions(self, **filters) -> dict[str, Any]:
        """Get all transactions with optional filters."""
        return await self._request("GET", "/transactions", params=filters)

    async def get_transaction(self, transaction_id: int) -> dict[str, Any]:
        """Get a transaction by ID."""
        return await self._request("GET", f"/transactions/{transaction_id}")

    async def create_transaction(self, data: dict[str, Any]) -> dict[str, Any]:
        """Create a new transaction."""
        return await self._request("POST", "/transactions", json=data)

    async def update_transaction(self, transaction_id: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update a transaction."""
        return await self._request("PUT", f"/transactions/{transaction_id}", json=data)

    async def delete_transaction(self, transaction_id: int) -> dict[str, Any]:
        """Delete a transaction."""
        return await self._request("DELETE", f"/transactions/{transaction_id}")

    async def update_transaction_status(self, transaction_id: int, status: str) -> dict[str, Any]:
        """Update transaction status."""
        return await self._request(
            "PATCH", f"/transactions/{transaction_id}/status", json={"status": status}
        )


# Global API client instance
api = APIClient()
