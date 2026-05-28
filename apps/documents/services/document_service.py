from rest_framework.exceptions import ValidationError

# Models

from apps.accounts.models import User
from apps.documents.models import Document

# Services
from apps.workspaces.services.base_service import BaseService


class DocumentService(BaseService):

    CREATE_REQUIRED_FIELDS = {
        "name",
        "document_type",
        "file"
    }

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    def create(*, user: User, validated_data: dict) -> Document:

        instance = Document(
            owner=user,
            name=validated_data.get("name"),
            document_type=validated_data.get("document_type"),
            file=validated_data.get("file")
        )

        # Full clean and save

        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    def update(*, user: User, document_id: int, validated_data: dict) -> Document:

        instance = DocumentService._resolve_document(
            user=user,
            document_id=document_id
        )

        DocumentService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=DocumentService.UPDATABLE_FIELDS
        )

        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    def remove(*, user: User, document_id: int) -> None:

        instance = DocumentService._resolve_document(
            user=user, document_id=document_id
        )

        instance.delete()

    @staticmethod
    def _resolve_document(user: User, document_id: int) -> Document:

        try:
            return user.documents.get(pk=document_id)
        except Document.DoesNotExist:
            raise ValidationError({'Document': "Document Not Found"})
