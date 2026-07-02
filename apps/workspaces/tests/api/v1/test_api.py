import uuid

import pytest
from rest_framework import status

# Models
from apps.workspaces.models import Workspace

pytestmark = pytest.mark.django_db


@pytest.fixture
def workspace_url_path(base_api_url_path):
    return f"{base_api_url_path}workspaces/"


class TestWorkspaceListAPIView:

    def test_requires_authentication(
        self,
        api_client,
        workspace_url_path,
    ):

        response = api_client.get(workspace_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_only_authenticated_user_workspaces(
        self,
        authenticated_client,
        workspace1_user1,
        workspace1_user2,
        workspace_url_path,
    ):

        response = authenticated_client.get(workspace_url_path)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {
            item["workspace_id"]
            for item in response.data["results"]
        }

        assert str(workspace1_user1.workspace_id) in returned_ids
        assert str(workspace1_user2.workspace_id) not in returned_ids


class TestWorkspaceCreateAPIView:

    def test_create_workspace(
        self,
        authenticated_client,
        workspace_url_path,
    ):

        payload = {
            "name": "Backend Tracker"
        }

        response = authenticated_client.post(
            workspace_url_path,
            payload,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == payload["name"]

        assert Workspace.objects.filter(name=payload["name"]).exists()

    def test_rejects_duplicate_workspace_name(
        self,
        authenticated_client,
        workspace1_user1,
        workspace_url_path,
    ):

        response = authenticated_client.post(
            workspace_url_path,
            {"name": workspace1_user1.name},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestWorkspaceRetrieveUpdateAPIView:

    def test_retrieve_workspace(
        self,
        authenticated_client,
        workspace1_user1,
        workspace_url_path,
    ):

        response = authenticated_client.get(
            f"{workspace_url_path}{workspace1_user1.workspace_id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["workspace_id"] == str(
            workspace1_user1.workspace_id
        )

    def test_returns_404_for_unknown_workspace(
        self,
        authenticated_client,
        workspace_url_path,
    ):

        response = authenticated_client.get(
            f"{workspace_url_path}{uuid.uuid4()}/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cannot_access_another_users_workspace(
        self,
        authenticated_client,
        workspace1_user2,
        workspace_url_path,
    ):

        response = authenticated_client.get(
            f"{workspace_url_path}{workspace1_user2.workspace_id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_workspace(
        self,
        authenticated_client,
        workspace1_user1,
        workspace_url_path,
    ):

        payload = {
            "name": "Updated Workspace"
        }

        response = authenticated_client.put(
            f"{workspace_url_path}{workspace1_user1.workspace_id}/",
            payload,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        workspace1_user1.refresh_from_db()

        assert workspace1_user1.name == payload["name"]

    def test_cannot_update_another_users_workspace(
        self,
        authenticated_client,
        workspace1_user2,
        workspace_url_path,
    ):

        response = authenticated_client.put(
            f"{workspace_url_path}{workspace1_user2.workspace_id}/",
            {"name": "Hack"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_rejects_duplicate_workspace_name_update(
        self,
        authenticated_client,
        workspace1_user1,
        workspace2_user1,
        workspace_url_path,
    ):

        response = authenticated_client.put(
            f"{workspace_url_path}{workspace1_user1.workspace_id}/",
            {"name": workspace2_user1.name},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestWorkspaceDeleteAPIView:

    def test_delete_workspace(
        self,
        authenticated_client,
        workspace1_user1,
        workspace_url_path,
    ):

        response = authenticated_client.delete(
            f"{workspace_url_path}{workspace1_user1.workspace_id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Workspace.objects.filter(
            workspace_id=workspace1_user1.workspace_id
        ).exists()

    def test_cannot_delete_another_users_workspace(
        self,
        authenticated_client,
        workspace1_user2,
        workspace_url_path,
    ):

        response = authenticated_client.delete(
            f"{workspace_url_path}{workspace1_user2.workspace_id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
