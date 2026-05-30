import pytest

from apps.companies.selectors.company_email_selector import CompanyEmailSelector


@pytest.mark.django_db
class TestCompanyEmailSelector:

    def test_list_returns_only_user_owned_emails(
        self,
        user,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user2,
    ):

        queryset = CompanyEmailSelector.list(user=user)

        assert co_email1_co1_ws1_user1 in queryset
        assert co_email1_co1_ws1_user2 not in queryset
        assert queryset.count() == 1

    def test_list_without_filters_returns_all_owned_emails(
        self,
        user,
        co_email1_co1_ws1_user1,
        co_email1_co2_ws1_user1,
    ):

        queryset = CompanyEmailSelector.list(user=user)

        assert co_email1_co1_ws1_user1 in queryset
        assert co_email1_co2_ws1_user1 in queryset
        assert queryset.count() == 2

    def test_list_filters_by_workspace_id(
        self,
        user,
        workspace_user1,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws2_user1,
    ):

        filters = CompanyEmailSelector.QueryFilter(
            workspace_id=workspace_user1.workspace_id,
        )

        queryset = CompanyEmailSelector.list(
            user=user,
            filters=filters,
        )

        assert co_email1_co1_ws1_user1 in queryset
        assert co_email1_co1_ws2_user1 not in queryset
        assert queryset.count() == 1

    def test_list_filters_by_company_id(
        self,
        user,
        co1_ws1_user1,
        co_email1_co1_ws1_user1,
        co_email1_co2_ws1_user1,
    ):

        filters = CompanyEmailSelector.QueryFilter(
            company_id=co1_ws1_user1.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=user,
            filters=filters,
        )

        assert co_email1_co1_ws1_user1 in queryset
        assert co_email1_co2_ws1_user1 not in queryset
        assert queryset.count() == 1

    def test_list_filters_by_email_id(
        self,
        user,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws2_user1,
    ):

        filters = CompanyEmailSelector.QueryFilter(
            id=co_email1_co1_ws1_user1.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=user,
            filters=filters,
        )

        assert co_email1_co1_ws1_user1 in queryset
        assert co_email1_co1_ws2_user1 not in queryset
        assert queryset.count() == 1

    def test_list_applies_multiple_filters(
        self,
        user,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws2_user1,
        co_email1_co2_ws1_user1
    ):

        filters = CompanyEmailSelector.QueryFilter(
            workspace_id=co_email1_co1_ws1_user1.company.workspace.workspace_id,
            company_id=co_email1_co1_ws1_user1.company.pk,
            id=co_email1_co1_ws1_user1.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=user,
            filters=filters,
        )

        assert list(queryset) == [co_email1_co1_ws1_user1]

    def test_list_never_returns_foreign_email_even_with_matching_id(
        self,
        user,
        co_email1_co1_ws1_user2,
    ):
        filters = CompanyEmailSelector.QueryFilter(
            id=co_email1_co1_ws1_user2.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=user,
            filters=filters,
        )

        assert queryset.count() == 0
