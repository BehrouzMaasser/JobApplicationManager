"""
Read-only query helpers for the Workspace domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from dataclasses import dataclass
from uuid import UUID

from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.workspaces.models import Workspace

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError
)


class WorkspaceSelector:
    """
    Provides reusable read operations for Workspace objects.
    """

    @dataclass
    class QueryFilter:
        workspace_id: str | None = None

    @staticmethod
    def get(user: User, workspace_id: UUID) -> Workspace | Exception:
        """
        Retrieve a Workspace from the Workspaces database.

        Returns:
            Workspace:
                Workspace of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the Workspace does not exist.

            AccessDeniedError:
                If the Workspace does not belong to this user.

        """

        try:
            workspace = Workspace.objects.get(workspace_id=workspace_id)
        except Workspace.DoesNotExist:
            raise ResourceNotFoundError(resource=f"Workspace {workspace_id}")

        if workspace.owner != user:
            raise AccessDeniedError(
                resource=f"Workspace {workspace_id}",
                message=f"Workspace {workspace_id} does not belong to {user}"
            )

        return workspace

    @staticmethod
    def list(
            *, user: User, filters: QueryFilter | None = None
    ) -> QuerySet[Workspace]:
        """
        Retrieve a list of Workspaces from the Workspaces database.

        Args:
            user (User):
                User who owns the Workspaces.

            filters (QueryFilter | None = None):
                Query filters applied to the Workspaces.
        """

        queryset = Workspace.objects.filter(owner=user)

        if not filters:
            return queryset

        if filters.workspace_id:
            queryset = queryset.filter(workspace_id=filters.workspace_id)

        return queryset
