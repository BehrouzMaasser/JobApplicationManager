import pytest
from rest_framework import status

from apps.applications.models import JobApplication

pytestmark = pytest.mark.django_db


class TestJobApplicationAPI:

    @pytest.fixture
    def job_application_list_url_path(self, base_api_url_path):

        return f"{base_api_url_path}job-applications/"

    @pytest.fixture
    def create_job_application1_url_path(
            self, base_api_url_path, job_position1_co1_ws1_user1
    ):

        return (f"{base_api_url_path}workspaces/"
                f"{job_position1_co1_ws1_user1.company.workspace.workspace_id}/"
                f"companies/{job_position1_co1_ws1_user1.company.id}/"
                f"job-positions/{job_position1_co1_ws1_user1.id}/"
                f"job-applications/")

    @pytest.fixture
    def job_application1_url_path(
            self,
            create_job_application1_url_path,
            job_application1
    ):

        return f"{create_job_application1_url_path}{job_application1.id}/"

    # List View Tests

    def test_list_requires_authentication(
            self, api_client, job_application_list_url_path
    ):

        response = api_client.get(job_application_list_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_job_applications(
            self,
            authenticated_client,
            job_application_list_url_path,
    ):

        response = authenticated_client.get(job_application_list_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_retrieve_job_applications_list_view(
            self,
            authenticated_client,
            job_application1,
            job_application_list_url_path
    ):

        response = authenticated_client.get(
            f"{job_application_list_url_path}{job_application1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_application1.id

    # Nested View Tests

    def test_create_job_applications_requires_authentication(
            self,
            api_client,
            create_job_application1_url_path,
            job_application1_api_valid_data,
    ):

        response = api_client.post(
            create_job_application1_url_path,
            job_application1_api_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_job_application(
            self,
            authenticated_client,
            create_job_application1_url_path,
            job_application1_api_valid_data,
    ):

        response = authenticated_client.post(
            create_job_application1_url_path,
            job_application1_api_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert JobApplication.objects.filter(pk=response.data["id"]).exists()

        assert (response.data["status"] ==
                job_application1_api_valid_data["status"])

        assert response.data["emails"] == job_application1_api_valid_data["emails"]

        assert (response.data["documents"] ==
                job_application1_api_valid_data.get("documents", []))

    def test_retrieve_job_application_nested_view_requires_authentication(
            self, api_client, job_application1_url_path
    ):

        response = api_client.get(job_application1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_job_application_nested_view(
            self,
            authenticated_client,
            job_application1,
            job_application1_url_path
    ):

        response = authenticated_client.get(job_application1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_application1.id

    def test_update_job_application_nested_view_requires_authentication(
            self, api_client, job_application1_url_path
    ):

        response = api_client.put(job_application1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_job_application(
            self,
            authenticated_client,
            job_application1,
            job_application1_url_path,
            job_application1_api_valid_data_updated
    ):

        response = authenticated_client.put(
            job_application1_url_path,
            job_application1_api_valid_data_updated,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        job_application1.refresh_from_db()

        assert (response.data["status"] ==
                job_application1_api_valid_data_updated["status"])

        assert (response.data["emails"] ==
                job_application1_api_valid_data_updated["emails"])

        assert (response.data["documents"] ==
                job_application1_api_valid_data_updated.get("documents", []))

    def test_partial_update_job_application_requires_authentication(
            self, api_client, job_application1_url_path
    ):

        response = api_client.patch(job_application1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_job_application(
            self,
            authenticated_client,
            job_application1,
            job_application1_url_path,
            job_application1_api_valid_data_updated
    ):

        partial_update_api_data = job_application1_api_valid_data_updated.copy()
        partial_update_api_data.pop("status")

        old_status = job_application1.status.id

        response = authenticated_client.patch(
            job_application1_url_path,
            partial_update_api_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        job_application1.refresh_from_db()

        # Emails should be changed
        assert [
                   email.id for
                   email in job_application1.emails.all()
               ] == partial_update_api_data["emails"]

        # Status should be unchanged
        assert job_application1.status.id == old_status

    def test_delete_job_application_requires_authentication(
            self, api_client, job_application1_url_path
    ):

        response = api_client.delete(job_application1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_job_application(
            self,
            authenticated_client,
            job_application1,
            job_application1_url_path,
    ):

        response = authenticated_client.delete(job_application1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert not (
            JobApplication.objects.filter(pk=job_application1.id).exists())
