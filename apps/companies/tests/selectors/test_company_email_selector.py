import pytest

from apps.companies.selectors.company_email_selector import CompanyEmailSelector

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
)


@pytest.mark.django_db
class TestCompanyEmailSelectorList:

    def test_list_returns_only_user_owned_emails(
        self,
        user1,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user2,
    ):

        queryset = CompanyEmailSelector.list(user=user1)

        assert set(queryset) == {co_email1_co1_ws1_user1}

    def test_list_without_filters_returns_all_owned_emails(
        self,
        user1,
        co_email1_co1_ws1_user1,
        co_email1_co2_ws1_user1,
    ):

        queryset = CompanyEmailSelector.list(user=user1)

        assert set(queryset) == {
            co_email1_co1_ws1_user1,
            co_email1_co2_ws1_user1,
        }

    def test_list_filters_by_workspace_id(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws2_user1,
    ):

        filters = CompanyEmailSelector.QueryFilter(
            workspace_id=co_email1_co1_ws1_user1.company.workspace.workspace_id,
        )

        queryset = CompanyEmailSelector.list(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {co_email1_co1_ws1_user1}

    def test_list_filters_by_company_id(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co2_ws1_user1,
    ):

        filters = CompanyEmailSelector.QueryFilter(
            company_id=co_email1_co1_ws1_user1.company.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {co_email1_co1_ws1_user1}

    def test_list_filters_by_email_id(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws2_user1,
    ):

        filters = CompanyEmailSelector.QueryFilter(
            id=co_email1_co1_ws1_user1.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {co_email1_co1_ws1_user1}

    def test_list_applies_multiple_filters(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws2_user1,
        co_email1_co2_ws1_user1,
    ):

        filters = CompanyEmailSelector.QueryFilter(
            workspace_id=co_email1_co1_ws1_user1.company.workspace.workspace_id,
            company_id=co_email1_co1_ws1_user1.company.pk,
            id=co_email1_co1_ws1_user1.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert set(queryset) == {co_email1_co1_ws1_user1}

    def test_list_never_returns_foreign_email_even_with_matching_id(
        self,
        user1,
        co_email1_co1_ws1_user2,
    ):

        filters = CompanyEmailSelector.QueryFilter(
            id=co_email1_co1_ws1_user2.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_user_has_no_emails(
        self,
        user1,
    ):

        queryset = CompanyEmailSelector.list(user=user1)

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_filters_match_nothing(
        self,
        co_email1_co1_ws1_user1,
    ):

        filters = CompanyEmailSelector.QueryFilter(
            id=999999,
        )

        queryset = CompanyEmailSelector.list(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_multiple_filters_do_not_match(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws2_user1,
    ):

        filters = CompanyEmailSelector.QueryFilter(
            workspace_id=co_email1_co1_ws1_user1.company.workspace.workspace_id,
            company_id=co_email1_co1_ws2_user1.company.pk,
        )

        queryset = CompanyEmailSelector.list(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            filters=filters,
        )

        assert queryset.count() == 0


@pytest.mark.django_db
class TestCompanyEmailSelectorGet:

    def test_get_returns_email_for_owner(
        self,
        user1,
        co_email1_co1_ws1_user1,
    ):

        company_email = CompanyEmailSelector.get(
            user=user1,
            company_email_id=co_email1_co1_ws1_user1.pk,
        )

        assert company_email == co_email1_co1_ws1_user1

    def test_get_raises_when_email_does_not_exist(
        self,
        user1,
    ):

        with pytest.raises(ResourceNotFoundError):
            CompanyEmailSelector.get(
                user=user1,
                company_email_id=999999,
            )

    def test_get_raises_when_email_belongs_to_another_user(
        self,
        user1,
        co_email1_co1_ws1_user2,
    ):

        with pytest.raises(AccessDeniedError):
            CompanyEmailSelector.get(
                user=user1,
                company_email_id=co_email1_co1_ws1_user2.pk,
            )
