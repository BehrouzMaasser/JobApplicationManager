import pytest
from rest_framework import status

from apps.companies.models import JobRequirement

pytestmark = pytest.mark.django_db


class TestJobRequirementAPI:

    @pytest.fixture
    def job_requirements_url_path(self, base_api_url_path):

        return f"{base_api_url_path}job-requirements/"

    @pytest.fixture
    def job_requirement_user1_url_path(
            self,  job_requirements_url_path, job_requirement_user1
    ):

        return f"{job_requirements_url_path}{job_requirement_user1.id}/"

    # List View Tests

    def test_list_requires_authentication(
            self, api_client, job_requirements_url_path
    ):

        response = api_client.get(job_requirements_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_job_requirements(
            self,
            authenticated_client,
            job_requirements_url_path,
            job_requirement_user1
    ):

        response = authenticated_client.get(job_requirements_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_retrieve_job_requirement_requires_authentication(
            self,
            api_client,
            job_requirement_user1_url_path,
            job_requirement_user1
    ):

        response = api_client.get(job_requirement_user1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_job_requirement(
            self,
            authenticated_client,
            job_requirement_user1_url_path,
            job_requirement_user1
    ):

        response = authenticated_client.get(job_requirement_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_requirement_user1.id

    def test_create_job_requirement_requires_authentication(
            self,
            api_client,
            job_requirements_url_path,
            job_requirement_user1_valid_data,
    ):

        response = api_client.post(
            job_requirements_url_path,
            job_requirement_user1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_job_requirement(
            self,
            authenticated_client,
            job_requirements_url_path,
            job_requirement_user1_valid_data,
    ):

        response = authenticated_client.post(
            job_requirements_url_path,
            job_requirement_user1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert JobRequirement.objects.filter(pk=response.data["id"]).exists()

        assert (response.data["title"] ==
                job_requirement_user1_valid_data["title"])

        assert (response.data["description"] ==
                job_requirement_user1_valid_data["description"])

    def test_update_job_requirement_requires_authentication(
            self,
            api_client,
            job_requirement_user1_url_path,
            job_requirement_user1_updated_valid_data,
    ):

        response = api_client.put(
            job_requirement_user1_url_path,
            job_requirement_user1_updated_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_job_requirement(
            self,
            authenticated_client,
            job_requirement_user1,
            job_requirement_user1_url_path,
            job_requirement_user1_updated_valid_data,
    ):

        response = authenticated_client.put(
            job_requirement_user1_url_path,
            job_requirement_user1_updated_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        job_requirement_user1.refresh_from_db()

        assert (job_requirement_user1.title ==
                job_requirement_user1_updated_valid_data["title"])

        assert (job_requirement_user1.description ==
                job_requirement_user1_updated_valid_data["description"])

    def test_partial_update_job_requirement_requires_authentication(
            self,
            api_client,
            job_requirement_user1,
            job_requirement_user1_url_path,
            job_requirement_user1_updated_valid_data,
    ):

        response = api_client.patch(
            job_requirement_user1_url_path,
            job_requirement_user1_updated_valid_data,
            format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_job_requirement(
            self,
            authenticated_client,
            job_requirement_user1,
            job_requirement_user1_url_path,
            job_requirement_user1_updated_valid_data,
    ):

        partial_update_api_data = job_requirement_user1_updated_valid_data.copy()
        partial_update_api_data.pop("title")

        old_title = job_requirement_user1.title

        response = authenticated_client.patch(
            job_requirement_user1_url_path,
            partial_update_api_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        job_requirement_user1.refresh_from_db()

        # Description should be changed
        assert (job_requirement_user1.description ==
                partial_update_api_data["description"])

        # Title should be unchanged
        assert job_requirement_user1.title == old_title

    def test_delete_job_requirement_requires_authentication(
            self,
            api_client,
            job_requirement_user1_url_path,
    ):

        response = api_client.delete(job_requirement_user1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_job_requirement(
            self,
            authenticated_client,
            job_requirement_user1,
            job_requirement_user1_url_path,
    ):

        response = authenticated_client.delete(job_requirement_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert not (
            JobRequirement.objects.filter(pk=job_requirement_user1.id).exists())
