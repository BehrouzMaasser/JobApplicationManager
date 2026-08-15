import pytest
from rest_framework import status

from apps.companies.models import JobBenefit

pytestmark = pytest.mark.django_db


# =========================================================
# LIST
# =========================================================

class TestJobBenefitListAPIView:

    @pytest.fixture
    def url(self, base_api_url_path):
        return f"{base_api_url_path}job-benefits/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_job_benefits(
        self,
        authenticated_client,
        url,
        job_benefit1_user1,
    ):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {obj["id"] for obj in response.data["results"]}
        assert job_benefit1_user1.id in returned_ids

    def test_does_not_return_foreign_benefits(
        self,
        authenticated_client,
        url,
        job_benefit1_user1,
        job_benefit1_user2,
    ):
        response = authenticated_client.get(url)

        returned_ids = {obj["id"] for obj in response.data["results"]}
        assert job_benefit1_user2.id not in returned_ids


# =========================================================
# RETRIEVE
# =========================================================

class TestJobBenefitRetrieveAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, job_benefit1_user1):
        return f"{base_api_url_path}job-benefits/{job_benefit1_user1.id}/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieves_job_benefit(
        self,
        authenticated_client,
        url,
        job_benefit1_user1,
    ):
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_benefit1_user1.id

    def test_returns_404_for_unknown_job_benefit(
        self,
        authenticated_client,
        base_api_url_path,
    ):
        response = authenticated_client.get(
            f"{base_api_url_path}job-benefits/999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"


# =========================================================
# CREATE
# =========================================================

class TestJobBenefitCreateAPIView:

    @pytest.fixture
    def url(self, base_api_url_path):
        return f"{base_api_url_path}job-benefits/"

    def test_requires_authentication(
        self,
        api_client,
        url,
        job_benefit1_user1_valid_data,
    ):
        response = api_client.post(url, job_benefit1_user1_valid_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_creates_job_benefit(
        self,
        authenticated_client,
        url,
        job_benefit1_user1_valid_data,
    ):
        response = authenticated_client.post(
            url,
            job_benefit1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        obj = JobBenefit.objects.get(pk=response.data["id"])

        assert obj.name == job_benefit1_user1_valid_data["name"]
        assert obj.description == job_benefit1_user1_valid_data["description"]

        assert JobBenefit.objects.filter(pk=response.data["id"]).exists()


# =========================================================
# UPDATE
# =========================================================

class TestJobBenefitUpdateAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, job_benefit1_user1):
        return f"{base_api_url_path}job-benefits/{job_benefit1_user1.id}/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.put(url, {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_full_update(
        self,
        authenticated_client,
        job_benefit1_user1,
        url,
        job_benefit1_user1_updated_valid_data,
    ):
        response = authenticated_client.put(
            url,
            job_benefit1_user1_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        job_benefit1_user1.refresh_from_db()

        assert (job_benefit1_user1.name ==
                job_benefit1_user1_updated_valid_data["name"])

        assert (job_benefit1_user1.description ==
                job_benefit1_user1_updated_valid_data["description"])

    def test_partial_update(
        self,
        authenticated_client,
        job_benefit1_user1,
        url,
        job_benefit1_user1_updated_valid_data,
    ):
        old_name = job_benefit1_user1.name

        payload = {
            "description": job_benefit1_user1_updated_valid_data["description"]
        }

        response = authenticated_client.patch(url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK

        job_benefit1_user1.refresh_from_db()

        assert job_benefit1_user1.description == payload["description"]
        assert job_benefit1_user1.name == old_name

    def test_returns_404_for_unknown_update(
        self,
        authenticated_client,
        base_api_url_path,
        job_benefit1_user1_updated_valid_data,
    ):
        response = authenticated_client.put(
            f"{base_api_url_path}job-benefits/999999/",
            job_benefit1_user1_updated_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


# =========================================================
# DELETE
# =========================================================

class TestJobBenefitDeleteAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, job_benefit1_user1):
        return f"{base_api_url_path}job-benefits/{job_benefit1_user1.id}/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_success(
        self,
        authenticated_client,
        job_benefit1_user1,
        url,
    ):
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not JobBenefit.objects.filter(pk=job_benefit1_user1.id).exists()

    def test_delete_unknown_object(
        self,
        authenticated_client,
        base_api_url_path,
    ):
        response = authenticated_client.delete(
            f"{base_api_url_path}job-benefits/999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_idempotency(
        self,
        authenticated_client,
        job_benefit1_user1,
        url,
    ):
        authenticated_client.delete(url)

        response = authenticated_client.delete(url)

        assert response.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_204_NO_CONTENT,
        )
