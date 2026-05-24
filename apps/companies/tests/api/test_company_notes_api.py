import pytest
from rest_framework import status

from apps.companies.models import CompanyNote

pytestmark = pytest.mark.django_db


class TestCompanyNoteAPI:

    @pytest.fixture
    def company_note_list_url_path(self, base_api_url_path):

        return f"{base_api_url_path}company-notes/"

    @pytest.fixture
    def create_co_note1_co1_ws1_user1_url_path(
            self, base_api_url_path, co1_ws1_user1
    ):

        return (f"{base_api_url_path}workspaces/"
                f"{co1_ws1_user1.workspace.workspace_id}/companies/"
                f"{co1_ws1_user1.id}/company-notes/")

    @pytest.fixture
    def co_note1_co1_ws1_user1_url_path(
            self, create_co_note1_co1_ws1_user1_url_path, co_note1_co1_ws1_user1
    ):

        return (f"{create_co_note1_co1_ws1_user1_url_path}"
                f"{co_note1_co1_ws1_user1.id}/")

    # List View Tests

    def test_list_requires_authentication(
            self, api_client, company_note_list_url_path
    ):

        response = api_client.get(company_note_list_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_company_notes(
            self,
            authenticated_client,
            company_note_list_url_path,
            co_note1_co1_ws1_user1
    ):

        response = authenticated_client.get(company_note_list_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_retrieve_company_note_list_view(
            self,
            authenticated_client,
            co_note1_co1_ws1_user1,
            company_note_list_url_path
    ):

        response = authenticated_client.get(
            f"{company_note_list_url_path}{co_note1_co1_ws1_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co_note1_co1_ws1_user1.id

    # Nested View Tests

    def test_create_company_note_requires_authentication(
            self,
            api_client,
            create_co_note1_co1_ws1_user1_url_path,
            co_note1_co1_ws1_user1_valid_data,
    ):

        response = api_client.post(
            create_co_note1_co1_ws1_user1_url_path,
            co_note1_co1_ws1_user1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_company_note(
            self,
            authenticated_client,
            create_co_note1_co1_ws1_user1_url_path,
            co_note1_co1_ws1_user1_valid_data,
    ):

        response = authenticated_client.post(
            create_co_note1_co1_ws1_user1_url_path,
            co_note1_co1_ws1_user1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert CompanyNote.objects.filter(pk=response.data["id"]).exists()
        assert response.data["title"] == co_note1_co1_ws1_user1_valid_data["title"]
        assert (response.data["content"] ==
                co_note1_co1_ws1_user1_valid_data["content"])

    def test_retrieve_company_note_nested_view(
            self,
            authenticated_client,
            co_note1_co1_ws1_user1,
            co_note1_co1_ws1_user1_url_path
    ):

        response = authenticated_client.get(co_note1_co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co_note1_co1_ws1_user1.id

    def test_retrieve_company_note_nested_view_requires_authentication(
            self,
            api_client,
            co_note1_co1_ws1_user1_url_path
    ):

        response = api_client.get(co_note1_co1_ws1_user1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_company_note_nested_authentication(
            self,
            api_client,
            co_note1_co1_ws1_user1_url_path,
            co_note1_co1_ws1_user1_updated_valid_data
    ):

        response = api_client.put(
            co_note1_co1_ws1_user1_url_path,
            co_note1_co1_ws1_user1_updated_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_company_note(
            self,
            authenticated_client,
            co_note1_co1_ws1_user1,
            co_note1_co1_ws1_user1_url_path,
            co_note1_co1_ws1_user1_updated_valid_data
    ):

        response = authenticated_client.put(
            co_note1_co1_ws1_user1_url_path,
            co_note1_co1_ws1_user1_updated_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        co_note1_co1_ws1_user1.refresh_from_db()

        assert (co_note1_co1_ws1_user1.title ==
                co_note1_co1_ws1_user1_updated_valid_data["title"])

        assert (co_note1_co1_ws1_user1.content ==
                co_note1_co1_ws1_user1_updated_valid_data["content"])

    def test_partial_update_company_note_requires_authentication(
            self,
            api_client,
            co_note1_co1_ws1_user1,
            co_note1_co1_ws1_user1_url_path,
            co_note1_co1_ws1_user1_updated_valid_data
    ):

        response = api_client.patch(
            co_note1_co1_ws1_user1_url_path,
            co_note1_co1_ws1_user1_updated_valid_data,
            format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_company_note(
            self,
            authenticated_client,
            co_note1_co1_ws1_user1,
            co_note1_co1_ws1_user1_url_path,
            co_note1_co1_ws1_user1_updated_valid_data
    ):

        partial_update_api_data = co_note1_co1_ws1_user1_updated_valid_data.copy()
        partial_update_api_data.pop("title")

        old_title = co_note1_co1_ws1_user1.title

        response = authenticated_client.patch(
            co_note1_co1_ws1_user1_url_path,
            partial_update_api_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        co_note1_co1_ws1_user1.refresh_from_db()

        # content should be changed
        assert co_note1_co1_ws1_user1.content == partial_update_api_data["content"]

        # Name should be unchanged
        assert co_note1_co1_ws1_user1.title == old_title

    def test_delete_company_note_requires_authentication(
            self,
            api_client,
            co_note1_co1_ws1_user1_url_path,
    ):

        response = api_client.delete(co_note1_co1_ws1_user1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_company_note(
            self,
            authenticated_client,
            co_note1_co1_ws1_user1,
            co_note1_co1_ws1_user1_url_path,
    ):

        response = authenticated_client.delete(co_note1_co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert not CompanyNote.objects.filter(pk=co_note1_co1_ws1_user1.id).exists()
