import pytest

from django.urls import reverse

from apps.companies.views import company_list_url

pytestmark = pytest.mark.django_db


class TestCompanyListView:

    def test_redirects_anonymous_user(self, client):
        response = client.get(reverse("company-list-web"))

        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_authenticated_user_can_access(self, client, workspace1_user1):
        client.force_login(workspace1_user1.owner)

        response = client.get(
            company_list_url(workspace_id=workspace1_user1.workspace_id)
        )

        assert response.status_code == 200
        assert "companies" in response.context

    def test_list_only_returns_users_companies(
            self,
            client,
            user2,
            co1_ws1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            company_list_url(workspace_id=co1_ws1_user1.workspace.workspace_id)
        )

        assert response.status_code == 200
        assert co1_ws1_user1 not in response.context["companies"]


class TestCompanyCreateView:

    def test_redirects_anonymous_user(
        self,
        client,
        workspace1_user1,
    ):
        response = client.get(
            reverse(
                "company-create-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                },
            )
        )

        assert response.status_code == 302

    def test_get_returns_page(
        self,
        client,
        workspace1_user1,
    ):
        client.force_login(workspace1_user1.owner)

        response = client.get(
            reverse(
                "company-create-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_creates_company(
        self,
        client,
        workspace1_user1,
    ):
        client.force_login(workspace1_user1.owner)

        response = client.post(
            reverse(
                "company-create-web",
                kwargs={
                    "workspace_id": workspace1_user1.workspace_id,
                },
            ),
            {
                "name": "My New Company",
                "website": "https://example.com",
            },
        )

        assert response.status_code == 302

    def test_create_company_invalid_workspace_uuid(
            self,
            client,
            user1,
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "company-create-web",
                kwargs={
                    "workspace_id": "00000000-0000-0000-0000-000000000000",
                },
            ),
            {
                "name": "ACME",
                "website": "",
            },
        )

        assert response.status_code == 404

    def test_create_company_invalid_workspace_id(
            self,
            client,
            user1,
    ):
        client.force_login(user1)

        response = client.post(
            reverse(
                "company-create-web",
                kwargs={
                    "workspace_id": "00000000-0000-0000-0000-000000000000",
                },
            ),
            {
                "name": "ACME",
                "website": "",
            },
        )

        assert response.status_code == 404


class TestCompanyDetailView:

    def test_redirects_anonymous_user(
        self,
        client,
        co1_ws1_user1,
    ):
        response = client.get(
            reverse(
                "company-detail-web",
                kwargs={
                    "pk": co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 302
        assert response.context is None

    def test_authenticated_user_can_access(
        self,
        client,
        co1_ws1_user1,
    ):
        client.force_login(co1_ws1_user1.workspace.owner)

        response = client.get(
            reverse(
                "company-detail-web",
                kwargs={
                    "pk": co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

        assert response.context["company"] == co1_ws1_user1

    def test_user_cannot_view_other_users_company(
            self,
            client,
            user2,
            co1_ws1_user1,
    ):
        client.force_login(user2)

        response = client.get(
            reverse(
                "company-detail-web",
                kwargs={"pk": co1_ws1_user1.pk},
            )
        )

        assert response.status_code == 403


class TestCompanyUpdateView:

    def test_get_returns_page(
        self,
        client,
        co1_ws1_user1,
    ):
        client.force_login(co1_ws1_user1.workspace.owner)

        response = client.get(
            reverse(
                "company-edit-web",
                kwargs={
                    "pk": co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_valid_post_updates_company(
        self,
        client,
        co1_ws1_user1,
    ):
        client.force_login(co1_ws1_user1.workspace.owner)

        response = client.post(
            reverse(
                "company-edit-web",
                kwargs={
                    "pk": co1_ws1_user1.pk,
                },
            ),
            {
                "name": "Updated Company",
                "website": "https://updated.com",
            },
        )

        assert response.status_code == 302

        co1_ws1_user1.refresh_from_db()

        assert co1_ws1_user1.name == "Updated Company"

    def test_user_cannot_update_other_users_company(
            self,
            client,
            user2,
            co1_ws1_user1,
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "company-edit-web",
                kwargs={"pk": co1_ws1_user1.pk},
            ),
            {
                "name": "Hacked",
                "website": "",
            },
        )

        assert response.status_code == 403

        co1_ws1_user1.refresh_from_db()

        assert co1_ws1_user1.name != "Hacked"


class TestCompanyDeleteView:

    def test_get_returns_confirmation(
        self,
        client,
        co1_ws1_user1
    ):
        client.force_login(co1_ws1_user1.workspace.owner)

        response = client.get(
            reverse(
                "company-delete-web",
                kwargs={
                    "pk": co1_ws1_user1.pk,
                },
            )
        )

        assert response.status_code == 200

    def test_post_deletes_company(
        self,
        client,
        co1_ws1_user1
    ):
        client.force_login(co1_ws1_user1.workspace.owner)

        company_pk = co1_ws1_user1.pk

        response = client.post(
            reverse(
                "company-delete-web",
                kwargs={
                    "pk": company_pk,
                },
            )
        )

        assert response.status_code == 302

        from apps.companies.models import Company

        assert not Company.objects.filter(pk=company_pk).exists()

    def test_user_cannot_delete_other_users_company(
            self,
            client,
            user2,
            co1_ws1_user1,
    ):
        client.force_login(user2)

        response = client.post(
            reverse(
                "company-delete-web",
                kwargs={"pk": co1_ws1_user1.pk},
            )
        )

        assert response.status_code == 403

        from apps.companies.models import Company

        assert Company.objects.filter(pk=co1_ws1_user1.pk).exists()
