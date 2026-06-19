import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.documents.api.v1.serializers import DocumentWriteSerializer


pytestmark = pytest.mark.django_db


class TestDocumentWriteSerializer:

    def test_valid_data(self, document_type_user1, api_upload_file1):

        data = {
            "name": "Resume",
            "document_type": document_type_user1.id,
            "file": api_upload_file1,
        }

        serializer = DocumentWriteSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_requires_name(self, document_type_user1, api_upload_file1):

        data = {
            "document_type": document_type_user1.id,
            "file": api_upload_file1,
        }

        serializer = DocumentWriteSerializer(data=data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_rejects_blank_name(self, document_type_user1, api_upload_file1):

        data = {
            "name": "",
            "document_type": document_type_user1.id,
            "file": api_upload_file1,
        }

        serializer = DocumentWriteSerializer(data=data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_rejects_null_name(self, document_type_user1, api_upload_file1):

        data = {
            "name": None,
            "document_type": document_type_user1.id,
            "file": api_upload_file1,
        }

        serializer = DocumentWriteSerializer(data=data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_rejects_name_too_long(self, document_type_user1, api_upload_file1):

        data = {
            "name": "a" * 51,
            "document_type": document_type_user1.id,
            "file": api_upload_file1,
        }

        serializer = DocumentWriteSerializer(data=data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_requires_document_type(self, api_upload_file1):

        data = {
            "name": "Resume",
            "file": api_upload_file1,
        }

        serializer = DocumentWriteSerializer(data=data)

        assert not serializer.is_valid()
        assert "document_type" in serializer.errors

    def test_rejects_invalid_document_type(self, api_upload_file1):

        data = {
            "name": "Resume",
            "document_type": 999999,
            "file": api_upload_file1,
        }

        serializer = DocumentWriteSerializer(data=data)

        assert not serializer.is_valid()
        assert "document_type" in serializer.errors

    def test_requires_file(self, document_type_user1):

        data = {
            "name": "Resume",
            "document_type": document_type_user1.id,
        }

        serializer = DocumentWriteSerializer(data=data)

        assert not serializer.is_valid()
        assert "file" in serializer.errors

    def test_rejects_null_file(self, document_type_user1):

        data = {
            "name": "Resume",
            "document_type": document_type_user1.id,
            "file": None,
        }

        serializer = DocumentWriteSerializer(data=data)

        assert not serializer.is_valid()
        assert "file" in serializer.errors

    def test_rejects_empty_file(self, document_type_user1):

        empty_file = SimpleUploadedFile(
            "empty.pdf",
            b"",
            content_type="application/pdf",
        )

        data = {
            "name": "Resume",
            "document_type": document_type_user1.id,
            "file": empty_file,
        }

        serializer = DocumentWriteSerializer(data=data)

        assert not serializer.is_valid()
        assert "file" in serializer.errors

    def test_read_only_fields_are_ignored(
            self, document_type_user1, api_upload_file1
    ):

        data = {
            "name": "Resume",
            "document_type": document_type_user1.id,
            "file": api_upload_file1,
            "owner": 999,
            "file_hash": "fakehash",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
        }

        serializer = DocumentWriteSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

        assert set(serializer.validated_data.keys()) == {
            "name",
            "document_type",
            "file",
        }
