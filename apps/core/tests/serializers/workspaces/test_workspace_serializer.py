from apps.workspaces.api.v1.serializers import (
    WorkspaceSerializer,
    DisplayWorkspaceSerializer,
)


class TestWorkspaceSerializerValidation:

    def test_accepts_valid_data(self):

        serializer = WorkspaceSerializer(
            data={"name": "Backend Tracker"}
        )

        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data["name"] == "Backend Tracker"

    def test_name_is_required(self):

        serializer = WorkspaceSerializer(data={})

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_name_cannot_be_blank(self):

        serializer = WorkspaceSerializer(
            data={"name": ""}
        )

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_name_cannot_exceed_max_length(self):

        serializer = WorkspaceSerializer(
            data={
                "name": "a" * 256
            }
        )

        assert not serializer.is_valid()
        assert "name" in serializer.errors


class TestWorkspaceSerializerReadOnlyFields:

    def test_ignores_read_only_fields(self):

        serializer = WorkspaceSerializer(
            data={
                "id": 10,
                "owner": 50,
                "workspace_id": "fake",
                "created_at": "2026-01-01",
                "updated_at": "2026-01-01",
                "name": "Workspace",
            }
        )

        assert serializer.is_valid(), serializer.errors

        assert serializer.validated_data == {
            "name": "Workspace",
        }


class TestDisplayWorkspaceSerializer:

    def test_input_fields_are_ignored(self):

        serializer = DisplayWorkspaceSerializer(
            data={
                "name": "Ignored",
                "workspace_id": "abc",
            }
        )

        assert serializer.is_valid()
        assert serializer.validated_data == {}

    def test_serializes_workspace(self, workspace1_user1):

        serializer = DisplayWorkspaceSerializer(
            instance=workspace1_user1
        )

        assert serializer.data["id"] == workspace1_user1.id
        assert serializer.data["workspace_id"] == str(workspace1_user1.workspace_id)
        assert serializer.data["name"] == workspace1_user1.name
