"""
Service layer for Document domain logic.

This module handles creation, update, and deletion of document records
while enforcing document ownership and validation rules.
"""

from typing import Any

from django.db import transaction

# Models
from apps.accounts.models import User
from apps.documents.models import Document

# Selectors
from apps.documents.selectors.document_selector import DocumentSelector

# Services
from apps.workspaces.services.base_service import BaseService


# Document Service
class DocumentService(BaseService):
    """
    Service responsible for managing Document domain operations.

    Ensures strict document ownership validation and delegates retrieval
    logic to selectors while maintaining validation consistency.
    """

    CREATE_REQUIRED_FIELDS = {
        "name",
        "document_type",
        "file",
    }

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: User,
        validated_data: dict[str, Any],
    ) -> Document:
        """
        Create a new Document instance.

        Calls:
            - django.db.models.base.Model.full_clean()
            - django.db.models.base.Model.save()

        Raises:
            ValidationError:
                If model validation fails.

        Returns:
            Document:
                The created document instance.
        """

        instance = Document(
            owner=user,
            name=validated_data.get("name"),
            document_type=validated_data.get("document_type"),
            file=validated_data.get("file"),
        )

        # Cleaning and saving the instance
        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        user: User,
        document_id: int,
        validated_data: dict[str, Any],
    ) -> Document:
        """
        Update an existing Document instance.

        Calls:
            - _resolve_document() to retrieve the target instance.
            - _update_non_m2m_fields() to apply updates.
            - django.db.models.base.Model.full_clean()
            - django.db.models.base.Model.save()

        Raises:
            ResourceNotFoundError:
                If the Document does not exist.

            AccessDeniedError:
                If the Document does not belong to the user.

            ValidationError:
                If model validation fails.

        Returns:
            Document:
                The updated document instance.
        """

        instance = DocumentService._resolve_document(
            user=user,
            document_id=document_id,
        )

        DocumentService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=DocumentService.UPDATABLE_FIELDS,
        )

        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def remove(
        *,
        user: User,
        document_id: int,
    ) -> None:
        """
        Remove a Document instance.

        Calls:
            - _resolve_document() to retrieve the target instance.
            - django.db.models.base.Model.delete()

        Raises:
            ResourceNotFoundError:
                If the Document does not exist.

            AccessDeniedError:
                If the Document does not belong to the user.

        Returns:
            None
        """

        instance = DocumentService._resolve_document(
            user=user,
            document_id=document_id,
        )

        instance.delete()

    @staticmethod
    def _resolve_document(
        *,
        user: User,
        document_id: int,
    ) -> Document:
        """
        Resolve a Document instance.

        Calls:
            DocumentSelector.get()

        Raises:
            ResourceNotFoundError:
                If the Document does not exist.

            AccessDeniedError:
                If the Document does not belong to the user.

        Returns:
            Document:
                The resolved document instance.
        """

        return DocumentSelector.get(
            user=user,
            document_id=document_id,
        )
