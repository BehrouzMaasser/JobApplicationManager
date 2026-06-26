from dataclasses import dataclass

from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import CompanyNote

# Exceptions
from apps.core.exceptions.exceptions import ResourceNotFoundError, AccessDeniedError


class CompanyNoteSelector:

    @dataclass
    class QueryFilter:

        workspace_id: str | None = None
        company_id: int | None = None
        id: int | None = None

    @staticmethod
    def get(*, user: User, company_note_id: int) -> CompanyNote | Exception:

        try:
            company_note = CompanyNote.objects.get(pk=company_note_id)
        except CompanyNote.DoesNotExist:
            raise ResourceNotFoundError(
                resource=f"Company Note {company_note_id}",
            )

        if company_note.company.workspace.owner != user:
            raise AccessDeniedError(
                resource=f"Company Note {company_note_id}",
                message=f"Company Note {company_note_id} does not belong to {user}"
            )

        return company_note

    @staticmethod
    def list(
            *, user: User, filters: None | QueryFilter = None
    ) -> QuerySet[CompanyNote]:

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
