import pytest

from apps.companies.selectors.company_selector import CompanySelector


@pytest.mark.django_db
class TestCompanySelector:

    def test_list_returns_only_user_owned_companies(
        self,
        user,
        co1_ws1_user1,
        co1_ws1_user2,
    ):

        queryset = CompanySelector.list(user=user)

        assert co1_ws1_user1 in queryset
        assert co1_ws1_user2 not in queryset
        assert queryset.count() == 1

    def test_list_without_filters_returns_all_owned_companies(
        self,
        user,
        co1_ws1_user1,
        co2_ws1_user1,
    ):

        queryset = CompanySelector.list(user=user)

        assert co1_ws1_user1 in queryset
        assert co2_ws1_user1 in queryset
        assert queryset.count() == 2

    def test_list_filters_by_workspace_id(
        self,
        user,
        workspace_user1,
        co1_ws1_user1,
        co1_ws2_user1,
    ):

        filters = CompanySelector.QueryFilter(
            workspace_id=workspace_user1.workspace_id,
        )

        queryset = CompanySelector.list(
            user=user,
            filters=filters,
        )

        assert co1_ws1_user1 in queryset
        assert co1_ws2_user1 not in queryset
        assert queryset.count() == 1

    def test_list_filters_by_company_id(
        self,
        user,
        co1_ws1_user1,
        co2_ws1_user1,
    ):
        filters = CompanySelector.QueryFilter(
            id=co1_ws1_user1.pk,
        )

        queryset = CompanySelector.list(
            user=user,
            filters=filters,
        )

        assert co1_ws1_user1 in queryset
        assert co2_ws1_user1 not in queryset
        assert queryset.count() == 1

    def test_list_applies_multiple_filters(
        self,
        user,
        co1_ws1_user1,
        co2_ws1_user1,
    ):

        filters = CompanySelector.QueryFilter(
            workspace_id=co1_ws1_user1.workspace.workspace_id,
            id=co1_ws1_user1.pk,
        )

        queryset = CompanySelector.list(
            user=user,
            filters=filters,
        )

        assert list(queryset) == [co1_ws1_user1]

    def test_list_never_returns_foreign_company_even_with_matching_id(
        self,
        user,
        co1_ws1_user2,
    ):

        filters = CompanySelector.QueryFilter(
            id=co1_ws1_user2.pk,
        )

        queryset = CompanySelector.list(
            user=user,
            filters=filters,
        )

        assert queryset.count() == 0
