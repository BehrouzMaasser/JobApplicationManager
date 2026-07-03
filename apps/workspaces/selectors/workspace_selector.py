"""
Read-only query helpers for the Workspace domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.workspaces.models import Workspace

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError
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

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving the
                Workspace.

        """

        try:
            workspace = Workspace.objects.get(workspace_id=workspace_id)
        except Workspace.DoesNotExist:
            raise ResourceNotFoundError(resource=f"Workspace {workspace_id}")
        except ValidationError as e:
            raise InfraStructureViolationError(e) from e

        if workspace.owner != user:
            raise AccessDeniedError(
                resource=f"Workspace {workspace_id}",
                message=f"Workspace {workspace_id} does not belong to {user}"
            )

        return workspace

    @staticmethod
    def list(
            *,
            user: User,
            filters: QueryFilter | None = None
    ) -> QuerySet[Workspace]:
        """
        Retrieve a queryset of Workspaces from the Workspaces database.

        Args:
            user (User):
                User who owns the Workspaces.

            filters (QueryFilter | None = None):
                Query filters applied to the Workspaces.

        Returns:
            QuerySet[Workspace]:
                - A queryset of the Workspaces owned by the user based on
                filters provided.
                - An Empty queryset if user owned no workspaces and nothing matches
                the filters provided.
        """

        queryset = Workspace.objects.filter(owner=user)

        if not filters:
            return queryset

        if filters.workspace_id:
            queryset = queryset.filter(workspace_id=filters.workspace_id)

        return queryset
