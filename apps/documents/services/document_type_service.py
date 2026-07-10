"""
Service layer for DocumentType domain logic.

This module handles creation, update, and deletion of document type records
while enforcing document type ownership and validation rules.
"""

from typing import Any

from django.db import transaction

# Models
from apps.accounts.models import User
from apps.documents.models import DocumentType

# Selectors
from apps.documents.selectors.document_type_selector import DocumentTypeSelector

# Services
from apps.workspaces.services.base_service import BaseService


# Document Type Service
class DocumentTypeService(BaseService):
    """
    Service responsible for managing DocumentType domain operations.

    Ensures strict document type ownership validation and delegates retrieval
    logic to selectors while maintaining validation consistency.
    """

    CREATE_REQUIRED_FIELDS = {
        "name",
    }

    UPDATABLE_FIELDS = {
        *CREATE_REQUIRED_FIELDS,
        "description",
    }

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: User,
        validated_data: dict[str, Any],
    ) -> DocumentType:
        """
        Create a new DocumentType instance.

        Calls:
            - django.db.models.base.Model.full_clean()
            - django.db.models.base.Model.save()

        Raises:
            ValidationError:
                If model validation fails.

        Returns:
            DocumentType:
                The created document type instance.
        """

        instance = DocumentType(
            owner=user,
            name=validated_data.get("name"),
            description=validated_data.get("description"),
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
        document_type_id: int,
        validated_data: dict[str, Any],
    ) -> DocumentType:
        """
        Update an existing DocumentType instance.

        Calls:
            - _resolve_document_type() to retrieve the target instance.
            - _update_non_m2m_fields() to apply updates.
            - django.db.models.base.Model.full_clean()
            - django.db.models.base.Model.save()

        Raises:
            ResourceNotFoundError:
                If the DocumentType does not exist.

            AccessDeniedError:
                If the DocumentType does not belong to the user.

            ValidationError:
                If model validation fails.

        Returns:
            DocumentType:
                The updated document type instance.
        """

        instance = DocumentTypeService._resolve_document_type(
            user=user,
            document_type_id=document_type_id,
        )

        DocumentTypeService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=DocumentTypeService.UPDATABLE_FIELDS,
        )

        # Cleaning and saving the instance
        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def remove(
        *,
        user: User,
        document_type_id: int,
    ) -> None:
        """
        Remove a DocumentType instance.

        Calls:
            - _resolve_document_type() to retrieve the target instance.
            - django.db.models.base.Model.delete()

        Raises:
            ResourceNotFoundError:
                If the DocumentType does not exist.

            AccessDeniedError:
                If the DocumentType does not belong to the user.

        Returns:
            None
        """

        instance = DocumentTypeService._resolve_document_type(
            user=user,
            document_type_id=document_type_id,
        )

        instance.delete()

    @staticmethod
    def _resolve_document_type(
        *,
        user: User,
        document_type_id: int,
    ) -> DocumentType:
        """
        Resolve a DocumentType instance.

        Calls:
            DocumentTypeSelector.get()

        Raises:
            ResourceNotFoundError:
                If the DocumentType does not exist.

            AccessDeniedError:
                If the DocumentType does not belong to the user.

        Returns:
            DocumentType:
                The resolved document type instance.
        """

        return DocumentTypeSelector.get(
            user=user,
            document_type_id=document_type_id,
        )
