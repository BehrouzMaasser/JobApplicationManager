import pytest

from apps.companies.selectors.company_selector import CompanySelector

from apps.core.exceptions.exceptions import ResourceNotFoundError, AccessDeniedError


@pytest.mark.django_db
class TestCompanySelectorList:

    def test_list_returns_only_user_owned_companies(
        self,
        user1,
        co1_ws1_user1,
        co1_ws1_user2,
    ):

        queryset = set(CompanySelector.list(user=user1))

        assert queryset == {co1_ws1_user1}

    def test_list_without_filters_returns_all_owned_companies(
        self,
        user1,
        co1_ws1_user1,
        co2_ws1_user1,
    ):

        queryset = CompanySelector.list(user=user1)

        assert {co1_ws1_user1, co2_ws1_user1} == set(queryset)

    def test_list_filters_by_workspace_id(
        self,
        co1_ws1_user1,
        co1_ws2_user1,
    ):

        filters = CompanySelector.QueryFilter(
            workspace_id=co1_ws1_user1.workspace.workspace_id,
        )

        queryset = CompanySelector.list(
            user=co1_ws1_user1.workspace.owner,
            filters=filters,
        )

        assert {co1_ws1_user1} == set(queryset)

    def test_list_filters_by_company_id(
        self,
        co1_ws1_user1,
        co2_ws1_user1,
    ):
        filters = CompanySelector.QueryFilter(
            id=co1_ws1_user1.pk,
        )

        queryset = CompanySelector.list(
            user=co1_ws1_user1.workspace.owner,
            filters=filters,
        )

        assert {co1_ws1_user1} == set(queryset)

    def test_list_applies_multiple_filters(
        self,
        co1_ws1_user1,
        co2_ws1_user1,
    ):

        filters = CompanySelector.QueryFilter(
            workspace_id=co1_ws1_user1.workspace.workspace_id,
            id=co1_ws1_user1.pk,
        )

        queryset = CompanySelector.list(
            user=co1_ws1_user1.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {co1_ws1_user1}

    def test_list_never_returns_foreign_company_even_with_matching_id(
        self,
        user1,
        co1_ws1_user2,
    ):

        filters = CompanySelector.QueryFilter(
            id=co1_ws1_user2.pk,
        )

        queryset = CompanySelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_user_has_no_companies(
            self,
            user1,
    ):
        queryset = CompanySelector.list(user=user1)

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_filters_match_nothing(
            self,
            co1_ws1_user1,
    ):
        filters = CompanySelector.QueryFilter(
            id=999999,
        )

        queryset = CompanySelector.list(
            user=co1_ws1_user1.workspace.owner,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_multiple_filters_do_not_match(
            self,
            co1_ws1_user1,
            co1_ws2_user1,
    ):
        filters = CompanySelector.QueryFilter(
            workspace_id=co1_ws1_user1.workspace.workspace_id,
            id=co1_ws2_user1.pk,
        )

        queryset = CompanySelector.list(
            user=co1_ws1_user1.workspace.owner,
            filters=filters,
        )

        assert queryset.count() == 0


@pytest.mark.django_db
class TestCompanySelectorGet:

    def test_get_returns_company_for_owner(
            self,
            user1,
            co1_ws1_user1,
    ):
        company = CompanySelector.get(
            user=user1,
            company_id=co1_ws1_user1.pk,
        )

        assert company == co1_ws1_user1

    def test_get_raises_when_company_does_not_exist(
            self,
            user1,
    ):
        with pytest.raises(ResourceNotFoundError):
            CompanySelector.get(
                user=user1,
                company_id=999999,
            )

    def test_get_raises_when_company_belongs_to_another_user(
            self,
            user1,
            co1_ws1_user2,
    ):
        with pytest.raises(AccessDeniedError):
            CompanySelector.get(
                user=user1,
                company_id=co1_ws1_user2.pk,
            )