"""
Service layer for JobBenefit domain logic.

This module handles creation, update, and deletion of job benefit records
associated with a user while enforcing user-level ownership rules.
"""

from typing import Any

from apps.accounts.models import User
# Models
from apps.companies.models import JobBenefit

# Selectors
from apps.companies.selectors.job_benefit_selector import JobBenefitSelector
from apps.core.common.contexts.base_context import JobBenefitContext

# Services
from apps.core.common.services.base_service import BaseService


# Job Benefit Service
class JobBenefitService(BaseService):
    """
    Service responsible for managing JobBenefit domain operations.

    Ensures strict user ownership validation for all operations.
    """

    MODEL = JobBenefit
    SELECTOR = JobBenefitSelector

    CREATE_FIELDS = ("user", "name", "description")
    SCALAR_UPDATABLE_FIELDS = ("name", "description")
    M2M_UPDATABLE_FIELDS = ()
    REQUIRED_M2M_FIELDS = ()
    NON_EMPTY_M2M_FIELDS = ()
    M2M_OWNER_FIELD_MAP = {}

    @classmethod
    def _resolve_create_dependencies(
            cls,
            user: User,
            context: JobBenefitContext
    ) -> dict[str, Any]:

        return {"user": user}

    @classmethod
    def _validate_resolved_instance(
        cls,
        *,
        instance: JobBenefit,
        context: JobBenefitContext
    ) -> None:
        """Job Benefit is the aggregate root; no additional validation required."""

        pass
