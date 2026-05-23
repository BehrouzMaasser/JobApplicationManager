from dataclasses import dataclass

from django.db.models import QuerySet

from apps.accounts.models import User
from apps.companies.models import Company


class CompanySelector:

    @dataclass
    class QueryFilter:

        workspace_id: str | None
        id: int | None = None

    @staticmethod
    def list(*, user: User, filters: None | QueryFilter) -> QuerySet[Company]:

        queryset = Company.objects.filter(workspace__owner=user)

        if not filters:
            return queryset

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(workspace__workspace_id=workspace_id)

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
