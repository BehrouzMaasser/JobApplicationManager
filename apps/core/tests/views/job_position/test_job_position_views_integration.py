import pytest

from django.urls import reverse

from apps.companies.models import JobPosition
from apps.companies.views import position_list_url

pytestmark = pytest.mark.django_db


class TestJobPositionListView:

    def test_redirects_anonymous_user(self, client):
        response = client.get(reverse("job-position-list-web"))

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access(
        self,
        client,
        co1_ws1_user1,
        job_position1_user1,
    ):
        client.force_login(co1_ws1_user1.workspace.owner)

        response = client.get(
            position_list_url(company_id=co1_ws1_user1.pk)
        )

        assert response.status_code == 200
        assert "job_positions" in response.context
        assert job_position1_user1 in response.context["job_positions"]

    def test_list_returns_only_users_job_positions(
        self,
        client,
        user2,
        job_position1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            position_list_url(company_id=job_position1_user1.company.pk)
        )

        assert response.status_code == 200
        assert job_position1_user1 not in response.context["job_positions"]


class TestJobPositionCreateView:

    def test_redirects_anonymous_user(
        self,
        client,
        co1_ws1_user1,
    ):
        response = client.get(
            reverse(
                "job-position-create-web",
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
                "job-position-create-web",
                kwargs={
                    "workspace_id": co1_ws1_user1.workspace.workspace_id,
                    "company_id": co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_creates_job_position_and_redirects(
        self,
        client,
        co1_ws1_user1,
        job_pos_user1_views_valid_data,
    ):
        client.force_login(co1_ws1_user1.workspace.owner)

        before = JobPosition.objects.count()

        response = client.post(
            reverse(
                "job-position-create-web",
                kwargs={
                    "workspace_id": co1_ws1_user1.workspace.workspace_id,
                    "company_id": co1_ws1_user1.pk,
                },
            ),
            job_pos_user1_views_valid_data,
        )

        assert response.status_code == 302
        assert JobPosition.objects.count() == before + 1

    def test_create_with_unknown_company_returns_404(
        self,
        client,
        user1,
        workspace1_user1,
        job_pos_user1_views_valid_data,
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "job-position-create-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                    "company_id": 999999,
                },
            ),
            job_pos_user1_views_valid_data,
        )

        assert response.status_code == 404

    def test_create_with_foreign_workspace_returns_404(
        self,
        client,
        user1,
        co1_ws1_user1,
        job_pos_user1_views_valid_data,
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "job-position-create-web",
                kwargs={
                    "workspace_id": "00000000-0000-0000-0000-000000000000",
                    "company_id": co1_ws1_user1.pk,
                },
            ),
            job_pos_user1_views_valid_data,
        )

        assert response.status_code == 404


class TestJobPositionDetailView:

    def test_redirects_anonymous_user(
        self,
        client,
        job_position1_user1,
    ):
        response = client.get(
            reverse(
                "job-position-detail-web",
                kwargs={
                    "pk": job_position1_user1.pk,
                },
            )
        )

        assert response.status_code == 302
        assert response.context is None

    def test_authenticated_user_can_access(
        self,
        client,
        job_position1_user1,
    ):
        client.force_login(job_position1_user1.company.workspace.owner)

        response = client.get(
            reverse(
                "job-position-detail-web",
                kwargs={
                    "pk": job_position1_user1.pk,
                },
            )
        )

        assert response.status_code == 200
        assert response.context["job_position"] == job_position1_user1

    def test_foreign_user_receives_404(
        self,
        client,
        user2,
        job_position1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse(
                "job-position-detail-web",
                kwargs={
                    "pk": job_position1_user1.pk,
                },
            )
        )

        assert response.status_code == 404


class TestJobPositionUpdateView:

    def test_get_returns_page(
        self,
        client,
        job_position1_user1,
    ):
        client.force_login(job_position1_user1.company.workspace.owner)

        response = client.get(
            reverse(
                "job-position-edit-web",
                kwargs={
                    "pk": job_position1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_updates_job_position_and_redirects(
        self,
        client,
        job_position1_user1,
        job_pos_user1_views_updated_valid_data,
    ):
        client.force_login(job_position1_user1.company.workspace.owner)

        response = client.post(
            reverse(
                "job-position-edit-web",
                kwargs={
                    "pk": job_position1_user1.pk,
                },
            ),
            job_pos_user1_views_updated_valid_data,
        )

        assert response.status_code == 302

        job_position1_user1.refresh_from_db()

        assert (
            job_position1_user1.title
            == job_pos_user1_views_updated_valid_data["title"]
        )

        assert (
            job_position1_user1.description
            == job_pos_user1_views_updated_valid_data["description"]
        )

        assert sorted(
            job_position1_user1.employment_types.values_list("pk", flat=True)
        ) == sorted(job_pos_user1_views_updated_valid_data["employment_types"])

        assert sorted(
            job_position1_user1.job_sites.values_list("pk", flat=True)
        ) == sorted(job_pos_user1_views_updated_valid_data["job_sites"])

        assert sorted(
            job_position1_user1.tasks.values_list("pk", flat=True)
        ) == sorted(job_pos_user1_views_updated_valid_data["tasks"])

        assert sorted(
            job_position1_user1.requirements.values_list("pk", flat=True)
        ) == sorted(job_pos_user1_views_updated_valid_data["requirements"])

    def test_foreign_user_receives_404_and_job_position_is_not_updated(
        self,
        client,
        user2,
        job_position1_user1,
        job_pos_user1_views_updated_valid_data,
    ):
        client.force_login(user2)

        original_title = job_position1_user1.title
        original_description = job_position1_user1.description

        response = client.post(
            reverse(
                "job-position-edit-web",
                kwargs={
                    "pk": job_position1_user1.pk,
                },
            ),
            job_pos_user1_views_updated_valid_data,
        )

        assert response.status_code == 404

        job_position1_user1.refresh_from_db()

        assert job_position1_user1.title == original_title
        assert job_position1_user1.description == original_description


class TestJobPositionDeleteView:

    def test_get_returns_confirmation(
        self,
        client,
        job_position1_user1,
    ):
        client.force_login(job_position1_user1.company.workspace.owner)

        response = client.get(
            reverse(
                "job-position-delete-web",
                kwargs={
                    "pk": job_position1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_post_deletes_job_position_and_redirects(
        self,
        client,
        job_position1_user1,
    ):
        client.force_login(job_position1_user1.company.workspace.owner)

        job_position_id = job_position1_user1.pk

        response = client.post(
            reverse(
                "job-position-delete-web",
                kwargs={
                    "pk": job_position_id,
                },
            )
        )

        assert response.status_code == 302
        assert not JobPosition.objects.filter(pk=job_position_id).exists()

    def test_foreign_user_receives_404_and_job_position_is_not_deleted(
        self,
        client,
        user2,
        job_position1_user1,
    ):
        client.force_login(user2)

        job_position_id = job_position1_user1.pk

        response = client.post(
            reverse(
                "job-position-delete-web",
                kwargs={
                    "pk": job_position_id,
                },
            )
        )

        assert response.status_code == 404
        assert JobPosition.objects.filter(pk=job_position_id).exists()
