from rest_framework import serializers

# Models
from apps.documents.models import (
    DocumentType,
    Document,
)


# Serializers
class DocumentTypeSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=40,
        required=True,
        allow_blank=False,
        allow_null=False
    )
    description = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=False
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
            "updated_at"
        ]


class DocumentSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=50,
        required=True,
        allow_blank=False,
        allow_null=False
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
