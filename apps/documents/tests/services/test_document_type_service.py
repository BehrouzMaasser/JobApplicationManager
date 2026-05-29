from unittest.mock import patch

import pytest

from rest_framework.exceptions import ValidationError

from apps.documents.services.document_type_service import DocumentTypeService

#   ----------------------------------- ****** -----------------------------------


# Creation:

@pytest.mark.django_db
def test_create_calls_full_clean(user, doc_type1_user1_valid_data):

    with patch("apps.documents.models.DocumentType.full_clean") as mock_full_clean:

        DocumentTypeService.create(
            user=user, validated_data=doc_type1_user1_valid_data
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_create_calls_save(user, doc_type1_user1_valid_data):

    with patch("apps.documents.models.DocumentType.save") as mock_save:

        DocumentTypeService.create(
            user=user, validated_data=doc_type1_user1_valid_data
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_create_successfully_returns_document_type(
        user, doc_type1_user1_valid_data
):

    document_type = DocumentTypeService.create(
        user=user,
        validated_data=doc_type1_user1_valid_data,
    )

    assert document_type.id is not None
    assert document_type.owner == user
    assert document_type.name == doc_type1_user1_valid_data["name"]

    if doc_type1_user1_valid_data.get("description"):
        assert document_type.description == doc_type1_user1_valid_data["description"]
    else:
        assert document_type.description is None

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_full_clean(document_type_user1, doc_type1_user1_valid_data):

    with patch(
            "apps.documents.models.DocumentType.full_clean"
    ) as mock_full_clean:

        DocumentTypeService.update(
            user=document_type_user1.owner,
            document_type_id=document_type_user1.id,
            validated_data=doc_type1_user1_valid_data
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_update_calls_save(document_type_user1, doc_type1_user1_valid_data):

    with patch(
            "apps.documents.models.DocumentType.save"
    ) as mock_save:

        DocumentTypeService.update(
            user=document_type_user1.owner,
            document_type_id=document_type_user1.id,
            validated_data=doc_type1_user1_valid_data
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_calls_resolve_document_type(
        document_type_user1,
        doc_type1_user1_valid_data
):

    with patch(
        "apps.documents.services.document_type_service.DocumentTypeService."
        "_resolve_document_type"
    ) as mock_resolve_document_type:

        DocumentTypeService.update(
            user=document_type_user1.owner,
            document_type_id=document_type_user1.id,
            validated_data=doc_type1_user1_valid_data,
        )

        mock_resolve_document_type.assert_called_once()


@pytest.mark.django_db
def test_update_calls_update_non_m2m_fields(
        document_type_user1,
        doc_type1_user1_valid_data
):

    with patch(
            "apps.documents.services.document_type_service.DocumentTypeService."
            "_update_non_m2m_fields"
    ) as mock_update_non_m2m_fields:

        DocumentTypeService.update(
            user=document_type_user1.owner,
            document_type_id=document_type_user1.id,
            validated_data=doc_type1_user1_valid_data,
        )

        mock_update_non_m2m_fields.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_delete_calls_resolve_document_type(document_type_user1):

    with patch(
        "apps.documents.services.document_type_service.DocumentTypeService."
        "_resolve_document_type"
    ) as mock_resolve_document_type:

        DocumentTypeService.remove(
            user=document_type_user1.owner,
            document_type_id=document_type_user1.id,
        )

        mock_resolve_document_type.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Retrieving

@pytest.mark.django_db
def test_access_to_someone_else_document_type_raises_validation_error(
        other_user, document_type_user1
):

    # Document Type don't belong to user
    with pytest.raises(ValidationError):
        DocumentTypeService._resolve_document_type(
            user=other_user,
            document_type_id=document_type_user1.id,
        )

#   ----------------------------------- ****** -----------------------------------
