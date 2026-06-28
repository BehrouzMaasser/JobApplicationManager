"""
REST API serializers for the Workspace domain.
"""

from rest_framework import serializers

# Models
from apps.workspaces.models import Workspace


# Serializers
class WorkspaceSerializer(serializers.ModelSerializer):
    """
    Serialize workspace data for API requests and responses.
    """

    class Meta:

        model = Workspace

        fields = [
            "id",
            "owner",
            "workspace_id",
            "name",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "owner": {"read_only": True},
            "workspace_id": {"read_only": True},
            "name": {"required": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class DisplayWorkspaceSerializer(WorkspaceSerializer):

    class Meta(WorkspaceSerializer.Meta):

        read_only_fields = WorkspaceSerializer.Meta.fields
