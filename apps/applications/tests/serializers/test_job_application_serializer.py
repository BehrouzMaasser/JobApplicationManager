from django.utils import timezone

from apps.applications.api.v1.serializers import JobApplicationSerializer
from apps.documents.tests.conftest import doc1_user1


class TestJobApplicationSerializer:

    def test_valid_data(self, status1, email1_co1_ws1_user1, doc1_user1):

        data = {
            "status": status1.pk,
            "date_applied": timezone.now(),
            "emails": [email1_co1_ws1_user1.id],
            "documents": [doc1_user1.id],
        }

        serializer = JobApplicationSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_valid_without_optional_fields(self, status1):

        data = {
            "status": status1.pk,
        }

        serializer = JobApplicationSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_accepts_null_date_applied(self, status1):

        data = {
            "status": status1.pk,
            "date_applied": None,
        }

        serializer = JobApplicationSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_rejects_invalid_email_pk(self, status1):

        data = {
            "status": status1.pk,
            "emails": [999999999999],
        }

        serializer = JobApplicationSerializer(data=data)

        assert not serializer.is_valid()
        assert "emails" in serializer.errors

    def test_rejects_invalid_document_pk(self, status1):

        data = {
            "status": status1.pk,
            "documents": [999999],
        }

        serializer = JobApplicationSerializer(data=data)

        assert not serializer.is_valid()
        assert "documents" in serializer.errors

    def test_rejects_invalid_date_applied(self, status1):

        data = {
            "status": status1.pk,
            "date_applied": "not-a-date",
        }

        serializer = JobApplicationSerializer(data=data)

        assert not serializer.is_valid()
        assert "date_applied" in serializer.errors

    def test_read_only_fields_are_ignored(self, status1):

        data = {
            "status": status1.pk,
            "owner": 999,
            "workspace": 999,
            "job_position": 999,
        }

        serializer = JobApplicationSerializer(data=data)

        assert serializer.is_valid(), serializer.errors
        assert "owner" not in serializer.validated_data
        assert "workspace" not in serializer.validated_data
        assert "job_position" not in serializer.validated_data

    def test_rejects_invalid_status(self):

        data = {
            "status": "invalid_status"
        }

        serializer = JobApplicationSerializer(data=data)

        assert not serializer.is_valid()
        assert "status" in serializer.errors

    def test_accepts_empty_emails(self, status1):

        data = {
            "status": status1.pk,
            "emails": [],
        }

        serializer = JobApplicationSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_accepts_empty_documents(self, status1):

        data = {
            "status": status1.pk,
            "documents": [],
        }

        serializer = JobApplicationSerializer(data=data)

        assert serializer.is_valid(), serializer.errors
