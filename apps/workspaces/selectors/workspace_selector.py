"""
Read-only query helpers for the Workspace domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from django.db.models import QuerySet

# Models
from apps.workspaces.models import Workspace

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector

# Filters for typing
from apps.core.common.types.filters import WorkspaceQueryFilter


class WorkspaceSelector(BaseSelector[Workspace]):
    """
    Selector responsible for retrieving Workspace objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = Workspace
    RESOURCE_NAME = "Workspace"
    LOOKUP_FIELD = "workspace_id"
    OWNER_PATH = "owner"

    @classmethod
    def apply_filters(
            cls,
            queryset: QuerySet[Workspace],
            filters: WorkspaceQueryFilter
    ) -> QuerySet[Workspace]:

        if filters.workspace_id:
            queryset = queryset.filter(workspace_id=filters.workspace_id)

        return queryset
