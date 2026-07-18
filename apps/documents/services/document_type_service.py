"""
Service layer for DocumentType domain logic.

This module handles creation, update, and deletion of document type records
while enforcing document type ownership and validation rules.
"""

from typing import Any

# Models
from apps.accounts.models import User
from apps.core.common.contexts.base_context import DocumentTypeContext
from apps.documents.models import DocumentType

# Selectors
from apps.documents.selectors.document_type_selector import DocumentTypeSelector

# Services
from apps.core.common.services.base_service import BaseService


# Document Type Service
class DocumentTypeService(BaseService):
    """
    Service responsible for managing DocumentType domain operations.

    Ensures strict document type ownership validation and delegates retrieval
    logic to selectors while maintaining validation consistency.
    """

    MODEL = DocumentType
    SELECTOR = DocumentTypeSelector

    CREATE_FIELDS = ("owner", "name", "description")
    SCALAR_UPDATABLE_FIELDS = ("name", "description")
    M2M_UPDATABLE_FIELDS = ()
    REQUIRED_M2M_FIELDS = ()
    NON_EMPTY_M2M_FIELDS = ()
    M2M_OWNER_FIELD_MAP = {}

    @classmethod
    def _resolve_create_dependencies(
            cls,
            user: User,
            context: DocumentTypeContext,
    ) -> dict[str, Any]:

        return {"owner": user}

    @classmethod
    def _validate_resolved_instance(
        cls,
        *,
        instance: DocumentType,
        context: DocumentTypeContext,
    ) -> None:
        """Document Type is the aggregate root; no additional validation required."""

        pass
