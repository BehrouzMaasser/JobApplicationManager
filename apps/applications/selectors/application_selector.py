"""
Read-only query helpers for the JobApplication domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from dataclasses import dataclass
from datetime import datetime

from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.applications.models import JobApplication

# Exceptions
from apps.core.exceptions.exceptions import (
    AccessDeniedError,
    InfraStructureViolationError,
    ResourceNotFoundError,
)


class JobApplicationSelector:
    """
    Provides reusable read operations for JobApplication objects.
    """

    @dataclass
    class QueryFilter:
        workspace_id: str | None = None
        company_id: int | None = None
        job_position_id: int | None = None
        id: int | None = None
        status_id: int | None = None
        date_applied: datetime | None = None

    @staticmethod
    def get(*, user: User, application_id: int) -> JobApplication | Exception:
        """
        Retrieve a JobApplication from the JobApplications database.

        Returns:
            JobApplication:
                JobApplication of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the JobApplication does not exist.

            AccessDeniedError:
                If the JobApplication does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving
                the JobApplication.
        """

        try:
            job_application = JobApplication.objects.get(pk=application_id)
        except JobApplication.DoesNotExist:
            raise ResourceNotFoundError(
                resource=f"Job Application {application_id}",
            )
        except Exception as e:
            raise InfraStructureViolationError(e) from e

        if job_application.owner != user:
            raise AccessDeniedError(
                resource=f"Job Application {application_id}",
                message=f"Job Application {application_id} does not belong to {user}",
            )

        return job_application

    @staticmethod
    def list(
        *,
        user: User,
        filters: None | QueryFilter = None,
    ) -> QuerySet[JobApplication]:
        """
        Retrieve a queryset of JobApplications from the JobApplications database.

        Args:
            user (User):
                User who owns the JobApplications.

            filters (QueryFilter | None = None):
                Query filters applied to the JobApplications.

        Returns:
            QuerySet[JobApplication]:
                - A queryset of the JobApplications owned by the user based on
                filters provided.
                - An empty queryset if the user owns no JobApplications or
                nothing matches the filters provided.
        """

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
