"""
Service layer for JobBenefit domain logic.

This module handles creation, update, and deletion of job benefit records
associated with a user while enforcing user-level ownership rules.
"""

from typing import Any
from django.db import transaction

# Models
from apps.accounts.models import User
from apps.companies.models import JobBenefit

# Selectors
from apps.companies.selectors.job_benefit_selector import JobBenefitSelector

# Services
from apps.workspaces.services.base_service import BaseService


# Job Benefit Service
class JobBenefitService(BaseService):
    """
    Service responsible for managing JobBenefit domain operations.

    Ensures strict user ownership validation for all operations.
    """

    CREATE_REQUIRED_FIELDS = {"name"}

    UPDATABLE_FIELDS = {
        *CREATE_REQUIRED_FIELDS,
        "description",
    }

    @staticmethod
    @transaction.atomic
    def create(*, user: User, validated_data: dict[str, Any]) -> JobBenefit:
        """
        Create a new JobBenefit under a user.

        Calls:
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ValidationError:
                If model validation fails.

        Returns:
            JobBenefit:
                The created job benefit instance.
        """

        instance = JobBenefit(
            user=user,
            name=validated_data.get("name"),
            description=validated_data.get("description"),
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
            job_benefit_id: int,
            validated_data: dict[str, Any]
    ) -> JobBenefit:
        """
        Update an existing JobBenefit instance.

        Calls:
            _resolve_job_benefit() to retrieve the target instance.
            _update_non_m2m_fields() to apply updates.
            django.db.models.base.Model.full_clean()
            django.db.models.base.Model.save()

        Raises:
            ResourceNotFoundError:
                If the JobBenefit does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            ValidationError:
                If model validation fails.

        Returns:
            JobBenefit:
                The updated job benefit instance.
        """

        # Domain Correctness Validation:

        instance = JobBenefitService._resolve_job_benefit(
            user=user,
            job_benefit_id=job_benefit_id
        )

        # ----------------------*****---------------------

        # Applying changes:
        JobBenefitService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobBenefitService.UPDATABLE_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        return instance

    @staticmethod
    def remove(*, user: User, job_benefit_id: int) -> JobBenefit:
        """
        Delete a JobBenefit instance.

        Calls:
            _resolve_job_benefit() to retrieve the target instance.
            django.db.models.base.Model.delete()

        Raises:
            ResourceNotFoundError:
                If the JobBenefit does not exist.

            AccessDeniedError:
                If the user does not own the resource.

        Returns:
            None
        """

        # Domain Correctness Validation:

        instance = JobBenefitService._resolve_job_benefit(
            user=user,
            job_benefit_id=job_benefit_id
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_job_benefit(*, user: User, job_benefit_id: int):
        """
        Resolve a JobBenefit and validate user ownership.

        Calls:
            JobBenefitSelector.get()

        Raises:
            ResourceNotFoundError:
                If the JobBenefit does not exist.

            AccessDeniedError:
                If the user does not own the resource.

        Returns:
            JobBenefit:
                The resolved job benefit instance.
        """

        return JobBenefitSelector.get(user=user, job_benefit_id=job_benefit_id)
