from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.workspaces.models import Workspace


class WorkspaceSelector:

    @staticmethod
    def list(*, user: User) -> QuerySet[Workspace]:

        return Workspace.objects.filter(owner=user)
