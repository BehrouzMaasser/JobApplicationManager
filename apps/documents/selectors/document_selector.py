from dataclasses import dataclass

from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.documents.models import Document

# Exceptions
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError
)


class DocumentSelector:

    @dataclass
    class QueryFilter:

        document_type_id: int | None = None
        id: int | None = None

    @staticmethod
    def get(*, user: User, document_id: int) -> Document:

        try:
            document = Document.objects.get(pk=document_id)
        except Document.DoesNotExist:
            raise ResourceNotFoundError(resource=f"Document {document_id}")

        if document.owner != user:
            raise AccessDeniedError(
                resource=f"Document {document_id}",
                message=f"Document {document_id} does not belong to {user}"
            )

        return document

    @staticmethod
    def list(
            *, user: User, filters: None | QueryFilter = None
    ) -> QuerySet[Document]:

        queryset = Document.objects.filter(owner=user)

        if not filters:
            return queryset

        if filters.document_type_id:
            queryset = queryset.filter(document_type__pk=filters.document_type_id)

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
