"""
Read-only query helpers for the CompanyNote domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import JobPosition

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError
)


class JobPositionSelector:
    """
    Provides reusable read operations for JobPosition objects.
    """

    @dataclass
    class QueryFilter:
        workspace_id: str | None = None
        company_id: str | None = None
        id: int | None = None

    @staticmethod
    def get(*, user: User, job_position_id: int) -> JobPosition | Exception:
        """
        Retrieve a JobPosition from the JobPositions database.

        Returns:
            JobPosition:
                JobPosition of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the JobPosition does not exist.

            AccessDeniedError:
                If the JobPosition does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                JobPosition.

        """

        try:
            job_position = JobPosition.objects.get(pk=job_position_id)
        except JobPosition.DoesNotExist:
            raise ResourceNotFoundError(
                resource=f"Job Position {job_position_id}"
            )
        except ValidationError as e:
            raise InfraStructureViolationError(e) from e

        if job_position.company.workspace.owner != user:
            raise AccessDeniedError(
                resource=f"Job Position {job_position_id}",
                message=f"Job Position {job_position_id} does not belong to {user}"
            )

        return job_position

    @staticmethod
    def list(
            *,
            user: User,
            filters: None | QueryFilter = None
    ) -> QuerySet[JobPosition]:
        """
        Retrieve a queryset of JobPositions from the JobPositions database.

        Args:
            user (User):
                User who owns the JobPositions.

            filters (QueryFilter | None = None):
                Query filters applied to the JobPositions.

        Returns:
            QuerySet[JobPosition]:
                - A queryset of the JobPositions owned by the user based on
                filters provided.
                - An Empty queryset if user owned no JobPositions and nothing
                matches the filters provided.
        """

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
