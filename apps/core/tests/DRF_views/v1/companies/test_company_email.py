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

    def test_does_not_return_foreign_company_emails(
        self,
        authenticated_client,
        url,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user2,
    ):
        response = authenticated_client.get(url)

        returned_ids = {item["id"] for item in response.data["results"]}
        assert co_email1_co1_ws1_user2.id not in returned_ids


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
        self,
        authenticated_client,
        base_api_url_path,
    ):
        url = f"{base_api_url_path}company-emails/999999/"
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"


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
        self,
        api_client,
        url,
        co_email1_co1_ws1_user1_api_v1_valid_data,
    ):
        response = api_client.post(
            url, co_email1_co1_ws1_user1_api_v1_valid_data, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_creates_company_email(
        self,
        authenticated_client,
        url,
        co_email1_co1_ws1_user1_api_v1_valid_data,
        co_email1_co1_ws1_user1,
    ):
        response = authenticated_client.post(
            url,
            co_email1_co1_ws1_user1_api_v1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        obj = CompanyEmail.objects.get(pk=response.data["id"])
        assert obj.title == co_email1_co1_ws1_user1_api_v1_valid_data["title"]
        assert obj.email == co_email1_co1_ws1_user1_api_v1_valid_data["email"]

        # DB persistence safety check
        assert CompanyEmail.objects.filter(id=response.data["id"]).exists()

    def test_cannot_create_in_foreign_company(
        self,
        authenticated_client,
        base_api_url_path,
        co1_ws1_user2,
        co_email1_co1_ws1_user1_api_v1_valid_data,
    ):
        url = (
            f"{base_api_url_path}workspaces/{co1_ws1_user2.workspace.workspace_id}/"
            f"companies/{co1_ws1_user2.pk}/company-emails/"
        )

        response = authenticated_client.post(
            url,
            co_email1_co1_ws1_user1_api_v1_valid_data,
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

class TestNestedCompanyEmailRetrieveAPIView:

    @pytest.fixture
    def base_url(self, base_api_url_path, co_email1_co1_ws1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{co_email1_co1_ws1_user1.company.workspace.workspace_id}/"
            f"companies/{co_email1_co1_ws1_user1.company.id}/company-emails/"
        )

    def test_requires_authentication(
        self,
        api_client,
        base_url,
        co_email1_co1_ws1_user1,
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

    def test_returns_404_for_unknown_email(
        self,
        authenticated_client,
        base_url,
    ):
        response = authenticated_client.get(f"{base_url}999999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"


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
        self,
        api_client,
        base_url,
        co_email1_co1_ws1_user1,
    ):
        response = api_client.put(
            f"{base_url}{co_email1_co1_ws1_user1.id}/",
            {},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_full_update(
        self,
        authenticated_client,
        base_url,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_updated_api_v1_valid_data,
    ):
        response = authenticated_client.put(
            f"{base_url}{co_email1_co1_ws1_user1.id}/",
            co_email1_co1_ws1_user1_updated_api_v1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        co_email1_co1_ws1_user1.refresh_from_db()

        assert (co_email1_co1_ws1_user1.title ==
                co_email1_co1_ws1_user1_updated_api_v1_valid_data["title"])

        assert (co_email1_co1_ws1_user1.email ==
                co_email1_co1_ws1_user1_updated_api_v1_valid_data["email"])

    def test_partial_update(
        self,
        authenticated_client,
        base_url,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_updated_api_v1_valid_data,
    ):
        old_title = co_email1_co1_ws1_user1.title

        payload = {"email": co_email1_co1_ws1_user1_updated_api_v1_valid_data["email"]}

        response = authenticated_client.patch(
            f"{base_url}{co_email1_co1_ws1_user1.id}/",
            payload,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        co_email1_co1_ws1_user1.refresh_from_db()

        assert co_email1_co1_ws1_user1.email == payload["email"]
        assert co_email1_co1_ws1_user1.title == old_title

    def test_patch_requires_authentication(
        self,
        api_client,
        base_url,
        co_email1_co1_ws1_user1,
    ):
        response = api_client.patch(
            f"{base_url}{co_email1_co1_ws1_user1.id}/",
            {"email": "x@test.com"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


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
        self,
        api_client,
        base_url,
        co_email1_co1_ws1_user1,
    ):
        response = api_client.delete(f"{base_url}{co_email1_co1_ws1_user1.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_success(
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

    def test_delete_foreign_company_email_forbidden(
        self,
        authenticated_client,
        base_api_url_path,
        co_email1_co1_ws1_user2,
    ):
        url = (
            f"{base_api_url_path}workspaces/"
            f"{co_email1_co1_ws1_user2.company.workspace.workspace_id}/companies/"
            f"{co_email1_co1_ws1_user2.company.pk}/company-emails/"
            f"{co_email1_co1_ws1_user2.id}/"
        )

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_delete_unknown_email(
        self,
        authenticated_client,
        base_url,
    ):
        response = authenticated_client.delete(f"{base_url}999999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_delete_idempotency(
        self,
        authenticated_client,
        base_url,
        co_email1_co1_ws1_user1,
    ):
        authenticated_client.delete(f"{base_url}{co_email1_co1_ws1_user1.id}/")

        response = authenticated_client.delete(
            f"{base_url}{co_email1_co1_ws1_user1.id}/"
        )

        assert response.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_204_NO_CONTENT,
        )
