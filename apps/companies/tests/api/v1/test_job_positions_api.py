import pytest
from rest_framework import status

from apps.companies.models import JobPosition

pytestmark = pytest.mark.django_db


# =========================================================
# LIST
# =========================================================

class TestJobPositionListAPIView:

    @pytest.fixture
    def url(self, base_api_url_path):
        return f"{base_api_url_path}job-positions/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_only_user_job_positions(
        self,
        authenticated_client,
        url,
        job_position1_user1,
        job_position1_user2,
    ):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {obj["id"] for obj in response.data["results"]}

        assert job_position1_user1.id in returned_ids
        assert job_position1_user2.id not in returned_ids


# =========================================================
# NESTED CREATE
# =========================================================

class TestNestedJobPositionCreateAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, co1_ws1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{co1_ws1_user1.workspace.workspace_id}/"
            f"companies/{co1_ws1_user1.id}/"
            f"job-positions/"
        )

    def test_requires_authentication(
        self,
        api_client,
        url,
        job_pos_user1_api_valid_data,
    ):
        response = api_client.post(url, job_pos_user1_api_valid_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_job_position_success(
        self,
        authenticated_client,
        url,
        job_pos_user1_api_valid_data,
    ):
        response = authenticated_client.post(
            url,
            job_pos_user1_api_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        obj = JobPosition.objects.get(pk=response.data["id"])

        assert obj.title == job_pos_user1_api_valid_data["title"]
        assert obj.description == job_pos_user1_api_valid_data["description"]

        assert set(obj.tasks.values_list("id", flat=True)) == set(
            job_pos_user1_api_valid_data["tasks"]
        )

        assert set(obj.requirements.values_list("id", flat=True)) == set(
            job_pos_user1_api_valid_data["requirements"]
        )

        assert set(obj.employment_types.values_list("id", flat=True)) == set(
            job_pos_user1_api_valid_data["employment_types"]
        )

    def test_invalid_payload_rejected(
        self,
        authenticated_client,
        url,
    ):
        response = authenticated_client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_create_in_foreign_company(
        self,
        authenticated_client,
        base_api_url_path,
        co1_ws1_user2,
        job_pos_user1_api_valid_data,
    ):
        url = (
            f"{base_api_url_path}workspaces/{co1_ws1_user2.workspace.workspace_id}/"
            f"companies/{co1_ws1_user2.id}/job-positions/"
        )

        response = authenticated_client.post(
            url,
            job_pos_user1_api_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


# =========================================================
# RETRIEVE (NESTED)
# =========================================================

class TestNestedJobPositionRetrieveAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, job_position1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{job_position1_user1.company.workspace.workspace_id}/"
            f"companies/{job_position1_user1.company.id}/"
            f"job-positions/{job_position1_user1.id}/"
        )

    def test_requires_authentication(self, api_client, url):
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieves_job_position(
        self,
        authenticated_client,
        url,
        job_position1_user1,
    ):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_position1_user1.id

    def test_returns_404_for_unknown_job_position(
        self,
        authenticated_client,
        url,
    ):
        response = authenticated_client.get(f"{url}999999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_forbidden_for_foreign_company(
        self,
        authenticated_client,
        base_api_url_path,
        workspace1_user2,
        job_position1_user2,
    ):
        url = (
            f"{base_api_url_path}workspaces/{workspace1_user2.workspace_id}/"
            f"companies/{job_position1_user2.company.id}/"
            f"job-positions/{job_position1_user2.id}/"
        )

        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


# =========================================================
# UPDATE (NESTED)
# =========================================================

class TestNestedJobPositionUpdateAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, job_position1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{job_position1_user1.company.workspace.workspace_id}/"
            f"companies/{job_position1_user1.company.id}/"
            f"job-positions/{job_position1_user1.id}/"
        )

    def test_requires_authentication(self, api_client, url):
        response = api_client.put(url, {}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_full_update_success(
        self,
        authenticated_client,
        url,
        job_position1_user1,
        job_pos_user1_api_updated_valid_data,
    ):
        response = authenticated_client.put(
            url,
            job_pos_user1_api_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        job_position1_user1.refresh_from_db()

        assert (job_position1_user1.title ==
                job_pos_user1_api_updated_valid_data["title"])

        assert (job_position1_user1.description ==
                job_pos_user1_api_updated_valid_data["description"])

        assert set(job_position1_user1.tasks.values_list("id", flat=True)) == set(
            job_pos_user1_api_updated_valid_data["tasks"]
        )

        assert (set(job_position1_user1.requirements.values_list("id", flat=True)) ==
                set(job_pos_user1_api_updated_valid_data["requirements"])
                )

        assert set(job_position1_user1.employment_types.values_list("id", flat=True)) == set(
            job_pos_user1_api_updated_valid_data["employment_types"]
        )

    def test_partial_update_success(
        self,
        authenticated_client,
        url,
        job_position1_user1,
        job_pos_user1_api_updated_valid_data,
    ):
        old_title = job_position1_user1.title

        payload = {
            "description": job_pos_user1_api_updated_valid_data["description"]
        }

        response = authenticated_client.patch(url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK

        job_position1_user1.refresh_from_db()

        assert job_position1_user1.description == payload["description"]
        assert job_position1_user1.title == old_title

    def test_invalid_update_payload(
        self,
        authenticated_client,
        url,
    ):
        response = authenticated_client.put(url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =========================================================
# DELETE (NESTED)
# =========================================================

class TestNestedJobPositionDeleteAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, job_position1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{job_position1_user1.company.workspace.workspace_id}/"
            f"companies/{job_position1_user1.company.id}/"
            f"job-positions/{job_position1_user1.id}/"
        )

    def test_requires_authentication(self, api_client, url):
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_success(
        self,
        authenticated_client,
        job_position1_user1,
        url,
    ):
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not JobPosition.objects.filter(pk=job_position1_user1.id).exists()

    def test_delete_unknown_object(
        self,
        authenticated_client,
        url,
    ):
        response = authenticated_client.delete(f"{url}999999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_idempotency(
        self,
        authenticated_client,
        job_position1_user1,
        url,
    ):
        authenticated_client.delete(url)
        response = authenticated_client.delete(url)

        assert response.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_204_NO_CONTENT,
        )
