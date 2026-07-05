import pytest
from rest_framework import status

from apps.companies.models import JobPosition

pytestmark = pytest.mark.django_db


class TestJobPositionListAPIView:

    @pytest.fixture
    def job_positions_url_path(self, base_api_url_path):
        return f"{base_api_url_path}job-positions/"

    def test_requires_authentication(
        self,
        api_client,
        job_positions_url_path,
    ):
        response = api_client.get(job_positions_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_job_positions(
        self,
        authenticated_client,
        job_positions_url_path,
        job_position1_user1,
    ):
        response = authenticated_client.get(job_positions_url_path)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {obj["id"] for obj in response.data["results"]}
        assert job_position1_user1.id in returned_ids


class TestNestedJobPositionCreateAPIView:

    @pytest.fixture
    def create_job_position_url_path(self, base_api_url_path, co1_ws1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{co1_ws1_user1.workspace.workspace_id}/"
            f"companies/{co1_ws1_user1.id}/"
            f"job-positions/"
        )

    def test_requires_authentication(
        self,
        api_client,
        create_job_position_url_path,
        job_pos_user1_api_valid_data,
    ):
        response = api_client.post(
            create_job_position_url_path,
            job_pos_user1_api_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_creates_job_position(
        self,
        authenticated_client,
        create_job_position_url_path,
        job_pos_user1_api_valid_data,
    ):
        response = authenticated_client.post(
            create_job_position_url_path,
            job_pos_user1_api_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

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


class TestNestedJobPositionRetrieveAPIView:

    @pytest.fixture
    def job_position_url_path(self, base_api_url_path, job_position1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{job_position1_user1.company.workspace.workspace_id}/"
            f"companies/{job_position1_user1.company.id}/"
            f"job-positions/{job_position1_user1.id}/"
        )

    def test_requires_authentication(self, api_client, job_position_url_path):
        response = api_client.get(job_position_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieves_job_position(
        self,
        authenticated_client,
        job_position_url_path,
        job_position1_user1,
    ):
        response = authenticated_client.get(job_position_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_position1_user1.id

    def test_returns_404_for_unknown_job_position(
        self,
        authenticated_client,
        job_position_url_path,
    ):
        response = authenticated_client.get(f"{job_position_url_path}999999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestNestedJobPositionUpdateAPIView:

    @pytest.fixture
    def job_position_url_path(self, base_api_url_path, job_position1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{job_position1_user1.company.workspace.workspace_id}/"
            f"companies/{job_position1_user1.company.id}/"
            f"job-positions/{job_position1_user1.id}/"
        )

    def test_requires_authentication(self, api_client, job_position_url_path):
        response = api_client.put(job_position_url_path, {}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_updates_job_position(
        self,
        authenticated_client,
        job_position1_user1,
        job_position_url_path,
        job_pos_user1_api_updated_valid_data,
    ):
        response = authenticated_client.put(
            job_position_url_path,
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

        assert set(job_position1_user1.requirements.values_list("id", flat=True)) == set(
            job_pos_user1_api_updated_valid_data["requirements"]
        )

        assert set(job_position1_user1.employment_types.values_list("id", flat=True)) == set(
            job_pos_user1_api_updated_valid_data["employment_types"]
        )


class TestNestedJobPositionDeleteAPIView:

    @pytest.fixture
    def job_position_url_path(self, base_api_url_path, job_position1_user1):
        return (
            f"{base_api_url_path}workspaces/"
            f"{job_position1_user1.company.workspace.workspace_id}/"
            f"companies/{job_position1_user1.company.id}/"
            f"job-positions/{job_position1_user1.id}/"
        )

    def test_requires_authentication(self, api_client, job_position_url_path):
        response = api_client.delete(job_position_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_deletes_job_position(
        self,
        authenticated_client,
        job_position1_user1,
        job_position_url_path,
    ):
        response = authenticated_client.delete(job_position_url_path)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not JobPosition.objects.filter(pk=job_position1_user1.id).exists()
