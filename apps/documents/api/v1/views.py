from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.mixins.document_file_response_mixin import DocumentFileResponseMixin

# Serializers
from apps.documents.api.v1.serializers import (
    DocumentTypeSerializer,
    DocumentReadSerializer,
    DocumentWriteSerializer
)

# Selectors
from apps.documents.selectors.document_type_selector import DocumentTypeSelector
from apps.documents.selectors.document_selector import DocumentSelector

# Services
from apps.documents.services.document_type_service import DocumentTypeService
from apps.documents.services.document_service import DocumentService


# ViewSets

class DocumentTypeViewSet(viewsets.ModelViewSet):

    # URL Path:
    # document-types/{id}

    permission_classes = [IsAuthenticated]
    serializer_class = DocumentTypeSerializer

    lookup_url_kwarg = "id"

    def get_queryset(self):

        return DocumentTypeSelector.list(user=self.request.user)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = DocumentTypeService.create(
            user=request.user,
            validated_data=serializer.validated_data
        )

        return Response(DocumentTypeSerializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = DocumentTypeService.update(
            user=request.user,
            document_type_id=self.kwargs['id'],
            validated_data=serializer.validated_data
        )

        return Response(DocumentTypeSerializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance = DocumentTypeService.update(
            user=request.user,
            document_type_id=self.kwargs['id'],
            validated_data=serializer.validated_data
        )

        return Response(DocumentTypeSerializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        DocumentTypeService.remove(
            user=request.user,
            document_type_id=self.kwargs['id']
        )

        return Response(status=status.HTTP_200_OK)


class DocumentViewSet(viewsets.ModelViewSet, DocumentFileResponseMixin):

    # URL Path:
    # documents/{id}

    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    lookup_url_kwarg = "id"

    def get_serializer_class(self):

        if self.action in ["list", "retrieve", "download"]:
            return DocumentReadSerializer
        else:
            return DocumentWriteSerializer

    def get_document(self):

        return DocumentSelector.get_object_or_404(
            user=self.request.user, document_id=self.kwargs['id']
        )

    @action(
        detail=True,
        methods=["get"],
        url_path="download",
    )
    def download(self, request, *args, **kwargs):

        return self.get_response()

    def get_queryset(self):

        return DocumentSelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters()
        )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = DocumentService.create(
            user=request.user,
            validated_data=serializer.validated_data
        )

        return Response(DocumentReadSerializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = DocumentService.update(
            user=request.user,
            document_id=self.kwargs['id'],
            validated_data=serializer.validated_data
        )

        return Response(DocumentReadSerializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance = DocumentService.update(
            user=request.user,
            document_id=self.kwargs['id'],
            validated_data=serializer.validated_data
        )

        return Response(DocumentReadSerializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        DocumentService.remove(
            user=request.user,
            document_id=self.kwargs['id']
        )

        return Response(status=status.HTTP_200_OK)

    def _get_queryset_filters(self):

        return DocumentSelector.QueryFilter(
            document_type_id=self.request.query_params.get("document_type")
        )
