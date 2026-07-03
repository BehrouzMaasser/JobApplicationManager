"""
Read-only query helpers for the CompanyEmail domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import Company, CompanyEmail

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError
)


class CompanyEmailSelector:
    """
    Provides reusable read operations for CompanyEmail objects.
    """

    @dataclass
    class QueryFilter:

        workspace_id: str | None = None
        company_id: int | None = None
        id: int | None = None

    @staticmethod
    def get(*, user: User, company_email_id: int) -> CompanyEmail | Exception:
        """
        Retrieve a CompanyEmail from the CompanyEmails database.

        Returns:
            CompanyEmail:
                CompanyEmail of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the CompanyEmail does not exist.

            AccessDeniedError:
                If the CompanyEmail does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                CompanyEmail.

        """

        try:
            company_email = CompanyEmail.objects.get(pk=company_email_id)
        except CompanyEmail.DoesNotExist:
            raise ResourceNotFoundError(
                resource=f"Company Email {company_email_id}"
            )
        except ValidationError as e:
            raise InfraStructureViolationError(e) from e

        if company_email.company.workspace.owner != user:
            raise AccessDeniedError(
                resource=f"Company Email {company_email_id}",
                message=f"Company Email {company_email_id} does not belong to {user}"
            )

        return company_email

    @staticmethod
    def list(*, user: User, filters: None | QueryFilter = None) -> QuerySet[Company]:
        """
        Retrieve a queryset of CompanyEmails from the CompanyEmails database.

        Args:
            user (User):
                User who owns the CompanyEmails.

            filters (QueryFilter | None = None):
                Query filters applied to the CompanyEmails.

        Returns:
            QuerySet[CompanyEmails]:
                - A queryset of the CompanyEmails owned by the user based on
                filters provided.
                - An Empty queryset if user owned no CompanyEmails and nothing
                matches the filters provided.
        """

        queryset = CompanyEmail.objects.filter(company__workspace__owner=user)

        if not filters:
            return queryset

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(company__workspace__workspace_id=workspace_id)

        if company_id := filters.company_id:
            queryset = queryset.filter(company__pk=company_id)

        if filters.id:
            queryset = queryset.filter(id=filters.id)

        return queryset
