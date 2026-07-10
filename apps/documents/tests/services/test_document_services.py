from unittest.mock import patch

import pytest

from django.core.exceptions import ValidationError

from apps.documents.services.document_service import DocumentService

from apps.core.exceptions.exceptions import AccessDeniedError


# =========================================================
# CREATE
# =========================================================

@pytest.mark.django_db
class TestDocumentServiceCreate:

    def test_create_returns_document_successfully(
        self,
        user1,
        doc1_user1_valid_data,
    ):
        document = DocumentService.create(
            user=user1,
            validated_data=doc1_user1_valid_data,
        )

        assert document.id is not None
        assert document.owner == user1
        assert document.name == doc1_user1_valid_data["name"]
        assert document.document_type == (
            doc1_user1_valid_data["document_type"]
        )
        assert document.file_hash is not None

    def test_create_calls_model_methods(
        self,
        user1,
        doc1_user1_valid_data,
    ):
        with patch(
            "apps.documents.models.Document.full_clean"
        ) as mock_clean, patch(
            "apps.documents.models.Document.save"
        ) as mock_save:

            DocumentService.create(
                user=user1,
                validated_data=doc1_user1_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()

    def test_create_rejects_foreign_document_type(
        self,
        user1,
        doc1_user1_valid_data,
        document_type_user2,
    ):
        doc1_user1_valid_data["document_type"] = document_type_user2

        with pytest.raises(ValidationError):
            DocumentService.create(
                user=user1,
                validated_data=doc1_user1_valid_data,
            )


# =========================================================
# UPDATE
# =========================================================

@pytest.mark.django_db
class TestDocumentServiceUpdate:

    def test_update_returns_updated_document(
        self,
        doc1_user1,
        doc1_user1_valid_data,
        document_type2_user1,
    ):

        doc1_user1_valid_data["name"] = "Updated Document"
        doc1_user1_valid_data["document_type"] = document_type2_user1

        document = DocumentService.update(
            user=doc1_user1.owner,
            document_id=doc1_user1.id,
            validated_data=doc1_user1_valid_data,
        )

        assert document.id == doc1_user1.id
        assert document.name == doc1_user1_valid_data["name"]
        assert document.document_type == doc1_user1_valid_data["document_type"]

    def test_update_resolves_document(
        self,
        doc1_user1,
        doc1_user1_valid_data,
    ):
        with patch(
            "apps.documents.services.document_service.DocumentService."
            "_resolve_document"
        ) as mock_resolve:

            mock_resolve.return_value = doc1_user1

            DocumentService.update(
                user=doc1_user1.owner,
                document_id=doc1_user1.id,
                validated_data=doc1_user1_valid_data,
            )

            mock_resolve.assert_called_once()

    def test_update_calls_update_non_m2m_fields(
        self,
        doc1_user1,
        doc1_user1_valid_data,
    ):
        with patch(
            "apps.documents.services.document_service.DocumentService."
            "_update_non_m2m_fields"
        ) as mock_update, patch(
            "apps.documents.services.document_service.DocumentService."
            "_resolve_document",
            return_value=doc1_user1,
        ):

            DocumentService.update(
                user=doc1_user1.owner,
                document_id=doc1_user1.id,
                validated_data=doc1_user1_valid_data,
            )

            mock_update.assert_called_once()

    def test_update_calls_model_methods(
        self,
        doc1_user1,
        doc1_user1_valid_data,
    ):
        with patch(
            "apps.documents.models.Document.full_clean"
        ) as mock_clean, patch(
            "apps.documents.models.Document.save"
        ) as mock_save, patch(
            "apps.documents.services.document_service.DocumentService."
            "_resolve_document",
            return_value=doc1_user1,
        ):

            DocumentService.update(
                user=doc1_user1.owner,
                document_id=doc1_user1.id,
                validated_data=doc1_user1_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()

    def test_partial_update_keeps_existing_fields(
        self,
        doc1_user1,
        doc1_user1_valid_data,
    ):
        doc1_user1_valid_data.pop("file")

        updated = DocumentService.update(
            user=doc1_user1.owner,
            document_id=doc1_user1.id,
            validated_data=doc1_user1_valid_data,
        )

        assert updated.name == doc1_user1_valid_data["name"]
        assert updated.document_type == doc1_user1_valid_data["document_type"]
        assert updated.file == doc1_user1.file


# =========================================================
# REMOVE
# =========================================================

@pytest.mark.django_db
class TestDocumentServiceRemove:

    def test_remove_resolves_document(
        self,
        doc1_user1,
    ):
        with patch(
            "apps.documents.services.document_service.DocumentService."
            "_resolve_document"
        ) as mock_resolve:

            mock_resolve.return_value = doc1_user1

            DocumentService.remove(
                user=doc1_user1.owner,
                document_id=doc1_user1.id,
            )

            mock_resolve.assert_called_once()

    def test_remove_calls_delete(
            self,
            doc1_user1,
    ):
        with patch(
                "apps.documents.services.document_service.DocumentService."
                "_resolve_document",
                return_value=doc1_user1,
        ), patch(
            "apps.documents.models.Document.delete"
        ) as mock_delete:
            DocumentService.remove(
                user=doc1_user1.owner,
                document_id=doc1_user1.id,
            )

            mock_delete.assert_called_once()


# =========================================================
# RESOLVE
# =========================================================

@pytest.mark.django_db
class TestDocumentServiceResolve:

    def test_returns_document_successfully(
        self,
        doc1_user1,
    ):
        result = DocumentService._resolve_document(
            user=doc1_user1.owner,
            document_id=doc1_user1.id,
        )

        assert result == doc1_user1

    def test_selector_is_used(
        self,
        doc1_user1,
    ):
        with patch(
            "apps.documents.services.document_service.DocumentSelector.get",
            return_value=doc1_user1,
        ) as mock_get:

            DocumentService._resolve_document(
                user=doc1_user1.owner,
                document_id=doc1_user1.id,
            )

            mock_get.assert_called_once()

    def test_accessing_other_users_document_raises_error(
        self,
        doc1_user1,
        user2,
    ):
        with pytest.raises(AccessDeniedError):

            DocumentService._resolve_document(
                user=user2,
                document_id=doc1_user1.id,
            )
