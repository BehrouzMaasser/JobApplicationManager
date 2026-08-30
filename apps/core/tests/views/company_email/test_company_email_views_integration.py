# apps/core/tests/companies/test_company_email_views_integration.py

import pytest

from django.urls import reverse

from apps.companies.models import CompanyEmail
from apps.companies.views import company_email_list_url


pytestmark = pytest.mark.django_db


class TestCompanyEmailListView:

    def test_redirects_anonymous_user(self, client):

        response = client.get(
            reverse("company-email-list-web")
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
            company_email_list_url(
                company_id=co1_ws1_user1.pk
            )
        )

        assert response.status_code == 200
        assert "emails" in response.context

        # ensure the expected template is used by the presentation layer
        template_names = [t.name for t in response.templates if t.name]
        assert "companies/email/list.html" in template_names

    def test_user_can_see_company_emails(
        self,
        client,
        co_email1_co1_ws1_user1,
    ):

        client.force_login(
            co_email1_co1_ws1_user1.company.workspace.owner
        )

        response = client.get(
            company_email_list_url(
                company_id=co_email1_co1_ws1_user1.company.pk
            )
        )

        assert response.status_code == 200

        assert (
            co_email1_co1_ws1_user1
            in response.context["emails"]
        )

    def test_user_cannot_see_foreign_company_emails(
        self,
        client,
        user2,
        co_email1_co1_ws1_user1,
    ):

        client.force_login(user2)

        response = client.get(
            company_email_list_url(
                company_id=co_email1_co1_ws1_user1.company.pk
            )
        )

        assert response.status_code == 200

        assert (
            co_email1_co1_ws1_user1
            not in response.context["emails"]
        )


