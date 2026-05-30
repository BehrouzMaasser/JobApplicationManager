from dataclasses import dataclass

from django.db.models import QuerySet

from apps.accounts.models import User
from apps.companies.models import Company, CompanyEmail


class CompanyEmailSelector:

    @dataclass
    class QueryFilter:

        workspace_id: str | None = None
        company_id: int | None = None
        id: int | None = None

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
