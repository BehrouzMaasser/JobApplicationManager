import pytest

from django.urls import reverse

from apps.companies.models import JobRequirement
pytestmark = pytest.mark.django_db


class TestJobRequirementListView:

    def test_anonymous_user_is_redirected_to_login(self, client):

        response = client.get(
            reverse("job-requirement-list-web")
        )

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access_view(
        self,
        client,
        user1,
        job_requirement1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse("job-requirement-list-web")
        )

        assert response.status_code == 200
        assert "job_requirements" in response.context

        template_names = [t.name for t in response.templates if t.name]
        assert "accounts/job_requirement/list.html" in template_names

    def test_user_only_sees_owned_job_requirements(
        self,
        client,
        user2,
        job_requirement1_user1,
    ):

        client.force_login(user2)

        response = client.get(
            reverse("job-requirement-list-web")
        )

        assert response.status_code == 200

        assert job_requirement1_user1 not in response.context["job_requirements"]


class TestJobRequirementCreateView:

    def test_anonymous_user_is_redirected(
        self,
        client,
    ):

        response = client.get(
            reverse("job-requirement-create-web")
        )

        assert response.status_code == 302

    def test_authenticated_user_can_open_create_page(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse("job-requirement-create-web")
        )

        assert response.status_code == 200

        template_names = [t.name for t in response.templates if t.name]
        assert "create_page.html" in template_names

    def test_valid_submission_creates_job_requirement_and_redirects(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse("job-requirement-create-web"),
            {
                "title": "New Req",
                "description": "Some Description",
            },
        )

        assert response.status_code == 302

        assert response.url == reverse(
            "job-requirement-list-web"
        )

        assert JobRequirement.objects.filter(
            user=user1,
            title="New Req",
        ).exists()

    def test_invalid_submission_renders_form_errors(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse("job-requirement-create-web"),
            {
                "title": "",
            },
        )

        assert response.status_code == 200

        assert response.context["form"].errors

        template_names = [t.name for t in response.templates if t.name]
        assert "create_page.html" in template_names


class TestJobRequirementDetailView:

    def test_anonymous_user_is_redirected(
        self,
        client,
        job_requirement1_user1,
    ):

        response = client.get(
            reverse(
                "job-requirement-detail-web",
                kwargs={
                    "pk": job_requirement1_user1.id,
                },
            )
        )

        assert response.status_code == 302

    def test_owner_can_view_job_requirement(
        self,
        client,
        user1,
        job_requirement1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse(
                "job-requirement-detail-web",
                kwargs={
                    "pk": job_requirement1_user1.id,
                },
            )
        )

        assert response.status_code == 200

        assert response.context["job_requirement"] == job_requirement1_user1

        template_names = [t.name for t in response.templates if t.name]
        assert "accounts/job_requirement/detail.html" in template_names

    def test_user_cannot_view_foreign_job_requirement(
        self,
        client,
        user2,
        job_requirement1_user1,
    ):

        client.force_login(user2)

        response = client.get(
            reverse(
                "job-requirement-detail-web",
                kwargs={
                    "pk": job_requirement1_user1.id,
                },
            )
        )

        assert response.status_code == 404


class TestJobRequirementUpdateView:

    def test_owner_can_open_update_page(
        self,
        client,
        user1,
        job_requirement1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse(
                "job-requirement-edit-web",
                kwargs={
                    "pk": job_requirement1_user1.id,
                },
            )
        )

        assert response.status_code == 200

        template_names = [t.name for t in response.templates if t.name]
        assert "edit_page.html" in template_names

    def test_valid_submission_updates_job_requirement_and_redirects(
        self,
        client,
        user1,
        job_requirement1_user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse(
                "job-requirement-edit-web",
                kwargs={
                    "pk": job_requirement1_user1.id,
                },
            ),
            {
                "title": "Updated Req",
                "description": "Updated",
            },
        )

        assert response.status_code == 302

        job_requirement1_user1.refresh_from_db()

        assert job_requirement1_user1.title == "Updated Req"

    def test_invalid_submission_renders_form_errors(
        self,
        client,
        user1,
        job_requirement1_user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse(
                "job-requirement-edit-web",
                kwargs={
                    "pk": job_requirement1_user1.id,
                },
            ),
            {
                "title": "",
            },
        )

        assert response.status_code == 200

        assert response.context["form"].errors

    def test_user_cannot_update_foreign_job_requirement(
        self,
        client,
        user2,
        job_requirement1_user1,
    ):

        client.force_login(user2)

        response = client.post(
            reverse(
                "job-requirement-edit-web",
                kwargs={
                    "pk": job_requirement1_user1.id,
                },
            ),
            {
                "title": "Unauthorized Update",
            },
        )

        assert response.status_code == 404

        job_requirement1_user1.refresh_from_db()

        assert job_requirement1_user1.title != "Unauthorized Update"


class TestJobRequirementDeleteView:

    def test_owner_can_open_delete_confirmation(
        self,
        client,
        user1,
        job_requirement1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse(
                "job-requirement-delete-web",
                kwargs={
                    "pk": job_requirement1_user1.id,
                },
            )
        )

        assert response.status_code == 200

        template_names = [t.name for t in response.templates if t.name]
        assert "delete_confirm.html" in template_names

    def test_valid_submission_deletes_job_requirement_and_redirects(
        self,
        client,
        user1,
        job_requirement1_user1,
    ):

        client.force_login(user1)

        pk = job_requirement1_user1.id

        response = client.post(
            reverse(
                "job-requirement-delete-web",
                kwargs={
                    "pk": pk,
                },
            )
        )

        assert response.status_code == 302

        assert not JobRequirement.objects.filter(
            id=pk
        ).exists()

    def test_user_cannot_delete_foreign_job_requirement(
        self,
        client,
        user2,
        job_requirement1_user1,
    ):

        client.force_login(user2)

        pk = job_requirement1_user1.id

        response = client.post(
            reverse(
                "job-requirement-delete-web",
                kwargs={
                    "pk": pk,
                },
            )
        )

        assert response.status_code == 404

        assert JobRequirement.objects.filter(
            id=pk
        ).exists()
