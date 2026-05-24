import pytest
from rest_framework import status

from apps.companies.models import Company

pytestmark = pytest.mark.django_db


class TestCompanyAPI:

    @pytest.fixture
    def company_list_url_path(self, base_api_url_path):

        return f"{base_api_url_path}companies/"

    @pytest.fixture
    def create_co1_ws1_user1_url_path(self, base_api_url_path, workspace_user1):

        return (f"{base_api_url_path}workspaces/{workspace_user1.workspace_id}/"
                f"companies/")

    @pytest.fixture
    def co1_ws1_user1_url_path(self, create_co1_ws1_user1_url_path, co1_ws1_user1):

        return f"{create_co1_ws1_user1_url_path}{co1_ws1_user1.id}/"

    # List View Tests

    def test_list_requires_authentication(self, api_client, company_list_url_path):

        response = api_client.get(company_list_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_companies(
            self, authenticated_client, company_list_url_path, co1_ws1_user1
    ):

        response = authenticated_client.get(company_list_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_retrieve_company_list_view(
            self, authenticated_client, co1_ws1_user1, company_list_url_path
    ):

        response = authenticated_client.get(
            f"{company_list_url_path}{co1_ws1_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co1_ws1_user1.id

    # Nested View Tests

    def test_create_company_requires_authentication(
            self,
            api_client,
            create_co1_ws1_user1_url_path,
            co1_ws1_user1_valid_data,
    ):

        response = api_client.post(
            create_co1_ws1_user1_url_path,
            co1_ws1_user1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_company(
            self,
            authenticated_client,
            create_co1_ws1_user1_url_path,
            co1_ws1_user1_valid_data,
    ):

        response = authenticated_client.post(
            create_co1_ws1_user1_url_path,
            co1_ws1_user1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert Company.objects.filter(pk=response.data["id"]).exists()
        assert response.data["name"] == co1_ws1_user1_valid_data["name"]
        assert response.data["website"] == co1_ws1_user1_valid_data["website"]

    def test_retrieve_company_nested_view_requires_authentication(
            self, api_client, co1_ws1_user1_url_path
    ):

        response = api_client.get(co1_ws1_user1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_company_nested_view(
            self, authenticated_client, co1_ws1_user1, co1_ws1_user1_url_path
    ):

        response = authenticated_client.get(co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co1_ws1_user1.id

    def test_update_company_nested_view_requires_authentication(
            self, api_client, co1_ws1_user1_url_path
    ):

        response = api_client.put(co1_ws1_user1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_company(
            self,
            authenticated_client,
            co1_ws1_user1,
            co1_ws1_user1_url_path,
            co1_ws1_user1_updated_valid_data
    ):

        response = authenticated_client.put(
            co1_ws1_user1_url_path,
            co1_ws1_user1_updated_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        co1_ws1_user1.refresh_from_db()

        assert co1_ws1_user1.name == co1_ws1_user1_updated_valid_data["name"]
        assert co1_ws1_user1.website == co1_ws1_user1_updated_valid_data["website"]

    def test_partial_update_company_requires_authentication(
            self, api_client, co1_ws1_user1_url_path
    ):

        response = api_client.patch(co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_company(
            self,
            authenticated_client,
            co1_ws1_user1,
            co1_ws1_user1_url_path,
            co1_ws1_user1_updated_valid_data
    ):

        partial_update_api_data = co1_ws1_user1_updated_valid_data.copy()
        partial_update_api_data.pop("name")

        old_name = co1_ws1_user1.name

        response = authenticated_client.patch(
            co1_ws1_user1_url_path,
            partial_update_api_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        co1_ws1_user1.refresh_from_db()

        # website should be changed
        assert co1_ws1_user1.website == partial_update_api_data["website"]

        # Name should be unchanged
        assert co1_ws1_user1.name == old_name

    def test_delete_company_requires_authentication(
            self, api_client, co1_ws1_user1_url_path
    ):

        response = api_client.delete(co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_company(
            self,
            authenticated_client,
            co1_ws1_user1,
            co1_ws1_user1_url_path,
    ):

        response = authenticated_client.delete(co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert not Company.objects.filter(pk=co1_ws1_user1.id).exists()
