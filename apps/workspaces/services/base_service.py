"""
Shared service-layer utilities.

Provides reusable helper methods for updating model fields and performing
common business-rule validations used across domain services.
"""

import django.db.models

# Models
from apps.accounts.models import User

# Exceptions
from apps.core.exceptions.exceptions import (
    BusinessRuleViolationError,
    DomainInvariantViolationError
)


# Base Service
class BaseService:
    """
    Base class providing reusable helper methods for domain services.

    The class centralizes common update operations and validation logic
    shared by multiple service implementations.
    """

    @staticmethod
    def _update_non_m2m_fields(
            instance: django.db.models.Model,
            validated_data: dict,
            fields_to_update: list[str]
    ) -> None:

        for field in fields_to_update:
            if field not in validated_data:
                continue
            setattr(instance, field, validated_data[field])

    @staticmethod
    def _update_m2m_fields(
            instance: django.db.models.Model,
            validated_data: dict,
            fields_to_update: list[str]
    ) -> None:

        for field in fields_to_update:
            if field not in validated_data:
                continue
            getattr(instance, field).set(validated_data.get(field))

    @staticmethod
    def _add_m2m_fields(
            instance: django.db.models.Model,
            validated_data: dict,
            m2m_fields: list[str]
    ) -> None:

        for field in m2m_fields:
            if field in validated_data:
                getattr(instance, field).add(*validated_data[field])

    @staticmethod
    def _m2m_ownership_validation(
            user: User, validated_data: dict, ownership_map: dict[str, str]
    ) -> None:

        # Make sure the m2m fields are associated to the user
        invalid_fields_with_ids: dict[str, list[str]] = dict()

        for field_name, ownership in ownership_map.items():
            if field_name in validated_data:
                for data in validated_data[field_name]:
                    # Some related models may not expose the configured ownership
                    # attribute.
                    # Those objects are ignored because ownership cannot be
                    # validated for them.
                    try:
                        if getattr(data, ownership) != user:
                            invalid_fields_with_ids.setdefault(
                                field_name, []
                            ).append(data.pk)
                    except AttributeError:
                        continue

        if invalid_fields_with_ids:
            raise DomainInvariantViolationError(
                message=[
                    f"The current user does not own the following {field}: {ids}"
                    for field, ids in invalid_fields_with_ids.items()
                ]
            )

    @staticmethod
    def _m2m_non_empty_validation(
            instance: django.db.models.Model, required_fields: list[str]
    ) -> None:

        empty_required_fields = []

        for field in required_fields:
            if not getattr(instance, field).exists():
                empty_required_fields.append(field)

        if empty_required_fields:
            raise BusinessRuleViolationError(
                fields=empty_required_fields,
                messages=["Should not be empty" for _ in empty_required_fields]
            )
