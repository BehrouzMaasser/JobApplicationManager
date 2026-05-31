import pytest

from apps.workspaces.selectors.workspace_selector import WorkspaceSelector


@pytest.mark.django_db
class TestWorkspaceSelector:

    def test_list_returns_only_user_notes(
            self,
            user,
            workspace_user1,
            other_workspace_user1,
            workspace_user2,
    ):

        result = WorkspaceSelector.list(user=user)

        assert len(result) == 2
        assert set(result) == {workspace_user1, other_workspace_user1}

    def test_list_filters_by_workspace_id(
            self,
            user,
            workspace_user1,
            other_workspace_user1,
            workspace_user2,
    ):

        filters = WorkspaceSelector.QueryFilter(
            workspace_id=workspace_user1.workspace_id,
        )

        result = WorkspaceSelector.list(user=user, filters=filters)

        assert list(result) == [workspace_user1]
