from contextlib import suppress
from typing import Any, Union

from argon2 import PasswordHasher
from fastapi import Request, UploadFile
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

ph = PasswordHasher()


class ErrorFormatter:
    """Format errors in a consistent and user-friendly way."""

    @classmethod
    def format_validation_error(
        cls, error: Union[ValidationError, RequestValidationError]
    ) -> dict[str, Any]:
        """
        Transform validation errors into a user-friendly format.

        Returns:
            Dict with field names as keys and error messages as values.
        """
        error_dict = {}

        for err in error.errors():
            field = cls._extract_field_name(err)
            message = cls._create_user_friendly_message(err)
            if message is not None:  # Only add non-null messages
                error_dict[field] = message

        return {"errors": error_dict}

    @staticmethod
    def _extract_field_name(error: dict[str, Any]) -> str:
        if "loc" in error and len(error["loc"]) > 0:
            return str(error["loc"][-1])
        return "general"

    @staticmethod
    def _create_user_friendly_message(error: dict[str, Any]) -> str:
        error_type = error.get("type", "")
        input_type = ErrorFormatter._extract_field_name(error)

        if input_type == "file":
            return "Request doesn't contain any files attached."
        elif error.get("input") is None:
            return "Request body is empty"
        elif error_type == "missing":
            return "This field is required"
        elif error_type == "value_error.str.min_length":
            return (
                f"Must be at least {error.get('ctx', {}).get('limit_value')} characters"
            )
        elif error_type == "value_error.email":
            return "Invalid email format"
        elif error_type == "value_error.any_str.min_length":
            return (
                f"Must be at least {error.get('ctx', {}).get('limit_value')} characters"
            )

        with suppress(Exception):
            return error.get("msg", "Invalid value").split(",")[1].strip().capitalize()


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):  # NOQA
    """
    Handle validation errors and return user-friendly error messages.

    Args:
        request: The incoming request
        exc: The validation exception

    Returns:
        A JSONResponse with formatted validation errors
    """
    return JSONResponse(
        status_code=422, content=ErrorFormatter.format_validation_error(exc)
    )


def clean_file_entry(file: UploadFile) -> UploadFile:
    if not file:
        raise HTTPException(
            status_code=400,
            detail="No file provided",
        )
    file_size = convert_bytes_to_mb(file.size)
    if file_size > 2.0:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 2 MB limit",
        )

    return file


def convert_bytes_to_mb(file_size: float) -> float:
    """
    1 MB = 1000^2 bytes
    1 MiB = 1024^2 bytes
    https://stackoverflow.com/questions/2365100/converting-bytes-to-megabytes
    """
    return float(file_size / (1000**2))
