import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.documents.models import Document


pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# M-01: Define the Persistence Schema
# ---------------------------------------------------------------------------


class TestDocumentSchema:

    def test_document_can_be_created_with_valid_data(
        self,
        document_type_user1,
        fake_file1
    ):
        document = Document(
            owner=document_type_user1.owner,
            name="Document 1",
            document_type=document_type_user1,
            file=fake_file1,
            file_hash="hash123",
        )

        document.full_clean()
        document.save()

        assert document.id is not None
        assert document.name == "Document 1"
        assert document.owner == document_type_user1.owner
        assert document.document_type == document_type_user1
        assert document.file_hash == "hash123"


class TestDocumentConstraints:

    def test_document_name_must_be_unique_per_owner(
        self,
        document_type_user1,
        fake_file1,
        fake_file2
    ):
        Document.objects.create(
            owner=document_type_user1.owner,
            name="Document 1",
            document_type=document_type_user1,
            file=fake_file1,
            file_hash="hash123",
        )

        with pytest.raises(IntegrityError):
            Document.objects.create(
                owner=document_type_user1.owner,
                name="Document 1",
                document_type=document_type_user1,
                file=fake_file2,
                file_hash="hash456",
            )

    def test_same_file_is_not_allowed_for_same_owner(
        self,
        document_type_user1,
        fake_file1
    ):
        Document.objects.create(
            owner=document_type_user1.owner,
            name="Document 1",
            document_type=document_type_user1,
            file=fake_file1,
            file_hash="hash123",
        )

        with pytest.raises(IntegrityError):
            Document.objects.create(
                owner=document_type_user1.owner,
                name="Document 2",
                document_type=document_type_user1,
                file=fake_file1,
                file_hash="hash123",
            )

    def test_same_file_is_allowed_for_different_users(
        self,
        document_type_user1,
        document_type_user2,
        fake_file1
    ):
        document1 = Document.objects.create(
            owner=document_type_user1.owner,
            name="Document 1",
            document_type=document_type_user1,
            file=fake_file1,
            file_hash="hash123",
        )

        document2 = Document.objects.create(
            owner=document_type_user2.owner,
            name="Document 1",
            document_type=document_type_user2,
            file=fake_file1,
            file_hash="hash123",
        )

        assert document1.owner != document2.owner


# ---------------------------------------------------------------------------
# M-02: Enforce Domain Invariants
# ---------------------------------------------------------------------------


class TestDocumentValidation:

    def test_document_requires_owner(
        self,
        document_type_user1,
        fake_file1
    ):
        document = Document(
            owner=None,
            name="Document 1",
            document_type=document_type_user1,
            file=fake_file1,
            file_hash="hash123",
        )

        with pytest.raises(ValidationError):
            document.full_clean()

    def test_document_requires_name(
        self,
        user1,
        document_type_user1,
        fake_file1
    ):
        document = Document(
            owner=user1,
            name=None,
            document_type=document_type_user1,
            file=fake_file1,
            file_hash="hash123",
        )

        with pytest.raises(ValidationError):
            document.full_clean()

    def test_document_name_cannot_be_blank(
        self,
        user1,
        document_type_user1,
        fake_file1
    ):
        document = Document(
            owner=user1,
            name="",
            document_type=document_type_user1,
            file=fake_file1,
            file_hash="hash123",
        )

        with pytest.raises(ValidationError):
            document.full_clean()

    def test_document_owner_must_match_document_type_owner(
        self,
        user1,
        document_type_user2,
        fake_file1
    ):
        document = Document(
            owner=user1,
            name="Document 1",
            document_type=document_type_user2,
            file=fake_file1,
            file_hash="hash123",
        )

        with pytest.raises(ValidationError):
            document.full_clean()


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestDocumentProperties:

    def test_document_string_representation(
        self,
        document_type_user1,
        fake_file1
    ):
        document = Document(
            owner=document_type_user1.owner,
            name="Document 1",
            document_type=document_type_user1,
            file=fake_file1,
            file_hash="hash123",
        )

        assert str(document) == "Document 1"
