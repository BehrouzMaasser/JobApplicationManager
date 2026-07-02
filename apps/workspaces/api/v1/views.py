"""
REST API views for managing workspaces.
"""

# Custom DRF Views
from apps.core.common.api.viewsets import BaseIdServiceViewSet

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

class WorkspaceViewSet(BaseIdServiceViewSet):
    """
    Expose CRUD endpoints for Workspace resources.

    Read operations are delegated to selectors and write operations to services.
    """

    # URL Path:
    # workspaces/{id}

    selector_class = WorkspaceSelector
    service_class = WorkspaceService

    service_lookup_id = 'workspace_id'
    selector_lookup_field = "workspace_id"
    lookup_url_kwarg = 'id'

    read_serializer_class = DisplayWorkspaceSerializer
    write_serializer_class = WorkspaceSerializer

    def get_queryset(self):
        """Return workspaces accessible to the authenticated user."""

        return self.selector.list(user=self.request.user)
