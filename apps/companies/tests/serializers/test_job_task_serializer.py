import pytest

from apps.companies.api.v1.serializers import JobTaskSerializer


@pytest.mark.django_db
class TestJobTaskSerializer:

    def test_valid_data(self, job_task1_user1_valid_data):

        serializer = JobTaskSerializer(data=job_task1_user1_valid_data)

        assert serializer.is_valid(), serializer.errors

    def test_title_required(self, job_task1_user1_valid_data):

        payload = job_task1_user1_valid_data.copy()
        payload.pop("title")

        serializer = JobTaskSerializer(data=payload)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_title_cannot_be_blank(self, job_task1_user1_valid_data):

        payload = job_task1_user1_valid_data.copy()
        payload["title"] = ""

        serializer = JobTaskSerializer(data=payload)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_description_is_optional(self, job_task1_user1_valid_data):

        payload = job_task1_user1_valid_data.copy()
        payload.pop("description", None)

        serializer = JobTaskSerializer(data=payload)

        assert serializer.is_valid(), serializer.errors

    def test_description_cannot_be_null_if_provided(self, job_task1_user1_valid_data):

        payload = job_task1_user1_valid_data.copy()
        payload["description"] = None

        serializer = JobTaskSerializer(data=payload)

        assert not serializer.is_valid()
        assert "description" in serializer.errors

    def test_read_only_fields_ignored_on_input(self, job_task1_user1_valid_data):

        payload = job_task1_user1_valid_data.copy()
        payload["id"] = 999

        serializer = JobTaskSerializer(data=payload)

        assert serializer.is_valid(), serializer.errors
        assert "id" not in serializer.validated_data
