import pytest
from rest_framework import status

from apps.companies.models import JobBenefit

pytestmark = pytest.mark.django_db


# =========================================================
# List
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
        assert any(obj["id"] == job_benefit1_user1.id for
                   obj in response.data["results"])


# =========================================================
# Retrieve
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


# =========================================================
# Create
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

        assert response.status_code == status.HTTP_200_OK

        obj = JobBenefit.objects.get(pk=response.data["id"])

        assert obj.name == job_benefit1_user1_valid_data["name"]
        assert obj.description == job_benefit1_user1_valid_data["description"]


# =========================================================
# Update
# =========================================================

class TestJobBenefitUpdateAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, job_benefit1_user1):
        return f"{base_api_url_path}job-benefits/{job_benefit1_user1.id}/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.put(url, {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_updates_job_benefit(
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
        payload = job_benefit1_user1_updated_valid_data.copy()
        payload.pop("name")

        old_name = job_benefit1_user1.name

        response = authenticated_client.patch(url, payload, format="json")

        assert response.status_code == status.HTTP_200_OK

        job_benefit1_user1.refresh_from_db()

        assert job_benefit1_user1.description == payload["description"]
        assert job_benefit1_user1.name == old_name


# =========================================================
# Delete
# =========================================================

class TestJobBenefitDeleteAPIView:

    @pytest.fixture
    def url(self, base_api_url_path, job_benefit1_user1):
        return f"{base_api_url_path}job-benefits/{job_benefit1_user1.id}/"

    def test_requires_authentication(self, api_client, url):
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_deletes_job_benefit(
        self,
        authenticated_client,
        job_benefit1_user1,
        url,
    ):
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not JobBenefit.objects.filter(pk=job_benefit1_user1.id).exists()
