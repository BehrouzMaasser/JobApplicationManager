from apps.workspaces.api.serializers import (
    WorkspaceSerializer,
    DisplayWorkspaceSerializer,
)


class TestWorkspaceSerializer:

    def test_valid_data(self):

        data = {
            "name": "Backend Job Tracker",
        }

        serializer = WorkspaceSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_requires_name(self):

        serializer = WorkspaceSerializer(data={})

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_rejects_blank_name(self):

        serializer = WorkspaceSerializer(data={
            "name": "",
        })

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_read_only_fields_are_ignored(self):

        data = {
            "name": "My Workspace",
            "id": 999,
            "owner": 999,
            "workspace_id": "fake-id",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
        }

        serializer = WorkspaceSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

        assert set(serializer.validated_data.keys()) == {"name"}

        assert "id" not in serializer.validated_data
        assert "owner" not in serializer.validated_data
        assert "workspace_id" not in serializer.validated_data
        assert "created_at" not in serializer.validated_data
        assert "updated_at" not in serializer.validated_data


class TestDisplayWorkspaceSerializer:

    def test_all_fields_are_read_only(self):

        data = {
            "name": "Should be ignored",
            "owner": 1,
            "workspace_id": "abc123",
        }

        serializer = DisplayWorkspaceSerializer(data=data)

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data == {}

    def test_serializes_workspace_instance(self, workspace_user1):

        serializer = DisplayWorkspaceSerializer(instance=workspace_user1)

        data = serializer.data

        assert data["id"] == workspace_user1.id
        assert data["name"] == workspace_user1.name
        assert data["workspace_id"] == str(workspace_user1.workspace_id)
