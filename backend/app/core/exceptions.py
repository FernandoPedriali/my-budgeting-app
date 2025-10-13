"""Custom exceptions and exception handlers."""

from typing import Any

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError


class AppException(Exception):
    """Base exception for application errors."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: dict[str, Any] | None = None,
    ) -> None:
        """
        Initialize exception.

        Args:
            message: Error message
            status_code: HTTP status code
            details: Additional error details
        """
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundException(AppException):
    """Exception for not found errors."""

    def __init__(self, message: str = "Resource not found") -> None:
        """Initialize exception."""
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class BadRequestException(AppException):
    """Exception for bad request errors."""

    def __init__(self, message: str = "Bad request") -> None:
        """Initialize exception."""
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


class ConflictException(AppException):
    """Exception for conflict errors."""

    def __init__(self, message: str = "Resource conflict") -> None:
        """Initialize exception."""
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handler for application exceptions.

    Args:
        request: FastAPI request
        exc: Exception raised

    Returns:
        JSON response with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "details": exc.details,
        },
    )


async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """
    Handler for Pydantic validation errors.

    Args:
        request: FastAPI request
        exc: Validation error

    Returns:
        JSON response with validation errors
    """
    errors = []
    for error in exc.errors():
        errors.append(
            {
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "errors": errors,
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handler for HTTP exceptions.

    Args:
        request: FastAPI request
        exc: HTTP exception

    Returns:
        JSON response with error
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler for generic exceptions.

    Args:
        request: FastAPI request
        exc: Generic exception

    Returns:
        JSON response with error
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": str(exc) if hasattr(exc, "__str__") else "Unknown error",
        },
    )
