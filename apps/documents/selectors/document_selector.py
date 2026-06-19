from dataclasses import dataclass

from django.db.models import QuerySet
from django import shortcuts

from apps.accounts.models import User
from apps.documents.models import Document


class DocumentSelector:

    @dataclass
    class QueryFilter:

        document_type_id: int | None = None
        id: int | None = None

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

    @staticmethod
    def get_object_or_404(*, user: User, document_id: int) -> Document:

        return shortcuts.get_object_or_404(Document, owner=user, id=document_id)
