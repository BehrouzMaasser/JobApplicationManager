import pytest
from rest_framework import status

from apps.companies.models import CompanyEmail

pytestmark = pytest.mark.django_db


class TestCompanyEmailAPI:

    @pytest.fixture
    def company_email_list_url_path(self, base_api_url_path):

        return f"{base_api_url_path}company-emails/"

    @pytest.fixture
    def create_co_email1_co1_ws1_user1_url_path(
            self, base_api_url_path, co_email1_co1_ws1_user1
    ):

        return (f"{base_api_url_path}workspaces/"
                f"{co_email1_co1_ws1_user1.company.workspace.workspace_id}/"
                f"companies/{co_email1_co1_ws1_user1.id}/company-emails/")

    @pytest.fixture
    def co_email1_co1_ws1_user1_url_path(
            self, create_co_email1_co1_ws1_user1_url_path, co_email1_co1_ws1_user1
    ):

        return (f"{create_co_email1_co1_ws1_user1_url_path}"
                f"{co_email1_co1_ws1_user1.id}/")

    # List View Tests

    def test_list_requires_authentication(
            self, api_client, company_email_list_url_path
    ):

        response = api_client.get(company_email_list_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_company_emails(
            self,
            authenticated_client,
            company_email_list_url_path,
            co_email1_co1_ws1_user1
    ):

        response = authenticated_client.get(company_email_list_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_retrieve_company_email_list_view(
            self,
            authenticated_client,
            co_email1_co1_ws1_user1,
            company_email_list_url_path
    ):

        response = authenticated_client.get(
            f"{company_email_list_url_path}{co_email1_co1_ws1_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co_email1_co1_ws1_user1.id

    # Nested View Tests

    def test_create_company_email_requires_authentication(
            self,
            api_client,
            create_co_email1_co1_ws1_user1_url_path,
            co_email1_co1_ws1_user1_valid_data,
    ):

        response = api_client.post(
            create_co_email1_co1_ws1_user1_url_path,
            co_email1_co1_ws1_user1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_company_email(
            self,
            authenticated_client,
            create_co_email1_co1_ws1_user1_url_path,
            co_email1_co1_ws1_user1_valid_data,
    ):

        response = authenticated_client.post(
            create_co_email1_co1_ws1_user1_url_path,
            co_email1_co1_ws1_user1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert CompanyEmail.objects.filter(pk=response.data["id"]).exists()

        assert (response.data["title"] ==
                co_email1_co1_ws1_user1_valid_data["title"])

        assert (response.data["email"] ==
                co_email1_co1_ws1_user1_valid_data["email"])

    def test_retrieve_company_email_nested_view(
            self,
            authenticated_client,
            co_email1_co1_ws1_user1,
            co_email1_co1_ws1_user1_url_path
    ):

        response = authenticated_client.get(co_email1_co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co_email1_co1_ws1_user1.id

    def test_retrieve_company_email_nested_view_requires_authentication(
            self,
            api_client,
            co_email1_co1_ws1_user1_url_path
    ):

        response = api_client.get(co_email1_co1_ws1_user1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_company_email_nested_authentication(
            self,
            api_client,
            co_email1_co1_ws1_user1_url_path,
            co_email1_co1_ws1_user1_updated_valid_data
    ):

        response = api_client.put(
            co_email1_co1_ws1_user1_url_path,
            co_email1_co1_ws1_user1_updated_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_company_email(
            self,
            authenticated_client,
            co_email1_co1_ws1_user1,
            co_email1_co1_ws1_user1_url_path,
            co_email1_co1_ws1_user1_updated_valid_data
    ):

        response = authenticated_client.put(
            co_email1_co1_ws1_user1_url_path,
            co_email1_co1_ws1_user1_updated_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        co_email1_co1_ws1_user1.refresh_from_db()

        assert (co_email1_co1_ws1_user1.title ==
                co_email1_co1_ws1_user1_updated_valid_data["title"])

        assert (co_email1_co1_ws1_user1.email ==
                co_email1_co1_ws1_user1_updated_valid_data["email"])

    def test_partial_update_company_email_requires_authentication(
            self,
            api_client,
            co_email1_co1_ws1_user1,
            co_email1_co1_ws1_user1_url_path,
            co_email1_co1_ws1_user1_updated_valid_data
    ):

        response = api_client.patch(
            co_email1_co1_ws1_user1_url_path,
            co_email1_co1_ws1_user1_updated_valid_data,
            format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_company_email(
            self,
            authenticated_client,
            co_email1_co1_ws1_user1,
            co_email1_co1_ws1_user1_url_path,
            co_email1_co1_ws1_user1_updated_valid_data
    ):

        partial_update_api_data = co_email1_co1_ws1_user1_updated_valid_data.copy()
        partial_update_api_data.pop("title")

        old_title = co_email1_co1_ws1_user1.title

        response = authenticated_client.patch(
            co_email1_co1_ws1_user1_url_path,
            partial_update_api_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        co_email1_co1_ws1_user1.refresh_from_db()

        # Email address should be changed
        assert co_email1_co1_ws1_user1.email == partial_update_api_data["email"]

        # Title should be unchanged
        assert co_email1_co1_ws1_user1.title == old_title

    def test_delete_company_email_requires_authentication(
            self,
            api_client,
            co_email1_co1_ws1_user1_url_path,
    ):

        response = api_client.delete(co_email1_co1_ws1_user1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_company_email(
            self,
            authenticated_client,
            co_email1_co1_ws1_user1,
            co_email1_co1_ws1_user1_url_path,
    ):

        response = authenticated_client.delete(co_email1_co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert not (
            CompanyEmail.objects.filter(pk=co_email1_co1_ws1_user1.id).exists())
