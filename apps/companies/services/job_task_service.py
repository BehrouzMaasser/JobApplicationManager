"""
Service layer for JobTask domain logic.

This module handles creation, update, and deletion of job task records
associated with a user while enforcing user-level ownership rules.
"""

from typing import Any
from django.db import transaction

# Models
from apps.accounts.models import User
from apps.companies.models import JobTask

# Selectors
from apps.companies.selectors.job_task_selector import JobTaskSelector

# Services
from apps.workspaces.services.base_service import BaseService


# Job Task Service
class JobTaskService(BaseService):
    """
    Service responsible for managing JobTask domain operations.

    Ensures strict user ownership validation for all operations.
    """

    CREATE_REQUIRED_FIELDS = {"title", "description"}

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(*, user: User, validated_data: dict[str, Any]) -> JobTask:
        """
        Create a new JobTask under a user.

        Calls:
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ValidationError:
                If model validation fails.

        Returns:
            JobTask:
                The created job task instance.
        """

        instance = JobTask(
            user=user,
            title=validated_data.get("title"),
            description=validated_data.get("description")
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def update(
            *,
            user: User,
            job_task_id: int,
            validated_data: dict[str, Any]
    ) -> JobTask:
        """
        Update an existing JobTask instance.

        Calls:
            _resolve_job_task() to retrieve the target instance.
            _update_non_m2m_fields() to apply updates.
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ResourceNotFoundError:
                If the JobTask does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            ValidationError:
                If model validation fails.

        Returns:
            JobTask:
                The updated job task instance.
        """

        # Domain Correctness Validation:

        instance = JobTaskService._resolve_job_task(
            user=user, job_task_id=job_task_id
        )

        # ----------------------*****---------------------

        # Applying changes:
        JobTaskService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobTaskService.UPDATABLE_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        return instance

    @staticmethod
    def remove(*, user: User, job_task_id: int) -> None:
        """
        Delete a JobTask instance.

        Calls:
            _resolve_job_task() to retrieve the target instance.
            django.db.models.base.Model.delete()

        Raises:
            ResourceNotFoundError:
                If the JobTask does not exist.

            AccessDeniedError:
                If the user does not own the resource.

        Returns:
            None
        """

        # Domain Correctness Validation:

        instance = JobTaskService._resolve_job_task(
            user=user, job_task_id=job_task_id
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_job_task(*, user: User, job_task_id: int) -> JobTask:
        """
        Resolve a JobTask and validate user ownership.

        Calls:
            JobTaskSelector.get()

        Raises:
            ResourceNotFoundError:
                If the JobTask does not exist.

            AccessDeniedError:
                If the user does not own the resource.

        Returns:
            JobTask:
                The resolved job task instance.
        """

        return JobTaskSelector.get(user=user, job_task_id=job_task_id)
