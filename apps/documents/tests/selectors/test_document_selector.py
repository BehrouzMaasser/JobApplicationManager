import pytest

from apps.core.common.types.filters import DocumentQueryFilter
from apps.core.exceptions.exceptions import ResourceNotFoundError
from apps.documents.selectors.document_selector import DocumentSelector


@pytest.mark.django_db
class TestDocumentSelectorList:

    def test_list_returns_only_user_documents(
            self,
            user1,
            doc1_user1,
            doc2_user1,
            doc1_user2,
    ):

        queryset = DocumentSelector.list(user=user1)

        assert set(queryset) == {
            doc1_user1,
            doc2_user1,
        }

    def test_list_filters_by_document_type(
            self,
            user1,
            doc1_user1,
            doc2_user1,
    ):

        filters = DocumentQueryFilter(
            document_type_id=doc1_user1.document_type.pk,
        )

        queryset = DocumentSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {
            doc1_user1,
        }

    def test_list_filters_by_document_id(
            self,
            user1,
            doc1_user1,
            doc2_user1,
    ):

        filters = DocumentQueryFilter(
            id=doc1_user1.pk,
        )

        queryset = DocumentSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {
            doc1_user1,
        }

    def test_list_applies_multiple_filters(
            self,
            user1,
            doc1_user1,
            doc2_user1,
    ):

        filters = DocumentQueryFilter(
            id=doc1_user1.pk,
            document_type_id=doc1_user1.document_type.pk,
        )

        queryset = DocumentSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {
            doc1_user1,
        }

    def test_list_never_returns_foreign_document(
            self,
            user1,
            doc1_user2,
    ):

        filters = DocumentQueryFilter(
            id=doc1_user2.pk,
        )

        queryset = DocumentSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []

    def test_list_returns_empty_queryset_when_filters_match_nothing(
            self,
            user1,
    ):

        filters = DocumentQueryFilter(
            id=999999,
        )

        queryset = DocumentSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []


@pytest.mark.django_db
class TestDocumentSelectorGet:

    def test_get_returns_document(
            self,
            user1,
            doc1_user1,
    ):

        document = DocumentSelector.get(
            user=user1,
            obj_id=doc1_user1.pk,
        )

        assert document == doc1_user1

    def test_get_foreign_document_raises_resource_not_found(
            self,
            user1,
            doc1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            DocumentSelector.get(
                user=user1,
                obj_id=doc1_user2.pk,
            )

    def test_get_unknown_document_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            DocumentSelector.get(
                user=user1,
                obj_id=999999,
            )
