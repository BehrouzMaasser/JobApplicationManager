import pytest

from django.urls import reverse

from apps.companies.models import JobBenefit
pytestmark = pytest.mark.django_db


class TestJobBenefitListView:

    def test_anonymous_user_is_redirected_to_login(self, client):

        response = client.get(
            reverse("job-benefit-list-web")
        )

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access_view(
        self,
        client,
        user1,
        job_benefit1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse("job-benefit-list-web")
        )

        assert response.status_code == 200
        assert "job_benefits" in response.context

        template_names = [t.name for t in response.templates if t.name]
        assert "accounts/job_benefit/list.html" in template_names

    def test_user_only_sees_owned_job_benefits(
        self,
        client,
        user2,
        job_benefit1_user1,
    ):

        client.force_login(user2)

        response = client.get(
            reverse("job-benefit-list-web")
        )

        assert response.status_code == 200

        assert job_benefit1_user1 not in response.context["job_benefits"]


class TestJobBenefitCreateView:

    def test_anonymous_user_is_redirected(
        self,
        client,
    ):

        response = client.get(
            reverse("job-benefit-create-web")
        )

        assert response.status_code == 302

    def test_authenticated_user_can_open_create_page(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse("job-benefit-create-web")
        )

        assert response.status_code == 200

        template_names = [t.name for t in response.templates if t.name]
        assert "create_page.html" in template_names

    def test_valid_submission_creates_job_benefit_and_redirects(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse("job-benefit-create-web"),
            {
                "name": "New Benefit",
                "description": "Some Description",
            },
        )

        assert response.status_code == 302

        assert response.url == reverse(
            "job-benefit-list-web"
        )

        assert JobBenefit.objects.filter(
            user=user1,
            name="New Benefit",
        ).exists()

    def test_invalid_submission_renders_form_errors(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse("job-benefit-create-web"),
            {
                "name": "",
            },
        )

        assert response.status_code == 200

        assert response.context["form"].errors

        template_names = [t.name for t in response.templates if t.name]
        assert "create_page.html" in template_names


class TestJobBenefitDetailView:

    def test_anonymous_user_is_redirected(
        self,
        client,
        job_benefit1_user1,
    ):

        response = client.get(
            reverse(
                "job-benefit-detail-web",
                kwargs={
                    "pk": job_benefit1_user1.id,
                },
            )
        )

        assert response.status_code == 302

    def test_owner_can_view_job_benefit(
        self,
        client,
        user1,
        job_benefit1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse(
                "job-benefit-detail-web",
                kwargs={
                    "pk": job_benefit1_user1.id,
                },
            )
        )

        assert response.status_code == 200

        assert response.context["job_benefit"] == job_benefit1_user1

        template_names = [t.name for t in response.templates if t.name]
        assert "accounts/job_benefit/detail.html" in template_names

    def test_user_cannot_view_foreign_job_benefit(
        self,
        client,
        user2,
        job_benefit1_user1,
    ):

        client.force_login(user2)

        response = client.get(
            reverse(
                "job-benefit-detail-web",
                kwargs={
                    "pk": job_benefit1_user1.id,
                },
            )
        )

        assert response.status_code == 404


class TestJobBenefitUpdateView:

    def test_owner_can_open_update_page(
        self,
        client,
        user1,
        job_benefit1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse(
                "job-benefit-edit-web",
                kwargs={
                    "pk": job_benefit1_user1.id,
                },
            )
        )

        assert response.status_code == 200

        template_names = [t.name for t in response.templates if t.name]
        assert "edit_page.html" in template_names

    def test_valid_submission_updates_job_benefit_and_redirects(
        self,
        client,
        user1,
        job_benefit1_user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse(
                "job-benefit-edit-web",
                kwargs={
                    "pk": job_benefit1_user1.id,
                },
            ),
            {
                "name": "Updated Benefit",
                "description": "Updated",
            },
        )

        assert response.status_code == 302

        job_benefit1_user1.refresh_from_db()

        assert job_benefit1_user1.name == "Updated Benefit"

    def test_invalid_submission_renders_form_errors(
        self,
        client,
        user1,
        job_benefit1_user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse(
                "job-benefit-edit-web",
                kwargs={
                    "pk": job_benefit1_user1.id,
                },
            ),
            {
                "name": "",
            },
        )

        assert response.status_code == 200

        assert response.context["form"].errors

    def test_user_cannot_update_foreign_job_benefit(
        self,
        client,
        user2,
        job_benefit1_user1,
    ):

        client.force_login(user2)

        response = client.post(
            reverse(
                "job-benefit-edit-web",
                kwargs={
                    "pk": job_benefit1_user1.id,
                },
            ),
            {
                "name": "Unauthorized Update",
            },
        )

        assert response.status_code == 404

        job_benefit1_user1.refresh_from_db()

        assert job_benefit1_user1.name != "Unauthorized Update"


class TestJobBenefitDeleteView:

    def test_owner_can_open_delete_confirmation(
        self,
        client,
        user1,
        job_benefit1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse(
                "job-benefit-delete-web",
                kwargs={
                    "pk": job_benefit1_user1.id,
                },
            )
        )

        assert response.status_code == 200

        template_names = [t.name for t in response.templates if t.name]
        assert "delete_confirm.html" in template_names

    def test_valid_submission_deletes_job_benefit_and_redirects(
        self,
        client,
        user1,
        job_benefit1_user1,
    ):

        client.force_login(user1)

        pk = job_benefit1_user1.id

        response = client.post(
            reverse(
                "job-benefit-delete-web",
                kwargs={
                    "pk": pk,
                },
            )
        )

        assert response.status_code == 302

        assert not JobBenefit.objects.filter(
            id=pk
        ).exists()

    def test_user_cannot_delete_foreign_job_benefit(
        self,
        client,
        user2,
        job_benefit1_user1,
    ):

        client.force_login(user2)

        pk = job_benefit1_user1.id

        response = client.post(
            reverse(
                "job-benefit-delete-web",
                kwargs={
                    "pk": pk,
                },
            )
        )

        assert response.status_code == 404

        assert JobBenefit.objects.filter(
            id=pk
        ).exists()
