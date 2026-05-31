import pytest

from apps.documents.selectors.document_selector import DocumentSelector


@pytest.mark.django_db
class TestDocumentSelector:

    def test_list_returns_only_user_documents(
            self,
            user,
            doc1_user1,
            doc2_user1,
            doc1_user2,
    ):

        result = DocumentSelector.list(user=user)

        assert len(result) == 2
        assert set(result) == {doc1_user1, doc2_user1}

    def test_list_filters_by_document_type(
            self,
            user,
            doc1_user1,
            doc2_user1,
            doc1_user2,
    ):

        filters = DocumentSelector.QueryFilter(
            document_type_id=doc1_user1.document_type.pk
        )

        result = DocumentSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [doc1_user1]

    def test_list_filters_by_id(
            self,
            user,
            doc1_user1,
            doc2_user1,
            doc1_user2,
    ):

        filters = DocumentSelector.QueryFilter(
            id=doc1_user1.pk
        )

        result = DocumentSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [doc1_user1]

    def test_list_combines_filters(
            self,
            user,
            doc1_user1,
            doc2_user1,
    ):

        filters = DocumentSelector.QueryFilter(
            document_type_id=doc1_user1.document_type.pk,
            id=doc1_user1.pk,
        )

        result = DocumentSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [doc1_user1]

    def test_list_does_not_return_other_users_document(
            self,
            user,
            doc1_user1,
            doc1_user2,
    ):

        filters = DocumentSelector.QueryFilter(
            id=doc1_user2.pk
        )

        result = DocumentSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == []
