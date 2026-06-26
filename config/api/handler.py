# config/api/handler.py

import logging

from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    BusinessRuleViolationError, DomainInvariantViolationError,
)


logger = logging.getLogger(__name__)


def _error_response(
    *,
    code: str,
    message: str,
    status_code: int,
    details: dict | None = None,
):
    return Response(
        {
            "error": {
                "code": code,
                "message": message,
                "details": details or {},
            }
        },
        status=status_code,
    )


def api_exception_handler(exc, context):

    #
    # Custom application exceptions
    #

    if isinstance(exc, DomainInvariantViolationError):
        logger.exception(exc)
        return _error_response(
            code="internal_server_error",
            message="An unexpected error occurred.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if isinstance(exc, ResourceNotFoundError):
        return _error_response(
            code="resource_not_found",
            message=exc.message,
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, AccessDeniedError):
        return _error_response(
            code="access_denied",
            message=exc.message,
            status_code=status.HTTP_403_FORBIDDEN,
        )

    if isinstance(exc, BusinessRuleViolationError):

        return _error_response(
            code="business_rule_violation",
            message=exc.message,
            details=exc.details,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    #
    # Django ValidationError
    #

    if isinstance(exc, ValidationError):

        if hasattr(exc, "message_dict"):
            details = exc.message_dict
        else:
            details = exc.messages

        return _error_response(
            code="validation_error",
            message="Validation failed",
            details=details,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    #
    # DRF handle its own exceptions if not caught up there
    #

    response = exception_handler(exc, context)

    if response is None:
        return None

    return _error_response(
        code="api_error",
        message="Request failed.",
        details=response.data,
        status_code=response.status_code,
    )
