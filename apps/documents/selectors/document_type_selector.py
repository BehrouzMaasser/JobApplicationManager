from dataclasses import dataclass

from django.db.models import QuerySet
from apps.accounts.models import User
from apps.documents.models import DocumentType


class DocumentTypeSelector:

    @dataclass
    class QueryFilter:
        id: int | None = None

    @staticmethod
    def list(
            *, user: User, filters: QueryFilter | None = None
    ) -> QuerySet[DocumentType]:

        if filters and filters.id:
            return DocumentType.objects.filter(owner=user, pk=filters.id)

        return DocumentType.objects.filter(owner=user)
