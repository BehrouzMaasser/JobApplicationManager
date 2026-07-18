import hashlib
from unittest.mock import patch

import pytest

from django.core.exceptions import ValidationError

from apps.core.common.contexts.contexts import (
    DocumentContext,
    EmptyContext,
)

from apps.core.exceptions.exceptions import (
    BusinessRuleViolationError,
    InfrastructureViolationError,
)

from apps.documents.models import Document
from apps.documents.services.document_service import DocumentService


pytestmark = pytest.mark.django_db


EMPTY_CONTEXT = EmptyContext()


# ============================================================================
# Hooks
# ============================================================================

class TestDocumentServiceHooks:

    def test_resolve_create_dependencies_assigns_owner(
        self,
        user1,
    ):

        dependencies = DocumentService._resolve_create_dependencies(
            user=user1,
            context=EMPTY_CONTEXT,
        )

        assert dependencies == {
            "owner": user1,
        }


# ============================================================================
# Create
# ============================================================================

class TestDocumentCreate:

    def test_create_creates_document(
        self,
        user1,
        doc1_user1_valid_data,
    ):

        document = DocumentService.create(
            user=user1,
            context=DocumentContext(),
            validated_data=doc1_user1_valid_data,
        )

        assert document.pk is not None
        assert document.owner == user1
        assert document.name == (
            doc1_user1_valid_data["name"]
        )
        assert document.document_type == (
            doc1_user1_valid_data["document_type"]
        )


    def test_create_ignores_owner_from_payload(
        self,
        user1,
        user2,
        doc1_user1_valid_data,
    ):

        document = DocumentService.create(
            user=user1,
            context=DocumentContext(),
            validated_data={
                **doc1_user1_valid_data,
                "owner": user2,
            },
        )

        assert document.owner == user1


    def test_create_generates_correct_file_hash(
        self,
        user1,
        doc1_user1_valid_data,
    ):

        document = DocumentService.create(
            user=user1,
            context=DocumentContext(),
            validated_data=doc1_user1_valid_data,
        )

        expected_hash = hashlib.sha256()

        for chunk in document.file.chunks():
            expected_hash.update(chunk)

        assert document.file_hash == (
            expected_hash.hexdigest()
        )


    def test_create_requires_file(
        self,
        user1,
        doc1_user1_valid_data,
    ):

        data = {
            **doc1_user1_valid_data,
            "file": None,
        }

        with pytest.raises(
            BusinessRuleViolationError
        ):

            DocumentService.create(
                user=user1,
                context=DocumentContext(),
                validated_data=data,
            )

        assert Document.objects.count() == 0


    def test_create_calls_full_clean(
        self,
        user1,
        doc1_user1_valid_data,
    ):

        with patch.object(
            Document,
            "full_clean",
        ) as mock_clean:

            DocumentService.create(
                user=user1,
                context=DocumentContext(),
                validated_data=doc1_user1_valid_data,
            )

            mock_clean.assert_called_once()


# ============================================================================
# Update
# ============================================================================

class TestDocumentUpdate:

    def test_update_changes_allowed_fields(
        self,
        doc1_user1,
    ):

        document = DocumentService.update(
            user=doc1_user1.owner,
            context=DocumentContext(
                id=doc1_user1.id
            ),
            validated_data={
                "name": "Updated",
            },
        )

        assert document.name == "Updated"


    def test_update_allows_partial_update(
        self,
        doc1_user1,
    ):

        old_type = doc1_user1.document_type

        document = DocumentService.update(
            user=doc1_user1.owner,
            context=DocumentContext(
                id=doc1_user1.id
            ),
            validated_data={
                "name": "Updated",
            },
        )

        assert document.name == "Updated"
        assert document.document_type == old_type


    def test_update_regenerates_hash_when_file_changes(
        self,
        doc1_user1,
        fake_file2,
    ):

        old_hash = doc1_user1.file_hash

        document = DocumentService.update(
            user=doc1_user1.owner,
            context=DocumentContext(
                id=doc1_user1.id
            ),
            validated_data={
                "file": fake_file2,
            },
        )

        assert document.file_hash != old_hash


    def test_update_keeps_hash_when_file_not_changed(
        self,
        doc1_user1,
    ):

        old_hash = doc1_user1.file_hash

        document = DocumentService.update(
            user=doc1_user1.owner,
            context=DocumentContext(
                id=doc1_user1.id
            ),
            validated_data={
                "name": "Updated",
            },
        )

        assert document.file_hash == old_hash


    def test_update_calls_full_clean(
        self,
        doc1_user1,
    ):

        with patch.object(
            Document,
            "full_clean",
        ) as mock_clean:

            DocumentService.update(
                user=doc1_user1.owner,
                context=DocumentContext(
                    id=doc1_user1.id
                ),
                validated_data={
                    "name": "Updated",
                },
            )

            mock_clean.assert_called_once()


# ============================================================================
# Remove
# ============================================================================

class TestDocumentRemove:

    def test_remove_deletes_document(
        self,
        doc1_user1,
    ):

        document_id = doc1_user1.id

        DocumentService.remove(
            user=doc1_user1.owner,
            context=DocumentContext(
                id=document_id,
            ),
        )

        assert not Document.objects.filter(
            id=document_id,
        ).exists()


# ============================================================================
# Selector
# ============================================================================

class TestDocumentResolution:

    def test_resolve_instance_uses_selector(
        self,
        doc1_user1,
    ):

        with patch.object(
            DocumentService.SELECTOR,
            "get",
            return_value=doc1_user1,
        ) as mock_get:

            DocumentService._resolve_instance(
                user=doc1_user1.owner,
                context=DocumentContext(
                    id=doc1_user1.id,
                ),
            )

            mock_get.assert_called_once_with(
                user=doc1_user1.owner,
                obj_id=doc1_user1.id,
            )


# ============================================================================
# Infrastructure
# ============================================================================

class TestDocumentInfrastructure:

    def test_unexpected_exception_is_translated(
        self,
        user1,
        doc1_user1_valid_data,
    ):

        with patch.object(
            DocumentService,
            "_save",
            side_effect=RuntimeError("boom"),
        ):

            with pytest.raises(
                InfrastructureViolationError
            ):

                DocumentService.create(
                    user=user1,
                    context=DocumentContext(),
                    validated_data=doc1_user1_valid_data,
                )
