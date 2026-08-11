import pytest
from rest_framework import status

from apps.companies.models import JobRequirement

pytestmark = pytest.mark.django_db


# =========================================================
# LIST
# =========================================================

class TestJobRequirementListAPIView:

    @pytest.fixture
    def url(self, base_api_url_path):
        return f"{base_api_url_path}job-requirements/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_job_requirements(
        self,
        authenticated_client,
        url,
        job_requirement1_user1,
    ):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {item["id"] for item in response.data["results"]}
        assert job_requirement1_user1.id in returned_ids

    def test_does_not_return_foreign_job_requirements(
        self,
        authenticated_client,
        url,
        job_requirement1_user1,
        job_requirement1_user2,
    ):
        response = authenticated_client.get(url)

        returned_ids = {item["id"] for item in response.data["results"]}
        assert job_requirement1_user2.id not in returned_ids


# =========================================================
# RETRIEVE (GLOBAL)
# =========================================================

class TestJobRequirementRetrieveAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, job_requirement1_user1):
        return f"{base_api_url_path}job-requirements/{job_requirement1_user1.id}/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieves_job_requirement(
        self,
        authenticated_client,
        url,
        job_requirement1_user1,
    ):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_requirement1_user1.id

    def test_returns_404_for_unknown_job_requirement(
        self,
        authenticated_client,
        base_api_url_path,
    ):
        response = authenticated_client.get(
            f"{base_api_url_path}job-requirements/999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"


# =========================================================
# CREATE
# =========================================================

class TestJobRequirementCreateAPIView:

    @pytest.fixture
    def url(self, base_api_url_path):
        return f"{base_api_url_path}job-requirements/"

    def test_requires_authentication(
        self,
        api_client,
        url,
        job_requirement1_user1_valid_data,
    ):
        response = api_client.post(
            url, job_requirement1_user1_valid_data, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_job_requirement_success(
        self,
        authenticated_client,
        url,
        job_requirement1_user1_valid_data,
    ):
        response = authenticated_client.post(
            url,
            job_requirement1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        obj = JobRequirement.objects.get(pk=response.data["id"])

        assert obj.title == job_requirement1_user1_valid_data["title"]
        assert obj.description == job_requirement1_user1_valid_data["description"]

        assert JobRequirement.objects.filter(pk=response.data["id"]).exists()

    def test_invalid_payload_rejected(
        self,
        authenticated_client,
        url,
    ):
        response = authenticated_client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =========================================================
# UPDATE
# =========================================================

class TestJobRequirementUpdateAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, job_requirement1_user1):
        return f"{base_api_url_path}job-requirements/{job_requirement1_user1.id}/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.put(url, {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_full_update_success(
        self,
        authenticated_client,
        job_requirement1_user1,
        url,
        job_requirement1_user1_updated_valid_data,
    ):
        response = authenticated_client.put(
            url,
            job_requirement1_user1_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        job_requirement1_user1.refresh_from_db()

        assert (job_requirement1_user1.title ==
                job_requirement1_user1_updated_valid_data["title"])

        assert (job_requirement1_user1.description ==
                job_requirement1_user1_updated_valid_data["description"])

    def test_partial_update_success(
        self,
        authenticated_client,
        job_requirement1_user1,
        url,
        job_requirement1_user1_updated_valid_data,
    ):
        old_title = job_requirement1_user1.title

        payload = {
            "description": job_requirement1_user1_updated_valid_data["description"]
        }

        response = authenticated_client.patch(url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK

        job_requirement1_user1.refresh_from_db()

        assert job_requirement1_user1.description == payload["description"]
        assert job_requirement1_user1.title == old_title

    def test_returns_404_for_unknown_update(
        self,
        authenticated_client,
        base_api_url_path,
        job_requirement1_user1_updated_valid_data,
    ):
        response = authenticated_client.put(
            f"{base_api_url_path}job-requirements/999999/",
            job_requirement1_user1_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"


# =========================================================
# DELETE
# =========================================================

class TestJobRequirementDeleteAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, job_requirement1_user1):
        return f"{base_api_url_path}job-requirements/{job_requirement1_user1.id}/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_success(
        self,
        authenticated_client,
        job_requirement1_user1,
        url,
    ):
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not JobRequirement.objects.filter(
            pk=job_requirement1_user1.id
        ).exists()

    def test_delete_unknown_object(
        self,
        authenticated_client,
        base_api_url_path,
    ):
        response = authenticated_client.delete(
            f"{base_api_url_path}job-requirements/999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_delete_idempotency(
        self,
        authenticated_client,
        job_requirement1_user1,
        url,
    ):
        authenticated_client.delete(url)
        response = authenticated_client.delete(url)

        assert response.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_204_NO_CONTENT,
        )
