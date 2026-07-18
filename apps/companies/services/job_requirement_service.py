"""
Service layer for JobRequirement domain logic.

This module handles creation, update, and deletion of job requirement records
associated with a user while enforcing user-level ownership rules.
"""

from typing import Any

from apps.accounts.models import User
# Models
from apps.companies.models import JobRequirement

# Selectors
from apps.companies.selectors.job_requirement_selector import JobRequirementSelector
from apps.core.common.contexts.base_context import JobRequirementContext

# Services
from apps.core.common.services.base_service import BaseService


# Job Requirement Service
class JobRequirementService(BaseService[JobRequirement]):
    """
    Service responsible for managing JobRequirement domain operations.

    Ensures strict user ownership validation for all operations.
    """

    MODEL = JobRequirement
    SELECTOR = JobRequirementSelector

    CREATE_FIELDS = ("user", "title", "description")
    SCALAR_UPDATABLE_FIELDS = ("title", "description")
    M2M_UPDATABLE_FIELDS = ()
    REQUIRED_M2M_FIELDS = ()
    NON_EMPTY_M2M_FIELDS = ()
    M2M_OWNER_FIELD_MAP = {}

    @classmethod
    def _resolve_create_dependencies(
            cls,
            user: User,
            context: JobRequirementContext
    ) -> dict[str, Any]:

        return {"user": user}

    @classmethod
    def _validate_resolved_instance(
        cls,
        *,
        instance: JobRequirement,
        context: JobRequirementContext
    ) -> None:
        """
        Job Requirement is the aggregate root; no additional validation required.
        """

        pass
