import pytest

from apps.companies.api.v1.serializers import JobBenefitSerializer


@pytest.mark.django_db
class TestJobBenefitSerializer:

    def test_valid_data(self, job_benefit1_user1_valid_data):

        serializer = JobBenefitSerializer(data=job_benefit1_user1_valid_data)

        assert serializer.is_valid(), serializer.errors

    def test_name_required(self, job_benefit1_user1_valid_data):

        payload = job_benefit1_user1_valid_data.copy()
        payload.pop("name")

        serializer = JobBenefitSerializer(data=payload)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_name_cannot_be_blank(self, job_benefit1_user1_valid_data):

        payload = job_benefit1_user1_valid_data.copy()
        payload["name"] = ""

        serializer = JobBenefitSerializer(data=payload)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_description_is_optional(self, job_benefit1_user1_valid_data):

        payload = job_benefit1_user1_valid_data.copy()
        payload.pop("description")

        serializer = JobBenefitSerializer(data=payload)

        assert serializer.is_valid(), serializer.errors

    def test_description_cannot_be_null_if_provided(
            self, job_benefit1_user1_valid_data
    ):

        payload = job_benefit1_user1_valid_data.copy()
        payload["description"] = None

        serializer = JobBenefitSerializer(data=payload)

        assert not serializer.is_valid()
        assert "description" in serializer.errors

    def test_description_cannot_be_empty_if_provided(
            self, job_benefit1_user1_valid_data
    ):

        payload = job_benefit1_user1_valid_data.copy()
        payload["description"] = ""

        serializer = JobBenefitSerializer(data=payload)

        assert not serializer.is_valid()
        assert "description" in serializer.errors

    def test_read_only_fields_ignored_on_input(self, job_benefit1_user1_valid_data):

        payload = job_benefit1_user1_valid_data.copy()
        payload["id"] = 999

        serializer = JobBenefitSerializer(data=payload)

        assert serializer.is_valid(), serializer.errors
        assert "id" not in serializer.validated_data
