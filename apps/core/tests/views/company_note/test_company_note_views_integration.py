import pytest

from django.urls import reverse

from apps.companies.models import CompanyNote
from apps.companies.views import company_note_list_url


pytestmark = pytest.mark.django_db


class TestCompanyNoteListView:

    def test_redirects_anonymous_user(self, client):
        response = client.get(
            reverse("company-note-list-web")
        )

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access(
        self,
        client,
        co1_ws1_user1,
    ):
        client.force_login(
            co1_ws1_user1.workspace.owner
        )

        response = client.get(
            company_note_list_url(
                company_id=co1_ws1_user1.pk
            )
        )

        assert response.status_code == 200
        assert "notes" in response.context

    def test_list_contains_company_notes(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(
            co_note1_co1_ws1_user1.company.workspace.owner
        )

        response = client.get(
            company_note_list_url(
                company_id=co_note1_co1_ws1_user1.company.pk
            )
        )

        assert response.status_code == 200

        assert (
            co_note1_co1_ws1_user1
            in response.context["notes"]
        )

    def test_list_does_not_return_other_users_notes(
        self,
        client,
        user2,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            company_note_list_url(
                company_id=co_note1_co1_ws1_user1.company.pk
            )
        )

        assert response.status_code == 200

        assert (
            co_note1_co1_ws1_user1
            not in response.context["notes"]
        )


class TestCompanyNoteCreateView:

    def test_redirects_anonymous_user(
        self,
        client,
        co1_ws1_user1,
    ):
        response = client.get(
            reverse(
                "company-note-create-web",
                kwargs={
                    "workspace_id": (
                        co1_ws1_user1.workspace.workspace_id
                    ),
                    "company_id": co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 302

    def test_get_returns_create_page(
        self,
        client,
        co1_ws1_user1,
    ):
        client.force_login(
            co1_ws1_user1.workspace.owner
        )

        response = client.get(
            reverse(
                "company-note-create-web",
                kwargs={
                    "workspace_id": (
                        co1_ws1_user1.workspace.workspace_id
                    ),
                    "company_id": co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_creates_company_note(
        self,
        client,
        co1_ws1_user1,
    ):
        client.force_login(
            co1_ws1_user1.workspace.owner
        )

        response = client.post(
            reverse(
                "company-note-create-web",
                kwargs={
                    "workspace_id": (
                        co1_ws1_user1.workspace.workspace_id
                    ),
                    "company_id": co1_ws1_user1.pk,
                },
            ),
            {
                "title": "New Note",
                "content": "New content",
            },
        )

        assert response.status_code == 302

        assert CompanyNote.objects.filter(
            company=co1_ws1_user1,
            title="New Note",
            content="New content",
        ).exists()

    def test_create_with_invalid_company_returns_404(
        self,
        client,
        user1,
        workspace1_user1,
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "company-note-create-web",
                kwargs={
                    "workspace_id": (
                        workspace1_user1.workspace_id
                    ),
                    "company_id": 9999999,
                },
            ),
            {
                "title": "New Note",
                "content": "content",
            },
        )

        assert response.status_code == 404

    def test_create_with_foreign_workspace_returns_404(
        self,
        client,
        user1,
        co1_ws1_user1,
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "company-note-create-web",
                kwargs={
                    "workspace_id": (
                        "00000000-0000-0000-0000-000000000000"
                    ),
                    "company_id": co1_ws1_user1.pk,
                },
            ),
            {
                "title": "New Note",
                "content": "content",
            },
        )

        assert response.status_code == 404


class TestCompanyNoteDetailView:

    def test_redirects_anonymous_user(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        response = client.get(
            reverse(
                "company-note-detail-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 302
        assert response.context is None

    def test_authenticated_user_can_view_note(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(
            co_note1_co1_ws1_user1.company.workspace.owner
        )

        response = client.get(
            reverse(
                "company-note-detail-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

        assert (
            response.context["note"]
            == co_note1_co1_ws1_user1
        )

    def test_user_cannot_view_other_users_note(
        self,
        client,
        user2,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse(
                "company-note-detail-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 404


class TestCompanyNoteUpdateView:

    def test_redirects_anonymous_user(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        response = client.get(
            reverse(
                "company-note-edit-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 302

    def test_get_returns_edit_page(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(
            co_note1_co1_ws1_user1.company.workspace.owner
        )

        response = client.get(
            reverse(
                "company-note-edit-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_updates_note(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(
            co_note1_co1_ws1_user1.company.workspace.owner
        )

        response = client.post(
            reverse(
                "company-note-edit-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            ),
            {
                "title": "Updated title",
                "content": "Updated content",
            },
        )

        assert response.status_code == 302

        co_note1_co1_ws1_user1.refresh_from_db()

        assert (
            co_note1_co1_ws1_user1.title
            == "Updated title"
        )

        assert (
            co_note1_co1_ws1_user1.content
            == "Updated content"
        )

    def test_user_cannot_update_other_users_note(
        self,
        client,
        user2,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "company-note-edit-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            ),
            {
                "title": "Unauthorized update",
                "content": "Unauthorized update",
            },
        )

        assert response.status_code == 404

        co_note1_co1_ws1_user1.refresh_from_db()

        assert (
            co_note1_co1_ws1_user1.title
            != "Unauthorized update"
        )

        assert (
            co_note1_co1_ws1_user1.content
            != "Unauthorized update"
        )


class TestCompanyNoteDeleteView:

    def test_redirects_anonymous_user(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        response = client.post(
            reverse(
                "company-note-delete-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 302

    def test_get_returns_confirmation_page(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(
            co_note1_co1_ws1_user1.company.workspace.owner
        )

        response = client.get(
            reverse(
                "company-note-delete-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_post_deletes_note(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(
            co_note1_co1_ws1_user1.company.workspace.owner
        )

        note_id = co_note1_co1_ws1_user1.pk

        response = client.post(
            reverse(
                "company-note-delete-web",
                kwargs={
                    "pk": note_id,
                },
            )
        )

        assert response.status_code == 302

        assert not CompanyNote.objects.filter(
            pk=note_id
        ).exists()

    def test_user_cannot_delete_other_users_note(
        self,
        client,
        user2,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(user2)

        note_id = co_note1_co1_ws1_user1.pk

        response = client.post(
            reverse(
                "company-note-delete-web",
                kwargs={
                    "pk": note_id,
                },
            )
        )

        assert response.status_code == 404

        assert CompanyNote.objects.filter(
            pk=note_id
        ).exists()
