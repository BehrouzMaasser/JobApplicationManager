import pytest

from django.urls import reverse


pytestmark = pytest.mark.django_db


class TestWorkspaceListView:

    def test_redirects_anonymous_user(self, client):
        response = client.get(reverse("workspace-list-web"))

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access(self, client, workspace1_user1):
        client.force_login(workspace1_user1.owner)

        response = client.get(
            reverse("workspace-list-web")
        )

        assert response.status_code == 200
        assert "workspaces" in response.context

    def test_authenticated_user_get_list(self, client, workspace1_user1):
        client.force_login(workspace1_user1.owner)

        response = client.get(
            reverse("workspace-list-web")
        )

        assert response.status_code == 200
        assert workspace1_user1 in response.context["workspaces"]

    def test_list_only_returns_users_workspaces(
            self,
            client,
            user2,
            workspace1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse("workspace-list-web")
        )

        assert response.status_code == 200
        assert workspace1_user1 not in response.context["workspaces"]


class TestWorkspaceCreateView:

    def test_redirects_anonymous_user(
        self,
        client,
    ):
        response = client.get(
            reverse(
                "workspace-create-web",
            )
        )

        assert response.status_code == 302

    def test_get_returns_page(
        self,
        client,
        user1
    ):
        client.force_login(user1)

        response = client.get(
            reverse(
                "workspace-create-web",
            )
        )

        assert response.status_code == 200

    def test_valid_post_creates_workspace(
        self,
        client,
        user1,
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "workspace-create-web",
            ),
            {
                "name": "T1",
            },
        )

        assert response.status_code == 302


class TestWorkspaceDetailView:

    def test_redirects_anonymous_user(
        self,
        client,
        workspace1_user1,
    ):
        response = client.get(
            reverse(
                "workspace-detail-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                },
            )
        )

        assert response.status_code == 302
        assert response.context is None

    def test_authenticated_user_can_access(
        self,
        client,
        workspace1_user1,
    ):
        client.force_login(workspace1_user1.owner)

        response = client.get(
            reverse(
                "workspace-detail-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                },
            )
        )

        assert response.status_code == 200

        assert response.context["workspace"] == workspace1_user1

    def test_user_cannot_view_other_users_workspace(
            self,
            client,
            user2,
            workspace1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse(
                "workspace-detail-web",
                kwargs={"workspace_id": workspace1_user1.workspace_id},
            )
        )

        assert response.status_code == 403


class TestWorkspaceUpdateView:

    def test_get_returns_page(
        self,
        client,
        workspace1_user1,
    ):
        client.force_login(workspace1_user1.owner)

        response = client.get(
            reverse(
                "workspace-edit-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_updates_workspace(
        self,
        client,
        workspace1_user1,
    ):
        client.force_login(workspace1_user1.owner)

        response = client.post(
            reverse(
                "workspace-edit-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                },
            ),
            {
                "name": "T1 Updated",
            },
        )

        assert response.status_code == 302

        workspace1_user1.refresh_from_db()

        assert workspace1_user1.name == "T1 Updated"

    def test_user_cannot_update_other_users_workspace(
            self,
            client,
            user2,
            workspace1_user1,
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "workspace-edit-web",
                kwargs={"workspace_id": workspace1_user1.workspace_id},
            ),
            {
                "name": "Cant Update",
            },
        )

        assert response.status_code == 403

        workspace1_user1.refresh_from_db()

        assert workspace1_user1.name != "Cant Update"


class TestWorkspaceDeleteView:

    def test_get_returns_confirmation(
        self,
        client,
        workspace1_user1
    ):
        client.force_login(workspace1_user1.owner)

        response = client.get(
            reverse(
                "workspace-delete-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                },
            )
        )

        assert response.status_code == 200

    def test_post_deletes_workspace(
        self,
        client,
        workspace1_user1
    ):
        client.force_login(workspace1_user1.owner)

        response = client.post(
            reverse(
                "workspace-delete-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                },
            )
        )

        assert response.status_code == 302

        from apps.workspaces.models import Workspace

        assert not Workspace.objects.filter(
            workspace_id=workspace1_user1.workspace_id
        ).exists()

    def test_user_cannot_delete_other_users_workspace(
            self,
            client,
            user2,
            workspace1_user1,
    ):
        client.force_login(user2)

        response = client.post(

            reverse(
                "workspace-delete-web",
                kwargs={"workspace_id": workspace1_user1.workspace_id},
            )
        )

        assert response.status_code == 403

        from apps.workspaces.models import Workspace

        assert Workspace.objects.filter(
            workspace_id=workspace1_user1.workspace_id
        ).exists()
