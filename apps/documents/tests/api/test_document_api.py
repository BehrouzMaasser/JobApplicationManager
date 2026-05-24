import pytest
from rest_framework import status

from apps.documents.models import Document


pytestmark = pytest.mark.django_db


class TestDocumentAPI:

    @pytest.fixture
    def document_url_path(self, base_api_url_path):

        return f"{base_api_url_path}documents/"

    def test_list_requires_authentication(self, api_client, document_url_path):

        response = api_client.get(document_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_documents(
            self, authenticated_client, document_url_path, doc1_user1
    ):

        response = authenticated_client.get(document_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_create_document(
            self,
            authenticated_client,
            document_url_path,
            doc1_user1_api_valid_data,
    ):

        response = authenticated_client.post(
            document_url_path,
            doc1_user1_api_valid_data,
            format="multipart"
        )

        assert response.status_code == status.HTTP_200_OK
        assert Document.objects.filter(pk=response.data["id"]).exists()
        assert response.data["name"] == doc1_user1_api_valid_data["name"]

    def test_retrieve_document(
            self, authenticated_client, doc1_user1, document_url_path
    ):

        response = authenticated_client.get(
            f"{document_url_path}{doc1_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == doc1_user1.id

    def test_update_document(
            self,
            authenticated_client,
            doc1_user1,
            document_url_path,
            doc1_user1_api_updated_valid_data
    ):

        response = authenticated_client.put(
            f"{document_url_path}{doc1_user1.id}/",
            doc1_user1_api_updated_valid_data,
            format="multipart"
        )

        assert response.status_code == status.HTTP_200_OK
        doc1_user1.refresh_from_db()
        assert doc1_user1.name == doc1_user1_api_updated_valid_data["name"]

    def test_partial_update_document(
            self,
            authenticated_client,
            doc1_user1,
            document_url_path,
            doc1_user1_api_updated_valid_data
    ):

        partial_update_api_data = doc1_user1_api_updated_valid_data.copy()
        partial_update_api_data.pop("name")

        old_name = doc1_user1.name

        response = authenticated_client.patch(
            f"{document_url_path}{doc1_user1.id}/",
            partial_update_api_data,
            format="multipart"
        )

        assert response.status_code == status.HTTP_200_OK

        doc1_user1.refresh_from_db()

        # Document Type should be changed
        assert (doc1_user1.document_type.id ==
                partial_update_api_data["document_type"])

        # Name should be unchanged
        assert doc1_user1.name == old_name

    def test_delete_document(
            self, authenticated_client, doc1_user1, document_url_path
    ):

        response = authenticated_client.delete(
            f"{document_url_path}{doc1_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert not Document.objects.filter(pk=doc1_user1.id).exists()
