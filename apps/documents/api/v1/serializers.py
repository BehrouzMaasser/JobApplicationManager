"""
REST API serializers for the Documents domain.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse

# Models
from apps.documents.models import (
    DocumentType,
    Document,
)


# Serializers

# =========================================================
# Document Type
# =========================================================

class DocumentTypeSerializer(serializers.ModelSerializer):
    """
    Serialize document type data for API requests and responses.
    """

    name = serializers.CharField(
        max_length=40,
        required=True,
        allow_blank=False,
        allow_null=False,
    )

    description = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=False,
    )

    class Meta:

        model = DocumentType

        fields = [
            "id",
            "owner",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]


# =========================================================
# Document
# =========================================================

class DocumentBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing the common fields shared by document
    read and write serializers.
    """

    name = serializers.CharField(
        max_length=50,
        required=True,
        allow_blank=False,
        allow_null=False,
    )

    document_type = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.all(),
        required=True,
        allow_null=False,
    )

    class Meta:

        model = Document

        fields = [
            "id",
            "owner",
            "name",
            "created_at",
            "updated_at",
            "document_type",
        ]

        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]


class DocumentReadSerializer(DocumentBaseSerializer):
    """
    Serialize document data for read operations, including the download URL.
    """

    file_url = serializers.SerializerMethodField(read_only=True)

    class Meta(DocumentBaseSerializer.Meta):

        fields = [
            *DocumentBaseSerializer.Meta.fields,
            "file_url",
        ]

    def get_file_url(self, document: Document) -> str | None:
        """
        Return the absolute download URL for the document when a request
        is available, otherwise return the relative URL.
        """

        request = self.context.get("request")

        url = reverse(
            "document-download",
            kwargs={"id": document.pk},
        )

        if request:
            return request.build_absolute_uri(url)

        return url


class DocumentWriteSerializer(DocumentBaseSerializer):
    """
    Serialize document data for create and update operations.
    """

    class Meta(DocumentBaseSerializer.Meta):

        fields = [
            *DocumentBaseSerializer.Meta.fields,
            "file",
        ]
