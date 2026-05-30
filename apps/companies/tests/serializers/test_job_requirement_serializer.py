import pytest

from apps.companies.api.serializers import JobRequirementSerializer


@pytest.mark.django_db
class TestJobRequirementSerializer:

    def test_valid_data(self, job_requirement_user1_valid_data):

        serializer = JobRequirementSerializer(data=job_requirement_user1_valid_data)

        assert serializer.is_valid()

    def test_description_required(self, job_requirement_user1_valid_data):

        job_requirement_user1_valid_data.pop("description")

        serializer = JobRequirementSerializer(data=job_requirement_user1_valid_data)

        assert not serializer.is_valid()
        assert "description" in serializer.errors
