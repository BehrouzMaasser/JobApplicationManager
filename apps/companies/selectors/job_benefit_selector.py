"""
Read-only query helpers for the JobBenefit domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import JobBenefit

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError
)


class JobBenefitSelector:
    """
    Provides reusable read operations for JobBenefit objects.
    """

    @staticmethod
    def get(*, user: User, job_benefit_id: int) -> JobBenefit | Exception:
        """
        Retrieve a JobBenefit from the JobBenefits database.

        Returns:
            JobBenefit:
                JobBenefit of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the JobBenefit does not exist.

            AccessDeniedError:
                If the JobBenefit does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                JobBenefit.

        """

        try:
            job_benefit = JobBenefit.objects.get(pk=job_benefit_id)
        except JobBenefit.DoesNotExist:
            raise ResourceNotFoundError(resource=f"Job Benefit {job_benefit_id}")
        except ValidationError as e:
            raise InfraStructureViolationError(e) from e

        if job_benefit.user != user:
            raise AccessDeniedError(
                resource=f"Job Benefit {job_benefit_id}",
                message=f"Job Benefit {job_benefit_id} does not belong to {user}"
            )

        return job_benefit

    @staticmethod
    def list(user: User) -> QuerySet[JobBenefit]:
        """
        Retrieve a queryset of JobBenefits from the JobBenefit database.

        Args:
            user (User):
                User who owns the JobBenefits.

        Returns:
            QuerySet[JobBenefit]:
                - All JobBenefits belonging to this user from the database.
        """

        return JobBenefit.objects.filter(user=user)