class TestCompanyEmailCreateView:

    def test_redirects_anonymous_user(
        self,
        client,
        co1_ws1_user1,
    ):

        response = client.get(
            reverse(
                "company-email-create-web",
                kwargs={
                    "workspace_id":
                        co1_ws1_user1.workspace.workspace_id,
                    "company_id":
                        co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 302

    def test_get_returns_page(
        self,
        client,
        co1_ws1_user1,
    ):

        client.force_login(
            co1_ws1_user1.workspace.owner
        )

        response = client.get(
            reverse(
                "company-email-create-web",
                kwargs={
                    "workspace_id":
                        co1_ws1_user1.workspace.workspace_id,
                    "company_id":
                        co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

        template_names = [t.name for t in response.templates if t.name]
        assert "create_page.html" in template_names

    def test_valid_post_creates_company_email(
        self,
        client,
        co1_ws1_user1,
    ):

        client.force_login(
            co1_ws1_user1.workspace.owner
        )

        response = client.post(
            reverse(
                "company-email-create-web",
                kwargs={
                    "workspace_id":
                        co1_ws1_user1.workspace.workspace_id,
                    "company_id":
                        co1_ws1_user1.pk,
                },
            ),
            {
                "title": "Main Email",
                "email": "main@example.com",
            },
        )

        assert response.status_code == 302

        assert CompanyEmail.objects.filter(
            company=co1_ws1_user1,
            title="Main Email",
            email="main@example.com",
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
                "company-email-create-web",
                kwargs={
                    "workspace_id":
                        workspace1_user1.workspace_id,
                    "company_id":
                        9999999,
                },
            ),
            {
                "title": "Email",
                "email": "email@example.com",
            },
        )

        assert response.status_code == 404

    def test_create_with_foreign_workspace_returns_400(
        self,
        client,
        user1,
        co1_ws1_user1,
    ):

        client.force_login(user1)

        response = client.post(
            reverse(
                "company-email-create-web",
                kwargs={
                    "workspace_id":
                        "00000000-0000-0000-0000-000000000000",
                    "company_id":
                        co1_ws1_user1.pk,
                },
            ),
            {
                "title": "Email",
                "email": "email@example.com",
            },
        )

        assert response.status_code == 400


class TestCompanyEmailDetailView:

    def test_redirects_anonymous_user(
        self,
        client,
        co_email1_co1_ws1_user1,
    ):

        response = client.get(
            reverse(
                "company-email-detail-web",
                kwargs={
                    "pk":
                        co_email1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 302

    def test_owner_can_access(
        self,
        client,
        co_email1_co1_ws1_user1,
    ):

        client.force_login(
            co_email1_co1_ws1_user1.company.workspace.owner
        )

        response = client.get(
            reverse(
                "company-email-detail-web",
                kwargs={
                    "pk":
                        co_email1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

        assert (
            response.context["email"]
            == co_email1_co1_ws1_user1
        )

        template_names = [t.name for t in response.templates if t.name]
        assert "companies/email/detail.html" in template_names

    def test_user_cannot_view_foreign_company_email(
        self,
        client,
        user2,
        co_email1_co1_ws1_user1,
    ):

        client.force_login(user2)

        response = client.get(
            reverse(
                "company-email-detail-web",
                kwargs={
                    "pk":
                        co_email1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 404


class TestCompanyEmailUpdateView:

    def test_get_returns_page(
        self,
        client,
        co_email1_co1_ws1_user1,
    ):

        client.force_login(
            co_email1_co1_ws1_user1.company.workspace.owner
        )

        response = client.get(
            reverse(
                "company-email-edit-web",
                kwargs={
                    "pk":
                        co_email1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_updates_company_email(
        self,
        client,
        co_email1_co1_ws1_user1,
    ):

        client.force_login(
            co_email1_co1_ws1_user1.company.workspace.owner
        )

        response = client.post(
            reverse(
                "company-email-edit-web",
                kwargs={
                    "pk":
                        co_email1_co1_ws1_user1.pk,
                },
            ),
            {
                "title": "Updated",
                "email": "updated@example.com",
            },
        )

        assert response.status_code == 302

        co_email1_co1_ws1_user1.refresh_from_db()

        assert (
            co_email1_co1_ws1_user1.title
            == "Updated"
        )

        assert (
            co_email1_co1_ws1_user1.email
            == "updated@example.com"
        )

    def test_user_cannot_update_foreign_company_email(
        self,
        client,
        user2,
        co_email1_co1_ws1_user1,
    ):

        client.force_login(user2)

        response = client.post(
            reverse(
                "company-email-edit-web",
                kwargs={
                    "pk":
                        co_email1_co1_ws1_user1.pk,
                },
            ),
            {
                "title": "Hacked",
                "email": "hacked@example.com",
            },
        )

        assert response.status_code == 404

        co_email1_co1_ws1_user1.refresh_from_db()

        assert (
            co_email1_co1_ws1_user1.title
            != "Hacked"
        )


class TestCompanyEmailDeleteView:

    def test_get_returns_confirmation(
        self,
        client,
        co_email1_co1_ws1_user1,
    ):

        client.force_login(
            co_email1_co1_ws1_user1.company.workspace.owner
        )

        response = client.get(
            reverse(
                "company-email-delete-web",
                kwargs={
                    "pk":
                        co_email1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_post_deletes_company_email(
        self,
        client,
        co_email1_co1_ws1_user1,
    ):

        client.force_login(
            co_email1_co1_ws1_user1.company.workspace.owner
        )

        email_id = co_email1_co1_ws1_user1.pk

        response = client.post(
            reverse(
                "company-email-delete-web",
                kwargs={
                    "pk": email_id,
                },
            )
        )

        assert response.status_code == 302

        assert not CompanyEmail.objects.filter(
            pk=email_id
        ).exists()

    def test_user_cannot_delete_foreign_company_email(
        self,
        client,
        user2,
        co_email1_co1_ws1_user1,
    ):

        client.force_login(user2)

        response = client.post(
            reverse(
                "company-email-delete-web",
                kwargs={
                    "pk":
                        co_email1_co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 404

        assert CompanyEmail.objects.filter(
            pk=co_email1_co1_ws1_user1.pk
        ).exists()
