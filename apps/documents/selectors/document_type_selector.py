"""
Read-only query helpers for the DocumentType domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.documents.models import DocumentType

# Exceptions
from apps.core.exceptions.exceptions import (
    AccessDeniedError,
    InfraStructureViolationError,
    ResourceNotFoundError,
)


class DocumentTypeSelector:
    """
    Provides reusable read operations for DocumentType objects.
    """

    @dataclass
    class QueryFilter:
        id: int | None = None

    @staticmethod
    def get(*, user: User, document_type_id: int) -> DocumentType | Exception:
        """
        Retrieve a DocumentType from the DocumentTypes database.

        Returns:
            DocumentType:
                DocumentType of the provided user from the database.

        Raises:
            ResourceNotFoundError:
                If the DocumentType does not exist.

            AccessDeniedError:
                If the DocumentType does not belong to this user.

            InfraStructureViolationError:
                If an unexpected internal error is encountered while retrieving
                the DocumentType.
        """

        try:
            document_type = DocumentType.objects.get(pk=document_type_id)
        except DocumentType.DoesNotExist:
            raise ResourceNotFoundError(
                resource=f"Document Type {document_type_id}"
            )
        except ValidationError as e:
            raise InfraStructureViolationError(e) from e

        if document_type.owner != user:
            raise AccessDeniedError(
                resource=f"Document Type {document_type_id}",
                message=f"Document Type {document_type_id} does not belong to {user}",
            )

        return document_type

    @staticmethod
    def list(
        *,
        user: User,
        filters: QueryFilter | None = None,
    ) -> QuerySet[DocumentType]:
        """
        Retrieve a queryset of DocumentTypes from the DocumentTypes database.

        Args:
            user (User):
                User who owns the DocumentTypes.

            filters (QueryFilter | None = None):
                Query filters applied to the DocumentTypes.

        Returns:
            QuerySet[DocumentType]:
                - A queryset of the DocumentTypes owned by the user based on
                filters provided.
                - An empty queryset if the user owns no DocumentTypes or
                nothing matches the filters provided.
        """

        queryset = DocumentType.objects.filter(owner=user)

        if not filters:
            return queryset

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
