import pytest

from apps.companies.api.v1.serializers import JobPositionSerializer


@pytest.mark.django_db
class TestJobPositionSerializer:

    def test_valid_data(self, job_pos_user1_api_updated_valid_data):

        serializer = JobPositionSerializer(data=job_pos_user1_api_updated_valid_data)

        assert serializer.is_valid(), serializer.errors

    def test_required_m2m_field_missing(self, job_pos_user1_api_updated_valid_data):

        payload = job_pos_user1_api_updated_valid_data.copy()
        payload.pop("requirements")

        serializer = JobPositionSerializer(data=payload)

        assert not serializer.is_valid()
        assert "requirements" in serializer.errors

    def test_required_m2m_fields_cannot_be_empty(
            self, job_pos_user1_api_updated_valid_data
    ):

        payload = job_pos_user1_api_updated_valid_data.copy()

        payload["employment_types"] = []
        payload["job_sites"] = []
        payload["tasks"] = []
        payload["requirements"] = []

        serializer = JobPositionSerializer(data=payload)

        assert not serializer.is_valid()

        assert "employment_types" in serializer.errors
        assert "job_sites" in serializer.errors
        assert "tasks" in serializer.errors
        assert "requirements" in serializer.errors

    def test_optional_m2m_benefits_can_be_empty(
            self, job_pos_user1_api_updated_valid_data
    ):

        payload = job_pos_user1_api_updated_valid_data.copy()
        payload["benefits"] = []

        serializer = JobPositionSerializer(data=payload)

        assert serializer.is_valid(), serializer.errors

    def test_title_is_required(self, job_pos_user1_api_updated_valid_data):

        payload = job_pos_user1_api_updated_valid_data.copy()
        payload.pop("title")

        serializer = JobPositionSerializer(data=payload)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_description_is_required(self, job_pos_user1_api_updated_valid_data):

        payload = job_pos_user1_api_updated_valid_data.copy()
        payload.pop("description")

        serializer = JobPositionSerializer(data=payload)

        assert not serializer.is_valid()
        assert "description" in serializer.errors
