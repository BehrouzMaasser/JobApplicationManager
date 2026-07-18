"""
Service layer for CompanyNote domain logic.

This module handles creation, update, and deletion of notes associated
with a company, ensuring workspace and company-level ownership validation.
"""

from typing import Any

from apps.accounts.models import User
# Models
from apps.companies.models import CompanyNote

# Selectors
from apps.companies.selectors.company_note_selector import CompanyNoteSelector

# Services
from apps.companies.services.company_service import CompanyService

# Contexts
from apps.core.common.contexts.base_context import (
    CompanyChildContext,
    CompanyContext
)
from apps.core.common.services.base_service import BaseService

# Exceptions
from apps.core.exceptions.exceptions import DomainInvariantViolationError


# Company Note Service
class CompanyNoteService(BaseService[CompanyNote]):
    """
    Service responsible for managing CompanyNote domain operations.

    Ensures that notes are always accessed within the correct company
    and workspace boundaries.
    """

    MODEL = CompanyNote
    SELECTOR = CompanyNoteSelector

    CREATE_FIELDS = ("company", "title", "content")
    SCALAR_UPDATABLE_FIELDS = ("title", "content")
    M2M_UPDATABLE_FIELDS = ()
    REQUIRED_M2M_FIELDS = ()
    NON_EMPTY_M2M_FIELDS = ()
    M2M_OWNER_FIELD_MAP = {}

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
        instance: CompanyNote,
        context: CompanyChildContext
    ) -> None:

        if instance.company.pk != context.company_id:
            raise DomainInvariantViolationError(
                f"Company Note {context.id} does not belong to Company "
                f"{context.company_id}"
            )

        if instance.company.workspace.workspace_id != context.workspace_id:
            raise DomainInvariantViolationError(
                f"Company Note {context.id}'s company {context.company_id} does not"
                f" belong to Workspace {context.workspace_id}"
            )
