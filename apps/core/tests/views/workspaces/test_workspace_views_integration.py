# apps/core/tests/workspaces/test_workspace_views_integration.py

import pytest

from django.urls import reverse

from apps.workspaces.models import Workspace


pytestmark = pytest.mark.django_db


class TestWorkspaceListView:

    def test_anonymous_user_is_redirected_to_login(self, client):

        response = client.get(
            reverse("workspace-list-web")
        )

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access_view(
        self,
        client,
        workspace1_user1,
    ):

        client.force_login(workspace1_user1.owner)

        response = client.get(
            reverse("workspace-list-web")
        )

        assert response.status_code == 200
        assert "workspaces" in response.context

        # Ensure the expected template is used by the presentation layer
        template_names = [t.name for t in response.templates if t.name]
        assert "workspaces/list.html" in template_names

    def test_user_only_sees_owned_workspaces(
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

    def test_anonymous_user_is_redirected(
        self,
        client,
    ):

        response = client.get(
            reverse("workspace-create-web")
        )

        assert response.status_code == 302

    def test_authenticated_user_can_open_create_page(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse("workspace-create-web")
        )

        assert response.status_code == 200

        # ensure the expected template is rendered for create
        template_names = [t.name for t in response.templates if t.name]
        assert "create_page.html" in template_names

    def test_valid_submission_creates_workspace_and_redirects(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse("workspace-create-web"),
            {
                "name": "New Workspace",
            },
        )

        assert response.status_code == 302

        assert response.url == reverse(
            "workspace-list-web"
        )

        assert Workspace.objects.filter(
            owner=user1,
            name="New Workspace",
        ).exists()

    def test_invalid_submission_renders_form_errors(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse("workspace-create-web"),
            {
                "name": "",
            },
        )

        assert response.status_code == 200

        assert response.context["form"].errors

        # verify the create template is used when rendering form errors
        template_names = [t.name for t in response.templates if t.name]
        assert "create_page.html" in template_names


class TestWorkspaceDetailView:

    def test_anonymous_user_is_redirected(
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

    def test_owner_can_view_workspace(
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

        # ensure correct template is used for detail view
        template_names = [t.name for t in response.templates if t.name]
        assert "workspaces/detail.html" in template_names

    def test_user_cannot_view_foreign_workspace(
        self,
        client,
        user2,
        workspace1_user1,
    ):

        client.force_login(user2)

        response = client.get(
            reverse(
                "workspace-detail-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                },
            )
        )

        assert response.status_code == 404


class TestWorkspaceUpdateView:

    def test_owner_can_open_update_page(
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

        template_names = [t.name for t in response.templates if t.name]
        assert "edit_page.html" in template_names

    def test_valid_submission_updates_workspace_and_redirects(
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
                "name": "Updated Workspace",
            },
        )

        assert response.status_code == 302

        workspace1_user1.refresh_from_db()

        assert workspace1_user1.name == "Updated Workspace"

    def test_invalid_submission_renders_form_errors(
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
                "name": "",
            },
        )

        assert response.status_code == 200

        assert response.context["form"].errors

    def test_user_cannot_update_foreign_workspace(
        self,
        client,
        user2,
        workspace1_user1,
    ):

        client.force_login(user2)

        response = client.post(
            reverse(
                "workspace-edit-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                },
            ),
            {
                "name": "Unauthorized Update",
            },
        )

        assert response.status_code == 404

        workspace1_user1.refresh_from_db()

        assert workspace1_user1.name != "Unauthorized Update"


class TestWorkspaceDeleteView:

    def test_owner_can_open_delete_confirmation(
        self,
        client,
        workspace1_user1,
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

        template_names = [t.name for t in response.templates if t.name]
        assert "delete_confirm.html" in template_names

    def test_valid_submission_deletes_workspace_and_redirects(
        self,
        client,
        workspace1_user1,
    ):

        client.force_login(workspace1_user1.owner)

        workspace_id = workspace1_user1.workspace_id

        response = client.post(
            reverse(
                "workspace-delete-web",
                kwargs={
                    "workspace_id": workspace_id,
                },
            )
        )

        assert response.status_code == 302

        assert not Workspace.objects.filter(
            workspace_id=workspace_id
        ).exists()

    def test_user_cannot_delete_foreign_workspace(
        self,
        client,
        user2,
        workspace1_user1,
    ):

        client.force_login(user2)

        workspace_id = workspace1_user1.workspace_id

        response = client.post(
            reverse(
                "workspace-delete-web",
                kwargs={
                    "workspace_id": workspace_id,
                },
            )
        )

        assert response.status_code == 404

        assert Workspace.objects.filter(
            workspace_id=workspace_id
        ).exists()
