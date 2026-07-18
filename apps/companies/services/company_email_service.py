"""
Service layer for CompanyEmail domain logic.

This module handles creation, update, and deletion of email records
associated with a company while enforcing workspace and company-level
ownership rules.
"""

from typing import Any

from apps.accounts.models import User
# Models
from apps.companies.models import CompanyEmail
from apps.core.common.contexts.base_context import CompanyChildContext

# Services
from apps.core.common.services.base_service import BaseService
from apps.companies.services.company_service import CompanyService

# Selectors
from apps.companies.selectors.company_email_selector import CompanyEmailSelector

# Contexts
from apps.core.common.contexts.base_context import CompanyContext

# Exceptions
from apps.core.exceptions.exceptions import DomainInvariantViolationError


# Company Email Service
class CompanyEmailService(BaseService[CompanyEmail]):
    """
    Service responsible for managing CompanyEmail domain operations.

    Ensures strict workspace and company ownership validation for all operations.
    """

    MODEL = CompanyEmail
    SELECTOR = CompanyEmailSelector

    CREATE_FIELDS = ("company", "title", "email")
    SCALAR_UPDATABLE_FIELDS = ("title", "email")
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
        instance: CompanyEmail,
        context: CompanyChildContext
    ) -> None:

        if instance.company_id != context.company_id:
            raise DomainInvariantViolationError(
                f"CompanyEmail {context.id} does not belong to "
                f"Company {context.company_id}"
            )

        if instance.company.workspace.workspace_id != context.workspace_id:
            raise DomainInvariantViolationError(
                f"CompanyEmail {context.id}'s company {context.company_id} does not"
                f" belong to Workspace {context.workspace_id}"
            )
