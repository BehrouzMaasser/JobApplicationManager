import pytest

from django.urls import reverse


pytestmark = pytest.mark.django_db


class TestDocumentListView:

    def test_redirects_anonymous_user(self, client):
        response = client.get(reverse("document-list-web"))

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access(self, client, user1):
        client.force_login(user1)

        response = client.get(
            reverse("document-list-web")
        )

        assert response.status_code == 200
        assert "documents" in response.context

    def test_authenticated_user_get_list(self, client, doc1_user1):
        client.force_login(doc1_user1.owner)

        response = client.get(
            reverse("document-list-web")
        )

        assert response.status_code == 200
        assert doc1_user1 in response.context["documents"]

    def test_list_only_returns_users_documents(
            self,
            client,
            user2,
            doc1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse("document-list-web")
        )

        assert response.status_code == 200
        assert doc1_user1 not in response.context["documents"]


class TestDocumentCreateView:

    def test_redirects_anonymous_user(
        self,
        client,
    ):
        response = client.get(
            reverse(
                "document-create-web",
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
                "document-create-web",
            )
        )

        assert response.status_code == 200

    def test_valid_post_creates_document(
        self,
        client,
        document_type_user1,
        api_upload_file1
    ):
        client.force_login(document_type_user1.owner)

        response = client.post(
            reverse(
                "document-create-web",
            ),
            {
                "name": "T1",
                "document_type": document_type_user1.pk,
                "file": api_upload_file1
            },
        )

        assert response.status_code == 302


class TestDocumentDetailView:

    def test_redirects_anonymous_user(
        self,
        client,
        doc1_user1,
    ):
        response = client.get(
            reverse(
                "document-detail-web",
                kwargs={
                    "pk": doc1_user1.pk,
                },
            )
        )

        assert response.status_code == 302
        assert response.context is None

    def test_authenticated_user_can_access(
        self,
        client,
        doc1_user1,
    ):
        client.force_login(doc1_user1.owner)

        response = client.get(
            reverse(
                "document-detail-web",
                kwargs={
                    "pk": doc1_user1.pk,
                }
            )
        )

        assert response.status_code == 200

        assert response.context["document"] == doc1_user1

    def test_user_cannot_view_other_users_document(
            self,
            client,
            user2,
            doc1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse(
                "document-detail-web",
                kwargs={"pk": doc1_user1.pk},
            )
        )

        assert response.status_code == 403


class TestDocumentUpdateView:

    def test_get_returns_page(
        self,
        client,
        doc1_user1,
    ):
        client.force_login(doc1_user1.owner)

        response = client.get(
            reverse(
                "document-edit-web",
                kwargs={
                    "pk": doc1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_updates_document(
        self,
        client,
        doc1_user1,
        document_type2_user1,
        api_upload_file2
    ):
        client.force_login(doc1_user1.owner)

        response = client.post(
            reverse(
                "document-edit-web",
                kwargs={
                    "pk": doc1_user1.pk,
                },
            ),
            {
                "name": "T1 Updated",
                "document_type": document_type2_user1.pk,
                "file": api_upload_file2
            },
        )

        assert response.status_code == 302

    def test_user_cannot_update_other_users_document(
            self,
            client,
            user2,
            doc1_user1,
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "document-edit-web",
                kwargs={"pk": doc1_user1.pk},
            ),
            {
                "name": "Cant Update",
            },
        )

        assert response.status_code == 403

        doc1_user1.refresh_from_db()

        assert doc1_user1.name != "Cant Update"


class TestDocumentDeleteView:

    def test_get_returns_confirmation(
        self,
        client,
        doc1_user1
    ):
        client.force_login(doc1_user1.owner)

        response = client.get(
            reverse(
                "document-delete-web",
                kwargs={
                    "pk": doc1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_post_deletes_document(
        self,
        client,
        doc1_user1
    ):
        client.force_login(doc1_user1.owner)

        response = client.post(
            reverse(
                "document-delete-web",
                kwargs={
                    "pk": doc1_user1.pk,
                },
            )
        )

        assert response.status_code == 302

        from apps.documents.models import Document

        assert not Document.objects.filter(
            pk=doc1_user1.pk
        ).exists()

    def test_user_cannot_delete_other_users_document(
            self,
            client,
            user2,
            doc1_user1,
    ):
        client.force_login(user2)

        response = client.post(

            reverse(
                "document-delete-web",
                kwargs={"pk": doc1_user1.pk},
            )
        )

        assert response.status_code == 403

        from apps.documents.models import Document

        assert Document.objects.filter(
            pk=doc1_user1.pk
        ).exists()
