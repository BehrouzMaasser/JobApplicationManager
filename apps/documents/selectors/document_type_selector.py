from dataclasses import dataclass

from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.documents.models import DocumentType

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError
)


class DocumentTypeSelector:

    @dataclass
    class QueryFilter:
        id: int | None = None

    @staticmethod
    def get(*, user: User, document_type_id: int) -> DocumentType:

        try:
            document_type = DocumentType.objects.get(pk=document_type_id)
        except DocumentType.DoesNotExist:
            raise ResourceNotFoundError(
                resource=f"Document Type {document_type_id}"
            )

        if document_type.owner != user:
            raise AccessDeniedError(
                resource=f"Document Type {document_type_id}",
                message=f"Document Type {document_type_id} does not belong to {user}"
            )

        return document_type

    @staticmethod
    def list(
            *, user: User, filters: QueryFilter | None = None
    ) -> QuerySet[DocumentType]:

        if filters and filters.id:
            return DocumentType.objects.filter(owner=user, pk=filters.id)

        return DocumentType.objects.filter(owner=user)
