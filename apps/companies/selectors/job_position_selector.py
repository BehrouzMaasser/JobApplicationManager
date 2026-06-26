from dataclasses import dataclass

from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import JobPosition

# Exceptions
from apps.core.exceptions.exceptions import ResourceNotFoundError, AccessDeniedError


class JobPositionSelector:

    @dataclass
    class QueryFilter:
        workspace_id: str | None = None
        company_id: str | None = None
        id: int | None = None

    @staticmethod
    def get(*, user: User, job_position_id: int) -> JobPosition | Exception:

        try:
            job_position = JobPosition.objects.get(pk=job_position_id)
        except JobPosition.DoesNotExist:
            raise ResourceNotFoundError(
                f"Job Position {job_position_id} does not exist"
            )

        if job_position.company.workspace.owner != user:
            raise AccessDeniedError(
                f"Job Position {job_position_id} does not belong to {user}"
            )

        return job_position

    @staticmethod
    def list(
            *, user: User, filters: None | QueryFilter = None
    ) -> QuerySet[JobPosition]:

        queryset = JobPosition.objects.filter(company__workspace__owner=user)

        if not filters:
            return queryset

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(company__workspace__workspace_id=workspace_id)

        if company_id := filters.company_id:
            queryset = queryset.filter(company__pk=company_id)

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
