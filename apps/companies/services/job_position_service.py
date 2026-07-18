"""
Service layer for JobPosition domain logic.

This module handles creation, update, and deletion of job position records
associated with a company while enforcing workspace and company-level
ownership rules.
"""

from typing import Any

# Models
from apps.accounts.models import User
from apps.companies.models import JobPosition

# Selectors
from apps.companies.selectors.job_position_selector import JobPositionSelector

# Services
from apps.companies.services.company_service import CompanyService

# Contexts
from apps.core.common.contexts.base_context import (
    CompanyChildContext,
    CompanyContext,
)
from apps.core.common.services.base_service import BaseService

# Exceptions
from apps.core.exceptions.exceptions import (
    BusinessRuleViolationError,
    DomainInvariantViolationError
)


# Job Position Service
class JobPositionService(BaseService[JobPosition]):
    """
    Service responsible for managing JobPosition domain operations.

    Ensures strict workspace and company ownership validation for all operations.
    """

    MODEL = JobPosition
    SELECTOR = JobPositionSelector

    CREATE_FIELDS = (
        "company",
        "title",
        "date_posted",
        "description",
        "min_salary",
        "max_salary",
        "job_position_ad_url",
        "job_location_url",
        "job_portal_url",
        "portal_username",
        "portal_password",
    )
    SCALAR_UPDATABLE_FIELDS = (
        "title",
        "date_posted",
        "description",
        "min_salary",
        "max_salary",
        "job_position_ad_url",
        "job_location_url",
        "job_portal_url",
        "portal_username",
        "portal_password",

    )
    REQUIRED_M2M_FIELDS = (
        "employment_types",
        "job_sites",
        "tasks",
        "requirements",
    )
    M2M_UPDATABLE_FIELDS = (
        "benefits",
        "employment_types",
        "job_sites",
        "tasks",
        "requirements",
    )
    NON_EMPTY_M2M_FIELDS = REQUIRED_M2M_FIELDS
    M2M_OWNER_FIELD_MAP = {
        "tasks": "user",
        "requirements": "user",
        "benefits": "user",
    }

    @classmethod
    def _update_validate(
            cls,
            *,
            user: User,
            instance: JobPosition,
            validated_data: dict[str, Any],
    ):

        cls._validate_date_posted(instance, validated_data)

    @classmethod
    def _resolve_create_dependencies(
            cls,
            user: User,
            context: CompanyChildContext
    ) -> dict[str, Any]:

        company = CompanyService._resolve_instance(
            user=user,
            context=CompanyContext(
                id=context.company_id,
                workspace_id=context.workspace_id,
            ),
        )

        return {"company": company}

    @classmethod
    def _validate_resolved_instance(
        cls,
        *,
        instance: JobPosition,
        context: CompanyChildContext
    ) -> None:

        if instance.company.pk != context.company_id:
            raise DomainInvariantViolationError(
                f"Job position {context.id} don't belong to Company"
                f" {context.company_id}"
            )

        if instance.company.workspace.workspace_id != context.workspace_id:
            print(instance.company.workspace.workspace_id)
            print(context.workspace_id)
            raise DomainInvariantViolationError(
                f"Workspace of Job position {context.id} don't match the given"
                f" workspace_id = {context.workspace_id}"
            )

    @staticmethod
    def _validate_date_posted(
            instance: JobPosition,
            validated_data: dict[str, Any]
    ) -> None:

        if date_posted := validated_data.get("date_posted"):
            for job_application in instance.job_applications.all():
                if (job_application.date_applied and
                        (job_application.date_applied < date_posted)):
                    raise BusinessRuleViolationError(
                        fields=["date_posted"],
                        messages=[
                            "Date posted cannot be after the job application's "
                            "date applied"
                        ]
                    )
