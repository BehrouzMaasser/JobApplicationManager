import pytest

from apps.companies.api.v1.serializers import JobBenefitSerializer


@pytest.mark.django_db
class TestJobBenefitSerializer:

    def test_valid_data(self, job_benefit1_user1_valid_data):

        serializer = JobBenefitSerializer(data=job_benefit1_user1_valid_data)

        assert serializer.is_valid()

    def test_name_required(self, job_benefit1_user1_valid_data):

        job_benefit1_user1_valid_data.pop("name")

        serializer = JobBenefitSerializer(data=job_benefit1_user1_valid_data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors
