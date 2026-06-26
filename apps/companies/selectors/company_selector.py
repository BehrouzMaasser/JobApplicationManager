from dataclasses import dataclass

from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import Company

# Exceptions
from apps.core.exceptions.exceptions import ResourceNotFoundError, AccessDeniedError


class CompanySelector:

    @dataclass
    class QueryFilter:

        workspace_id: str | None = None
        id: int | None = None

    @staticmethod
    def get(*, user: User, company_id: int) -> Company | Exception:

        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise ResourceNotFoundError(f"Company {company_id} does not exist")

        if company.workspace.owner != user:
            raise AccessDeniedError(
                f"Company {company_id} does not belong to {user}"
            )

        return company

    @staticmethod
    def list(*, user: User, filters: None | QueryFilter = None) -> QuerySet[Company]:

        queryset = Company.objects.filter(workspace__owner=user)

        if not filters:
            return queryset

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(workspace__workspace_id=workspace_id)

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
