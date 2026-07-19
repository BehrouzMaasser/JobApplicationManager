"""
Service layer for JobTask domain logic.

This module handles creation, update, and deletion of job task records
associated with a user while enforcing user-level ownership rules.
"""

from typing import Any

# Models
from apps.accounts.models import User
from apps.companies.models import JobTask

# Selectors
from apps.companies.selectors.job_task_selector import JobTaskSelector
from apps.core.common.contexts.contexts import JobTaskContext

# Services
from apps.core.common.services.base_service import BaseService


# Job Task Service
class JobTaskService(BaseService[JobTask]):
    """
    Service responsible for managing JobTask domain operations.

    Ensures strict user ownership validation for all operations.
    """

    MODEL = JobTask
    SELECTOR = JobTaskSelector

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
            context: JobTaskContext
    ) -> dict[str, Any]:

        return {"user": user}

    @classmethod
    def _validate_resolved_instance(
        cls,
        *,
        instance: JobTask,
        context: JobTaskContext
    ) -> None:
        """Job Task is the aggregate root; no additional validation required."""

        pass
