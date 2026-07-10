import pytest

from apps.documents.selectors.document_type_selector import DocumentTypeSelector

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError
)


@pytest.mark.django_db
class TestDocumentTypeSelectorList:

    def test_list_returns_only_user_owned_document_types(
        self,
        user1,
        document_type_user1,
        document_type2_user1,
        document_type_user2,
    ):
        queryset = set(DocumentTypeSelector.list(user=user1))

        assert queryset == {
            document_type_user1,
            document_type2_user1,
        }

    def test_list_without_filters_returns_all_owned_document_types(
        self,
        user1,
        document_type_user1,
        document_type2_user1,
    ):
        queryset = DocumentTypeSelector.list(user=user1)

        assert {
            document_type_user1,
            document_type2_user1,
        } == set(queryset)

    def test_list_filters_by_document_type_id(
        self,
        user1,
        document_type_user1,
        document_type2_user1,
    ):
        filters = DocumentTypeSelector.QueryFilter(
            id=document_type_user1.pk,
        )

        queryset = DocumentTypeSelector.list(
            user=user1,
            filters=filters,
        )

        assert {document_type_user1} == set(queryset)

    def test_list_never_returns_foreign_document_type_even_with_matching_id(
        self,
        user1,
        document_type_user2,
    ):
        filters = DocumentTypeSelector.QueryFilter(
            id=document_type_user2.pk,
        )

        queryset = DocumentTypeSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_user_has_no_document_types(
        self,
        user2,
    ):
        queryset = DocumentTypeSelector.list(user=user2)

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_filters_match_nothing(
        self,
        user1,
    ):
        filters = DocumentTypeSelector.QueryFilter(
            id=999999,
        )

        queryset = DocumentTypeSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0


@pytest.mark.django_db
class TestDocumentTypeSelectorGet:

    def test_get_returns_document_type_for_owner(
        self,
        user1,
        document_type_user1,
    ):
        document_type = DocumentTypeSelector.get(
            user=user1,
            document_type_id=document_type_user1.pk,
        )

        assert document_type == document_type_user1

    def test_get_raises_when_document_type_does_not_exist(
        self,
        user1,
    ):
        with pytest.raises(ResourceNotFoundError):
            DocumentTypeSelector.get(
                user=user1,
                document_type_id=999999,
            )

    def test_get_raises_when_document_type_belongs_to_another_user(
        self,
        user1,
        document_type_user2,
    ):
        with pytest.raises(AccessDeniedError):
            DocumentTypeSelector.get(
                user=user1,
                document_type_id=document_type_user2.pk,
            )

    def test_get_raises_infrastructure_error_for_invalid_document_type_id(
        self,
        user1,
    ):
        with pytest.raises(InfraStructureViolationError):
            DocumentTypeSelector.get(
                user=user1,
                document_type_id="invalid-id",
            )
