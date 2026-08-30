# Job Task integration tests audit:
# - Added a duplicate-create integration assertion to ensure the web form
#   surface reflects the same business validation as the API (no duplicate
#   tasks can be created for the same user).
# - Kept changes minimal and consistent with existing test style.
import pytest

from django.urls import reverse

from apps.companies.models import JobTask
pytestmark = pytest.mark.django_db


class TestJobTaskListView:

    def test_anonymous_user_is_redirected_to_login(self, client):

        response = client.get(
            reverse("job-task-list-web")
        )

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access_view(
        self,
        client,
        user1,
        job_task1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse("job-task-list-web")
        )

        assert response.status_code == 200
        assert "job_tasks" in response.context

        template_names = [t.name for t in response.templates if t.name]
        assert "accounts/job_task/list.html" in template_names

    def test_user_only_sees_owned_job_tasks(
        self,
        client,
        user2,
        job_task1_user1,
    ):

        client.force_login(user2)

        response = client.get(
            reverse("job-task-list-web")
        )

        assert response.status_code == 200

        assert job_task1_user1 not in response.context["job_tasks"]


class TestJobTaskCreateView:

    def test_anonymous_user_is_redirected(
        self,
        client,
    ):

        response = client.get(
            reverse("job-task-create-web")
        )

        assert response.status_code == 302

    def test_authenticated_user_can_open_create_page(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse("job-task-create-web")
        )

        assert response.status_code == 200

        template_names = [t.name for t in response.templates if t.name]
        assert "create_page.html" in template_names

    def test_valid_submission_creates_job_task_and_redirects(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse("job-task-create-web"),
            {
                "title": "New Task",
                "description": "Some Description",
            },
        )

        assert response.status_code == 302

        assert response.url == reverse(
            "job-task-list-web"
        )

        assert JobTask.objects.filter(
            user=user1,
            title="New Task",
        ).exists()

    def test_duplicate_submission_shows_form_errors(
        self,
        client,
        user1,
        job_task1_user1,
    ):
        """
        Submitting a create form with the same title/description for the same
        user should render the form with errors and not create a duplicate.
        """
        client.force_login(user1)

        response = client.post(
            reverse("job-task-create-web"),
            {
                "title": job_task1_user1.title,
                "description": job_task1_user1.description,
            },
        )

        assert response.status_code == 200

        assert response.context["form"].errors

        # Ensure no duplicate was created
        assert JobTask.objects.filter(
            user=user1,
            title=job_task1_user1.title
        ).count() == 1

    def test_invalid_submission_renders_form_errors(
        self,
        client,
        user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse("job-task-create-web"),
            {
                "title": "",
            },
        )

        assert response.status_code == 200

        assert response.context["form"].errors

        template_names = [t.name for t in response.templates if t.name]
        assert "create_page.html" in template_names


class TestJobTaskDetailView:

    def test_anonymous_user_is_redirected(
        self,
        client,
        job_task1_user1,
    ):

        response = client.get(
            reverse(
                "job-task-detail-web",
                kwargs={
                    "pk": job_task1_user1.id,
                },
            )
        )

        assert response.status_code == 302

    def test_owner_can_view_job_task(
        self,
        client,
        user1,
        job_task1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse(
                "job-task-detail-web",
                kwargs={
                    "pk": job_task1_user1.id,
                },
            )
        )

        assert response.status_code == 200

        assert response.context["job_task"] == job_task1_user1

        template_names = [t.name for t in response.templates if t.name]
        assert "accounts/job_task/detail.html" in template_names

    def test_user_cannot_view_foreign_job_task(
        self,
        client,
        user2,
        job_task1_user1,
    ):

        client.force_login(user2)

        response = client.get(
            reverse(
                "job-task-detail-web",
                kwargs={
                    "pk": job_task1_user1.id,
                },
            )
        )

        assert response.status_code == 404


class TestJobTaskUpdateView:

    def test_owner_can_open_update_page(
        self,
        client,
        user1,
        job_task1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse(
                "job-task-edit-web",
                kwargs={
                    "pk": job_task1_user1.id,
                },
            )
        )

        assert response.status_code == 200

        template_names = [t.name for t in response.templates if t.name]
        assert "edit_page.html" in template_names

    def test_valid_submission_updates_job_task_and_redirects(
        self,
        client,
        user1,
        job_task1_user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse(
                "job-task-edit-web",
                kwargs={
                    "pk": job_task1_user1.id,
                },
            ),
            {
                "title": "Updated Task",
                "description": "Updated",
            },
        )

        assert response.status_code == 302

        job_task1_user1.refresh_from_db()

        assert job_task1_user1.title == "Updated Task"

    def test_invalid_submission_renders_form_errors(
        self,
        client,
        user1,
        job_task1_user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse(
                "job-task-edit-web",
                kwargs={
                    "pk": job_task1_user1.id,
                },
            ),
            {
                "title": "",
            },
        )

        assert response.status_code == 200

        assert response.context["form"].errors

    def test_user_cannot_update_foreign_job_task(
        self,
        client,
        user2,
        job_task1_user1,
    ):

        client.force_login(user2)

        response = client.post(
            reverse(
                "job-task-edit-web",
                kwargs={
                    "pk": job_task1_user1.id,
                },
            ),
            {
                "title": "Unauthorized Update",
            },
        )

        assert response.status_code == 404

        job_task1_user1.refresh_from_db()

        assert job_task1_user1.title != "Unauthorized Update"


class TestJobTaskDeleteView:

    def test_owner_can_open_delete_confirmation(
        self,
        client,
        user1,
        job_task1_user1,
    ):

        client.force_login(user1)

        response = client.get(
            reverse(
                "job-task-delete-web",
                kwargs={
                    "pk": job_task1_user1.id,
                },
            )
        )

        assert response.status_code == 200

        template_names = [t.name for t in response.templates if t.name]
        assert "delete_confirm.html" in template_names

    def test_valid_submission_deletes_job_task_and_redirects(
        self,
        client,
        job_task1_user1,
    ):

        client.force_login(job_task1_user1.user)

        pk = job_task1_user1.id

        response = client.post(
            reverse(
                "job-task-delete-web",
                kwargs={
                    "pk": pk,
                },
            )
        )

        assert response.status_code == 302

        assert not JobTask.objects.filter(
            id=pk
        ).exists()

    def test_user_cannot_delete_foreign_job_task(
        self,
        client,
        user2,
        job_task1_user1,
    ):

        client.force_login(user2)

        pk = job_task1_user1.id

        response = client.post(
            reverse(
                "job-task-delete-web",
                kwargs={
                    "pk": pk,
                },
            )
        )

        assert response.status_code == 404

        assert JobTask.objects.filter(
            id=pk
        ).exists()
