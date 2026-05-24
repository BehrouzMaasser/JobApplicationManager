import pytest
from rest_framework import status

from apps.documents.models import DocumentType


pytestmark = pytest.mark.django_db


class TestDocumentTypeAPI:

    @pytest.fixture
    def document_type_url_path(self, base_api_url_path):

        return f"{base_api_url_path}document-types/"

    def test_list_requires_authentication(self, api_client, document_type_url_path):

        response = api_client.get(document_type_url_path)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_document_types(
            self, authenticated_client,
            document_type_url_path,
            document_type_user1
    ):

        response = authenticated_client.get(document_type_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_create_document_type(
            self,
            authenticated_client,
            document_type_url_path,
            doc_type1_user1_valid_data,
    ):

        response = authenticated_client.post(
            document_type_url_path,
            doc_type1_user1_valid_data,
            format="multipart"
        )

        assert response.status_code == status.HTTP_200_OK
        assert DocumentType.objects.filter(pk=response.data["id"]).exists()
        assert response.data["name"] == doc_type1_user1_valid_data["name"]

    def test_retrieve_document(
            self, authenticated_client, document_type_user1, document_type_url_path
    ):

        response = authenticated_client.get(
            f"{document_type_url_path}{document_type_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == document_type_user1.id

    def test_update_document(
            self,
            authenticated_client,
            document_type_user1,
            document_type_url_path,
            doc_type1_user1_valid_data
    ):

        response = authenticated_client.put(
            f"{document_type_url_path}{document_type_user1.id}/",
            doc_type1_user1_valid_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        document_type_user1.refresh_from_db()
        assert document_type_user1.name == doc_type1_user1_valid_data["name"]

    def test_partial_update_document(
            self,
            authenticated_client,
            document_type_user1,
            document_type_url_path,
            doc_type1_user1_valid_data
    ):

        partial_update_api_data = doc_type1_user1_valid_data.copy()
        partial_update_api_data.pop("name")

        old_name = document_type_user1.name

        response = authenticated_client.patch(
            f"{document_type_url_path}{document_type_user1.id}/",
            partial_update_api_data,
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK

        document_type_user1.refresh_from_db()

        # Description should be changed
        assert (document_type_user1.description ==
                partial_update_api_data["description"])

        # Name should be unchanged
        assert document_type_user1.name == old_name

    def test_delete_document(
            self, authenticated_client, document_type_user1, document_type_url_path
    ):

        response = authenticated_client.delete(
            f"{document_type_url_path}{document_type_user1.id}/"
        )

        assert response.status_code == status.HTTP_200_OK
        assert not DocumentType.objects.filter(pk=document_type_user1.id).exists()
