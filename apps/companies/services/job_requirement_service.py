"""
Service layer for JobRequirement domain logic.

This module handles creation, update, and deletion of job requirement records
associated with a user while enforcing user-level ownership rules.
"""

from typing import Any
from django.db import transaction

# Models
from apps.accounts.models import User
from apps.companies.models import JobRequirement

# Selectors
from apps.companies.selectors.job_requirement_selector import JobRequirementSelector

# Services
from apps.workspaces.services.base_service import BaseService


# Job Requirement Service
class JobRequirementService(BaseService):
    """
    Service responsible for managing JobRequirement domain operations.

    Ensures strict user ownership validation for all operations.
    """

    CREATE_REQUIRED_FIELDS = {
        "title",
        "description"
    }

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(*, user: User, validated_data: dict[str, Any]) -> JobRequirement:
        """
        Create a new JobRequirement under a user.

        Calls:
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ValidationError:
                If model validation fails.

        Returns:
            JobRequirement:
                The created job requirement instance.
        """

        instance = JobRequirement(
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
            job_requirement_id: int,
            validated_data: dict[str, Any]
    ) -> JobRequirement:
        """
        Update an existing JobRequirement instance.

        Calls:
            _resolve_job_requirement() to retrieve the target instance.
            _update_non_m2m_fields() to apply updates.
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ResourceNotFoundError:
                If the JobRequirement does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            ValidationError:
                If model validation fails.

        Returns:
            JobRequirement:
                The updated job requirement instance.
        """

        # Domain Correctness Validation:

        instance = JobRequirementService._resolve_job_requirement(
            user=user, job_requirement_id=job_requirement_id
        )

        # ----------------------*****---------------------

        # Applying changes:
        JobRequirementService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobRequirementService.UPDATABLE_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        return instance

    @staticmethod
    def remove(*, user: User, job_requirement_id: int) -> None:
        """
        Delete a JobRequirement instance.

        Calls:
            _resolve_job_requirement() to retrieve the target instance.
            django.db.models.base.Model.delete()

        Raises:
            ResourceNotFoundError:
                If the JobRequirement does not exist.

            AccessDeniedError:
                If the user does not own the resource.

        Returns:
            None
        """

        # Domain Correctness Validation:

        instance = JobRequirementService._resolve_job_requirement(
            user=user, job_requirement_id=job_requirement_id
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_job_requirement(
            *, user: User, job_requirement_id: int
    ) -> JobRequirement:
        """
        Resolve a JobRequirement and validate user ownership.

        Calls:
            JobRequirementSelector.get()

        Raises:
            ResourceNotFoundError:
                If the JobRequirement does not exist.

            AccessDeniedError:
                If the user does not own the resource.

        Returns:
            JobRequirement:
                The resolved job requirement instance.
        """

        return JobRequirementSelector.get(
            user=user, job_requirement_id=job_requirement_id
        )
