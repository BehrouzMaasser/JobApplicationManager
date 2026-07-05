import pytest
from rest_framework import status

from apps.companies.models import CompanyNote

pytestmark = pytest.mark.django_db


# =========================================================
# LIST
# =========================================================
class TestCompanyNoteListAPIView:

    @pytest.fixture
    def company_note_list_url_path(self, base_api_url_path):
        return f"{base_api_url_path}company-notes/"

    def test_requires_authentication(
        self,
        api_client,
        company_note_list_url_path,
    ):
        response = api_client.get(company_note_list_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_company_notes(
        self,
        authenticated_client,
        company_note_list_url_path,
        co_note1_co1_ws1_user1,
    ):
        response = authenticated_client.get(company_note_list_url_path)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {item["id"] for item in response.data["results"]}
        assert co_note1_co1_ws1_user1.id in returned_ids


# =========================================================
# RETRIEVE (global endpoint)
# =========================================================
class TestCompanyNoteRetrieveAPIView:

    @pytest.fixture
    def company_note_list_url_path(self, base_api_url_path):
        return f"{base_api_url_path}company-notes/"

    def test_requires_authentication(
        self,
        api_client,
        company_note_list_url_path,
        co_note1_co1_ws1_user1,
    ):
        response = api_client.get(
            f"{company_note_list_url_path}{co_note1_co1_ws1_user1.id}/"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_company_note(
        self,
        authenticated_client,
        company_note_list_url_path,
        co_note1_co1_ws1_user1,
    ):
        response = authenticated_client.get(
            f"{company_note_list_url_path}{co_note1_co1_ws1_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co_note1_co1_ws1_user1.id

    def test_returns_404_for_unknown_company_note(
        self,
        authenticated_client,
        company_note_list_url_path,
    ):
        response = authenticated_client.get(
            f"{company_note_list_url_path}999999/"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


# =========================================================
# NESTED CREATE
# =========================================================
class TestNestedCompanyNoteCreateAPIView:

    @pytest.fixture
    def create_company_note_url_path(self, base_api_url_path, co1_ws1_user1):
        return (
            f"{base_api_url_path}"
            f"workspaces/{co1_ws1_user1.workspace.workspace_id}/"
            f"companies/{co1_ws1_user1.id}/company-notes/"
        )

    def test_requires_authentication(
        self,
        api_client,
        create_company_note_url_path,
        co_note1_co1_ws1_user1_valid_data,
    ):
        response = api_client.post(
            create_company_note_url_path,
            co_note1_co1_ws1_user1_valid_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_company_note(
        self,
        authenticated_client,
        create_company_note_url_path,
        co_note1_co1_ws1_user1_valid_data,
    ):
        response = authenticated_client.post(
            create_company_note_url_path,
            co_note1_co1_ws1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        assert CompanyNote.objects.filter(
            id=response.data["id"]
        ).exists()

        assert response.data["title"] == co_note1_co1_ws1_user1_valid_data["title"]

        assert (response.data["content"] ==
                co_note1_co1_ws1_user1_valid_data["content"])


# =========================================================
# NESTED RETRIEVE
# =========================================================
class TestNestedCompanyNoteRetrieveAPIView:

    @pytest.fixture
    def create_company_note_url_path(self, base_api_url_path, co1_ws1_user1):
        return (
            f"{base_api_url_path}"
            f"workspaces/{co1_ws1_user1.workspace.workspace_id}/"
            f"companies/{co1_ws1_user1.id}/company-notes/"
        )

    def test_retrieve_requires_authentication(
        self,
        api_client,
        create_company_note_url_path,
        co_note1_co1_ws1_user1,
    ):
        response = api_client.get(
            f"{create_company_note_url_path}{co_note1_co1_ws1_user1.id}/"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_company_note(
        self,
        authenticated_client,
        create_company_note_url_path,
        co_note1_co1_ws1_user1,
    ):
        response = authenticated_client.get(
            f"{create_company_note_url_path}{co_note1_co1_ws1_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co_note1_co1_ws1_user1.id

    def test_returns_404_for_unknown_note(
        self,
        authenticated_client,
        create_company_note_url_path,
    ):
        response = authenticated_client.get(
            f"{create_company_note_url_path}999999/"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


# =========================================================
# NESTED UPDATE
# =========================================================
class TestNestedCompanyNoteUpdateAPIView:

    @pytest.fixture
    def create_company_note_url_path(self, base_api_url_path, co1_ws1_user1):
        return (
            f"{base_api_url_path}"
            f"workspaces/{co1_ws1_user1.workspace.workspace_id}/"
            f"companies/{co1_ws1_user1.id}/company-notes/"
        )

    def test_update_requires_authentication(
        self,
        api_client,
        create_company_note_url_path,
        co_note1_co1_ws1_user1_updated_valid_data,
        co_note1_co1_ws1_user1,
    ):
        response = api_client.put(
            f"{create_company_note_url_path}{co_note1_co1_ws1_user1.id}/",
            co_note1_co1_ws1_user1_updated_valid_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_company_note(
        self,
        authenticated_client,
        create_company_note_url_path,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
    ):
        response = authenticated_client.put(
            f"{create_company_note_url_path}{co_note1_co1_ws1_user1.id}/",
            co_note1_co1_ws1_user1_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        co_note1_co1_ws1_user1.refresh_from_db()

        assert (co_note1_co1_ws1_user1.title ==
                co_note1_co1_ws1_user1_updated_valid_data["title"])

        assert (co_note1_co1_ws1_user1.content ==
                co_note1_co1_ws1_user1_updated_valid_data["content"])

    def test_partial_update_company_note(
        self,
        authenticated_client,
        create_company_note_url_path,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
    ):
        old_title = co_note1_co1_ws1_user1.title

        partial_data = {
            "content": co_note1_co1_ws1_user1_updated_valid_data["content"]
        }

        response = authenticated_client.patch(
            f"{create_company_note_url_path}{co_note1_co1_ws1_user1.id}/",
            partial_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        co_note1_co1_ws1_user1.refresh_from_db()

        assert co_note1_co1_ws1_user1.content == partial_data["content"]
        assert co_note1_co1_ws1_user1.title == old_title


# =========================================================
# NESTED DELETE
# =========================================================
class TestNestedCompanyNoteDeleteAPIView:

    @pytest.fixture
    def create_company_note_url_path(self, base_api_url_path, co1_ws1_user1):
        return (
            f"{base_api_url_path}"
            f"workspaces/{co1_ws1_user1.workspace.workspace_id}/"
            f"companies/{co1_ws1_user1.id}/company-notes/"
        )

    def test_delete_requires_authentication(
        self,
        api_client,
        create_company_note_url_path,
        co_note1_co1_ws1_user1,
    ):
        response = api_client.delete(
            f"{create_company_note_url_path}{co_note1_co1_ws1_user1.id}/"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_company_note(
        self,
        authenticated_client,
        create_company_note_url_path,
        co_note1_co1_ws1_user1,
    ):
        response = authenticated_client.delete(
            f"{create_company_note_url_path}{co_note1_co1_ws1_user1.id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not CompanyNote.objects.filter(
            id=co_note1_co1_ws1_user1.id
        ).exists()
