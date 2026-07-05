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
def create_co1_ws1_user1_url_path(
    base_api_url_path,
    workspace1_user1,
):

    return (
        f"{base_api_url_path}"
        f"workspaces/{workspace1_user1.workspace_id}/companies/"
    )


@pytest.fixture
def co1_ws1_user1_url_path(
    create_co1_ws1_user1_url_path,
    co1_ws1_user1,
):

    return (
        f"{create_co1_ws1_user1_url_path}"
        f"{co1_ws1_user1.id}/"
    )


# =========================================================
# Company List API
# =========================================================

class TestCompanyListAPIView:

    def test_requires_authentication(
        self,
        api_client,
        company_list_url_path,
    ):

        response = api_client.get(company_list_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_only_authenticated_user_companies(
        self,
        authenticated_client,
        company_list_url_path,
        co1_ws1_user1,
        co1_ws1_user2,
    ):

        response = authenticated_client.get(company_list_url_path)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {
            item["id"]
            for item in response.data["results"]
        }

        assert co1_ws1_user1.id in returned_ids
        assert co1_ws1_user2.id not in returned_ids

    def test_filters_by_workspace(
        self,
        authenticated_client,
        company_list_url_path,
        workspace1_user1,
        co1_ws1_user1,
        co1_ws2_user1,
    ):

        response = authenticated_client.get(
            company_list_url_path,
            {
                "workspace_id": workspace1_user1.workspace_id,
            },
        )

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {
            item["id"]
            for item in response.data["results"]
        }

        assert co1_ws1_user1.id in returned_ids
        assert co1_ws2_user1.id not in returned_ids

    def test_retrieve_company(
        self,
        authenticated_client,
        company_list_url_path,
        co1_ws1_user1,
    ):

        response = authenticated_client.get(
            f"{company_list_url_path}{co1_ws1_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co1_ws1_user1.id

    def test_returns_404_for_unknown_company(
        self,
        authenticated_client,
        company_list_url_path,
    ):

        response = authenticated_client.get(
            f"{company_list_url_path}99999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_cannot_access_another_users_company(
        self,
        authenticated_client,
        company_list_url_path,
        co1_ws1_user2,
    ):

        response = authenticated_client.get(
            f"{company_list_url_path}{co1_ws1_user2.id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"]["code"] == "access_denied"


# =========================================================
# Nested Company Create API
# =========================================================

class TestNestedCompanyCreateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        create_co1_ws1_user1_url_path,
        co1_ws1_user1_valid_data,
    ):

        response = api_client.post(
            create_co1_ws1_user1_url_path,
            co1_ws1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_company(
        self,
        authenticated_client,
        create_co1_ws1_user1_url_path,
        co1_ws1_user1_valid_data,
        workspace1_user1,
    ):

        response = authenticated_client.post(
            create_co1_ws1_user1_url_path,
            co1_ws1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        assert response.data["name"] == co1_ws1_user1_valid_data["name"]
        assert response.data["website"] == co1_ws1_user1_valid_data["website"]

        assert Company.objects.filter(
            workspace=workspace1_user1,
            name=co1_ws1_user1_valid_data["name"],
        ).exists()

    def test_cannot_create_company_in_another_users_workspace(
        self,
        authenticated_client,
        workspace1_user2,
        co1_ws1_user1_valid_data,
        base_api_url_path,
    ):

        url = (
            f"{base_api_url_path}"
            f"workspaces/{workspace1_user2.workspace_id}/companies/"
        )

        response = authenticated_client.post(
            url,
            co1_ws1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"]["code"] == "access_denied"


# =========================================================
# Company Retrieve (nested context)
# =========================================================

class TestNestedCompanyRetrieveAPIView:

    def test_requires_authentication(
        self,
        api_client,
        co1_ws1_user1_url_path,
    ):

        response = api_client.get(co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_company(
        self,
        authenticated_client,
        co1_ws1_user1,
        co1_ws1_user1_url_path,
    ):

        response = authenticated_client.get(co1_ws1_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == co1_ws1_user1.id

    def test_returns_404_for_unknown_company(
        self,
        authenticated_client,
        create_co1_ws1_user1_url_path,
    ):

        url = f"{create_co1_ws1_user1_url_path}9999999/"

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_cannot_access_another_users_company(
        self,
        authenticated_client,
        workspace1_user2,
        co1_ws1_user2,
        base_api_url_path,
    ):

        url = (
            f"{base_api_url_path}"
            f"workspaces/{workspace1_user2.workspace_id}/"
            f"companies/{co1_ws1_user2.id}/"
        )

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"]["code"] == "access_denied"


# =========================================================
# Nested Company Update API
# =========================================================

class TestNestedCompanyUpdateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        co1_ws1_user1_url_path,
        co1_ws1_user1_updated_valid_data,
    ):

        response = api_client.put(
            co1_ws1_user1_url_path,
            co1_ws1_user1_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_company(
        self,
        authenticated_client,
        co1_ws1_user1,
        co1_ws1_user1_url_path,
        co1_ws1_user1_updated_valid_data,
    ):

        response = authenticated_client.put(
            co1_ws1_user1_url_path,
            co1_ws1_user1_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        co1_ws1_user1.refresh_from_db()

        assert co1_ws1_user1.name == co1_ws1_user1_updated_valid_data["name"]
        assert co1_ws1_user1.website == co1_ws1_user1_updated_valid_data["website"]

    def test_partial_update_requires_authentication(
        self,
        api_client,
        co1_ws1_user1_url_path,
    ):

        response = api_client.patch(
            co1_ws1_user1_url_path,
            {"name": "New Name"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_company(
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

    def test_returns_404_for_unknown_company_update(
        self,
        authenticated_client,
        create_co1_ws1_user1_url_path,
    ):

        url = f"{create_co1_ws1_user1_url_path}9999999/"

        response = authenticated_client.put(
            url,
            {"name": "X", "website": "https://x.com"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_cannot_update_another_users_company(
        self,
        authenticated_client,
        workspace1_user2,
        co1_ws1_user2,
        base_api_url_path,
    ):

        url = (
            f"{base_api_url_path}"
            f"workspaces/{workspace1_user2.workspace_id}/"
            f"companies/{co1_ws1_user2.id}/"
        )

        response = authenticated_client.put(
            url,
            {"name": "Hack", "website": "https://hack.com"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"]["code"] == "access_denied"


# =========================================================
# Nested Company Delete API
# =========================================================

class TestNestedCompanyDeleteAPIView:

    def test_requires_authentication(
        self,
        api_client,
        co1_ws1_user1_url_path,
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

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Company.objects.filter(
            pk=co1_ws1_user1.id
        ).exists()

    def test_returns_404_for_unknown_company(
        self,
        authenticated_client,
        create_co1_ws1_user1_url_path,
    ):

        url = f"{create_co1_ws1_user1_url_path}9999999/"

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_cannot_delete_another_users_company(
        self,
        authenticated_client,
        workspace1_user2,
        co1_ws1_user2,
        base_api_url_path,
    ):

        url = (
            f"{base_api_url_path}"
            f"workspaces/{workspace1_user2.workspace_id}/"
            f"companies/{co1_ws1_user2.id}/"
        )

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"]["code"] == "access_denied"
