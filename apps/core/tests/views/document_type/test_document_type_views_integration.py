import pytest

from django.urls import reverse


pytestmark = pytest.mark.django_db


class TestDocumentTypeListView:

    def test_redirects_anonymous_user(self, client):
        response = client.get(reverse("document-type-list-web"))

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access(self, client, user1):
        client.force_login(user1)

        response = client.get(
            reverse("document-type-list-web")
        )

        assert response.status_code == 200
        assert "document_types" in response.context

    def test_authenticated_user_get_list(self, client, document_type_user1):
        client.force_login(document_type_user1.owner)

        response = client.get(
            reverse("document-type-list-web")
        )

        assert response.status_code == 200
        assert document_type_user1 in response.context["document_types"]

    def test_list_only_returns_users_document_types(
            self,
            client,
            user2,
            document_type_user1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse("document-type-list-web")
        )

        assert response.status_code == 200
        assert document_type_user1 not in response.context["document_types"]


class TestDocumentTypeCreateView:

    def test_redirects_anonymous_user(
        self,
        client,
    ):
        response = client.get(
            reverse(
                "document-type-create-web",
            )
        )

        assert response.status_code == 302

    def test_get_returns_page(
        self,
        client,
        user1
    ):
        client.force_login(user1)

        response = client.get(
            reverse(
                "document-type-create-web",
            )
        )

        assert response.status_code == 200

    def test_valid_post_creates_document_type(
        self,
        client,
        user1,
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "document-type-create-web",
            ),
            {
                "name": "T1",
            },
        )

        assert response.status_code == 302


class TestDocumentTypeDetailView:

    def test_redirects_anonymous_user(
        self,
        client,
        document_type_user1,
    ):
        response = client.get(
            reverse(
                "document-type-detail-web",
                kwargs={
                    "pk": document_type_user1.pk,
                },
            )
        )

        assert response.status_code == 302
        assert response.context is None

    def test_authenticated_user_can_access(
        self,
        client,
        document_type_user1,
    ):
        client.force_login(document_type_user1.owner)

        response = client.get(
            reverse(
                "document-type-detail-web",
                kwargs={
                    "pk": document_type_user1.pk,
                }
            )
        )

        assert response.status_code == 200

        assert response.context["document_type"] == document_type_user1

    def test_user_cannot_view_other_users_document_type(
            self,
            client,
            user2,
            document_type_user1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse(
                "document-type-detail-web",
                kwargs={"pk": document_type_user1.pk},
            )
        )

        assert response.status_code == 404


class TestDocumentTypeUpdateView:

    def test_get_returns_page(
        self,
        client,
        document_type_user1,
    ):
        client.force_login(document_type_user1.owner)

        response = client.get(
            reverse(
                "document-type-edit-web",
                kwargs={
                    "pk": document_type_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_updates_document_type(
        self,
        client,
        document_type_user1,
    ):
        client.force_login(document_type_user1.owner)

        response = client.post(
            reverse(
                "document-type-edit-web",
                kwargs={
                    "pk": document_type_user1.pk,
                },
            ),
            {
                "name": "T1 Updated",
            },
        )

        assert response.status_code == 302

        document_type_user1.refresh_from_db()

        assert document_type_user1.name == "T1 Updated"

    def test_user_cannot_update_other_users_document_type(
            self,
            client,
            user2,
            document_type_user1,
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "document-type-edit-web",
                kwargs={"pk": document_type_user1.pk},
            ),
            {
                "name": "Cant Update",
            },
        )

        assert response.status_code == 404

        document_type_user1.refresh_from_db()

        assert document_type_user1.name != "Cant Update"


class TestDocumentTypeDeleteView:

    def test_get_returns_confirmation(
        self,
        client,
        document_type_user1
    ):
        client.force_login(document_type_user1.owner)

        response = client.get(
            reverse(
                "document-type-delete-web",
                kwargs={
                    "pk": document_type_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_post_deletes_document_type(
        self,
        client,
        document_type_user1
    ):
        client.force_login(document_type_user1.owner)

        response = client.post(
            reverse(
                "document-type-delete-web",
                kwargs={
                    "pk": document_type_user1.pk,
                },
            )
        )

        assert response.status_code == 302

        from apps.documents.models import DocumentType

        assert not DocumentType.objects.filter(
            pk=document_type_user1.pk
        ).exists()

    def test_user_cannot_delete_other_users_document_type(
            self,
            client,
            user2,
            document_type_user1,
    ):
        client.force_login(user2)

        response = client.post(

            reverse(
                "document-type-delete-web",
                kwargs={"pk": document_type_user1.pk},
            )
        )

        assert response.status_code == 404

        from apps.documents.models import DocumentType

        assert DocumentType.objects.filter(
            pk=document_type_user1.pk
        ).exists()
