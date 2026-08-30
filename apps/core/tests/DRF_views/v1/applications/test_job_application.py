import pytest
from rest_framework import status

from apps.applications.models import JobApplication

pytestmark = pytest.mark.django_db


# =========================================================
# Fixtures
# =========================================================

@pytest.fixture
def job_application_list_url_path(base_api_url_path):
    return f"{base_api_url_path}job-applications/"


@pytest.fixture
def create_job_application_url_path(
    base_api_url_path,
    job_position1_co1_ws1_user1,
):
    return (
        f"{base_api_url_path}"
        f"workspaces/{job_position1_co1_ws1_user1.company.workspace.workspace_id}/"
        f"companies/{job_position1_co1_ws1_user1.company.id}/"
        f"job-positions/{job_position1_co1_ws1_user1.id}/"
        f"job-applications/"
    )


@pytest.fixture
def job_application_detail_url_path(
    create_job_application_url_path,
    job_application1,
):
    return f"{create_job_application_url_path}{job_application1.id}/"


@pytest.fixture
def flat_job_application_detail_url_path(
    job_application_list_url_path,
    job_application1,
):
    return f"{job_application_list_url_path}{job_application1.id}/"


# =========================================================
# JOB APPLICATION LIST API
# =========================================================

class TestJobApplicationListAPIView:

    def test_requires_authentication(
        self,
        api_client,
        job_application_list_url_path,
    ):
        response = api_client.get(job_application_list_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_only_user_job_applications(
        self,
        authenticated_client,
        job_application_list_url_path,
        job_app1_pos1_co2_ws1_user1,
        job_app1_pos1_co1_ws1_user2,
    ):
        response = authenticated_client.get(job_application_list_url_path)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {item["id"] for item in response.data["results"]}

        assert job_app1_pos1_co2_ws1_user1.id in returned_ids
        assert job_app1_pos1_co1_ws1_user2.id not in returned_ids

    def test_list_pagination_structure(
        self,
        authenticated_client,
        job_application_list_url_path,
    ):
        response = authenticated_client.get(job_application_list_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data


# =========================================================
# JOB APPLICATION RETRIEVE (FLAT)
# =========================================================

class TestJobApplicationRetrieveAPIView:

    def test_requires_authentication(
        self,
        api_client,
        flat_job_application_detail_url_path,
    ):
        response = api_client.get(flat_job_application_detail_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_job_application_success(
        self,
        authenticated_client,
        flat_job_application_detail_url_path,
        job_application1,
    ):
        response = authenticated_client.get(
            flat_job_application_detail_url_path
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_application1.id

    def test_returns_404_for_unknown_job_application(
        self,
        authenticated_client,
        job_application_list_url_path,
    ):
        response = authenticated_client.get(
            f"{job_application_list_url_path}99999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_cannot_access_foreign_job_application(
        self,
        authenticated_client,
        job_application_list_url_path,
        job_app1_pos1_co1_ws1_user2,
    ):
        response = authenticated_client.get(
            f"{job_application_list_url_path}{job_app1_pos1_co1_ws1_user2.id}/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"


# =========================================================
# NESTED CREATE
# =========================================================

class TestNestedJobApplicationCreateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        create_job_application_url_path,
        job_application1_api_valid_data,
    ):
        response = api_client.post(
            create_job_application_url_path,
            job_application1_api_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_job_application_success(
        self,
        authenticated_client,
        create_job_application_url_path,
        job_application1_api_valid_data,
    ):
        response = authenticated_client.post(
            create_job_application_url_path,
            job_application1_api_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert JobApplication.objects.filter(
            pk=response.data["id"]
        ).exists()

        assert response.data["status"] == job_application1_api_valid_data["status"]
        assert response.data["emails"] == job_application1_api_valid_data.get("emails", [])
        assert response.data["documents"] == job_application1_api_valid_data.get(
            "documents", []
        )

    def test_invalid_payload_rejected(
        self,
        authenticated_client,
        create_job_application_url_path,
    ):
        response = authenticated_client.post(
            create_job_application_url_path,
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_rejects_foreign_email_ownership(
        self,
        authenticated_client,
        create_job_application_url_path,
        job_application1_api_valid_data,
        co_email1_co1_ws1_user2,
    ):
        """
        Posting an email that exists in the database but is owned by another user
        should be rejected by the create flow (service-level ownership validation).
        """
        payload = job_application1_api_valid_data.copy()
        payload["emails"] = [co_email1_co1_ws1_user2.id]

        response = authenticated_client.post(
            create_job_application_url_path,
            payload,
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =========================================================
# NESTED RETRIEVE
# =========================================================

class TestNestedJobApplicationRetrieveAPIView:

    def test_requires_authentication(
        self,
        api_client,
        job_application_detail_url_path,
    ):
        response = api_client.get(job_application_detail_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_success(
        self,
        authenticated_client,
        job_application_detail_url_path,
        job_application1,
    ):
        response = authenticated_client.get(job_application_detail_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_application1.id

    def test_returns_404_for_unknown_job_application(
        self,
        authenticated_client,
        create_job_application_url_path,
    ):
        response = authenticated_client.get(
            f"{create_job_application_url_path}99999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"


# =========================================================
# NESTED UPDATE / PATCH
# =========================================================

class TestNestedJobApplicationUpdateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        job_application_detail_url_path,
        job_application1_api_valid_data_updated,
    ):
        response = api_client.put(
            job_application_detail_url_path,
            job_application1_api_valid_data_updated,
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_full_update_success(
        self,
        authenticated_client,
        job_application1,
        job_application_detail_url_path,
        job_application1_api_valid_data_updated,
    ):
        response = authenticated_client.put(
            job_application_detail_url_path,
            job_application1_api_valid_data_updated,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        job_application1.refresh_from_db()

        assert response.data["status"] == job_application1_api_valid_data_updated["status"]
        assert response.data["emails"] == job_application1_api_valid_data_updated["emails"]
        assert response.data["documents"] == job_application1_api_valid_data_updated.get(
            "documents", []
        )

    def test_partial_update_success(
        self,
        authenticated_client,
        job_application1,
        job_application_detail_url_path,
        job_application1_api_valid_data_updated,
    ):
        partial_data = job_application1_api_valid_data_updated.copy()
        partial_data.pop("status")

        old_status = job_application1.status_id

        response = authenticated_client.patch(
            job_application_detail_url_path,
            partial_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        job_application1.refresh_from_db()

        assert sorted(
            job_application1.emails.values_list("id", flat=True)
        ) == sorted(partial_data["emails"])

        assert job_application1.status_id == old_status

    def test_put_requires_all_required_fields(
        self,
        authenticated_client,
        job_application_detail_url_path,
    ):
        response = authenticated_client.put(
            job_application_detail_url_path,
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =========================================================
# NESTED DELETE
# =========================================================

class TestNestedJobApplicationDeleteAPIView:

    def test_requires_authentication(
        self,
        api_client,
        job_application_detail_url_path,
    ):
        response = api_client.delete(job_application_detail_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_success(
        self,
        authenticated_client,
        job_application1,
        job_application_detail_url_path,
    ):
        response = authenticated_client.delete(job_application_detail_url_path)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not JobApplication.objects.filter(
            pk=job_application1.id
        ).exists()

    def test_delete_idempotency_or_not_found(
        self,
        authenticated_client,
        job_application_detail_url_path,
    ):
        authenticated_client.delete(job_application_detail_url_path)

        response = authenticated_client.delete(job_application_detail_url_path)

        assert response.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_204_NO_CONTENT,
        )
