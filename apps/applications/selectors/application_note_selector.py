from dataclasses import dataclass

from django.db.models import QuerySet

from apps.accounts.models import User
from apps.applications.models import JobApplicationNote
from apps.core.exceptions.exceptions import ResourceNotFoundError, AccessDeniedError


class JobApplicationNoteSelector:

    @dataclass
    class QueryFilter:
        workspace_id: str | None = None
        company_id: int | None = None
        job_position_id: int | None = None
        job_application_id: int | None = None
        id: int | None = None

    @staticmethod
    def get(user: User, application_note_id: int) -> JobApplicationNote | Exception:

        try:
            application_note = JobApplicationNote.objects.get(pk=application_note_id)
        except JobApplicationNote.DoesNotExist:
            raise ResourceNotFoundError(
                f"Job Application Note {application_note_id} does not exist"
            )

        if application_note.job_application.owner != user:
            raise AccessDeniedError(
                f"Job Application Note {application_note_id} does not belong to"
                f" {user}"
            )

        return application_note

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
