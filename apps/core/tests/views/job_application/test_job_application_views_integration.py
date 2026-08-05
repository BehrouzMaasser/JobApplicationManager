import pytest

from django.urls import reverse
from django.utils import timezone

from apps.applications.views import application_list_url

pytestmark = pytest.mark.django_db


class TestJobApplicationListView:

    def test_redirects_anonymous_user(self, client):
        response = client.get(
            reverse("job-application-list-web")
        )

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access(
        self,
        client,
        job_application1,
    ):
        client.force_login(
            job_application1.workspace.owner
        )

        response = client.get(
            application_list_url(
                workspace_id=job_application1.workspace.workspace_id,
                company_id=job_application1.job_position.company.pk,
                job_position_id=job_application1.job_position.pk,
            )
        )

        assert response.status_code == 200
        assert (
            job_application1
            in response.context["job_applications"]
        )

    def test_list_only_returns_users_job_applications(
        self,
        client,
        user2,
        job_application1,
    ):
        client.force_login(user2)

        response = client.get(
            application_list_url(
                workspace_id=job_application1.workspace.workspace_id,
                company_id=job_application1.job_position.company.pk,
                job_position_id=job_application1.job_position.pk,
            )
        )

        assert response.status_code == 200

        assert (
            job_application1
            not in response.context["job_applications"]
        )


class TestJobApplicationCreateView:

    def test_redirects_anonymous_user(
        self,
        client,
        job_application1,
    ):
        response = client.get(
            reverse(
                "job-application-create-web",
                kwargs={
                    "workspace_id": (
                        job_application1.workspace.workspace_id
                    ),
                    "company_id": (
                        job_application1.job_position.company.pk
                    ),
                    "job_position_id": (
                        job_application1.job_position.pk
                    ),
                },
            )
        )

        assert response.status_code == 302

    def test_get_returns_page(
        self,
        client,
        job_application1,
    ):
        client.force_login(
            job_application1.workspace.owner
        )

        response = client.get(
            reverse(
                "job-application-create-web",
                kwargs={
                    "workspace_id": (
                        job_application1.workspace.workspace_id
                    ),
                    "company_id": (
                        job_application1.job_position.company.pk
                    ),
                    "job_position_id": (
                        job_application1.job_position.pk
                    ),
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_creates_job_application(
        self,
        client,
        job_application1_valid_view_data,
        job_position1_co1_ws1_user1
    ):
        client.force_login(
            job_position1_co1_ws1_user1.company.workspace.owner
        )

        response = client.post(
            reverse(
                "job-application-create-web",
                kwargs={
                    "workspace_id": (
                        job_position1_co1_ws1_user1.company.workspace.workspace_id
                    ),
                    "company_id": (
                        job_position1_co1_ws1_user1.company.pk
                    ),
                    "job_position_id": (
                        job_position1_co1_ws1_user1.pk
                    ),
                },
            ),
            job_application1_valid_view_data,
        )

        assert response.status_code == 302

    def test_create_invalid_company_id_returns_404(
        self,
        client,
        user1,
        job_position1_co1_ws1_user1,
        status1
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "job-application-create-web",
                kwargs={
                    "workspace_id": (
                        job_position1_co1_ws1_user1.company.workspace.workspace_id
                    ),
                    "company_id": "9999999",
                    "job_position_id": (
                        job_position1_co1_ws1_user1.pk
                    ),
                },
            ),
            {
                "status": status1.pk,
                "date_applied": timezone.now(),
            },
        )

        assert response.status_code == 404

    def test_create_invalid_workspace_id_returns_404(
        self,
        client,
        user1,
        job_position1_co1_ws1_user1,
        status1
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "job-application-create-web",
                kwargs={
                    "workspace_id": "00000000-0000-0000-0000-000000000000",
                    "company_id": job_position1_co1_ws1_user1.company.pk,
                    "job_position_id": job_position1_co1_ws1_user1.pk,
                },
            ),
            {
                "status": status1.pk,
                "date_applied": timezone.now(),
            },
        )

        assert response.status_code == 404


class TestJobApplicationDetailView:

    def test_redirects_anonymous_user(
        self,
        client,
        job_application1,
    ):
        response = client.get(
            reverse(
                "job-application-detail-web",
                kwargs={
                    "pk": job_application1.pk,
                },
            )
        )

        assert response.status_code == 302
        assert response.context is None

    def test_authenticated_user_can_access(
        self,
        client,
        job_application1,
    ):
        client.force_login(
            job_application1.workspace.owner
        )

        response = client.get(
            reverse(
                "job-application-detail-web",
                kwargs={
                    "pk": job_application1.pk,
                },
            )
        )

        assert response.status_code == 200

        assert (
            response.context["job_application"]
            == job_application1
        )

    def test_user_cannot_view_other_users_application(
        self,
        client,
        user2,
        job_application1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse(
                "job-application-detail-web",
                kwargs={
                    "pk": job_application1.pk,
                },
            )
        )

        assert response.status_code == 404


class TestJobApplicationUpdateView:

    def test_get_returns_page(
        self,
        client,
        job_application1,
    ):
        client.force_login(
            job_application1.workspace.owner
        )

        response = client.get(
            reverse(
                "job-application-edit-web",
                kwargs={
                    "pk": job_application1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_updates_application(
        self,
        client,
        job_application1,
        job_application1_valid_view_data_updated
    ):
        client.force_login(
            job_application1.workspace.owner
        )

        response = client.post(
            reverse(
                "job-application-edit-web",
                kwargs={
                    "pk": job_application1.pk,
                },
            ),
            job_application1_valid_view_data_updated,
        )

        assert response.status_code == 302

        job_application1.refresh_from_db()

        assert (
            job_application1.status.id
            == job_application1_valid_view_data_updated["status"]
        )

    def test_user_cannot_update_other_users_application(
        self,
        client,
        user2,
        job_application1,
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "job-application-edit-web",
                kwargs={
                    "pk": job_application1.pk,
                },
            ),
            {
                "status": "rejected",
            },
        )

        assert response.status_code == 404


class TestJobApplicationDeleteView:

    def test_get_returns_confirmation(
        self,
        client,
        job_application1,
    ):
        client.force_login(
            job_application1.workspace.owner
        )

        response = client.get(
            reverse(
                "job-application-delete-web",
                kwargs={
                    "pk": job_application1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_post_deletes_application(
        self,
        client,
        job_application1,
    ):
        client.force_login(
            job_application1.workspace.owner
        )

        application_id = job_application1.pk

        response = client.post(
            reverse(
                "job-application-delete-web",
                kwargs={
                    "pk": application_id,
                },
            )
        )

        assert response.status_code == 302

        from apps.applications.models import JobApplication

        assert not JobApplication.objects.filter(
            pk=application_id
        ).exists()

    def test_user_cannot_delete_other_users_application(
        self,
        client,
        user2,
        job_application1,
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "job-application-delete-web",
                kwargs={
                    "pk": job_application1.pk,
                },
            )
        )

        assert response.status_code == 404

        from apps.applications.models import JobApplication

        assert JobApplication.objects.filter(
            pk=job_application1.pk
        ).exists()
