import pytest

from apps.documents.selectors.document_type_selector import DocumentTypeSelector


@pytest.mark.django_db
class TestDocumentTypeSelector:

    def test_list_returns_only_user_document_types(
            self,
            user,
            document_type_user1,
            document_type2_user1,
            document_type_user2,
    ):

        result = DocumentTypeSelector.list(user=user)

        assert len(result) == 2
        assert set(result) == {document_type_user1, document_type2_user1}

    def test_list_filters_by_id(
            self,
            user,
            document_type_user1,
            document_type2_user1,
            document_type_user2,
    ):

        filters = DocumentTypeSelector.QueryFilter(
            id=document_type_user1.pk
        )

        result = DocumentTypeSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [document_type_user1]

    def test_list_does_not_return_other_users_document_type_by_id(
            self,
            document_type_user1,
            document_type_user2,
    ):

        filters = DocumentTypeSelector.QueryFilter(
            id=document_type_user2.pk
        )

        result = DocumentTypeSelector.list(
            user=document_type_user1.owner,
            filters=filters,
        )

        assert list(result) == []
