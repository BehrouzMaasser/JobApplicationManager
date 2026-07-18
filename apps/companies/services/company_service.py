"""
Service layer for Company domain logic.

This module contains all business operations related to Company entities,
including creation, update, and deletion, while enforcing workspace-level
invariants and validation rules.
"""

from typing import Any

from apps.accounts.models import User
# Models
from apps.companies.models import Company
from apps.core.common.contexts.base_context import WorkspaceContext, CompanyContext
from apps.core.common.services.base_service import BaseService

# Exceptions
from apps.core.exceptions.exceptions import DomainInvariantViolationError

# Parent Service
from apps.workspaces.services.workspace_service import WorkspaceService

# Selectors
from apps.companies.selectors.company_selector import CompanySelector


# Company Service
class CompanyService(BaseService[Company]):
    """
    Service responsible for handling Company domain operations.

    This service enforces workspace boundaries and delegates retrieval
    logic to selectors while ensuring validation consistency.
    """

    MODEL = Company
    SELECTOR = CompanySelector

    CREATE_FIELDS = ("workspace", "name", "website")
    SCALAR_UPDATABLE_FIELDS = ("name", "website")
    M2M_UPDATABLE_FIELDS = ()
    REQUIRED_M2M_FIELDS = ()
    NON_EMPTY_M2M_FIELDS = ()
    M2M_OWNER_FIELD_MAP = {}

    @classmethod
    def _resolve_create_dependencies(
            cls,
            user: User,
            context: CompanyContext
    ) -> dict[str, Any]:

        workspace = WorkspaceService._resolve_instance(
            user=user,
            context=WorkspaceContext(id=context.workspace_id)
        )

        return {"workspace": workspace}

    @classmethod
    def _validate_resolved_instance(
        cls,
        *,
        instance: Company,
        context: CompanyContext
    ) -> None:

        if instance.workspace.workspace_id != context.workspace_id:
            raise DomainInvariantViolationError(
                f"Company {instance.pk} does not belong to Workspace"
                f" {context.workspace_id}"
            )
