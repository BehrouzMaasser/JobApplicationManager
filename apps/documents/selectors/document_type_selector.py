from django.db.models import QuerySet
from apps.accounts.models import User
from apps.documents.models import DocumentType


class DocumentTypeSelector:

    @staticmethod
    def list(*, user: User) -> QuerySet[DocumentType]:

        return DocumentType.objects.filter(owner=user)
