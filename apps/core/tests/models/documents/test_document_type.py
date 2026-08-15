import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.documents.models import DocumentType


pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# M-01: Define the Persistence Schema
# ---------------------------------------------------------------------------


class TestDocumentTypeSchema:

    def test_document_type_can_be_created_with_valid_data(self, user1):
        document_type = DocumentType(
            owner=user1,
            name="Document Type",
        )

        document_type.full_clean()
        document_type.save()

        assert document_type.id is not None
        assert document_type.owner == user1
        assert document_type.name == "Document Type"

    def test_document_type_description_can_be_optional(self, user1):
        empty_description = DocumentType(
            owner=user1,
            name="Type 1",
            description="",
        )

        no_description = DocumentType(
            owner=user1,
            name="Type 2",
            description=None,
        )

        empty_description.full_clean()
        no_description.full_clean()

        assert empty_description.description == ""
        assert no_description.description is None


class TestDocumentTypeConstraints:

    def test_document_type_name_is_case_insensitive_unique_per_owner(
        self,
        user1,
    ):
        DocumentType.objects.create(
            owner=user1,
            name="Document Type",
        )

        with pytest.raises(IntegrityError):
            DocumentType.objects.create(
                owner=user1,
                name="document type",
            )

    def test_same_document_type_name_is_allowed_for_different_users(
        self,
        user1,
        user2,
    ):
        document_type1 = DocumentType.objects.create(
            owner=user1,
            name="Document Type",
        )

        document_type2 = DocumentType.objects.create(
            owner=user2,
            name="Document Type",
        )

        assert document_type1.owner != document_type2.owner
        assert document_type1.name == document_type2.name


# ---------------------------------------------------------------------------
# M-02: Enforce Domain Invariants
# ---------------------------------------------------------------------------


class TestDocumentTypeValidation:

    def test_document_type_requires_owner(self):
        document_type = DocumentType(
            owner=None,
            name="Document Type",
        )

        with pytest.raises(ValidationError):
            document_type.full_clean()

    def test_document_type_requires_name(self, user1):
        document_type = DocumentType(
            owner=user1,
            name=None,
        )

        with pytest.raises(ValidationError):
            document_type.full_clean()

    def test_document_type_name_cannot_be_blank(self, user1):
        document_type = DocumentType(
            owner=user1,
            name="",
        )

        with pytest.raises(ValidationError):
            document_type.full_clean()


# ---------------------------------------------------------------------------
# M-03: Persistence Normalization
# ---------------------------------------------------------------------------


class TestDocumentTypeNormalization:

    def test_empty_description_is_normalized_to_none_after_save(
        self,
        user1,
    ):
        document_type = DocumentType(
            owner=user1,
            name="Document Type",
            description="",
        )

        document_type.save()

        assert document_type.description is None

    def test_whitespace_description_is_normalized_to_none_after_save(
        self,
        user1,
    ):
        document_type = DocumentType(
            owner=user1,
            name="Document Type",
            description="   ",
        )

        document_type.save()

        assert document_type.description is None

    def test_existing_description_is_preserved_after_save(
        self,
        user1,
    ):
        document_type = DocumentType(
            owner=user1,
            name="Document Type",
            description="Some Description",
        )

        document_type.save()

        assert document_type.description == "Some Description"


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestDocumentTypeProperties:

    def test_document_type_string_representation(self, user1):
        document_type = DocumentType(
            owner=user1,
            name="Document Type",
        )

        assert str(document_type) == "Document Type"
