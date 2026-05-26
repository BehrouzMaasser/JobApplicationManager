import pytest
from rest_framework import status

from apps.applications.models import JobApplicationNote

pytestmark = pytest.mark.django_db


class TestJobApplicationNoteAPI:

    @pytest.fixture
    def job_app_notes_list_url_path(self, base_api_url_path):

        return f"{base_api_url_path}job-application-notes/"

    @pytest.fixture
    def create_app_note1_url_path(
            self, base_api_url_path, job_application1
    ):

        return (f"{base_api_url_path}workspaces/"
                f"{job_application1.workspace.workspace_id}/"
                f"companies/{job_application1.job_position.company.id}/"
                f"job-positions/{job_application1.job_position.id}/"
                f"job-applications/{job_application1.id}/job-application-notes/")

    @pytest.fixture
    def app_note1_url_path(self, create_app_note1_url_path, app_note1):

        return f"{create_app_note1_url_path}{app_note1.id}/"

    # List View Tests

    def test_list_requires_authentication(
            self, api_client, job_app_notes_list_url_path
    ):

        response = api_client.get(job_app_notes_list_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_job_app_notes(
            self,
            authenticated_client,
            job_app_notes_list_url_path,
    ):

        response = authenticated_client.get(job_app_notes_list_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_retrieve_job_app_notes_list_view(
            self,
            authenticated_client,
            app_note1,
            job_app_notes_list_url_path
    ):

        response = authenticated_client.get(
            f"{job_app_notes_list_url_path}{app_note1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == app_note1.id

    # Nested View Tests

    def test_create_job_app_note_requires_authentication(
            self,
            api_client,
            create_app_note1_url_path,
            app_note1_valid_data,
    ):

        response = api_client.post(
            create_app_note1_url_path,
            app_note1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_app_note1(
            self,
            authenticated_client,
            create_app_note1_url_path,
            app_note1_valid_data,
    ):

        response = authenticated_client.post(
            create_app_note1_url_path,
            app_note1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert JobApplicationNote.objects.filter(pk=response.data["id"]).exists()

        assert response.data["title"] == app_note1_valid_data["title"]
        assert response.data["content"] == app_note1_valid_data["content"]

    def test_retrieve_job_app_note_nested_view_requires_authentication(
            self, api_client, app_note1_url_path
    ):

        response = api_client.get(app_note1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_job_app_note_nested_view(
            self, authenticated_client, app_note1, app_note1_url_path
    ):

        response = authenticated_client.get(app_note1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == app_note1.id

    def test_update_job_app_note_nested_view_requires_authentication(
            self, api_client, app_note1_url_path
    ):

        response = api_client.put(app_note1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_job_app_note1(
            self,
            authenticated_client,
            app_note1,
            app_note1_url_path,
            app_note1_valid_data_updated
    ):

        response = authenticated_client.put(
            app_note1_url_path,
            app_note1_valid_data_updated,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        app_note1.refresh_from_db()

        assert app_note1.title == app_note1_valid_data_updated["title"]
        assert app_note1.content == app_note1_valid_data_updated["content"]

    def test_partial_update_job_app_note_requires_authentication(
            self, api_client, app_note1_url_path
    ):

        response = api_client.patch(app_note1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_job_app_note1(
            self,
            authenticated_client,
            app_note1,
            app_note1_url_path,
            app_note1_valid_data_updated
    ):

        partial_update_api_data = app_note1_valid_data_updated.copy()
        partial_update_api_data.pop("title")

        old_title = app_note1.title

        response = authenticated_client.patch(
            app_note1_url_path,
            partial_update_api_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        app_note1.refresh_from_db()

        # Content should be changed
        assert app_note1.content == app_note1_valid_data_updated["content"]

        # Title should be unchanged
        assert app_note1.title == old_title

    def test_delete_job_app_note_requires_authentication(
            self, api_client, app_note1_url_path
    ):

        response = api_client.delete(app_note1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_job_app_note1(
            self,
            authenticated_client,
            app_note1,
            app_note1_url_path,
    ):

        response = authenticated_client.delete(app_note1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert not JobApplicationNote.objects.filter(pk=app_note1.id).exists()
