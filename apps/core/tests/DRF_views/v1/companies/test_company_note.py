import pytest
from rest_framework import status

from apps.companies.models import CompanyNote

pytestmark = pytest.mark.django_db


# =========================================================
# LIST
# =========================================================

class TestCompanyNoteListAPIView:

    @pytest.fixture
    def url(self, base_api_url_path):
        return f"{base_api_url_path}company-notes/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_company_notes(
        self,
        authenticated_client,
        url,
        co_note1_co1_ws1_user1,
    ):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {item["id"] for item in response.data["results"]}
        assert co_note1_co1_ws1_user1.id in returned_ids

    def test_does_not_return_foreign_company_notes(
        self,
        authenticated_client,
        url,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user2,
    ):
        response = authenticated_client.get(url)

        returned_ids = {item["id"] for item in response.data["results"]}
        assert co_note1_co1_ws1_user2.id not in returned_ids


# =========================================================
# RETRIEVE (global endpoint)
# =========================================================

class TestCompanyNoteRetrieveAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, co_note1_co1_ws1_user1):
        return f"{base_api_url_path}company-notes/{co_note1_co1_ws1_user1.id}/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieves_company_note(
        self,
        authenticated_client,
        url,
        co_note1_co1_ws1_user1,
    ):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co_note1_co1_ws1_user1.id

    def test_returns_404_for_unknown_note(
        self,
        authenticated_client,
        base_api_url_path,
    ):
        response = authenticated_client.get(
            f"{base_api_url_path}company-notes/999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


# =========================================================
# NESTED CREATE
# =========================================================

class TestNestedCompanyNoteCreateAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, co1_ws1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{co1_ws1_user1.workspace.workspace_id}/"
            f"companies/{co1_ws1_user1.id}/company-notes/"
        )

    def test_requires_authentication(
        self,
        api_client,
        url,
        co_note1_co1_ws1_user1_valid_data,
    ):
        response = api_client.post(
            url, co_note1_co1_ws1_user1_valid_data, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_company_note_success(
        self,
        authenticated_client,
        url,
        co_note1_co1_ws1_user1_valid_data,
    ):
        response = authenticated_client.post(
            url,
            co_note1_co1_ws1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        obj_id = response.data["id"]

        assert CompanyNote.objects.filter(id=obj_id).exists()
        assert response.data["title"] == co_note1_co1_ws1_user1_valid_data["title"]
        assert (response.data["content"] ==
                co_note1_co1_ws1_user1_valid_data["content"])

    def test_cannot_create_in_foreign_company(
        self,
        authenticated_client,
        base_api_url_path,
        co1_ws1_user2,
        co_note1_co1_ws1_user1_valid_data,
    ):
        url = (
            f"{base_api_url_path}workspaces/{co1_ws1_user2.workspace.workspace_id}/"
            f"companies/{co1_ws1_user2.id}/company-notes/"
        )

        response = authenticated_client.post(
            url,
            co_note1_co1_ws1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_payload_rejected(
        self,
        authenticated_client,
        url,
    ):
        response = authenticated_client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =========================================================
# NESTED RETRIEVE
# =========================================================

class TestNestedCompanyNoteRetrieveAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, co1_ws1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{co1_ws1_user1.workspace.workspace_id}/"
            f"companies/{co1_ws1_user1.id}/company-notes/"
        )

    def test_requires_authentication(
        self,
        api_client,
        url,
        co_note1_co1_ws1_user1,
    ):
        response = api_client.get(f"{url}{co_note1_co1_ws1_user1.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieves_company_note(
        self,
        authenticated_client,
        url,
        co_note1_co1_ws1_user1,
    ):
        response = authenticated_client.get(f"{url}{co_note1_co1_ws1_user1.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co_note1_co1_ws1_user1.id

    def test_returns_404_for_unknown_note(
        self,
        authenticated_client,
        url,
    ):
        response = authenticated_client.get(f"{url}999999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


# =========================================================
# NESTED UPDATE
# =========================================================

class TestNestedCompanyNoteUpdateAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, co1_ws1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{co1_ws1_user1.workspace.workspace_id}/"
            f"companies/{co1_ws1_user1.id}/company-notes/"
        )

    def test_requires_authentication(
        self,
        api_client,
        url,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
    ):
        response = api_client.put(
            f"{url}{co_note1_co1_ws1_user1.id}/",
            co_note1_co1_ws1_user1_updated_valid_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_full_update_success(
        self,
        authenticated_client,
        url,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
    ):
        response = authenticated_client.put(
            f"{url}{co_note1_co1_ws1_user1.id}/",
            co_note1_co1_ws1_user1_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        co_note1_co1_ws1_user1.refresh_from_db()

        assert (co_note1_co1_ws1_user1.title ==
                co_note1_co1_ws1_user1_updated_valid_data["title"])

        assert (co_note1_co1_ws1_user1.content ==
                co_note1_co1_ws1_user1_updated_valid_data["content"])

    def test_partial_update_success(
        self,
        authenticated_client,
        url,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
    ):
        old_title = co_note1_co1_ws1_user1.title

        payload = {"content": co_note1_co1_ws1_user1_updated_valid_data["content"]}

        response = authenticated_client.patch(
            f"{url}{co_note1_co1_ws1_user1.id}/",
            payload,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        co_note1_co1_ws1_user1.refresh_from_db()

        assert co_note1_co1_ws1_user1.content == payload["content"]
        assert co_note1_co1_ws1_user1.title == old_title

    def test_patch_requires_authentication(
        self,
        api_client,
        url,
        co_note1_co1_ws1_user1,
    ):
        response = api_client.patch(
            f"{url}{co_note1_co1_ws1_user1.id}/",
            {"title": "x"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# =========================================================
# NESTED DELETE
# =========================================================

class TestNestedCompanyNoteDeleteAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, co1_ws1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{co1_ws1_user1.workspace.workspace_id}/"
            f"companies/{co1_ws1_user1.id}/company-notes/"
        )

    def test_requires_authentication(
        self,
        api_client,
        url,
        co_note1_co1_ws1_user1,
    ):
        response = api_client.delete(f"{url}{co_note1_co1_ws1_user1.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_success(
        self,
        authenticated_client,
        url,
        co_note1_co1_ws1_user1,
    ):
        response = authenticated_client.delete(f"{url}{co_note1_co1_ws1_user1.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CompanyNote.objects.filter(id=co_note1_co1_ws1_user1.id).exists()

    def test_delete_foreign_note_forbidden(
        self,
        authenticated_client,
        base_api_url_path,
        co_note1_co1_ws1_user2,
    ):
        url = (
            f"{base_api_url_path}workspaces/"
            f"{co_note1_co1_ws1_user2.company.workspace.workspace_id}/companies/"
            f"{co_note1_co1_ws1_user2.company.id}/company-notes/"
            f"{co_note1_co1_ws1_user2.id}/"
        )

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_unknown_note(
        self,
        authenticated_client,
        url,
    ):
        response = authenticated_client.delete(f"{url}999999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
