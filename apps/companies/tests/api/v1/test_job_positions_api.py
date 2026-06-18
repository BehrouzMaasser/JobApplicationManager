import pytest
from rest_framework import status

from apps.companies.models import JobPosition

pytestmark = pytest.mark.django_db


class TestJobPositionAPI:

    @pytest.fixture
    def job_position_list_url_path(self, base_api_url_path):

        return f"{base_api_url_path}job-positions/"

    @pytest.fixture
    def create_job_position1_user1_url_path(self, base_api_url_path, co1_ws1_user1):

        return (f"{base_api_url_path}workspaces/"
                f"{co1_ws1_user1.workspace.workspace_id}/companies/"
                f"{co1_ws1_user1.id}/job-positions/")

    @pytest.fixture
    def job_position1_user1_url_path(
            self,
            create_job_position1_user1_url_path,
            job_position1_user1
    ):

        return (f"{create_job_position1_user1_url_path}"
                f"{job_position1_user1.id}/")

    # List View Tests

    def test_list_requires_authentication(
            self, api_client, job_position_list_url_path
    ):

        response = api_client.get(job_position_list_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_job_positions(
            self,
            authenticated_client,
            job_position_list_url_path,
    ):

        response = authenticated_client.get(job_position_list_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_retrieve_job_positions_list_view(
            self,
            authenticated_client,
            job_position1_user1,
            job_position1_user1_url_path
    ):

        response = authenticated_client.get(job_position1_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_position1_user1.id

    # Nested View Tests

    def test_create_job_positions_requires_authentication(
            self,
            api_client,
            create_job_position1_user1_url_path,
            job_pos_user1_api_valid_data,
    ):

        response = api_client.post(
            create_job_position1_user1_url_path,
            job_pos_user1_api_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_job_position(
            self,
            authenticated_client,
            create_job_position1_user1_url_path,
            job_pos_user1_api_valid_data,
    ):

        response = authenticated_client.post(
            create_job_position1_user1_url_path,
            job_pos_user1_api_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert JobPosition.objects.filter(pk=response.data["id"]).exists()
        assert response.data["title"] == job_pos_user1_api_valid_data["title"]

        assert (response.data["description"] ==
                job_pos_user1_api_valid_data["description"])

        assert response.data["tasks"] == job_pos_user1_api_valid_data["tasks"]

        assert (response.data["requirements"] ==
                job_pos_user1_api_valid_data["requirements"])

        assert (response.data["benefits"] ==
                job_pos_user1_api_valid_data.get("benefits", []))

    def test_retrieve_job_positions_nested_view_requires_authentication(
            self, api_client, job_position1_user1_url_path
    ):

        response = api_client.get(job_position1_user1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_job_position_nested_view(
            self,
            authenticated_client,
            job_position1_user1,
            job_position1_user1_url_path
    ):

        response = authenticated_client.get(job_position1_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_position1_user1.id

    def test_update_job_position_nested_view_requires_authentication(
            self, api_client, job_position1_user1_url_path
    ):

        response = api_client.put(job_position1_user1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_job_position(
            self,
            authenticated_client,
            job_position1_user1,
            job_position1_user1_url_path,
            job_pos_user1_api_updated_valid_data
    ):

        response = authenticated_client.put(
            job_position1_user1_url_path,
            job_pos_user1_api_updated_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        job_position1_user1.refresh_from_db()

        assert (job_position1_user1.title ==
                job_pos_user1_api_updated_valid_data["title"])

        assert (job_position1_user1.description ==
                job_pos_user1_api_updated_valid_data["description"])

        assert ([task.id for task in job_position1_user1.tasks.all()] ==
                job_pos_user1_api_updated_valid_data["tasks"])

        assert (
                [
                    requirement.id for
                    requirement in job_position1_user1.requirements.all()
                ] ==
                job_pos_user1_api_updated_valid_data["requirements"]
        )

        assert ([benefit.id for benefit in job_position1_user1.benefits.all()] ==
                job_pos_user1_api_updated_valid_data.get("benefits", []))

    def test_partial_update_job_position_requires_authentication(
            self, api_client, job_position1_user1_url_path
    ):

        response = api_client.patch(job_position1_user1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_job_position(
            self,
            authenticated_client,
            job_position1_user1,
            job_position1_user1_url_path,
            job_pos_user1_api_updated_valid_data
    ):

        partial_update_api_data = job_pos_user1_api_updated_valid_data.copy()
        partial_update_api_data.pop("title")

        old_title = job_position1_user1.title

        response = authenticated_client.patch(
            job_position1_user1_url_path,
            partial_update_api_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        job_position1_user1.refresh_from_db()

        # Employment Types should be changed
        assert [
                   empl_type.id for
                   empl_type in job_position1_user1.employment_types.all()
               ] == partial_update_api_data["employment_types"]

        # Title should be unchanged
        assert job_position1_user1.title == old_title

    def test_delete_job_positions_requires_authentication(
            self, api_client, job_position1_user1_url_path
    ):

        response = api_client.delete(job_position1_user1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_job_position(
            self,
            authenticated_client,
            job_position1_user1,
            job_position1_user1_url_path,
    ):

        response = authenticated_client.delete(job_position1_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert not JobPosition.objects.filter(pk=job_position1_user1.id).exists()
