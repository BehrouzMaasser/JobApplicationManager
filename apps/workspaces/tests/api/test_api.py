import pytest
from rest_framework import status

from apps.workspaces.models import Workspace


pytestmark = pytest.mark.django_db


class TestWorkspaceAPI:

    @pytest.fixture
    def workspace_url_path(self, base_api_url_path):
        return f"{base_api_url_path}workspaces/"

    def test_list_requires_authentication(self, api_client, workspace_url_path):
        response = api_client.get(workspace_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_workspaces(self, authenticated_client, workspace_url_path):
        response = authenticated_client.get(workspace_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_create_workspace(self, authenticated_client, workspace_url_path):
        payload = {
            "name": "New Workspace"
        }

        response = authenticated_client.post(
            workspace_url_path,
            payload,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "New Workspace"

        assert Workspace.objects.filter(name="New Workspace").exists()

    def test_retrieve_workspace(
            self, authenticated_client, workspace_user1, workspace_url_path
    ):
        response = authenticated_client.get(
            f"{workspace_url_path}{workspace_user1.workspace_id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["workspace_id"] == str(workspace_user1.workspace_id)

    def test_update_workspace(
            self, authenticated_client, workspace_user1, workspace_url_path
    ):
        payload = {
            "name": "Updated Workspace"
        }

        response = authenticated_client.put(
            f"{workspace_url_path}{workspace_user1.workspace_id}/",
            payload,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "Updated Workspace"

        workspace_user1.refresh_from_db()
        assert workspace_user1.name == "Updated Workspace"

    def test_delete_workspace(
            self, authenticated_client, workspace_user1, workspace_url_path
    ):
        response = authenticated_client.delete(
            f"{workspace_url_path}{workspace_user1.workspace_id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert not Workspace.objects.filter(
            workspace_id=workspace_user1.workspace_id
        ).exists()
