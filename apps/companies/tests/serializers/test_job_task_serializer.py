import pytest

from apps.companies.api.serializers import JobTaskSerializer


@pytest.mark.django_db
class TestJobTaskSerializer:

    def test_valid_data(self, job_task_user1_valid_data):

        serializer = JobTaskSerializer(data=job_task_user1_valid_data)

        assert serializer.is_valid()

    def test_title_required(self, job_task_user1_valid_data):

        job_task_user1_valid_data.pop("title")

        serializer = JobTaskSerializer(data=job_task_user1_valid_data)

        assert not serializer.is_valid()
        assert "title" in serializer.errors
