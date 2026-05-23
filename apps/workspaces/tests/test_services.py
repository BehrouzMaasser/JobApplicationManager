from unittest.mock import patch

import pytest

from django.core.exceptions import ValidationError

from apps.workspaces.services.workspace_service import WorkspaceService


#   ----------------------------------- ****** -----------------------------------

# Test Creating

@pytest.mark.django_db
def test_create_workspace_successfully_returns_workspace(
        user, workspace1_user1_valid_data
):

    workspace = WorkspaceService.create(
        user=user, validated_data=workspace1_user1_valid_data
    )

    assert workspace.id is not None
    assert workspace.workspace_id is not None
    assert workspace.name == workspace1_user1_valid_data["name"]
    assert workspace.owner == user


@pytest.mark.django_db
def test_create_workspace_calls_full_clean(user, workspace1_user1_valid_data):

    with patch("apps.workspaces.models.Workspace.full_clean") as mock_full_clean:
        WorkspaceService.create(
            user=user, validated_data=workspace1_user1_valid_data
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_create_workspace_calls_save(user, workspace1_user1_valid_data):

    with patch("apps.workspaces.models.Workspace.save") as mock_save:

        WorkspaceService.create(
            user=user, validated_data=workspace1_user1_valid_data
        )

        mock_save.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Updating

@pytest.mark.django_db
def test_update_workspace_successfully_returns_updated_workspace(
        user, workspace1_user1_updated_valid_data, workspace_user1
):

    updated_workspace = WorkspaceService.update(
        user=user,
        validated_data=workspace1_user1_updated_valid_data,
        workspace_id=workspace_user1.workspace_id
    )

    assert updated_workspace.workspace_id == workspace_user1.workspace_id
    assert updated_workspace.name == workspace1_user1_updated_valid_data["name"]
    assert updated_workspace.owner == user


@pytest.mark.django_db
def test_update_workspace_calls_full_clean(
        user, workspace1_user1_updated_valid_data, workspace_user1
):

    with patch("apps.workspaces.models.Workspace.full_clean") as mock_full_clean:
        WorkspaceService.update(
            user=user,
            validated_data=workspace1_user1_updated_valid_data,
            workspace_id=workspace_user1.workspace_id
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_update_workspace_calls_save(
        user,
        workspace1_user1_updated_valid_data,
        workspace_user1
):

    with patch("apps.workspaces.models.Workspace.save") as mock_save:

        WorkspaceService.update(
            user=user,
            validated_data=workspace1_user1_updated_valid_data,
            workspace_id=workspace_user1.workspace_id
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_workspace_calls_resolve_workspace(
        user, workspace1_user1_updated_valid_data, workspace_user1
):

    with patch(
            "apps.workspaces.services.workspace_service.WorkspaceService."
            "_resolve_workspace"
    ) as mock_resolve_workspace:

        WorkspaceService.update(
            user=user,
            workspace_id=workspace_user1.workspace_id,
            validated_data=workspace1_user1_updated_valid_data
        )

        mock_resolve_workspace.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_remove_workspace_calls_resolve_workspace(user, workspace_user1):

    with patch(
            "apps.workspaces.services.workspace_service.WorkspaceService."
            "_resolve_workspace"
    ) as mock_resolve_workspace:

        WorkspaceService.remove(
            user=user,
            workspace_id=workspace_user1.workspace_id,
        )

        mock_resolve_workspace.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test retrieving workspace

@pytest.mark.django_db
def test_resolve_workspace_successfully_returns_workspace(user, workspace_user1):

    workspace = WorkspaceService._resolve_workspace(
        user=user,
        workspace_id=workspace_user1.workspace_id
    )

    assert workspace.workspace_id == workspace_user1.workspace_id
    assert workspace.owner == workspace_user1.owner
    assert workspace.name == workspace_user1.name


@pytest.mark.django_db
def test_access_to_a_workspace_of_another_user_raises_error(
        user, other_user, workspace_user1
):

    with pytest.raises(ValidationError):
        WorkspaceService._resolve_workspace(
            user=other_user,
            workspace_id=workspace_user1.workspace_id,
        )


@pytest.mark.django_db
def test_resolve_workspace_with_invalid_workspace_id_raises_error(user):

    with pytest.raises(ValidationError):
        WorkspaceService.remove(
            user=user,
            workspace_id="someInvalidIDWhichIsNotUUID",
        )

#   ----------------------------------- ****** -----------------------------------
