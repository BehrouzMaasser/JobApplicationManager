import pytest
from rest_framework import status

from apps.documents.models import Document

pytestmark = pytest.mark.django_db


# =========================================================
# Fixtures
# =========================================================

@pytest.fixture
def document_list_url_path(base_api_url_path):
    return f"{base_api_url_path}documents/"


@pytest.fixture
def document_detail_url_path(document_list_url_path, doc1_user1):
    return f"{document_list_url_path}{doc1_user1.id}/"


# =========================================================
# DOCUMENT LIST API
# =========================================================

class TestDocumentListAPIView:

    def test_requires_authentication(
        self,
        api_client,
        document_list_url_path,
    ):
        response = api_client.get(document_list_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_only_user_documents(
        self,
        authenticated_client,
        document_list_url_path,
        doc1_user1,
        doc1_user2,
    ):
        response = authenticated_client.get(document_list_url_path)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {
            item["id"] for item in response.data["results"]
        }

        assert doc1_user1.id in returned_ids
        assert doc1_user2.id not in returned_ids

    def test_list_pagination_structure(
        self,
        authenticated_client,
        document_list_url_path,
    ):
        response = authenticated_client.get(document_list_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data


# =========================================================
# DOCUMENT RETRIEVE
# =========================================================

class TestDocumentRetrieveAPIView:

    def test_requires_authentication(
        self,
        api_client,
        document_detail_url_path,
    ):
        response = api_client.get(document_detail_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_success(
        self,
        authenticated_client,
        document_detail_url_path,
        doc1_user1,
    ):
        response = authenticated_client.get(document_detail_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == doc1_user1.id

    def test_returns_404_for_unknown_document(
        self,
        authenticated_client,
        document_list_url_path,
    ):
        response = authenticated_client.get(
            f"{document_list_url_path}999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_cannot_access_foreign_document(
        self,
        authenticated_client,
        document_list_url_path,
        doc1_user2,
    ):
        response = authenticated_client.get(
            f"{document_list_url_path}{doc1_user2.id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"]["code"] == "access_denied"


# =========================================================
# DOCUMENT CREATE
# =========================================================

class TestDocumentCreateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        document_list_url_path,
        doc1_user1_api_valid_data,
    ):
        response = api_client.post(
            document_list_url_path,
            doc1_user1_api_valid_data,
            format="multipart",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_success(
        self,
        authenticated_client,
        document_list_url_path,
        doc1_user1_api_valid_data,
    ):
        response = authenticated_client.post(
            document_list_url_path,
            doc1_user1_api_valid_data,
            format="multipart",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert response.data["name"] == doc1_user1_api_valid_data["name"]

        assert Document.objects.filter(
            pk=response.data["id"]
        ).exists()

    def test_invalid_payload_rejected(
        self,
        authenticated_client,
        document_list_url_path,
    ):
        response = authenticated_client.post(
            document_list_url_path,
            {},
            format="multipart",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =========================================================
# DOCUMENT UPDATE / PATCH
# =========================================================

class TestDocumentUpdateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        document_detail_url_path,
        doc1_user1_api_updated_valid_data,
    ):
        response = api_client.put(
            document_detail_url_path,
            doc1_user1_api_updated_valid_data,
            format="multipart",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_full_update_success(
        self,
        authenticated_client,
        doc1_user1,
        document_detail_url_path,
        doc1_user1_api_updated_valid_data,
    ):
        response = authenticated_client.put(
            document_detail_url_path,
            doc1_user1_api_updated_valid_data,
            format="multipart",
        )

        assert response.status_code == status.HTTP_200_OK

        doc1_user1.refresh_from_db()

        assert (
            doc1_user1.name
            == doc1_user1_api_updated_valid_data["name"]
        )

    def test_partial_update_success(
        self,
        authenticated_client,
        doc1_user1,
        document_detail_url_path,
        doc1_user1_api_updated_valid_data,
    ):
        payload = doc1_user1_api_updated_valid_data.copy()
        payload.pop("name")

        old_name = doc1_user1.name

        response = authenticated_client.patch(
            document_detail_url_path,
            payload,
            format="multipart",
        )

        assert response.status_code == status.HTTP_200_OK

        doc1_user1.refresh_from_db()

        assert doc1_user1.name == old_name
        assert doc1_user1.document_type.id == payload["document_type"]

    def test_put_requires_all_required_fields(
        self,
        authenticated_client,
        document_detail_url_path,
    ):
        response = authenticated_client.put(
            document_detail_url_path,
            {},
            format="multipart",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_update_foreign_document(
        self,
        authenticated_client,
        document_list_url_path,
        doc1_user2,
        doc1_user1_api_updated_valid_data,
    ):
        response = authenticated_client.put(
            f"{document_list_url_path}{doc1_user2.id}/",
            doc1_user1_api_updated_valid_data,
            format="multipart",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN


# =========================================================
# DOCUMENT DELETE
# =========================================================

class TestDocumentDeleteAPIView:

    def test_requires_authentication(
        self,
        api_client,
        document_detail_url_path,
    ):
        response = api_client.delete(document_detail_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_success(
        self,
        authenticated_client,
        document_detail_url_path,
        doc1_user1,
    ):
        response = authenticated_client.delete(document_detail_url_path)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Document.objects.filter(
            pk=doc1_user1.id
        ).exists()

    def test_delete_idempotency_or_not_found(
        self,
        authenticated_client,
        document_detail_url_path,
    ):
        authenticated_client.delete(document_detail_url_path)

        response = authenticated_client.delete(document_detail_url_path)

        assert response.status_code in (
            status.HTTP_204_NO_CONTENT,
            status.HTTP_404_NOT_FOUND,
        )

    def test_cannot_delete_foreign_document(
        self,
        authenticated_client,
        document_list_url_path,
        doc1_user2,
    ):
        response = authenticated_client.delete(
            f"{document_list_url_path}{doc1_user2.id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
