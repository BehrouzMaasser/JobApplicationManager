import pytest
from rest_framework import status

from apps.companies.models import JobTask

pytestmark = pytest.mark.django_db


class TestJobTaskListAPIView:

    @pytest.fixture
    def job_tasks_url_path(self, base_api_url_path):
        return f"{base_api_url_path}job-tasks/"

    def test_requires_authentication(
        self,
        api_client,
        job_tasks_url_path,
    ):
        response = api_client.get(job_tasks_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_job_tasks(
        self,
        authenticated_client,
        job_tasks_url_path,
        job_task1_user1,
    ):
        response = authenticated_client.get(job_tasks_url_path)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {item["id"] for item in response.data["results"]}
        assert job_task1_user1.id in returned_ids


class TestJobTaskRetrieveAPIView:

    @pytest.fixture
    def job_tasks_url_path(self, base_api_url_path):
        return f"{base_api_url_path}job-tasks/"

    def test_requires_authentication(
        self,
        api_client,
        job_tasks_url_path,
        job_task1_user1,
    ):
        response = api_client.get(f"{job_tasks_url_path}{job_task1_user1.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_job_task(
        self,
        authenticated_client,
        job_tasks_url_path,
        job_task1_user1,
    ):
        response = authenticated_client.get(
            f"{job_tasks_url_path}{job_task1_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_task1_user1.id

    def test_returns_404_for_unknown_job_task(
        self,
        authenticated_client,
        job_tasks_url_path,
    ):
        response = authenticated_client.get(f"{job_tasks_url_path}999999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestJobTaskCreateAPIView:

    @pytest.fixture
    def job_tasks_url_path(self, base_api_url_path):
        return f"{base_api_url_path}job-tasks/"

    def test_requires_authentication(
        self,
        api_client,
        job_tasks_url_path,
        job_task1_user1_valid_data,
    ):
        response = api_client.post(
            job_tasks_url_path,
            job_task1_user1_valid_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_job_task(
        self,
        authenticated_client,
        job_tasks_url_path,
        job_task1_user1_valid_data,
    ):
        response = authenticated_client.post(
            job_tasks_url_path,
            job_task1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        assert JobTask.objects.filter(id=response.data["id"]).exists()

        assert response.data["title"] == job_task1_user1_valid_data["title"]

        assert (response.data["description"] ==
                job_task1_user1_valid_data["description"])


class TestJobTaskUpdateAPIView:

    @pytest.fixture
    def job_tasks_url_path(self, base_api_url_path):
        return f"{base_api_url_path}job-tasks/"

    def test_requires_authentication(
        self,
        api_client,
        job_tasks_url_path,
        job_task1_user1,
        job_task1_user1_updated_valid_data,
    ):
        response = api_client.put(
            f"{job_tasks_url_path}{job_task1_user1.id}/",
            job_task1_user1_updated_valid_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_job_task(
        self,
        authenticated_client,
        job_tasks_url_path,
        job_task1_user1,
        job_task1_user1_updated_valid_data,
    ):
        response = authenticated_client.put(
            f"{job_tasks_url_path}{job_task1_user1.id}/",
            job_task1_user1_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        job_task1_user1.refresh_from_db()

        assert job_task1_user1.title == job_task1_user1_updated_valid_data["title"]

        assert (job_task1_user1.description ==
                job_task1_user1_updated_valid_data["description"])

    def test_partial_update_job_task(
        self,
        authenticated_client,
        job_tasks_url_path,
        job_task1_user1,
        job_task1_user1_updated_valid_data,
    ):
        old_title = job_task1_user1.title

        partial_data = {
            "description": job_task1_user1_updated_valid_data["description"]
        }

        response = authenticated_client.patch(
            f"{job_tasks_url_path}{job_task1_user1.id}/",
            partial_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        job_task1_user1.refresh_from_db()

        assert job_task1_user1.description == partial_data["description"]
        assert job_task1_user1.title == old_title


class TestJobTaskDeleteAPIView:

    @pytest.fixture
    def job_tasks_url_path(self, base_api_url_path):
        return f"{base_api_url_path}job-tasks/"

    def test_requires_authentication(
        self,
        api_client,
        job_tasks_url_path,
        job_task1_user1,
    ):
        response = api_client.delete(f"{job_tasks_url_path}{job_task1_user1.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_job_task(
        self,
        authenticated_client,
        job_tasks_url_path,
        job_task1_user1,
    ):
        response = authenticated_client.delete(
            f"{job_tasks_url_path}{job_task1_user1.id}/"
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not JobTask.objects.filter(id=job_task1_user1.id).exists()
