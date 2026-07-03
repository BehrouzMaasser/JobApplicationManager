"""
Read-only query helpers for the Company domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import Company

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError
)


class CompanySelector:
    """
    Provides reusable read operations for Company objects.
    """

    @dataclass
    class QueryFilter:

        workspace_id: str | None = None
        id: int | None = None

    @staticmethod
    def get(*, user: User, company_id: int) -> Company | Exception:
        """
        Retrieve a Company from the Companies database.

        Returns:
            Company:
                Company of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the Company does not exist.

            AccessDeniedError:
                If the Company does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                Company.

        """

        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise ResourceNotFoundError(resource=f"Company {company_id}")
        except ValidationError as e:
            raise InfraStructureViolationError(e) from e

        if company.workspace.owner != user:
            raise AccessDeniedError(
                resource=f"Company {company_id}",
                message=f"Company {company_id} does not belong to {user}"
            )

        return company

    @staticmethod
    def list(*, user: User, filters: None | QueryFilter = None) -> QuerySet[Company]:
        """
        Retrieve a queryset of Companies from the Companies database.

        Args:
            user (User):
                User who owns the Companies.

            filters (QueryFilter | None = None):
                Query filters applied to the Companies.

        Returns:
            QuerySet[Company]:
                - A queryset of the Companies owned by the user based on
                filters provided.
                - An Empty queryset if user owned no Companies and nothing matches
                the filters provided.
        """

        queryset = Company.objects.filter(workspace__owner=user)

        if not filters:
            return queryset

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(workspace__workspace_id=workspace_id)

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
