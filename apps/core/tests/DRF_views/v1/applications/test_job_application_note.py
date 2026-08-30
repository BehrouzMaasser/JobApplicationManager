import pytest
from rest_framework import status

from apps.applications.models import JobApplicationNote

pytestmark = pytest.mark.django_db


# =========================================================
# Fixtures
# =========================================================

@pytest.fixture
def job_application_note_list_url_path(base_api_url_path):
    return f"{base_api_url_path}job-application-notes/"


@pytest.fixture
def create_job_application_note_url_path(
    base_api_url_path,
    job_application1,
):
    return (
        f"{base_api_url_path}workspaces/"
        f"{job_application1.workspace.workspace_id}/"
        f"companies/{job_application1.job_position.company.id}/"
        f"job-positions/{job_application1.job_position.id}/"
        f"job-applications/{job_application1.id}/"
        f"job-application-notes/"
    )


@pytest.fixture
def job_application_note_detail_url_path(
    create_job_application_note_url_path,
    app_note1,
):
    return f"{create_job_application_note_url_path}{app_note1.id}/"


# =========================================================
# JOB APPLICATION NOTE LIST API
# =========================================================

class TestJobApplicationNoteListAPIView:

    def test_requires_authentication(
        self,
        api_client,
        job_application_note_list_url_path,
    ):
        response = api_client.get(job_application_note_list_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_job_application_notes(
        self,
        authenticated_client,
        job_application_note_list_url_path,
        app_note1,
        app_note1_user2,
    ):
        """
        Ensure the list endpoint returns notes accessible to the current user
        and does not leak notes owned by other users.
        """
        response = authenticated_client.get(job_application_note_list_url_path)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {
            item["id"] for item in response.data["results"]
        }

        assert app_note1.id in returned_ids
        # The fixture app_note1_user2 belongs to a different user and must not be returned
        assert app_note1_user2.id not in returned_ids

    def test_list_pagination_structure(
        self,
        authenticated_client,
        job_application_note_list_url_path,
    ):
        response = authenticated_client.get(job_application_note_list_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data


# =========================================================
# JOB APPLICATION NOTE RETRIEVE (FLAT)
# =========================================================

class TestJobApplicationNoteRetrieveAPIView:

    def test_requires_authentication(
        self,
        api_client,
        job_application_note_detail_url_path,
    ):
        response = api_client.get(job_application_note_detail_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_success(
        self,
        authenticated_client,
        job_application_note_detail_url_path,
        app_note1,
    ):
        response = authenticated_client.get(job_application_note_detail_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == app_note1.id

    def test_returns_404_for_unknown_job_application_note(
        self,
        authenticated_client,
        job_application_note_list_url_path,
    ):
        response = authenticated_client.get(
            f"{job_application_note_list_url_path}99999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


# =========================================================
# NESTED CREATE
# =========================================================

class TestNestedJobApplicationNoteCreateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        create_job_application_note_url_path,
        app_note1_valid_data,
    ):
        response = api_client.post(
            create_job_application_note_url_path,
            app_note1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_success(
        self,
        authenticated_client,
        create_job_application_note_url_path,
        app_note1_valid_data,
        job_application1,
    ):
        """
        Ensure nested create succeeds and that the created note is associated
        with the nested job application implied by the URL.
        """
        response = authenticated_client.post(
            create_job_application_note_url_path,
            app_note1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert JobApplicationNote.objects.filter(
            pk=response.data["id"]
        ).exists()

        # Validate persisted object's relation to the nested job application
        created = JobApplicationNote.objects.get(pk=response.data["id"])
        assert created.job_application == job_application1

        assert response.data["title"] == app_note1_valid_data["title"]
        assert response.data["content"] == app_note1_valid_data["content"]

    def test_invalid_payload_rejected(
        self,
        authenticated_client,
        create_job_application_note_url_path,
    ):
        response = authenticated_client.post(
            create_job_application_note_url_path,
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =========================================================
# NESTED RETRIEVE
# =========================================================

class TestNestedJobApplicationNoteRetrieveAPIView:

    def test_requires_authentication(
        self,
        api_client,
        job_application_note_detail_url_path,
    ):
        response = api_client.get(job_application_note_detail_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_success(
        self,
        authenticated_client,
        job_application_note_detail_url_path,
        app_note1,
    ):
        response = authenticated_client.get(
            job_application_note_detail_url_path
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == app_note1.id

    def test_returns_404_for_unknown_job_application_note(
        self,
        authenticated_client,
        create_job_application_note_url_path,
    ):
        response = authenticated_client.get(
            f"{create_job_application_note_url_path}99999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"


# =========================================================
# NESTED UPDATE / PATCH
# =========================================================

class TestNestedJobApplicationNoteUpdateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        job_application_note_detail_url_path,
        app_note1_valid_data_updated,
    ):
        response = api_client.put(
            job_application_note_detail_url_path,
            app_note1_valid_data_updated,
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_full_update_success(
        self,
        authenticated_client,
        app_note1,
        job_application_note_detail_url_path,
        app_note1_valid_data_updated,
    ):
        response = authenticated_client.put(
            job_application_note_detail_url_path,
            app_note1_valid_data_updated,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        app_note1.refresh_from_db()

        assert app_note1.title == app_note1_valid_data_updated["title"]
        assert app_note1.content == app_note1_valid_data_updated["content"]

    def test_partial_update_success(
        self,
        authenticated_client,
        app_note1,
        job_application_note_detail_url_path,
        app_note1_valid_data_updated,
    ):
        partial_data = app_note1_valid_data_updated.copy()
        partial_data.pop("title")

        old_title = app_note1.title

        response = authenticated_client.patch(
            job_application_note_detail_url_path,
            partial_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        app_note1.refresh_from_db()

        assert app_note1.content == partial_data["content"]
        assert app_note1.title == old_title

    def test_put_requires_all_required_fields(
        self,
        authenticated_client,
        job_application_note_detail_url_path,
    ):
        response = authenticated_client.put(
            job_application_note_detail_url_path,
            {"content": "Updated"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =========================================================
# NESTED DELETE
# =========================================================

class TestNestedJobApplicationNoteDeleteAPIView:

    def test_requires_authentication(
        self,
        api_client,
        job_application_note_detail_url_path,
    ):
        response = api_client.delete(job_application_note_detail_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_success(
        self,
        authenticated_client,
        app_note1,
        job_application_note_detail_url_path,
    ):
        response = authenticated_client.delete(
            job_application_note_detail_url_path
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not JobApplicationNote.objects.filter(
            pk=app_note1.id
        ).exists()

    def test_delete_idempotency_or_not_found(
        self,
        authenticated_client,
        app_note1,
        job_application_note_detail_url_path,
    ):
        authenticated_client.delete(job_application_note_detail_url_path)

        response = authenticated_client.delete(
            job_application_note_detail_url_path
        )

        assert response.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_204_NO_CONTENT,
        )
