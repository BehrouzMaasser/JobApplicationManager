"""
Service layer for JobApplicationNote domain logic.

This module handles creation, update, and deletion of job application
notes while enforcing workspace, company, job position, and job
application ownership rules.
"""

from typing import Any

# Models
from apps.accounts.models import User
from apps.applications.models import JobApplicationNote

# Selectors
from apps.applications.selectors.application_note_selector import (
    JobApplicationNoteSelector,
)

# Services
from apps.core.common.services.base_service import BaseService
from apps.applications.services.application_service import (
    JobApplicationService,
)

# Contexts
from apps.core.common.contexts.contexts import (
    JobApplicationChildContext,
    JobApplicationContext,
)

# Exceptions
from apps.core.exceptions.exceptions import (
    DomainInvariantViolationError,
)


# Job Application Note Service
class JobApplicationNoteService(BaseService[JobApplicationNote]):
    """
    Service responsible for managing JobApplicationNote domain operations.

    Ensures strict workspace, company, job position, and job application
    ownership validation for all operations.
    """

    MODEL = JobApplicationNote
    SELECTOR = JobApplicationNoteSelector

    CREATE_FIELDS = ("job_application", "title", "content")
    SCALAR_UPDATABLE_FIELDS = ("title", "content")
    M2M_UPDATABLE_FIELDS = ()
    REQUIRED_M2M_FIELDS = ()
    NON_EMPTY_M2M_FIELDS = ()
    M2M_OWNER_FIELD_MAP = {}

    @classmethod
    def _resolve_create_dependencies(
            cls,
            user: User,
            context: JobApplicationChildContext,
    ) -> dict[str, Any]:

        job_application = JobApplicationService._resolve_instance(
            user=user,
            context=JobApplicationContext(
                id=context.job_application_id,
                workspace_id=context.workspace_id,
                company_id=context.company_id,
                job_position_id=context.job_position_id,
            ),
        )

        return {"job_application": job_application}

    @classmethod
    def _validate_resolved_instance(
        cls,
        *,
        instance: JobApplicationNote,
        context: JobApplicationChildContext,
    ) -> None:

        if instance.job_application.pk != context.job_application_id:
            raise DomainInvariantViolationError(
                f"JobApplicationNote {context.id} does not belong to "
                f"JobApplication {context.job_application_id}"
            )

        if (
                instance.job_application.job_position.pk
                != context.job_position_id
        ):
            raise DomainInvariantViolationError(
                f"JobApplicationNote {context.id}'s JobApplication "
                f"{context.job_application_id} does not belong to "
                f"JobPosition {context.job_position_id}"
            )

        if (
                instance.job_application.job_position.company.pk
                != context.company_id
        ):
            raise DomainInvariantViolationError(
                f"JobApplicationNote {context.id}'s JobPosition "
                f"{context.job_position_id} does not belong to "
                f"Company {context.company_id}"
            )

        if (
                instance.job_application.workspace.workspace_id
                != context.workspace_id
        ):
            raise DomainInvariantViolationError(
                f"JobApplicationNote {context.id}'s workspace does not belong "
                f"to Workspace {context.workspace_id}"
            )
