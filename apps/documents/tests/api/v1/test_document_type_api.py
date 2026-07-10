import pytest
from rest_framework import status

from apps.documents.models import DocumentType

pytestmark = pytest.mark.django_db


# =========================================================
# Fixtures
# =========================================================

@pytest.fixture
def document_type_list_url_path(base_api_url_path):
    return f"{base_api_url_path}document-types/"


@pytest.fixture
def document_type_detail_url_path(
    document_type_list_url_path,
    document_type_user1,
):
    return f"{document_type_list_url_path}{document_type_user1.id}/"


# =========================================================
# DOCUMENT TYPE LIST API
# =========================================================

class TestDocumentTypeListAPIView:

    def test_requires_authentication(
        self,
        api_client,
        document_type_list_url_path,
    ):
        response = api_client.get(document_type_list_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_only_user_document_types(
        self,
        authenticated_client,
        document_type_list_url_path,
        document_type_user1,
        document_type_user2,
    ):
        response = authenticated_client.get(document_type_list_url_path)

        assert response.status_code == status.HTTP_200_OK

        returned_ids = {item["id"] for item in response.data["results"]}

        assert document_type_user1.id in returned_ids
        assert document_type_user2.id not in returned_ids

    def test_list_pagination_structure(
        self,
        authenticated_client,
        document_type_list_url_path,
    ):
        response = authenticated_client.get(document_type_list_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data


# =========================================================
# DOCUMENT TYPE RETRIEVE
# =========================================================

class TestDocumentTypeRetrieveAPIView:

    def test_requires_authentication(
        self,
        api_client,
        document_type_detail_url_path,
    ):
        response = api_client.get(document_type_detail_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_document_type_success(
        self,
        authenticated_client,
        document_type_detail_url_path,
        document_type_user1,
    ):
        response = authenticated_client.get(document_type_detail_url_path)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == document_type_user1.id

    def test_returns_404_for_unknown_document_type(
        self,
        authenticated_client,
        document_type_list_url_path,
    ):
        response = authenticated_client.get(
            f"{document_type_list_url_path}99999999/"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["error"]["code"] == "resource_not_found"

    def test_cannot_access_foreign_document_type(
        self,
        authenticated_client,
        document_type_list_url_path,
        document_type_user2,
    ):
        response = authenticated_client.get(
            f"{document_type_list_url_path}{document_type_user2.id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"]["code"] == "access_denied"


# =========================================================
# DOCUMENT TYPE CREATE
# =========================================================

class TestDocumentTypeCreateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        document_type_list_url_path,
        doc_type1_user1_valid_data,
    ):
        response = api_client.post(
            document_type_list_url_path,
            doc_type1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_document_type_success(
        self,
        authenticated_client,
        document_type_list_url_path,
        doc_type1_user1_valid_data,
    ):
        response = authenticated_client.post(
            document_type_list_url_path,
            doc_type1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert response.data["name"] == doc_type1_user1_valid_data["name"]

        assert DocumentType.objects.filter(
            pk=response.data["id"],
        ).exists()

    def test_invalid_payload_rejected(
        self,
        authenticated_client,
        document_type_list_url_path,
    ):
        response = authenticated_client.post(
            document_type_list_url_path,
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


# =========================================================
# DOCUMENT TYPE UPDATE / PATCH
# =========================================================

class TestDocumentTypeUpdateAPIView:

    def test_requires_authentication(
        self,
        api_client,
        document_type_detail_url_path,
        doc_type1_user1_valid_data,
    ):
        response = api_client.put(
            document_type_detail_url_path,
            doc_type1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_full_update_success(
        self,
        authenticated_client,
        document_type_user1,
        document_type_detail_url_path,
        doc_type1_user1_valid_data,
    ):
        response = authenticated_client.put(
            document_type_detail_url_path,
            doc_type1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        document_type_user1.refresh_from_db()

        assert document_type_user1.name == doc_type1_user1_valid_data["name"]
        assert (
            document_type_user1.description
            == doc_type1_user1_valid_data["description"]
        )

    def test_partial_update_success(
        self,
        authenticated_client,
        document_type_user1,
        document_type_detail_url_path,
    ):
        old_name = document_type_user1.name

        response = authenticated_client.patch(
            document_type_detail_url_path,
            {"description": "Updated description"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        document_type_user1.refresh_from_db()

        assert document_type_user1.description == "Updated description"
        assert document_type_user1.name == old_name

    def test_put_requires_all_required_fields(
        self,
        authenticated_client,
        document_type_detail_url_path,
    ):
        response = authenticated_client.put(
            document_type_detail_url_path,
            {"description": "Only description"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_update_foreign_document_type(
        self,
        authenticated_client,
        document_type_user2,
        document_type_list_url_path,
        doc_type1_user1_valid_data,
    ):
        response = authenticated_client.put(
            f"{document_type_list_url_path}{document_type_user2.id}/",
            doc_type1_user1_valid_data,
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"]["code"] == "access_denied"


# =========================================================
# DOCUMENT TYPE DELETE
# =========================================================

class TestDocumentTypeDeleteAPIView:

    def test_requires_authentication(
        self,
        api_client,
        document_type_detail_url_path,
    ):
        response = api_client.delete(document_type_detail_url_path)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_success(
        self,
        authenticated_client,
        document_type_user1,
        document_type_detail_url_path,
    ):
        response = authenticated_client.delete(document_type_detail_url_path)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not DocumentType.objects.filter(
            pk=document_type_user1.id
        ).exists()

    def test_delete_idempotency_or_not_found(
        self,
        authenticated_client,
        document_type_detail_url_path,
    ):
        authenticated_client.delete(document_type_detail_url_path)

        response = authenticated_client.delete(document_type_detail_url_path)

        assert response.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_204_NO_CONTENT,
        )

    def test_cannot_delete_foreign_document_type(
        self,
        authenticated_client,
        document_type_user2,
        document_type_list_url_path,
    ):
        response = authenticated_client.delete(
            f"{document_type_list_url_path}{document_type_user2.id}/"
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["error"]["code"] == "access_denied"
