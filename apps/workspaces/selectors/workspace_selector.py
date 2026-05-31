from dataclasses import dataclass

from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.workspaces.models import Workspace


class WorkspaceSelector:

    @dataclass
    class QueryFilter:
        workspace_id: str | None = None

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
