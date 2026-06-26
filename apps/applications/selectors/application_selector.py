from dataclasses import dataclass
from datetime import datetime

from django.db.models import QuerySet

from apps.accounts.models import User
from apps.applications.models import JobApplication
from apps.core.exceptions.exceptions import ResourceNotFoundError, AccessDeniedError


class JobApplicationSelector:

    @dataclass
    class QueryFilter:
        workspace_id: str | None = None
        company_id: int | None = None
        job_position_id: int | None = None
        id: int | None = None
        status_id: int | None = None
        date_applied: datetime | None = None

    @staticmethod
    def get(user: User, application_id: int) -> JobApplication | Exception:

        try:
            job_application = JobApplication.objects.get(pk=application_id)
        except JobApplication.DoesNotExist:
            raise ResourceNotFoundError(
                "Job Application",
                f"Job Application {application_id} does not exist"
            )

        if job_application.owner != user:
            raise AccessDeniedError(
                "Job Application",
                f"Job Application {application_id} does not belong to {user}"
            )

        return job_application

    @staticmethod
    def list(
            *, user: User, filters: None | QueryFilter = None
    ) -> QuerySet[JobApplication]:

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
