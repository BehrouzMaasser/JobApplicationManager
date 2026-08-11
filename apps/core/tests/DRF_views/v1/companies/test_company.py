import pytest
from rest_framework import status

from apps.companies.models import Company

pytestmark = pytest.mark.django_db


# =========================================================
# Fixtures
# =========================================================

@pytest.fixture
def company_list_url_path(base_api_url_path):
    return f"{base_api_url_path}companies/"


@pytest.fixture
def create_company_url_path(base_api_url_path, workspace1_user1):
    return (f"{base_api_url_path}workspaces/{workspace1_user1.workspace_id}/"
            f"companies/")


@pytest.fixture
def company_detail_url_path(company_list_url_path, co1_ws1_user1):
    return f"{company_list_url_path}{co1_ws1_user1.id}/"


@pytest.fixture
def co1_ws1_user1_url_path(co1_ws1_user1, base_api_url_path):

    return (f"{base_api_url_path}workspaces/{co1_ws1_user1.workspace.workspace_id}/"
            f"companies/{co1_ws1_user1.id}/")


# =========================================================
# COMPANY LIST API
# =========================================================

class TestCompanyListAPIView:

    def test_requires_authentication(self, api_client, company_list_url_path):
        response = api_client.get(company_list_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_only_user_companies(
        self,
        authenticated_client,
        company_list_url_path,
        co1_ws1_user1,
        co1_ws1_user2,
    ):
        response = authenticated_client.get(company_list_url_path)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {item["id"] for item in response.data["results"]}

        assert co1_ws1_user1.id in returned_ids
        assert co1_ws1_user2.id not in returned_ids

    def test_list_pagination_structure(
            self, authenticated_client, company_list_url_path
    ):
        response = authenticated_client.get(company_list_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data


# =========================================================
# COMPANY RETRIEVE (FLAT)
# =========================================================

class TestCompanyRetrieveAPIView:

    def test_retrieve_company_success(
        self,
        authenticated_client,
        company_detail_url_path,
        co1_ws1_user1,
    ):
        response = authenticated_client.get(company_detail_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co1_ws1_user1.id

    def test_returns_404_for_unknown_company(
            self, authenticated_client, company_list_url_path
    ):
        response = authenticated_client.get(f"{company_list_url_path}99999999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_cannot_access_foreign_company(
        self,
        authenticated_client,
        company_list_url_path,
        co1_ws1_user2,
    ):
        response = authenticated_client.get(
            f"{company_list_url_path}{co1_ws1_user2.id}/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"


# =========================================================
# NESTED CREATE
# =========================================================

class TestNestedCompanyCreateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        create_company_url_path,
        co1_ws1_user1_api_v1_valid_data,
    ):
        response = api_client.post(
            create_company_url_path, co1_ws1_user1_api_v1_valid_data, format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_company_success(
        self,
        authenticated_client,
        create_company_url_path,
        co1_ws1_user1_api_v1_valid_data,
        workspace1_user1,
    ):
        response = authenticated_client.post(
            create_company_url_path,
            co1_ws1_user1_api_v1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert response.data["name"] == co1_ws1_user1_api_v1_valid_data["name"]
        assert response.data["website"] == co1_ws1_user1_api_v1_valid_data["website"]

        assert Company.objects.filter(
            workspace=workspace1_user1,
            name=co1_ws1_user1_api_v1_valid_data["name"],
        ).exists()

    def test_cannot_create_in_foreign_workspace(
        self,
        authenticated_client,
        base_api_url_path,
        workspace1_user2,
        co1_ws1_user1_api_v1_valid_data,
    ):
        url = (f"{base_api_url_path}workspaces/{workspace1_user2.workspace_id}/"
               f"companies/")

        response = authenticated_client.post(
            url, co1_ws1_user1_api_v1_valid_data, format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_payload_rejected(
        self,
        authenticated_client,
        create_company_url_path,
    ):
        response = authenticated_client.post(
            create_company_url_path, {}, format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =========================================================
# NESTED RETRIEVE
# =========================================================

class TestNestedCompanyRetrieveAPIView:

    def test_retrieve_success(
        self,
        authenticated_client,
        co1_ws1_user1_url_path,
        co1_ws1_user1,
    ):
        response = authenticated_client.get(co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co1_ws1_user1.id

    def test_returns_404_for_unknown_company(
        self,
        authenticated_client,
        create_company_url_path,
    ):
        response = authenticated_client.get(f"{create_company_url_path}9999999/")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_forbidden_for_foreign_workspace_company(
        self,
        authenticated_client,
        base_api_url_path,
        workspace1_user2,
        co1_ws1_user2,
    ):
        url = (f"{base_api_url_path}workspaces/{workspace1_user2.workspace_id}/"
               f"companies/{co1_ws1_user2.id}/")

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"


# =========================================================
# NESTED UPDATE / PATCH
# =========================================================

class TestNestedCompanyUpdateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        co1_ws1_user1_url_path,
        co1_ws1_user1_updated_api_v1_valid_data,
    ):
        response = api_client.put(
            co1_ws1_user1_url_path, co1_ws1_user1_updated_api_v1_valid_data, format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_full_update_success(
        self,
        authenticated_client,
        co1_ws1_user1,
        co1_ws1_user1_url_path,
        co1_ws1_user1_updated_api_v1_valid_data,
    ):
        response = authenticated_client.put(
            co1_ws1_user1_url_path,
            co1_ws1_user1_updated_api_v1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        co1_ws1_user1.refresh_from_db()
        assert co1_ws1_user1.name == co1_ws1_user1_updated_api_v1_valid_data["name"]
        assert co1_ws1_user1.website == co1_ws1_user1_updated_api_v1_valid_data["website"]

    def test_partial_update_success(
        self,
        authenticated_client,
        co1_ws1_user1,
        co1_ws1_user1_url_path,
    ):
        old_name = co1_ws1_user1.name

        response = authenticated_client.patch(
            co1_ws1_user1_url_path,
            {"website": "https://updated.com"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        co1_ws1_user1.refresh_from_db()

        assert co1_ws1_user1.website == "https://updated.com"
        assert co1_ws1_user1.name == old_name

    def test_put_requires_all_required_fields(
        self,
        authenticated_client,
        co1_ws1_user1_url_path,
    ):
        response = authenticated_client.put(
            co1_ws1_user1_url_path,
            {"website": "https://updated.com"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_update_foreign_company(
        self,
        authenticated_client,
        base_api_url_path,
        workspace1_user2,
        co1_ws1_user2,
    ):
        url = (f"{base_api_url_path}workspaces/{workspace1_user2.workspace_id}/"
               f"companies/{co1_ws1_user2.id}/")

        response = authenticated_client.put(
            url,
            {"name": "Hack", "website": "https://hack.com"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"


# =========================================================
# NESTED DELETE
# =========================================================

class TestNestedCompanyDeleteAPIView:

    def test_requires_authentication(self, api_client, co1_ws1_user1_url_path):
        response = api_client.delete(co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_success(
            self, authenticated_client, co1_ws1_user1, co1_ws1_user1_url_path
    ):
        response = authenticated_client.delete(co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Company.objects.filter(pk=co1_ws1_user1.id).exists()

    def test_delete_idempotency_or_not_found(
        self,
        authenticated_client,
        co1_ws1_user1,
        co1_ws1_user1_url_path,
    ):
        authenticated_client.delete(co1_ws1_user1_url_path)

        response = authenticated_client.delete(co1_ws1_user1_url_path)

        assert response.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_204_NO_CONTENT,
        )

    def test_cannot_delete_foreign_company(
        self,
        authenticated_client,
        base_api_url_path,
        workspace1_user2,
        co1_ws1_user2,
    ):
        url = (f"{base_api_url_path}workspaces/{workspace1_user2.workspace_id}/"
               f"companies/{co1_ws1_user2.id}/")

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"
