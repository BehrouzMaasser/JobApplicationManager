import pytest

from apps.documents.selectors.document_selector import DocumentSelector

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError
)


@pytest.mark.django_db
class TestDocumentSelectorList:

    def test_list_returns_only_user_owned_documents(
        self,
        user1,
        doc1_user1,
        doc2_user1,
        doc1_user2,
    ):
        queryset = set(DocumentSelector.list(user=user1))

        assert queryset == {
            doc1_user1,
            doc2_user1,
        }

    def test_list_without_filters_returns_all_owned_documents(
        self,
        user1,
        doc1_user1,
        doc2_user1,
    ):
        queryset = DocumentSelector.list(user=user1)

        assert {
            doc1_user1,
            doc2_user1,
        } == set(queryset)

    def test_list_filters_by_document_type_id(
        self,
        user1,
        doc1_user1,
        doc2_user1,
    ):
        filters = DocumentSelector.QueryFilter(
            document_type_id=doc1_user1.document_type.pk,
        )

        queryset = DocumentSelector.list(
            user=user1,
            filters=filters,
        )

        assert {doc1_user1} == set(queryset)

    def test_list_filters_by_document_id(
        self,
        user1,
        doc1_user1,
        doc2_user1,
    ):
        filters = DocumentSelector.QueryFilter(
            id=doc1_user1.pk,
        )

        queryset = DocumentSelector.list(
            user=user1,
            filters=filters,
        )

        assert {doc1_user1} == set(queryset)

    def test_list_applies_multiple_filters(
        self,
        user1,
        doc1_user1,
        doc2_user1,
    ):
        filters = DocumentSelector.QueryFilter(
            document_type_id=doc1_user1.document_type.pk,
            id=doc1_user1.pk,
        )

        queryset = DocumentSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {doc1_user1}

    def test_list_never_returns_foreign_document_even_with_matching_id(
        self,
        user1,
        doc1_user2,
    ):
        filters = DocumentSelector.QueryFilter(
            id=doc1_user2.pk,
        )

        queryset = DocumentSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_user_has_no_documents(
        self,
        user1,
    ):
        queryset = DocumentSelector.list(user=user1)

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_filters_match_nothing(
        self,
        user1,
        doc1_user1,
    ):
        filters = DocumentSelector.QueryFilter(
            id=999999,
        )

        queryset = DocumentSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_multiple_filters_do_not_match(
        self,
        user1,
        doc1_user1,
        doc2_user1,
    ):
        filters = DocumentSelector.QueryFilter(
            document_type_id=doc1_user1.document_type.pk,
            id=doc2_user1.pk,
        )

        queryset = DocumentSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0


@pytest.mark.django_db
class TestDocumentSelectorGet:

    def test_get_returns_document_for_owner(
        self,
        user1,
        doc1_user1,
    ):
        document = DocumentSelector.get(
            user=user1,
            document_id=doc1_user1.pk,
        )

        assert document == doc1_user1

    def test_get_raises_when_document_does_not_exist(
        self,
        user1,
    ):
        with pytest.raises(ResourceNotFoundError):
            DocumentSelector.get(
                user=user1,
                document_id=999999,
            )

    def test_get_raises_when_document_belongs_to_another_user(
        self,
        user1,
        doc1_user2,
    ):
        with pytest.raises(AccessDeniedError):
            DocumentSelector.get(
                user=user1,
                document_id=doc1_user2.pk,
            )

    def test_get_raises_infrastructure_error_for_invalid_document_id(
        self,
        user1,
    ):
        with pytest.raises(InfraStructureViolationError):
            DocumentSelector.get(
                user=user1,
                document_id="invalid-id",
            )
            