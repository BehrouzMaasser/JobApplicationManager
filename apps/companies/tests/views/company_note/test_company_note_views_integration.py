import pytest

from django.urls import reverse

from apps.companies.views import company_note_list_url

pytestmark = pytest.mark.django_db


class TestCompanyNoteListView:

    def test_redirects_anonymous_user(self, client):
        response = client.get(reverse("company-note-list-web"))

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access(self, client, co1_ws1_user1):
        client.force_login(co1_ws1_user1.workspace.owner)

        response = client.get(
            company_note_list_url(company_id=co1_ws1_user1.pk)
        )

        assert response.status_code == 200
        assert "notes" in response.context

    def test_authenticated_user_get_list(self, client, co_note1_co1_ws1_user1):
        client.force_login(co_note1_co1_ws1_user1.company.workspace.owner)

        response = client.get(
            company_note_list_url(company_id=co_note1_co1_ws1_user1.company.pk)
        )

        assert response.status_code == 200
        assert co_note1_co1_ws1_user1 in response.context["notes"]

    def test_list_only_returns_users_company_notes(
            self,
            client,
            user2,
            co_note1_co1_ws1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            company_note_list_url(company_id=co_note1_co1_ws1_user1.company.pk)
        )

        assert response.status_code == 200
        assert co_note1_co1_ws1_user1 not in response.context["notes"]


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
                    "workspace_id": co1_ws1_user1.workspace.workspace_id,
                    "company_id": co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 302

    def test_get_returns_page(
        self,
        client,
        co1_ws1_user1,
    ):
        client.force_login(co1_ws1_user1.workspace.owner)

        response = client.get(
            reverse(
                "company-note-create-web",
                kwargs={
                    "workspace_id": co1_ws1_user1.workspace.workspace_id,
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
        client.force_login(co1_ws1_user1.workspace.owner)

        response = client.post(
            reverse(
                "company-note-create-web",
                kwargs={
                    "workspace_id": co1_ws1_user1.workspace.workspace_id,
                    "company_id": co1_ws1_user1.pk,
                },
            ),
            {
                "title": "T1",
                "content": "content",
            },
        )

        assert response.status_code == 302

    def test_create_company_note_invalid_company_id(
            self,
            client,
            user1,
            workspace1_user1
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "company-note-create-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                    "company_id": "9999999",
                },
            ),
            {
                "title": "T1",
                "content": "content",
            },
        )

        assert response.status_code == 404

    def test_create_company_email_invalid_workspace_id(
            self,
            client,
            user1,
            co1_ws1_user1
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "company-note-create-web",
                kwargs={
                    "workspace_id": "00000000-0000-0000-0000-000000000000",
                    "company_id": co1_ws1_user1.pk,
                },
            ),
            {
                "title": "T1",
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

    def test_authenticated_user_can_access(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(co_note1_co1_ws1_user1.company.workspace.owner)

        response = client.get(
            reverse(
                "company-note-detail-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

        assert response.context["note"] == co_note1_co1_ws1_user1

    def test_user_cannot_view_other_users_company_note(
            self,
            client,
            user2,
            co_note1_co1_ws1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse(
                "company-note-detail-web",
                kwargs={"pk": co_note1_co1_ws1_user1.pk},
            )
        )

        assert response.status_code == 403


class TestCompanyNoteUpdateView:

    def test_get_returns_page(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(co_note1_co1_ws1_user1.company.workspace.owner)

        response = client.get(
            reverse(
                "company-note-edit-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_updates_company_note(
        self,
        client,
        co_note1_co1_ws1_user1,
    ):
        client.force_login(co_note1_co1_ws1_user1.company.workspace.owner)

        response = client.post(
            reverse(
                "company-note-edit-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            ),
            {
                "title": "T1 Updated",
                "content": "Updated content",
            },
        )

        assert response.status_code == 302

        co_note1_co1_ws1_user1.refresh_from_db()

        assert co_note1_co1_ws1_user1.title == "T1 Updated"
        assert co_note1_co1_ws1_user1.content == "Updated content"

    def test_user_cannot_update_other_users_company_note(
            self,
            client,
            user2,
            co_note1_co1_ws1_user1,
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "company-note-edit-web",
                kwargs={"pk": co_note1_co1_ws1_user1.pk},
            ),
            {
                "title": "Cant Update",
                "content": "Cant Update",
            },
        )

        assert response.status_code == 403

        co_note1_co1_ws1_user1.refresh_from_db()

        assert co_note1_co1_ws1_user1.title != "Cant Update"
        assert co_note1_co1_ws1_user1.content != "Cant Update"


class TestCompanyNoteDeleteView:

    def test_get_returns_confirmation(
        self,
        client,
        co_note1_co1_ws1_user1
    ):
        client.force_login(co_note1_co1_ws1_user1.company.workspace.owner)

        response = client.get(
            reverse(
                "company-note-delete-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_post_deletes_company_note(
        self,
        client,
        co_note1_co1_ws1_user1
    ):
        client.force_login(co_note1_co1_ws1_user1.company.workspace.owner)

        response = client.post(
            reverse(
                "company-note-delete-web",
                kwargs={
                    "pk": co_note1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 302

        from apps.companies.models import CompanyNote

        assert not CompanyNote.objects.filter(
            pk=co_note1_co1_ws1_user1.pk
        ).exists()

    def test_user_cannot_delete_other_users_company_note(
            self,
            client,
            user2,
            co_note1_co1_ws1_user1,
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "company-note-delete-web",
                kwargs={"pk": co_note1_co1_ws1_user1.pk},
            )
        )

        assert response.status_code == 403

        from apps.companies.models import CompanyNote

        assert CompanyNote.objects.filter(pk=co_note1_co1_ws1_user1.pk).exists()
