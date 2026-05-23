from dataclasses import dataclass

from django.db.models import QuerySet
from apps.accounts.models import User
from apps.documents.models import Document


class DocumentSelector:

    @dataclass
    class QueryFilter:

        document_type_id: int

    @staticmethod
    def list(*, user: User, filters: None | QueryFilter) -> QuerySet[Document]:

        queryset = Document.objects.filter(owner=user)

        if not filters:
            return queryset

        if filters.document_type_id:
            queryset.filter(document_type=filters.document_type_id)

        return Document.objects.filter(owner=user)
