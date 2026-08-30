import pytest

from apps.applications.api.v1.serializers import JobApplicationNoteSerializer

pytestmark = pytest.mark.django_db


class TestJobApplicationNoteSerializer:

    def test_valid_data(self):

        data = {
            "title": "Interview feedback",
            "content": "Strong technical discussion.",
        }

        serializer = JobApplicationNoteSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_rejects_blank_title(self):

        data = {
            "title": "",
            "content": "Some content",
        }

        serializer = JobApplicationNoteSerializer(data=data)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_rejects_null_title(self):

        data = {
            "title": None,
            "content": "Some content",
        }

        serializer = JobApplicationNoteSerializer(data=data)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_rejects_title_too_long(self):

        data = {
            "title": "a" * 61,
            "content": "Some content",
        }

        serializer = JobApplicationNoteSerializer(data=data)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_rejects_blank_content(self):

        data = {
            "title": "Valid title",
            "content": "",
        }

        serializer = JobApplicationNoteSerializer(data=data)

        assert not serializer.is_valid()
        assert "content" in serializer.errors

    def test_rejects_null_content(self):

        data = {
            "title": "Valid title",
            "content": None,
        }

        serializer = JobApplicationNoteSerializer(data=data)

        assert not serializer.is_valid()
        assert "content" in serializer.errors

    def test_read_only_job_application_ignored(self):

        data = {
            "title": "Test",
            "content": "Test content",
            "job_application": 99999999,
        }

        serializer = JobApplicationNoteSerializer(data=data)

        assert serializer.is_valid(), serializer.errors
        assert "job_application" not in serializer.validated_data

    def test_requires_title(self):

        data = {
            "content": "Some content",
        }

        serializer = JobApplicationNoteSerializer(data=data)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_requires_content(self):

        data = {
            "title": "Valid title",
        }

        serializer = JobApplicationNoteSerializer(data=data)

        assert not serializer.is_valid()
        assert "content" in serializer.errors

    def test_accepts_title_at_max_length(self):

        data = {
            "title": "a" * 60,
            "content": "Valid content",
        }

        serializer = JobApplicationNoteSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_serialization_outputs_fields(self, app_note1):
        """
        Verify serializer produces expected output for a saved instance.
        """
        serializer = JobApplicationNoteSerializer(instance=app_note1)
        data = serializer.data

        assert data["id"] == app_note1.id
        assert data["title"] == app_note1.title
        assert data["content"] == app_note1.content
