"""
Read-only query helpers for the JobTask domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import JobTask

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError
)


class JobTaskSelector:
    """
    Provides reusable read operations for JobTask objects.
    """

    @staticmethod
    def get(*, user: User, job_task_id: int) -> JobTask | Exception:
        """
        Retrieve a JobTask from the JobTasks database.

        Returns:
            JobTask:
                JobTask of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the JobTask does not exist.

            AccessDeniedError:
                If the JobTask does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                JobTask.

        """

        try:
            job_task = JobTask.objects.get(pk=job_task_id)
        except JobTask.DoesNotExist:
            raise ResourceNotFoundError(resource=f"Job Task {job_task_id}")
        except ValidationError as e:
            raise InfraStructureViolationError(e) from e

        if job_task.user != user:
            raise AccessDeniedError(
                resource=f"Job Task {job_task_id}",
                message=f"Job Task {job_task_id} does not belong to {user}"
            )

        return job_task

    @staticmethod
    def list(user: User) -> QuerySet[JobTask]:
        """
        Retrieve a queryset of JobTasks from the JobTasks database.

        Args:
            user (User):
                User who owns the JobTasks.

        Returns:
            QuerySet[JobTask]:
                - All JobTasks belonging to this user from the database.
        """

        return JobTask.objects.filter(user=user)
