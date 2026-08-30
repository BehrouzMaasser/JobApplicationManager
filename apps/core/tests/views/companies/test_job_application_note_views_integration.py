import pytest

from django.urls import reverse

from apps.applications.models import JobApplicationNote

pytestmark = pytest.mark.django_db


class TestJobApplicationNoteListView:

    def test_redirects_anonymous_user(self, client):
        response = client.get(reverse("job-application-note-list-web"))
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access_and_see_notes(
        self, client, job_application1, app_note1
    ):
        client.force_login(job_application1.workspace.owner)

        url = (
            f"{reverse('job-application-note-list-web')}"
            f"?workspace_id={job_application1.workspace.workspace_id}"
            f"&company_id={job_application1.job_position.company.pk}"
            f"&job_position_id={job_application1.job_position.pk}"
            f"&job_application_id={job_application1.pk}"
        )

        response = client.get(url)

        assert response.status_code == 200
        assert app_note1 in response.context["application_notes"]

    def test_list_only_returns_users_notes(
            self, client, user2, job_application1, app_note1
    ):
        client.force_login(user2)

        url = (
            f"{reverse('job-application-note-list-web')}"
            f"?workspace_id={job_application1.workspace.workspace_id}"
            f"&company_id={job_application1.job_position.company.pk}"
            f"&job_position_id={job_application1.job_position.pk}"
            f"&job_application_id={job_application1.pk}"
        )

        response = client.get(url)

        assert response.status_code == 200
        assert app_note1 not in response.context["application_notes"]


class TestJobApplicationNoteCreateView:

    def test_redirects_anonymous_user(self, client, job_application1):
        response = client.get(
            reverse(
                "job-application-note-create-web",
                kwargs={"job_application_id": job_application1.pk}
            )
        )
        assert response.status_code == 302

    def test_get_returns_page_for_owner(self, client, job_application1):
        client.force_login(job_application1.workspace.owner)

        response = client.get(
            reverse(
                "job-application-note-create-web",
                kwargs={"job_application_id": job_application1.pk}
            )
        )

        assert response.status_code == 200

    def test_valid_post_creates_note(
            self, client, job_application1, app_note1_valid_data
    ):
        client.force_login(job_application1.workspace.owner)

        response = client.post(
            reverse(
                "job-application-note-create-web",
                kwargs={"job_application_id": job_application1.pk}
            ),
            app_note1_valid_data,
        )

        assert response.status_code == 302

        assert JobApplicationNote.objects.filter(
            job_application=job_application1, title=app_note1_valid_data["title"]
        ).exists()

    def test_create_invalid_job_application_returns_404(
            self, client, user1, app_note1_valid_data
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "job-application-note-create-web",
                kwargs={"job_application_id": "9999999"}
            ),
            app_note1_valid_data,
        )

        assert response.status_code == 404


class TestJobApplicationNoteDetailView:

    def test_redirects_anonymous_user(self, client, app_note1):
        response = client.get(
            reverse(
                "job-application-note-detail-web",
                kwargs={"pk": app_note1.pk}
            )
        )
        assert response.status_code == 302
        assert response.context is None

    def test_authenticated_user_can_access(self, client, app_note1):
        client.force_login(app_note1.job_application.workspace.owner)

        response = client.get(
            reverse(
                "job-application-note-detail-web",
                kwargs={"pk": app_note1.pk}
            )
        )

        assert response.status_code == 200
        assert response.context["application_note"] == app_note1

    def test_user_cannot_view_other_users_note(self, client, user2, app_note1):
        client.force_login(user2)

        response = client.get(
            reverse(
                "job-application-note-detail-web",
                kwargs={"pk": app_note1.pk}
            )
        )

        assert response.status_code == 404


class TestJobApplicationNoteUpdateView:

    def test_get_returns_page(self, client, app_note1):
        client.force_login(app_note1.job_application.workspace.owner)

        response = client.get(
            reverse(
                "job-application-note-edit-web",
                kwargs={"pk": app_note1.pk}
            )
        )

        assert response.status_code == 200

    def test_valid_post_updates_note(
            self, client, app_note1, app_note1_valid_data_updated
    ):
        client.force_login(app_note1.job_application.workspace.owner)

        response = client.post(
            reverse(
                "job-application-note-edit-web",
                kwargs={"pk": app_note1.pk}
            ),
            app_note1_valid_data_updated,
        )

        assert response.status_code == 302

        app_note1.refresh_from_db()
        assert app_note1.title == app_note1_valid_data_updated["title"]
        assert app_note1.content == app_note1_valid_data_updated["content"]

    def test_user_cannot_update_other_users_note(
            self, client, user2, app_note1, app_note1_valid_data_updated
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "job-application-note-edit-web",
                kwargs={"pk": app_note1.pk}
            ),
            app_note1_valid_data_updated,
        )

        assert response.status_code == 404


class TestJobApplicationNoteDeleteView:

    def test_get_returns_confirmation(self, client, app_note1):
        client.force_login(app_note1.job_application.workspace.owner)

        response = client.get(
            reverse(
                "job-application-note-delete-web", kwargs={"pk": app_note1.pk}
            )
        )

        assert response.status_code == 200

    def test_post_deletes_note(self, client, app_note1):
        client.force_login(app_note1.job_application.workspace.owner)

        note_id = app_note1.pk

        response = client.post(
            reverse(
                "job-application-note-delete-web", kwargs={"pk": note_id}
            )
        )

        assert response.status_code == 302

        assert not JobApplicationNote.objects.filter(pk=note_id).exists()

    def test_user_cannot_delete_other_users_note(self, client, user2, app_note1):
        client.force_login(user2)

        response = client.post(
            reverse(
                "job-application-note-delete-web",
                kwargs={"pk": app_note1.pk}
            )
        )

        assert response.status_code == 404

        assert JobApplicationNote.objects.filter(pk=app_note1.pk).exists()
