import uuid

import pytest

from apps.core.common.types.filters import WorkspaceQueryFilter
from apps.core.exceptions.exceptions import ResourceNotFoundError
from apps.workspaces.selectors.workspace_selector import WorkspaceSelector


@pytest.mark.django_db
class TestWorkspaceSelectorBaseQueryset:

    def test_base_queryset_returns_all_workspaces(
            self,
            workspace1_user1,
            workspace2_user1,
            workspace1_user2,
    ):

        queryset = WorkspaceSelector.base_queryset()

        assert set(queryset) == {
            workspace1_user1,
            workspace2_user1,
            workspace1_user2,
        }


@pytest.mark.django_db
class TestWorkspaceSelectorAccessibleQueryset:

    def test_accessible_queryset_returns_only_owned_workspaces(
            self,
            workspace1_user1,
            workspace2_user1,
            workspace1_user2,
    ):

        queryset = WorkspaceSelector.accessible_queryset(
            user=workspace1_user1.owner
        )

        assert set(queryset) == {
            workspace1_user1,
            workspace2_user1,
        }


@pytest.mark.django_db
class TestWorkspaceSelectorList:

    def test_list_returns_only_user_workspaces(
            self,
            workspace1_user1,
            workspace2_user1,
            workspace1_user2,
    ):

        result = WorkspaceSelector.list(user=workspace1_user1.owner)

        assert set(result) == {
            workspace1_user1,
            workspace2_user1,
        }

    def test_list_filters_by_workspace_id(
            self,
            workspace1_user1,
            workspace2_user1,
    ):

        filters = WorkspaceQueryFilter(
            workspace_id=workspace1_user1.workspace_id,
        )

        result = WorkspaceSelector.list(
            user=workspace1_user1.owner,
            filters=filters,
        )

        assert list(result) == [workspace1_user1]

    def test_list_never_returns_other_users_workspace(
            self,
            workspace1_user1,
            workspace1_user2,
    ):

        filters = WorkspaceQueryFilter(
            workspace_id=workspace1_user2.workspace_id,
        )

        result = WorkspaceSelector.list(
            user=workspace1_user1.owner,
            filters=filters,
        )

        assert list(result) == []


@pytest.mark.django_db
class TestWorkspaceSelectorGet:

    def test_get_returns_workspace(self, workspace1_user2):

        workspace = WorkspaceSelector.get(
            user=workspace1_user2.owner,
            obj_id=workspace1_user2.workspace_id,
        )

        assert workspace == workspace1_user2

    def test_get_other_users_workspace_raises_resource_not_found(
            self,
            user1,
            workspace1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            WorkspaceSelector.get(
                user=user1,
                obj_id=workspace1_user2.workspace_id,
            )

    def test_get_non_existing_workspace_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            WorkspaceSelector.get(
                user=user1,
                obj_id=uuid.uuid4(),
            )
