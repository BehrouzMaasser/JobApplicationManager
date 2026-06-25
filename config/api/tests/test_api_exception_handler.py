from config.api.handler import api_exception_handler

# Exceptions
from django.core.exceptions import ValidationError
from apps.core.exceptions.exceptions import ResourceNotFoundError, AccessDeniedError, \
    BusinessRuleViolationError


def test_resource_not_found_error():

    exc = ResourceNotFoundError("Company")

    response = api_exception_handler(
        exc,
        context={},
    )

    assert response.status_code == 404

    assert response.data == {
        "error": {
            "code": "resource_not_found",
            "message": "Resource Company not found",
            "details": {},
        }
    }


def test_access_denied_error():

    exc = AccessDeniedError("Workspace")

    response = api_exception_handler(
        exc,
        context={},
    )

    assert response.status_code == 403

    assert response.data == {
        "error": {
            "code": "access_denied",
            "message": "Access to Workspace was denied",
            "details": {},
        }
    }


def test_business_rule_violation_error():

    exc = BusinessRuleViolationError(
        fields=["emails", "documents"],
        messages=[
            "Emails should belong to current company",
            "Documents should belong to current workspace"
        ],
    )

    response = api_exception_handler(exc, context={})

    assert response.status_code == 400

    assert response.data == {
        "error": {
            "code": "business_rule_violation",
            "message": "Business rule violated",
            "details": {
                "emails": [
                    "Emails should belong to current company"
                ],
                "documents": [
                    "Documents should belong to current workspace"
                ]
            }
        }
    }


def test_django_validation_error():

    exc = ValidationError({
        "name": [
            "This field is required."
        ]
    })

    response = api_exception_handler(
        exc,
        context={},
    )

    assert response.status_code == 400

    assert response.data == {
        "error": {
            "code": "validation_error",
            "message": "Validation failed",
            "details": {
                "name": [
                    "This field is required."
                ]
            },
        }
    }
