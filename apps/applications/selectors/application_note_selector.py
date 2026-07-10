"""
Read-only query helpers for the JobApplicationNote domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.applications.models import JobApplicationNote

# Exceptions
from apps.core.exceptions.exceptions import (
    AccessDeniedError,
    InfraStructureViolationError,
    ResourceNotFoundError,
)


class JobApplicationNoteSelector:
    """
    Provides reusable read operations for JobApplicationNote objects.
    """

    @dataclass
    class QueryFilter:
        workspace_id: str | None = None
        company_id: int | None = None
        job_position_id: int | None = None
        job_application_id: int | None = None
        id: int | None = None

    @staticmethod
    def get(
        *,
        user: User,
        application_note_id: int,
    ) -> JobApplicationNote | Exception:
        """
        Retrieve a JobApplicationNote from the JobApplicationNotes database.

        Returns:
            JobApplicationNote:
                JobApplicationNote of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the JobApplicationNote does not exist.

            AccessDeniedError:
                If the JobApplicationNote does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving
                the JobApplicationNote.
        """

        try:
            application_note = JobApplicationNote.objects.get(
                pk=application_note_id
            )
        except JobApplicationNote.DoesNotExist:
            raise ResourceNotFoundError(
                resource=f"Job Application Note {application_note_id}"
            )
        except ValidationError as e:
            raise InfraStructureViolationError(e) from e

        if application_note.job_application.owner != user:
            raise AccessDeniedError(
                resource=f"Job Application Note {application_note_id}",
                message=f"Job Application Note {application_note_id} does not belong "
                        f"to {user}",
            )

        return application_note

    @staticmethod
    def list(
        *,
        user: User,
        filters: None | QueryFilter = None,
    ) -> QuerySet[JobApplicationNote]:
        """
        Retrieve a queryset of JobApplicationNotes from the
        JobApplicationNotes database.

        Args:
            user (User):
                User who owns the JobApplicationNotes.

            filters (QueryFilter | None = None):
                Query filters applied to the JobApplicationNotes.

        Returns:
            QuerySet[JobApplicationNote]:
                - A queryset of the JobApplicationNotes owned by the user based
                on filters provided.
                - An empty queryset if the user owns no JobApplicationNotes or
                nothing matches the filters provided.
        """

        queryset = JobApplicationNote.objects.filter(
            job_application__owner=user
        )

        if not filters:
            return queryset

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(
                job_application__workspace__workspace_id=workspace_id
            )

        if company_id := filters.company_id:
            queryset = queryset.filter(
                job_application__job_position__company__pk=company_id
            )

        if job_position_id := filters.job_position_id:
            queryset = queryset.filter(
                job_application__job_position__pk=job_position_id
            )

        if job_application_id := filters.job_application_id:
            queryset = queryset.filter(
                job_application__pk=job_application_id
            )

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
