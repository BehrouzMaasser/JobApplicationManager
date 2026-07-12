"""
Read-only query helpers for the DocumentType domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector

# For Typings
from apps.core.common.types.filters import DocumentTypeQueryFilter
from django.db.models import QuerySet

# Models
from apps.documents.models import DocumentType


class DocumentTypeSelector(BaseSelector):
    """
    Selector responsible for retrieving DocumentType objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = DocumentType
    RESOURCE_NAME = "Document Type"
    LOOKUP_FIELD = "pk"
    OWNER_PATH = "owner"

    @classmethod
    def apply_filters(
            cls,
            queryset: QuerySet[DocumentType],
            filters: DocumentTypeQueryFilter
    ) -> QuerySet[DocumentType]:

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
