from dataclasses import dataclass

from django.db.models import QuerySet

from apps.accounts.models import User
from apps.applications.models import JobApplicationNote


class JobApplicationNoteSelector:

    @dataclass
    class QueryFilter:
        workspace_id: str | None = None
        company_id: int | None = None
        job_position_id: int | None = None
        job_application_id: int | None = None
        id: int | None = None

    @staticmethod
    def list(
            *,
            user: User,
            filters: None | QueryFilter = None
    ) -> QuerySet[JobApplicationNote]:

        queryset = JobApplicationNote.objects.filter(job_application__owner=user)

        if not filters:
            return queryset

        if filters.workspace_id:
            queryset = queryset.filter(
                job_application__workspace__workspace_id=filters.workspace_id
            )

        if filters.company_id:
            queryset = queryset.filter(
                job_application__job_position__company__pk=filters.company_id
            )

        if filters.job_position_id:
            queryset = queryset.filter(
                job_application__job_position__pk=filters.job_position_id
            )

        if filters.job_application_id:
            queryset = queryset.filter(
                job_application__pk=filters.job_application_id
            )

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
