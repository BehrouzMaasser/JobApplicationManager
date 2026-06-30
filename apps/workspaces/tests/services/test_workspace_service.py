from unittest.mock import patch
from uuid import UUID

import pytest

# Django
from django.core.exceptions import ValidationError

# Exceptions
from apps.core.exceptions.exceptions import (
    AccessDeniedError,
    InfraStructureViolationError
)

# Models
from apps.workspaces.models import Workspace

# Services
from apps.workspaces.services.workspace_service import WorkspaceService


pytestmark = pytest.mark.django_db

#   ----------------------------------- ****** -----------------------------------


class TestWorkspaceServiceCreate:

    def test_create_successfully_returns_workspace(
            self, user1, workspace1_user1_valid_data
    ):

        workspace = WorkspaceService.create(
            user=user1, validated_data=workspace1_user1_valid_data
        )

        assert isinstance(workspace.workspace_id, UUID)
        assert workspace.name == workspace1_user1_valid_data["name"]
        assert workspace.owner == user1

    def test_create_successfully_creates_workspace_in_database(
            self, user1, workspace1_user1_valid_data
    ):

        workspace = WorkspaceService.create(
            user=user1, validated_data=workspace1_user1_valid_data
        )

        Workspace.objects.get(workspace_id=workspace.workspace_id)

    def test_create_raise_error_if_duplicate_workspace(
            self, user1, workspace1_user1_valid_data
    ):

        WorkspaceService.create(
            user=user1, validated_data=workspace1_user1_valid_data
        )

        with pytest.raises(ValidationError) as e:
            WorkspaceService.create(
                user=user1, validated_data=workspace1_user1_valid_data
            )

            assert e.error_dict["__all__"][0].code == "duplicate_workspace_name"

    def test_create_calls_full_clean(self, user1, workspace1_user1_valid_data):

        with patch("apps.workspaces.models.Workspace.full_clean") as mock_full_clean:
            WorkspaceService.create(
                user=user1, validated_data=workspace1_user1_valid_data
            )

            mock_full_clean.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


class TestWorkspaceServiceUpdate:

    def test_update_successfully_returns_updated_workspace(
        self, user1, workspace1_user1_updated_valid_data, workspace1_user1
    ):

        updated_workspace = WorkspaceService.update(
            user=user1,
            validated_data=workspace1_user1_updated_valid_data,
            workspace_id=workspace1_user1.workspace_id
        )

        assert updated_workspace.workspace_id == workspace1_user1.workspace_id
        assert updated_workspace.name == workspace1_user1_updated_valid_data["name"]
        assert updated_workspace.owner == user1

    def test_update_raise_error_if_name_already_exists(
        self, user1, workspace1_user1, workspace2_user1
    ):

        with pytest.raises(ValidationError) as e:
            WorkspaceService.update(
                user=user1,
                validated_data={"name": workspace1_user1.name},
                workspace_id=workspace2_user1.workspace_id
            )

            assert e.error_dict["__all__"][0].code == "duplicate_workspace_name"

    def test_update_successfully_updates_workspace_in_database(
        self, user1, workspace1_user1_updated_valid_data, workspace1_user1
    ):

        WorkspaceService.update(
            user=user1,
            validated_data=workspace1_user1_updated_valid_data,
            workspace_id=workspace1_user1.workspace_id
        )

        workspace1_user1.refresh_from_db()

        assert workspace1_user1.name == workspace1_user1_updated_valid_data["name"]
        assert workspace1_user1.owner == user1

    def test_update_calls_full_clean(
        self, user1, workspace1_user1_updated_valid_data, workspace1_user1
    ):

        with patch("apps.workspaces.models.Workspace.full_clean") as mock_full_clean:
            WorkspaceService.update(
                user=user1,
                validated_data=workspace1_user1_updated_valid_data,
                workspace_id=workspace1_user1.workspace_id
            )

            mock_full_clean.assert_called_once()

    def test_update_calls_resolve_workspace(
        self, user1, workspace1_user1_updated_valid_data, workspace1_user1
    ):

        with patch(
            "apps.workspaces.services.workspace_service.WorkspaceService."
            "_resolve_workspace"
        ) as mock_resolve_workspace:

            WorkspaceService.update(
                user=user1,
                workspace_id=workspace1_user1.workspace_id,
                validated_data=workspace1_user1_updated_valid_data
            )

            mock_resolve_workspace.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


class TestWorkspaceServiceRemove:

    def test_remove_calls_resolve_workspace(self, user1, workspace1_user1):

        with patch(
            "apps.workspaces.services.workspace_service.WorkspaceService."
            "_resolve_workspace"
        ) as mock_resolve_workspace:

            WorkspaceService.remove(
                user=user1,
                workspace_id=workspace1_user1.workspace_id,
            )

            mock_resolve_workspace.assert_called_once()

    def test_remove_deletes_the_workspace_from_database(
            self, user1, workspace1_user1
    ):

        WorkspaceService.remove(
            user=user1,
            workspace_id=workspace1_user1.workspace_id,
        )

        with pytest.raises(Workspace.DoesNotExist):
            Workspace.objects.get(workspace_id=workspace1_user1.workspace_id)


#   ----------------------------------- ****** -----------------------------------


class TestWorkspaceServiceResolve:

    def test_resolve_successfully_returns_workspace(self, user1, workspace1_user1):

        workspace = WorkspaceService._resolve_workspace(
            user=user1,
            workspace_id=workspace1_user1.workspace_id
        )

        assert workspace.workspace_id == workspace1_user1.workspace_id
        assert workspace.owner == workspace1_user1.owner
        assert workspace.name == workspace1_user1.name

    def test_access_to_workspace_of_another_user_raises_error(
        self, user2, workspace1_user1
    ):

        with pytest.raises(AccessDeniedError):
            WorkspaceService._resolve_workspace(
                user=user2,
                workspace_id=workspace1_user1.workspace_id,
            )

    def test_resolve_workspace_with_invalid_workspace_id_raises_error(self, user1):

        with pytest.raises(InfraStructureViolationError):
            WorkspaceService.remove(
                user=user1,
                workspace_id="someInvalidIDWhichIsNotUUID",
            )

#   ----------------------------------- ****** -----------------------------------
