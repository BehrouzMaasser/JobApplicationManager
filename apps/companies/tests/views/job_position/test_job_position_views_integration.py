import pytest

from django.urls import reverse

from apps.companies.views import position_list_url

pytestmark = pytest.mark.django_db


class TestJobPositionListView:

    def test_redirects_anonymous_user(self, client):
        response = client.get(reverse("job-position-list-web"))

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access(
            self, client, co1_ws1_user1, job_position1_user1
    ):
        client.force_login(co1_ws1_user1.workspace.owner)

        response = client.get(
            position_list_url(company_id=co1_ws1_user1.pk)
        )

        assert response.status_code == 200
        assert job_position1_user1 in response.context["job_positions"]

    def test_authenticated_user_get_list(self, client, job_position1_user1):
        client.force_login(job_position1_user1.company.workspace.owner)

        response = client.get(
            position_list_url(company_id=job_position1_user1.company.pk)
        )

        assert response.status_code == 200
        assert job_position1_user1 in response.context["job_positions"]

    def test_list_only_returns_users_job_positions(
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

    def test_valid_post_creates_job_position(
        self,
        client,
        co1_ws1_user1,
        job_pos_user1_views_valid_data
    ):
        client.force_login(co1_ws1_user1.workspace.owner)

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

        print(response.context)

        assert response.status_code == 302

    def test_create_job_position_invalid_company_id(
            self,
            client,
            user1,
            workspace1_user1,
            job_pos_user1_views_valid_data
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "job-position-create-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                    "company_id": "9999999",
                },
            ),
            job_pos_user1_views_valid_data,
        )

        assert response.status_code == 404

    def test_create_job_position_invalid_workspace_id(
            self,
            client,
            user1,
            co1_ws1_user1,
            job_pos_user1_views_valid_data
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

    def test_user_cannot_view_other_users_job_position(
            self,
            client,
            user2,
            job_position1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse(
                "job-position-detail-web",
                kwargs={"pk": job_position1_user1.pk},
            )
        )

        assert response.status_code == 403


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

    def test_valid_post_updates_job_position(
        self,
        client,
        job_position1_user1,
        job_pos_user1_views_updated_valid_data
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

        assert (job_position1_user1.title ==
                job_pos_user1_views_updated_valid_data.get("title"))

        assert (job_position1_user1.description ==
                job_pos_user1_views_updated_valid_data.get("description"))

        assert (list(e.pk for e in job_position1_user1.employment_types.all()) ==
                list(job_pos_user1_views_updated_valid_data.get("employment_types")))

        assert (list(j.pk for j in job_position1_user1.job_sites.all()) ==
                list(job_pos_user1_views_updated_valid_data.get("job_sites")))

        assert (list(t.pk for t in job_position1_user1.tasks.all()) ==
                list(job_pos_user1_views_updated_valid_data.get("tasks")))

        assert (list(r.pk for r in job_position1_user1.requirements.all()) ==
                list(job_pos_user1_views_updated_valid_data.get("requirements")))

    def test_user_cannot_update_other_users_job_position(
            self,
            client,
            user2,
            job_position1_user1,
            job_pos_user1_views_updated_valid_data
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "job-position-edit-web",
                kwargs={"pk": job_position1_user1.pk},
            ),
            job_pos_user1_views_updated_valid_data,
        )

        assert response.status_code == 403

        job_position1_user1.refresh_from_db()

        assert job_position1_user1.title != "Cant Update"
        assert job_position1_user1.description != "Cant Update"


class TestJobPositionDeleteView:

    def test_get_returns_confirmation(
        self,
        client,
        job_position1_user1
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

    def test_post_deletes_job_position(
        self,
        client,
        job_position1_user1
    ):
        client.force_login(job_position1_user1.company.workspace.owner)

        response = client.post(
            reverse(
                "job-position-delete-web",
                kwargs={
                    "pk": job_position1_user1.pk,
                },
            )
        )

        assert response.status_code == 302

        from apps.companies.models import JobPosition

        assert not JobPosition.objects.filter(
            pk=job_position1_user1.pk
        ).exists()

    def test_user_cannot_delete_other_users_job_position(
            self,
            client,
            user2,
            job_position1_user1,
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "job-position-delete-web",
                kwargs={"pk": job_position1_user1.pk},
            )
        )

        assert response.status_code == 403

        from apps.companies.models import JobPosition

        assert JobPosition.objects.filter(pk=job_position1_user1.pk).exists()
