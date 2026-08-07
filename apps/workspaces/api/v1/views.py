"""
REST API views for managing workspaces.
"""

# Custom DRF Views
from apps.core.common.api.viewsets import BaseContextServiceViewSet
from apps.core.common.contexts.contexts import EmptyContext, WorkspaceContext

# Serializers
from apps.workspaces.api.v1.serializers import (
    DisplayWorkspaceSerializer,
    WorkspaceSerializer,
)

# Selectors
from apps.workspaces.selectors.workspace_selector import WorkspaceSelector

# Services
from apps.workspaces.services.workspace_service import WorkspaceService


# ViewSets

class WorkspaceViewSet(BaseContextServiceViewSet):
    """
    Expose CRUD endpoints for Workspace resources.

    Read operations are delegated to selectors and write operations to services.
    """

    # URL Path:
    # workspaces/{id}

    selector_class = WorkspaceSelector
    service_class = WorkspaceService

    lookup_url_kwarg = 'id'

    read_serializer_class = DisplayWorkspaceSerializer
    write_serializer_class = WorkspaceSerializer

    def get_create_context(self) -> EmptyContext:
        """
        Context used when creating a workspace.
        """

        return EmptyContext()

    def get_update_context(self) -> WorkspaceContext:
        """
        Context used when updating/deleting a workspace.
        """

        return WorkspaceContext(
            id=self.kwargs['id'],
        )

    def get_queryset(self):
        """Return workspaces accessible to the authenticated user."""

        return self.selector.list(user=self.request.user)
