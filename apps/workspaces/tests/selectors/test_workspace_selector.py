import uuid

import pytest

# Exceptions
from apps.core.exceptions.exceptions import (
    AccessDeniedError,
    ResourceNotFoundError
)

# Selectors
from apps.workspaces.selectors.workspace_selector import WorkspaceSelector


@pytest.mark.django_db
class TestWorkspaceSelectorList:

    def test_list_returns_only_user_workspaces(
            self,
            workspace1_user1,
            workspace2_user1,
            workspace1_user2,
    ):

        result = WorkspaceSelector.list(user=workspace1_user1.owner)

        assert set(result) == {workspace1_user1, workspace2_user1}

    def test_list_filters_by_workspace_id(
            self,
            workspace1_user1,
            workspace2_user1,
    ):

        filters = WorkspaceSelector.QueryFilter(
            workspace_id=workspace1_user1.workspace_id,
        )

        result = WorkspaceSelector.list(user=workspace1_user1.owner, filters=filters)

        assert list(result) == [workspace1_user1]

    def test_filter_by_id_dont_force_accessing_to_another_user_workspace(
            self,
            workspace1_user1,
            workspace1_user2,
    ):

        filters = WorkspaceSelector.QueryFilter(
            workspace_id=workspace1_user2.workspace_id,
        )

        result = WorkspaceSelector.list(user=workspace1_user1.owner, filters=filters)

        assert list(result) == []


@pytest.mark.django_db
class TestWorkspaceSelectorGet:

    def test_successfully_get_workspace(self, workspace1_user2):

        workspace = WorkspaceSelector.get(
                user=workspace1_user2.owner,
                workspace_id=workspace1_user2.workspace_id
            )

        assert workspace.owner == workspace1_user2.owner
        assert workspace.workspace_id == workspace1_user2.workspace_id

    def test_access_to_someone_else_workspace_raise_error(
            self,
            user1,
            workspace1_user2,
    ):

        with pytest.raises(AccessDeniedError):
            WorkspaceSelector.get(
                user=user1,
                workspace_id=workspace1_user2.workspace_id
            )

    def test_access_to_non_existence_workspace_raise_error(self, user1):

        with pytest.raises(ResourceNotFoundError):
            WorkspaceSelector.get(user=user1, workspace_id=str(uuid.uuid4()))
