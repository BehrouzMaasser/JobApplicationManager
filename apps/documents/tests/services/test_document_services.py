import copy

from unittest.mock import patch

import pytest

from rest_framework.exceptions import ValidationError

from apps.documents.services.document_service import DocumentService

#   ----------------------------------- ****** -----------------------------------


# Creation:

@pytest.mark.django_db
def test_create_successfully_returns_document(
        user, doc1_user1_valid_data
):

    document = DocumentService.create(
        user=user,
        validated_data=doc1_user1_valid_data
    )

    assert document.id is not None
    assert document.owner == user
    assert document.name == doc1_user1_valid_data["name"]
    assert document.document_type == doc1_user1_valid_data["document_type"]
    assert document.file == doc1_user1_valid_data["file"]
    assert document.file_hash is not None


@pytest.mark.django_db
def test_create_calls_full_clean(user, doc1_user1_valid_data):

    with patch("apps.documents.models.Document.full_clean") as mock_full_clean:

        DocumentService.create(user=user, validated_data=doc1_user1_valid_data)

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_create_calls_save(user, doc1_user1_valid_data):

    with patch("apps.documents.models.Document.save") as mock_save:

        DocumentService.create(user=user, validated_data=doc1_user1_valid_data)

        mock_save.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_successfully_returns_updated_document(
        doc1_user1_valid_data, doc1_user1, document_type2_user1
):

    updated_data = copy.deepcopy(doc1_user1_valid_data)
    updated_data["name"] = "Document 1 Updated"
    updated_data["document_type"] = document_type2_user1

    document = DocumentService.update(
        user=doc1_user1.owner,
        document_id=doc1_user1.id,
        validated_data=updated_data,
    )

    assert document.id == doc1_user1.id
    assert document.owner == doc1_user1.owner
    assert document.name == updated_data["name"]
    assert document.document_type == updated_data["document_type"]
    assert document.file == updated_data["file"]
    assert document.file_hash is not None


@pytest.mark.django_db
def test_update_calls_full_clean(doc1_user1_valid_data, doc1_user1):

    with patch("apps.documents.models.Document.full_clean") as mock_full_clean:

        DocumentService.update(
            user=doc1_user1.owner,
            validated_data=doc1_user1_valid_data,
            document_id=doc1_user1.id
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_update_calls_save(doc1_user1_valid_data, doc1_user1):

    with patch("apps.documents.models.Document.save") as mock_save:

        DocumentService.update(
            user=doc1_user1.owner,
            validated_data=doc1_user1_valid_data,
            document_id=doc1_user1.id
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_calls_resolve_document(doc1_user1_valid_data, doc1_user1):

    with patch(
        "apps.documents.services.document_service.DocumentService."
        "_resolve_document"
    ) as mock_resolve_document:

        DocumentService.update(
            user=doc1_user1.owner,
            document_id=doc1_user1.id,
            validated_data=doc1_user1_valid_data,
        )

        mock_resolve_document.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_delete_calls_resolve_document(
        document_type2_user1, fake_file2, doc1_user1
):

    with patch(
        "apps.documents.services.document_service.DocumentService."
        "_resolve_document"
    ) as mock_resolve_document:

        DocumentService.remove(
            user=doc1_user1.owner,
            document_id=doc1_user1.id,
        )

        mock_resolve_document.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Retrieving

@pytest.mark.django_db
def test_access_document_of_other_user_raises_error(
        doc1_user1, other_user
):

    with pytest.raises(ValidationError):
        DocumentService._resolve_document(
            user=other_user,
            document_id=doc1_user1.id,
        )

#   ----------------------------------- ****** -----------------------------------
