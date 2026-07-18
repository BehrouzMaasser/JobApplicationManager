from unittest.mock import patch

import pytest

from django.core.exceptions import ValidationError

from apps.core.common.contexts.contexts import (
    EmptyContext,
    DocumentTypeContext,
)

from apps.documents.models import DocumentType
from apps.documents.services.document_type_service import (
    DocumentTypeService,
)


pytestmark = pytest.mark.django_db


EMPTY_CONTEXT = EmptyContext()


# ============================================================================
# Hooks
# ============================================================================

class TestDocumentTypeServiceHooks:

    def test_resolve_create_dependencies_assigns_owner(
        self,
        user1,
    ):

        dependencies = (
            DocumentTypeService
            ._resolve_create_dependencies(
                user=user1,
                context=EMPTY_CONTEXT,
            )
        )

        assert dependencies == {
            "owner": user1,
        }


# ============================================================================
# Create
# ============================================================================

class TestDocumentTypeCreate:

    def test_create_creates_document_type(
        self,
        user1,
        doc_type1_user1_valid_data,
    ):

        document_type = DocumentTypeService.create(
            user=user1,
            context=EMPTY_CONTEXT,
            validated_data=doc_type1_user1_valid_data,
        )

        assert document_type.id is not None
        assert document_type.owner == user1
        assert document_type.name == (
            doc_type1_user1_valid_data["name"]
        )
        assert document_type.description == (
            doc_type1_user1_valid_data.get(
                "description"
            )
        )


    def test_create_ignores_owner_from_payload(
        self,
        user1,
        user2,
        doc_type1_user1_valid_data,
    ):

        document_type = DocumentTypeService.create(
            user=user1,
            context=EMPTY_CONTEXT,
            validated_data={
                **doc_type1_user1_valid_data,
                "owner": user2,
            },
        )

        assert document_type.owner == user1


    def test_create_delegates_model_validation(
        self,
        user1,
        doc_type1_user1_valid_data,
    ):

        with patch.object(
            DocumentType,
            "full_clean",
        ) as mock_clean:

            DocumentTypeService.create(
                user=user1,
                context=EMPTY_CONTEXT,
                validated_data=doc_type1_user1_valid_data,
            )

            mock_clean.assert_called_once()


    def test_create_rejects_invalid_model_data(
        self,
        user1,
    ):

        with pytest.raises(
            ValidationError
        ):

            DocumentTypeService.create(
                user=user1,
                context=EMPTY_CONTEXT,
                validated_data={
                    "name": None,
                    "description": "invalid",
                },
            )


# ============================================================================
# Update
# ============================================================================

class TestDocumentTypeUpdate:

    def test_update_changes_allowed_fields(
        self,
        document_type_user1,
    ):

        updated = DocumentTypeService.update(
            user=document_type_user1.owner,
            context=DocumentTypeContext(
                id=document_type_user1.id
            ),
            validated_data={
                "name": "Updated",
                "description": "Updated description",
            },
        )

        assert updated.id == document_type_user1.id
        assert updated.name == "Updated"
        assert updated.description == (
            "Updated description"
        )


    def test_update_allows_partial_update(
        self,
        document_type_user1,
    ):

        old_description = (
            document_type_user1.description
        )

        updated = DocumentTypeService.update(
            user=document_type_user1.owner,
            context=DocumentTypeContext(
                id=document_type_user1.id
            ),
            validated_data={
                "name": "Updated name",
            },
        )

        assert updated.name == "Updated name"
        assert updated.description == old_description


    def test_update_ignores_non_updatable_fields(
        self,
        document_type_user1,
        user2,
    ):

        updated = DocumentTypeService.update(
            user=document_type_user1.owner,
            context=DocumentTypeContext(
                id=document_type_user1.id
            ),
            validated_data={
                "owner": user2,
            },
        )

        assert updated.owner == (
            document_type_user1.owner
        )


    def test_update_delegates_model_validation(
        self,
        document_type_user1,
    ):

        with patch.object(
            DocumentType,
            "full_clean",
        ) as mock_clean:

            DocumentTypeService.update(
                user=document_type_user1.owner,
                context=DocumentTypeContext(
                    id=document_type_user1.id
                ),
                validated_data={
                    "name": "Updated",
                },
            )

            mock_clean.assert_called_once()


# ============================================================================
# Remove
# ============================================================================

class TestDocumentTypeRemove:

    def test_remove_deletes_document_type(
        self,
        document_type_user1,
    ):

        document_type_id = document_type_user1.id

        DocumentTypeService.remove(
            user=document_type_user1.owner,
            context=DocumentTypeContext(
                id=document_type_id,
            ),
        )

        assert not DocumentType.objects.filter(
            id=document_type_id,
        ).exists()


# ============================================================================
# Resolution
# ============================================================================

class TestDocumentTypeResolution:

    def test_resolve_instance_uses_selector(
        self,
        document_type_user1,
    ):

        with patch.object(
            DocumentTypeService.SELECTOR,
            "get",
            return_value=document_type_user1,
        ) as mock_get:

            DocumentTypeService._resolve_instance(
                user=document_type_user1.owner,
                context=DocumentTypeContext(
                    id=document_type_user1.id
                ),
            )

            mock_get.assert_called_once_with(
                user=document_type_user1.owner,
                obj_id=document_type_user1.id,
            )


# ============================================================================
# Aggregate validation
# ============================================================================

class TestValidateResolvedInstance:

    def test_document_type_has_no_extra_validation(
        self,
        document_type_user1,
    ):

        DocumentTypeService._validate_resolved_instance(
            instance=document_type_user1,
            context=DocumentTypeContext(
                id=document_type_user1.id
            ),
        )
