import copy
from unittest.mock import patch

import pytest

from apps.documents.services.document_type_service import DocumentTypeService

from apps.core.exceptions.exceptions import AccessDeniedError


# =========================================================
# CREATE
# =========================================================

@pytest.mark.django_db
class TestDocumentTypeServiceCreate:

    def test_create_returns_document_type_successfully(
        self,
        user1,
        doc_type1_user1_valid_data,
    ):
        document_type = DocumentTypeService.create(
            user=user1,
            validated_data=doc_type1_user1_valid_data,
        )

        assert document_type.id is not None
        assert document_type.owner == user1
        assert document_type.name == (
            doc_type1_user1_valid_data["name"]
        )

        assert document_type.description == (
            doc_type1_user1_valid_data.get("description")
        )

    def test_create_calls_model_methods(
        self,
        user1,
        doc_type1_user1_valid_data,
    ):
        with patch(
            "apps.documents.models.DocumentType.full_clean"
        ) as mock_clean, patch(
            "apps.documents.models.DocumentType.save"
        ) as mock_save:

            DocumentTypeService.create(
                user=user1,
                validated_data=doc_type1_user1_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()


# =========================================================
# UPDATE
# =========================================================

@pytest.mark.django_db
class TestDocumentTypeServiceUpdate:

    def test_update_returns_updated_document_type(
        self,
        document_type_user1,
        doc_type1_user1_valid_data,
    ):
        payload = copy.deepcopy(doc_type1_user1_valid_data)

        payload["name"] = "Updated Document Type"
        payload["description"] = "Updated description"

        updated = DocumentTypeService.update(
            user=document_type_user1.owner,
            document_type_id=document_type_user1.id,
            validated_data=payload,
        )

        assert updated.id == document_type_user1.id
        assert updated.name == payload["name"]
        assert updated.description == payload["description"]

    def test_update_resolves_document_type(
        self,
        document_type_user1,
        doc_type1_user1_valid_data,
    ):
        with patch(
            "apps.documents.services.document_type_service."
            "DocumentTypeService._resolve_document_type"
        ) as mock_resolve:

            mock_resolve.return_value = document_type_user1

            DocumentTypeService.update(
                user=document_type_user1.owner,
                document_type_id=document_type_user1.id,
                validated_data=doc_type1_user1_valid_data,
            )

            mock_resolve.assert_called_once()

    def test_update_calls_update_non_m2m_fields(
        self,
        document_type_user1,
        doc_type1_user1_valid_data,
    ):
        with patch(
            "apps.documents.services.document_type_service."
            "DocumentTypeService._update_non_m2m_fields"
        ) as mock_update, patch(
            "apps.documents.services.document_type_service."
            "DocumentTypeService._resolve_document_type",
            return_value=document_type_user1,
        ):

            DocumentTypeService.update(
                user=document_type_user1.owner,
                document_type_id=document_type_user1.id,
                validated_data=doc_type1_user1_valid_data,
            )

            mock_update.assert_called_once()

    def test_update_calls_model_methods(
        self,
        document_type_user1,
        doc_type1_user1_valid_data,
    ):
        with patch(
            "apps.documents.models.DocumentType.full_clean"
        ) as mock_clean, patch(
            "apps.documents.models.DocumentType.save"
        ) as mock_save, patch(
            "apps.documents.services.document_type_service."
            "DocumentTypeService._resolve_document_type",
            return_value=document_type_user1,
        ):

            DocumentTypeService.update(
                user=document_type_user1.owner,
                document_type_id=document_type_user1.id,
                validated_data=doc_type1_user1_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()

    def test_partial_update_keeps_existing_fields(
        self,
        document_type_user1,
        doc_type1_user1_valid_data,
    ):
        payload = copy.deepcopy(doc_type1_user1_valid_data)

        payload.pop("description")

        updated = DocumentTypeService.update(
            user=document_type_user1.owner,
            document_type_id=document_type_user1.id,
            validated_data=payload,
        )

        assert updated.name == payload["name"]
        assert updated.description == document_type_user1.description


# =========================================================
# REMOVE
# =========================================================

@pytest.mark.django_db
class TestDocumentTypeServiceRemove:

    def test_remove_resolves_document_type(
        self,
        document_type_user1,
    ):
        with patch(
            "apps.documents.services.document_type_service."
            "DocumentTypeService._resolve_document_type"
        ) as mock_resolve:

            mock_resolve.return_value = document_type_user1

            DocumentTypeService.remove(
                user=document_type_user1.owner,
                document_type_id=document_type_user1.id,
            )

            mock_resolve.assert_called_once()

    def test_remove_calls_delete(
        self,
        document_type_user1,
    ):
        with patch(
            "apps.documents.services.document_type_service."
            "DocumentTypeService._resolve_document_type",
            return_value=document_type_user1,
        ), patch(
            "apps.documents.models.DocumentType.delete"
        ) as mock_delete:

            DocumentTypeService.remove(
                user=document_type_user1.owner,
                document_type_id=document_type_user1.id,
            )

            mock_delete.assert_called_once()


# =========================================================
# RESOLVE
# =========================================================

@pytest.mark.django_db
class TestDocumentTypeServiceResolve:

    def test_returns_document_type_successfully(
        self,
        document_type_user1,
    ):
        result = DocumentTypeService._resolve_document_type(
            user=document_type_user1.owner,
            document_type_id=document_type_user1.id,
        )

        assert result == document_type_user1

    def test_selector_is_used(
        self,
        document_type_user1,
    ):
        with patch(
            "apps.documents.services.document_type_service."
            "DocumentTypeSelector.get",
            return_value=document_type_user1,
        ) as mock_get:

            DocumentTypeService._resolve_document_type(
                user=document_type_user1.owner,
                document_type_id=document_type_user1.id,
            )

            mock_get.assert_called_once()

    def test_accessing_other_users_document_type_raises_error(
        self,
        user2,
        document_type_user1,
    ):
        with pytest.raises(AccessDeniedError):

            DocumentTypeService._resolve_document_type(
                user=user2,
                document_type_id=document_type_user1.id,
            )
