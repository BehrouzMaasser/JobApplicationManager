import pytest

from apps.companies.api.v1.serializers import JobPositionSerializer


@pytest.mark.django_db
class TestJobPositionSerializer:

    def test_valid_data(self, job_pos_user1_api_updated_valid_data):

        serializer = JobPositionSerializer(data=job_pos_user1_api_updated_valid_data)

        assert serializer.is_valid(), serializer.errors

    def test_required_m2m_fields(self, job_pos_user1_api_updated_valid_data):

        job_pos_user1_api_updated_valid_data.pop("requirements")

        serializer = JobPositionSerializer(data=job_pos_user1_api_updated_valid_data)

        assert not serializer.is_valid()
        assert "requirements" in serializer.errors

    def test_empty_required_m2m_not_allowed(
            self, job_pos_user1_api_updated_valid_data
    ):

        job_pos_user1_api_updated_valid_data["employment_types"] = []
        job_pos_user1_api_updated_valid_data["job_sites"] = []
        job_pos_user1_api_updated_valid_data["tasks"] = []
        job_pos_user1_api_updated_valid_data["requirements"] = []

        serializer = JobPositionSerializer(data=job_pos_user1_api_updated_valid_data)

        assert not serializer.is_valid()

        assert "employment_types" in serializer.errors
        assert "job_sites" in serializer.errors
        assert "tasks" in serializer.errors
        assert "requirements" in serializer.errors

    def test_benefits_can_be_empty(self, job_pos_user1_api_updated_valid_data):

        job_pos_user1_api_updated_valid_data["benefits"] = []

        serializer = JobPositionSerializer(data=job_pos_user1_api_updated_valid_data)

        assert serializer.is_valid(), serializer.errors

    def test_title_required(self, job_pos_user1_api_updated_valid_data):

        job_pos_user1_api_updated_valid_data.pop("title")

        serializer = JobPositionSerializer(data=job_pos_user1_api_updated_valid_data)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_description_required(self, job_pos_user1_api_updated_valid_data):

        job_pos_user1_api_updated_valid_data.pop("description")

        serializer = JobPositionSerializer(data=job_pos_user1_api_updated_valid_data)

        assert not serializer.is_valid()
        assert "description" in serializer.errors
