"""
REST API views for managing the Documents domain.

This module defines DRF ViewSets that:
- Delegate read operations to selector layer
- Delegate write operations to service layer
- Provide document download functionality
"""

from django.db.models import QuerySet

# DRF
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

from apps.core.common.types.filters import DocumentQueryFilter
# Mixins
from apps.core.mixins.document_file_response_mixin import (
    DocumentFileResponseMixin,
)

# Serializers
from apps.documents.api.v1.serializers import (
    DocumentTypeSerializer,
    DocumentReadSerializer,
    DocumentWriteSerializer,
)

# Models (for typing only)
from apps.documents.models import (
    Document,
    DocumentType,
)

# Selectors
from apps.documents.selectors.document_selector import (
    DocumentSelector,
)
from apps.documents.selectors.document_type_selector import (
    DocumentTypeSelector,
)

# Services
from apps.documents.services.document_service import DocumentService
from apps.documents.services.document_type_service import (
    DocumentTypeService,
)

# Base ViewSets
from apps.core.common.api.viewsets import (
    BaseIdServiceViewSet,
)


# =========================================================
# Document Type
# =========================================================

class DocumentTypeViewSet(BaseIdServiceViewSet):
    """
    CRUD API for Document Types.
    """

    service_class = DocumentTypeService
    selector_class = DocumentTypeSelector

    read_serializer_class = DocumentTypeSerializer
    write_serializer_class = DocumentTypeSerializer

    lookup_url_kwarg = "id"
    selector_lookup_field = "document_type_id"
    service_lookup_id = "document_type_id"

    def get_queryset(self) -> QuerySet[DocumentType]:
        """
        Return all document types for the authenticated user.
        """

        return self.selector.list(user=self.request.user)


# =========================================================
# Document
# =========================================================

class DocumentViewSet(
    BaseIdServiceViewSet,
    DocumentFileResponseMixin,
):
    """
    CRUD API for Documents.

    Also provides a download endpoint for the stored document file.
    """

    parser_classes = (MultiPartParser, FormParser)

    service_class = DocumentService
    selector_class = DocumentSelector

    read_serializer_class = DocumentReadSerializer
    write_serializer_class = DocumentWriteSerializer

    lookup_url_kwarg = "id"
    selector_lookup_field = "document_id"
    service_lookup_id = "document_id"

    @action(
        detail=True,
        methods=["get"],
        url_path="download",
    )
    def download(self, request, *args, **kwargs):
        """
        Download the document file.
        """

        return self.get_response()

    def get_queryset(self) -> QuerySet[Document]:
        """
        Return filtered documents for the authenticated user.
        """

        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def _get_queryset_filters(
        self,
    ) -> DocumentQueryFilter:
        """
        Build selector filter object from query parameters.
        """

        return DocumentQueryFilter(
            document_type_id=self.request.query_params.get(
                "document_type"
            ),
        )
