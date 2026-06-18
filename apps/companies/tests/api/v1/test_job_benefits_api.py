import pytest
from rest_framework import status

from apps.companies.models import JobBenefit

pytestmark = pytest.mark.django_db


class TestJobBenefitAPI:

    @pytest.fixture
    def job_benefits_url_path(self, base_api_url_path):

        return f"{base_api_url_path}job-benefits/"

    @pytest.fixture
    def job_benefit_user1_url_path(
            self,  job_benefits_url_path, job_benefit_user1
    ):

        return f"{job_benefits_url_path}{job_benefit_user1.id}/"

    # List View Tests

    def test_list_requires_authentication(
            self, api_client, job_benefits_url_path
    ):

        response = api_client.get(job_benefits_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_job_benefits(
            self,
            authenticated_client,
            job_benefits_url_path,
            job_benefit_user1
    ):

        response = authenticated_client.get(job_benefits_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_retrieve_job_benefit_requires_authentication(
            self,
            api_client,
            job_benefit_user1_url_path,
            job_benefit_user1
    ):

        response = api_client.get(job_benefit_user1_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_job_benefit(
            self,
            authenticated_client,
            job_benefit_user1_url_path,
            job_benefit_user1
    ):

        response = authenticated_client.get(job_benefit_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == job_benefit_user1.id

    def test_create_job_benefit_requires_authentication(
            self,
            api_client,
            job_benefits_url_path,
            job_benefit1_user1_valid_data,
    ):

        response = api_client.post(
            job_benefits_url_path,
            job_benefit1_user1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_job_benefit(
            self,
            authenticated_client,
            job_benefits_url_path,
            job_benefit1_user1_valid_data,
    ):

        response = authenticated_client.post(
            job_benefits_url_path,
            job_benefit1_user1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        assert JobBenefit.objects.filter(pk=response.data["id"]).exists()

        assert (response.data["name"] ==
                job_benefit1_user1_valid_data["name"])

        assert (response.data["description"] ==
                job_benefit1_user1_valid_data["description"])

    def test_update_job_benefit_requires_authentication(
            self,
            api_client,
            job_benefit_user1_url_path,
            job_benefit1_user1_updated_valid_data,
    ):

        response = api_client.put(
            job_benefit_user1_url_path,
            job_benefit1_user1_updated_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_job_benefit(
            self,
            authenticated_client,
            job_benefit_user1,
            job_benefit_user1_url_path,
            job_benefit1_user1_updated_valid_data,
    ):

        response = authenticated_client.put(
            job_benefit_user1_url_path,
            job_benefit1_user1_updated_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        job_benefit_user1.refresh_from_db()

        assert (job_benefit_user1.name ==
                job_benefit1_user1_updated_valid_data["name"])

        assert (job_benefit_user1.description ==
                job_benefit1_user1_updated_valid_data["description"])

    def test_partial_update_job_benefit_requires_authentication(
            self,
            api_client,
            job_benefit_user1,
            job_benefit_user1_url_path,
            job_benefit1_user1_updated_valid_data,
    ):

        response = api_client.patch(
            job_benefit_user1_url_path,
            job_benefit1_user1_updated_valid_data,
            format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_partial_update_job_benefit(
            self,
            authenticated_client,
            job_benefit_user1,
            job_benefit_user1_url_path,
            job_benefit1_user1_updated_valid_data,
    ):

        partial_update_api_data = job_benefit1_user1_updated_valid_data.copy()
        partial_update_api_data.pop("name")

        old_name = job_benefit_user1.name

        response = authenticated_client.patch(
            job_benefit_user1_url_path,
            partial_update_api_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        job_benefit_user1.refresh_from_db()

        # Description should be changed
        assert (job_benefit_user1.description ==
                partial_update_api_data["description"])

        # Name should be unchanged
        assert job_benefit_user1.name == old_name

    def test_delete_job_benefit_requires_authentication(
            self,
            api_client,
            job_benefit_user1_url_path,
    ):

        response = api_client.delete(job_benefit_user1_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_job_benefit(
            self,
            authenticated_client,
            job_benefit_user1,
            job_benefit_user1_url_path,
    ):

        response = authenticated_client.delete(job_benefit_user1_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert not JobBenefit.objects.filter(pk=job_benefit_user1.id).exists()
