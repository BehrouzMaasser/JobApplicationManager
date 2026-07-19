"""
Business services for managing workspaces.

Contains operations responsible for creating, updating, and deleting
workspace instances while enforcing business rules.
"""

# Imports for typings
from typing import Any

from apps.accounts.models import User
from apps.core.common.contexts.contexts import WorkspaceContext
# Models
from apps.workspaces.models import Workspace

# Selectors
from apps.workspaces.selectors.workspace_selector import WorkspaceSelector

# Services
from apps.core.common.services.base_service import BaseService


# Workspace Service
class WorkspaceService(BaseService[Workspace]):
    """
    Implements business operations for the Workspace domain.
    All persistence and business-rule validation related to workspaces
    should be performed through this service.
    """

    MODEL = Workspace
    SELECTOR = WorkspaceSelector

    CREATE_FIELDS = ("owner", "name")
    SCALAR_UPDATABLE_FIELDS = ("name", )
    M2M_UPDATABLE_FIELDS = ()
    REQUIRED_M2M_FIELDS = ()
    NON_EMPTY_M2M_FIELDS = ()
    M2M_OWNER_FIELD_MAP = {}

    @classmethod
    def _resolve_create_dependencies(
            cls,
            user: User,
            context: WorkspaceContext
    ) -> dict[str, Any]:

        return {"owner": user}

    @classmethod
    def _validate_resolved_instance(
        cls,
        *,
        instance: Workspace,
        context: WorkspaceContext
    ) -> None:
        """Workspace is the aggregate root; no additional validation required."""

        pass
