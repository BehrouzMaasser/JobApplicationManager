"""
Read-only query helpers for the CompanyNote domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import CompanyNote

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError
)


class CompanyNoteSelector:
    """
    Provides reusable read operations for CompanyNote objects.
    """

    @dataclass
    class QueryFilter:

        workspace_id: str | None = None
        company_id: int | None = None
        id: int | None = None

    @staticmethod
    def get(*, user: User, company_note_id: int) -> CompanyNote | Exception:
        """
        Retrieve a CompanyNote from the CompanyNotes database.

        Returns:
            CompanyNote:
                CompanyNote of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the CompanyNote does not exist.

            AccessDeniedError:
                If the CompanyNote does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                CompanyNote.

        """

        try:
            company_note = CompanyNote.objects.get(pk=company_note_id)
        except CompanyNote.DoesNotExist:
            raise ResourceNotFoundError(
                resource=f"Company Note {company_note_id}",
            )
        except ValidationError as e:
            raise InfraStructureViolationError(e) from e

        if company_note.company.workspace.owner != user:
            raise AccessDeniedError(
                resource=f"Company Note {company_note_id}",
                message=f"Company Note {company_note_id} does not belong to {user}"
            )

        return company_note

    @staticmethod
    def list(
            *,
            user: User,
            filters: None | QueryFilter = None
    ) -> QuerySet[CompanyNote]:
        """
        Retrieve a queryset of CompanyNotes from the CompanyNotes database.

        Args:
            user (User):
                User who owns the CompanyNotes.

            filters (QueryFilter | None = None):
                Query filters applied to the CompanyNotes.

        Returns:
            QuerySet[CompanyNotes]:
                - A queryset of the CompanyNotes owned by the user based on
                filters provided.
                - An Empty queryset if user owned no CompanyNotes and nothing
                matches the filters provided.
        """

        queryset = CompanyNote.objects.filter(company__workspace__owner=user)

        if not filters:
            return queryset

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(company__workspace__workspace_id=workspace_id)

        if company_id := filters.company_id:
            queryset = queryset.filter(company__pk=company_id)

        if filters.id:
            queryset = queryset.filter(id=filters.id)

        return queryset
