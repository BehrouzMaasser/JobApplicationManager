from rest_framework.permissions import BasePermission


class IsWorkspaceOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        if hasattr(obj, "workspace"):
            return obj.workspace.owner == request.user

        return False
