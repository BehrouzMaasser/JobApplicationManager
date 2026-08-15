import pytest

from apps.companies.api.v1.serializers import JobRequirementSerializer


@pytest.mark.django_db
class TestJobRequirementSerializer:

    def test_valid_data(self, job_requirement1_user1_valid_data):

        serializer = JobRequirementSerializer(data=job_requirement1_user1_valid_data)

        assert serializer.is_valid(), serializer.errors

    def test_title_required(self, job_requirement1_user1_valid_data):

        payload = job_requirement1_user1_valid_data.copy()
        payload.pop("title")

        serializer = JobRequirementSerializer(data=payload)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_description_required(self, job_requirement1_user1_valid_data):

        payload = job_requirement1_user1_valid_data.copy()
        payload.pop("description")

        serializer = JobRequirementSerializer(data=payload)

        assert not serializer.is_valid()
        assert "description" in serializer.errors

    def test_title_cannot_be_blank(self, job_requirement1_user1_valid_data):

        payload = job_requirement1_user1_valid_data.copy()
        payload["title"] = ""

        serializer = JobRequirementSerializer(data=payload)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_description_cannot_be_blank(self, job_requirement1_user1_valid_data):

        payload = job_requirement1_user1_valid_data.copy()
        payload["description"] = ""

        serializer = JobRequirementSerializer(data=payload)

        assert not serializer.is_valid()
        assert "description" in serializer.errors

    def test_read_only_fields_ignored_on_input(
            self, job_requirement1_user1_valid_data
    ):

        payload = job_requirement1_user1_valid_data.copy()
        payload["id"] = 999

        serializer = JobRequirementSerializer(data=payload)

        assert serializer.is_valid(), serializer.errors
        assert "id" not in serializer.validated_data
