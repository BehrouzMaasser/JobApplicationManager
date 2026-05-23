from dataclasses import dataclass

from django.db.models import QuerySet

from apps.accounts.models import User
from apps.applications.models import JobApplication


class JobApplicationSelector:

    @dataclass
    class QueryFilter:
        workspace_id: str | None
        company_id: int | None
        job_position_id: int | None
        id: int | None = None
        status_id: int | None = None
        date_applied: str | None = None

    @staticmethod
    def list(*, user: User, filters: None | QueryFilter) -> QuerySet[JobApplication]:

        queryset = JobApplication.objects.filter(owner=user)

        if not filters:
            return queryset

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(workspace__workspace_id=workspace_id)

        if company_id := filters.company_id:
            queryset = queryset.filter(job_position__company__pk=company_id)

        if job_position_id := filters.job_position_id:
            queryset = queryset.filter(job_position__pk=job_position_id)

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        if status_id := filters.status_id:
            queryset = queryset.filter(status__pk=status_id)

        if date_applied := filters.date_applied:
            queryset = queryset.filter(date_applied=date_applied)

        return queryset
