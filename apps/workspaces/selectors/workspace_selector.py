from dataclasses import dataclass
from uuid import UUID

from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.workspaces.models import Workspace

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    InfraStructureViolationError,
    AccessDeniedError
)


class WorkspaceSelector:

    @dataclass
    class QueryFilter:
        workspace_id: str | None = None

    @staticmethod
    def get(user: User, workspace_id: UUID) -> Workspace | Exception:

        try:
            workspace = Workspace.objects.get(workspace_id=workspace_id)
        except Workspace.DoesNotExist:
            raise ResourceNotFoundError(f"Workspace {workspace_id} does not exist")
        except Exception as e:
            raise InfraStructureViolationError(str(e))

        if workspace.owner != user:
            raise AccessDeniedError(
                f"Workspace {workspace_id} does not belong to {user}"
            )

        return workspace

    @staticmethod
    def list(
            *, user: User, filters: QueryFilter | None = None
    ) -> QuerySet[Workspace]:

        queryset = Workspace.objects.filter(owner=user)

        if not filters:
            return queryset

        if filters.workspace_id:
            queryset = queryset.filter(workspace_id=filters.workspace_id)

        return queryset
