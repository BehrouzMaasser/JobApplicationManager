"""
Read-only query helpers for the JobRequirement domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import JobRequirement

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError
)


class JobRequirementSelector:
    """
    Provides reusable read operations for JobRequirement objects.
    """

    @staticmethod
    def get(*, user: User, job_requirement_id: int) -> JobRequirement | Exception:
        """
        Retrieve a JobRequirement from the JobRequirements database.

        Returns:
            JobRequirement:
                JobRequirement of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the JobRequirement does not exist.

            AccessDeniedError:
                If the JobRequirement does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                JobRequirement.

        """

        try:
            job_requirement = JobRequirement.objects.get(pk=job_requirement_id)
        except JobRequirement.DoesNotExist:
            raise ResourceNotFoundError(
                resource=f"Job Requirement {job_requirement_id}"
            )
        except ValidationError as e:
            raise InfraStructureViolationError(e) from e

        if job_requirement.user != user:
            raise AccessDeniedError(
                resource=f"Job Requirement {job_requirement_id}",
                message=f"Job Requirement {job_requirement_id} does not belong to"
                        f" {user}"
            )

        return job_requirement

    @staticmethod
    def list(user: User) -> QuerySet[JobRequirement]:
        """
        Retrieve a queryset of JobRequirements from the JobRequirements database.

        Args:
            user (User):
                User who owns the JobRequirements.

        Returns:
            QuerySet[JobRequirement]:
                - All JobRequirements belonging to this user from the database.
        """

        return JobRequirement.objects.filter(user=user)
