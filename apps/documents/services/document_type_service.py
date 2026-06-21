# Models
from apps.accounts.models import User
from apps.documents.models import DocumentType

# Selectors
from apps.documents.selectors.document_type_selector import DocumentTypeSelector

# Services
from apps.workspaces.services.base_service import BaseService


class DocumentTypeService(BaseService):

    CREATE_REQUIRED_FIELDS = {
        'name'
    }

    UPDATABLE_FIELDS = {
        *CREATE_REQUIRED_FIELDS,
        'description',
    }

    @staticmethod
    def create(*, user: User, validated_data: dict) -> DocumentType:

        instance = DocumentType(
            owner=user,
            name=validated_data.get('name'),
            description=validated_data.get('description'),
        )

        # Full clean and save
        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    def update(
            *,  user: User, document_type_id: int, validated_data: dict
    ) -> DocumentType:

        instance = DocumentTypeService._resolve_document_type(
            user=user, document_type_id=document_type_id
        )

        DocumentTypeService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=DocumentTypeService.UPDATABLE_FIELDS,
        )

        # Full clean and save
        instance.full_clean()
        instance.save()

        return instance

    @staticmethod
    def remove(*, user: User, document_type_id: int) -> None:

        instance = DocumentTypeService._resolve_document_type(
            user=user, document_type_id=document_type_id
        )

        instance.delete()

    @staticmethod
    def _resolve_document_type(user: User, document_type_id: int) -> DocumentType:

        return DocumentTypeSelector.get(user=user, document_type_id=document_type_id)
