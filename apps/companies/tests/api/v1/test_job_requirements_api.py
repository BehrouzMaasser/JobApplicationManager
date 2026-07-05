import pytest
from rest_framework import status

from apps.companies.models import JobRequirement

pytestmark = pytest.mark.django_db


# =========================================================
# LIST
# =========================================================
class TestJobRequirementListAPIView:

    @pytest.fixture
    def job_requirements_url_path(self, base_api_url_path):
        return f"{base_api_url_path}job-requirements/"

    def test_requires_authentication(
        self,
        api_client,
        job_requirements_url_path,
    ):
        response = api_client.get(job_requirements_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_job_requirements(
        self,
        authenticated_client,
        job_requirements_url_path,
        job_requirement1_user1,
    ):
        response = authenticated_client.get(job_requirements_url_path)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {item["id"] for item in response.data["results"]}
        assert job_requirement1_user1.id in returned_ids


# =========================================================
# RETRIEVE (global endpoint)
# =========================================================
class TestJobRequirementRetrieveAPIView:

    @pytest.fixture
    def job_requirements_url_path(self, base_api_url_path):
        return f"{base_api_url_path}job-requirements/"

    def test_requires_authentication(
        self,
        api_client,
        job_requirements_url_path,
        job_requirement1_user1,
    ):
        response = api_client.get(
            f"{job_requirements_url_path}{job_requirement1_user1.id}/"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_job_requirement(
        self,
        authenticated_client,
        job_requirements_url_path,
        job_requirement1_user1,
    ):
        response = authenticated_client.get(
            f"{job_requirements_url_path}{job_requirement1_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_requirement1_user1.id

    def test_returns_404_for_unknown_job_requirement(
        self,
        authenticated_client,
        job_requirements_url_path,
    ):
        response = authenticated_client.get(
            f"{job_requirements_url_path}999999/"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


# =========================================================
# CREATE
# =========================================================
class TestJobRequirementCreateAPIView:

    @pytest.fixture
    def job_requirements_url_path(self, base_api_url_path):
        return f"{base_api_url_path}job-requirements/"

    def test_requires_authentication(
        self,
        api_client,
        job_requirements_url_path,
        job_requirement1_user1_valid_data,
    ):
        response = api_client.post(
            job_requirements_url_path,
            job_requirement1_user1_valid_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_job_requirement(
        self,
        authenticated_client,
        job_requirements_url_path,
        job_requirement1_user1_valid_data,
    ):
        response = authenticated_client.post(
            job_requirements_url_path,
            job_requirement1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        assert JobRequirement.objects.filter(
            id=response.data["id"]
        ).exists()

        assert response.data["title"] == job_requirement1_user1_valid_data["title"]
        assert (response.data["description"] ==
                job_requirement1_user1_valid_data["description"])


# =========================================================
# UPDATE
# =========================================================
class TestJobRequirementUpdateAPIView:

    @pytest.fixture
    def job_requirements_url_path(self, base_api_url_path):
        return f"{base_api_url_path}job-requirements/"

    def test_update_requires_authentication(
        self,
        api_client,
        job_requirements_url_path,
        job_requirement1_user1,
        job_requirement1_user1_updated_valid_data,
    ):
        response = api_client.put(
            f"{job_requirements_url_path}{job_requirement1_user1.id}/",
            job_requirement1_user1_updated_valid_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_job_requirement(
        self,
        authenticated_client,
        job_requirement1_user1,
        job_requirements_url_path,
        job_requirement1_user1_updated_valid_data,
    ):
        response = authenticated_client.put(
            f"{job_requirements_url_path}{job_requirement1_user1.id}/",
            job_requirement1_user1_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        job_requirement1_user1.refresh_from_db()

        assert (job_requirement1_user1.title ==
                job_requirement1_user1_updated_valid_data["title"])

        assert (job_requirement1_user1.description ==
                job_requirement1_user1_updated_valid_data["description"])

    def test_partial_update_job_requirement(
        self,
        authenticated_client,
        job_requirements_url_path,
        job_requirement1_user1,
        job_requirement1_user1_updated_valid_data,
    ):
        old_title = job_requirement1_user1.title

        partial_data = {
            "description": job_requirement1_user1_updated_valid_data["description"]
        }

        response = authenticated_client.patch(
            f"{job_requirements_url_path}{job_requirement1_user1.id}/",
            partial_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        job_requirement1_user1.refresh_from_db()

        assert job_requirement1_user1.description == partial_data["description"]
        assert job_requirement1_user1.title == old_title


# =========================================================
# DELETE
# =========================================================
class TestJobRequirementDeleteAPIView:

    @pytest.fixture
    def job_requirements_url_path(self, base_api_url_path):
        return f"{base_api_url_path}job-requirements/"

    def test_delete_requires_authentication(
        self,
        api_client,
        job_requirements_url_path,
        job_requirement1_user1,
    ):
        response = api_client.delete(
            f"{job_requirements_url_path}{job_requirement1_user1.id}/"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_job_requirement(
        self,
        authenticated_client,
        job_requirement1_user1,
        job_requirements_url_path,
    ):
        response = authenticated_client.delete(
            f"{job_requirements_url_path}{job_requirement1_user1.id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not JobRequirement.objects.filter(
            id=job_requirement1_user1.id
        ).exists()
