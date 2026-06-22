from dataclasses import dataclass

from django.db.models import QuerySet

from apps.accounts.models import User
from apps.companies.models import Company, CompanyEmail
from apps.core.exceptions.exceptions import ResourceNotFoundError, AccessDeniedError


class CompanyEmailSelector:

    @dataclass
    class QueryFilter:

        workspace_id: str | None = None
        company_id: int | None = None
        id: int | None = None

    @staticmethod
    def get(*, user: User, company_email_id: int) -> CompanyEmail | Exception:

        try:
            company_email = CompanyEmail.objects.get(pk=company_email_id)
        except CompanyEmail.DoesNotExist:
            raise ResourceNotFoundError(
                f"Company Email {company_email_id} does not exist"
            )

        if company_email.company.workspace.owner != user:
            raise AccessDeniedError(
                f"Company Email {company_email_id} does not belong to {user}"
            )

        return company_email

    @staticmethod
    def list(*, user: User, filters: None | QueryFilter = None) -> QuerySet[Company]:

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
