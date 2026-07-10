"""
Read-only query helpers for the Document domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from dataclasses import dataclass

from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.documents.models import Document

# Exceptions
from apps.core.exceptions.exceptions import (
    AccessDeniedError,
    InfraStructureViolationError,
    ResourceNotFoundError,
)


class DocumentSelector:
    """
    Provides reusable read operations for Document objects.
    """

    @dataclass
    class QueryFilter:
        document_type_id: int | None = None
        id: int | None = None

    @staticmethod
    def get(*, user: User, document_id: int) -> Document | Exception:
        """
        Retrieve a Document from the Documents database.

        Returns:
            Document:
                Document of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the Document does not exist.

            AccessDeniedError:
                If the Document does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving
                the Document.
        """

        try:
            document = Document.objects.get(pk=document_id)
        except Document.DoesNotExist:
            raise ResourceNotFoundError(
                resource=f"Document {document_id}"
            )
        except Exception as e:
            raise InfraStructureViolationError(e) from e

        if document.owner != user:
            raise AccessDeniedError(
                resource=f"Document {document_id}",
                message=f"Document {document_id} does not belong to {user}",
            )

        return document

    @staticmethod
    def list(
        *,
        user: User,
        filters: None | QueryFilter = None,
    ) -> QuerySet[Document]:
        """
        Retrieve a queryset of Documents from the Documents database.

        Args:
            user (User):
                User who owns the Documents.

            filters (QueryFilter | None = None):
                Query filters applied to the Documents.

        Returns:
            QuerySet[Document]:
                - A queryset of the Documents owned by the user based on
                filters provided.
                - An empty queryset if the user owns no Documents or nothing
                matches the filters provided.
        """

        queryset = Document.objects.filter(owner=user)

        if not filters:
            return queryset

        if document_type_id := filters.document_type_id:
            queryset = queryset.filter(document_type__pk=document_type_id)

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
