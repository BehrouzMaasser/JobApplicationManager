"""
Read-only query helpers for the Document domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector

# For typings
from apps.core.common.types.filters import DocumentQueryFilter
from django.db.models import QuerySet

# Models
from apps.documents.models import Document


class DocumentSelector(BaseSelector[Document]):
    """
    Selector responsible for retrieving Document objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = Document
    RESOURCE_NAME = "Document"
    LOOKUP_FIELD = "pk"
    OWNER_PATH = "owner"

    @classmethod
    def apply_filters(
            cls,
            queryset: QuerySet[Document],
            filters: DocumentQueryFilter
    ) -> QuerySet[Document]:

        if (document_type_id := filters.document_type_id) is not None:
            queryset = queryset.filter(document_type__pk=document_type_id)

        if filters.id is not None:
            queryset = queryset.filter(pk=filters.id)

        return queryset
