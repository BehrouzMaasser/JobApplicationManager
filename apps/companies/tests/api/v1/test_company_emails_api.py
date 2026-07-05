import pytest
from rest_framework import status

from apps.companies.models import CompanyEmail

pytestmark = pytest.mark.django_db


# =========================================================
# LIST
# =========================================================

class TestCompanyEmailListAPIView:

    @pytest.fixture
    def url(self, base_api_url_path):
        return f"{base_api_url_path}company-emails/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_company_emails(
        self,
        authenticated_client,
        url,
        co_email1_co1_ws1_user1,
    ):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {item["id"] for item in response.data["results"]}
        assert co_email1_co1_ws1_user1.id in returned_ids


# =========================================================
# RETRIEVE (global endpoint)
# =========================================================

class TestCompanyEmailRetrieveAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, co_email1_co1_ws1_user1):
        return f"{base_api_url_path}company-emails/{co_email1_co1_ws1_user1.id}/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieves_company_email(
        self,
        authenticated_client,
        url,
        co_email1_co1_ws1_user1,
    ):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co_email1_co1_ws1_user1.id

    def test_returns_404_for_unknown_email(
            self, authenticated_client, base_api_url_path
    ):
        url = f"{base_api_url_path}company-emails/999999/"
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


# =========================================================
# NESTED CREATE
# =========================================================

class TestNestedCompanyEmailCreateAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, co_email1_co1_ws1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{co_email1_co1_ws1_user1.company.workspace.workspace_id}/"
            f"companies/{co_email1_co1_ws1_user1.company.id}/company-emails/"
        )

    def test_requires_authentication(
            self, api_client, url, co_email1_co1_ws1_user1_valid_data
    ):
        response = api_client.post(
            url, co_email1_co1_ws1_user1_valid_data, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_creates_company_email(
        self,
        authenticated_client,
        url,
        co_email1_co1_ws1_user1_valid_data,
    ):
        response = authenticated_client.post(
            url, co_email1_co1_ws1_user1_valid_data, format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        obj = CompanyEmail.objects.get(pk=response.data["id"])

        assert obj.title == co_email1_co1_ws1_user1_valid_data["title"]
        assert obj.email == co_email1_co1_ws1_user1_valid_data["email"]


# =========================================================
# NESTED RETRIEVE
# =========================================================

class TestNestedCompanyEmailRetrieveAPIView:

    @pytest.fixture
    def base_url(self, base_api_url_path, co_email1_co1_ws1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{co_email1_co1_ws1_user1.company.workspace.workspace_id}/"
            f"companies/{co_email1_co1_ws1_user1.company.id}/company-emails/"
        )

    def test_requires_authentication(
            self, api_client, base_url, co_email1_co1_ws1_user1
    ):
        response = api_client.get(f"{base_url}{co_email1_co1_ws1_user1.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieves_company_email(
        self,
        authenticated_client,
        base_url,
        co_email1_co1_ws1_user1,
    ):
        response = authenticated_client.get(
            f"{base_url}{co_email1_co1_ws1_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co_email1_co1_ws1_user1.id

    def test_returns_404_for_unknown_email(self, authenticated_client, base_url):
        response = authenticated_client.get(f"{base_url}999999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


# =========================================================
# NESTED UPDATE
# =========================================================

class TestNestedCompanyEmailUpdateAPIView:

    @pytest.fixture
    def base_url(self, base_api_url_path, co_email1_co1_ws1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{co_email1_co1_ws1_user1.company.workspace.workspace_id}/"
            f"companies/{co_email1_co1_ws1_user1.company.id}/company-emails/"
        )

    def test_requires_authentication(
            self, api_client, base_url, co_email1_co1_ws1_user1
    ):
        response = api_client.put(f"{base_url}{co_email1_co1_ws1_user1.id}/", {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_updates_company_email(
        self,
        authenticated_client,
        base_url,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_updated_valid_data,
    ):
        response = authenticated_client.put(
            f"{base_url}{co_email1_co1_ws1_user1.id}/",
            co_email1_co1_ws1_user1_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        co_email1_co1_ws1_user1.refresh_from_db()

        assert (co_email1_co1_ws1_user1.title ==
                co_email1_co1_ws1_user1_updated_valid_data["title"])

        assert (co_email1_co1_ws1_user1.email ==
                co_email1_co1_ws1_user1_updated_valid_data["email"])

    def test_partial_update_company_email(
        self,
        authenticated_client,
        base_url,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_updated_valid_data,
    ):
        old_title = co_email1_co1_ws1_user1.title

        payload = {
            "email": co_email1_co1_ws1_user1_updated_valid_data["email"]
        }

        response = authenticated_client.patch(
            f"{base_url}{co_email1_co1_ws1_user1.id}/",
            payload,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        co_email1_co1_ws1_user1.refresh_from_db()

        assert co_email1_co1_ws1_user1.email == payload["email"]
        assert co_email1_co1_ws1_user1.title == old_title


# =========================================================
# NESTED DELETE
# =========================================================

class TestNestedCompanyEmailDeleteAPIView:

    @pytest.fixture
    def base_url(self, base_api_url_path, co_email1_co1_ws1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{co_email1_co1_ws1_user1.company.workspace.workspace_id}/"
            f"companies/{co_email1_co1_ws1_user1.company.id}/company-emails/"
        )

    def test_requires_authentication(
            self, api_client, base_url, co_email1_co1_ws1_user1
    ):
        response = api_client.delete(f"{base_url}{co_email1_co1_ws1_user1.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_deletes_company_email(
        self,
        authenticated_client,
        base_url,
        co_email1_co1_ws1_user1,
    ):
        response = authenticated_client.delete(
            f"{base_url}{co_email1_co1_ws1_user1.id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CompanyEmail.objects.filter(
            pk=co_email1_co1_ws1_user1.id
        ).exists()
