import pytest

from apps.core.common.types.filters import DocumentTypeQueryFilter
from apps.core.exceptions.exceptions import ResourceNotFoundError
from apps.documents.selectors.document_type_selector import (
    DocumentTypeSelector,
)


@pytest.mark.django_db
class TestDocumentTypeSelectorList:

    def test_list_returns_only_user_document_types(
            self,
            user1,
            document_type_user1,
            document_type2_user1,
            document_type_user2,
    ):

        queryset = DocumentTypeSelector.list(user=user1)

        assert set(queryset) == {
            document_type_user1,
            document_type2_user1,
        }

    def test_list_filters_by_document_type_id(
            self,
            user1,
            document_type_user1,
            document_type2_user1,
    ):

        filters = DocumentTypeQueryFilter(
            id=document_type_user1.pk,
        )

        queryset = DocumentTypeSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {
            document_type_user1,
        }

    def test_list_never_returns_foreign_document_type(
            self,
            user1,
            document_type_user2,
    ):

        filters = DocumentTypeQueryFilter(
            id=document_type_user2.pk,
        )

        queryset = DocumentTypeSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []

    def test_list_returns_empty_queryset_when_filter_matches_nothing(
            self,
            user1,
    ):

        filters = DocumentTypeQueryFilter(
            id=999999,
        )

        queryset = DocumentTypeSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []


@pytest.mark.django_db
class TestDocumentTypeSelectorGet:

    def test_get_returns_document_type(
            self,
            user1,
            document_type_user1,
    ):

        document_type = DocumentTypeSelector.get(
            user=user1,
            obj_id=document_type_user1.pk,
        )

        assert document_type == document_type_user1

    def test_get_foreign_document_type_raises_resource_not_found(
            self,
            user1,
            document_type_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            DocumentTypeSelector.get(
                user=user1,
                obj_id=document_type_user2.pk,
            )

    def test_get_unknown_document_type_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            DocumentTypeSelector.get(
                user=user1,
                obj_id=999999,
            )
