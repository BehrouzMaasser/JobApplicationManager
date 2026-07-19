"""
Service layer for Document domain logic.

This module handles creation, update, and deletion of document records
while enforcing document ownership and validation rules.
"""
import hashlib
from typing import Any

# Models
from apps.accounts.models import User
from apps.core.common.contexts.contexts import DocumentContext
from apps.core.exceptions.exceptions import BusinessRuleViolationError
from apps.documents.models import Document

# Selectors
from apps.documents.selectors.document_selector import DocumentSelector

# Services
from apps.core.common.services.base_service import BaseService


# Document Service
class DocumentService(BaseService[Document]):
    """
    Service responsible for managing Document domain operations.

    Ensures strict document ownership validation and delegates retrieval
    logic to selectors while maintaining validation consistency.
    """

    MODEL = Document
    SELECTOR = DocumentSelector

    CREATE_FIELDS = ("owner", "name", "document_type", "file")
    SCALAR_UPDATABLE_FIELDS = ("name", "document_type", "file")
    M2M_UPDATABLE_FIELDS = ()
    REQUIRED_M2M_FIELDS = ()
    NON_EMPTY_M2M_FIELDS = ()
    M2M_OWNER_FIELD_MAP = {}

    @classmethod
    def _create_validate(
            cls,
            *,
            user: User,
            instance: Document,
            validated_data: dict[str, Any]
    ) -> None:

        if instance.file:
            cls._add_file_hash(instance=instance)
        else:
            raise BusinessRuleViolationError(
                fields=["file"],
                messages=["Please upload a file for this document."]
            )

    @classmethod
    def _resolve_create_dependencies(
            cls,
            user: User,
            context: DocumentContext
    ) -> dict[str, Any]:

        return {"owner": user}

    @classmethod
    def _validate_resolved_instance(
        cls,
        *,
        instance: Document,
        context: DocumentContext
    ) -> None:
        """Document is the aggregate root; no additional validation required."""

        pass

    @classmethod
    def _add_file_hash(cls, instance: Document) -> None:

        hasher = hashlib.sha256()
        for chunk in instance.file.chunks():
            hasher.update(chunk)

        instance.file_hash = hasher.hexdigest()

    @classmethod
    def _apply_scalar_updates(
            cls,
            *,
            instance: Document,
            validated_data: dict[str, Any]
    ) -> None:
        super()._apply_scalar_updates(
            instance=instance,
            validated_data=validated_data,
        )

        if "file" in validated_data:
            cls._add_file_hash(instance)
